from typing import Any, Optional

from pydantic import Field

from .base_model import BaseModel
from .enums import AtomExecutionState, CalculationState, EditType


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


class SchedulerObservationsUpdatesObscalcUpdateValue(BaseModel):
    id: Any
    observation_time: Optional[Any] = Field(alias="observationTime")
    execution: "SchedulerObservationsUpdatesObscalcUpdateValueExecution"


class SchedulerObservationsUpdatesObscalcUpdateValueExecution(BaseModel):
    visits: "SchedulerObservationsUpdatesObscalcUpdateValueExecutionVisits"


class SchedulerObservationsUpdatesObscalcUpdateValueExecutionVisits(BaseModel):
    matches: list[
        "SchedulerObservationsUpdatesObscalcUpdateValueExecutionVisitsMatches"
    ]


class SchedulerObservationsUpdatesObscalcUpdateValueExecutionVisitsMatches(BaseModel):
    observation: "SchedulerObservationsUpdatesObscalcUpdateValueExecutionVisitsMatchesObservation"
    atom_records: "SchedulerObservationsUpdatesObscalcUpdateValueExecutionVisitsMatchesAtomRecords" = Field(
        alias="atomRecords"
    )


class SchedulerObservationsUpdatesObscalcUpdateValueExecutionVisitsMatchesObservation(
    BaseModel
):
    id: Any


class SchedulerObservationsUpdatesObscalcUpdateValueExecutionVisitsMatchesAtomRecords(
    BaseModel
):
    matches: list[
        "SchedulerObservationsUpdatesObscalcUpdateValueExecutionVisitsMatchesAtomRecordsMatches"
    ]


class SchedulerObservationsUpdatesObscalcUpdateValueExecutionVisitsMatchesAtomRecordsMatches(
    BaseModel
):
    execution_state: AtomExecutionState = Field(alias="executionState")
    id: Any


SchedulerObservationsUpdates.model_rebuild()
SchedulerObservationsUpdatesObscalcUpdate.model_rebuild()
SchedulerObservationsUpdatesObscalcUpdateValue.model_rebuild()
SchedulerObservationsUpdatesObscalcUpdateValueExecution.model_rebuild()
SchedulerObservationsUpdatesObscalcUpdateValueExecutionVisits.model_rebuild()
SchedulerObservationsUpdatesObscalcUpdateValueExecutionVisitsMatches.model_rebuild()
SchedulerObservationsUpdatesObscalcUpdateValueExecutionVisitsMatchesAtomRecords.model_rebuild()
