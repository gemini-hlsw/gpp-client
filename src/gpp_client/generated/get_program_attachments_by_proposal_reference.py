from typing import Optional

from .base_model import BaseModel
from .fragments import AttachmentDetails


class GetProgramAttachmentsByProposalReference(BaseModel):
    program: Optional["GetProgramAttachmentsByProposalReferenceProgram"]


class GetProgramAttachmentsByProposalReferenceProgram(BaseModel):
    attachments: list["GetProgramAttachmentsByProposalReferenceProgramAttachments"]


class GetProgramAttachmentsByProposalReferenceProgramAttachments(AttachmentDetails):
    pass


GetProgramAttachmentsByProposalReference.model_rebuild()
GetProgramAttachmentsByProposalReferenceProgram.model_rebuild()
