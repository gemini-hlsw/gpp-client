from typing import Any, Optional

from pydantic import Field

from .base_model import BaseModel
from .enums import Existence
from .fragments import TargetDetails


class RestoreTargetById(BaseModel):
    update_targets: "RestoreTargetByIdUpdateTargets" = Field(alias="updateTargets")


class RestoreTargetByIdUpdateTargets(BaseModel):
    has_more: bool = Field(alias="hasMore")
    targets: list["RestoreTargetByIdUpdateTargetsTargets"]


class RestoreTargetByIdUpdateTargetsTargets(TargetDetails):
    program: "RestoreTargetByIdUpdateTargetsTargetsProgram"


class RestoreTargetByIdUpdateTargetsTargetsProgram(BaseModel):
    id: Any
    name: Optional[Any]
    description: Optional[Any]
    existence: Existence


RestoreTargetById.model_rebuild()
RestoreTargetByIdUpdateTargets.model_rebuild()
RestoreTargetByIdUpdateTargetsTargets.model_rebuild()
