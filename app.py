"""CCC181 Week 2: a "Hello, Flask" starter app.

Run it with:
    flask --app app run --debug
then open http://127.0.0.1:5000
"""
from flask import Flask, render_template

app = Flask(__name__)

# Sample data for the demo. A real app would load this from a database later.
SERVICES = [
    {"id": 1, "name": "Application and Testing"},
    {"id": 2, "name": "Printed-Card Collection"},
]

# Fictional data for testing only.
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
    return render_template(
        "index.html",
        tickets=TICKETS,
        services=SERVICES,
    )


@app.route("/queue/<int:ticket_id>")
def ticket(ticket_id):
    # <int:ticket_id> only matches numbers, so /queue/abc returns 404.
    return render_template("ticket.html", ticket_id=ticket_id)


@app.route("/hello")
def hello():
    # The plain-string version from the Routes slide.
    return "Hello, CCC181!"


if __name__ == "__main__":
    # Lets you also start the app with: python app.py
    app.run(debug=True)
