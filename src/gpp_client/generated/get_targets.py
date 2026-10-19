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


class GetTargets(BaseModel):
    targets: "GetTargetsTargets"


class GetTargetsTargets(BaseModel):
    has_more: bool = Field(alias="hasMore")
    matches: list["GetTargetsTargetsMatches"]


class GetTargetsTargetsMatches(TargetDetails, TargetProgramSummary):
    pass


GetTargets.model_rebuild()
GetTargetsTargets.model_rebuild()
