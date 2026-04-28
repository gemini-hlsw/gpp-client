from typing import Annotated, Any, Literal, Optional, Union

from pydantic import Field

from .base_model import BaseModel
from .enums import (
    AttachmentType,
    Band,
    BrightnessIntegratedUnits,
    CalculationState,
    CloudExtinctionPreset,
    CoolStarTemperature,
    GalaxySpectrum,
    GmosAmpReadMode,
    GmosBinning,
    GmosImagingVariantType,
    GmosNorthBuiltinFpu,
    GmosNorthFilter,
    GmosNorthGrating,
    GmosRoi,
    GmosSouthBuiltinFpu,
    GmosSouthFilter,
    GmosSouthGrating,
    GuideState,
    HiiRegionSpectrum,
    ImageQualityPreset,
    Instrument,
    ObservationValidationCode,
    ObservationWorkflowState,
    ObservingModeType,
    PlanetaryNebulaSpectrum,
    PlanetSpectrum,
    PosAngleConstraintMode,
    QuasarSpectrum,
    ScienceBand,
    ScienceMode,
    SkyBackground,
    StellarLibrarySpectrum,
    TelescopeConfigGeneratorType,
    TimingWindowInclusion,
    WaterVapor,
    WavelengthOrder,
)


class GetGOATSObservations(BaseModel):
    observations: "GetGOATSObservationsObservations"


class GetGOATSObservationsObservations(BaseModel):
    matches: list["GetGOATSObservationsObservationsMatches"]
    has_more: bool = Field(alias="hasMore")


class GetGOATSObservationsObservationsMatches(BaseModel):
    id: Any
    reference: Optional["GetGOATSObservationsObservationsMatchesReference"]
    instrument: Optional[Instrument]
    title: Any
    constraint_set: "GetGOATSObservationsObservationsMatchesConstraintSet" = Field(
        alias="constraintSet"
    )
    workflow: Optional["GetGOATSObservationsObservationsMatchesWorkflow"]
    attachments: list["GetGOATSObservationsObservationsMatchesAttachments"]
    timing_windows: list["GetGOATSObservationsObservationsMatchesTimingWindows"] = (
        Field(alias="timingWindows")
    )
    target_environment: "GetGOATSObservationsObservationsMatchesTargetEnvironment" = (
        Field(alias="targetEnvironment")
    )
    pos_angle_constraint: "GetGOATSObservationsObservationsMatchesPosAngleConstraint" = Field(
        alias="posAngleConstraint"
    )
    science_band: Optional[ScienceBand] = Field(alias="scienceBand")
    observation_duration: Optional[
        "GetGOATSObservationsObservationsMatchesObservationDuration"
    ] = Field(alias="observationDuration")
    observer_notes: Optional[Any] = Field(alias="observerNotes")
    science_requirements: "GetGOATSObservationsObservationsMatchesScienceRequirements" = Field(
        alias="scienceRequirements"
    )
    observing_mode: Optional["GetGOATSObservationsObservationsMatchesObservingMode"] = (
        Field(alias="observingMode")
    )
    program: "GetGOATSObservationsObservationsMatchesProgram"


class GetGOATSObservationsObservationsMatchesReference(BaseModel):
    label: Any


class GetGOATSObservationsObservationsMatchesConstraintSet(BaseModel):
    image_quality: ImageQualityPreset = Field(alias="imageQuality")
    cloud_extinction: CloudExtinctionPreset = Field(alias="cloudExtinction")
    sky_background: SkyBackground = Field(alias="skyBackground")
    water_vapor: WaterVapor = Field(alias="waterVapor")
    elevation_range: "GetGOATSObservationsObservationsMatchesConstraintSetElevationRange" = Field(
        alias="elevationRange"
    )


class GetGOATSObservationsObservationsMatchesConstraintSetElevationRange(BaseModel):
    air_mass: Optional[
        "GetGOATSObservationsObservationsMatchesConstraintSetElevationRangeAirMass"
    ] = Field(alias="airMass")
    hour_angle: Optional[
        "GetGOATSObservationsObservationsMatchesConstraintSetElevationRangeHourAngle"
    ] = Field(alias="hourAngle")


class GetGOATSObservationsObservationsMatchesConstraintSetElevationRangeAirMass(
    BaseModel
):
    min: Any
    max: Any


class GetGOATSObservationsObservationsMatchesConstraintSetElevationRangeHourAngle(
    BaseModel
):
    min_hours: Any = Field(alias="minHours")
    max_hours: Any = Field(alias="maxHours")


class GetGOATSObservationsObservationsMatchesWorkflow(BaseModel):
    calculation_state: CalculationState = Field(alias="calculationState")
    value: "GetGOATSObservationsObservationsMatchesWorkflowValue"


class GetGOATSObservationsObservationsMatchesWorkflowValue(BaseModel):
    state: ObservationWorkflowState
    valid_transitions: list[ObservationWorkflowState] = Field(alias="validTransitions")
    validation_errors: list[
        "GetGOATSObservationsObservationsMatchesWorkflowValueValidationErrors"
    ] = Field(alias="validationErrors")


class GetGOATSObservationsObservationsMatchesWorkflowValueValidationErrors(BaseModel):
    code: ObservationValidationCode


class GetGOATSObservationsObservationsMatchesAttachments(BaseModel):
    id: Any
    attachment_type: AttachmentType = Field(alias="attachmentType")
    file_name: Any = Field(alias="fileName")
    description: Optional[Any]
    updated_at: Any = Field(alias="updatedAt")


class GetGOATSObservationsObservationsMatchesTimingWindows(BaseModel):
    inclusion: TimingWindowInclusion
    start_utc: Any = Field(alias="startUtc")
    end: Optional[
        Annotated[
            Union[
                "GetGOATSObservationsObservationsMatchesTimingWindowsEndTimingWindowEndAt",
                "GetGOATSObservationsObservationsMatchesTimingWindowsEndTimingWindowEndAfter",
            ],
            Field(discriminator="typename__"),
        ]
    ]


class GetGOATSObservationsObservationsMatchesTimingWindowsEndTimingWindowEndAt(
    BaseModel
):
    typename__: Literal["TimingWindowEndAt"] = Field(alias="__typename")
    at_utc: Any = Field(alias="atUtc")


class GetGOATSObservationsObservationsMatchesTimingWindowsEndTimingWindowEndAfter(
    BaseModel
):
    typename__: Literal["TimingWindowEndAfter"] = Field(alias="__typename")
    after: "GetGOATSObservationsObservationsMatchesTimingWindowsEndTimingWindowEndAfterAfter"
    repeat: Optional[
        "GetGOATSObservationsObservationsMatchesTimingWindowsEndTimingWindowEndAfterRepeat"
    ]


class GetGOATSObservationsObservationsMatchesTimingWindowsEndTimingWindowEndAfterAfter(
    BaseModel
):
    seconds: Any


class GetGOATSObservationsObservationsMatchesTimingWindowsEndTimingWindowEndAfterRepeat(
    BaseModel
):
    period: "GetGOATSObservationsObservationsMatchesTimingWindowsEndTimingWindowEndAfterRepeatPeriod"
    times: Optional[Any]


class GetGOATSObservationsObservationsMatchesTimingWindowsEndTimingWindowEndAfterRepeatPeriod(
    BaseModel
):
    seconds: Any


class GetGOATSObservationsObservationsMatchesTargetEnvironment(BaseModel):
    asterism: list["GetGOATSObservationsObservationsMatchesTargetEnvironmentAsterism"]
    first_science_target: Optional[
        "GetGOATSObservationsObservationsMatchesTargetEnvironmentFirstScienceTarget"
    ] = Field(alias="firstScienceTarget")


class GetGOATSObservationsObservationsMatchesTargetEnvironmentAsterism(BaseModel):
    id: Any
    name: Any
    opportunity: Optional[
        "GetGOATSObservationsObservationsMatchesTargetEnvironmentAsterismOpportunity"
    ]


class GetGOATSObservationsObservationsMatchesTargetEnvironmentAsterismOpportunity(
    BaseModel
):
    typename__: Literal["Opportunity"] = Field(alias="__typename")


class GetGOATSObservationsObservationsMatchesTargetEnvironmentFirstScienceTarget(
    BaseModel
):
    id: Any
    name: Any
    opportunity: Optional[
        "GetGOATSObservationsObservationsMatchesTargetEnvironmentFirstScienceTargetOpportunity"
    ]
    sidereal: Optional[
        "GetGOATSObservationsObservationsMatchesTargetEnvironmentFirstScienceTargetSidereal"
    ]
    source_profile: "GetGOATSObservationsObservationsMatchesTargetEnvironmentFirstScienceTargetSourceProfile" = Field(
        alias="sourceProfile"
    )


class GetGOATSObservationsObservationsMatchesTargetEnvironmentFirstScienceTargetOpportunity(
    BaseModel
):
    typename__: Literal["Opportunity"] = Field(alias="__typename")


class GetGOATSObservationsObservationsMatchesTargetEnvironmentFirstScienceTargetSidereal(
    BaseModel
):
    ra: "GetGOATSObservationsObservationsMatchesTargetEnvironmentFirstScienceTargetSiderealRa"
    dec: "GetGOATSObservationsObservationsMatchesTargetEnvironmentFirstScienceTargetSiderealDec"
    proper_motion: Optional[
        "GetGOATSObservationsObservationsMatchesTargetEnvironmentFirstScienceTargetSiderealProperMotion"
    ] = Field(alias="properMotion")
    parallax: Optional[
        "GetGOATSObservationsObservationsMatchesTargetEnvironmentFirstScienceTargetSiderealParallax"
    ]
    radial_velocity: Optional[
        "GetGOATSObservationsObservationsMatchesTargetEnvironmentFirstScienceTargetSiderealRadialVelocity"
    ] = Field(alias="radialVelocity")


class GetGOATSObservationsObservationsMatchesTargetEnvironmentFirstScienceTargetSiderealRa(
    BaseModel
):
    hms: Any
    hours: Any
    degrees: Any


class GetGOATSObservationsObservationsMatchesTargetEnvironmentFirstScienceTargetSiderealDec(
    BaseModel
):
    dms: Any
    degrees: Any


class GetGOATSObservationsObservationsMatchesTargetEnvironmentFirstScienceTargetSiderealProperMotion(
    BaseModel
):
    ra: "GetGOATSObservationsObservationsMatchesTargetEnvironmentFirstScienceTargetSiderealProperMotionRa"
    dec: "GetGOATSObservationsObservationsMatchesTargetEnvironmentFirstScienceTargetSiderealProperMotionDec"


class GetGOATSObservationsObservationsMatchesTargetEnvironmentFirstScienceTargetSiderealProperMotionRa(
    BaseModel
):
    milliarcseconds_per_year: Any = Field(alias="milliarcsecondsPerYear")


class GetGOATSObservationsObservationsMatchesTargetEnvironmentFirstScienceTargetSiderealProperMotionDec(
    BaseModel
):
    milliarcseconds_per_year: Any = Field(alias="milliarcsecondsPerYear")


class GetGOATSObservationsObservationsMatchesTargetEnvironmentFirstScienceTargetSiderealParallax(
    BaseModel
):
    milliarcseconds: Any


class GetGOATSObservationsObservationsMatchesTargetEnvironmentFirstScienceTargetSiderealRadialVelocity(
    BaseModel
):
    kilometers_per_second: Any = Field(alias="kilometersPerSecond")


class GetGOATSObservationsObservationsMatchesTargetEnvironmentFirstScienceTargetSourceProfile(
    BaseModel
):
    point: Optional[
        "GetGOATSObservationsObservationsMatchesTargetEnvironmentFirstScienceTargetSourceProfilePoint"
    ]


class GetGOATSObservationsObservationsMatchesTargetEnvironmentFirstScienceTargetSourceProfilePoint(
    BaseModel
):
    band_normalized: Optional[
        "GetGOATSObservationsObservationsMatchesTargetEnvironmentFirstScienceTargetSourceProfilePointBandNormalized"
    ] = Field(alias="bandNormalized")


class GetGOATSObservationsObservationsMatchesTargetEnvironmentFirstScienceTargetSourceProfilePointBandNormalized(
    BaseModel
):
    brightnesses: list[
        "GetGOATSObservationsObservationsMatchesTargetEnvironmentFirstScienceTargetSourceProfilePointBandNormalizedBrightnesses"
    ]
    sed: Optional[
        "GetGOATSObservationsObservationsMatchesTargetEnvironmentFirstScienceTargetSourceProfilePointBandNormalizedSed"
    ]


class GetGOATSObservationsObservationsMatchesTargetEnvironmentFirstScienceTargetSourceProfilePointBandNormalizedBrightnesses(
    BaseModel
):
    band: Band
    value: Any
    units: BrightnessIntegratedUnits


class GetGOATSObservationsObservationsMatchesTargetEnvironmentFirstScienceTargetSourceProfilePointBandNormalizedSed(
    BaseModel
):
    black_body_temp_k: Optional[Any] = Field(alias="blackBodyTempK")
    cool_star: Optional[CoolStarTemperature] = Field(alias="coolStar")
    flux_densities: Optional[
        list[
            "GetGOATSObservationsObservationsMatchesTargetEnvironmentFirstScienceTargetSourceProfilePointBandNormalizedSedFluxDensities"
        ]
    ] = Field(alias="fluxDensities")
    flux_densities_attachment: Optional[Any] = Field(alias="fluxDensitiesAttachment")
    galaxy: Optional[GalaxySpectrum]
    hii_region: Optional[HiiRegionSpectrum] = Field(alias="hiiRegion")
    planet: Optional[PlanetSpectrum]
    planetary_nebula: Optional[PlanetaryNebulaSpectrum] = Field(alias="planetaryNebula")
    power_law: Optional[Any] = Field(alias="powerLaw")
    quasar: Optional[QuasarSpectrum]
    stellar_library: Optional[StellarLibrarySpectrum] = Field(alias="stellarLibrary")


class GetGOATSObservationsObservationsMatchesTargetEnvironmentFirstScienceTargetSourceProfilePointBandNormalizedSedFluxDensities(
    BaseModel
):
    wavelength: "GetGOATSObservationsObservationsMatchesTargetEnvironmentFirstScienceTargetSourceProfilePointBandNormalizedSedFluxDensitiesWavelength"
    density: Any


class GetGOATSObservationsObservationsMatchesTargetEnvironmentFirstScienceTargetSourceProfilePointBandNormalizedSedFluxDensitiesWavelength(
    BaseModel
):
    nanometers: Any


class GetGOATSObservationsObservationsMatchesPosAngleConstraint(BaseModel):
    mode: PosAngleConstraintMode
    angle: "GetGOATSObservationsObservationsMatchesPosAngleConstraintAngle"


class GetGOATSObservationsObservationsMatchesPosAngleConstraintAngle(BaseModel):
    degrees: Any


class GetGOATSObservationsObservationsMatchesObservationDuration(BaseModel):
    seconds: Any
    minutes: Any
    hours: Any
    iso: str


class GetGOATSObservationsObservationsMatchesScienceRequirements(BaseModel):
    mode: Optional[ScienceMode]
    spectroscopy: Optional[
        "GetGOATSObservationsObservationsMatchesScienceRequirementsSpectroscopy"
    ]
    exposure_time_mode: Optional[
        "GetGOATSObservationsObservationsMatchesScienceRequirementsExposureTimeMode"
    ] = Field(alias="exposureTimeMode")


