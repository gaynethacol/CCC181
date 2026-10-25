"""LicenseQ: a student driver's licensing queue prototype."""

from flask import (
    Flask, abort, flash, redirect,
    render_template, request, url_for
)

app = Flask(__name__)
app.secret_key = "dev-only-change-me"

SERVICES = [
    {"id": 1, "name": "Application and Testing"},
    {"id": 2, "name": "Printed-Card Collection"},
]

# Tickets reset whenever the server restarts.
TICKETS = []


def queue_order(item):
    return item.get("queue_order", item["number"])


def next_queue_order():
    return max(
        (queue_order(item) for item in TICKETS),
        default=0,
    ) + 1


def find_ticket(ticket_id):
    current = next(
        (item for item in TICKETS if item["number"] == ticket_id),
        None,
    )

    if current is None:
        abort(404)

    return current


def selected_service(raw_value):
    if raw_value in (None, ""):
        return None

    try:
        service_id = int(raw_value)
    except (TypeError, ValueError):
        abort(400)

    if service_id not in [service["id"] for service in SERVICES]:
        abort(400)

    return service_id


def people_ahead(current):
    return sum(
        1 for item in TICKETS
        if item["service_id"] == current["service_id"]
        and item["status"] == "waiting"
        and queue_order(item) < queue_order(current)
    )


def ticket_service(current):
    return next(
        service for service in SERVICES
        if service["id"] == current["service_id"]
    )


@app.get("/")
def index():
    return render_template("index.html")


@app.get("/join")
def join_form():
    return render_template(
        "join.html",
        services=SERVICES,
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

    if service_id not in [service["id"] for service in SERVICES]:
        errors["service_id"] = "Choose a queue."

    if errors:
        flash("Please fix the highlighted fields.", "danger")

        return render_template(
            "join.html",
            services=SERVICES,
            form=form,
            errors=errors,
        ), 400

    number = max(
        (item["number"] for item in TICKETS),
        default=0,
    ) + 1

    TICKETS.append({
        "number": number,
        "name": name,
        "contact_number": contact_number,
        "service_id": service_id,
        "status": "waiting",
        "queue_order": next_queue_order(),
    })

    flash(
        f"You joined the queue. Your ticket is #{number}.",
        "success",
    )

    return redirect(url_for("ticket", ticket_id=number))


@app.get("/queue/<int:ticket_id>")
def ticket(ticket_id):
    current = find_ticket(ticket_id)

    return render_template(
        "ticket.html",
        ticket=current,
        service=ticket_service(current),
        ahead=people_ahead(current),
    )


@app.get("/queue/<int:ticket_id>/status.json")
def ticket_status(ticket_id):
    current = find_ticket(ticket_id)
    service = ticket_service(current)

    return {
        "status": current["status"],
        "ahead": people_ahead(current),
        "service": service["name"],
    }


@app.post("/queue/<int:ticket_id>/leave")
def leave_queue(ticket_id):
    current = find_ticket(ticket_id)

    if current["status"] not in ("waiting", "called"):
        flash(
            "This ticket is no longer in the active queue.",
            "warning",
        )
        return redirect(url_for("ticket", ticket_id=ticket_id))

    current["status"] = "no-show"

    flash(
        f"You left the queue. Ticket #{ticket_id} is no longer active.",
        "success",
    )

    return redirect(url_for("index"))


@app.get("/staff")
def staff_dashboard():
    service_id = selected_service(
        request.args.get("service_id")
    )

    queue = [
        item for item in TICKETS
        if item["status"] in ("waiting", "called")
        and (
            service_id is None
            or item["service_id"] == service_id
        )
    ]

    queue.sort(key=queue_order)

    return render_template(
        "staff.html",
        queue=queue,
        services=SERVICES,
        names={service["id"]: service["name"] for service in SERVICES},
        selected=service_id,
        can_call=(
            any(item["status"] == "waiting" for item in queue)
            and not any(item["status"] == "called" for item in queue)
        ),
    )


@app.post("/staff/call-next")
def call_next():
    service_id = selected_service(
        request.form.get("service_id")
    )

    queue = [
        item for item in TICKETS
        if service_id is None or item["service_id"] == service_id
    ]

    if any(item["status"] == "called" for item in queue):
        flash("Resolve the currently called ticket first.", "warning")
    else:
        waiting = [
            item for item in queue
            if item["status"] == "waiting"
        ]

        if waiting:
            current = min(waiting, key=queue_order)
            current["status"] = "called"

            flash(
                f"Calling ticket #{current['number']}.",
                "info",
            )
        else:
            flash("No applicants are waiting in this queue.", "info")

    return redirect(
        url_for("staff_dashboard", service_id=service_id)
    )


@app.post("/staff/tickets/<int:ticket_id>/<action>")
def staff_action(ticket_id, action):
    if action not in ("call", "serve", "no-show", "requeue", "transfer"):
        abort(404)

    current = find_ticket(ticket_id)

    service_id = selected_service(
        request.form.get("service_id")
    )

    def back():
        return redirect(
            url_for("staff_dashboard", service_id=service_id)
        )

    if current["status"] not in ("waiting", "called"):
        flash("This ticket is no longer active.", "warning")
        return back()

    if action == "call":
        if current["status"] != "waiting":
            flash("This ticket has already been called.", "warning")
            return back()

        same_queue = [
            item for item in TICKETS
            if item["service_id"] == current["service_id"]
        ]

        if any(item["status"] == "called" for item in same_queue):
            flash(
                "Resolve the called ticket in this queue first.",
                "warning",
            )
            return back()

        first = min(
            (
                item for item in same_queue
                if item["status"] == "waiting"
            ),
            key=queue_order,
        )

        if first["number"] != ticket_id:
            flash("Call the first waiting applicant first.", "warning")
            return back()

        current["status"] = "called"
        flash(f"Calling ticket #{ticket_id}.", "info")

    elif action in ("serve", "no-show"):
        if current["status"] != "called":
            flash(
                "Call this applicant before updating the outcome.",
                "warning",
            )
            return back()

        current["status"] = (
            "served" if action == "serve" else "no-show"
        )

        flash(
            f"Ticket #{ticket_id} marked {current['status']}.",
            "info",
        )

    elif action == "requeue":
        if current["status"] != "called":
            flash(
                "Only a called applicant can be moved to the end.",
                "warning",
            )
            return back()

        if request.form.get("confirm") != "yes":
            flash("Confirm the move before continuing.", "warning")
            return back()

        current["queue_order"] = next_queue_order()
        current["status"] = "waiting"

        flash(
            f"Ticket #{ticket_id} moved to the end of its queue.",
            "info",
        )

    elif action == "transfer":
        if current["service_id"] != 1 or current["status"] != "called":
            flash(
                "Call an application-stage ticket before transferring.",
                "warning",
            )
            return back()

        if request.form.get("confirm") != "yes":
            flash(
                "Confirm eligibility before transferring.",
                "warning",
            )
            return back()

        current["queue_order"] = next_queue_order()
        current["service_id"] = 2
        current["status"] = "waiting"

        flash(
            f"Ticket #{ticket_id} transferred to card collection.",
            "success",
        )

    return back()


@app.get("/hello")
def hello():
    return "Hello, LicenseQ!"


if __name__ == "__main__":
    app.run(debug=True)