from pydantic import Field

from .base_model import BaseModel
from .fragments import TargetDetails, TargetProgramSummary


class CloneTarget(BaseModel):
    clone_target: "CloneTargetCloneTarget" = Field(alias="cloneTarget")


class CloneTargetCloneTarget(BaseModel):
    new_target: "CloneTargetCloneTargetNewTarget" = Field(alias="newTarget")


class CloneTargetCloneTargetNewTarget(TargetDetails, TargetProgramSummary):
    pass


CloneTarget.model_rebuild()
CloneTargetCloneTarget.model_rebuild()
