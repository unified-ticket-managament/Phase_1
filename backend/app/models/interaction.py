import uuid
from typing import TYPE_CHECKING

from sqlalchemy import Enum, ForeignKey
from sqlalchemy.dialects.postgresql import JSONB, UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship

from shared_models.database import Base
from shared_models.mixins import TimestampMixin

if TYPE_CHECKING:
    from .ticket import Ticket
    from .attachment import Attachment


class Interaction(TimestampMixin, Base):
    """
    Stores every interaction that occurs within a ticket.

    Examples:
    - Client Email
    - Agent Reply
    - Internal Note
    - Status Change
    - Phone Call
    - SMS
    """

    __tablename__ = "interactions"

    interaction_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        primary_key=True,
        default=uuid.uuid4,
    )

    ticket_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("tickets.ticket_id"),
        nullable=False,
    )

    type: Mapped[str] = mapped_column(
        Enum(
            "EMAIL",
            "SMS",
            "PHONE",
            "INTERNAL_NOTE",
            "STATUS_CHANGE",
            "AGENT_REPLY",
            "FILE",
            "RESOLUTION",
            name="interaction_type_enum",
        ),
        nullable=False,
    )

    direction: Mapped[str] = mapped_column(
        Enum(
            "INBOUND",
            "OUTBOUND",
            "INTERNAL",
            name="interaction_direction_enum",
        ),
        nullable=False,
    )

    content: Mapped[dict] = mapped_column(
        JSONB,
        nullable=False,
    )

    # -----------------------------
    # Relationships
    # -----------------------------

    ticket: Mapped["Ticket"] = relationship(
        "Ticket",
        back_populates="interactions",
    )

    attachments: Mapped[list["Attachment"]] = relationship(
        "Attachment",
        back_populates="interaction",
        cascade="all, delete-orphan",
    )

    def __repr__(self) -> str:
        return (
            f"<Interaction(interaction_id={self.interaction_id}, "
            f"type='{self.type}')>"
        )