# interaction.py

import uuid
from datetime import datetime, timezone

from sqlalchemy import DateTime, Enum, ForeignKey
from sqlalchemy.dialects.postgresql import JSONB, UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.database.base import Base


def utc_now():
    return datetime.now(timezone.utc)


class Interaction(Base):
    __tablename__ = "interactions"

    interaction_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        primary_key=True,
        default=uuid.uuid4
    )

    ticket_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("tickets.ticket_id"),
        nullable=False
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
            name="interaction_type_enum"
        ),
        nullable=False
    )

    direction: Mapped[str] = mapped_column(
        Enum(
            "INBOUND",
            "OUTBOUND",
            "INTERNAL",
            name="interaction_direction_enum"
        ),
        nullable=False
    )

    content: Mapped[dict] = mapped_column(
        JSONB,
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

    ticket = relationship(
        "Ticket",
        back_populates="interactions"
    )

    attachments = relationship(
        "Attachment",
        back_populates="interaction",
        cascade="all, delete-orphan"
    )