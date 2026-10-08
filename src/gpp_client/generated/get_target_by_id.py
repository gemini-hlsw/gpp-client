from typing import Optional

from .base_model import BaseModel
from .fragments import (  # noqa: F401
    TargetDetails,
    TargetDetailsNonsidereal,
    TargetDetailsOpportunity,
    TargetDetailsSidereal,
    TargetProgramSummary,
    TargetProgramSummaryProgram,
)


class GetTargetById(BaseModel):
    target: Optional["GetTargetByIdTarget"]


class GetTargetByIdTarget(TargetDetails, TargetProgramSummary):
    pass


GetTargetById.model_rebuild()
