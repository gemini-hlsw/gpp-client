from typing import Any, Optional

from pydantic import Field

from .base_model import BaseModel
from .enums import AtomExecutionState, CalculationState, EditType


class ObsCalculationUpdate(BaseModel):
    obscalc_update: "ObsCalculationUpdateObscalcUpdate" = Field(alias="obscalcUpdate")


class ObsCalculationUpdateObscalcUpdate(BaseModel):
    edit_type: EditType = Field(alias="editType")
    new_calculation_state: Optional[CalculationState] = Field(
        alias="newCalculationState"
    )
    observation_id: Any = Field(alias="observationId")
    old_calculation_state: Optional[CalculationState] = Field(
        alias="oldCalculationState"
    )
    value: Optional["ObsCalculationUpdateObscalcUpdateValue"]


class ObsCalculationUpdateObscalcUpdateValue(BaseModel):
    id: Any
    observation_time: Optional[Any] = Field(alias="observationTime")
    execution: "ObsCalculationUpdateObscalcUpdateValueExecution"


class ObsCalculationUpdateObscalcUpdateValueExecution(BaseModel):
    visits: "ObsCalculationUpdateObscalcUpdateValueExecutionVisits"


class ObsCalculationUpdateObscalcUpdateValueExecutionVisits(BaseModel):
    matches: list["ObsCalculationUpdateObscalcUpdateValueExecutionVisitsMatches"]


class ObsCalculationUpdateObscalcUpdateValueExecutionVisitsMatches(BaseModel):
    observation: (
        "ObsCalculationUpdateObscalcUpdateValueExecutionVisitsMatchesObservation"
    )
    atom_records: (
        "ObsCalculationUpdateObscalcUpdateValueExecutionVisitsMatchesAtomRecords"
    ) = Field(alias="atomRecords")


class ObsCalculationUpdateObscalcUpdateValueExecutionVisitsMatchesObservation(
    BaseModel
):
    id: Any


class ObsCalculationUpdateObscalcUpdateValueExecutionVisitsMatchesAtomRecords(
    BaseModel
):
    matches: list[
        "ObsCalculationUpdateObscalcUpdateValueExecutionVisitsMatchesAtomRecordsMatches"
    ]


class ObsCalculationUpdateObscalcUpdateValueExecutionVisitsMatchesAtomRecordsMatches(
    BaseModel
):
    execution_state: AtomExecutionState = Field(alias="executionState")
    id: Any


ObsCalculationUpdate.model_rebuild()
ObsCalculationUpdateObscalcUpdate.model_rebuild()
ObsCalculationUpdateObscalcUpdateValue.model_rebuild()
ObsCalculationUpdateObscalcUpdateValueExecution.model_rebuild()
ObsCalculationUpdateObscalcUpdateValueExecutionVisits.model_rebuild()
ObsCalculationUpdateObscalcUpdateValueExecutionVisitsMatches.model_rebuild()
ObsCalculationUpdateObscalcUpdateValueExecutionVisitsMatchesAtomRecords.model_rebuild()