class GetGOATSObservationsObservationsMatchesScienceRequirementsSpectroscopy(BaseModel):
    wavelength: Optional[
        "GetGOATSObservationsObservationsMatchesScienceRequirementsSpectroscopyWavelength"
    ]


class GetGOATSObservationsObservationsMatchesScienceRequirementsSpectroscopyWavelength(
    BaseModel
):
    nanometers: Any


class GetGOATSObservationsObservationsMatchesScienceRequirementsExposureTimeMode(
    BaseModel
):
    signal_to_noise: Optional[
        "GetGOATSObservationsObservationsMatchesScienceRequirementsExposureTimeModeSignalToNoise"
    ] = Field(alias="signalToNoise")
    time_and_count: Optional[
        "GetGOATSObservationsObservationsMatchesScienceRequirementsExposureTimeModeTimeAndCount"
    ] = Field(alias="timeAndCount")


class GetGOATSObservationsObservationsMatchesScienceRequirementsExposureTimeModeSignalToNoise(
    BaseModel
):
    value: Any
    at: "GetGOATSObservationsObservationsMatchesScienceRequirementsExposureTimeModeSignalToNoiseAt"


class GetGOATSObservationsObservationsMatchesScienceRequirementsExposureTimeModeSignalToNoiseAt(
    BaseModel
):
    nanometers: Any


class GetGOATSObservationsObservationsMatchesScienceRequirementsExposureTimeModeTimeAndCount(
    BaseModel
):
    time: "GetGOATSObservationsObservationsMatchesScienceRequirementsExposureTimeModeTimeAndCountTime"
    count: Any
    at: "GetGOATSObservationsObservationsMatchesScienceRequirementsExposureTimeModeTimeAndCountAt"


class GetGOATSObservationsObservationsMatchesScienceRequirementsExposureTimeModeTimeAndCountTime(
    BaseModel
):
    seconds: Any


class GetGOATSObservationsObservationsMatchesScienceRequirementsExposureTimeModeTimeAndCountAt(
    BaseModel
):
    nanometers: Any


class GetGOATSObservationsObservationsMatchesObservingMode(BaseModel):
    instrument: Instrument
    mode: ObservingModeType
    gmos_north_long_slit: Optional[
        "GetGOATSObservationsObservationsMatchesObservingModeGmosNorthLongSlit"
    ] = Field(alias="gmosNorthLongSlit")
    gmos_south_long_slit: Optional[
        "GetGOATSObservationsObservationsMatchesObservingModeGmosSouthLongSlit"
    ] = Field(alias="gmosSouthLongSlit")
    gmos_north_imaging: Optional[
        "GetGOATSObservationsObservationsMatchesObservingModeGmosNorthImaging"
    ] = Field(alias="gmosNorthImaging")
    gmos_south_imaging: Optional[
        "GetGOATSObservationsObservationsMatchesObservingModeGmosSouthImaging"
    ] = Field(alias="gmosSouthImaging")


class GetGOATSObservationsObservationsMatchesObservingModeGmosNorthLongSlit(BaseModel):
    grating: GmosNorthGrating
    filter_: Optional[GmosNorthFilter] = Field(alias="filter")
    fpu: GmosNorthBuiltinFpu
    central_wavelength: "GetGOATSObservationsObservationsMatchesObservingModeGmosNorthLongSlitCentralWavelength" = Field(
        alias="centralWavelength"
    )
    wavelength_dithers: list[
        "GetGOATSObservationsObservationsMatchesObservingModeGmosNorthLongSlitWavelengthDithers"
    ] = Field(alias="wavelengthDithers")
    x_bin: GmosBinning = Field(alias="xBin")
    y_bin: GmosBinning = Field(alias="yBin")
    amp_read_mode: GmosAmpReadMode = Field(alias="ampReadMode")
    roi: GmosRoi
    exposure_time_mode: "GetGOATSObservationsObservationsMatchesObservingModeGmosNorthLongSlitExposureTimeMode" = Field(
        alias="exposureTimeMode"
    )
    offsets: list[
        "GetGOATSObservationsObservationsMatchesObservingModeGmosNorthLongSlitOffsets"
    ]


class GetGOATSObservationsObservationsMatchesObservingModeGmosNorthLongSlitCentralWavelength(
    BaseModel
):
    nanometers: Any


class GetGOATSObservationsObservationsMatchesObservingModeGmosNorthLongSlitWavelengthDithers(
    BaseModel
):
    nanometers: Any


class GetGOATSObservationsObservationsMatchesObservingModeGmosNorthLongSlitExposureTimeMode(
    BaseModel
):
    signal_to_noise: Optional[
        "GetGOATSObservationsObservationsMatchesObservingModeGmosNorthLongSlitExposureTimeModeSignalToNoise"
    ] = Field(alias="signalToNoise")
    time_and_count: Optional[
        "GetGOATSObservationsObservationsMatchesObservingModeGmosNorthLongSlitExposureTimeModeTimeAndCount"
    ] = Field(alias="timeAndCount")


class GetGOATSObservationsObservationsMatchesObservingModeGmosNorthLongSlitExposureTimeModeSignalToNoise(
    BaseModel
):
    value: Any
    at: "GetGOATSObservationsObservationsMatchesObservingModeGmosNorthLongSlitExposureTimeModeSignalToNoiseAt"


class GetGOATSObservationsObservationsMatchesObservingModeGmosNorthLongSlitExposureTimeModeSignalToNoiseAt(
    BaseModel
):
    nanometers: Any


class GetGOATSObservationsObservationsMatchesObservingModeGmosNorthLongSlitExposureTimeModeTimeAndCount(
    BaseModel
):
    time: "GetGOATSObservationsObservationsMatchesObservingModeGmosNorthLongSlitExposureTimeModeTimeAndCountTime"
    count: Any
    at: "GetGOATSObservationsObservationsMatchesObservingModeGmosNorthLongSlitExposureTimeModeTimeAndCountAt"


class GetGOATSObservationsObservationsMatchesObservingModeGmosNorthLongSlitExposureTimeModeTimeAndCountTime(
    BaseModel
):
    seconds: Any


class GetGOATSObservationsObservationsMatchesObservingModeGmosNorthLongSlitExposureTimeModeTimeAndCountAt(
    BaseModel
):
    nanometers: Any


class GetGOATSObservationsObservationsMatchesObservingModeGmosNorthLongSlitOffsets(
    BaseModel
):
    arcseconds: Any


class GetGOATSObservationsObservationsMatchesObservingModeGmosSouthLongSlit(BaseModel):
    grating: GmosSouthGrating
    filter_: Optional[GmosSouthFilter] = Field(alias="filter")
    fpu: GmosSouthBuiltinFpu
    central_wavelength: "GetGOATSObservationsObservationsMatchesObservingModeGmosSouthLongSlitCentralWavelength" = Field(
        alias="centralWavelength"
    )
    wavelength_dithers: list[
        "GetGOATSObservationsObservationsMatchesObservingModeGmosSouthLongSlitWavelengthDithers"
    ] = Field(alias="wavelengthDithers")
    x_bin: GmosBinning = Field(alias="xBin")
    y_bin: GmosBinning = Field(alias="yBin")
    amp_read_mode: GmosAmpReadMode = Field(alias="ampReadMode")
    roi: GmosRoi
    exposure_time_mode: "GetGOATSObservationsObservationsMatchesObservingModeGmosSouthLongSlitExposureTimeMode" = Field(
        alias="exposureTimeMode"
    )
    offsets: list[
        "GetGOATSObservationsObservationsMatchesObservingModeGmosSouthLongSlitOffsets"
    ]


class GetGOATSObservationsObservationsMatchesObservingModeGmosSouthLongSlitCentralWavelength(
    BaseModel
):
    nanometers: Any


class GetGOATSObservationsObservationsMatchesObservingModeGmosSouthLongSlitWavelengthDithers(
    BaseModel
):
    nanometers: Any


class GetGOATSObservationsObservationsMatchesObservingModeGmosSouthLongSlitExposureTimeMode(
    BaseModel
):
    signal_to_noise: Optional[
        "GetGOATSObservationsObservationsMatchesObservingModeGmosSouthLongSlitExposureTimeModeSignalToNoise"
    ] = Field(alias="signalToNoise")
    time_and_count: Optional[
        "GetGOATSObservationsObservationsMatchesObservingModeGmosSouthLongSlitExposureTimeModeTimeAndCount"
    ] = Field(alias="timeAndCount")


class GetGOATSObservationsObservationsMatchesObservingModeGmosSouthLongSlitExposureTimeModeSignalToNoise(
    BaseModel
):
    value: Any
    at: "GetGOATSObservationsObservationsMatchesObservingModeGmosSouthLongSlitExposureTimeModeSignalToNoiseAt"


class GetGOATSObservationsObservationsMatchesObservingModeGmosSouthLongSlitExposureTimeModeSignalToNoiseAt(
    BaseModel
):
    nanometers: Any


class GetGOATSObservationsObservationsMatchesObservingModeGmosSouthLongSlitExposureTimeModeTimeAndCount(
    BaseModel
):
    time: "GetGOATSObservationsObservationsMatchesObservingModeGmosSouthLongSlitExposureTimeModeTimeAndCountTime"
    count: Any
    at: "GetGOATSObservationsObservationsMatchesObservingModeGmosSouthLongSlitExposureTimeModeTimeAndCountAt"


class GetGOATSObservationsObservationsMatchesObservingModeGmosSouthLongSlitExposureTimeModeTimeAndCountTime(
    BaseModel
):
    seconds: Any


class GetGOATSObservationsObservationsMatchesObservingModeGmosSouthLongSlitExposureTimeModeTimeAndCountAt(
    BaseModel
):
    nanometers: Any


class GetGOATSObservationsObservationsMatchesObservingModeGmosSouthLongSlitOffsets(
    BaseModel
):
    arcseconds: Any


class GetGOATSObservationsObservationsMatchesObservingModeGmosNorthImaging(BaseModel):
    filters: list[
        "GetGOATSObservationsObservationsMatchesObservingModeGmosNorthImagingFilters"
    ]
    amp_read_mode: GmosAmpReadMode = Field(alias="ampReadMode")
    bin: GmosBinning
    roi: GmosRoi
    variant: (
        "GetGOATSObservationsObservationsMatchesObservingModeGmosNorthImagingVariant"
    )


class GetGOATSObservationsObservationsMatchesObservingModeGmosNorthImagingFilters(
    BaseModel
):
    filter_: GmosNorthFilter = Field(alias="filter")
    exposure_time_mode: "GetGOATSObservationsObservationsMatchesObservingModeGmosNorthImagingFiltersExposureTimeMode" = Field(
        alias="exposureTimeMode"
    )


class GetGOATSObservationsObservationsMatchesObservingModeGmosNorthImagingFiltersExposureTimeMode(
    BaseModel
):
    signal_to_noise: Optional[
        "GetGOATSObservationsObservationsMatchesObservingModeGmosNorthImagingFiltersExposureTimeModeSignalToNoise"
    ] = Field(alias="signalToNoise")
    time_and_count: Optional[
        "GetGOATSObservationsObservationsMatchesObservingModeGmosNorthImagingFiltersExposureTimeModeTimeAndCount"
    ] = Field(alias="timeAndCount")


class GetGOATSObservationsObservationsMatchesObservingModeGmosNorthImagingFiltersExposureTimeModeSignalToNoise(
    BaseModel
):
    value: Any
    at: "GetGOATSObservationsObservationsMatchesObservingModeGmosNorthImagingFiltersExposureTimeModeSignalToNoiseAt"


class GetGOATSObservationsObservationsMatchesObservingModeGmosNorthImagingFiltersExposureTimeModeSignalToNoiseAt(
    BaseModel
):
    nanometers: Any


class GetGOATSObservationsObservationsMatchesObservingModeGmosNorthImagingFiltersExposureTimeModeTimeAndCount(
    BaseModel
):
    time: "GetGOATSObservationsObservationsMatchesObservingModeGmosNorthImagingFiltersExposureTimeModeTimeAndCountTime"
    count: Any
    at: "GetGOATSObservationsObservationsMatchesObservingModeGmosNorthImagingFiltersExposureTimeModeTimeAndCountAt"


class GetGOATSObservationsObservationsMatchesObservingModeGmosNorthImagingFiltersExposureTimeModeTimeAndCountTime(
    BaseModel
):
    seconds: Any


class GetGOATSObservationsObservationsMatchesObservingModeGmosNorthImagingFiltersExposureTimeModeTimeAndCountAt(
    BaseModel
):
    nanometers: Any


class GetGOATSObservationsObservationsMatchesObservingModeGmosNorthImagingVariant(
    BaseModel
):
    variant_type: GmosImagingVariantType = Field(alias="variantType")
    grouped: Optional[
        "GetGOATSObservationsObservationsMatchesObservingModeGmosNorthImagingVariantGrouped"
    ]
    interleaved: Optional[
        "GetGOATSObservationsObservationsMatchesObservingModeGmosNorthImagingVariantInterleaved"
    ]
    pre_imaging: Optional[
        "GetGOATSObservationsObservationsMatchesObservingModeGmosNorthImagingVariantPreImaging"
    ] = Field(alias="preImaging")


class GetGOATSObservationsObservationsMatchesObservingModeGmosNorthImagingVariantGrouped(
    BaseModel
):
    sky_count: Any = Field(alias="skyCount")
    sky_offsets: "GetGOATSObservationsObservationsMatchesObservingModeGmosNorthImagingVariantGroupedSkyOffsets" = Field(
        alias="skyOffsets"
    )
    order: WavelengthOrder
    offsets: "GetGOATSObservationsObservationsMatchesObservingModeGmosNorthImagingVariantGroupedOffsets"


class GetGOATSObservationsObservationsMatchesObservingModeGmosNorthImagingVariantGroupedSkyOffsets(
    BaseModel
):
    generator_type: TelescopeConfigGeneratorType = Field(alias="generatorType")
    enumerated: Optional[
        "GetGOATSObservationsObservationsMatchesObservingModeGmosNorthImagingVariantGroupedSkyOffsetsEnumerated"
    ]
    random: Optional[
        "GetGOATSObservationsObservationsMatchesObservingModeGmosNorthImagingVariantGroupedSkyOffsetsRandom"
    ]
    spiral: Optional[
        "GetGOATSObservationsObservationsMatchesObservingModeGmosNorthImagingVariantGroupedSkyOffsetsSpiral"
    ]
    uniform: Optional[
        "GetGOATSObservationsObservationsMatchesObservingModeGmosNorthImagingVariantGroupedSkyOffsetsUniform"
    ]


class GetGOATSObservationsObservationsMatchesObservingModeGmosNorthImagingVariantGroupedSkyOffsetsEnumerated(
    BaseModel
):
    values: list[
        "GetGOATSObservationsObservationsMatchesObservingModeGmosNorthImagingVariantGroupedSkyOffsetsEnumeratedValues"
    ]


class GetGOATSObservationsObservationsMatchesObservingModeGmosNorthImagingVariantGroupedSkyOffsetsEnumeratedValues(
    BaseModel
):
    guiding: GuideState
    offset: "GetGOATSObservationsObservationsMatchesObservingModeGmosNorthImagingVariantGroupedSkyOffsetsEnumeratedValuesOffset"


class GetGOATSObservationsObservationsMatchesObservingModeGmosNorthImagingVariantGroupedSkyOffsetsEnumeratedValuesOffset(
    BaseModel
):
    p: "GetGOATSObservationsObservationsMatchesObservingModeGmosNorthImagingVariantGroupedSkyOffsetsEnumeratedValuesOffsetP"
    q: "GetGOATSObservationsObservationsMatchesObservingModeGmosNorthImagingVariantGroupedSkyOffsetsEnumeratedValuesOffsetQ"


