"""LicenseQ: a driver's licensing queue prototype."""

import os
from datetime import datetime, timezone
from zoneinfo import ZoneInfo

from dotenv import load_dotenv
from flask import (
    Flask, abort, flash, redirect,
    render_template, request, url_for,
)
from flask_migrate import Migrate
from sqlalchemy import and_, func, or_, select
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import joinedload

from models import db, User, Service, Ticket


load_dotenv()

app = Flask(__name__)
app.secret_key = "dev-only-change-me"

app.config["SQLALCHEMY_DATABASE_URI"] = os.environ["DATABASE_URL"]
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

db.init_app(app)
migrate = Migrate(app, db)

APPLICATION_SERVICE_ID = 1
CARD_COLLECTION_SERVICE_ID = 2


@app.template_filter("manila_time")
def manila_time(value):
    if value is None:
        return "—"

    return value.astimezone(
        ZoneInfo("Asia/Manila")
    ).strftime("%b %d, %Y · %I:%M %p")


def all_services(active_only=False):
    statement = select(Service).order_by(Service.id)

    if active_only:
        statement = statement.where(Service.active.is_(True))

    return db.session.scalars(statement).all()


def find_ticket(ticket_id):
    return db.get_or_404(Ticket, ticket_id)


def selected_service(raw_value):
    if raw_value in (None, ""):
        return None

    try:
        service_id = int(raw_value)
    except (TypeError, ValueError):
        abort(400)

    if db.session.get(Service, service_id) is None:
        abort(400)

    return service_id


def people_ahead(current):
    return db.session.scalar(
        select(func.count(Ticket.id)).where(
            Ticket.service_id == current.service_id,
            Ticket.status == "waiting",
            or_(
                Ticket.queued_at < current.queued_at,
                and_(
                    Ticket.queued_at == current.queued_at,
                    Ticket.id < current.id,
                ),
            ),
        )
    )


def first_waiting(service_id=None):
    statement = select(Ticket).where(
        Ticket.status == "waiting"
    )

    if service_id is not None:
        statement = statement.where(
            Ticket.service_id == service_id
        )

    return db.session.scalar(
        statement.order_by(
            Ticket.queued_at,
            Ticket.id,
        ).limit(1)
    )


def has_called(service_id=None):
    statement = select(Ticket.id).where(
        Ticket.status == "called"
    )

    if service_id is not None:
        statement = statement.where(
            Ticket.service_id == service_id
        )

    return db.session.scalar(statement.limit(1)) is not None


def lock_queue_changes():
    db.session.scalars(
        select(Service)
        .order_by(Service.id)
        .with_for_update()
    ).all()


def save_change():
    try:
        db.session.commit()
        return True
    except IntegrityError:
        db.session.rollback()
        flash(
            "The change could not be saved. Refresh and try again.",
            "danger",
        )
        return False


@app.get("/")
def index():
    return render_template("index.html")


@app.get("/join")
def join_form():
    return render_template(
        "join.html",
        services=all_services(active_only=True),
        form={},
        errors={},
    )


@app.post("/join")
def join():
    form = request.form

    name = form.get("name", "").strip()
    contact_number = form.get("contact_number", "").strip()
    service_id = form.get("service_id", type=int)

    errors = {}

    if not name:
        errors["name"] = "Enter your full name."
    elif len(name) > 100:
        errors["name"] = "Use 100 characters or fewer."

    if not (
        len(contact_number) == 11
        and contact_number.isascii()
        and contact_number.isdigit()
        and contact_number.startswith("09")
    ):
        errors["contact_number"] = (
            "Enter an 11-digit mobile number starting with 09."
        )

    # Serialize joins to the same service before checking duplicates.
    service = (
        db.session.scalar(
            select(Service)
            .where(Service.id == service_id)
            .with_for_update()
        )
        if service_id is not None
        else None
    )

    if service is None or not service.active:
        errors["service_id"] = "Choose an available queue."

    if errors:
        db.session.rollback()
        flash("Please fix the highlighted fields.", "danger")

        return render_template(
            "join.html",
            services=all_services(active_only=True),
            form=form,
            errors=errors,
        ), 400

    # Reopen an existing waiting or called ticket for the same details.
    existing = db.session.scalar(
        select(Ticket)
        .join(Ticket.user)
        .where(
            Ticket.service_id == service_id,
            Ticket.status.in_(("waiting", "called")),
            func.lower(User.name) == func.lower(name),
            User.contact_number == contact_number,
        )
        .order_by(Ticket.id)
        .limit(1)
    )

    if existing is not None:
        existing_id = existing.id
        db.session.rollback()

        flash(
            f"You already have an active ticket for this queue: "
            f"#{existing_id}.",
            "info",
        )

        return redirect(
            url_for("ticket", ticket_id=existing_id)
        )

    applicant = User(
        name=name,
        contact_number=contact_number,
    )

    current = Ticket(
        user=applicant,
        service=service,
        status="waiting",
    )

    db.session.add(current)

    try:
        db.session.commit()
    except IntegrityError:
        db.session.rollback()
        flash(
            "Your ticket could not be saved. Check your details and retry.",
            "danger",
        )

        return render_template(
            "join.html",
            services=all_services(active_only=True),
            form=form,
            errors={},
        ), 409

    flash(
        f"You joined the queue. Your ticket is #{current.id}.",
        "success",
    )

    return redirect(
        url_for("ticket", ticket_id=current.id)
    )


