from typing import Annotated, Any, Literal, Optional, Union

from pydantic import Field

from .base_model import BaseModel
from .enums import (
    AttachmentType,
    CalculationState,
    CalibrationRole,
    CloudExtinctionPreset,
    EphemerisKeyType,
    Existence,
    Flamingos2Decker,
    Flamingos2Disperser,
    Flamingos2Filter,
    Flamingos2Fpu,
    Flamingos2ReadMode,
    Flamingos2ReadoutMode,
    Flamingos2Reads,
    GeminiCallForProposalsType,
    GhostBinning,
    GhostIfu1FiberAgitator,
    GhostIfu2FiberAgitator,
    GhostReadMode,
    GhostResolutionMode,
    GmosBinning,
    GmosNorthBuiltinFpu,
    GmosNorthFilter,
    GmosNorthGrating,
    GmosSouthBuiltinFpu,
    GmosSouthFilter,
    GmosSouthGrating,
    ImageQualityPreset,
    Instrument,
    KeckInstrument,
    ObservationValidationCode,
    ObservationWorkflowState,
    Observatory,
    ObservingModeType,
    ProgramType,
    ProposalStatus,
    ScienceBand,
    ScienceMode,
    ScienceSubtype,
    SkyBackground,
    SlitOffsetMode,
    SubaruCallForProposalsType,
    SubaruInstrument,
    TelluricTag,
    TimingWindowInclusion,
    VisitorObservingModeType,
    WaterVapor,
)


class AttachmentDetails(BaseModel):
    id: Any
    file_name: Any = Field(alias="fileName")
    attachment_type: AttachmentType = Field(alias="attachmentType")
    file_size: Any = Field(alias="fileSize")
    checked: bool
    description: Optional[Any]
    updated_at: Any = Field(alias="updatedAt")


class CallForProposalsCore(BaseModel):
    id: Any
    title: Any


class CallForProposalsDetails(CallForProposalsCore):
    semester: Any
    active: "CallForProposalsDetailsActive"
    submission_deadline_default: Optional[Any] = Field(
        alias="submissionDeadlineDefault"
    )
    existence: Existence
    observatory: Observatory
    gemini: Optional["CallForProposalsDetailsGemini"]
    keck: Optional["CallForProposalsDetailsKeck"]
    subaru: Optional["CallForProposalsDetailsSubaru"]


class CallForProposalsDetailsActive(BaseModel):
    start: Any
    end: Any


class CallForProposalsDetailsGemini(BaseModel):
    type_: GeminiCallForProposalsType = Field(alias="type")
    instruments: list[Instrument]


class CallForProposalsDetailsKeck(BaseModel):
    instruments: list[KeckInstrument]


class CallForProposalsDetailsSubaru(BaseModel):
    type_: SubaruCallForProposalsType = Field(alias="type")
    instruments: list[SubaruInstrument]


class CallForProposalsObservatory(BaseModel):
    observatory: Observatory
    gemini: Optional["CallForProposalsObservatoryGemini"]
    keck: Optional["CallForProposalsObservatoryKeck"]
    subaru: Optional["CallForProposalsObservatorySubaru"]


class CallForProposalsObservatoryGemini(BaseModel):
    type_: GeminiCallForProposalsType = Field(alias="type")
    instruments: list[Instrument]


class CallForProposalsObservatoryKeck(BaseModel):
    instruments: list[KeckInstrument]


class CallForProposalsObservatorySubaru(BaseModel):
    type_: SubaruCallForProposalsType = Field(alias="type")
    instruments: list[SubaruInstrument]


class ConstraintSetDetails(BaseModel):
    image_quality: ImageQualityPreset = Field(alias="imageQuality")
    cloud_extinction: CloudExtinctionPreset = Field(alias="cloudExtinction")
    sky_background: SkyBackground = Field(alias="skyBackground")
    water_vapor: WaterVapor = Field(alias="waterVapor")
    elevation_range: "ConstraintSetDetailsElevationRange" = Field(
        alias="elevationRange"
    )


class ConstraintSetDetailsElevationRange(BaseModel):
    air_mass: Optional["ConstraintSetDetailsElevationRangeAirMass"] = Field(
        alias="airMass"
    )
    hour_angle: Optional["ConstraintSetDetailsElevationRangeHourAngle"] = Field(
        alias="hourAngle"
    )


class ConstraintSetDetailsElevationRangeAirMass(BaseModel):
    min: Any
    max: Any


class ConstraintSetDetailsElevationRangeHourAngle(BaseModel):
    min_hours: Any = Field(alias="minHours")
    max_hours: Any = Field(alias="maxHours")


class ExecutionDetails(BaseModel):
    digest: Optional["ExecutionDetailsDigest"]


class ExecutionDetailsDigest(BaseModel):
    value: Optional["ExecutionDetailsDigestValue"]


