from typing import Optional

from .base_model import BaseModel
from .fragments import AttachmentDetails


class GetProgramAttachmentsByReference(BaseModel):
    program: Optional["GetProgramAttachmentsByReferenceProgram"]


class GetProgramAttachmentsByReferenceProgram(BaseModel):
    attachments: list["GetProgramAttachmentsByReferenceProgramAttachments"]


GetProgramAttachmentsByReferenceProgramAttachments = AttachmentDetails
GetProgramAttachmentsByReference.model_rebuild()
GetProgramAttachmentsByReferenceProgram.model_rebuild()
