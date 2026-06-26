"""Create ticket management tables.

Revision ID: a1037971b066
Revises:
Create Date: 2026-06-26

"""

from typing import Sequence, Union

import sqlalchemy as sa
from alembic import op
from sqlalchemy.dialects import postgresql


# revision identifiers
revision: str = "a1037971b066"
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


# PostgreSQL enum objects for the ticket service.
ticket_status_enum = postgresql.ENUM(
    "OPEN",
    "IN_PROGRESS",
    "WAITING_FOR_CLIENT",
    "RESOLVED",
    "CLOSED",
    name="ticket_status_enum",
    create_type=False,
)

ticket_priority_enum = postgresql.ENUM(
    "LOW",
    "MEDIUM",
    "HIGH",
    "CRITICAL",
    name="ticket_priority_enum",
    create_type=False,
)

interaction_type_enum = postgresql.ENUM(
    "EMAIL",
    "SMS",
    "PHONE",
    "INTERNAL_NOTE",
    "STATUS_CHANGE",
    "AGENT_REPLY",
    "FILE",
    "RESOLUTION",
    name="interaction_type_enum",
    create_type=False,
)

interaction_direction_enum = postgresql.ENUM(
    "INBOUND",
    "OUTBOUND",
    "INTERNAL",
    name="interaction_direction_enum",
    create_type=False,
)


def upgrade() -> None:
    ticket_status_enum.create(op.get_bind(), checkfirst=True)
    ticket_priority_enum.create(op.get_bind(), checkfirst=True)
    interaction_type_enum.create(op.get_bind(), checkfirst=True)
    interaction_direction_enum.create(op.get_bind(), checkfirst=True)

    op.create_table(
        "tickets",
        sa.Column(
            "ticket_id",
            postgresql.UUID(as_uuid=True),
            primary_key=True,
            nullable=False,
        ),
        sa.Column(
            "client_user_id",
            postgresql.UUID(as_uuid=True),
            sa.ForeignKey("users.id"),
            nullable=False,
        ),
        sa.Column(
            "assigned_user_id",
            postgresql.UUID(as_uuid=True),
            sa.ForeignKey("users.id"),
            nullable=False,
        ),
        sa.Column("title", sa.String(length=255), nullable=False),
        sa.Column(
            "status",
            ticket_status_enum,
            nullable=False,
            server_default="OPEN",
        ),
        sa.Column(
            "priority",
            ticket_priority_enum,
            nullable=False,
            server_default="MEDIUM",
        ),
        sa.Column(
            "created_at",
            sa.DateTime(timezone=True),
            nullable=False,
            server_default=sa.text("CURRENT_TIMESTAMP"),
        ),
        sa.Column(
            "updated_at",
            sa.DateTime(timezone=True),
            nullable=False,
            server_default=sa.text("CURRENT_TIMESTAMP"),
            server_onupdate=sa.text("CURRENT_TIMESTAMP"),
        ),
    )

    op.create_table(
        "interactions",
        sa.Column(
            "interaction_id",
            postgresql.UUID(as_uuid=True),
            primary_key=True,
            nullable=False,
        ),
        sa.Column(
            "ticket_id",
            postgresql.UUID(as_uuid=True),
            sa.ForeignKey("tickets.ticket_id"),
            nullable=False,
        ),
        sa.Column("type", interaction_type_enum, nullable=False),
        sa.Column("direction", interaction_direction_enum, nullable=False),
        sa.Column("content", postgresql.JSONB(), nullable=False),
        sa.Column(
            "created_at",
            sa.DateTime(timezone=True),
            nullable=False,
            server_default=sa.text("CURRENT_TIMESTAMP"),
        ),
        sa.Column(
            "updated_at",
            sa.DateTime(timezone=True),
            nullable=False,
            server_default=sa.text("CURRENT_TIMESTAMP"),
            server_onupdate=sa.text("CURRENT_TIMESTAMP"),
        ),
    )

    op.create_table(
        "attachments",
        sa.Column(
            "attachment_id",
            postgresql.UUID(as_uuid=True),
            primary_key=True,
            nullable=False,
        ),
        sa.Column(
            "interaction_id",
            postgresql.UUID(as_uuid=True),
            sa.ForeignKey("interactions.interaction_id"),
            nullable=False,
        ),
        sa.Column("file_name", sa.String(length=255), nullable=False),
        sa.Column("file_type", sa.String(length=100), nullable=False),
        sa.Column("file_url", sa.String(length=500), nullable=False),
        sa.Column(
            "created_at",
            sa.DateTime(timezone=True),
            nullable=False,
            server_default=sa.text("CURRENT_TIMESTAMP"),
        ),
        sa.Column(
            "updated_at",
            sa.DateTime(timezone=True),
            nullable=False,
            server_default=sa.text("CURRENT_TIMESTAMP"),
            server_onupdate=sa.text("CURRENT_TIMESTAMP"),
        ),
    )


def downgrade() -> None:
    op.drop_table("attachments")
    op.drop_table("interactions")
    op.drop_table("tickets")

    ticket_status_enum.drop(op.get_bind(), checkfirst=True)
    ticket_priority_enum.drop(op.get_bind(), checkfirst=True)
    interaction_type_enum.drop(op.get_bind(), checkfirst=True)
    interaction_direction_enum.drop(op.get_bind(), checkfirst=True)