class ExecutionDetailsDigestValue(BaseModel):
    acquisition: Optional["ExecutionDetailsDigestValueAcquisition"]
    setup: "ExecutionDetailsDigestValueSetup"


class ExecutionDetailsDigestValueAcquisition(BaseModel):
    time_estimate: "ExecutionDetailsDigestValueAcquisitionTimeEstimate" = Field(
        alias="timeEstimate"
    )


class ExecutionDetailsDigestValueAcquisitionTimeEstimate(BaseModel):
    total: "ExecutionDetailsDigestValueAcquisitionTimeEstimateTotal"


class ExecutionDetailsDigestValueAcquisitionTimeEstimateTotal(BaseModel):
    seconds: Any


class ExecutionDetailsDigestValueSetup(BaseModel):
    full: "ExecutionDetailsDigestValueSetupFull"
    reacquisition: "ExecutionDetailsDigestValueSetupReacquisition"


class ExecutionDetailsDigestValueSetupFull(BaseModel):
    seconds: Any


class ExecutionDetailsDigestValueSetupReacquisition(BaseModel):
    seconds: Any


class ExposureTimeModeDetails(BaseModel):
    signal_to_noise: Optional["ExposureTimeModeDetailsSignalToNoise"] = Field(
        alias="signalToNoise"
    )
    time_and_count: Optional["ExposureTimeModeDetailsTimeAndCount"] = Field(
        alias="timeAndCount"
    )


class ExposureTimeModeDetailsSignalToNoise(BaseModel):
    value: Any
    at: "ExposureTimeModeDetailsSignalToNoiseAt"


class ExposureTimeModeDetailsSignalToNoiseAt(BaseModel):
    nanometers: Any


class ExposureTimeModeDetailsTimeAndCount(BaseModel):
    time: "ExposureTimeModeDetailsTimeAndCountTime"
    count: Any
    at: "ExposureTimeModeDetailsTimeAndCountAt"


class ExposureTimeModeDetailsTimeAndCountTime(BaseModel):
    seconds: Any


class ExposureTimeModeDetailsTimeAndCountAt(BaseModel):
    nanometers: Any


class Flamingos2LongSlitDetails(BaseModel):
    decker: Flamingos2Decker
    default_decker: Flamingos2Decker = Field(alias="defaultDecker")
    default_offsets: list["Flamingos2LongSlitDetailsDefaultOffsets"] = Field(
        alias="defaultOffsets"
    )
    disperser: Flamingos2Disperser
    filter_: Flamingos2Filter = Field(alias="filter")
    fpu: Flamingos2Fpu
    telluric_type: "Flamingos2LongSlitDetailsTelluricType" = Field(alias="telluricType")
    exposure_time_mode: "Flamingos2LongSlitDetailsExposureTimeMode" = Field(
        alias="exposureTimeMode"
    )
    explicit_read_mode: Optional[Flamingos2ReadMode] = Field(alias="explicitReadMode")
    explicit_reads: Optional[Flamingos2Reads] = Field(alias="explicitReads")
    explicit_decker: Optional[Flamingos2Decker] = Field(alias="explicitDecker")
    readout_mode: Flamingos2ReadoutMode = Field(alias="readoutMode")
    default_readout_mode: Flamingos2ReadoutMode = Field(alias="defaultReadoutMode")
    offsets: list["Flamingos2LongSlitDetailsOffsets"]
    acquisition: "Flamingos2LongSlitDetailsAcquisition"
    initial_disperser: Flamingos2Disperser = Field(alias="initialDisperser")
    initial_filter: Flamingos2Filter = Field(alias="initialFilter")
    initial_fpu: Flamingos2Fpu = Field(alias="initialFpu")


class Flamingos2LongSlitDetailsDefaultOffsets(BaseModel):
    q: "Flamingos2LongSlitDetailsDefaultOffsetsQ"
    p: "Flamingos2LongSlitDetailsDefaultOffsetsP"


class Flamingos2LongSlitDetailsDefaultOffsetsQ(BaseModel):
    arcseconds: Any


class Flamingos2LongSlitDetailsDefaultOffsetsP(BaseModel):
    arcseconds: Any


class Flamingos2LongSlitDetailsTelluricType(BaseModel):
    tag: TelluricTag
    star_types: Optional[list[str]] = Field(alias="starTypes")


class Flamingos2LongSlitDetailsExposureTimeMode(ExposureTimeModeDetails):
    pass


class Flamingos2LongSlitDetailsOffsets(BaseModel):
    q: "Flamingos2LongSlitDetailsOffsetsQ"
    p: "Flamingos2LongSlitDetailsOffsetsP"


class Flamingos2LongSlitDetailsOffsetsQ(BaseModel):
    arcseconds: Any


class Flamingos2LongSlitDetailsOffsetsP(BaseModel):
    arcseconds: Any


