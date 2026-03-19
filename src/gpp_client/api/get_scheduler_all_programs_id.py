from typing import Any, Literal, Optional

from pydantic import Field

from .base_model import BaseModel


class GetSchedulerAllProgramsId(BaseModel):
    programs: "GetSchedulerAllProgramsIdPrograms"


class GetSchedulerAllProgramsIdPrograms(BaseModel):
    matches: list["GetSchedulerAllProgramsIdProgramsMatches"]


class GetSchedulerAllProgramsIdProgramsMatches(BaseModel):
    reference: Optional["GetSchedulerAllProgramsIdProgramsMatchesReference"]
    id: Any


class GetSchedulerAllProgramsIdProgramsMatchesReference(BaseModel):
    typename__: Literal[
        "CalibrationProgramReference",
        "CommissioningProgramReference",
        "EngineeringProgramReference",
        "ExampleProgramReference",
        "LibraryProgramReference",
        "MonitoringProgramReference",
        "ProgramReference",
        "ScienceProgramReference",
        "SystemProgramReference",
    ] = Field(alias="__typename")
    label: Any


GetSchedulerAllProgramsId.model_rebuild()
GetSchedulerAllProgramsIdPrograms.model_rebuild()
GetSchedulerAllProgramsIdProgramsMatches.model_rebuild()
