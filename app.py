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


@app.route("/join")
def join_form():
    return render_template("join.html")


@app.route("/staff")
def staff_dashboard():
    return render_template("staff.html")


@app.route("/queue/<int:ticket_id>")
def ticket(ticket_id):
    return render_template("ticket.html", ticket_id=ticket_id)


@app.route("/hello")
def hello():
    return "Hello, LicenseQ!"


if __name__ == "__main__":
    app.run(debug=True)