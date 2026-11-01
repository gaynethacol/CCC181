"""Add initial LicenseQ services without duplicating them."""

from sqlalchemy import select

from app import app
from models import db, Service


# Placeholder durations for the prototype, not measured waiting times.
INITIAL_SERVICES = [
    {"name": "Application and Testing", "avg_minutes": 30},
    {"name": "Printed-Card Collection", "avg_minutes": 5},
]


with app.app_context():
    added = 0

    for details in INITIAL_SERVICES:
        existing = db.session.scalar(
            select(Service).where(Service.name == details["name"])
        )

        if existing is None:
            db.session.add(Service(**details))
            added += 1

    db.session.commit()
    print(f"Seeding complete. Added {added} service(s).")