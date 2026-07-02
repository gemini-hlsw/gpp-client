from typing import Annotated, Any, Literal, Optional, Union

from pydantic import Field

from .base_model import BaseModel
from .enums import (
    AtomExecutionState,
    CalculationState,
    CloudExtinctionPreset,
    EditType,
    EphemerisKeyType,
    ImageQualityPreset,
    Instrument,
    ObservationWorkflowState,
    SkyBackground,
    TimingWindowInclusion,
    WaterVapor,
)


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
    program: "SchedulerObservationsUpdatesObscalcUpdateValueProgram"
    workflow: Optional["SchedulerObservationsUpdatesObscalcUpdateValueWorkflow"]
    execution: "SchedulerObservationsUpdatesObscalcUpdateValueExecution"
    target_environment: "SchedulerObservationsUpdatesObscalcUpdateValueTargetEnvironment" = Field(
        alias="targetEnvironment"
    )
    constraint_set: "SchedulerObservationsUpdatesObscalcUpdateValueConstraintSet" = (
        Field(alias="constraintSet")
    )
    timing_windows: list[
        "SchedulerObservationsUpdatesObscalcUpdateValueTimingWindows"
    ] = Field(alias="timingWindows")
    instrument: Optional[Instrument]


class SchedulerObservationsUpdatesObscalcUpdateValueProgram(BaseModel):
    active: "SchedulerObservationsUpdatesObscalcUpdateValueProgramActive"


class SchedulerObservationsUpdatesObscalcUpdateValueProgramActive(BaseModel):
    end: Any
    start: Any


class SchedulerObservationsUpdatesObscalcUpdateValueWorkflow(BaseModel):
    value: "SchedulerObservationsUpdatesObscalcUpdateValueWorkflowValue"


class SchedulerObservationsUpdatesObscalcUpdateValueWorkflowValue(BaseModel):
    state: ObservationWorkflowState


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


class SchedulerObservationsUpdatesObscalcUpdateValueTargetEnvironment(BaseModel):
    asterism: list[
        "SchedulerObservationsUpdatesObscalcUpdateValueTargetEnvironmentAsterism"
    ]
    explicit_base: Optional[
        "SchedulerObservationsUpdatesObscalcUpdateValueTargetEnvironmentExplicitBase"
    ] = Field(alias="explicitBase")


class SchedulerObservationsUpdatesObscalcUpdateValueTargetEnvironmentAsterism(
    BaseModel
):
    name: Any
    sidereal: Optional[
        "SchedulerObservationsUpdatesObscalcUpdateValueTargetEnvironmentAsterismSidereal"
    ]
    nonsidereal: Optional[
        "SchedulerObservationsUpdatesObscalcUpdateValueTargetEnvironmentAsterismNonsidereal"
    ]


class SchedulerObservationsUpdatesObscalcUpdateValueTargetEnvironmentAsterismSidereal(
    BaseModel
):
    ra: "SchedulerObservationsUpdatesObscalcUpdateValueTargetEnvironmentAsterismSiderealRa"
    dec: "SchedulerObservationsUpdatesObscalcUpdateValueTargetEnvironmentAsterismSiderealDec"
    epoch: Any


class SchedulerObservationsUpdatesObscalcUpdateValueTargetEnvironmentAsterismSiderealRa(
    BaseModel
):
    hours: Any
    hms: Any
    degrees: Any


class SchedulerObservationsUpdatesObscalcUpdateValueTargetEnvironmentAsterismSiderealDec(
    BaseModel
):
    degrees: Any
    dms: Any


class SchedulerObservationsUpdatesObscalcUpdateValueTargetEnvironmentAsterismNonsidereal(
    BaseModel
):
    des: str
    key_type: EphemerisKeyType = Field(alias="keyType")
    key: str


class SchedulerObservationsUpdatesObscalcUpdateValueTargetEnvironmentExplicitBase(
    BaseModel
):
    ra: "SchedulerObservationsUpdatesObscalcUpdateValueTargetEnvironmentExplicitBaseRa"
    dec: (
        "SchedulerObservationsUpdatesObscalcUpdateValueTargetEnvironmentExplicitBaseDec"
    )


class SchedulerObservationsUpdatesObscalcUpdateValueTargetEnvironmentExplicitBaseRa(
    BaseModel
):
    hms: Any


class SchedulerObservationsUpdatesObscalcUpdateValueTargetEnvironmentExplicitBaseDec(
    BaseModel
):
    dms: Any


class SchedulerObservationsUpdatesObscalcUpdateValueConstraintSet(BaseModel):
    image_quality: ImageQualityPreset = Field(alias="imageQuality")
    cloud_extinction: CloudExtinctionPreset = Field(alias="cloudExtinction")
    sky_background: SkyBackground = Field(alias="skyBackground")
    water_vapor: WaterVapor = Field(alias="waterVapor")
    elevation_range: "SchedulerObservationsUpdatesObscalcUpdateValueConstraintSetElevationRange" = Field(
        alias="elevationRange"
    )


