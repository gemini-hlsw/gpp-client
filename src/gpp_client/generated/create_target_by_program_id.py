from pydantic import Field

from .base_model import BaseModel
from .fragments import TargetDetails, TargetProgramSummary


class CreateTargetByProgramId(BaseModel):
    create_target: "CreateTargetByProgramIdCreateTarget" = Field(alias="createTarget")


class CreateTargetByProgramIdCreateTarget(BaseModel):
    target: "CreateTargetByProgramIdCreateTargetTarget"


class CreateTargetByProgramIdCreateTargetTarget(TargetDetails, TargetProgramSummary):
    pass


CreateTargetByProgramId.model_rebuild()
CreateTargetByProgramIdCreateTarget.model_rebuild()