class Flamingos2LongSlitDetailsAcquisition(BaseModel):
    exposure_time_mode: "Flamingos2LongSlitDetailsAcquisitionExposureTimeMode" = Field(
        alias="exposureTimeMode"
    )


class Flamingos2LongSlitDetailsAcquisitionExposureTimeMode(ExposureTimeModeDetails):
    pass


class GeminiScienceSubtypeOnProposal(BaseModel):
    gemini: Optional["GeminiScienceSubtypeOnProposalGemini"]


class GeminiScienceSubtypeOnProposalGemini(BaseModel):
    typename__: Literal[
        "Classical",
        "DemoScience",
        "DirectorsTime",
        "FastTurnaround",
        "GeminiProposalType",
        "LargeProgram",
        "PoorWeather",
        "Queue",
        "SystemVerification",
    ] = Field(alias="__typename")
    science_subtype: ScienceSubtype = Field(alias="scienceSubtype")


class GmosNorthImagingDetails(BaseModel):
    filters: list["GmosNorthImagingDetailsFilters"]
    bin: GmosBinning


class GmosNorthImagingDetailsFilters(BaseModel):
    filter_: GmosNorthFilter = Field(alias="filter")


class GmosNorthLongSlitDetails(BaseModel):
    grating: GmosNorthGrating
    filter_: Optional[GmosNorthFilter] = Field(alias="filter")
    fpu: GmosNorthBuiltinFpu
    central_wavelength: "GmosNorthLongSlitDetailsCentralWavelength" = Field(
        alias="centralWavelength"
    )
    offsets: list["GmosNorthLongSlitDetailsOffsets"]
    x_bin: GmosBinning = Field(alias="xBin")
    y_bin: GmosBinning = Field(alias="yBin")


class GmosNorthLongSlitDetailsCentralWavelength(BaseModel):
    nanometers: Any


class GmosNorthLongSlitDetailsOffsets(BaseModel):
    arcseconds: Any


class GmosSouthImagingDetails(BaseModel):
    filters: list["GmosSouthImagingDetailsFilters"]
    bin: GmosBinning


class GmosSouthImagingDetailsFilters(BaseModel):
    filter_: GmosSouthFilter = Field(alias="filter")


class GmosSouthLongSlitDetails(BaseModel):
    grating: GmosSouthGrating
    filter_: Optional[GmosSouthFilter] = Field(alias="filter")
    fpu: GmosSouthBuiltinFpu
    central_wavelength: "GmosSouthLongSlitDetailsCentralWavelength" = Field(
        alias="centralWavelength"
    )
    offsets: list["GmosSouthLongSlitDetailsOffsets"]
    x_bin: GmosBinning = Field(alias="xBin")
    y_bin: GmosBinning = Field(alias="yBin")


class GmosSouthLongSlitDetailsCentralWavelength(BaseModel):
    nanometers: Any


class GmosSouthLongSlitDetailsOffsets(BaseModel):
    arcseconds: Any


class Igrins2LongSlitDetails(BaseModel):
    exposure_time_mode: "Igrins2LongSlitDetailsExposureTimeMode" = Field(
        alias="exposureTimeMode"
    )
    offset_mode: SlitOffsetMode = Field(alias="offsetMode")
    default_offset_mode: SlitOffsetMode = Field(alias="defaultOffsetMode")
    explicit_offset_mode: Optional[SlitOffsetMode] = Field(alias="explicitOffsetMode")
    save_svc_images: bool = Field(alias="saveSVCImages")
    default_save_svc_images: bool = Field(alias="defaultSaveSVCImages")
    explicit_save_svc_images: Optional[bool] = Field(alias="explicitSaveSVCImages")
    offsets: list["Igrins2LongSlitDetailsOffsets"]
    default_offsets: list["Igrins2LongSlitDetailsDefaultOffsets"] = Field(
        alias="defaultOffsets"
    )
    explicit_offsets: Optional[list["Igrins2LongSlitDetailsExplicitOffsets"]] = Field(
        alias="explicitOffsets"
    )
    telluric_type: "Igrins2LongSlitDetailsTelluricType" = Field(alias="telluricType")


class Igrins2LongSlitDetailsExposureTimeMode(BaseModel):
    signal_to_noise: Optional["Igrins2LongSlitDetailsExposureTimeModeSignalToNoise"] = (
        Field(alias="signalToNoise")
    )
    time_and_count: Optional["Igrins2LongSlitDetailsExposureTimeModeTimeAndCount"] = (
        Field(alias="timeAndCount")
    )


class Igrins2LongSlitDetailsExposureTimeModeSignalToNoise(BaseModel):
    value: Any
    at: "Igrins2LongSlitDetailsExposureTimeModeSignalToNoiseAt"


class Igrins2LongSlitDetailsExposureTimeModeSignalToNoiseAt(BaseModel):
    nanometers: Any