class GetGOATSObservationsObservationsMatchesObservingModeGmosNorthImagingVariantGroupedSkyOffsetsEnumeratedValuesOffsetP(
    BaseModel
):
    arcseconds: Any


class GetGOATSObservationsObservationsMatchesObservingModeGmosNorthImagingVariantGroupedSkyOffsetsEnumeratedValuesOffsetQ(
    BaseModel
):
    arcseconds: Any


class GetGOATSObservationsObservationsMatchesObservingModeGmosNorthImagingVariantGroupedSkyOffsetsRandom(
    BaseModel
):
    seed: Any
    size: "GetGOATSObservationsObservationsMatchesObservingModeGmosNorthImagingVariantGroupedSkyOffsetsRandomSize"
    center: "GetGOATSObservationsObservationsMatchesObservingModeGmosNorthImagingVariantGroupedSkyOffsetsRandomCenter"


class GetGOATSObservationsObservationsMatchesObservingModeGmosNorthImagingVariantGroupedSkyOffsetsRandomSize(
    BaseModel
):
    arcseconds: Any


class GetGOATSObservationsObservationsMatchesObservingModeGmosNorthImagingVariantGroupedSkyOffsetsRandomCenter(
    BaseModel
):
    p: "GetGOATSObservationsObservationsMatchesObservingModeGmosNorthImagingVariantGroupedSkyOffsetsRandomCenterP"
    q: "GetGOATSObservationsObservationsMatchesObservingModeGmosNorthImagingVariantGroupedSkyOffsetsRandomCenterQ"


class GetGOATSObservationsObservationsMatchesObservingModeGmosNorthImagingVariantGroupedSkyOffsetsRandomCenterP(
    BaseModel
):
    arcseconds: Any


class GetGOATSObservationsObservationsMatchesObservingModeGmosNorthImagingVariantGroupedSkyOffsetsRandomCenterQ(
    BaseModel
):
    arcseconds: Any


class GetGOATSObservationsObservationsMatchesObservingModeGmosNorthImagingVariantGroupedSkyOffsetsSpiral(
    BaseModel
):
    seed: Any
    size: "GetGOATSObservationsObservationsMatchesObservingModeGmosNorthImagingVariantGroupedSkyOffsetsSpiralSize"
    center: "GetGOATSObservationsObservationsMatchesObservingModeGmosNorthImagingVariantGroupedSkyOffsetsSpiralCenter"


class GetGOATSObservationsObservationsMatchesObservingModeGmosNorthImagingVariantGroupedSkyOffsetsSpiralSize(
    BaseModel
):
    arcseconds: Any


class GetGOATSObservationsObservationsMatchesObservingModeGmosNorthImagingVariantGroupedSkyOffsetsSpiralCenter(
    BaseModel
):
    p: "GetGOATSObservationsObservationsMatchesObservingModeGmosNorthImagingVariantGroupedSkyOffsetsSpiralCenterP"
    q: "GetGOATSObservationsObservationsMatchesObservingModeGmosNorthImagingVariantGroupedSkyOffsetsSpiralCenterQ"


class GetGOATSObservationsObservationsMatchesObservingModeGmosNorthImagingVariantGroupedSkyOffsetsSpiralCenterP(
    BaseModel
):
    arcseconds: Any


class GetGOATSObservationsObservationsMatchesObservingModeGmosNorthImagingVariantGroupedSkyOffsetsSpiralCenterQ(
    BaseModel
):
    arcseconds: Any


class GetGOATSObservationsObservationsMatchesObservingModeGmosNorthImagingVariantGroupedSkyOffsetsUniform(
    BaseModel
):
    corner_a: "GetGOATSObservationsObservationsMatchesObservingModeGmosNorthImagingVariantGroupedSkyOffsetsUniformCornerA" = Field(
        alias="cornerA"
    )
    corner_b: "GetGOATSObservationsObservationsMatchesObservingModeGmosNorthImagingVariantGroupedSkyOffsetsUniformCornerB" = Field(
        alias="cornerB"
    )


class GetGOATSObservationsObservationsMatchesObservingModeGmosNorthImagingVariantGroupedSkyOffsetsUniformCornerA(
    BaseModel
):
    p: "GetGOATSObservationsObservationsMatchesObservingModeGmosNorthImagingVariantGroupedSkyOffsetsUniformCornerAP"
    q: "GetGOATSObservationsObservationsMatchesObservingModeGmosNorthImagingVariantGroupedSkyOffsetsUniformCornerAQ"


class GetGOATSObservationsObservationsMatchesObservingModeGmosNorthImagingVariantGroupedSkyOffsetsUniformCornerAP(
    BaseModel
):
    arcseconds: Any


class GetGOATSObservationsObservationsMatchesObservingModeGmosNorthImagingVariantGroupedSkyOffsetsUniformCornerAQ(
    BaseModel
):
    arcseconds: Any


class GetGOATSObservationsObservationsMatchesObservingModeGmosNorthImagingVariantGroupedSkyOffsetsUniformCornerB(
    BaseModel
):
    p: "GetGOATSObservationsObservationsMatchesObservingModeGmosNorthImagingVariantGroupedSkyOffsetsUniformCornerBP"
    q: "GetGOATSObservationsObservationsMatchesObservingModeGmosNorthImagingVariantGroupedSkyOffsetsUniformCornerBQ"


class GetGOATSObservationsObservationsMatchesObservingModeGmosNorthImagingVariantGroupedSkyOffsetsUniformCornerBP(
    BaseModel
):
    arcseconds: Any


class GetGOATSObservationsObservationsMatchesObservingModeGmosNorthImagingVariantGroupedSkyOffsetsUniformCornerBQ(
    BaseModel
):
    arcseconds: Any


class GetGOATSObservationsObservationsMatchesObservingModeGmosNorthImagingVariantGroupedOffsets(
    BaseModel
):
    generator_type: TelescopeConfigGeneratorType = Field(alias="generatorType")
    random: Optional[
        "GetGOATSObservationsObservationsMatchesObservingModeGmosNorthImagingVariantGroupedOffsetsRandom"
    ]
    spiral: Optional[
        "GetGOATSObservationsObservationsMatchesObservingModeGmosNorthImagingVariantGroupedOffsetsSpiral"
    ]
    uniform: Optional[
        "GetGOATSObservationsObservationsMatchesObservingModeGmosNorthImagingVariantGroupedOffsetsUniform"
    ]
    enumerated: Optional[
        "GetGOATSObservationsObservationsMatchesObservingModeGmosNorthImagingVariantGroupedOffsetsEnumerated"
    ]


class GetGOATSObservationsObservationsMatchesObservingModeGmosNorthImagingVariantGroupedOffsetsRandom(
    BaseModel
):
    seed: Any
    size: "GetGOATSObservationsObservationsMatchesObservingModeGmosNorthImagingVariantGroupedOffsetsRandomSize"
    center: "GetGOATSObservationsObservationsMatchesObservingModeGmosNorthImagingVariantGroupedOffsetsRandomCenter"


class GetGOATSObservationsObservationsMatchesObservingModeGmosNorthImagingVariantGroupedOffsetsRandomSize(
    BaseModel
):
    arcseconds: Any


class GetGOATSObservationsObservationsMatchesObservingModeGmosNorthImagingVariantGroupedOffsetsRandomCenter(
    BaseModel
):
    p: "GetGOATSObservationsObservationsMatchesObservingModeGmosNorthImagingVariantGroupedOffsetsRandomCenterP"
    q: "GetGOATSObservationsObservationsMatchesObservingModeGmosNorthImagingVariantGroupedOffsetsRandomCenterQ"


class GetGOATSObservationsObservationsMatchesObservingModeGmosNorthImagingVariantGroupedOffsetsRandomCenterP(
    BaseModel
):
    arcseconds: Any


class GetGOATSObservationsObservationsMatchesObservingModeGmosNorthImagingVariantGroupedOffsetsRandomCenterQ(
    BaseModel
):
    arcseconds: Any


class GetGOATSObservationsObservationsMatchesObservingModeGmosNorthImagingVariantGroupedOffsetsSpiral(
    BaseModel
):
    seed: Any
    size: "GetGOATSObservationsObservationsMatchesObservingModeGmosNorthImagingVariantGroupedOffsetsSpiralSize"
    center: "GetGOATSObservationsObservationsMatchesObservingModeGmosNorthImagingVariantGroupedOffsetsSpiralCenter"


class GetGOATSObservationsObservationsMatchesObservingModeGmosNorthImagingVariantGroupedOffsetsSpiralSize(
    BaseModel
):
    arcseconds: Any


class GetGOATSObservationsObservationsMatchesObservingModeGmosNorthImagingVariantGroupedOffsetsSpiralCenter(
    BaseModel
):
    p: "GetGOATSObservationsObservationsMatchesObservingModeGmosNorthImagingVariantGroupedOffsetsSpiralCenterP"
    q: "GetGOATSObservationsObservationsMatchesObservingModeGmosNorthImagingVariantGroupedOffsetsSpiralCenterQ"


class GetGOATSObservationsObservationsMatchesObservingModeGmosNorthImagingVariantGroupedOffsetsSpiralCenterP(
    BaseModel
):
    arcseconds: Any


class GetGOATSObservationsObservationsMatchesObservingModeGmosNorthImagingVariantGroupedOffsetsSpiralCenterQ(
    BaseModel
):
    arcseconds: Any


class GetGOATSObservationsObservationsMatchesObservingModeGmosNorthImagingVariantGroupedOffsetsUniform(
    BaseModel
):
    corner_a: "GetGOATSObservationsObservationsMatchesObservingModeGmosNorthImagingVariantGroupedOffsetsUniformCornerA" = Field(
        alias="cornerA"
    )
    corner_b: "GetGOATSObservationsObservationsMatchesObservingModeGmosNorthImagingVariantGroupedOffsetsUniformCornerB" = Field(
        alias="cornerB"
    )


class GetGOATSObservationsObservationsMatchesObservingModeGmosNorthImagingVariantGroupedOffsetsUniformCornerA(
    BaseModel
):
    p: "GetGOATSObservationsObservationsMatchesObservingModeGmosNorthImagingVariantGroupedOffsetsUniformCornerAP"
    q: "GetGOATSObservationsObservationsMatchesObservingModeGmosNorthImagingVariantGroupedOffsetsUniformCornerAQ"


class GetGOATSObservationsObservationsMatchesObservingModeGmosNorthImagingVariantGroupedOffsetsUniformCornerAP(
    BaseModel
):
    arcseconds: Any


class GetGOATSObservationsObservationsMatchesObservingModeGmosNorthImagingVariantGroupedOffsetsUniformCornerAQ(
    BaseModel
):
    arcseconds: Any


class GetGOATSObservationsObservationsMatchesObservingModeGmosNorthImagingVariantGroupedOffsetsUniformCornerB(
    BaseModel
):
    p: "GetGOATSObservationsObservationsMatchesObservingModeGmosNorthImagingVariantGroupedOffsetsUniformCornerBP"
    q: "GetGOATSObservationsObservationsMatchesObservingModeGmosNorthImagingVariantGroupedOffsetsUniformCornerBQ"


class GetGOATSObservationsObservationsMatchesObservingModeGmosNorthImagingVariantGroupedOffsetsUniformCornerBP(
    BaseModel
):
    arcseconds: Any


class GetGOATSObservationsObservationsMatchesObservingModeGmosNorthImagingVariantGroupedOffsetsUniformCornerBQ(
    BaseModel
):
    arcseconds: Any


class GetGOATSObservationsObservationsMatchesObservingModeGmosNorthImagingVariantGroupedOffsetsEnumerated(
    BaseModel
):
    values: list[
        "GetGOATSObservationsObservationsMatchesObservingModeGmosNorthImagingVariantGroupedOffsetsEnumeratedValues"
    ]


class GetGOATSObservationsObservationsMatchesObservingModeGmosNorthImagingVariantGroupedOffsetsEnumeratedValues(
    BaseModel
):
    guiding: GuideState
    offset: "GetGOATSObservationsObservationsMatchesObservingModeGmosNorthImagingVariantGroupedOffsetsEnumeratedValuesOffset"


class GetGOATSObservationsObservationsMatchesObservingModeGmosNorthImagingVariantGroupedOffsetsEnumeratedValuesOffset(
    BaseModel
):
    p: "GetGOATSObservationsObservationsMatchesObservingModeGmosNorthImagingVariantGroupedOffsetsEnumeratedValuesOffsetP"
    q: "GetGOATSObservationsObservationsMatchesObservingModeGmosNorthImagingVariantGroupedOffsetsEnumeratedValuesOffsetQ"


class GetGOATSObservationsObservationsMatchesObservingModeGmosNorthImagingVariantGroupedOffsetsEnumeratedValuesOffsetP(
    BaseModel
):
    arcseconds: Any


class GetGOATSObservationsObservationsMatchesObservingModeGmosNorthImagingVariantGroupedOffsetsEnumeratedValuesOffsetQ(
    BaseModel
):
    arcseconds: Any


class GetGOATSObservationsObservationsMatchesObservingModeGmosNorthImagingVariantInterleaved(
    BaseModel
):
    offsets: "GetGOATSObservationsObservationsMatchesObservingModeGmosNorthImagingVariantInterleavedOffsets"
    sky_count: Any = Field(alias="skyCount")
    sky_offsets: "GetGOATSObservationsObservationsMatchesObservingModeGmosNorthImagingVariantInterleavedSkyOffsets" = Field(
        alias="skyOffsets"
    )


class GetGOATSObservationsObservationsMatchesObservingModeGmosNorthImagingVariantInterleavedOffsets(
    BaseModel
):
    generator_type: TelescopeConfigGeneratorType = Field(alias="generatorType")
    enumerated: Optional[
        "GetGOATSObservationsObservationsMatchesObservingModeGmosNorthImagingVariantInterleavedOffsetsEnumerated"
    ]
    random: Optional[
        "GetGOATSObservationsObservationsMatchesObservingModeGmosNorthImagingVariantInterleavedOffsetsRandom"
    ]
    spiral: Optional[
        "GetGOATSObservationsObservationsMatchesObservingModeGmosNorthImagingVariantInterleavedOffsetsSpiral"
    ]
    uniform: Optional[
        "GetGOATSObservationsObservationsMatchesObservingModeGmosNorthImagingVariantInterleavedOffsetsUniform"
    ]


class GetGOATSObservationsObservationsMatchesObservingModeGmosNorthImagingVariantInterleavedOffsetsEnumerated(
    BaseModel
):
    values: list[
        "GetGOATSObservationsObservationsMatchesObservingModeGmosNorthImagingVariantInterleavedOffsetsEnumeratedValues"
    ]


class GetGOATSObservationsObservationsMatchesObservingModeGmosNorthImagingVariantInterleavedOffsetsEnumeratedValues(
    BaseModel
):
    guiding: GuideState
    offset: "GetGOATSObservationsObservationsMatchesObservingModeGmosNorthImagingVariantInterleavedOffsetsEnumeratedValuesOffset"


class GetGOATSObservationsObservationsMatchesObservingModeGmosNorthImagingVariantInterleavedOffsetsEnumeratedValuesOffset(
    BaseModel
):
    p: "GetGOATSObservationsObservationsMatchesObservingModeGmosNorthImagingVariantInterleavedOffsetsEnumeratedValuesOffsetP"
    q: "GetGOATSObservationsObservationsMatchesObservingModeGmosNorthImagingVariantInterleavedOffsetsEnumeratedValuesOffsetQ"


