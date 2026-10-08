from typing import Optional

from .base_model import BaseModel
from .fragments import (  # noqa: F401
    ProgramDetail,
    ProgramDetailActive,
    ProgramDetailPi,
    ProgramDetailProposal,
    ProgramGroupElements,
    ProgramGroupElementsAllGroupElements,
)


class GetProgramByReference(BaseModel):
    program: Optional["GetProgramByReferenceProgram"]


class GetProgramByReferenceProgram(ProgramDetail, ProgramGroupElements):
    pass


GetProgramByReference.model_rebuild()