class Igrins2LongSlitDetailsExposureTimeModeTimeAndCount(BaseModel):
    time: "Igrins2LongSlitDetailsExposureTimeModeTimeAndCountTime"
    count: Any
    at: "Igrins2LongSlitDetailsExposureTimeModeTimeAndCountAt"


class Igrins2LongSlitDetailsExposureTimeModeTimeAndCountTime(BaseModel):
    seconds: Any


class Igrins2LongSlitDetailsExposureTimeModeTimeAndCountAt(BaseModel):
    nanometers: Any


class Igrins2LongSlitDetailsOffsets(BaseModel):
    q: "Igrins2LongSlitDetailsOffsetsQ"
    p: "Igrins2LongSlitDetailsOffsetsP"


class Igrins2LongSlitDetailsOffsetsQ(BaseModel):
    arcseconds: Any


class Igrins2LongSlitDetailsOffsetsP(BaseModel):
    arcseconds: Any


class Igrins2LongSlitDetailsDefaultOffsets(BaseModel):
    q: "Igrins2LongSlitDetailsDefaultOffsetsQ"
    p: "Igrins2LongSlitDetailsDefaultOffsetsP"


class Igrins2LongSlitDetailsDefaultOffsetsQ(BaseModel):
    arcseconds: Any


class Igrins2LongSlitDetailsDefaultOffsetsP(BaseModel):
    arcseconds: Any


class Igrins2LongSlitDetailsExplicitOffsets(BaseModel):
    q: "Igrins2LongSlitDetailsExplicitOffsetsQ"
    p: "Igrins2LongSlitDetailsExplicitOffsetsP"


class Igrins2LongSlitDetailsExplicitOffsetsQ(BaseModel):
    arcseconds: Any


class Igrins2LongSlitDetailsExplicitOffsetsP(BaseModel):
    arcseconds: Any


class Igrins2LongSlitDetailsTelluricType(BaseModel):
    tag: TelluricTag
    star_types: Optional[list[str]] = Field(alias="starTypes")


class VisitorDetails(BaseModel):
    mode: VisitorObservingModeType
    name: Optional[Any]
    central_wavelength: "VisitorDetailsCentralWavelength" = Field(
        alias="centralWavelength"
    )
    total_request_time: Optional["VisitorDetailsTotalRequestTime"] = Field(
        alias="totalRequestTime"
    )
    ags_diameter: "VisitorDetailsAgsDiameter" = Field(alias="agsDiameter")


class VisitorDetailsCentralWavelength(BaseModel):
    nanometers: Any


class VisitorDetailsTotalRequestTime(BaseModel):
    seconds: Any


class VisitorDetailsAgsDiameter(BaseModel):
    dms: str
    hms: str


class GhostDetectorConfigDetails(BaseModel):
    binning: GhostBinning
    default_binning: GhostBinning = Field(alias="defaultBinning")
    default_read_mode: GhostReadMode = Field(alias="defaultReadMode")
    explicit_binning: Optional[GhostBinning] = Field(alias="explicitBinning")
    explicit_read_mode: Optional[GhostReadMode] = Field(alias="explicitReadMode")
    read_mode: GhostReadMode = Field(alias="readMode")
    exposure_time_mode: "GhostDetectorConfigDetailsExposureTimeMode" = Field(
        alias="exposureTimeMode"
    )


class GhostDetectorConfigDetailsExposureTimeMode(BaseModel):
    signal_to_noise: Optional[
        "GhostDetectorConfigDetailsExposureTimeModeSignalToNoise"
    ] = Field(alias="signalToNoise")
    time_and_count: Optional[
        "GhostDetectorConfigDetailsExposureTimeModeTimeAndCount"
    ] = Field(alias="timeAndCount")


class GhostDetectorConfigDetailsExposureTimeModeSignalToNoise(BaseModel):
    value: Any
    at: "GhostDetectorConfigDetailsExposureTimeModeSignalToNoiseAt"


class GhostDetectorConfigDetailsExposureTimeModeSignalToNoiseAt(BaseModel):
    nanometers: Any


class GhostDetectorConfigDetailsExposureTimeModeTimeAndCount(BaseModel):
    at: "GhostDetectorConfigDetailsExposureTimeModeTimeAndCountAt"
    time: "GhostDetectorConfigDetailsExposureTimeModeTimeAndCountTime"
    count: Any


class GhostDetectorConfigDetailsExposureTimeModeTimeAndCountAt(BaseModel):
    nanometers: Any


class GhostDetectorConfigDetailsExposureTimeModeTimeAndCountTime(BaseModel):
    seconds: Any