@app.get("/queue/<int:ticket_id>")
def ticket(ticket_id):
    current = find_ticket(ticket_id)

    return render_template(
        "ticket.html",
        ticket=current,
        service=current.service,
        ahead=people_ahead(current),
    )


@app.get("/queue/<int:ticket_id>/status.json")
def ticket_status(ticket_id):
    current = find_ticket(ticket_id)

    return {
        "status": current.status,
        "ahead": people_ahead(current),
        "service": current.service.name,
    }, 200, {"Cache-Control": "no-store"}


@app.post("/queue/<int:ticket_id>/leave")
def leave_queue(ticket_id):
    lock_queue_changes()
    current = find_ticket(ticket_id)

    if current.status != "waiting":
        db.session.rollback()
        flash(
            "Only a waiting ticket can leave the queue.",
            "warning",
        )
        return redirect(
            url_for("ticket", ticket_id=ticket_id)
        )

    current.status = "left"

    if save_change():
        flash(
            f"You left the queue. Ticket #{ticket_id} is no longer active.",
            "success",
        )
        return redirect(url_for("index"))

    return redirect(
        url_for("ticket", ticket_id=ticket_id)
    )


@app.get("/staff")
def staff_dashboard():
    service_id = selected_service(
        request.args.get("service_id")
    )

    statement = (
        select(Ticket)
        .options(
            joinedload(Ticket.user),
            joinedload(Ticket.service),
        )
        .where(Ticket.status.in_(("waiting", "called")))
    )

    if service_id is not None:
        statement = statement.where(
            Ticket.service_id == service_id
        )

    queue = db.session.scalars(
        statement.order_by(
            Ticket.queued_at,
            Ticket.id,
        )
    ).all()

    services = all_services()

    return render_template(
        "staff.html",
        queue=queue,
        services=services,
        names={
            service.id: service.name
            for service in services
        },
        selected=service_id,
        application_service_id=APPLICATION_SERVICE_ID,
        can_call=(
            any(item.status == "waiting" for item in queue)
            and not any(item.status == "called" for item in queue)
        ),
    )


@app.post("/staff/call-next")
def call_next():
    service_id = selected_service(
        request.form.get("service_id")
    )

    lock_queue_changes()

    if has_called(service_id):
        db.session.rollback()
        flash(
            "Resolve the currently called ticket first.",
            "warning",
        )
    else:
        current = first_waiting(service_id)

        if current is None:
            db.session.rollback()
            flash(
                "No applicants are waiting in this queue.",
                "info",
            )
        else:
            current.status = "called"
            current.called_at = datetime.now(timezone.utc)

            if save_change():
                flash(
                    f"Calling ticket #{current.id}.",
                    "info",
                )

    return redirect(
        url_for("staff_dashboard", service_id=service_id)
    )


@app.post("/staff/tickets/<int:ticket_id>/<action>")
def staff_action(ticket_id, action):
    if action not in (
        "call", "serve", "no-show", "requeue", "transfer"
    ):
        abort(404)

    service_id = selected_service(
        request.form.get("service_id")
    )

    lock_queue_changes()
    current = find_ticket(ticket_id)

    def back():
        return redirect(
            url_for("staff_dashboard", service_id=service_id)
        )

    def reject(message):
        db.session.rollback()
        flash(message, "warning")
        return back()

    if current.status not in ("waiting", "called"):
        return reject("This ticket is no longer active.")

    if action == "call":
        if current.status != "waiting":
            return reject("This ticket has already been called.")

        if has_called(current.service_id):
            return reject(
                "Resolve the called ticket in this queue first."
            )

        first = first_waiting(current.service_id)

        if first is None or first.id != current.id:
            return reject("Call the first waiting applicant first.")

        current.status = "called"
        current.called_at = datetime.now(timezone.utc)
        message = f"Calling ticket #{ticket_id}."

    elif action in ("serve", "no-show"):
        if current.status != "called":
            return reject(
                "Call this applicant before updating the outcome."
            )

        current.status = (
            "served" if action == "serve" else "no-show"
        )

        if action == "serve":
            current.served_at = datetime.now(timezone.utc)

        message = f"Ticket #{ticket_id} marked {current.status}."

    elif action == "requeue":
        if current.status != "called":
            return reject(
                "Only a called applicant can be moved to the end."
            )

        if request.form.get("confirm") != "yes":
            return reject("Confirm the move before continuing.")

        current.queued_at = datetime.now(timezone.utc)
        current.called_at = None
        current.served_at = None
        current.status = "waiting"

        message = (
            f"Ticket #{ticket_id} moved to the end of its queue."
        )

    else:
        if (
            current.service_id != APPLICATION_SERVICE_ID
            or current.status != "called"
        ):
            return reject(
                "Call an application-stage ticket before transferring."
            )

        if request.form.get("confirm") != "yes":
            return reject(
                "Confirm eligibility before transferring."
            )

        destination = db.session.get(
            Service, CARD_COLLECTION_SERVICE_ID
        )

        if destination is None or not destination.active:
            return reject(
                "The printed-card collection queue is unavailable."
            )

        current.service = destination
        current.queued_at = datetime.now(timezone.utc)
        current.called_at = None
        current.served_at = None
        current.status = "waiting"

        message = (
            f"Ticket #{ticket_id} transferred to card collection."
        )

    if save_change():
        flash(message, "info")

    return back()


