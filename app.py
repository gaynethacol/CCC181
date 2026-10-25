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

# Fictional sample data for local testing.
TICKETS = [
    {
        "number": 1,
        "name": "Ana",
        "contact_number": "09000000001",
        "service_id": 1,
        "status": "waiting",
    },
    {
        "number": 2,
        "name": "Ben",
        "contact_number": "09000000002",
        "service_id": 2,
        "status": "waiting",
    },
]


@app.route("/")
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
    })

    flash(
        f"You joined the queue. Your ticket is #{number}.",
        "success",
    )

    return redirect(url_for("ticket", ticket_id=number))


@app.route("/staff")
def staff_dashboard():
    return render_template("staff.html")


@app.route("/queue/<int:ticket_id>")
def ticket(ticket_id):
    if not any(item["number"] == ticket_id for item in TICKETS):
        abort(404)

    return render_template("ticket.html", ticket_id=ticket_id)


@app.route("/hello")
def hello():
    return "Hello, LicenseQ!"


if __name__ == "__main__":
    app.run(debug=True)