class GhostIfuDetails(BaseModel):
    default_ifu_1_agitator: GhostIfu1FiberAgitator = Field(alias="defaultIfu1Agitator")
    default_ifu_2_agitator: GhostIfu2FiberAgitator = Field(alias="defaultIfu2Agitator")
    explicit_ifu_1_agitator: Optional[GhostIfu1FiberAgitator] = Field(
        alias="explicitIfu1Agitator"
    )
    explicit_ifu_2_agitator: Optional[GhostIfu2FiberAgitator] = Field(
        alias="explicitIfu2Agitator"
    )
    ifu_1_agitator: GhostIfu1FiberAgitator = Field(alias="ifu1Agitator")
    ifu_2_agitator: GhostIfu2FiberAgitator = Field(alias="ifu2Agitator")
    resolution_mode: GhostResolutionMode = Field(alias="resolutionMode")
    step_count: Any = Field(alias="stepCount")
    blue: "GhostIfuDetailsBlue"
    red: "GhostIfuDetailsRed"
    sky_position: Optional["GhostIfuDetailsSkyPosition"] = Field(alias="skyPosition")
    slit_viewing_camera_exposure_time: Optional[
        "GhostIfuDetailsSlitViewingCameraExposureTime"
    ] = Field(alias="slitViewingCameraExposureTime")


class GhostIfuDetailsBlue(GhostDetectorConfigDetails):
    pass


class GhostIfuDetailsRed(GhostDetectorConfigDetails):
    pass


class GhostIfuDetailsSkyPosition(BaseModel):
    dec: "GhostIfuDetailsSkyPositionDec"
    ra: "GhostIfuDetailsSkyPositionRa"


class GhostIfuDetailsSkyPositionDec(BaseModel):
    degrees: Any


class GhostIfuDetailsSkyPositionRa(BaseModel):
    degrees: Any


class GhostIfuDetailsSlitViewingCameraExposureTime(BaseModel):
    seconds: Any


class Igrins2LongSlitAndVisitorOnObservingMode(BaseModel):
    igrins_2_long_slit: Optional[
        "Igrins2LongSlitAndVisitorOnObservingModeIgrins2LongSlit"
    ] = Field(alias="igrins2LongSlit")
    visitor: Optional["Igrins2LongSlitAndVisitorOnObservingModeVisitor"]
    ghost_ifu: Optional["Igrins2LongSlitAndVisitorOnObservingModeGhostIfu"] = Field(
        alias="ghostIfu"
    )


class Igrins2LongSlitAndVisitorOnObservingModeIgrins2LongSlit(Igrins2LongSlitDetails):
    pass


class Igrins2LongSlitAndVisitorOnObservingModeVisitor(VisitorDetails):
    pass


class Igrins2LongSlitAndVisitorOnObservingModeGhostIfu(GhostIfuDetails):
    pass


class NonsiderealTargetDetails(BaseModel):
    des: str
    key_type: EphemerisKeyType = Field(alias="keyType")
    key: str


class ObservationCore(BaseModel):
    id: Any
    existence: Existence
    reference: Optional["ObservationCoreReference"]
    title: Any
    instrument: Optional[Instrument]
    calibration_role: Optional[CalibrationRole] = Field(alias="calibrationRole")


class ObservationCoreReference(BaseModel):
    label: Any


class ObservingModeDetails(BaseModel):
    instrument: Instrument
    mode: ObservingModeType
    gmos_north_long_slit: Optional["ObservingModeDetailsGmosNorthLongSlit"] = Field(
        alias="gmosNorthLongSlit"
    )
    gmos_south_long_slit: Optional["ObservingModeDetailsGmosSouthLongSlit"] = Field(
        alias="gmosSouthLongSlit"
    )
    gmos_north_imaging: Optional["ObservingModeDetailsGmosNorthImaging"] = Field(
        alias="gmosNorthImaging"
    )
    gmos_south_imaging: Optional["ObservingModeDetailsGmosSouthImaging"] = Field(
        alias="gmosSouthImaging"
    )
    flamingos_2_long_slit: Optional["ObservingModeDetailsFlamingos2LongSlit"] = Field(
        alias="flamingos2LongSlit"
    )
    igrins_2_long_slit: Optional["ObservingModeDetailsIgrins2LongSlit"] = Field(
        alias="igrins2LongSlit"
    )
    visitor: Optional["ObservingModeDetailsVisitor"]
    ghost_ifu: Optional["ObservingModeDetailsGhostIfu"] = Field(alias="ghostIfu")


class ObservingModeDetailsGmosNorthLongSlit(GmosNorthLongSlitDetails):
    pass


class ObservingModeDetailsGmosSouthLongSlit(GmosSouthLongSlitDetails):
    pass


class ObservingModeDetailsGmosNorthImaging(GmosNorthImagingDetails):
    pass


class ObservingModeDetailsGmosSouthImaging(GmosSouthImagingDetails):
    pass


class ObservingModeDetailsFlamingos2LongSlit(Flamingos2LongSlitDetails):
    pass


class ObservingModeDetailsIgrins2LongSlit(Igrins2LongSlitDetails):
    pass