class GetGOATSObservationsObservationsMatchesObservingModeGmosNorthImagingVariantInterleavedOffsetsEnumeratedValuesOffsetP(
    BaseModel
):
    arcseconds: Any


class GetGOATSObservationsObservationsMatchesObservingModeGmosNorthImagingVariantInterleavedOffsetsEnumeratedValuesOffsetQ(
    BaseModel
):
    arcseconds: Any


class GetGOATSObservationsObservationsMatchesObservingModeGmosNorthImagingVariantInterleavedOffsetsRandom(
    BaseModel
):
    seed: Any
    size: "GetGOATSObservationsObservationsMatchesObservingModeGmosNorthImagingVariantInterleavedOffsetsRandomSize"
    center: "GetGOATSObservationsObservationsMatchesObservingModeGmosNorthImagingVariantInterleavedOffsetsRandomCenter"


class GetGOATSObservationsObservationsMatchesObservingModeGmosNorthImagingVariantInterleavedOffsetsRandomSize(
    BaseModel
):
    arcseconds: Any


class GetGOATSObservationsObservationsMatchesObservingModeGmosNorthImagingVariantInterleavedOffsetsRandomCenter(
    BaseModel
):
    p: "GetGOATSObservationsObservationsMatchesObservingModeGmosNorthImagingVariantInterleavedOffsetsRandomCenterP"
    q: "GetGOATSObservationsObservationsMatchesObservingModeGmosNorthImagingVariantInterleavedOffsetsRandomCenterQ"


class GetGOATSObservationsObservationsMatchesObservingModeGmosNorthImagingVariantInterleavedOffsetsRandomCenterP(
    BaseModel
):
    arcseconds: Any


class GetGOATSObservationsObservationsMatchesObservingModeGmosNorthImagingVariantInterleavedOffsetsRandomCenterQ(
    BaseModel
):
    arcseconds: Any


class GetGOATSObservationsObservationsMatchesObservingModeGmosNorthImagingVariantInterleavedOffsetsSpiral(
    BaseModel
):
    seed: Any
    size: "GetGOATSObservationsObservationsMatchesObservingModeGmosNorthImagingVariantInterleavedOffsetsSpiralSize"
    center: "GetGOATSObservationsObservationsMatchesObservingModeGmosNorthImagingVariantInterleavedOffsetsSpiralCenter"


class GetGOATSObservationsObservationsMatchesObservingModeGmosNorthImagingVariantInterleavedOffsetsSpiralSize(
    BaseModel
):
    arcseconds: Any


class GetGOATSObservationsObservationsMatchesObservingModeGmosNorthImagingVariantInterleavedOffsetsSpiralCenter(
    BaseModel
):
    p: "GetGOATSObservationsObservationsMatchesObservingModeGmosNorthImagingVariantInterleavedOffsetsSpiralCenterP"
    q: "GetGOATSObservationsObservationsMatchesObservingModeGmosNorthImagingVariantInterleavedOffsetsSpiralCenterQ"


class GetGOATSObservationsObservationsMatchesObservingModeGmosNorthImagingVariantInterleavedOffsetsSpiralCenterP(
    BaseModel
):
    arcseconds: Any


class GetGOATSObservationsObservationsMatchesObservingModeGmosNorthImagingVariantInterleavedOffsetsSpiralCenterQ(
    BaseModel
):
    arcseconds: Any


class GetGOATSObservationsObservationsMatchesObservingModeGmosNorthImagingVariantInterleavedOffsetsUniform(
    BaseModel
):
    corner_a: "GetGOATSObservationsObservationsMatchesObservingModeGmosNorthImagingVariantInterleavedOffsetsUniformCornerA" = Field(
        alias="cornerA"
    )
    corner_b: "GetGOATSObservationsObservationsMatchesObservingModeGmosNorthImagingVariantInterleavedOffsetsUniformCornerB" = Field(
        alias="cornerB"
    )


class GetGOATSObservationsObservationsMatchesObservingModeGmosNorthImagingVariantInterleavedOffsetsUniformCornerA(
    BaseModel
):
    p: "GetGOATSObservationsObservationsMatchesObservingModeGmosNorthImagingVariantInterleavedOffsetsUniformCornerAP"
    q: "GetGOATSObservationsObservationsMatchesObservingModeGmosNorthImagingVariantInterleavedOffsetsUniformCornerAQ"


class GetGOATSObservationsObservationsMatchesObservingModeGmosNorthImagingVariantInterleavedOffsetsUniformCornerAP(
    BaseModel
):
    arcseconds: Any


class GetGOATSObservationsObservationsMatchesObservingModeGmosNorthImagingVariantInterleavedOffsetsUniformCornerAQ(
    BaseModel
):
    arcseconds: Any


class GetGOATSObservationsObservationsMatchesObservingModeGmosNorthImagingVariantInterleavedOffsetsUniformCornerB(
    BaseModel
):
    p: "GetGOATSObservationsObservationsMatchesObservingModeGmosNorthImagingVariantInterleavedOffsetsUniformCornerBP"
    q: "GetGOATSObservationsObservationsMatchesObservingModeGmosNorthImagingVariantInterleavedOffsetsUniformCornerBQ"


class GetGOATSObservationsObservationsMatchesObservingModeGmosNorthImagingVariantInterleavedOffsetsUniformCornerBP(
    BaseModel
):
    arcseconds: Any


class GetGOATSObservationsObservationsMatchesObservingModeGmosNorthImagingVariantInterleavedOffsetsUniformCornerBQ(
    BaseModel
):
    arcseconds: Any


class GetGOATSObservationsObservationsMatchesObservingModeGmosNorthImagingVariantInterleavedSkyOffsets(
    BaseModel
):
    generator_type: TelescopeConfigGeneratorType = Field(alias="generatorType")
    enumerated: Optional[
        "GetGOATSObservationsObservationsMatchesObservingModeGmosNorthImagingVariantInterleavedSkyOffsetsEnumerated"
    ]
    random: Optional[
        "GetGOATSObservationsObservationsMatchesObservingModeGmosNorthImagingVariantInterleavedSkyOffsetsRandom"
    ]
    spiral: Optional[
        "GetGOATSObservationsObservationsMatchesObservingModeGmosNorthImagingVariantInterleavedSkyOffsetsSpiral"
    ]
    uniform: Optional[
        "GetGOATSObservationsObservationsMatchesObservingModeGmosNorthImagingVariantInterleavedSkyOffsetsUniform"
    ]


class GetGOATSObservationsObservationsMatchesObservingModeGmosNorthImagingVariantInterleavedSkyOffsetsEnumerated(
    BaseModel
):
    values: list[
        "GetGOATSObservationsObservationsMatchesObservingModeGmosNorthImagingVariantInterleavedSkyOffsetsEnumeratedValues"
    ]


class GetGOATSObservationsObservationsMatchesObservingModeGmosNorthImagingVariantInterleavedSkyOffsetsEnumeratedValues(
    BaseModel
):
    guiding: GuideState
    offset: "GetGOATSObservationsObservationsMatchesObservingModeGmosNorthImagingVariantInterleavedSkyOffsetsEnumeratedValuesOffset"


class GetGOATSObservationsObservationsMatchesObservingModeGmosNorthImagingVariantInterleavedSkyOffsetsEnumeratedValuesOffset(
    BaseModel
):
    p: "GetGOATSObservationsObservationsMatchesObservingModeGmosNorthImagingVariantInterleavedSkyOffsetsEnumeratedValuesOffsetP"
    q: "GetGOATSObservationsObservationsMatchesObservingModeGmosNorthImagingVariantInterleavedSkyOffsetsEnumeratedValuesOffsetQ"


class GetGOATSObservationsObservationsMatchesObservingModeGmosNorthImagingVariantInterleavedSkyOffsetsEnumeratedValuesOffsetP(
    BaseModel
):
    arcseconds: Any


class GetGOATSObservationsObservationsMatchesObservingModeGmosNorthImagingVariantInterleavedSkyOffsetsEnumeratedValuesOffsetQ(
    BaseModel
):
    arcseconds: Any


class GetGOATSObservationsObservationsMatchesObservingModeGmosNorthImagingVariantInterleavedSkyOffsetsRandom(
    BaseModel
):
    seed: Any
    size: "GetGOATSObservationsObservationsMatchesObservingModeGmosNorthImagingVariantInterleavedSkyOffsetsRandomSize"
    center: "GetGOATSObservationsObservationsMatchesObservingModeGmosNorthImagingVariantInterleavedSkyOffsetsRandomCenter"


class GetGOATSObservationsObservationsMatchesObservingModeGmosNorthImagingVariantInterleavedSkyOffsetsRandomSize(
    BaseModel
):
    arcseconds: Any


class GetGOATSObservationsObservationsMatchesObservingModeGmosNorthImagingVariantInterleavedSkyOffsetsRandomCenter(
    BaseModel
):
    p: "GetGOATSObservationsObservationsMatchesObservingModeGmosNorthImagingVariantInterleavedSkyOffsetsRandomCenterP"
    q: "GetGOATSObservationsObservationsMatchesObservingModeGmosNorthImagingVariantInterleavedSkyOffsetsRandomCenterQ"


class GetGOATSObservationsObservationsMatchesObservingModeGmosNorthImagingVariantInterleavedSkyOffsetsRandomCenterP(
    BaseModel
):
    arcseconds: Any


class GetGOATSObservationsObservationsMatchesObservingModeGmosNorthImagingVariantInterleavedSkyOffsetsRandomCenterQ(
    BaseModel
):
    arcseconds: Any


class GetGOATSObservationsObservationsMatchesObservingModeGmosNorthImagingVariantInterleavedSkyOffsetsSpiral(
    BaseModel
):
    seed: Any
    size: "GetGOATSObservationsObservationsMatchesObservingModeGmosNorthImagingVariantInterleavedSkyOffsetsSpiralSize"
    center: "GetGOATSObservationsObservationsMatchesObservingModeGmosNorthImagingVariantInterleavedSkyOffsetsSpiralCenter"


class GetGOATSObservationsObservationsMatchesObservingModeGmosNorthImagingVariantInterleavedSkyOffsetsSpiralSize(
    BaseModel
):
    arcseconds: Any


class GetGOATSObservationsObservationsMatchesObservingModeGmosNorthImagingVariantInterleavedSkyOffsetsSpiralCenter(
    BaseModel
):
    p: "GetGOATSObservationsObservationsMatchesObservingModeGmosNorthImagingVariantInterleavedSkyOffsetsSpiralCenterP"
    q: "GetGOATSObservationsObservationsMatchesObservingModeGmosNorthImagingVariantInterleavedSkyOffsetsSpiralCenterQ"


class GetGOATSObservationsObservationsMatchesObservingModeGmosNorthImagingVariantInterleavedSkyOffsetsSpiralCenterP(
    BaseModel
):
    arcseconds: Any


class GetGOATSObservationsObservationsMatchesObservingModeGmosNorthImagingVariantInterleavedSkyOffsetsSpiralCenterQ(
    BaseModel
):
    arcseconds: Any


class GetGOATSObservationsObservationsMatchesObservingModeGmosNorthImagingVariantInterleavedSkyOffsetsUniform(
    BaseModel
):
    corner_a: "GetGOATSObservationsObservationsMatchesObservingModeGmosNorthImagingVariantInterleavedSkyOffsetsUniformCornerA" = Field(
        alias="cornerA"
    )
    corner_b: "GetGOATSObservationsObservationsMatchesObservingModeGmosNorthImagingVariantInterleavedSkyOffsetsUniformCornerB" = Field(
        alias="cornerB"
    )


class GetGOATSObservationsObservationsMatchesObservingModeGmosNorthImagingVariantInterleavedSkyOffsetsUniformCornerA(
    BaseModel
):
    p: "GetGOATSObservationsObservationsMatchesObservingModeGmosNorthImagingVariantInterleavedSkyOffsetsUniformCornerAP"
    q: "GetGOATSObservationsObservationsMatchesObservingModeGmosNorthImagingVariantInterleavedSkyOffsetsUniformCornerAQ"


class GetGOATSObservationsObservationsMatchesObservingModeGmosNorthImagingVariantInterleavedSkyOffsetsUniformCornerAP(
    BaseModel
):
    arcseconds: Any


class GetGOATSObservationsObservationsMatchesObservingModeGmosNorthImagingVariantInterleavedSkyOffsetsUniformCornerAQ(
    BaseModel
):
    arcseconds: Any


class GetGOATSObservationsObservationsMatchesObservingModeGmosNorthImagingVariantInterleavedSkyOffsetsUniformCornerB(
    BaseModel
):
    p: "GetGOATSObservationsObservationsMatchesObservingModeGmosNorthImagingVariantInterleavedSkyOffsetsUniformCornerBP"
    q: "GetGOATSObservationsObservationsMatchesObservingModeGmosNorthImagingVariantInterleavedSkyOffsetsUniformCornerBQ"


class GetGOATSObservationsObservationsMatchesObservingModeGmosNorthImagingVariantInterleavedSkyOffsetsUniformCornerBP(
    BaseModel
):
    arcseconds: Any


class GetGOATSObservationsObservationsMatchesObservingModeGmosNorthImagingVariantInterleavedSkyOffsetsUniformCornerBQ(
    BaseModel
):
    arcseconds: Any


class GetGOATSObservationsObservationsMatchesObservingModeGmosNorthImagingVariantPreImaging(
    BaseModel
):
    offset_1: "GetGOATSObservationsObservationsMatchesObservingModeGmosNorthImagingVariantPreImagingOffset1" = Field(
        alias="offset1"
    )
    offset_2: "GetGOATSObservationsObservationsMatchesObservingModeGmosNorthImagingVariantPreImagingOffset2" = Field(
        alias="offset2"
    )
    offset_3: "GetGOATSObservationsObservationsMatchesObservingModeGmosNorthImagingVariantPreImagingOffset3" = Field(
        alias="offset3"
    )
    offset_4: "GetGOATSObservationsObservationsMatchesObservingModeGmosNorthImagingVariantPreImagingOffset4" = Field(
        alias="offset4"
    )


class GetGOATSObservationsObservationsMatchesObservingModeGmosNorthImagingVariantPreImagingOffset1(
    BaseModel
):
    p: "GetGOATSObservationsObservationsMatchesObservingModeGmosNorthImagingVariantPreImagingOffset1P"
    q: "GetGOATSObservationsObservationsMatchesObservingModeGmosNorthImagingVariantPreImagingOffset1Q"


class GetGOATSObservationsObservationsMatchesObservingModeGmosNorthImagingVariantPreImagingOffset1P(
    BaseModel
):
    arcseconds: Any


class GetGOATSObservationsObservationsMatchesObservingModeGmosNorthImagingVariantPreImagingOffset1Q(
    BaseModel
):
    arcseconds: Any


class GetGOATSObservationsObservationsMatchesObservingModeGmosNorthImagingVariantPreImagingOffset2(
    BaseModel
):
    p: "GetGOATSObservationsObservationsMatchesObservingModeGmosNorthImagingVariantPreImagingOffset2P"
    q: "GetGOATSObservationsObservationsMatchesObservingModeGmosNorthImagingVariantPreImagingOffset2Q"


class GetGOATSObservationsObservationsMatchesObservingModeGmosNorthImagingVariantPreImagingOffset2P(
    BaseModel
):
    arcseconds: Any


