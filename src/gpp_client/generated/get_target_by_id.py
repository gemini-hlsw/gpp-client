from typing import Optional

from .base_model import BaseModel
from .fragments import TargetDetails, TargetProgramSummary


class GetTargetById(BaseModel):
    target: Optional["GetTargetByIdTarget"]


class GetTargetByIdTarget(TargetDetails, TargetProgramSummary):
    pass


GetTargetById.model_rebuild()
