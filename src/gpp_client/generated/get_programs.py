from pydantic import Field

from .base_model import BaseModel
from .fragments import ProgramDetail, ProgramGroupElements


class GetPrograms(BaseModel):
    programs: "GetProgramsPrograms"


class GetProgramsPrograms(BaseModel):
    has_more: bool = Field(alias="hasMore")
    matches: list["GetProgramsProgramsMatches"]


class GetProgramsProgramsMatches(ProgramDetail, ProgramGroupElements):
    pass


GetPrograms.model_rebuild()
GetProgramsPrograms.model_rebuild()