class GetGOATSObservationsObservationsMatchesObservingModeGmosNorthImagingVariantPreImagingOffset2Q(
    BaseModel
):
    arcseconds: Any


class GetGOATSObservationsObservationsMatchesObservingModeGmosNorthImagingVariantPreImagingOffset3(
    BaseModel
):
    p: "GetGOATSObservationsObservationsMatchesObservingModeGmosNorthImagingVariantPreImagingOffset3P"
    q: "GetGOATSObservationsObservationsMatchesObservingModeGmosNorthImagingVariantPreImagingOffset3Q"


class GetGOATSObservationsObservationsMatchesObservingModeGmosNorthImagingVariantPreImagingOffset3P(
    BaseModel
):
    arcseconds: Any


class GetGOATSObservationsObservationsMatchesObservingModeGmosNorthImagingVariantPreImagingOffset3Q(
    BaseModel
):
    arcseconds: Any


class GetGOATSObservationsObservationsMatchesObservingModeGmosNorthImagingVariantPreImagingOffset4(
    BaseModel
):
    p: "GetGOATSObservationsObservationsMatchesObservingModeGmosNorthImagingVariantPreImagingOffset4P"
    q: "GetGOATSObservationsObservationsMatchesObservingModeGmosNorthImagingVariantPreImagingOffset4Q"


class GetGOATSObservationsObservationsMatchesObservingModeGmosNorthImagingVariantPreImagingOffset4P(
    BaseModel
):
    arcseconds: Any


class GetGOATSObservationsObservationsMatchesObservingModeGmosNorthImagingVariantPreImagingOffset4Q(
    BaseModel
):
    arcseconds: Any


class GetGOATSObservationsObservationsMatchesObservingModeGmosSouthImaging(BaseModel):
    filters: list[
        "GetGOATSObservationsObservationsMatchesObservingModeGmosSouthImagingFilters"
    ]
    amp_read_mode: GmosAmpReadMode = Field(alias="ampReadMode")
    bin: GmosBinning
    roi: GmosRoi
    variant: (
        "GetGOATSObservationsObservationsMatchesObservingModeGmosSouthImagingVariant"
    )
    amp_read_mode: GmosAmpReadMode = Field(alias="ampReadMode")
    bin: GmosBinning
    roi: GmosRoi
    variant: (
        "GetGOATSObservationsObservationsMatchesObservingModeGmosSouthImagingVariant"
    )


class GetGOATSObservationsObservationsMatchesObservingModeGmosSouthImagingFilters(
    BaseModel
):
    filter_: GmosSouthFilter = Field(alias="filter")
    exposure_time_mode: "GetGOATSObservationsObservationsMatchesObservingModeGmosSouthImagingFiltersExposureTimeMode" = Field(
        alias="exposureTimeMode"
    )


class GetGOATSObservationsObservationsMatchesObservingModeGmosSouthImagingFiltersExposureTimeMode(
    BaseModel
):
    signal_to_noise: Optional[
        "GetGOATSObservationsObservationsMatchesObservingModeGmosSouthImagingFiltersExposureTimeModeSignalToNoise"
    ] = Field(alias="signalToNoise")
    time_and_count: Optional[
        "GetGOATSObservationsObservationsMatchesObservingModeGmosSouthImagingFiltersExposureTimeModeTimeAndCount"
    ] = Field(alias="timeAndCount")


class GetGOATSObservationsObservationsMatchesObservingModeGmosSouthImagingFiltersExposureTimeModeSignalToNoise(
    BaseModel
):
    value: Any
    at: "GetGOATSObservationsObservationsMatchesObservingModeGmosSouthImagingFiltersExposureTimeModeSignalToNoiseAt"


class GetGOATSObservationsObservationsMatchesObservingModeGmosSouthImagingFiltersExposureTimeModeSignalToNoiseAt(
    BaseModel
):
    nanometers: Any


class GetGOATSObservationsObservationsMatchesObservingModeGmosSouthImagingFiltersExposureTimeModeTimeAndCount(
    BaseModel
):
    time: "GetGOATSObservationsObservationsMatchesObservingModeGmosSouthImagingFiltersExposureTimeModeTimeAndCountTime"
    count: Any
    at: "GetGOATSObservationsObservationsMatchesObservingModeGmosSouthImagingFiltersExposureTimeModeTimeAndCountAt"


class GetGOATSObservationsObservationsMatchesObservingModeGmosSouthImagingFiltersExposureTimeModeTimeAndCountTime(
    BaseModel
):
    seconds: Any


class GetGOATSObservationsObservationsMatchesObservingModeGmosSouthImagingFiltersExposureTimeModeTimeAndCountAt(
    BaseModel
):
    nanometers: Any


class GetGOATSObservationsObservationsMatchesObservingModeGmosSouthImagingVariant(
    BaseModel
):
    variant_type: GmosImagingVariantType = Field(alias="variantType")
    grouped: Optional[
        "GetGOATSObservationsObservationsMatchesObservingModeGmosSouthImagingVariantGrouped"
    ]
    interleaved: Optional[
        "GetGOATSObservationsObservationsMatchesObservingModeGmosSouthImagingVariantInterleaved"
    ]
    pre_imaging: Optional[
        "GetGOATSObservationsObservationsMatchesObservingModeGmosSouthImagingVariantPreImaging"
    ] = Field(alias="preImaging")


class GetGOATSObservationsObservationsMatchesObservingModeGmosSouthImagingVariantGrouped(
    BaseModel
):
    sky_count: Any = Field(alias="skyCount")
    sky_offsets: "GetGOATSObservationsObservationsMatchesObservingModeGmosSouthImagingVariantGroupedSkyOffsets" = Field(
        alias="skyOffsets"
    )
    order: WavelengthOrder
    offsets: "GetGOATSObservationsObservationsMatchesObservingModeGmosSouthImagingVariantGroupedOffsets"


class GetGOATSObservationsObservationsMatchesObservingModeGmosSouthImagingVariantGroupedSkyOffsets(
    BaseModel
):
    generator_type: TelescopeConfigGeneratorType = Field(alias="generatorType")
    enumerated: Optional[
        "GetGOATSObservationsObservationsMatchesObservingModeGmosSouthImagingVariantGroupedSkyOffsetsEnumerated"
    ]
    random: Optional[
        "GetGOATSObservationsObservationsMatchesObservingModeGmosSouthImagingVariantGroupedSkyOffsetsRandom"
    ]
    spiral: Optional[
        "GetGOATSObservationsObservationsMatchesObservingModeGmosSouthImagingVariantGroupedSkyOffsetsSpiral"
    ]
    uniform: Optional[
        "GetGOATSObservationsObservationsMatchesObservingModeGmosSouthImagingVariantGroupedSkyOffsetsUniform"
    ]


class GetGOATSObservationsObservationsMatchesObservingModeGmosSouthImagingVariantGroupedSkyOffsetsEnumerated(
    BaseModel
):
    values: list[
        "GetGOATSObservationsObservationsMatchesObservingModeGmosSouthImagingVariantGroupedSkyOffsetsEnumeratedValues"
    ]


class GetGOATSObservationsObservationsMatchesObservingModeGmosSouthImagingVariantGroupedSkyOffsetsEnumeratedValues(
    BaseModel
):
    guiding: GuideState
    offset: "GetGOATSObservationsObservationsMatchesObservingModeGmosSouthImagingVariantGroupedSkyOffsetsEnumeratedValuesOffset"


class GetGOATSObservationsObservationsMatchesObservingModeGmosSouthImagingVariantGroupedSkyOffsetsEnumeratedValuesOffset(
    BaseModel
):
    p: "GetGOATSObservationsObservationsMatchesObservingModeGmosSouthImagingVariantGroupedSkyOffsetsEnumeratedValuesOffsetP"
    q: "GetGOATSObservationsObservationsMatchesObservingModeGmosSouthImagingVariantGroupedSkyOffsetsEnumeratedValuesOffsetQ"


class GetGOATSObservationsObservationsMatchesObservingModeGmosSouthImagingVariantGroupedSkyOffsetsEnumeratedValuesOffsetP(
    BaseModel
):
    arcseconds: Any


class GetGOATSObservationsObservationsMatchesObservingModeGmosSouthImagingVariantGroupedSkyOffsetsEnumeratedValuesOffsetQ(
    BaseModel
):
    arcseconds: Any


class GetGOATSObservationsObservationsMatchesObservingModeGmosSouthImagingVariantGroupedSkyOffsetsRandom(
    BaseModel
):
    seed: Any
    size: "GetGOATSObservationsObservationsMatchesObservingModeGmosSouthImagingVariantGroupedSkyOffsetsRandomSize"
    center: "GetGOATSObservationsObservationsMatchesObservingModeGmosSouthImagingVariantGroupedSkyOffsetsRandomCenter"


class GetGOATSObservationsObservationsMatchesObservingModeGmosSouthImagingVariantGroupedSkyOffsetsRandomSize(
    BaseModel
):
    arcseconds: Any


class GetGOATSObservationsObservationsMatchesObservingModeGmosSouthImagingVariantGroupedSkyOffsetsRandomCenter(
    BaseModel
):
    p: "GetGOATSObservationsObservationsMatchesObservingModeGmosSouthImagingVariantGroupedSkyOffsetsRandomCenterP"
    q: "GetGOATSObservationsObservationsMatchesObservingModeGmosSouthImagingVariantGroupedSkyOffsetsRandomCenterQ"


class GetGOATSObservationsObservationsMatchesObservingModeGmosSouthImagingVariantGroupedSkyOffsetsRandomCenterP(
    BaseModel
):
    arcseconds: Any


class GetGOATSObservationsObservationsMatchesObservingModeGmosSouthImagingVariantGroupedSkyOffsetsRandomCenterQ(
    BaseModel
):
    arcseconds: Any


class GetGOATSObservationsObservationsMatchesObservingModeGmosSouthImagingVariantGroupedSkyOffsetsSpiral(
    BaseModel
):
    seed: Any
    size: "GetGOATSObservationsObservationsMatchesObservingModeGmosSouthImagingVariantGroupedSkyOffsetsSpiralSize"
    center: "GetGOATSObservationsObservationsMatchesObservingModeGmosSouthImagingVariantGroupedSkyOffsetsSpiralCenter"


class GetGOATSObservationsObservationsMatchesObservingModeGmosSouthImagingVariantGroupedSkyOffsetsSpiralSize(
    BaseModel
):
    arcseconds: Any


class GetGOATSObservationsObservationsMatchesObservingModeGmosSouthImagingVariantGroupedSkyOffsetsSpiralCenter(
    BaseModel
):
    p: "GetGOATSObservationsObservationsMatchesObservingModeGmosSouthImagingVariantGroupedSkyOffsetsSpiralCenterP"
    q: "GetGOATSObservationsObservationsMatchesObservingModeGmosSouthImagingVariantGroupedSkyOffsetsSpiralCenterQ"


class GetGOATSObservationsObservationsMatchesObservingModeGmosSouthImagingVariantGroupedSkyOffsetsSpiralCenterP(
    BaseModel
):
    arcseconds: Any


class GetGOATSObservationsObservationsMatchesObservingModeGmosSouthImagingVariantGroupedSkyOffsetsSpiralCenterQ(
    BaseModel
):
    arcseconds: Any


class GetGOATSObservationsObservationsMatchesObservingModeGmosSouthImagingVariantGroupedSkyOffsetsUniform(
    BaseModel
):
    corner_a: "GetGOATSObservationsObservationsMatchesObservingModeGmosSouthImagingVariantGroupedSkyOffsetsUniformCornerA" = Field(
        alias="cornerA"
    )
    corner_b: "GetGOATSObservationsObservationsMatchesObservingModeGmosSouthImagingVariantGroupedSkyOffsetsUniformCornerB" = Field(
        alias="cornerB"
    )


class GetGOATSObservationsObservationsMatchesObservingModeGmosSouthImagingVariantGroupedSkyOffsetsUniformCornerA(
    BaseModel
):
    p: "GetGOATSObservationsObservationsMatchesObservingModeGmosSouthImagingVariantGroupedSkyOffsetsUniformCornerAP"
    q: "GetGOATSObservationsObservationsMatchesObservingModeGmosSouthImagingVariantGroupedSkyOffsetsUniformCornerAQ"


class GetGOATSObservationsObservationsMatchesObservingModeGmosSouthImagingVariantGroupedSkyOffsetsUniformCornerAP(
    BaseModel
):
    arcseconds: Any


class GetGOATSObservationsObservationsMatchesObservingModeGmosSouthImagingVariantGroupedSkyOffsetsUniformCornerAQ(
    BaseModel
):
    arcseconds: Any


class GetGOATSObservationsObservationsMatchesObservingModeGmosSouthImagingVariantGroupedSkyOffsetsUniformCornerB(
    BaseModel
):
    p: "GetGOATSObservationsObservationsMatchesObservingModeGmosSouthImagingVariantGroupedSkyOffsetsUniformCornerBP"
    q: "GetGOATSObservationsObservationsMatchesObservingModeGmosSouthImagingVariantGroupedSkyOffsetsUniformCornerBQ"


class GetGOATSObservationsObservationsMatchesObservingModeGmosSouthImagingVariantGroupedSkyOffsetsUniformCornerBP(
    BaseModel
):
    arcseconds: Any


class GetGOATSObservationsObservationsMatchesObservingModeGmosSouthImagingVariantGroupedSkyOffsetsUniformCornerBQ(
    BaseModel
):
    arcseconds: Any


class GetGOATSObservationsObservationsMatchesObservingModeGmosSouthImagingVariantGroupedOffsets(
    BaseModel
):
    generator_type: TelescopeConfigGeneratorType = Field(alias="generatorType")
    random: Optional[
        "GetGOATSObservationsObservationsMatchesObservingModeGmosSouthImagingVariantGroupedOffsetsRandom"
    ]
    spiral: Optional[
        "GetGOATSObservationsObservationsMatchesObservingModeGmosSouthImagingVariantGroupedOffsetsSpiral"
    ]
    uniform: Optional[
        "GetGOATSObservationsObservationsMatchesObservingModeGmosSouthImagingVariantGroupedOffsetsUniform"
    ]
    enumerated: Optional[
        "GetGOATSObservationsObservationsMatchesObservingModeGmosSouthImagingVariantGroupedOffsetsEnumerated"
    ]


class GetGOATSObservationsObservationsMatchesObservingModeGmosSouthImagingVariantGroupedOffsetsRandom(
    BaseModel
):
    seed: Any
    size: "GetGOATSObservationsObservationsMatchesObservingModeGmosSouthImagingVariantGroupedOffsetsRandomSize"
    center: "GetGOATSObservationsObservationsMatchesObservingModeGmosSouthImagingVariantGroupedOffsetsRandomCenter"


class GetGOATSObservationsObservationsMatchesObservingModeGmosSouthImagingVariantGroupedOffsetsRandomSize(
    BaseModel
):
    arcseconds: Any


class GetGOATSObservationsObservationsMatchesObservingModeGmosSouthImagingVariantGroupedOffsetsRandomCenter(
    BaseModel
):
    p: "GetGOATSObservationsObservationsMatchesObservingModeGmosSouthImagingVariantGroupedOffsetsRandomCenterP"
    q: "GetGOATSObservationsObservationsMatchesObservingModeGmosSouthImagingVariantGroupedOffsetsRandomCenterQ"


class GetGOATSObservationsObservationsMatchesObservingModeGmosSouthImagingVariantGroupedOffsetsRandomCenterP(
    BaseModel
):
    arcseconds: Any


