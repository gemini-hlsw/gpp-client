from pydantic import Field

from .base_model import BaseModel
from .fragments import (  # noqa: F401
    TargetDetails,
    TargetDetailsNonsidereal,
    TargetDetailsOpportunity,
    TargetDetailsSidereal,
    TargetProgramSummary,
    TargetProgramSummaryProgram,
)


class CreateTargetByProgramReference(BaseModel):
    create_target: "CreateTargetByProgramReferenceCreateTarget" = Field(
        alias="createTarget"
    )


class CreateTargetByProgramReferenceCreateTarget(BaseModel):
    target: "CreateTargetByProgramReferenceCreateTargetTarget"


class CreateTargetByProgramReferenceCreateTargetTarget(
    TargetDetails, TargetProgramSummary
):
    pass


CreateTargetByProgramReference.model_rebuild()
CreateTargetByProgramReferenceCreateTarget.model_rebuild()
