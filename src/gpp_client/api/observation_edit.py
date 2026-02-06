from typing import Annotated, Any, Literal, Optional, Union

from pydantic import Field

from .base_model import BaseModel
from .enums import (
    CalibrationRole,
    CloudExtinctionPreset,
    EditType,
    Existence,
    GmosNorthBuiltinFpu,
    GmosNorthFilter,
    GmosNorthGrating,
    GmosSouthBuiltinFpu,
    GmosSouthFilter,
    GmosSouthGrating,
    ImageQualityPreset,
    Instrument,
    ObservingModeType,
    ScienceBand,
    ScienceMode,
    SkyBackground,
    TimingWindowInclusion,
    WaterVapor,
)


class ObservationEdit(BaseModel):
    observation_edit: "ObservationEditObservationEdit" = Field(alias="observationEdit")


class ObservationEditObservationEdit(BaseModel):
    edit_type: EditType = Field(alias="editType")
    observation_id: Any = Field(alias="observationId")
    value: Optional["ObservationEditObservationEditValue"]


class ObservationEditObservationEditValue(BaseModel):
    id: Any
    existence: Existence
    reference: Optional["ObservationEditObservationEditValueReference"]
    calibration_role: Optional[CalibrationRole] = Field(alias="calibrationRole")
    instrument: Optional[Instrument]
    index: Any
    title: Any
    subtitle: Optional[Any]
    science_requirements: "ObservationEditObservationEditValueScienceRequirements" = (
        Field(alias="scienceRequirements")
    )
    science_band: Optional[ScienceBand] = Field(alias="scienceBand")
    observing_mode: Optional["ObservationEditObservationEditValueObservingMode"] = (
        Field(alias="observingMode")
    )
    constraint_set: "ObservationEditObservationEditValueConstraintSet" = Field(
        alias="constraintSet"
    )
    timing_windows: list["ObservationEditObservationEditValueTimingWindows"] = Field(
        alias="timingWindows"
    )
    target_environment: "ObservationEditObservationEditValueTargetEnvironment" = Field(
        alias="targetEnvironment"
    )


class ObservationEditObservationEditValueReference(BaseModel):
    label: Any


class ObservationEditObservationEditValueScienceRequirements(BaseModel):
    mode: Optional[ScienceMode]


class ObservationEditObservationEditValueObservingMode(BaseModel):
    instrument: Instrument
    mode: ObservingModeType
    gmos_north_long_slit: Optional[
        "ObservationEditObservationEditValueObservingModeGmosNorthLongSlit"
    ] = Field(alias="gmosNorthLongSlit")
    gmos_south_long_slit: Optional[
        "ObservationEditObservationEditValueObservingModeGmosSouthLongSlit"
    ] = Field(alias="gmosSouthLongSlit")


class ObservationEditObservationEditValueObservingModeGmosNorthLongSlit(BaseModel):
    grating: GmosNorthGrating
    filter: Optional[GmosNorthFilter]
    fpu: GmosNorthBuiltinFpu
    central_wavelength: (
        "ObservationEditObservationEditValueObservingModeGmosNorthLongSlitCentralWavelength"
    ) = Field(alias="centralWavelength")


class ObservationEditObservationEditValueObservingModeGmosNorthLongSlitCentralWavelength(
    BaseModel
):
    nanometers: Any


class ObservationEditObservationEditValueObservingModeGmosSouthLongSlit(BaseModel):
    grating: GmosSouthGrating
    filter: Optional[GmosSouthFilter]
    fpu: GmosSouthBuiltinFpu
    central_wavelength: (
        "ObservationEditObservationEditValueObservingModeGmosSouthLongSlitCentralWavelength"
    ) = Field(alias="centralWavelength")


class ObservationEditObservationEditValueObservingModeGmosSouthLongSlitCentralWavelength(
    BaseModel
):
    nanometers: Any


class ObservationEditObservationEditValueConstraintSet(BaseModel):
    image_quality: ImageQualityPreset = Field(alias="imageQuality")
    cloud_extinction: CloudExtinctionPreset = Field(alias="cloudExtinction")
    sky_background: SkyBackground = Field(alias="skyBackground")
    water_vapor: WaterVapor = Field(alias="waterVapor")
    elevation_range: (
        "ObservationEditObservationEditValueConstraintSetElevationRange"
    ) = Field(alias="elevationRange")


class ObservationEditObservationEditValueConstraintSetElevationRange(BaseModel):
    air_mass: Optional[
        "ObservationEditObservationEditValueConstraintSetElevationRangeAirMass"
    ] = Field(alias="airMass")
    hour_angle: Optional[
        "ObservationEditObservationEditValueConstraintSetElevationRangeHourAngle"
    ] = Field(alias="hourAngle")


class ObservationEditObservationEditValueConstraintSetElevationRangeAirMass(BaseModel):
    min: Any
    max: Any