class GetGOATSObservationsObservationsMatchesObservingModeGmosSouthImagingVariantGroupedOffsetsRandomCenterQ(
    BaseModel
):
    arcseconds: Any


class GetGOATSObservationsObservationsMatchesObservingModeGmosSouthImagingVariantGroupedOffsetsSpiral(
    BaseModel
):
    seed: Any
    size: "GetGOATSObservationsObservationsMatchesObservingModeGmosSouthImagingVariantGroupedOffsetsSpiralSize"
    center: "GetGOATSObservationsObservationsMatchesObservingModeGmosSouthImagingVariantGroupedOffsetsSpiralCenter"


class GetGOATSObservationsObservationsMatchesObservingModeGmosSouthImagingVariantGroupedOffsetsSpiralSize(
    BaseModel
):
    arcseconds: Any


class GetGOATSObservationsObservationsMatchesObservingModeGmosSouthImagingVariantGroupedOffsetsSpiralCenter(
    BaseModel
):
    p: "GetGOATSObservationsObservationsMatchesObservingModeGmosSouthImagingVariantGroupedOffsetsSpiralCenterP"
    q: "GetGOATSObservationsObservationsMatchesObservingModeGmosSouthImagingVariantGroupedOffsetsSpiralCenterQ"


class GetGOATSObservationsObservationsMatchesObservingModeGmosSouthImagingVariantGroupedOffsetsSpiralCenterP(
    BaseModel
):
    arcseconds: Any


class GetGOATSObservationsObservationsMatchesObservingModeGmosSouthImagingVariantGroupedOffsetsSpiralCenterQ(
    BaseModel
):
    arcseconds: Any


class GetGOATSObservationsObservationsMatchesObservingModeGmosSouthImagingVariantGroupedOffsetsUniform(
    BaseModel
):
    corner_a: "GetGOATSObservationsObservationsMatchesObservingModeGmosSouthImagingVariantGroupedOffsetsUniformCornerA" = Field(
        alias="cornerA"
    )
    corner_b: "GetGOATSObservationsObservationsMatchesObservingModeGmosSouthImagingVariantGroupedOffsetsUniformCornerB" = Field(
        alias="cornerB"
    )


class GetGOATSObservationsObservationsMatchesObservingModeGmosSouthImagingVariantGroupedOffsetsUniformCornerA(
    BaseModel
):
    p: "GetGOATSObservationsObservationsMatchesObservingModeGmosSouthImagingVariantGroupedOffsetsUniformCornerAP"
    q: "GetGOATSObservationsObservationsMatchesObservingModeGmosSouthImagingVariantGroupedOffsetsUniformCornerAQ"


class GetGOATSObservationsObservationsMatchesObservingModeGmosSouthImagingVariantGroupedOffsetsUniformCornerAP(
    BaseModel
):
    arcseconds: Any


class GetGOATSObservationsObservationsMatchesObservingModeGmosSouthImagingVariantGroupedOffsetsUniformCornerAQ(
    BaseModel
):
    arcseconds: Any


class GetGOATSObservationsObservationsMatchesObservingModeGmosSouthImagingVariantGroupedOffsetsUniformCornerB(
    BaseModel
):
    p: "GetGOATSObservationsObservationsMatchesObservingModeGmosSouthImagingVariantGroupedOffsetsUniformCornerBP"
    q: "GetGOATSObservationsObservationsMatchesObservingModeGmosSouthImagingVariantGroupedOffsetsUniformCornerBQ"


class GetGOATSObservationsObservationsMatchesObservingModeGmosSouthImagingVariantGroupedOffsetsUniformCornerBP(
    BaseModel
):
    arcseconds: Any


class GetGOATSObservationsObservationsMatchesObservingModeGmosSouthImagingVariantGroupedOffsetsUniformCornerBQ(
    BaseModel
):
    arcseconds: Any


class GetGOATSObservationsObservationsMatchesObservingModeGmosSouthImagingVariantGroupedOffsetsEnumerated(
    BaseModel
):
    values: list[
        "GetGOATSObservationsObservationsMatchesObservingModeGmosSouthImagingVariantGroupedOffsetsEnumeratedValues"
    ]


class GetGOATSObservationsObservationsMatchesObservingModeGmosSouthImagingVariantGroupedOffsetsEnumeratedValues(
    BaseModel
):
    guiding: GuideState
    offset: "GetGOATSObservationsObservationsMatchesObservingModeGmosSouthImagingVariantGroupedOffsetsEnumeratedValuesOffset"


class GetGOATSObservationsObservationsMatchesObservingModeGmosSouthImagingVariantGroupedOffsetsEnumeratedValuesOffset(
    BaseModel
):
    p: "GetGOATSObservationsObservationsMatchesObservingModeGmosSouthImagingVariantGroupedOffsetsEnumeratedValuesOffsetP"
    q: "GetGOATSObservationsObservationsMatchesObservingModeGmosSouthImagingVariantGroupedOffsetsEnumeratedValuesOffsetQ"


class GetGOATSObservationsObservationsMatchesObservingModeGmosSouthImagingVariantGroupedOffsetsEnumeratedValuesOffsetP(
    BaseModel
):
    arcseconds: Any


class GetGOATSObservationsObservationsMatchesObservingModeGmosSouthImagingVariantGroupedOffsetsEnumeratedValuesOffsetQ(
    BaseModel
):
    arcseconds: Any


class GetGOATSObservationsObservationsMatchesObservingModeGmosSouthImagingVariantInterleaved(
    BaseModel
):
    offsets: "GetGOATSObservationsObservationsMatchesObservingModeGmosSouthImagingVariantInterleavedOffsets"
    sky_count: Any = Field(alias="skyCount")
    sky_offsets: "GetGOATSObservationsObservationsMatchesObservingModeGmosSouthImagingVariantInterleavedSkyOffsets" = Field(
        alias="skyOffsets"
    )


class GetGOATSObservationsObservationsMatchesObservingModeGmosSouthImagingVariantInterleavedOffsets(
    BaseModel
):
    generator_type: TelescopeConfigGeneratorType = Field(alias="generatorType")
    enumerated: Optional[
        "GetGOATSObservationsObservationsMatchesObservingModeGmosSouthImagingVariantInterleavedOffsetsEnumerated"
    ]
    random: Optional[
        "GetGOATSObservationsObservationsMatchesObservingModeGmosSouthImagingVariantInterleavedOffsetsRandom"
    ]
    spiral: Optional[
        "GetGOATSObservationsObservationsMatchesObservingModeGmosSouthImagingVariantInterleavedOffsetsSpiral"
    ]
    uniform: Optional[
        "GetGOATSObservationsObservationsMatchesObservingModeGmosSouthImagingVariantInterleavedOffsetsUniform"
    ]


class GetGOATSObservationsObservationsMatchesObservingModeGmosSouthImagingVariantInterleavedOffsetsEnumerated(
    BaseModel
):
    values: list[
        "GetGOATSObservationsObservationsMatchesObservingModeGmosSouthImagingVariantInterleavedOffsetsEnumeratedValues"
    ]


class GetGOATSObservationsObservationsMatchesObservingModeGmosSouthImagingVariantInterleavedOffsetsEnumeratedValues(
    BaseModel
):
    guiding: GuideState
    offset: "GetGOATSObservationsObservationsMatchesObservingModeGmosSouthImagingVariantInterleavedOffsetsEnumeratedValuesOffset"


class GetGOATSObservationsObservationsMatchesObservingModeGmosSouthImagingVariantInterleavedOffsetsEnumeratedValuesOffset(
    BaseModel
):
    p: "GetGOATSObservationsObservationsMatchesObservingModeGmosSouthImagingVariantInterleavedOffsetsEnumeratedValuesOffsetP"
    q: "GetGOATSObservationsObservationsMatchesObservingModeGmosSouthImagingVariantInterleavedOffsetsEnumeratedValuesOffsetQ"


class GetGOATSObservationsObservationsMatchesObservingModeGmosSouthImagingVariantInterleavedOffsetsEnumeratedValuesOffsetP(
    BaseModel
):
    arcseconds: Any


class GetGOATSObservationsObservationsMatchesObservingModeGmosSouthImagingVariantInterleavedOffsetsEnumeratedValuesOffsetQ(
    BaseModel
):
    arcseconds: Any


class GetGOATSObservationsObservationsMatchesObservingModeGmosSouthImagingVariantInterleavedOffsetsRandom(
    BaseModel
):
    seed: Any
    size: "GetGOATSObservationsObservationsMatchesObservingModeGmosSouthImagingVariantInterleavedOffsetsRandomSize"
    center: "GetGOATSObservationsObservationsMatchesObservingModeGmosSouthImagingVariantInterleavedOffsetsRandomCenter"


class GetGOATSObservationsObservationsMatchesObservingModeGmosSouthImagingVariantInterleavedOffsetsRandomSize(
    BaseModel
):
    arcseconds: Any


class GetGOATSObservationsObservationsMatchesObservingModeGmosSouthImagingVariantInterleavedOffsetsRandomCenter(
    BaseModel
):
    p: "GetGOATSObservationsObservationsMatchesObservingModeGmosSouthImagingVariantInterleavedOffsetsRandomCenterP"
    q: "GetGOATSObservationsObservationsMatchesObservingModeGmosSouthImagingVariantInterleavedOffsetsRandomCenterQ"


class GetGOATSObservationsObservationsMatchesObservingModeGmosSouthImagingVariantInterleavedOffsetsRandomCenterP(
    BaseModel
):
    arcseconds: Any


class GetGOATSObservationsObservationsMatchesObservingModeGmosSouthImagingVariantInterleavedOffsetsRandomCenterQ(
    BaseModel
):
    arcseconds: Any


class GetGOATSObservationsObservationsMatchesObservingModeGmosSouthImagingVariantInterleavedOffsetsSpiral(
    BaseModel
):
    seed: Any
    size: "GetGOATSObservationsObservationsMatchesObservingModeGmosSouthImagingVariantInterleavedOffsetsSpiralSize"
    center: "GetGOATSObservationsObservationsMatchesObservingModeGmosSouthImagingVariantInterleavedOffsetsSpiralCenter"


class GetGOATSObservationsObservationsMatchesObservingModeGmosSouthImagingVariantInterleavedOffsetsSpiralSize(
    BaseModel
):
    arcseconds: Any


class GetGOATSObservationsObservationsMatchesObservingModeGmosSouthImagingVariantInterleavedOffsetsSpiralCenter(
    BaseModel
):
    p: "GetGOATSObservationsObservationsMatchesObservingModeGmosSouthImagingVariantInterleavedOffsetsSpiralCenterP"
    q: "GetGOATSObservationsObservationsMatchesObservingModeGmosSouthImagingVariantInterleavedOffsetsSpiralCenterQ"


class GetGOATSObservationsObservationsMatchesObservingModeGmosSouthImagingVariantInterleavedOffsetsSpiralCenterP(
    BaseModel
):
    arcseconds: Any


class GetGOATSObservationsObservationsMatchesObservingModeGmosSouthImagingVariantInterleavedOffsetsSpiralCenterQ(
    BaseModel
):
    arcseconds: Any


class GetGOATSObservationsObservationsMatchesObservingModeGmosSouthImagingVariantInterleavedOffsetsUniform(
    BaseModel
):
    corner_a: "GetGOATSObservationsObservationsMatchesObservingModeGmosSouthImagingVariantInterleavedOffsetsUniformCornerA" = Field(
        alias="cornerA"
    )
    corner_b: "GetGOATSObservationsObservationsMatchesObservingModeGmosSouthImagingVariantInterleavedOffsetsUniformCornerB" = Field(
        alias="cornerB"
    )


class GetGOATSObservationsObservationsMatchesObservingModeGmosSouthImagingVariantInterleavedOffsetsUniformCornerA(
    BaseModel
):
    p: "GetGOATSObservationsObservationsMatchesObservingModeGmosSouthImagingVariantInterleavedOffsetsUniformCornerAP"
    q: "GetGOATSObservationsObservationsMatchesObservingModeGmosSouthImagingVariantInterleavedOffsetsUniformCornerAQ"


class GetGOATSObservationsObservationsMatchesObservingModeGmosSouthImagingVariantInterleavedOffsetsUniformCornerAP(
    BaseModel
):
    arcseconds: Any


class GetGOATSObservationsObservationsMatchesObservingModeGmosSouthImagingVariantInterleavedOffsetsUniformCornerAQ(
    BaseModel
):
    arcseconds: Any


class GetGOATSObservationsObservationsMatchesObservingModeGmosSouthImagingVariantInterleavedOffsetsUniformCornerB(
    BaseModel
):
    p: "GetGOATSObservationsObservationsMatchesObservingModeGmosSouthImagingVariantInterleavedOffsetsUniformCornerBP"
    q: "GetGOATSObservationsObservationsMatchesObservingModeGmosSouthImagingVariantInterleavedOffsetsUniformCornerBQ"


class GetGOATSObservationsObservationsMatchesObservingModeGmosSouthImagingVariantInterleavedOffsetsUniformCornerBP(
    BaseModel
):
    arcseconds: Any


class GetGOATSObservationsObservationsMatchesObservingModeGmosSouthImagingVariantInterleavedOffsetsUniformCornerBQ(
    BaseModel
):
    arcseconds: Any


class GetGOATSObservationsObservationsMatchesObservingModeGmosSouthImagingVariantInterleavedSkyOffsets(
    BaseModel
):
    generator_type: TelescopeConfigGeneratorType = Field(alias="generatorType")
    enumerated: Optional[
        "GetGOATSObservationsObservationsMatchesObservingModeGmosSouthImagingVariantInterleavedSkyOffsetsEnumerated"
    ]
    random: Optional[
        "GetGOATSObservationsObservationsMatchesObservingModeGmosSouthImagingVariantInterleavedSkyOffsetsRandom"
    ]
    spiral: Optional[
        "GetGOATSObservationsObservationsMatchesObservingModeGmosSouthImagingVariantInterleavedSkyOffsetsSpiral"
    ]
    uniform: Optional[
        "GetGOATSObservationsObservationsMatchesObservingModeGmosSouthImagingVariantInterleavedSkyOffsetsUniform"
    ]


class GetGOATSObservationsObservationsMatchesObservingModeGmosSouthImagingVariantInterleavedSkyOffsetsEnumerated(
    BaseModel
):
    values: list[
        "GetGOATSObservationsObservationsMatchesObservingModeGmosSouthImagingVariantInterleavedSkyOffsetsEnumeratedValues"
    ]


class GetGOATSObservationsObservationsMatchesObservingModeGmosSouthImagingVariantInterleavedSkyOffsetsEnumeratedValues(
    BaseModel
):
    guiding: GuideState
    offset: "GetGOATSObservationsObservationsMatchesObservingModeGmosSouthImagingVariantInterleavedSkyOffsetsEnumeratedValuesOffset"


class GetGOATSObservationsObservationsMatchesObservingModeGmosSouthImagingVariantInterleavedSkyOffsetsEnumeratedValuesOffset(
    BaseModel
):
    p: "GetGOATSObservationsObservationsMatchesObservingModeGmosSouthImagingVariantInterleavedSkyOffsetsEnumeratedValuesOffsetP"
    q: "GetGOATSObservationsObservationsMatchesObservingModeGmosSouthImagingVariantInterleavedSkyOffsetsEnumeratedValuesOffsetQ"


