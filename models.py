"""Database models for LicenseQ."""

from datetime import datetime

from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import CheckConstraint, ForeignKey, UniqueConstraint, func
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship


class Base(DeclarativeBase):
    pass


db = SQLAlchemy(model_class=Base)


class User(db.Model):
    __tablename__ = "users"

    __table_args__ = (
        CheckConstraint(
            "length(btrim(name)) > 0",
            name="ck_users_name_not_blank",
        ),
        CheckConstraint(
            "contact_number ~ '^09[0-9]{9}$'",
            name="ck_users_contact_number_format",
        ),
    )

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(db.String(100), nullable=False)

    contact_number: Mapped[str] = mapped_column(
        db.String(11),
        nullable=False,
    )

    created_at: Mapped[datetime] = mapped_column(
        db.DateTime(timezone=True),
        nullable=False,
        server_default=func.now(),
    )

    tickets: Mapped[list["Ticket"]] = relationship(
        back_populates="user",
        passive_deletes="all",
    )


class Service(db.Model):
    __tablename__ = "services"

    __table_args__ = (
        UniqueConstraint("name", name="uq_services_name"),
        CheckConstraint(
            "length(btrim(name)) > 0",
            name="ck_services_name_not_blank",
        ),
        CheckConstraint(
            "avg_minutes > 0",
            name="ck_services_avg_minutes_positive",
        ),
    )

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(db.String(100), nullable=False)
    avg_minutes: Mapped[int] = mapped_column(nullable=False)

    active: Mapped[bool] = mapped_column(
        db.Boolean,
        nullable=False,
        server_default="true",
    )

    tickets: Mapped[list["Ticket"]] = relationship(
        back_populates="service",
        passive_deletes="all",
    )


class Ticket(db.Model):
    __tablename__ = "tickets"

    __table_args__ = (
        CheckConstraint(
            "status IN ('waiting', 'called', 'served', 'no-show', 'left')",
            name="ck_tickets_status",
        ),
    )

    id: Mapped[int] = mapped_column(primary_key=True)

    user_id: Mapped[int] = mapped_column(
        ForeignKey("users.id", ondelete="RESTRICT"),
        nullable=False,
        index=True,
    )

    service_id: Mapped[int] = mapped_column(
        ForeignKey("services.id", ondelete="RESTRICT"),
        nullable=False,
        index=True,
    )

    status: Mapped[str] = mapped_column(
        db.String(20),
        nullable=False,
        server_default="waiting",
    )

    created_at: Mapped[datetime] = mapped_column(
        db.DateTime(timezone=True),
        nullable=False,
        server_default=func.now(),
    )

    queued_at: Mapped[datetime] = mapped_column(
        db.DateTime(timezone=True),
        nullable=False,
        server_default=func.now(),
    )

    called_at: Mapped[datetime | None] = mapped_column(
        db.DateTime(timezone=True),
        nullable=True,
    )

    served_at: Mapped[datetime | None] = mapped_column(
        db.DateTime(timezone=True),
        nullable=True,
    )

    user: Mapped["User"] = relationship(back_populates="tickets")
    service: Mapped["Service"] = relationship(back_populates="tickets")