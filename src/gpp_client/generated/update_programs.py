from pydantic import Field

from .base_model import BaseModel
from .fragments import ProgramDetail, ProgramGroupElements


class UpdatePrograms(BaseModel):
    update_programs: "UpdateProgramsUpdatePrograms" = Field(alias="updatePrograms")


class UpdateProgramsUpdatePrograms(BaseModel):
    has_more: bool = Field(alias="hasMore")
    programs: list["UpdateProgramsUpdateProgramsPrograms"]


class UpdateProgramsUpdateProgramsPrograms(ProgramDetail, ProgramGroupElements):
    pass


UpdatePrograms.model_rebuild()
UpdateProgramsUpdatePrograms.model_rebuild()
