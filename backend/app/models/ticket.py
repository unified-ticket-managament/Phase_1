# ticket.py

import uuid
from datetime import datetime, timezone

from sqlalchemy import DateTime, Enum, ForeignKey, String
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.database.base import Base


def utc_now() -> datetime:
    return datetime.now(timezone.utc)


class Ticket(Base):
    __tablename__ = "tickets"

    ticket_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        primary_key=True,
        default=uuid.uuid4
    )

    client_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("clients.client_id"),
        nullable=False
    )

    assigned_staff_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("staff.staff_id"),
        nullable=False
    )

    title: Mapped[str] = mapped_column(
        String(255),
        nullable=False
    )

    status: Mapped[str] = mapped_column(
        Enum(
            "OPEN",
            "IN_PROGRESS",
            "WAITING_FOR_CLIENT",
            "RESOLVED",
            "CLOSED",
            name="ticket_status_enum"
        ),
        default="OPEN",
        nullable=False
    )

    priority: Mapped[str] = mapped_column(
        Enum(
            "LOW",
            "MEDIUM",
            "HIGH",
            "CRITICAL",
            name="ticket_priority_enum"
        ),
        default="MEDIUM",
        nullable=False
    )

    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        default=utc_now,
        nullable=False
    )

    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        default=utc_now,
        onupdate=utc_now,
        nullable=False
    )

    interactions = relationship(
        "Interaction",
        back_populates="ticket",
        cascade="all, delete-orphan"
    )