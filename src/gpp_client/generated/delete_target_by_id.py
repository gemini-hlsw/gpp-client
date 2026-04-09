from typing import Any, Optional

from pydantic import Field

from .base_model import BaseModel
from .enums import Existence
from .fragments import TargetDetails


class DeleteTargetById(BaseModel):
    update_targets: "DeleteTargetByIdUpdateTargets" = Field(alias="updateTargets")


class DeleteTargetByIdUpdateTargets(BaseModel):
    has_more: bool = Field(alias="hasMore")
    targets: list["DeleteTargetByIdUpdateTargetsTargets"]


class DeleteTargetByIdUpdateTargetsTargets(TargetDetails):
    program: "DeleteTargetByIdUpdateTargetsTargetsProgram"


class DeleteTargetByIdUpdateTargetsTargetsProgram(BaseModel):
    id: Any
    name: Optional[Any]
    description: Optional[Any]
    existence: Existence


DeleteTargetById.model_rebuild()
DeleteTargetByIdUpdateTargets.model_rebuild()
DeleteTargetByIdUpdateTargetsTargets.model_rebuild()