class ObservingModeDetailsVisitor(VisitorDetails):
    pass


class ObservingModeDetailsGhostIfu(GhostIfuDetails):
    pass


class ProgramCore(BaseModel):
    id: Any
    name: Optional[Any]
    existence: Existence
    description: Optional[Any]


class ScienceRequirementsDetails(BaseModel):
    mode: Optional[ScienceMode]


class SiderealTargetDetails(BaseModel):
    ra: "SiderealTargetDetailsRa"
    dec: "SiderealTargetDetailsDec"
    epoch: Any


class SiderealTargetDetailsRa(BaseModel):
    hours: Any
    hms: Any
    degrees: Any


class SiderealTargetDetailsDec(BaseModel):
    degrees: Any
    dms: Any


class TargetEnvironmentDetails(BaseModel):
    asterism: list["TargetEnvironmentDetailsAsterism"]
    explicit_base: Optional["TargetEnvironmentDetailsExplicitBase"] = Field(
        alias="explicitBase"
    )


class TargetEnvironmentDetailsAsterism(BaseModel):
    name: Any
    sidereal: Optional["TargetEnvironmentDetailsAsterismSidereal"]
    nonsidereal: Optional["TargetEnvironmentDetailsAsterismNonsidereal"]


class TargetEnvironmentDetailsAsterismSidereal(SiderealTargetDetails):
    pass


class TargetEnvironmentDetailsAsterismNonsidereal(NonsiderealTargetDetails):
    pass


class TargetEnvironmentDetailsExplicitBase(BaseModel):
    ra: "TargetEnvironmentDetailsExplicitBaseRa"
    dec: "TargetEnvironmentDetailsExplicitBaseDec"


class TargetEnvironmentDetailsExplicitBaseRa(BaseModel):
    hms: Any


class TargetEnvironmentDetailsExplicitBaseDec(BaseModel):
    dms: Any


class TimingWindowDetails(BaseModel):
    inclusion: TimingWindowInclusion
    start_utc: Any = Field(alias="startUtc")
    end: Optional[
        Annotated[
            Union[
                "TimingWindowDetailsEndTimingWindowEndAt",
                "TimingWindowDetailsEndTimingWindowEndAfter",
            ],
            Field(discriminator="typename__"),
        ]
    ]


class TimingWindowDetailsEndTimingWindowEndAt(BaseModel):
    typename__: Literal["TimingWindowEndAt"] = Field(alias="__typename")
    at_utc: Any = Field(alias="atUtc")


class TimingWindowDetailsEndTimingWindowEndAfter(BaseModel):
    typename__: Literal["TimingWindowEndAfter"] = Field(alias="__typename")
    after: "TimingWindowDetailsEndTimingWindowEndAfterAfter"
    repeat: Optional["TimingWindowDetailsEndTimingWindowEndAfterRepeat"]


class TimingWindowDetailsEndTimingWindowEndAfterAfter(BaseModel):
    seconds: Any


class TimingWindowDetailsEndTimingWindowEndAfterRepeat(BaseModel):
    period: "TimingWindowDetailsEndTimingWindowEndAfterRepeatPeriod"
    times: Optional[Any]


class TimingWindowDetailsEndTimingWindowEndAfterRepeatPeriod(BaseModel):
    seconds: Any


class WorkflowCore(BaseModel):
    state: CalculationState


class WorkflowDetails(WorkflowCore):
    value: "WorkflowDetailsValue"


class WorkflowDetailsValue(BaseModel):
    state: ObservationWorkflowState
    valid_transitions: list[ObservationWorkflowState] = Field(alias="validTransitions")
    validation_errors: list["WorkflowDetailsValueValidationErrors"] = Field(
        alias="validationErrors"
    )


class WorkflowDetailsValueValidationErrors(BaseModel):
    code: ObservationValidationCode
    messages: list[str]


class ObservationDetails(ObservationCore):
    observer_notes: Optional[Any] = Field(alias="observerNotes")
    subtitle: Optional[Any]
    program: "ObservationDetailsProgram"
    science_requirements: "ObservationDetailsScienceRequirements" = Field(
        alias="scienceRequirements"
    )
    science_band: Optional[ScienceBand] = Field(alias="scienceBand")
    workflow: Optional["ObservationDetailsWorkflow"]
    observing_mode: Optional["ObservationDetailsObservingMode"] = Field(
        alias="observingMode"
    )
    constraint_set: "ObservationDetailsConstraintSet" = Field(alias="constraintSet")
    timing_windows: list["ObservationDetailsTimingWindows"] = Field(
        alias="timingWindows"
    )
    target_environment: "ObservationDetailsTargetEnvironment" = Field(
        alias="targetEnvironment"
    )
    execution: "ObservationDetailsExecution"
    execution: "ObservationDetailsExecution"