@app.post("/staff/tickets/<int:ticket_id>/delete")
def delete_ticket(ticket_id):
    service_id = selected_service(
        request.form.get("service_id")
    )

    if request.form.get("confirm") != "yes":
        flash(
            "Confirm ticket deletion before continuing.",
            "warning",
        )
        return redirect(
            url_for("staff_dashboard", service_id=service_id)
        )

    lock_queue_changes()
    current = find_ticket(ticket_id)

    db.session.delete(current)

    if save_change():
        flash(
            f"Ticket #{ticket_id} permanently deleted.",
            "success",
        )

    return redirect(
        url_for("staff_dashboard", service_id=service_id)
    )


def service_form_values():
    name = request.form.get("name", "").strip()
    avg_minutes = request.form.get("avg_minutes", type=int)

    if not name or len(name) > 100:
        return None, None, "Enter a service name of 1–100 characters."

    if avg_minutes is None or not 1 <= avg_minutes <= 2147483647:
        return None, None, "Enter a positive whole number for minutes."

    return name, avg_minutes, None


def render_services(form=None, editing=None, status=200):
    ticket_counts = dict(
        db.session.execute(
            select(
                Ticket.service_id,
                func.count(Ticket.id),
            ).group_by(Ticket.service_id)
        ).all()
    )

    return render_template(
        "services.html",
        services=all_services(),
        ticket_counts=ticket_counts,
        form=form or {},
        editing=editing,
    ), status


@app.get("/staff/services")
def manage_services():
    return render_services()


@app.post("/staff/services")
def create_service():
    name, avg_minutes, error = service_form_values()

    if error:
        flash(error, "danger")
        return render_services(
            form=request.form,
            status=400,
        )

    db.session.add(
        Service(
            name=name,
            avg_minutes=avg_minutes,
            active=True,
        )
    )

    try:
        db.session.commit()
    except IntegrityError:
        db.session.rollback()
        flash(
            "A service with that name already exists.",
            "danger",
        )
        return render_services(
            form=request.form,
            status=409,
        )

    flash("Service created.", "success")
    return redirect(url_for("manage_services"))


@app.post("/staff/services/<int:service_id>/<action>")
def manage_service_action(service_id, action):
    if action not in ("edit", "toggle", "delete"):
        abort(404)

    lock_queue_changes()
    service = db.get_or_404(Service, service_id)

    if action == "edit":
        name, avg_minutes, error = service_form_values()

        if error:
            db.session.rollback()
            flash(error, "danger")
            return render_services(
                form=request.form,
                editing=service_id,
                status=400,
            )

        service.name = name
        service.avg_minutes = avg_minutes
        message = "Service updated."

    elif action == "toggle":
        service.active = not service.active

        message = (
            "Service activated."
            if service.active
            else "Service deactivated. Existing tickets are retained."
        )

    else:
        if request.form.get("confirm") != "yes":
            db.session.rollback()
            flash(
                "Confirm deletion before continuing.",
                "warning",
            )
            return redirect(url_for("manage_services"))

        has_tickets = db.session.scalar(
            select(Ticket.id)
            .where(Ticket.service_id == service_id)
            .limit(1)
        )

        if has_tickets is not None:
            db.session.rollback()
            flash(
                "This service has tickets. Deactivate it instead.",
                "warning",
            )
            return redirect(url_for("manage_services"))

        db.session.delete(service)
        message = "Unused service deleted."

    try:
        db.session.commit()
    except IntegrityError:
        db.session.rollback()
        flash(
            "Unable to save. The name may already exist, "
            "or the service may have linked tickets.",
            "danger",
        )
        return render_services(
            form=request.form,
            editing=service_id if action == "edit" else None,
            status=409,
        )

    flash(message, "success")
    return redirect(url_for("manage_services"))


@app.get("/hello")
def hello():
    return "Hello, LicenseQ!"


if __name__ == "__main__":
    app.run(debug=True)