class GetGOATSObservationsObservationsMatchesObservingModeGmosSouthImagingVariantInterleavedSkyOffsetsEnumeratedValuesOffsetP(
    BaseModel
):
    arcseconds: Any


class GetGOATSObservationsObservationsMatchesObservingModeGmosSouthImagingVariantInterleavedSkyOffsetsEnumeratedValuesOffsetQ(
    BaseModel
):
    arcseconds: Any


class GetGOATSObservationsObservationsMatchesObservingModeGmosSouthImagingVariantInterleavedSkyOffsetsRandom(
    BaseModel
):
    seed: Any
    size: "GetGOATSObservationsObservationsMatchesObservingModeGmosSouthImagingVariantInterleavedSkyOffsetsRandomSize"
    center: "GetGOATSObservationsObservationsMatchesObservingModeGmosSouthImagingVariantInterleavedSkyOffsetsRandomCenter"


class GetGOATSObservationsObservationsMatchesObservingModeGmosSouthImagingVariantInterleavedSkyOffsetsRandomSize(
    BaseModel
):
    arcseconds: Any


class GetGOATSObservationsObservationsMatchesObservingModeGmosSouthImagingVariantInterleavedSkyOffsetsRandomCenter(
    BaseModel
):
    p: "GetGOATSObservationsObservationsMatchesObservingModeGmosSouthImagingVariantInterleavedSkyOffsetsRandomCenterP"
    q: "GetGOATSObservationsObservationsMatchesObservingModeGmosSouthImagingVariantInterleavedSkyOffsetsRandomCenterQ"


class GetGOATSObservationsObservationsMatchesObservingModeGmosSouthImagingVariantInterleavedSkyOffsetsRandomCenterP(
    BaseModel
):
    arcseconds: Any


class GetGOATSObservationsObservationsMatchesObservingModeGmosSouthImagingVariantInterleavedSkyOffsetsRandomCenterQ(
    BaseModel
):
    arcseconds: Any


class GetGOATSObservationsObservationsMatchesObservingModeGmosSouthImagingVariantInterleavedSkyOffsetsSpiral(
    BaseModel
):
    seed: Any
    size: "GetGOATSObservationsObservationsMatchesObservingModeGmosSouthImagingVariantInterleavedSkyOffsetsSpiralSize"
    center: "GetGOATSObservationsObservationsMatchesObservingModeGmosSouthImagingVariantInterleavedSkyOffsetsSpiralCenter"


class GetGOATSObservationsObservationsMatchesObservingModeGmosSouthImagingVariantInterleavedSkyOffsetsSpiralSize(
    BaseModel
):
    arcseconds: Any


class GetGOATSObservationsObservationsMatchesObservingModeGmosSouthImagingVariantInterleavedSkyOffsetsSpiralCenter(
    BaseModel
):
    p: "GetGOATSObservationsObservationsMatchesObservingModeGmosSouthImagingVariantInterleavedSkyOffsetsSpiralCenterP"
    q: "GetGOATSObservationsObservationsMatchesObservingModeGmosSouthImagingVariantInterleavedSkyOffsetsSpiralCenterQ"


class GetGOATSObservationsObservationsMatchesObservingModeGmosSouthImagingVariantInterleavedSkyOffsetsSpiralCenterP(
    BaseModel
):
    arcseconds: Any


class GetGOATSObservationsObservationsMatchesObservingModeGmosSouthImagingVariantInterleavedSkyOffsetsSpiralCenterQ(
    BaseModel
):
    arcseconds: Any


class GetGOATSObservationsObservationsMatchesObservingModeGmosSouthImagingVariantInterleavedSkyOffsetsUniform(
    BaseModel
):
    corner_a: "GetGOATSObservationsObservationsMatchesObservingModeGmosSouthImagingVariantInterleavedSkyOffsetsUniformCornerA" = Field(
        alias="cornerA"
    )
    corner_b: "GetGOATSObservationsObservationsMatchesObservingModeGmosSouthImagingVariantInterleavedSkyOffsetsUniformCornerB" = Field(
        alias="cornerB"
    )


class GetGOATSObservationsObservationsMatchesObservingModeGmosSouthImagingVariantInterleavedSkyOffsetsUniformCornerA(
    BaseModel
):
    p: "GetGOATSObservationsObservationsMatchesObservingModeGmosSouthImagingVariantInterleavedSkyOffsetsUniformCornerAP"
    q: "GetGOATSObservationsObservationsMatchesObservingModeGmosSouthImagingVariantInterleavedSkyOffsetsUniformCornerAQ"


class GetGOATSObservationsObservationsMatchesObservingModeGmosSouthImagingVariantInterleavedSkyOffsetsUniformCornerAP(
    BaseModel
):
    arcseconds: Any


class GetGOATSObservationsObservationsMatchesObservingModeGmosSouthImagingVariantInterleavedSkyOffsetsUniformCornerAQ(
    BaseModel
):
    arcseconds: Any


class GetGOATSObservationsObservationsMatchesObservingModeGmosSouthImagingVariantInterleavedSkyOffsetsUniformCornerB(
    BaseModel
):
    p: "GetGOATSObservationsObservationsMatchesObservingModeGmosSouthImagingVariantInterleavedSkyOffsetsUniformCornerBP"
    q: "GetGOATSObservationsObservationsMatchesObservingModeGmosSouthImagingVariantInterleavedSkyOffsetsUniformCornerBQ"


class GetGOATSObservationsObservationsMatchesObservingModeGmosSouthImagingVariantInterleavedSkyOffsetsUniformCornerBP(
    BaseModel
):
    arcseconds: Any


class GetGOATSObservationsObservationsMatchesObservingModeGmosSouthImagingVariantInterleavedSkyOffsetsUniformCornerBQ(
    BaseModel
):
    arcseconds: Any


class GetGOATSObservationsObservationsMatchesObservingModeGmosSouthImagingVariantPreImaging(
    BaseModel
):
    offset_1: "GetGOATSObservationsObservationsMatchesObservingModeGmosSouthImagingVariantPreImagingOffset1" = Field(
        alias="offset1"
    )
    offset_2: "GetGOATSObservationsObservationsMatchesObservingModeGmosSouthImagingVariantPreImagingOffset2" = Field(
        alias="offset2"
    )
    offset_3: "GetGOATSObservationsObservationsMatchesObservingModeGmosSouthImagingVariantPreImagingOffset3" = Field(
        alias="offset3"
    )
    offset_4: "GetGOATSObservationsObservationsMatchesObservingModeGmosSouthImagingVariantPreImagingOffset4" = Field(
        alias="offset4"
    )


class GetGOATSObservationsObservationsMatchesObservingModeGmosSouthImagingVariantPreImagingOffset1(
    BaseModel
):
    p: "GetGOATSObservationsObservationsMatchesObservingModeGmosSouthImagingVariantPreImagingOffset1P"
    q: "GetGOATSObservationsObservationsMatchesObservingModeGmosSouthImagingVariantPreImagingOffset1Q"


class GetGOATSObservationsObservationsMatchesObservingModeGmosSouthImagingVariantPreImagingOffset1P(
    BaseModel
):
    arcseconds: Any


class GetGOATSObservationsObservationsMatchesObservingModeGmosSouthImagingVariantPreImagingOffset1Q(
    BaseModel
):
    arcseconds: Any


class GetGOATSObservationsObservationsMatchesObservingModeGmosSouthImagingVariantPreImagingOffset2(
    BaseModel
):
    p: "GetGOATSObservationsObservationsMatchesObservingModeGmosSouthImagingVariantPreImagingOffset2P"
    q: "GetGOATSObservationsObservationsMatchesObservingModeGmosSouthImagingVariantPreImagingOffset2Q"


class GetGOATSObservationsObservationsMatchesObservingModeGmosSouthImagingVariantPreImagingOffset2P(
    BaseModel
):
    arcseconds: Any


class GetGOATSObservationsObservationsMatchesObservingModeGmosSouthImagingVariantPreImagingOffset2Q(
    BaseModel
):
    arcseconds: Any


class GetGOATSObservationsObservationsMatchesObservingModeGmosSouthImagingVariantPreImagingOffset3(
    BaseModel
):
    p: "GetGOATSObservationsObservationsMatchesObservingModeGmosSouthImagingVariantPreImagingOffset3P"
    q: "GetGOATSObservationsObservationsMatchesObservingModeGmosSouthImagingVariantPreImagingOffset3Q"


class GetGOATSObservationsObservationsMatchesObservingModeGmosSouthImagingVariantPreImagingOffset3P(
    BaseModel
):
    arcseconds: Any


class GetGOATSObservationsObservationsMatchesObservingModeGmosSouthImagingVariantPreImagingOffset3Q(
    BaseModel
):
    arcseconds: Any


class GetGOATSObservationsObservationsMatchesObservingModeGmosSouthImagingVariantPreImagingOffset4(
    BaseModel
):
    p: "GetGOATSObservationsObservationsMatchesObservingModeGmosSouthImagingVariantPreImagingOffset4P"
    q: "GetGOATSObservationsObservationsMatchesObservingModeGmosSouthImagingVariantPreImagingOffset4Q"


class GetGOATSObservationsObservationsMatchesObservingModeGmosSouthImagingVariantPreImagingOffset4P(
    BaseModel
):
    arcseconds: Any


class GetGOATSObservationsObservationsMatchesObservingModeGmosSouthImagingVariantPreImagingOffset4Q(
    BaseModel
):
    arcseconds: Any


class GetGOATSObservationsObservationsMatchesProgram(BaseModel):
    allocations: list["GetGOATSObservationsObservationsMatchesProgramAllocations"]
    time_charge: list["GetGOATSObservationsObservationsMatchesProgramTimeCharge"] = (
        Field(alias="timeCharge")
    )


class GetGOATSObservationsObservationsMatchesProgramAllocations(BaseModel):
    science_band: ScienceBand = Field(alias="scienceBand")
    duration: "GetGOATSObservationsObservationsMatchesProgramAllocationsDuration"


class GetGOATSObservationsObservationsMatchesProgramAllocationsDuration(BaseModel):
    hours: Any


class GetGOATSObservationsObservationsMatchesProgramTimeCharge(BaseModel):
    band: Optional[ScienceBand]
    time: "GetGOATSObservationsObservationsMatchesProgramTimeChargeTime"


class GetGOATSObservationsObservationsMatchesProgramTimeChargeTime(BaseModel):
    program: "GetGOATSObservationsObservationsMatchesProgramTimeChargeTimeProgram"


class GetGOATSObservationsObservationsMatchesProgramTimeChargeTimeProgram(BaseModel):
    hours: Any