class ObservationDetailsProgram(ProgramCore):
    pass


class ObservationDetailsScienceRequirements(ScienceRequirementsDetails):
    pass


class ObservationDetailsWorkflow(WorkflowDetails):
    pass


class ObservationDetailsObservingMode(ObservingModeDetails):
    pass


class ObservationDetailsConstraintSet(ConstraintSetDetails):
    pass


class ObservationDetailsTimingWindows(TimingWindowDetails):
    pass


class ObservationDetailsTargetEnvironment(TargetEnvironmentDetails):
    pass


class ObservationDetailsExecution(BaseModel):
    digest: Optional["ObservationDetailsExecutionDigest"]


class ObservationDetailsExecutionDigest(BaseModel):
    value: Optional["ObservationDetailsExecutionDigestValue"]


class ObservationDetailsExecutionDigestValue(BaseModel):
    acquisition: Optional["ObservationDetailsExecutionDigestValueAcquisition"]


class ObservationDetailsExecutionDigestValueAcquisition(BaseModel):
    time_estimate: "ObservationDetailsExecutionDigestValueAcquisitionTimeEstimate" = (
        Field(alias="timeEstimate")
    )


class ObservationDetailsExecutionDigestValueAcquisitionTimeEstimate(BaseModel):
    total: "ObservationDetailsExecutionDigestValueAcquisitionTimeEstimateTotal"
    program: "ObservationDetailsExecutionDigestValueAcquisitionTimeEstimateProgram"
    non_charged: "ObservationDetailsExecutionDigestValueAcquisitionTimeEstimateNonCharged" = Field(
        alias="nonCharged"
    )


class ObservationDetailsExecutionDigestValueAcquisitionTimeEstimateTotal(BaseModel):
    seconds: Any


class ObservationDetailsExecutionDigestValueAcquisitionTimeEstimateProgram(BaseModel):
    seconds: Any


class ObservationDetailsExecutionDigestValueAcquisitionTimeEstimateNonCharged(
    BaseModel
):
    seconds: Any


class ObservationExecution(BaseModel):
    execution: "ObservationExecutionExecution"


class ObservationExecutionExecution(ExecutionDetails):
    pass


class ObservationWorkflowCore(BaseModel):
    state: ObservationWorkflowState


class ObservationWorkflowDetails(ObservationWorkflowCore):
    valid_transitions: list[ObservationWorkflowState] = Field(alias="validTransitions")
    validation_errors: list["ObservationWorkflowDetailsValidationErrors"] = Field(
        alias="validationErrors"
    )


class ObservationWorkflowDetailsValidationErrors(BaseModel):
    code: ObservationValidationCode
    messages: list[str]


class OpportunityTargetDetails(BaseModel):
    region: "OpportunityTargetDetailsRegion"


class OpportunityTargetDetailsRegion(BaseModel):
    right_ascension_arc: "OpportunityTargetDetailsRegionRightAscensionArc" = Field(
        alias="rightAscensionArc"
    )
    declination_arc: "OpportunityTargetDetailsRegionDeclinationArc" = Field(
        alias="declinationArc"
    )


class OpportunityTargetDetailsRegionRightAscensionArc(BaseModel):
    start: Optional["OpportunityTargetDetailsRegionRightAscensionArcStart"]
    end: Optional["OpportunityTargetDetailsRegionRightAscensionArcEnd"]


class OpportunityTargetDetailsRegionRightAscensionArcStart(BaseModel):
    degrees: Any


class OpportunityTargetDetailsRegionRightAscensionArcEnd(BaseModel):
    degrees: Any


class OpportunityTargetDetailsRegionDeclinationArc(BaseModel):
    start: Optional["OpportunityTargetDetailsRegionDeclinationArcStart"]
    end: Optional["OpportunityTargetDetailsRegionDeclinationArcEnd"]


class OpportunityTargetDetailsRegionDeclinationArcStart(BaseModel):
    degrees: Any


class OpportunityTargetDetailsRegionDeclinationArcEnd(BaseModel):
    degrees: Any


class ProgramDetail(ProgramCore):
    type_: ProgramType = Field(alias="type")
    active: "ProgramDetailActive"
    proposal_status: ProposalStatus = Field(alias="proposalStatus")
    proposal: Optional["ProgramDetailProposal"]
    pi: Optional["ProgramDetailPi"]


class ProgramDetailActive(BaseModel):
    start: Any
    end: Any


class ProgramDetailProposal(BaseModel):
    call: Optional["ProgramDetailProposalCall"]


class ProgramDetailProposalCall(BaseModel):
    semester: Any
    active: "ProgramDetailProposalCallActive"


class ProgramDetailProposalCallActive(BaseModel):
    start: Any
    end: Any


class ProgramDetailPi(BaseModel):
    id: Any


class ProgramGroupElements(BaseModel):
    all_group_elements: list["ProgramGroupElementsAllGroupElements"] = Field(
        alias="allGroupElements"
    )