class ObservationEditObservationEditValueConstraintSetElevationRangeHourAngle(
    BaseModel
):
    min_hours: Any = Field(alias="minHours")
    max_hours: Any = Field(alias="maxHours")


class ObservationEditObservationEditValueTimingWindows(BaseModel):
    inclusion: TimingWindowInclusion
    start_utc: Any = Field(alias="startUtc")
    end: Optional[
        Annotated[
            Union[
                "ObservationEditObservationEditValueTimingWindowsEndTimingWindowEndAt",
                "ObservationEditObservationEditValueTimingWindowsEndTimingWindowEndAfter",
            ],
            Field(discriminator="typename__"),
        ]
    ]


class ObservationEditObservationEditValueTimingWindowsEndTimingWindowEndAt(BaseModel):
    typename__: Literal["TimingWindowEndAt"] = Field(alias="__typename")
    at_utc: Any = Field(alias="atUtc")


class ObservationEditObservationEditValueTimingWindowsEndTimingWindowEndAfter(
    BaseModel
):
    typename__: Literal["TimingWindowEndAfter"] = Field(alias="__typename")
    after: (
        "ObservationEditObservationEditValueTimingWindowsEndTimingWindowEndAfterAfter"
    )
    repeat: Optional[
        "ObservationEditObservationEditValueTimingWindowsEndTimingWindowEndAfterRepeat"
    ]


class ObservationEditObservationEditValueTimingWindowsEndTimingWindowEndAfterAfter(
    BaseModel
):
    seconds: Any


class ObservationEditObservationEditValueTimingWindowsEndTimingWindowEndAfterRepeat(
    BaseModel
):
    period: "ObservationEditObservationEditValueTimingWindowsEndTimingWindowEndAfterRepeatPeriod"
    times: Optional[Any]


class ObservationEditObservationEditValueTimingWindowsEndTimingWindowEndAfterRepeatPeriod(
    BaseModel
):
    seconds: Any


class ObservationEditObservationEditValueTargetEnvironment(BaseModel):
    asterism: list["ObservationEditObservationEditValueTargetEnvironmentAsterism"]
    explicit_base: Optional[
        "ObservationEditObservationEditValueTargetEnvironmentExplicitBase"
    ] = Field(alias="explicitBase")


class ObservationEditObservationEditValueTargetEnvironmentAsterism(BaseModel):
    sidereal: Optional[
        "ObservationEditObservationEditValueTargetEnvironmentAsterismSidereal"
    ]
    nonsidereal: Optional[
        "ObservationEditObservationEditValueTargetEnvironmentAsterismNonsidereal"
    ]
    name: Any


class ObservationEditObservationEditValueTargetEnvironmentAsterismSidereal(BaseModel):
    ra: "ObservationEditObservationEditValueTargetEnvironmentAsterismSiderealRa"
    dec: "ObservationEditObservationEditValueTargetEnvironmentAsterismSiderealDec"
    epoch: Any


class ObservationEditObservationEditValueTargetEnvironmentAsterismSiderealRa(BaseModel):
    hms: Any


class ObservationEditObservationEditValueTargetEnvironmentAsterismSiderealDec(
    BaseModel
):
    dms: Any


class ObservationEditObservationEditValueTargetEnvironmentAsterismNonsidereal(
    BaseModel
):
    des: str


class ObservationEditObservationEditValueTargetEnvironmentExplicitBase(BaseModel):
    ra: "ObservationEditObservationEditValueTargetEnvironmentExplicitBaseRa"
    dec: "ObservationEditObservationEditValueTargetEnvironmentExplicitBaseDec"


class ObservationEditObservationEditValueTargetEnvironmentExplicitBaseRa(BaseModel):
    hms: Any


class ObservationEditObservationEditValueTargetEnvironmentExplicitBaseDec(BaseModel):
    dms: Any


ObservationEdit.model_rebuild()
ObservationEditObservationEdit.model_rebuild()
ObservationEditObservationEditValue.model_rebuild()
ObservationEditObservationEditValueObservingMode.model_rebuild()
ObservationEditObservationEditValueObservingModeGmosNorthLongSlit.model_rebuild()
ObservationEditObservationEditValueObservingModeGmosSouthLongSlit.model_rebuild()
ObservationEditObservationEditValueConstraintSet.model_rebuild()
ObservationEditObservationEditValueConstraintSetElevationRange.model_rebuild()
ObservationEditObservationEditValueTimingWindows.model_rebuild()
ObservationEditObservationEditValueTimingWindowsEndTimingWindowEndAfter.model_rebuild()
ObservationEditObservationEditValueTimingWindowsEndTimingWindowEndAfterRepeat.model_rebuild()
ObservationEditObservationEditValueTargetEnvironment.model_rebuild()
ObservationEditObservationEditValueTargetEnvironmentAsterism.model_rebuild()
ObservationEditObservationEditValueTargetEnvironmentAsterismSidereal.model_rebuild()
ObservationEditObservationEditValueTargetEnvironmentExplicitBase.model_rebuild()
