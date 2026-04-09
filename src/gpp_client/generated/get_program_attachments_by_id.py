from typing import Optional

from .base_model import BaseModel
from .fragments import AttachmentDetails


class GetProgramAttachmentsById(BaseModel):
    program: Optional["GetProgramAttachmentsByIdProgram"]


class GetProgramAttachmentsByIdProgram(BaseModel):
    attachments: list["GetProgramAttachmentsByIdProgramAttachments"]


class GetProgramAttachmentsByIdProgramAttachments(AttachmentDetails):
    pass


GetProgramAttachmentsById.model_rebuild()
GetProgramAttachmentsByIdProgram.model_rebuild()
