from typing import Optional

from .base_model import BaseModel
from .fragments import AttachmentDetails


class GetProgramAttachmentsByReference(BaseModel):
    program: Optional["GetProgramAttachmentsByReferenceProgram"]


class GetProgramAttachmentsByReferenceProgram(BaseModel):
    attachments: list["GetProgramAttachmentsByReferenceProgramAttachments"]


class GetProgramAttachmentsByReferenceProgramAttachments(AttachmentDetails):
    pass


GetProgramAttachmentsByReference.model_rebuild()
GetProgramAttachmentsByReferenceProgram.model_rebuild()
