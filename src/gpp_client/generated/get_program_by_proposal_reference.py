from typing import Optional

from .base_model import BaseModel
from .fragments import ProgramDetail, ProgramGroupElements


class GetProgramByProposalReference(BaseModel):
    program: Optional["GetProgramByProposalReferenceProgram"]


class GetProgramByProposalReferenceProgram(ProgramDetail, ProgramGroupElements):
    pass


GetProgramByProposalReference.model_rebuild()
