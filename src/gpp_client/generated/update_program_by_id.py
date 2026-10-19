from pydantic import Field

from .base_model import BaseModel
from .fragments import (  # noqa: F401
    ProgramDetail,
    ProgramDetailActive,
    ProgramDetailPi,
    ProgramDetailProposal,
    ProgramGroupElements,
    ProgramGroupElementsAllGroupElements,
)


class UpdateProgramById(BaseModel):
    update_programs: "UpdateProgramByIdUpdatePrograms" = Field(alias="updatePrograms")


class UpdateProgramByIdUpdatePrograms(BaseModel):
    has_more: bool = Field(alias="hasMore")
    programs: list["UpdateProgramByIdUpdateProgramsPrograms"]


class UpdateProgramByIdUpdateProgramsPrograms(ProgramDetail, ProgramGroupElements):
    pass


UpdateProgramById.model_rebuild()
UpdateProgramByIdUpdatePrograms.model_rebuild()