GetGOATSObservations.model_rebuild()
GetGOATSObservationsObservations.model_rebuild()
GetGOATSObservationsObservationsMatches.model_rebuild()
GetGOATSObservationsObservationsMatchesConstraintSet.model_rebuild()
GetGOATSObservationsObservationsMatchesConstraintSetElevationRange.model_rebuild()
GetGOATSObservationsObservationsMatchesWorkflow.model_rebuild()
GetGOATSObservationsObservationsMatchesWorkflowValue.model_rebuild()
GetGOATSObservationsObservationsMatchesTimingWindows.model_rebuild()
GetGOATSObservationsObservationsMatchesTimingWindowsEndTimingWindowEndAfter.model_rebuild()
GetGOATSObservationsObservationsMatchesTimingWindowsEndTimingWindowEndAfterRepeat.model_rebuild()
GetGOATSObservationsObservationsMatchesTargetEnvironment.model_rebuild()
GetGOATSObservationsObservationsMatchesTargetEnvironmentAsterism.model_rebuild()
GetGOATSObservationsObservationsMatchesTargetEnvironmentFirstScienceTarget.model_rebuild()
GetGOATSObservationsObservationsMatchesTargetEnvironmentFirstScienceTargetSidereal.model_rebuild()
GetGOATSObservationsObservationsMatchesTargetEnvironmentFirstScienceTargetSiderealProperMotion.model_rebuild()
GetGOATSObservationsObservationsMatchesTargetEnvironmentFirstScienceTargetSourceProfile.model_rebuild()
GetGOATSObservationsObservationsMatchesTargetEnvironmentFirstScienceTargetSourceProfilePoint.model_rebuild()
GetGOATSObservationsObservationsMatchesTargetEnvironmentFirstScienceTargetSourceProfilePointBandNormalized.model_rebuild()
GetGOATSObservationsObservationsMatchesTargetEnvironmentFirstScienceTargetSourceProfilePointBandNormalizedSed.model_rebuild()
GetGOATSObservationsObservationsMatchesTargetEnvironmentFirstScienceTargetSourceProfilePointBandNormalizedSedFluxDensities.model_rebuild()
GetGOATSObservationsObservationsMatchesPosAngleConstraint.model_rebuild()
GetGOATSObservationsObservationsMatchesScienceRequirements.model_rebuild()
GetGOATSObservationsObservationsMatchesScienceRequirementsSpectroscopy.model_rebuild()
GetGOATSObservationsObservationsMatchesScienceRequirementsExposureTimeMode.model_rebuild()
GetGOATSObservationsObservationsMatchesScienceRequirementsExposureTimeModeSignalToNoise.model_rebuild()
GetGOATSObservationsObservationsMatchesScienceRequirementsExposureTimeModeTimeAndCount.model_rebuild()
GetGOATSObservationsObservationsMatchesObservingMode.model_rebuild()
GetGOATSObservationsObservationsMatchesObservingModeGmosNorthLongSlit.model_rebuild()
GetGOATSObservationsObservationsMatchesObservingModeGmosNorthLongSlitExposureTimeMode.model_rebuild()
GetGOATSObservationsObservationsMatchesObservingModeGmosNorthLongSlitExposureTimeModeSignalToNoise.model_rebuild()
GetGOATSObservationsObservationsMatchesObservingModeGmosNorthLongSlitExposureTimeModeTimeAndCount.model_rebuild()
GetGOATSObservationsObservationsMatchesObservingModeGmosSouthLongSlit.model_rebuild()
GetGOATSObservationsObservationsMatchesObservingModeGmosSouthLongSlitExposureTimeMode.model_rebuild()
GetGOATSObservationsObservationsMatchesObservingModeGmosSouthLongSlitExposureTimeModeSignalToNoise.model_rebuild()
GetGOATSObservationsObservationsMatchesObservingModeGmosSouthLongSlitExposureTimeModeTimeAndCount.model_rebuild()
GetGOATSObservationsObservationsMatchesObservingModeGmosNorthImaging.model_rebuild()
GetGOATSObservationsObservationsMatchesObservingModeGmosNorthImagingFilters.model_rebuild()
GetGOATSObservationsObservationsMatchesObservingModeGmosNorthImagingFiltersExposureTimeMode.model_rebuild()
GetGOATSObservationsObservationsMatchesObservingModeGmosNorthImagingFiltersExposureTimeModeSignalToNoise.model_rebuild()
GetGOATSObservationsObservationsMatchesObservingModeGmosNorthImagingFiltersExposureTimeModeTimeAndCount.model_rebuild()
GetGOATSObservationsObservationsMatchesObservingModeGmosNorthImagingVariant.model_rebuild()
GetGOATSObservationsObservationsMatchesObservingModeGmosNorthImagingVariantGrouped.model_rebuild()
GetGOATSObservationsObservationsMatchesObservingModeGmosNorthImagingVariantGroupedSkyOffsets.model_rebuild()
GetGOATSObservationsObservationsMatchesObservingModeGmosNorthImagingVariantGroupedSkyOffsetsEnumerated.model_rebuild()
GetGOATSObservationsObservationsMatchesObservingModeGmosNorthImagingVariantGroupedSkyOffsetsEnumeratedValues.model_rebuild()
GetGOATSObservationsObservationsMatchesObservingModeGmosNorthImagingVariantGroupedSkyOffsetsEnumeratedValuesOffset.model_rebuild()
GetGOATSObservationsObservationsMatchesObservingModeGmosNorthImagingVariantGroupedSkyOffsetsRandom.model_rebuild()
GetGOATSObservationsObservationsMatchesObservingModeGmosNorthImagingVariantGroupedSkyOffsetsRandomCenter.model_rebuild()
GetGOATSObservationsObservationsMatchesObservingModeGmosNorthImagingVariantGroupedSkyOffsetsSpiral.model_rebuild()
GetGOATSObservationsObservationsMatchesObservingModeGmosNorthImagingVariantGroupedSkyOffsetsSpiralCenter.model_rebuild()
GetGOATSObservationsObservationsMatchesObservingModeGmosNorthImagingVariantGroupedSkyOffsetsUniform.model_rebuild()
GetGOATSObservationsObservationsMatchesObservingModeGmosNorthImagingVariantGroupedSkyOffsetsUniformCornerA.model_rebuild()
GetGOATSObservationsObservationsMatchesObservingModeGmosNorthImagingVariantGroupedSkyOffsetsUniformCornerB.model_rebuild()
GetGOATSObservationsObservationsMatchesObservingModeGmosNorthImagingVariantGroupedOffsets.model_rebuild()
GetGOATSObservationsObservationsMatchesObservingModeGmosNorthImagingVariantGroupedOffsetsRandom.model_rebuild()
GetGOATSObservationsObservationsMatchesObservingModeGmosNorthImagingVariantGroupedOffsetsRandomCenter.model_rebuild()
GetGOATSObservationsObservationsMatchesObservingModeGmosNorthImagingVariantGroupedOffsetsSpiral.model_rebuild()
GetGOATSObservationsObservationsMatchesObservingModeGmosNorthImagingVariantGroupedOffsetsSpiralCenter.model_rebuild()
GetGOATSObservationsObservationsMatchesObservingModeGmosNorthImagingVariantGroupedOffsetsUniform.model_rebuild()
GetGOATSObservationsObservationsMatchesObservingModeGmosNorthImagingVariantGroupedOffsetsUniformCornerA.model_rebuild()
GetGOATSObservationsObservationsMatchesObservingModeGmosNorthImagingVariantGroupedOffsetsUniformCornerB.model_rebuild()
GetGOATSObservationsObservationsMatchesObservingModeGmosNorthImagingVariantGroupedOffsetsEnumerated.model_rebuild()
GetGOATSObservationsObservationsMatchesObservingModeGmosNorthImagingVariantGroupedOffsetsEnumeratedValues.model_rebuild()
GetGOATSObservationsObservationsMatchesObservingModeGmosNorthImagingVariantGroupedOffsetsEnumeratedValuesOffset.model_rebuild()
GetGOATSObservationsObservationsMatchesObservingModeGmosNorthImagingVariantInterleaved.model_rebuild()
GetGOATSObservationsObservationsMatchesObservingModeGmosNorthImagingVariantInterleavedOffsets.model_rebuild()
GetGOATSObservationsObservationsMatchesObservingModeGmosNorthImagingVariantInterleavedOffsetsEnumerated.model_rebuild()
GetGOATSObservationsObservationsMatchesObservingModeGmosNorthImagingVariantInterleavedOffsetsEnumeratedValues.model_rebuild()
GetGOATSObservationsObservationsMatchesObservingModeGmosNorthImagingVariantInterleavedOffsetsEnumeratedValuesOffset.model_rebuild()
GetGOATSObservationsObservationsMatchesObservingModeGmosNorthImagingVariantInterleavedOffsetsRandom.model_rebuild()
GetGOATSObservationsObservationsMatchesObservingModeGmosNorthImagingVariantInterleavedOffsetsRandomCenter.model_rebuild()
GetGOATSObservationsObservationsMatchesObservingModeGmosNorthImagingVariantInterleavedOffsetsSpiral.model_rebuild()
GetGOATSObservationsObservationsMatchesObservingModeGmosNorthImagingVariantInterleavedOffsetsSpiralCenter.model_rebuild()
GetGOATSObservationsObservationsMatchesObservingModeGmosNorthImagingVariantInterleavedOffsetsUniform.model_rebuild()
GetGOATSObservationsObservationsMatchesObservingModeGmosNorthImagingVariantInterleavedOffsetsUniformCornerA.model_rebuild()
GetGOATSObservationsObservationsMatchesObservingModeGmosNorthImagingVariantInterleavedOffsetsUniformCornerB.model_rebuild()
GetGOATSObservationsObservationsMatchesObservingModeGmosNorthImagingVariantInterleavedSkyOffsets.model_rebuild()
GetGOATSObservationsObservationsMatchesObservingModeGmosNorthImagingVariantInterleavedSkyOffsetsEnumerated.model_rebuild()
GetGOATSObservationsObservationsMatchesObservingModeGmosNorthImagingVariantInterleavedSkyOffsetsEnumeratedValues.model_rebuild()
GetGOATSObservationsObservationsMatchesObservingModeGmosNorthImagingVariantInterleavedSkyOffsetsEnumeratedValuesOffset.model_rebuild()
GetGOATSObservationsObservationsMatchesObservingModeGmosNorthImagingVariantInterleavedSkyOffsetsRandom.model_rebuild()
GetGOATSObservationsObservationsMatchesObservingModeGmosNorthImagingVariantInterleavedSkyOffsetsRandomCenter.model_rebuild()
GetGOATSObservationsObservationsMatchesObservingModeGmosNorthImagingVariantInterleavedSkyOffsetsSpiral.model_rebuild()
GetGOATSObservationsObservationsMatchesObservingModeGmosNorthImagingVariantInterleavedSkyOffsetsSpiralCenter.model_rebuild()
GetGOATSObservationsObservationsMatchesObservingModeGmosNorthImagingVariantInterleavedSkyOffsetsUniform.model_rebuild()
GetGOATSObservationsObservationsMatchesObservingModeGmosNorthImagingVariantInterleavedSkyOffsetsUniformCornerA.model_rebuild()
GetGOATSObservationsObservationsMatchesObservingModeGmosNorthImagingVariantInterleavedSkyOffsetsUniformCornerB.model_rebuild()
GetGOATSObservationsObservationsMatchesObservingModeGmosNorthImagingVariantPreImaging.model_rebuild()
GetGOATSObservationsObservationsMatchesObservingModeGmosNorthImagingVariantPreImagingOffset1.model_rebuild()
GetGOATSObservationsObservationsMatchesObservingModeGmosNorthImagingVariantPreImagingOffset2.model_rebuild()
GetGOATSObservationsObservationsMatchesObservingModeGmosNorthImagingVariantPreImagingOffset3.model_rebuild()
GetGOATSObservationsObservationsMatchesObservingModeGmosNorthImagingVariantPreImagingOffset4.model_rebuild()
GetGOATSObservationsObservationsMatchesObservingModeGmosSouthImaging.model_rebuild()
GetGOATSObservationsObservationsMatchesObservingModeGmosSouthImagingFilters.model_rebuild()
GetGOATSObservationsObservationsMatchesObservingModeGmosSouthImagingFiltersExposureTimeMode.model_rebuild()
GetGOATSObservationsObservationsMatchesObservingModeGmosSouthImagingFiltersExposureTimeModeSignalToNoise.model_rebuild()
GetGOATSObservationsObservationsMatchesObservingModeGmosSouthImagingFiltersExposureTimeModeTimeAndCount.model_rebuild()
GetGOATSObservationsObservationsMatchesObservingModeGmosSouthImagingVariant.model_rebuild()
GetGOATSObservationsObservationsMatchesObservingModeGmosSouthImagingVariantGrouped.model_rebuild()
GetGOATSObservationsObservationsMatchesObservingModeGmosSouthImagingVariantGroupedSkyOffsets.model_rebuild()
GetGOATSObservationsObservationsMatchesObservingModeGmosSouthImagingVariantGroupedSkyOffsetsEnumerated.model_rebuild()
GetGOATSObservationsObservationsMatchesObservingModeGmosSouthImagingVariantGroupedSkyOffsetsEnumeratedValues.model_rebuild()
GetGOATSObservationsObservationsMatchesObservingModeGmosSouthImagingVariantGroupedSkyOffsetsEnumeratedValuesOffset.model_rebuild()
GetGOATSObservationsObservationsMatchesObservingModeGmosSouthImagingVariantGroupedSkyOffsetsRandom.model_rebuild()
GetGOATSObservationsObservationsMatchesObservingModeGmosSouthImagingVariantGroupedSkyOffsetsRandomCenter.model_rebuild()
GetGOATSObservationsObservationsMatchesObservingModeGmosSouthImagingVariantGroupedSkyOffsetsSpiral.model_rebuild()
GetGOATSObservationsObservationsMatchesObservingModeGmosSouthImagingVariantGroupedSkyOffsetsSpiralCenter.model_rebuild()
GetGOATSObservationsObservationsMatchesObservingModeGmosSouthImagingVariantGroupedSkyOffsetsUniform.model_rebuild()
GetGOATSObservationsObservationsMatchesObservingModeGmosSouthImagingVariantGroupedSkyOffsetsUniformCornerA.model_rebuild()
GetGOATSObservationsObservationsMatchesObservingModeGmosSouthImagingVariantGroupedSkyOffsetsUniformCornerB.model_rebuild()
GetGOATSObservationsObservationsMatchesObservingModeGmosSouthImagingVariantGroupedOffsets.model_rebuild()
GetGOATSObservationsObservationsMatchesObservingModeGmosSouthImagingVariantGroupedOffsetsRandom.model_rebuild()
GetGOATSObservationsObservationsMatchesObservingModeGmosSouthImagingVariantGroupedOffsetsRandomCenter.model_rebuild()
GetGOATSObservationsObservationsMatchesObservingModeGmosSouthImagingVariantGroupedOffsetsSpiral.model_rebuild()
GetGOATSObservationsObservationsMatchesObservingModeGmosSouthImagingVariantGroupedOffsetsSpiralCenter.model_rebuild()
GetGOATSObservationsObservationsMatchesObservingModeGmosSouthImagingVariantGroupedOffsetsUniform.model_rebuild()
GetGOATSObservationsObservationsMatchesObservingModeGmosSouthImagingVariantGroupedOffsetsUniformCornerA.model_rebuild()
GetGOATSObservationsObservationsMatchesObservingModeGmosSouthImagingVariantGroupedOffsetsUniformCornerB.model_rebuild()
GetGOATSObservationsObservationsMatchesObservingModeGmosSouthImagingVariantGroupedOffsetsEnumerated.model_rebuild()
GetGOATSObservationsObservationsMatchesObservingModeGmosSouthImagingVariantGroupedOffsetsEnumeratedValues.model_rebuild()
GetGOATSObservationsObservationsMatchesObservingModeGmosSouthImagingVariantGroupedOffsetsEnumeratedValuesOffset.model_rebuild()
GetGOATSObservationsObservationsMatchesObservingModeGmosSouthImagingVariantInterleaved.model_rebuild()
GetGOATSObservationsObservationsMatchesObservingModeGmosSouthImagingVariantInterleavedOffsets.model_rebuild()
GetGOATSObservationsObservationsMatchesObservingModeGmosSouthImagingVariantInterleavedOffsetsEnumerated.model_rebuild()
GetGOATSObservationsObservationsMatchesObservingModeGmosSouthImagingVariantInterleavedOffsetsEnumeratedValues.model_rebuild()
GetGOATSObservationsObservationsMatchesObservingModeGmosSouthImagingVariantInterleavedOffsetsEnumeratedValuesOffset.model_rebuild()
GetGOATSObservationsObservationsMatchesObservingModeGmosSouthImagingVariantInterleavedOffsetsRandom.model_rebuild()
GetGOATSObservationsObservationsMatchesObservingModeGmosSouthImagingVariantInterleavedOffsetsRandomCenter.model_rebuild()
GetGOATSObservationsObservationsMatchesObservingModeGmosSouthImagingVariantInterleavedOffsetsSpiral.model_rebuild()
GetGOATSObservationsObservationsMatchesObservingModeGmosSouthImagingVariantInterleavedOffsetsSpiralCenter.model_rebuild()
GetGOATSObservationsObservationsMatchesObservingModeGmosSouthImagingVariantInterleavedOffsetsUniform.model_rebuild()
GetGOATSObservationsObservationsMatchesObservingModeGmosSouthImagingVariantInterleavedOffsetsUniformCornerA.model_rebuild()
GetGOATSObservationsObservationsMatchesObservingModeGmosSouthImagingVariantInterleavedOffsetsUniformCornerB.model_rebuild()
GetGOATSObservationsObservationsMatchesObservingModeGmosSouthImagingVariantInterleavedSkyOffsets.model_rebuild()
GetGOATSObservationsObservationsMatchesObservingModeGmosSouthImagingVariantInterleavedSkyOffsetsEnumerated.model_rebuild()
GetGOATSObservationsObservationsMatchesObservingModeGmosSouthImagingVariantInterleavedSkyOffsetsEnumeratedValues.model_rebuild()
GetGOATSObservationsObservationsMatchesObservingModeGmosSouthImagingVariantInterleavedSkyOffsetsEnumeratedValuesOffset.model_rebuild()
GetGOATSObservationsObservationsMatchesObservingModeGmosSouthImagingVariantInterleavedSkyOffsetsRandom.model_rebuild()
GetGOATSObservationsObservationsMatchesObservingModeGmosSouthImagingVariantInterleavedSkyOffsetsRandomCenter.model_rebuild()
GetGOATSObservationsObservationsMatchesObservingModeGmosSouthImagingVariantInterleavedSkyOffsetsSpiral.model_rebuild()
GetGOATSObservationsObservationsMatchesObservingModeGmosSouthImagingVariantInterleavedSkyOffsetsSpiralCenter.model_rebuild()
GetGOATSObservationsObservationsMatchesObservingModeGmosSouthImagingVariantInterleavedSkyOffsetsUniform.model_rebuild()
GetGOATSObservationsObservationsMatchesObservingModeGmosSouthImagingVariantInterleavedSkyOffsetsUniformCornerA.model_rebuild()
GetGOATSObservationsObservationsMatchesObservingModeGmosSouthImagingVariantInterleavedSkyOffsetsUniformCornerB.model_rebuild()
GetGOATSObservationsObservationsMatchesObservingModeGmosSouthImagingVariantPreImaging.model_rebuild()
GetGOATSObservationsObservationsMatchesObservingModeGmosSouthImagingVariantPreImagingOffset1.model_rebuild()
GetGOATSObservationsObservationsMatchesObservingModeGmosSouthImagingVariantPreImagingOffset2.model_rebuild()
GetGOATSObservationsObservationsMatchesObservingModeGmosSouthImagingVariantPreImagingOffset3.model_rebuild()
GetGOATSObservationsObservationsMatchesObservingModeGmosSouthImagingVariantPreImagingOffset4.model_rebuild()
GetGOATSObservationsObservationsMatchesProgram.model_rebuild()
GetGOATSObservationsObservationsMatchesProgramAllocations.model_rebuild()
GetGOATSObservationsObservationsMatchesProgramTimeCharge.model_rebuild()
GetGOATSObservationsObservationsMatchesProgramTimeChargeTime.model_rebuild()
