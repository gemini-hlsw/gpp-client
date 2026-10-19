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


class CreateTargetByProposalReference(BaseModel):
    create_target: "CreateTargetByProposalReferenceCreateTarget" = Field(
        alias="createTarget"
    )


class CreateTargetByProposalReferenceCreateTarget(BaseModel):
    target: "CreateTargetByProposalReferenceCreateTargetTarget"


class CreateTargetByProposalReferenceCreateTargetTarget(
    TargetDetails, TargetProgramSummary
):
    pass


CreateTargetByProposalReference.model_rebuild()
CreateTargetByProposalReferenceCreateTarget.model_rebuild()
