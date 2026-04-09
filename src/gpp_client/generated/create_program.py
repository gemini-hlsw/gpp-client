from pydantic import Field

from .base_model import BaseModel
from .fragments import ProgramDetail, ProgramGroupElements


class CreateProgram(BaseModel):
    create_program: "CreateProgramCreateProgram" = Field(alias="createProgram")


class CreateProgramCreateProgram(BaseModel):
    program: "CreateProgramCreateProgramProgram"


class CreateProgramCreateProgramProgram(ProgramDetail, ProgramGroupElements):
    pass


CreateProgram.model_rebuild()
CreateProgramCreateProgram.model_rebuild()
