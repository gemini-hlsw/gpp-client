from pydantic import Field

from .base_model import BaseModel
from .fragments import TargetDetails, TargetProgramSummary


class GetTargets(BaseModel):
    targets: "GetTargetsTargets"


class GetTargetsTargets(BaseModel):
    has_more: bool = Field(alias="hasMore")
    matches: list["GetTargetsTargetsMatches"]


class GetTargetsTargetsMatches(TargetDetails, TargetProgramSummary):
    pass


GetTargets.model_rebuild()
GetTargetsTargets.model_rebuild()
