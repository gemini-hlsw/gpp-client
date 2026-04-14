from typing import Optional

from .base_model import BaseModel
from .fragments import ProgramDetail, ProgramGroupElements


class GetProgramById(BaseModel):
    program: Optional["GetProgramByIdProgram"]


class GetProgramByIdProgram(ProgramDetail, ProgramGroupElements):
    pass


GetProgramById.model_rebuild()
