from pydantic import Field

from .base_model import BaseModel
from .fragments import TargetDetails, TargetProgramSummary


class UpdateTargetById(BaseModel):
    update_targets: "UpdateTargetByIdUpdateTargets" = Field(alias="updateTargets")


class UpdateTargetByIdUpdateTargets(BaseModel):
    has_more: bool = Field(alias="hasMore")
    targets: list["UpdateTargetByIdUpdateTargetsTargets"]


class UpdateTargetByIdUpdateTargetsTargets(TargetDetails, TargetProgramSummary):
    pass


UpdateTargetById.model_rebuild()
UpdateTargetByIdUpdateTargets.model_rebuild()
