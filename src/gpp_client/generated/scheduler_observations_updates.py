from typing import Any, Optional

from pydantic import Field

from .base_model import BaseModel
from .enums import CalculationState, EditType
from .fragments import ObservationDetails, ProgramCore


class SchedulerObservationsUpdates(BaseModel):
    obscalc_update: "SchedulerObservationsUpdatesObscalcUpdate" = Field(
        alias="obscalcUpdate"
    )


class SchedulerObservationsUpdatesObscalcUpdate(BaseModel):
    old_calculation_state: Optional[CalculationState] = Field(
        alias="oldCalculationState"
    )
    new_calculation_state: Optional[CalculationState] = Field(
        alias="newCalculationState"
    )
    edit_type: EditType = Field(alias="editType")
    value: Optional["SchedulerObservationsUpdatesObscalcUpdateValue"]


class SchedulerObservationsUpdatesObscalcUpdateValue(ObservationDetails):
    observation_time: Optional[Any] = Field(alias="observationTime")
    program: "SchedulerObservationsUpdatesObscalcUpdateValueProgram"


class SchedulerObservationsUpdatesObscalcUpdateValueProgram(ProgramCore):
    active: "SchedulerObservationsUpdatesObscalcUpdateValueProgramActive"


class SchedulerObservationsUpdatesObscalcUpdateValueProgramActive(BaseModel):
    start: Any
    end: Any


SchedulerObservationsUpdates.model_rebuild()
SchedulerObservationsUpdatesObscalcUpdate.model_rebuild()
SchedulerObservationsUpdatesObscalcUpdateValue.model_rebuild()
SchedulerObservationsUpdatesObscalcUpdateValueProgram.model_rebuild()
