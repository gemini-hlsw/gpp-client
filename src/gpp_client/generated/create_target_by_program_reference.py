from pydantic import Field

from .base_model import BaseModel
from .fragments import TargetDetails, TargetProgramSummary


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
