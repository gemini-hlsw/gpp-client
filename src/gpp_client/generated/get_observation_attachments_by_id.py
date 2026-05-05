from typing import Optional

from .base_model import BaseModel
from .fragments import AttachmentDetails


class GetObservationAttachmentsById(BaseModel):
    observation: Optional["GetObservationAttachmentsByIdObservation"]


class GetObservationAttachmentsByIdObservation(BaseModel):
    attachments: list["GetObservationAttachmentsByIdObservationAttachments"]


class GetObservationAttachmentsByIdObservationAttachments(AttachmentDetails):
    pass


GetObservationAttachmentsById.model_rebuild()
GetObservationAttachmentsByIdObservation.model_rebuild()
