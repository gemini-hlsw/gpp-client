from pydantic import Field

from .base_model import BaseModel
from .fragments import GOATSProgram


class GetGOATSPrograms(BaseModel):
    programs: "GetGOATSProgramsPrograms"


class GetGOATSProgramsPrograms(BaseModel):
    matches: list["GetGOATSProgramsProgramsMatches"]
    has_more: bool = Field(alias="hasMore")


class GetGOATSProgramsProgramsMatches(GOATSProgram):
    pass


GetGOATSPrograms.model_rebuild()
GetGOATSProgramsPrograms.model_rebuild()
