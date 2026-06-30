# attachment_service.py

from uuid import UUID

from fastapi import HTTPException, status

from app.enums import InteractionDirection, InteractionStatus
from app.repositories.attachment_repository import AttachmentRepository
from app.repositories.interaction_repository import InteractionRepository
from app.repositories.ticket_repository import TicketRepository
from app.schemas.attachment import (
    AttachmentCreate,
    AttachmentUploadRequest,
    AttachmentUploadResponse,
)
from app.schemas.interaction import InteractionCreate


class AttachmentService:
    """
    Handles file uploads on a ticket.

    Every uploaded file is recorded as an Interaction
    (interaction_type="ATTACHMENT") so it appears on the
    ticket timeline, and its file metadata is stored in
    its own Attachment row linked to that interaction.
    """

    def __init__(
        self,
        attachment_repository: AttachmentRepository,
        interaction_repository: InteractionRepository,
        ticket_repository: TicketRepository,
    ):
        self.attachment_repository = attachment_repository
        self.interaction_repository = interaction_repository
        self.ticket_repository = ticket_repository

    async def upload_attachment(
        self,
        ticket_id: UUID,
        request: AttachmentUploadRequest,
    ) -> AttachmentUploadResponse:

        ticket = await self.ticket_repository.get_by_id(ticket_id)

        if ticket is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Ticket not found.",
            )

        interaction = await self.interaction_repository.create(
            InteractionCreate(
                ticket_id=ticket_id,
                interaction_type="ATTACHMENT",
                direction=InteractionDirection.INTERNAL,
                status=InteractionStatus.ASSIGNED,
                performed_by=request.performed_by,
                payload={
                    "filename": request.filename,
                },
                is_visible=True,
                message_id=None,
            )
        )

        attachment = await self.attachment_repository.create(
            AttachmentCreate(
                interaction_id=interaction.interaction_id,
                filename=request.filename,
                mime_type=request.mime_type,
                size_bytes=request.size_bytes,
                storage_key=request.storage_key,
                scan_status=request.scan_status,
            )
        )

        return AttachmentUploadResponse(
            interaction_id=interaction.interaction_id,
            attachment_id=attachment.attachment_id,
            ticket_id=ticket_id,
            filename=attachment.filename,
            message="Attachment uploaded successfully.",
        )