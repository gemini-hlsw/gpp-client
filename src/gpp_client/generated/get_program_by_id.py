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


class GetProgramById(BaseModel):
    program: Optional["GetProgramByIdProgram"]


class GetProgramByIdProgram(ProgramDetail, ProgramGroupElements):
    pass


GetProgramById.model_rebuild()
