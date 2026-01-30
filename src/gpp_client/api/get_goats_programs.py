from typing import Any, Literal, Optional

from pydantic import Field

from .base_model import BaseModel
from .enums import ProgramType, ProposalStatus


class GetGOATSPrograms(BaseModel):
    programs: "GetGOATSProgramsPrograms"


class GetGOATSProgramsPrograms(BaseModel):
    matches: list["GetGOATSProgramsProgramsMatches"]
    has_more: bool = Field(alias="hasMore")


class GetGOATSProgramsProgramsMatches(BaseModel):
    id: Any
    name: Optional[Any]
    description: Optional[Any]
    reference: Optional["GetGOATSProgramsProgramsMatchesReference"]
    proposal_status: ProposalStatus = Field(alias="proposalStatus")
    type: ProgramType


class GetGOATSProgramsProgramsMatchesReference(BaseModel):
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


GetGOATSPrograms.model_rebuild()
GetGOATSProgramsPrograms.model_rebuild()
GetGOATSProgramsProgramsMatches.model_rebuild()
