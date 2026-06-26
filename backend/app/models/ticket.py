import uuid
from typing import TYPE_CHECKING

from sqlalchemy import Enum, ForeignKey, String
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship

from shared_models.database import Base
from shared_models.mixins import TimestampMixin

if TYPE_CHECKING:
    from shared_models.models import User
    from .interaction import Interaction


class Ticket(TimestampMixin, Base):
    """
    Ticket model.

    A ticket belongs to one client and is assigned
    to one staff member.
    """

    __tablename__ = "tickets"

    ticket_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        primary_key=True,
        default=uuid.uuid4,
    )

    # Client (User having Client role)
    client_user_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("users.id"),
        nullable=False,
    )

    # Assigned Staff (User having Staff role)
    assigned_user_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("users.id"),
        nullable=False,
    )

    title: Mapped[str] = mapped_column(
        String(255),
        nullable=False,
    )

    status: Mapped[str] = mapped_column(
        Enum(
            "OPEN",
            "IN_PROGRESS",
            "WAITING_FOR_CLIENT",
            "RESOLVED",
            "CLOSED",
            name="ticket_status_enum",
        ),
        nullable=False,
        default="OPEN",
    )

    priority: Mapped[str] = mapped_column(
        Enum(
            "LOW",
            "MEDIUM",
            "HIGH",
            "CRITICAL",
            name="ticket_priority_enum",
        ),
        nullable=False,
        default="MEDIUM",
    )

    # -----------------------------
    # Relationships
    # -----------------------------

    client: Mapped["User"] = relationship(
        "User",
        foreign_keys=[client_user_id],
    )

    assigned_user: Mapped["User"] = relationship(
        "User",
        foreign_keys=[assigned_user_id],
    )

    interactions: Mapped[list["Interaction"]] = relationship(
        "Interaction",
        back_populates="ticket",
        cascade="all, delete-orphan",
    )

    def __repr__(self) -> str:
        return (
            f"<Ticket(ticket_id={self.ticket_id}, "
            f"title='{self.title}', "
            f"status='{self.status}')>"
        )