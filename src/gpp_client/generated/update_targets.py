from pydantic import Field

from .base_model import BaseModel
from .fragments import TargetDetails, TargetProgramSummary


class UpdateTargets(BaseModel):
    update_targets: "UpdateTargetsUpdateTargets" = Field(alias="updateTargets")


class UpdateTargetsUpdateTargets(BaseModel):
    has_more: bool = Field(alias="hasMore")
    targets: list["UpdateTargetsUpdateTargetsTargets"]


class UpdateTargetsUpdateTargetsTargets(TargetDetails, TargetProgramSummary):
    pass


UpdateTargets.model_rebuild()
UpdateTargetsUpdateTargets.model_rebuild()