class ProgramGroupElementsAllGroupElements(BaseModel):
    parent_group_id: Optional[Any] = Field(alias="parentGroupId")
    observation: Optional["ProgramGroupElementsAllGroupElementsObservation"]
    group: Optional["ProgramGroupElementsAllGroupElementsGroup"]


class ProgramGroupElementsAllGroupElementsObservation(BaseModel):
    id: Any
    group_id: Optional[Any] = Field(alias="groupId")


class ProgramGroupElementsAllGroupElementsGroup(BaseModel):
    id: Any
    name: Optional[Any]
    minimum_required: Optional[Any] = Field(alias="minimumRequired")
    ordered: bool
    parent_id: Optional[Any] = Field(alias="parentId")
    parent_index: Any = Field(alias="parentIndex")
    minimum_interval: Optional[
        "ProgramGroupElementsAllGroupElementsGroupMinimumInterval"
    ] = Field(alias="minimumInterval")
    maximum_interval: Optional[
        "ProgramGroupElementsAllGroupElementsGroupMaximumInterval"
    ] = Field(alias="maximumInterval")
    system: bool


class ProgramGroupElementsAllGroupElementsGroupMinimumInterval(BaseModel):
    seconds: Any


class ProgramGroupElementsAllGroupElementsGroupMaximumInterval(BaseModel):
    seconds: Any


class SchedulerProposal(BaseModel):
    call: Optional["SchedulerProposalCall"]
    gemini: Optional["SchedulerProposalGemini"]


class SchedulerProposalCall(BaseModel):
    active: "SchedulerProposalCallActive"
    semester: Any


class SchedulerProposalCallActive(BaseModel):
    start: Any
    end: Any


class SchedulerProposalGemini(BaseModel):
    typename__: Literal[
        "Classical",
        "DemoScience",
        "DirectorsTime",
        "FastTurnaround",
        "GeminiProposalType",
        "LargeProgram",
        "PoorWeather",
        "Queue",
        "SystemVerification",
    ] = Field(alias="__typename")
    science_subtype: ScienceSubtype = Field(alias="scienceSubtype")


class TargetCore(BaseModel):
    id: Any
    existence: Existence
    name: Any
    calibration_role: Optional[CalibrationRole] = Field(alias="calibrationRole")


class TargetDetails(TargetCore):
    opportunity: Optional["TargetDetailsOpportunity"]
    sidereal: Optional["TargetDetailsSidereal"]
    nonsidereal: Optional["TargetDetailsNonsidereal"]


class TargetDetailsOpportunity(OpportunityTargetDetails):
    pass


class TargetDetailsSidereal(SiderealTargetDetails):
    pass


class TargetDetailsNonsidereal(NonsiderealTargetDetails):
    pass


class TargetProgramSummary(BaseModel):
    program: "TargetProgramSummaryProgram"


class TargetProgramSummaryProgram(ProgramCore):
    pass


AttachmentDetails.model_rebuild()
CallForProposalsCore.model_rebuild()
CallForProposalsDetails.model_rebuild()
CallForProposalsObservatory.model_rebuild()
ConstraintSetDetails.model_rebuild()
ExecutionDetails.model_rebuild()
ExposureTimeModeDetails.model_rebuild()
Flamingos2LongSlitDetails.model_rebuild()
GeminiScienceSubtypeOnProposal.model_rebuild()
GmosNorthImagingDetails.model_rebuild()
GmosNorthLongSlitDetails.model_rebuild()
GmosSouthImagingDetails.model_rebuild()
GmosSouthLongSlitDetails.model_rebuild()
Igrins2LongSlitDetails.model_rebuild()
VisitorDetails.model_rebuild()
GhostDetectorConfigDetails.model_rebuild()
GhostIfuDetails.model_rebuild()
Igrins2LongSlitAndVisitorOnObservingMode.model_rebuild()
NonsiderealTargetDetails.model_rebuild()
ObservationCore.model_rebuild()
ObservingModeDetails.model_rebuild()
ProgramCore.model_rebuild()
ScienceRequirementsDetails.model_rebuild()
SiderealTargetDetails.model_rebuild()
TargetEnvironmentDetails.model_rebuild()
TimingWindowDetails.model_rebuild()
WorkflowCore.model_rebuild()
WorkflowDetails.model_rebuild()
ObservationDetails.model_rebuild()
ObservationExecution.model_rebuild()
ObservationWorkflowCore.model_rebuild()
ObservationWorkflowDetails.model_rebuild()
OpportunityTargetDetails.model_rebuild()
ProgramDetail.model_rebuild()
ProgramGroupElements.model_rebuild()
SchedulerProposal.model_rebuild()
TargetCore.model_rebuild()
TargetDetails.model_rebuild()
TargetProgramSummary.model_rebuild()
