from typing import Optional

from .base_model import BaseModel
from .fragments import ProgramDetail, ProgramGroupElements


class GetProgramByReference(BaseModel):
    program: Optional["GetProgramByReferenceProgram"]


class GetProgramByReferenceProgram(ProgramDetail, ProgramGroupElements):
    pass


GetProgramByReference.model_rebuild()
