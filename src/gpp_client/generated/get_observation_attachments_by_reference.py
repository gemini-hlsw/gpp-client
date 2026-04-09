from typing import Optional

from .base_model import BaseModel
from .fragments import AttachmentDetails


class GetObservationAttachmentsByReference(BaseModel):
    observation: Optional["GetObservationAttachmentsByReferenceObservation"]


class GetObservationAttachmentsByReferenceObservation(BaseModel):
    attachments: list["GetObservationAttachmentsByReferenceObservationAttachments"]


class GetObservationAttachmentsByReferenceObservationAttachments(AttachmentDetails):
    pass


GetObservationAttachmentsByReference.model_rebuild()
GetObservationAttachmentsByReferenceObservation.model_rebuild()