class SchedulerObservationsUpdatesObscalcUpdateValueConstraintSetElevationRange(
    BaseModel
):
    air_mass: Optional[
        "SchedulerObservationsUpdatesObscalcUpdateValueConstraintSetElevationRangeAirMass"
    ] = Field(alias="airMass")
    hour_angle: Optional[
        "SchedulerObservationsUpdatesObscalcUpdateValueConstraintSetElevationRangeHourAngle"
    ] = Field(alias="hourAngle")


class SchedulerObservationsUpdatesObscalcUpdateValueConstraintSetElevationRangeAirMass(
    BaseModel
):
    min: Any
    max: Any


class SchedulerObservationsUpdatesObscalcUpdateValueConstraintSetElevationRangeHourAngle(
    BaseModel
):
    min_hours: Any = Field(alias="minHours")
    max_hours: Any = Field(alias="maxHours")


class SchedulerObservationsUpdatesObscalcUpdateValueTimingWindows(BaseModel):
    inclusion: TimingWindowInclusion
    start_utc: Any = Field(alias="startUtc")
    end: Optional[
        Annotated[
            Union[
                "SchedulerObservationsUpdatesObscalcUpdateValueTimingWindowsEndTimingWindowEndAt",
                "SchedulerObservationsUpdatesObscalcUpdateValueTimingWindowsEndTimingWindowEndAfter",
            ],
            Field(discriminator="typename__"),
        ]
    ]


class SchedulerObservationsUpdatesObscalcUpdateValueTimingWindowsEndTimingWindowEndAt(
    BaseModel
):
    typename__: Literal["TimingWindowEndAt"] = Field(alias="__typename")
    at_utc: Any = Field(alias="atUtc")


class SchedulerObservationsUpdatesObscalcUpdateValueTimingWindowsEndTimingWindowEndAfter(
    BaseModel
):
    typename__: Literal["TimingWindowEndAfter"] = Field(alias="__typename")
    after: "SchedulerObservationsUpdatesObscalcUpdateValueTimingWindowsEndTimingWindowEndAfterAfter"
    repeat: Optional[
        "SchedulerObservationsUpdatesObscalcUpdateValueTimingWindowsEndTimingWindowEndAfterRepeat"
    ]


class SchedulerObservationsUpdatesObscalcUpdateValueTimingWindowsEndTimingWindowEndAfterAfter(
    BaseModel
):
    seconds: Any


class SchedulerObservationsUpdatesObscalcUpdateValueTimingWindowsEndTimingWindowEndAfterRepeat(
    BaseModel
):
    period: "SchedulerObservationsUpdatesObscalcUpdateValueTimingWindowsEndTimingWindowEndAfterRepeatPeriod"
    times: Optional[Any]


class SchedulerObservationsUpdatesObscalcUpdateValueTimingWindowsEndTimingWindowEndAfterRepeatPeriod(
    BaseModel
):
    seconds: Any


SchedulerObservationsUpdates.model_rebuild()
SchedulerObservationsUpdatesObscalcUpdate.model_rebuild()
SchedulerObservationsUpdatesObscalcUpdateValue.model_rebuild()
SchedulerObservationsUpdatesObscalcUpdateValueProgram.model_rebuild()
SchedulerObservationsUpdatesObscalcUpdateValueWorkflow.model_rebuild()
SchedulerObservationsUpdatesObscalcUpdateValueExecution.model_rebuild()
SchedulerObservationsUpdatesObscalcUpdateValueExecutionVisits.model_rebuild()
SchedulerObservationsUpdatesObscalcUpdateValueExecutionVisitsMatches.model_rebuild()
SchedulerObservationsUpdatesObscalcUpdateValueExecutionVisitsMatchesAtomRecords.model_rebuild()
SchedulerObservationsUpdatesObscalcUpdateValueTargetEnvironment.model_rebuild()
SchedulerObservationsUpdatesObscalcUpdateValueTargetEnvironmentAsterism.model_rebuild()
SchedulerObservationsUpdatesObscalcUpdateValueTargetEnvironmentAsterismSidereal.model_rebuild()
SchedulerObservationsUpdatesObscalcUpdateValueTargetEnvironmentExplicitBase.model_rebuild()
SchedulerObservationsUpdatesObscalcUpdateValueConstraintSet.model_rebuild()
SchedulerObservationsUpdatesObscalcUpdateValueConstraintSetElevationRange.model_rebuild()
SchedulerObservationsUpdatesObscalcUpdateValueTimingWindows.model_rebuild()
SchedulerObservationsUpdatesObscalcUpdateValueTimingWindowsEndTimingWindowEndAfter.model_rebuild()
SchedulerObservationsUpdatesObscalcUpdateValueTimingWindowsEndTimingWindowEndAfterRepeat.model_rebuild()
