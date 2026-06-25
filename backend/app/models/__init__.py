from app.database.base import Base

from app.models.ticket import Ticket
from app.models.interaction import Interaction
from app.models.attachment import Attachment

__all__ = [
    "Base",
    "Ticket",
    "Interaction",
    "Attachment",
]