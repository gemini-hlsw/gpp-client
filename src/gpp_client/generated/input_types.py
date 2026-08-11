from typing import Any, Optional

from pydantic import Field

from .base_model import BaseModel
from .enums import (
    ArcType,
    AttachmentType,
    Band,
    BlindOffsetType,
    Breakpoint,
    BrightnessIntegratedUnits,
    BrightnessSurfaceUnits,
    CalculationState,
    CalibrationRole,
    CatalogName,
    ChargeClass,
    CloudExtinctionPreset,
    ConditionsExpectationType,
    ConditionsMeasurementSource,
    ConfigurationRequestStatus,
    ConsiderForBand3,
    CoolStarTemperature,
    DatabaseOperation,
    DatasetQaState,
    DatasetStage,
    EducationalStatus,
    EphemerisKeyType,
    ExchangePartner,
    ExecutionEventType,
    ExecutionRequirement,
    Existence,
    Flamingos2CustomSlitWidth,
    Flamingos2Decker,
    Flamingos2Disperser,
    Flamingos2Filter,
    Flamingos2Fpu,
    Flamingos2LyotWheel,
    Flamingos2ReadMode,
    Flamingos2ReadoutMode,
    Flamingos2Reads,
    FluxDensityContinuumIntegratedUnits,
    FluxDensityContinuumSurfaceUnits,
    FocalPlane,
    GalaxySpectrum,
    GcalArc,
    GcalContinuum,
    GcalDiffuser,
    GcalFilter,
    GcalShutter,
    GeminiCallForProposalsType,
    Gender,
    GhostBinning,
    GhostIfu1FiberAgitator,
    GhostIfu2FiberAgitator,
    GhostReadMode,
    GhostResolutionMode,
    GmosAmpCount,
    GmosAmpGain,
    GmosAmpReadMode,
    GmosBinning,
    GmosCustomSlitWidth,
    GmosDtax,
    GmosEOffsetting,
    GmosGratingOrder,
    GmosLongSlitAcquisitionRoi,
    GmosMosAcquisitionType,
    GmosNorthBuiltinFpu,
    GmosNorthDetector,
    GmosNorthFilter,
    GmosNorthGrating,
    GmosNorthStageMode,
    GmosRoi,
    GmosSouthBuiltinFpu,
    GmosSouthDetector,
    GmosSouthFilter,
    GmosSouthGrating,
    GmosSouthStageMode,
    GnirsAcquisitionType,
    GnirsCamera,
    GnirsDecker,
    GnirsFilter,
    GnirsFpuIfu,
    GnirsFpuOther,
    GnirsFpuSlit,
    GnirsGrating,
    GnirsPrism,
    GnirsReadMode,
    GnirsWellDepth,
    GuideState,
    HiiRegionSpectrum,
    Ignore,
    ImageQualityPreset,
    ImagingCapability,
    Instrument,
    KeckInstrument,
    LineFluxIntegratedUnits,
    LineFluxSurfaceUnits,
    MosPreImaging,
    ObservationWorkflowState,
    Observatory,
    ObserveClass,
    ObservingModeType,
    Partner,
    PartnerLinkType,
    PlanetaryNebulaSpectrum,
    PlanetSpectrum,
    PosAngleConstraintMode,
    ProgramType,
    ProgramUserRole,
    ProposalStatus,
    QuasarSpectrum,
    ScienceBand,
    ScienceSubtype,
    SeeingTrend,
    SequenceCommand,
    SequenceType,
    Site,
    SkyBackground,
    SlewStage,
    SlitOffsetMode,
    SmartGcalType,
    SpectroscopyCapability,
    StellarLibrarySpectrum,
    StepStage,
    SubaruCallForProposalsType,
    SubaruInstrument,
    TacCategory,
    TargetDisposition,
    TelluricTag,
    TimeAccountingCategory,
    TimeChargeCorrectionOp,
    TimingWindowInclusion,
    TooActivation,
    TooTriggerStatus,
    UserType,
    VisitorObservingModeType,
    WaterVapor,
    WavelengthOrder,
)


class AddDatasetEventInput(BaseModel):
    dataset_id: Any = Field(alias=str("datasetId"))
    dataset_stage: DatasetStage = Field(alias=str("datasetStage"))
    client_time: Optional[Any] = Field(alias=str("clientTime"), default=None)
    idempotency_key: Optional[Any] = Field(alias=str("idempotencyKey"), default=None)


class AddProgramUserInput(BaseModel):
    program_id: Any = Field(alias=str("programId"))
    role: ProgramUserRole
    set_: Optional["ProgramUserPropertiesInput"] = Field(alias=str("SET"), default=None)


class AddSequenceEventInput(BaseModel):
    visit_id: Any = Field(alias=str("visitId"))
    command: SequenceCommand
    client_time: Optional[Any] = Field(alias=str("clientTime"), default=None)
    idempotency_key: Optional[Any] = Field(alias=str("idempotencyKey"), default=None)


class AddSlewEventInput(BaseModel):
    observation_id: Any = Field(alias=str("observationId"))
    slew_stage: SlewStage = Field(alias=str("slewStage"))
    client_time: Optional[Any] = Field(alias=str("clientTime"), default=None)
    idempotency_key: Optional[Any] = Field(alias=str("idempotencyKey"), default=None)


class AddStepEventInput(BaseModel):
    step_id: Any = Field(alias=str("stepId"))
    visit_id: Any = Field(alias=str("visitId"))
    step_stage: StepStage = Field(alias=str("stepStage"))
    client_time: Optional[Any] = Field(alias=str("clientTime"), default=None)
    idempotency_key: Optional[Any] = Field(alias=str("idempotencyKey"), default=None)


class AddEventBatchEntryInput(BaseModel):
    dataset: Optional["AddDatasetEventInput"] = None
    sequence: Optional["AddSequenceEventInput"] = None
    slew: Optional["AddSlewEventInput"] = None
    step: Optional["AddStepEventInput"] = None


class AddEventBatchInput(BaseModel):
    events: list["AddEventBatchEntryInput"]


class AddTimeChargeCorrectionInput(BaseModel):
    visit_id: Any = Field(alias=str("visitId"))
    correction: "TimeChargeCorrectionInput"


class AirMassRangeInput(BaseModel):
    min: Optional[Any] = None
    max: Optional[Any] = None


class AllocationInput(BaseModel):
    category: TimeAccountingCategory
    science_band: ScienceBand = Field(alias=str("scienceBand"))
    duration: "TimeSpanInput"


class AngleInput(BaseModel):
    microarcseconds: Optional[Any] = None
    microseconds: Optional[Any] = None
    milliarcseconds: Optional[Any] = None
    milliseconds: Optional[Any] = None
    arcseconds: Optional[Any] = None
    seconds: Optional[Any] = None
    arcminutes: Optional[Any] = None
    minutes: Optional[Any] = None
    degrees: Optional[Any] = None
    hours: Optional[Any] = None
    dms: Optional[str] = None
    hms: Optional[str] = None


class BandBrightnessIntegratedInput(BaseModel):
    band: Band
    value: Optional[Any] = None
    units: Optional[BrightnessIntegratedUnits] = None
    error: Optional[Any] = None


class BandBrightnessSurfaceInput(BaseModel):
    band: Band
    value: Optional[Any] = None
    units: Optional[BrightnessSurfaceUnits] = None
    error: Optional[Any] = None


class BandNormalizedIntegratedInput(BaseModel):
    sed: Optional["UnnormalizedSedInput"] = None
    brightnesses: Optional[list["BandBrightnessIntegratedInput"]] = None


class BandNormalizedSurfaceInput(BaseModel):
    sed: Optional["UnnormalizedSedInput"] = None
    brightnesses: Optional[list["BandBrightnessSurfaceInput"]] = None


class GeminiCallPropertiesInput(BaseModel):
    type_: Optional[GeminiCallForProposalsType] = Field(alias=str("type"), default=None)
    coordinate_limits: Optional["SiteCoordinateLimitsInput"] = Field(
        alias=str("coordinateLimits"), default=None
    )
    instruments: Optional[list[Instrument]] = None
    proprietary_months: Optional[Any] = Field(
        alias=str("proprietaryMonths"), default=None
    )
    exchange_partners: Optional[list["CallForProposalsExchangePartnerInput"]] = Field(
        alias=str("exchangePartners"), default=None
    )


class KeckCallPropertiesInput(BaseModel):
    instruments: Optional[list[KeckInstrument]] = None
    coordinate_limits: Optional["CoordinateLimitsInput"] = Field(
        alias=str("coordinateLimits"), default=None
    )


class SubaruCallPropertiesInput(BaseModel):
    type_: Optional[SubaruCallForProposalsType] = Field(alias=str("type"), default=None)
    instruments: Optional[list[SubaruInstrument]] = None
    coordinate_limits: Optional["CoordinateLimitsInput"] = Field(
        alias=str("coordinateLimits"), default=None
    )


class CallForProposalsPropertiesInput(BaseModel):
    semester: Optional[Any] = None
    title: Optional[Any] = None
    active_start: Optional[Any] = Field(alias=str("activeStart"), default=None)
    active_end: Optional[Any] = Field(alias=str("activeEnd"), default=None)
    partners: Optional[list["CallForProposalsPartnerInput"]] = None
    submission_deadline_default: Optional[Any] = Field(
        alias=str("submissionDeadlineDefault"), default=None
    )
    existence: Optional[Existence] = None
    gemini: Optional["GeminiCallPropertiesInput"] = None
    keck: Optional["KeckCallPropertiesInput"] = None
    subaru: Optional["SubaruCallPropertiesInput"] = None


class SiteCoordinateLimitsInput(BaseModel):
    north: Optional["CoordinateLimitsInput"] = None
    south: Optional["CoordinateLimitsInput"] = None


class CoordinateLimitsInput(BaseModel):
    ra_start: Optional["RightAscensionInput"] = Field(
        alias=str("raStart"), default=None
    )
    ra_end: Optional["RightAscensionInput"] = Field(alias=str("raEnd"), default=None)
    dec_start: Optional["DeclinationInput"] = Field(alias=str("decStart"), default=None)
    dec_end: Optional["DeclinationInput"] = Field(alias=str("decEnd"), default=None)


class CallForProposalsPartnerInput(BaseModel):
    gemini_partner: Partner = Field(alias=str("geminiPartner"))
    submission_deadline_override: Optional[Any] = Field(
        alias=str("submissionDeadlineOverride"), default=None
    )


class CallForProposalsExchangePartnerInput(BaseModel):
    exchange_partner: ExchangePartner = Field(alias=str("exchangePartner"))
    submission_deadline_override: Optional[Any] = Field(
        alias=str("submissionDeadlineOverride"), default=None
    )


class CatalogInfoInput(BaseModel):
    name: Optional[CatalogName] = None
    id: Optional[Any] = None
    object_type: Optional[Any] = Field(alias=str("objectType"), default=None)


class ChangeProgramUserRoleInput(BaseModel):
    program_user_id: Any = Field(alias=str("programUserId"))
    new_role: ProgramUserRole = Field(alias=str("newRole"))


class ChangePrincipalInvestigatorInput(BaseModel):
    program_user_id: Any = Field(alias=str("programUserId"))


class CloneObservationInput(BaseModel):
    observation_id: Optional[Any] = Field(alias=str("observationId"), default=None)
    observation_reference: Optional[Any] = Field(
        alias=str("observationReference"), default=None
    )
    set_: Optional["ObservationPropertiesInput"] = Field(alias=str("SET"), default=None)


class CloneTargetInput(BaseModel):
    target_id: Any = Field(alias=str("targetId"))
    set_: Optional["TargetPropertiesInput"] = Field(alias=str("SET"), default=None)
    replace_in: Optional[list[Any]] = Field(alias=str("REPLACE_IN"), default=None)


class ConstraintSetInput(BaseModel):
    image_quality: Optional[ImageQualityPreset] = Field(
        alias=str("imageQuality"), default=None
    )
    cloud_extinction: Optional[CloudExtinctionPreset] = Field(
        alias=str("cloudExtinction"), default=None
    )
    sky_background: Optional[SkyBackground] = Field(
        alias=str("skyBackground"), default=None
    )
    water_vapor: Optional[WaterVapor] = Field(alias=str("waterVapor"), default=None)
    elevation_range: Optional["ElevationRangeInput"] = Field(
        alias=str("elevationRange"), default=None
    )


class ConditionsEntryInput(BaseModel):
    measurement: Optional["ConditionsMeasurementInput"] = None
    intuition: Optional["ConditionsIntuitionInput"] = None


class ConditionsMeasurementInput(BaseModel):
    source: ConditionsMeasurementSource
    seeing: Optional["AngleInput"] = None
    extinction: Optional[Any] = None
    wavelength: Optional["WavelengthInput"] = None
    azimuth: Optional["AngleInput"] = None
    elevation: Optional["AngleInput"] = None


class ConditionsIntuitionInput(BaseModel):
    expectation: Optional["ConditionsExpectationInput"] = None
    seeing_trend: Optional[SeeingTrend] = Field(alias=str("seeingTrend"), default=None)


class ConditionsExpectationInput(BaseModel):
    type_: ConditionsExpectationType = Field(alias=str("type"))
    timeframe: "TimeSpanInput"


class CoordinatesInput(BaseModel):
    ra: Optional["RightAscensionInput"] = None
    dec: Optional["DeclinationInput"] = None


class CreateCallForProposalsInput(BaseModel):
    set_: Optional["CallForProposalsPropertiesInput"] = Field(
        alias=str("SET"), default=None
    )


class CreateObservationInput(BaseModel):
    program_id: Optional[Any] = Field(alias=str("programId"), default=None)
    proposal_reference: Optional[Any] = Field(
        alias=str("proposalReference"), default=None
    )
    program_reference: Optional[Any] = Field(
        alias=str("programReference"), default=None
    )
    set_: Optional["ObservationPropertiesInput"] = Field(alias=str("SET"), default=None)


class CreateProgramInput(BaseModel):
    set_: Optional["ProgramPropertiesInput"] = Field(alias=str("SET"), default=None)


class CreateProgramNoteInput(BaseModel):
    program_id: Optional[Any] = Field(alias=str("programId"), default=None)
    proposal_reference: Optional[Any] = Field(
        alias=str("proposalReference"), default=None
    )
    program_reference: Optional[Any] = Field(
        alias=str("programReference"), default=None
    )
    set_: "ProgramNotePropertiesInput" = Field(alias=str("SET"))


class CreateProposalInput(BaseModel):
    program_id: Any = Field(alias=str("programId"))
    set_: "ProposalPropertiesInput" = Field(alias=str("SET"))


class CreateTargetInput(BaseModel):
    program_id: Optional[Any] = Field(alias=str("programId"), default=None)
    proposal_reference: Optional[Any] = Field(
        alias=str("proposalReference"), default=None
    )
    program_reference: Optional[Any] = Field(
        alias=str("programReference"), default=None
    )
    set_: "TargetPropertiesInput" = Field(alias=str("SET"))


class DatasetPropertiesInput(BaseModel):
    qa_state: Optional[DatasetQaState] = Field(alias=str("qaState"), default=None)
    comment: Optional[Any] = None


class DeclinationInput(BaseModel):
    microarcseconds: Optional[Any] = None
    degrees: Optional[Any] = None
    dms: Optional[Any] = None


class DeleteProgramUserInput(BaseModel):
    program_user_id: Any = Field(alias=str("programUserId"))


class DeleteProposalInput(BaseModel):
    program_id: Any = Field(alias=str("programId"))


class EditAsterismsPatchInput(BaseModel):
    add: Optional[list[Any]] = Field(alias=str("ADD"), default=None)
    delete: Optional[list[Any]] = Field(alias=str("DELETE"), default=None)


class ElevationRangeInput(BaseModel):
    air_mass: Optional["AirMassRangeInput"] = Field(alias=str("airMass"), default=None)
    hour_angle: Optional["HourAngleRangeInput"] = Field(
        alias=str("hourAngle"), default=None
    )


class EmissionLineIntegratedInput(BaseModel):
    wavelength: "WavelengthInput"
    line_width: Optional[Any] = Field(alias=str("lineWidth"), default=None)
    line_flux: Optional["LineFluxIntegratedInput"] = Field(
        alias=str("lineFlux"), default=None
    )


class EmissionLineSurfaceInput(BaseModel):
    wavelength: "WavelengthInput"
    line_width: Optional[Any] = Field(alias=str("lineWidth"), default=None)
    line_flux: Optional["LineFluxSurfaceInput"] = Field(
        alias=str("lineFlux"), default=None
    )


class EmissionLinesIntegratedInput(BaseModel):
    lines: Optional[list["EmissionLineIntegratedInput"]] = None
    flux_density_continuum: Optional["FluxDensityContinuumIntegratedInput"] = Field(
        alias=str("fluxDensityContinuum"), default=None
    )


class EmissionLinesSurfaceInput(BaseModel):
    lines: Optional[list["EmissionLineSurfaceInput"]] = None
    flux_density_continuum: Optional["FluxDensityContinuumSurfaceInput"] = Field(
        alias=str("fluxDensityContinuum"), default=None
    )


class ExposureTimeModeInput(BaseModel):
    signal_to_noise: Optional["SignalToNoiseExposureTimeModeInput"] = Field(
        alias=str("signalToNoise"), default=None
    )
    time_and_count: Optional["TimeAndCountExposureTimeModeInput"] = Field(
        alias=str("timeAndCount"), default=None
    )


class TimeAndCountExposureTimeModeInput(BaseModel):
    time: "TimeSpanInput"
    count: Any
    at: "WavelengthInput"


class FluxDensity(BaseModel):
    wavelength: "WavelengthInput"
    density: Any


class FluxDensityContinuumIntegratedInput(BaseModel):
    value: Any
    units: FluxDensityContinuumIntegratedUnits
    error: Optional[Any] = None


class FluxDensityContinuumSurfaceInput(BaseModel):
    value: Any
    units: FluxDensityContinuumSurfaceUnits
    error: Optional[Any] = None


class GaussianInput(BaseModel):
    fwhm: Optional["AngleInput"] = None
    spectral_definition: Optional["SpectralDefinitionIntegratedInput"] = Field(
        alias=str("spectralDefinition"), default=None
    )


class GmosCcdModeInput(BaseModel):
    x_bin: Optional[GmosBinning] = Field(alias=str("xBin"), default=None)
    y_bin: Optional[GmosBinning] = Field(alias=str("yBin"), default=None)
    amp_count: Optional[GmosAmpCount] = Field(alias=str("ampCount"), default=None)
    amp_gain: Optional[GmosAmpGain] = Field(alias=str("ampGain"), default=None)
    amp_read_mode: Optional[GmosAmpReadMode] = Field(
        alias=str("ampReadMode"), default=None
    )


class GmosCustomMaskInput(BaseModel):
    attachment_id: Optional[Any] = Field(alias=str("attachmentId"), default=None)
    slit_width: GmosCustomSlitWidth = Field(alias=str("slitWidth"))


class GmosNodAndShuffleInput(BaseModel):
    pos_a: "OffsetInput" = Field(alias=str("posA"))
    pos_b: "OffsetInput" = Field(alias=str("posB"))
    e_offset: GmosEOffsetting = Field(alias=str("eOffset"))
    shuffle_offset: Any = Field(alias=str("shuffleOffset"))
    shuffle_cycles: Any = Field(alias=str("shuffleCycles"))


class GmosNorthDynamicInput(BaseModel):
    exposure: "TimeSpanInput"
    readout: "GmosCcdModeInput"
    dtax: GmosDtax
    roi: GmosRoi
    grating_config: Optional["GmosNorthGratingConfigInput"] = Field(
        alias=str("gratingConfig"), default=None
    )
    filter_: Optional[GmosNorthFilter] = Field(alias=str("filter"), default=None)
    fpu: Optional["GmosNorthFpuInput"] = None


class GmosNorthFpuInput(BaseModel):
    custom_mask: Optional["GmosCustomMaskInput"] = Field(
        alias=str("customMask"), default=None
    )
    builtin: Optional[GmosNorthBuiltinFpu] = None


class GmosNorthGratingConfigInput(BaseModel):
    grating: GmosNorthGrating
    order: GmosGratingOrder
    wavelength: "WavelengthInput"


class GmosNorthLongSlitAcquisitionInput(BaseModel):
    explicit_filter: Optional[GmosNorthFilter] = Field(
        alias=str("explicitFilter"), default=None
    )
    explicit_roi: Optional[GmosLongSlitAcquisitionRoi] = Field(
        alias=str("explicitRoi"), default=None
    )
    exposure_time_mode: Optional["ExposureTimeModeInput"] = Field(
        alias=str("exposureTimeMode"), default=None
    )


class GmosNorthLongSlitInput(BaseModel):
    grating: Optional[GmosNorthGrating] = None
    filter_: Optional[GmosNorthFilter] = Field(alias=str("filter"), default=None)
    fpu: Optional[GmosNorthBuiltinFpu] = None
    central_wavelength: Optional["WavelengthInput"] = Field(
        alias=str("centralWavelength"), default=None
    )
    exposure_time_mode: Optional["ExposureTimeModeInput"] = Field(
        alias=str("exposureTimeMode"), default=None
    )
    explicit_x_bin: Optional[GmosBinning] = Field(
        alias=str("explicitXBin"), default=None
    )
    explicit_y_bin: Optional[GmosBinning] = Field(
        alias=str("explicitYBin"), default=None
    )
    explicit_amp_read_mode: Optional[GmosAmpReadMode] = Field(
        alias=str("explicitAmpReadMode"), default=None
    )
    explicit_amp_gain: Optional[GmosAmpGain] = Field(
        alias=str("explicitAmpGain"), default=None
    )
    explicit_roi: Optional[GmosRoi] = Field(alias=str("explicitRoi"), default=None)
    explicit_wavelength_dithers: Optional[list["WavelengthDitherInput"]] = Field(
        alias=str("explicitWavelengthDithers"), default=None
    )
    explicit_offsets: Optional[list["OffsetComponentInput"]] = Field(
        alias=str("explicitOffsets"), default=None
    )
    explicit_spatial_offsets: Optional[list["OffsetComponentInput"]] = Field(
        alias=str("explicitSpatialOffsets"), default=None
    )
    acquisition: Optional["GmosNorthLongSlitAcquisitionInput"] = None


class GmosNorthImagingInput(BaseModel):
    variant: Optional["ImagingVariantInput"] = None
    filters: Optional[list["GmosNorthImagingFilterInput"]] = None
    explicit_bin: Optional[GmosBinning] = Field(alias=str("explicitBin"), default=None)
    explicit_amp_read_mode: Optional[GmosAmpReadMode] = Field(
        alias=str("explicitAmpReadMode"), default=None
    )
    explicit_amp_gain: Optional[GmosAmpGain] = Field(
        alias=str("explicitAmpGain"), default=None
    )
    explicit_roi: Optional[GmosRoi] = Field(alias=str("explicitRoi"), default=None)


class GmosNorthStaticInput(BaseModel):
    stage_mode: Optional[GmosNorthStageMode] = Field(
        alias=str("stageMode"), default=None
    )
    detector: Optional[GmosNorthDetector] = None
    mos_pre_imaging: Optional[MosPreImaging] = Field(
        alias=str("mosPreImaging"), default=None
    )
    nod_and_shuffle: Optional["GmosNodAndShuffleInput"] = Field(
        alias=str("nodAndShuffle"), default=None
    )


class GmosSouthDynamicInput(BaseModel):
    exposure: "TimeSpanInput"
    readout: "GmosCcdModeInput"
    dtax: GmosDtax
    roi: GmosRoi
    grating_config: Optional["GmosSouthGratingConfigInput"] = Field(
        alias=str("gratingConfig"), default=None
    )
    filter_: Optional[GmosSouthFilter] = Field(alias=str("filter"), default=None)
    fpu: Optional["GmosSouthFpuInput"] = None


class GmosSouthFpuInput(BaseModel):
    custom_mask: Optional["GmosCustomMaskInput"] = Field(
        alias=str("customMask"), default=None
    )
    builtin: Optional[GmosSouthBuiltinFpu] = None


class GmosSouthGratingConfigInput(BaseModel):
    grating: GmosSouthGrating
    order: GmosGratingOrder
    wavelength: "WavelengthInput"


class GmosSouthLongSlitAcquisitionInput(BaseModel):
    explicit_filter: Optional[GmosSouthFilter] = Field(
        alias=str("explicitFilter"), default=None
    )
    explicit_roi: Optional[GmosLongSlitAcquisitionRoi] = Field(
        alias=str("explicitRoi"), default=None
    )
    exposure_time_mode: Optional["ExposureTimeModeInput"] = Field(
        alias=str("exposureTimeMode"), default=None
    )


class GmosSouthLongSlitInput(BaseModel):
    grating: Optional[GmosSouthGrating] = None
    filter_: Optional[GmosSouthFilter] = Field(alias=str("filter"), default=None)
    fpu: Optional[GmosSouthBuiltinFpu] = None
    central_wavelength: Optional["WavelengthInput"] = Field(
        alias=str("centralWavelength"), default=None
    )
    exposure_time_mode: Optional["ExposureTimeModeInput"] = Field(
        alias=str("exposureTimeMode"), default=None
    )
    explicit_x_bin: Optional[GmosBinning] = Field(
        alias=str("explicitXBin"), default=None
    )
    explicit_y_bin: Optional[GmosBinning] = Field(
        alias=str("explicitYBin"), default=None
    )
    explicit_amp_read_mode: Optional[GmosAmpReadMode] = Field(
        alias=str("explicitAmpReadMode"), default=None
    )
    explicit_amp_gain: Optional[GmosAmpGain] = Field(
        alias=str("explicitAmpGain"), default=None
    )
    explicit_roi: Optional[GmosRoi] = Field(alias=str("explicitRoi"), default=None)
    explicit_wavelength_dithers: Optional[list["WavelengthDitherInput"]] = Field(
        alias=str("explicitWavelengthDithers"), default=None
    )
    explicit_offsets: Optional[list["OffsetComponentInput"]] = Field(
        alias=str("explicitOffsets"), default=None
    )
    explicit_spatial_offsets: Optional[list["OffsetComponentInput"]] = Field(
        alias=str("explicitSpatialOffsets"), default=None
    )
    acquisition: Optional["GmosSouthLongSlitAcquisitionInput"] = None


class GmosNorthMosInput(BaseModel):
    grating: Optional[GmosNorthGrating] = None
    filter_: Optional[GmosNorthFilter] = Field(alias=str("filter"), default=None)
    custom_mask: Optional["GmosCustomMaskInput"] = Field(
        alias=str("customMask"), default=None
    )
    central_wavelength: Optional["WavelengthInput"] = Field(
        alias=str("centralWavelength"), default=None
    )
    acquisition_type: Optional[GmosMosAcquisitionType] = Field(
        alias=str("acquisitionType"), default=None
    )
    exposure_time_mode: Optional["ExposureTimeModeInput"] = Field(
        alias=str("exposureTimeMode"), default=None
    )
    explicit_x_bin: Optional[GmosBinning] = Field(
        alias=str("explicitXBin"), default=None
    )
    explicit_y_bin: Optional[GmosBinning] = Field(
        alias=str("explicitYBin"), default=None
    )
    explicit_amp_read_mode: Optional[GmosAmpReadMode] = Field(
        alias=str("explicitAmpReadMode"), default=None
    )
    explicit_amp_gain: Optional[GmosAmpGain] = Field(
        alias=str("explicitAmpGain"), default=None
    )
    explicit_roi: Optional[GmosRoi] = Field(alias=str("explicitRoi"), default=None)
    explicit_wavelength_dithers: Optional[list["WavelengthDitherInput"]] = Field(
        alias=str("explicitWavelengthDithers"), default=None
    )
    explicit_offsets: Optional[list["OffsetComponentInput"]] = Field(
        alias=str("explicitOffsets"), default=None
    )
    acquisition: Optional["GmosNorthMosAcquisitionInput"] = None


class GmosNorthMosAcquisitionInput(BaseModel):
    explicit_filter: Optional[GmosNorthFilter] = Field(
        alias=str("explicitFilter"), default=None
    )
    exposure_time_mode: Optional["ExposureTimeModeInput"] = Field(
        alias=str("exposureTimeMode"), default=None
    )


class GmosSouthMosInput(BaseModel):
    grating: Optional[GmosSouthGrating] = None
    filter_: Optional[GmosSouthFilter] = Field(alias=str("filter"), default=None)
    custom_mask: Optional["GmosCustomMaskInput"] = Field(
        alias=str("customMask"), default=None
    )
    central_wavelength: Optional["WavelengthInput"] = Field(
        alias=str("centralWavelength"), default=None
    )
    acquisition_type: Optional[GmosMosAcquisitionType] = Field(
        alias=str("acquisitionType"), default=None
    )
    exposure_time_mode: Optional["ExposureTimeModeInput"] = Field(
        alias=str("exposureTimeMode"), default=None
    )
    explicit_x_bin: Optional[GmosBinning] = Field(
        alias=str("explicitXBin"), default=None
    )
    explicit_y_bin: Optional[GmosBinning] = Field(
        alias=str("explicitYBin"), default=None
    )
    explicit_amp_read_mode: Optional[GmosAmpReadMode] = Field(
        alias=str("explicitAmpReadMode"), default=None
    )
    explicit_amp_gain: Optional[GmosAmpGain] = Field(
        alias=str("explicitAmpGain"), default=None
    )
    explicit_roi: Optional[GmosRoi] = Field(alias=str("explicitRoi"), default=None)
    explicit_wavelength_dithers: Optional[list["WavelengthDitherInput"]] = Field(
        alias=str("explicitWavelengthDithers"), default=None
    )
    explicit_offsets: Optional[list["OffsetComponentInput"]] = Field(
        alias=str("explicitOffsets"), default=None
    )
    acquisition: Optional["GmosSouthMosAcquisitionInput"] = None


class GmosSouthMosAcquisitionInput(BaseModel):
    explicit_filter: Optional[GmosSouthFilter] = Field(
        alias=str("explicitFilter"), default=None
    )
    exposure_time_mode: Optional["ExposureTimeModeInput"] = Field(
        alias=str("exposureTimeMode"), default=None
    )


class GmosSouthImagingFilterInput(BaseModel):
    filter_: GmosSouthFilter = Field(alias=str("filter"))
    exposure_time_mode: Optional["ExposureTimeModeInput"] = Field(
        alias=str("exposureTimeMode"), default=None
    )


class GmosSouthImagingInput(BaseModel):
    variant: Optional["ImagingVariantInput"] = None
    filters: Optional[list["GmosSouthImagingFilterInput"]] = None
    explicit_bin: Optional[GmosBinning] = Field(alias=str("explicitBin"), default=None)
    explicit_amp_read_mode: Optional[GmosAmpReadMode] = Field(
        alias=str("explicitAmpReadMode"), default=None
    )
    explicit_amp_gain: Optional[GmosAmpGain] = Field(
        alias=str("explicitAmpGain"), default=None
    )
    explicit_roi: Optional[GmosRoi] = Field(alias=str("explicitRoi"), default=None)


class GmosSouthStaticInput(BaseModel):
    stage_mode: Optional[GmosSouthStageMode] = Field(
        alias=str("stageMode"), default=None
    )
    detector: Optional[GmosSouthDetector] = None
    mos_pre_imaging: Optional[MosPreImaging] = Field(
        alias=str("mosPreImaging"), default=None
    )
    nod_and_shuffle: Optional["GmosNodAndShuffleInput"] = Field(
        alias=str("nodAndShuffle"), default=None
    )


class CloneGroupInput(BaseModel):
    group_id: Any = Field(alias=str("groupId"))
    set_: Optional["GroupPropertiesInput"] = Field(alias=str("SET"), default=None)


class HourAngleRangeInput(BaseModel):
    min_hours: Optional[Any] = Field(alias=str("minHours"), default=None)
    max_hours: Optional[Any] = Field(alias=str("maxHours"), default=None)


class LineFluxIntegratedInput(BaseModel):
    value: Any
    units: LineFluxIntegratedUnits


class LineFluxSurfaceInput(BaseModel):
    value: Any
    units: LineFluxSurfaceUnits


class LinkUserInput(BaseModel):
    program_user_id: Any = Field(alias=str("programUserId"))
    user_id: Any = Field(alias=str("userId"))


class CreateUserInvitationInput(BaseModel):
    program_user_id: Any = Field(alias=str("programUserId"))
    recipient_email: Any = Field(alias=str("recipientEmail"))


class RedeemUserInvitationInput(BaseModel):
    key: Any
    accept: Optional[bool] = True


class RevokeUserInvitationInput(BaseModel):
    id: Any


class SetObservationWorkflowStateInput(BaseModel):
    observation_id: Any = Field(alias=str("observationId"))
    state: ObservationWorkflowState


class UserSuppliedEphemerisElement(BaseModel):
    when: Optional[Any] = None
    coordinates: Optional["CoordinatesInput"] = None
    velocity: Optional["OffsetInput"] = None


class UserSuppliedEphemeris(BaseModel):
    gn: list["UserSuppliedEphemerisElement"]
    gs: list["UserSuppliedEphemerisElement"]


class NonsiderealInput(BaseModel):
    key_type: Optional[EphemerisKeyType] = Field(alias=str("keyType"), default=None)
    des: Optional[Any] = None
    key: Optional[Any] = None
    ephemeris: Optional["UserSuppliedEphemeris"] = None


class ConfigurationRequestProperties(BaseModel):
    status: Optional[ConfigurationRequestStatus] = None
    justification: Optional[Any] = None
    feedback: Optional[Any] = None


class SchedulingConstraintsInput(BaseModel):
    too_activation: Optional[TooActivation] = Field(
        alias=str("tooActivation"), default=None
    )
    explicit_execution_requirement: Optional[ExecutionRequirement] = Field(
        alias=str("explicitExecutionRequirement"), default=None
    )
    is_splittable: Optional[bool] = Field(alias=str("isSplittable"), default=None)
    timing_windows: Optional[list["TimingWindowInput"]] = Field(
        alias=str("timingWindows"), default=None
    )


class ObservationPropertiesInput(BaseModel):
    subtitle: Optional[Any] = None
    science_band: Optional[ScienceBand] = Field(alias=str("scienceBand"), default=None)
    pos_angle_constraint: Optional["PosAngleConstraintInput"] = Field(
        alias=str("posAngleConstraint"), default=None
    )
    target_environment: Optional["TargetEnvironmentInput"] = Field(
        alias=str("targetEnvironment"), default=None
    )
    constraint_set: Optional["ConstraintSetInput"] = Field(
        alias=str("constraintSet"), default=None
    )
    timing_windows: Optional[list["TimingWindowInput"]] = Field(
        alias=str("timingWindows"), default=None
    )
    scheduling_constraints: Optional["SchedulingConstraintsInput"] = Field(
        alias=str("schedulingConstraints"), default=None
    )
    attachments: Optional[list[Any]] = None
    science_requirements: Optional["ScienceRequirementsInput"] = Field(
        alias=str("scienceRequirements"), default=None
    )
    observing_mode: Optional["ObservingModeInput"] = Field(
        alias=str("observingMode"), default=None
    )
    existence: Optional[Existence] = None
    group_id: Optional[Any] = Field(alias=str("groupId"), default=None)
    group_index: Optional[Any] = Field(alias=str("groupIndex"), default=None)
    observer_notes: Optional[Any] = Field(alias=str("observerNotes"), default=None)


class ObservationTimesInput(BaseModel):
    observation_time: Optional[Any] = Field(alias=str("observationTime"), default=None)
    observation_duration: Optional["TimeSpanInput"] = Field(
        alias=str("observationDuration"), default=None
    )


class OffsetComponentInput(BaseModel):
    microarcseconds: Optional[Any] = None
    milliarcseconds: Optional[Any] = None
    arcseconds: Optional[Any] = None


class OffsetInput(BaseModel):
    p: "OffsetComponentInput"
    q: "OffsetComponentInput"


class TelescopeConfigGeneratorInput(BaseModel):
    enumerated: Optional["EnumeratedTelescopeConfigGeneratorInput"] = None
    random: Optional["RandomTelescopeConfigGeneratorInput"] = None
    spiral: Optional["SpiralTelescopeConfigGeneratorInput"] = None
    uniform: Optional["UniformTelescopeConfigGeneratorInput"] = None


class EnumeratedTelescopeConfigGeneratorInput(BaseModel):
    values: list["TelescopeConfigInput"]


class RandomTelescopeConfigGeneratorInput(BaseModel):
    size: "AngleInput"
    center: Optional["OffsetInput"] = None
    seed: Optional[Any] = None


class SpiralTelescopeConfigGeneratorInput(BaseModel):
    size: "AngleInput"
    center: Optional["OffsetInput"] = None
    seed: Optional[Any] = None


class UniformTelescopeConfigGeneratorInput(BaseModel):
    corner_a: "OffsetInput" = Field(alias=str("cornerA"))
    corner_b: "OffsetInput" = Field(alias=str("cornerB"))


class ParallaxInput(BaseModel):
    microarcseconds: Optional[Any] = None
    milliarcseconds: Optional[Any] = None


class PartnerLinkInput(BaseModel):
    link_type: Optional[PartnerLinkType] = Field(alias=str("linkType"), default=None)
    gemini_partner: Optional[Partner] = Field(alias=str("geminiPartner"), default=None)
    exchange_partner: Optional[ExchangePartner] = Field(
        alias=str("exchangePartner"), default=None
    )


class PartnerSplitInput(BaseModel):
    partner: Partner
    percent: Any


class PosAngleConstraintInput(BaseModel):
    mode: Optional[PosAngleConstraintMode] = None
    angle: Optional["AngleInput"] = None


class ProgramPropertiesInput(BaseModel):
    name: Optional[Any] = None
    description: Optional[Any] = None
    goa: Optional["GoaPropertiesInput"] = None
    existence: Optional[Existence] = None
    active_start: Optional[Any] = Field(alias=str("activeStart"), default=None)
    active_end: Optional[Any] = Field(alias=str("activeEnd"), default=None)


class ProgramNotePropertiesInput(BaseModel):
    title: Optional[Any] = None
    text: Optional[Any] = None
    is_private: Optional[bool] = Field(alias=str("isPrivate"), default=None)
    existence: Optional[Existence] = None


class ProgramUserPropertiesInput(BaseModel):
    partner_link: Optional["PartnerLinkInput"] = Field(
        alias=str("partnerLink"), default=None
    )
    preferred_profile: Optional["UserProfileInput"] = Field(
        alias=str("preferredProfile"), default=None
    )
    educational_status: Optional[EducationalStatus] = Field(
        alias=str("educationalStatus"), default=None
    )
    thesis: Optional[bool] = None
    gender: Optional[Gender] = None
    affiliation: Optional[Any] = None
    has_data_access: Optional[bool] = Field(alias=str("hasDataAccess"), default=None)
    classical_visitor: Optional[bool] = Field(
        alias=str("classicalVisitor"), default=None
    )


class ProperMotionComponentInput(BaseModel):
    microarcseconds_per_year: Optional[Any] = Field(
        alias=str("microarcsecondsPerYear"), default=None
    )
    milliarcseconds_per_year: Optional[Any] = Field(
        alias=str("milliarcsecondsPerYear"), default=None
    )


class ProperMotionInput(BaseModel):
    ra: "ProperMotionComponentInput"
    dec: "ProperMotionComponentInput"


class GeminiProposalTypeInput(BaseModel):
    classical: Optional["ClassicalInput"] = None
    demo_science: Optional["DemoScienceInput"] = Field(
        alias=str("demoScience"), default=None
    )
    directors_time: Optional["DirectorsTimeInput"] = Field(
        alias=str("directorsTime"), default=None
    )
    fast_turnaround: Optional["FastTurnaroundInput"] = Field(
        alias=str("fastTurnaround"), default=None
    )
    large_program: Optional["LargeProgramInput"] = Field(
        alias=str("largeProgram"), default=None
    )
    poor_weather: Optional["PoorWeatherInput"] = Field(
        alias=str("poorWeather"), default=None
    )
    queue: Optional["QueueInput"] = None
    system_verification: Optional["SystemVerificationInput"] = Field(
        alias=str("systemVerification"), default=None
    )


class KeckProposalTypeInput(BaseModel):
    min_percent_time: Optional[Any] = Field(alias=str("minPercentTime"), default=None)
    partner_splits: Optional[list["PartnerSplitInput"]] = Field(
        alias=str("partnerSplits"), default=None
    )


class SubaruProposalTypeInput(BaseModel):
    min_percent_time: Optional[Any] = Field(alias=str("minPercentTime"), default=None)
    partner_splits: Optional[list["PartnerSplitInput"]] = Field(
        alias=str("partnerSplits"), default=None
    )


class ClassicalInput(BaseModel):
    min_percent_time: Optional[Any] = Field(alias=str("minPercentTime"), default=None)
    partner_splits: Optional[list["PartnerSplitInput"]] = Field(
        alias=str("partnerSplits"), default=None
    )
    exchange_partner: Optional[ExchangePartner] = Field(
        alias=str("exchangePartner"), default=None
    )
    aeon_multi_facility: Optional[bool] = Field(
        alias=str("aeonMultiFacility"), default=None
    )
    jwst_synergy: Optional[bool] = Field(alias=str("jwstSynergy"), default=None)
    us_long_term: Optional[bool] = Field(alias=str("usLongTerm"), default=None)


class DemoScienceInput(BaseModel):
    explicit_too_activation_ceiling: Optional[TooActivation] = Field(
        alias=str("explicitTooActivationCeiling"), default=None
    )
    min_percent_time: Optional[Any] = Field(alias=str("minPercentTime"), default=None)


class DirectorsTimeInput(BaseModel):
    explicit_too_activation_ceiling: Optional[TooActivation] = Field(
        alias=str("explicitTooActivationCeiling"), default=None
    )
    min_percent_time: Optional[Any] = Field(alias=str("minPercentTime"), default=None)


class FastTurnaroundInput(BaseModel):
    explicit_too_activation_ceiling: Optional[TooActivation] = Field(
        alias=str("explicitTooActivationCeiling"), default=None
    )
    min_percent_time: Optional[Any] = Field(alias=str("minPercentTime"), default=None)
    reviewer_id: Optional[Any] = Field(alias=str("reviewerId"), default=None)
    mentor_id: Optional[Any] = Field(alias=str("mentorId"), default=None)


class LargeProgramInput(BaseModel):
    explicit_too_activation_ceiling: Optional[TooActivation] = Field(
        alias=str("explicitTooActivationCeiling"), default=None
    )
    min_percent_time: Optional[Any] = Field(alias=str("minPercentTime"), default=None)
    min_percent_total_time: Optional[Any] = Field(
        alias=str("minPercentTotalTime"), default=None
    )
    total_time: Optional["TimeSpanInput"] = Field(alias=str("totalTime"), default=None)
    aeon_multi_facility: Optional[bool] = Field(
        alias=str("aeonMultiFacility"), default=None
    )
    jwst_synergy: Optional[bool] = Field(alias=str("jwstSynergy"), default=None)


class DeleteSequenceInput(BaseModel):
    observation_id: Optional[Any] = Field(alias=str("observationId"), default=None)
    observation_reference: Optional[Any] = Field(
        alias=str("observationReference"), default=None
    )


class PoorWeatherInput(BaseModel):
    ignore: Optional[Ignore] = None


class QueueInput(BaseModel):
    explicit_too_activation_ceiling: Optional[TooActivation] = Field(
        alias=str("explicitTooActivationCeiling"), default=None
    )
    min_percent_time: Optional[Any] = Field(alias=str("minPercentTime"), default=None)
    partner_splits: Optional[list["PartnerSplitInput"]] = Field(
        alias=str("partnerSplits"), default=None
    )
    exchange_partner: Optional[ExchangePartner] = Field(
        alias=str("exchangePartner"), default=None
    )
    consider_for_band_3: Optional[ConsiderForBand3] = Field(
        alias=str("considerForBand3"), default=None
    )
    aeon_multi_facility: Optional[bool] = Field(
        alias=str("aeonMultiFacility"), default=None
    )
    jwst_synergy: Optional[bool] = Field(alias=str("jwstSynergy"), default=None)
    us_long_term: Optional[bool] = Field(alias=str("usLongTerm"), default=None)


class SystemVerificationInput(BaseModel):
    explicit_too_activation_ceiling: Optional[TooActivation] = Field(
        alias=str("explicitTooActivationCeiling"), default=None
    )
    min_percent_time: Optional[Any] = Field(alias=str("minPercentTime"), default=None)


class ProposalPropertiesInput(BaseModel):
    category: Optional[TacCategory] = None
    call_id: Optional[Any] = Field(alias=str("callId"), default=None)
    gemini: Optional["GeminiProposalTypeInput"] = None
    keck: Optional["KeckProposalTypeInput"] = None
    subaru: Optional["SubaruProposalTypeInput"] = None


class RadialVelocityInput(BaseModel):
    centimeters_per_second: Optional[Any] = Field(
        alias=str("centimetersPerSecond"), default=None
    )
    meters_per_second: Optional[Any] = Field(alias=str("metersPerSecond"), default=None)
    kilometers_per_second: Optional[Any] = Field(
        alias=str("kilometersPerSecond"), default=None
    )


class RecordDatasetInput(BaseModel):
    step_id: Any = Field(alias=str("stepId"))
    visit_id: Any = Field(alias=str("visitId"))
    filename: Any
    qa_state: Optional[DatasetQaState] = Field(alias=str("qaState"), default=None)
    comment: Optional[Any] = None
    idempotency_key: Optional[Any] = Field(alias=str("idempotencyKey"), default=None)


class RecordVisitInput(BaseModel):
    observation_id: Any = Field(alias=str("observationId"))
    client_time: Optional[Any] = Field(alias=str("clientTime"), default=None)
    idempotency_key: Optional[Any] = Field(alias=str("idempotencyKey"), default=None)


class RecordGmosNorthVisitInput(BaseModel):
    observation_id: Any = Field(alias=str("observationId"))
    gmos_north: "GmosNorthStaticInput" = Field(alias=str("gmosNorth"))
    time: Optional[Any] = None
    idempotency_key: Optional[Any] = Field(alias=str("idempotencyKey"), default=None)


class RecordGmosSouthVisitInput(BaseModel):
    observation_id: Any = Field(alias=str("observationId"))
    gmos_south: "GmosSouthStaticInput" = Field(alias=str("gmosSouth"))
    time: Optional[Any] = None
    idempotency_key: Optional[Any] = Field(alias=str("idempotencyKey"), default=None)


class RefreshArchiveDuplicationInput(BaseModel):
    observation_id: Optional[Any] = Field(alias=str("observationId"), default=None)
    observation_reference: Optional[Any] = Field(
        alias=str("observationReference"), default=None
    )


class ResetAcquisitionInput(BaseModel):
    observation_id: Optional[Any] = Field(alias=str("observationId"), default=None)
    observation_reference: Optional[Any] = Field(
        alias=str("observationReference"), default=None
    )


class RightAscensionInput(BaseModel):
    microseconds: Optional[Any] = None
    degrees: Optional[Any] = None
    hours: Optional[Any] = None
    hms: Optional[Any] = None


class ObservingModeInput(BaseModel):
    exchange: Optional["ExchangeInput"] = None
    flamingos_2_imaging: Optional["Flamingos2ImagingInput"] = Field(
        alias=str("flamingos2Imaging"), default=None
    )
    flamingos_2_long_slit: Optional["Flamingos2LongSlitInput"] = Field(
        alias=str("flamingos2LongSlit"), default=None
    )
    ghost_ifu: Optional["GhostIfuInput"] = Field(alias=str("ghostIfu"), default=None)
    gmos_north_imaging: Optional["GmosNorthImagingInput"] = Field(
        alias=str("gmosNorthImaging"), default=None
    )
    gmos_north_long_slit: Optional["GmosNorthLongSlitInput"] = Field(
        alias=str("gmosNorthLongSlit"), default=None
    )
    gmos_north_mos: Optional["GmosNorthMosInput"] = Field(
        alias=str("gmosNorthMos"), default=None
    )
    gmos_south_imaging: Optional["GmosSouthImagingInput"] = Field(
        alias=str("gmosSouthImaging"), default=None
    )
    gmos_south_long_slit: Optional["GmosSouthLongSlitInput"] = Field(
        alias=str("gmosSouthLongSlit"), default=None
    )
    gmos_south_mos: Optional["GmosSouthMosInput"] = Field(
        alias=str("gmosSouthMos"), default=None
    )
    gnirs_imaging: Optional["GnirsImagingInput"] = Field(
        alias=str("gnirsImaging"), default=None
    )
    gnirs_spectroscopy: Optional["GnirsSpectroscopyInput"] = Field(
        alias=str("gnirsSpectroscopy"), default=None
    )
    igrins_2_long_slit: Optional["Igrins2LongSlitInput"] = Field(
        alias=str("igrins2LongSlit"), default=None
    )
    visitor: Optional["VisitorInput"] = None


class VisitorInput(BaseModel):
    mode: Optional[VisitorObservingModeType] = None
    central_wavelength: Optional["WavelengthInput"] = Field(
        alias=str("centralWavelength"), default=None
    )
    ags_diameter: Optional["AngleInput"] = Field(alias=str("agsDiameter"), default=None)
    science_fov_diameter: Optional["AngleInput"] = Field(
        alias=str("scienceFovDiameter"), default=None
    )
    name: Optional[Any] = None
    total_request_time: Optional["TimeSpanInput"] = Field(
        alias=str("totalRequestTime"), default=None
    )


class ExchangeInput(BaseModel):
    keck_instrument: Optional[KeckInstrument] = Field(
        alias=str("keckInstrument"), default=None
    )
    subaru_instrument: Optional[SubaruInstrument] = Field(
        alias=str("subaruInstrument"), default=None
    )
    total_request_time: Optional["TimeSpanInput"] = Field(
        alias=str("totalRequestTime"), default=None
    )


class ScienceRequirementsInput(BaseModel):
    exposure_time_mode: Optional["ExposureTimeModeInput"] = Field(
        alias=str("exposureTimeMode"), default=None
    )
    spectroscopy: Optional["SpectroscopyScienceRequirementsInput"] = None
    imaging: Optional["ImagingScienceRequirementsInput"] = None


class SetAllocationsInput(BaseModel):
    program_id: Optional[Any] = Field(alias=str("programId"), default=None)
    proposal_reference: Optional[Any] = Field(
        alias=str("proposalReference"), default=None
    )
    program_reference: Optional[Any] = Field(
        alias=str("programReference"), default=None
    )
    allocations: list["AllocationInput"]


class SetGuideTargetNameInput(BaseModel):
    observation_id: Optional[Any] = Field(alias=str("observationId"), default=None)
    observation_reference: Optional[Any] = Field(
        alias=str("observationReference"), default=None
    )
    target_name: Optional[Any] = Field(alias=str("targetName"), default=None)


class SetProgramReferenceInput(BaseModel):
    program_id: Optional[Any] = Field(alias=str("programId"), default=None)
    proposal_reference: Optional[Any] = Field(
        alias=str("proposalReference"), default=None
    )
    program_reference: Optional[Any] = Field(
        alias=str("programReference"), default=None
    )
    set_: "ProgramReferencePropertiesInput" = Field(alias=str("SET"))


class ProgramReferencePropertiesInput(BaseModel):
    calibration: Optional["ProgramReferencePropertiesCalibrationInput"] = None
    commissioning: Optional["ProgramReferencePropertiesCommissioningInput"] = None
    engineering: Optional["ProgramReferencePropertiesEngineeringInput"] = None
    example: Optional["ProgramReferencePropertiesExampleInput"] = None
    keck: Optional["ProgramReferencePropertiesKeckInput"] = None
    library: Optional["ProgramReferencePropertiesLibraryInput"] = None
    monitoring: Optional["ProgramReferencePropertiesMonitoringInput"] = None
    science: Optional["ProgramReferencePropertiesScienceInput"] = None
    subaru: Optional["ProgramReferencePropertiesSubaruInput"] = None
    system: Optional["ProgramReferencePropertiesSystemInput"] = None


class SetProgramResourceLimitInput(BaseModel):
    program_id: Any = Field(alias=str("programId"))
    limit: Any


class ProgramReferencePropertiesCalibrationInput(BaseModel):
    semester: Any
    instrument: Instrument


class ProgramReferencePropertiesCommissioningInput(BaseModel):
    semester: Any
    instrument: Instrument


class ProgramReferencePropertiesEngineeringInput(BaseModel):
    semester: Any
    instrument: Instrument


class ProgramReferencePropertiesExampleInput(BaseModel):
    instrument: Instrument


class ProgramReferencePropertiesLibraryInput(BaseModel):
    instrument: Instrument
    description: Any


class ProgramReferencePropertiesMonitoringInput(BaseModel):
    semester: Any
    instrument: Instrument


class ProgramReferencePropertiesKeckInput(BaseModel):
    semester: Any


class ProgramReferencePropertiesScienceInput(BaseModel):
    semester: Any
    science_subtype: ScienceSubtype = Field(alias=str("scienceSubtype"))


class ProgramReferencePropertiesSubaruInput(BaseModel):
    semester: Any
    subaru_type: SubaruCallForProposalsType = Field(alias=str("subaruType"))


class ProgramReferencePropertiesSystemInput(BaseModel):
    description: Any


class SetProposalStatusInput(BaseModel):
    program_id: Optional[Any] = Field(alias=str("programId"), default=None)
    proposal_reference: Optional[Any] = Field(
        alias=str("proposalReference"), default=None
    )
    program_reference: Optional[Any] = Field(
        alias=str("programReference"), default=None
    )
    status: ProposalStatus


class SiderealInput(BaseModel):
    ra: Optional["RightAscensionInput"] = None
    dec: Optional["DeclinationInput"] = None
    epoch: Optional[Any] = None
    proper_motion: Optional["ProperMotionInput"] = Field(
        alias=str("properMotion"), default=None
    )
    radial_velocity: Optional["RadialVelocityInput"] = Field(
        alias=str("radialVelocity"), default=None
    )
    parallax: Optional["ParallaxInput"] = None
    catalog_info: Optional["CatalogInfoInput"] = Field(
        alias=str("catalogInfo"), default=None
    )


class OpportunityInput(BaseModel):
    region: "RegionInput"


class RegionInput(BaseModel):
    right_ascension_arc: "RightAscensionArcInput" = Field(
        alias=str("rightAscensionArc")
    )
    declination_arc: "DeclinationArcInput" = Field(alias=str("declinationArc"))


class RightAscensionArcInput(BaseModel):
    type_: ArcType = Field(alias=str("type"))
    start: Optional["RightAscensionInput"] = None
    end: Optional["RightAscensionInput"] = None


class DeclinationArcInput(BaseModel):
    type_: ArcType = Field(alias=str("type"))
    start: Optional["DeclinationInput"] = None
    end: Optional["DeclinationInput"] = None


class SignalToNoiseExposureTimeModeInput(BaseModel):
    value: Any
    at: "WavelengthInput"


class SourceProfileInput(BaseModel):
    point: Optional["SpectralDefinitionIntegratedInput"] = None
    uniform: Optional["SpectralDefinitionSurfaceInput"] = None
    gaussian: Optional["GaussianInput"] = None


class SpectralDefinitionIntegratedInput(BaseModel):
    band_normalized: Optional["BandNormalizedIntegratedInput"] = Field(
        alias=str("bandNormalized"), default=None
    )
    emission_lines: Optional["EmissionLinesIntegratedInput"] = Field(
        alias=str("emissionLines"), default=None
    )


class SpectralDefinitionSurfaceInput(BaseModel):
    band_normalized: Optional["BandNormalizedSurfaceInput"] = Field(
        alias=str("bandNormalized"), default=None
    )
    emission_lines: Optional["EmissionLinesSurfaceInput"] = Field(
        alias=str("emissionLines"), default=None
    )


class SpectroscopyScienceRequirementsInput(BaseModel):
    wavelength: Optional["WavelengthInput"] = None
    resolution: Optional[Any] = None
    wavelength_coverage: Optional["WavelengthInput"] = Field(
        alias=str("wavelengthCoverage"), default=None
    )
    focal_plane: Optional[FocalPlane] = Field(alias=str("focalPlane"), default=None)
    focal_plane_angle: Optional["AngleInput"] = Field(
        alias=str("focalPlaneAngle"), default=None
    )
    capability: Optional[SpectroscopyCapability] = None


class StepConfigInput(BaseModel):
    bias: Optional[bool] = None
    dark: Optional[bool] = None
    gcal: Optional["StepConfigGcalInput"] = None
    science: Optional[bool] = None
    smart_gcal: Optional["StepConfigSmartGcalInput"] = Field(
        alias=str("smartGcal"), default=None
    )


class StepConfigGcalInput(BaseModel):
    arcs: Optional[list[GcalArc]] = None
    continuum: Optional[GcalContinuum] = None
    diffuser: GcalDiffuser
    filter_: GcalFilter = Field(alias=str("filter"))
    shutter: GcalShutter


class StepConfigSmartGcalInput(BaseModel):
    smart_gcal_type: SmartGcalType = Field(alias=str("smartGcalType"))


class ObscalcUpdateInput(BaseModel):
    program_id: Optional[Any] = Field(alias=str("programId"), default=None)
    observation_id: Optional[Any] = Field(alias=str("observationId"), default=None)
    old_calculation_state: Optional["WhereOptionEqCalculationState"] = Field(
        alias=str("oldCalculationState"), default=None
    )
    old_state: Optional["WhereOptionEqCalculationState"] = Field(
        alias=str("oldState"), default=None
    )
    new_calculation_state: Optional["WhereOptionEqCalculationState"] = Field(
        alias=str("newCalculationState"), default=None
    )
    new_state: Optional["WhereOptionEqCalculationState"] = Field(
        alias=str("newState"), default=None
    )
    executable_only: Optional[bool] = Field(alias=str("executableOnly"), default=False)


class WhereOrderCalculationState(BaseModel):
    eq: Optional[CalculationState] = Field(alias=str("EQ"), default=None)
    neq: Optional[CalculationState] = Field(alias=str("NEQ"), default=None)
    in_: Optional[list[CalculationState]] = Field(alias=str("IN"), default=None)
    nin: Optional[list[CalculationState]] = Field(alias=str("NIN"), default=None)
    gt: Optional[CalculationState] = Field(alias=str("GT"), default=None)
    lt: Optional[CalculationState] = Field(alias=str("LT"), default=None)
    gte: Optional[CalculationState] = Field(alias=str("GTE"), default=None)
    lte: Optional[CalculationState] = Field(alias=str("LTE"), default=None)


class WhereOptionEqCalculationState(BaseModel):
    is_null: Optional[bool] = Field(alias=str("IS_NULL"), default=None)
    eq: Optional[CalculationState] = Field(alias=str("EQ"), default=None)
    neq: Optional[CalculationState] = Field(alias=str("NEQ"), default=None)
    in_: Optional[list[CalculationState]] = Field(alias=str("IN"), default=None)
    nin: Optional[list[CalculationState]] = Field(alias=str("NIN"), default=None)


class ExecutionEventAddedInput(BaseModel):
    program_id: Optional[Any] = Field(alias=str("programId"), default=None)
    observation_id: Optional[Any] = Field(alias=str("observationId"), default=None)
    visit_id: Optional[Any] = Field(alias=str("visitId"), default=None)
    event_type: Optional["WhereEqExecutionEventType"] = Field(
        alias=str("eventType"), default=None
    )


class TargetEditInput(BaseModel):
    target_id: Optional[Any] = Field(alias=str("targetId"), default=None)
    program_id: Optional[Any] = Field(alias=str("programId"), default=None)


class GroupEditInput(BaseModel):
    group_id: Optional[Any] = Field(alias=str("groupId"), default=None)
    program_id: Optional[Any] = Field(alias=str("programId"), default=None)


class ConfigurationRequestEditInput(BaseModel):
    program_id: Optional[Any] = Field(alias=str("programId"), default=None)


class DatasetEditInput(BaseModel):
    dataset_id: Optional[Any] = Field(alias=str("datasetId"), default=None)
    observation_id: Optional[Any] = Field(alias=str("observationId"), default=None)
    program_id: Optional[Any] = Field(alias=str("programId"), default=None)
    is_written: Optional[bool] = Field(alias=str("isWritten"), default=None)


class ObservationEditInput(BaseModel):
    observation_id: Optional[Any] = Field(alias=str("observationId"), default=None)
    program_id: Optional[Any] = Field(alias=str("programId"), default=None)


class ProgramEditInput(BaseModel):
    program_id: Optional[Any] = Field(alias=str("programId"), default=None)


class TargetEnvironmentInput(BaseModel):
    explicit_base: Optional["CoordinatesInput"] = Field(
        alias=str("explicitBase"), default=None
    )
    asterism: Optional[list[Any]] = None
    explicit_signal_to_noise_target_id: Optional[Any] = Field(
        alias=str("explicitSignalToNoiseTargetId"), default=None
    )
    use_blind_offset: Optional[bool] = Field(alias=str("useBlindOffset"), default=None)
    blind_offset_target: Optional["TargetPropertiesInput"] = Field(
        alias=str("blindOffsetTarget"), default=None
    )
    blind_offset_type: Optional[BlindOffsetType] = Field(
        alias=str("blindOffsetType"), default=None
    )


class TargetPropertiesInput(BaseModel):
    name: Optional[Any] = None
    sidereal: Optional["SiderealInput"] = None
    nonsidereal: Optional["NonsiderealInput"] = None
    opportunity: Optional["OpportunityInput"] = None
    source_profile: Optional["SourceProfileInput"] = Field(
        alias=str("sourceProfile"), default=None
    )
    existence: Optional[Existence] = None


class TelescopeConfigInput(BaseModel):
    offset: Optional["OffsetInput"] = None
    guiding: Optional[GuideState] = None


class TimingWindowRepeatInput(BaseModel):
    period: "TimeSpanInput"
    times: Optional[Any] = None


class TimingWindowEndInput(BaseModel):
    at_utc: Optional[Any] = Field(alias=str("atUtc"), default=None)
    after: Optional["TimeSpanInput"] = None
    repeat: Optional["TimingWindowRepeatInput"] = None


class TimingWindowInput(BaseModel):
    inclusion: TimingWindowInclusion
    start_utc: Any = Field(alias=str("startUtc"))
    end: Optional["TimingWindowEndInput"] = None


class UnnormalizedSedInput(BaseModel):
    stellar_library: Optional[StellarLibrarySpectrum] = Field(
        alias=str("stellarLibrary"), default=None
    )
    cool_star: Optional[CoolStarTemperature] = Field(
        alias=str("coolStar"), default=None
    )
    galaxy: Optional[GalaxySpectrum] = None
    planet: Optional[PlanetSpectrum] = None
    quasar: Optional[QuasarSpectrum] = None
    hii_region: Optional[HiiRegionSpectrum] = Field(
        alias=str("hiiRegion"), default=None
    )
    planetary_nebula: Optional[PlanetaryNebulaSpectrum] = Field(
        alias=str("planetaryNebula"), default=None
    )
    power_law: Optional[Any] = Field(alias=str("powerLaw"), default=None)
    black_body_temp_k: Optional[Any] = Field(alias=str("blackBodyTempK"), default=None)
    flux_densities: Optional[list["FluxDensity"]] = Field(
        alias=str("fluxDensities"), default=None
    )
    flux_densities_attachment: Optional[Any] = Field(
        alias=str("fluxDensitiesAttachment"), default=None
    )


class UpdateAsterismsInput(BaseModel):
    set_: "EditAsterismsPatchInput" = Field(alias=str("SET"))
    where: Optional["WhereObservation"] = Field(alias=str("WHERE"), default=None)
    limit: Optional[Any] = Field(alias=str("LIMIT"), default=None)
    include_deleted: Optional[bool] = Field(alias=str("includeDeleted"), default=False)


class UpdateAttachmentsInput(BaseModel):
    set_: "AttachmentPropertiesInput" = Field(alias=str("SET"))
    where: Optional["WhereAttachment"] = Field(alias=str("WHERE"), default=None)
    limit: Optional[Any] = Field(alias=str("LIMIT"), default=None)


class UpdateCallsForProposalsInput(BaseModel):
    set_: "CallForProposalsPropertiesInput" = Field(alias=str("SET"))
    where: Optional["WhereCallForProposals"] = Field(alias=str("WHERE"), default=None)
    limit: Optional[Any] = Field(alias=str("LIMIT"), default=None)
    include_deleted: Optional[bool] = Field(alias=str("includeDeleted"), default=False)


class UpdateDatasetsInput(BaseModel):
    set_: "DatasetPropertiesInput" = Field(alias=str("SET"))
    where: Optional["WhereDataset"] = Field(alias=str("WHERE"), default=None)
    limit: Optional[Any] = Field(alias=str("LIMIT"), default=None)


class UpdateGroupsInput(BaseModel):
    set_: "GroupPropertiesInput" = Field(alias=str("SET"))
    where: Optional["WhereGroup"] = Field(alias=str("WHERE"), default=None)
    limit: Optional[Any] = Field(alias=str("LIMIT"), default=None)


class UpdateObservationsInput(BaseModel):
    set_: "ObservationPropertiesInput" = Field(alias=str("SET"))
    where: Optional["WhereObservation"] = Field(alias=str("WHERE"), default=None)
    limit: Optional[Any] = Field(alias=str("LIMIT"), default=None)
    include_deleted: Optional[bool] = Field(alias=str("includeDeleted"), default=False)


class UpdateConfigurationRequestsInput(BaseModel):
    set_: "ConfigurationRequestProperties" = Field(alias=str("SET"))
    where: Optional["WhereConfigurationRequest"] = Field(
        alias=str("WHERE"), default=None
    )
    limit: Optional[Any] = Field(alias=str("LIMIT"), default=None)


class UpdateObservationsTimesInput(BaseModel):
    set_: "ObservationTimesInput" = Field(alias=str("SET"))
    where: Optional["WhereObservation"] = Field(alias=str("WHERE"), default=None)
    limit: Optional[Any] = Field(alias=str("LIMIT"), default=None)
    include_deleted: Optional[bool] = Field(alias=str("includeDeleted"), default=False)


class UpdateProgramUsersInput(BaseModel):
    set_: "ProgramUserPropertiesInput" = Field(alias=str("SET"))
    where: Optional["WhereProgramUser"] = Field(alias=str("WHERE"), default=None)
    limit: Optional[Any] = Field(alias=str("LIMIT"), default=None)


class UpdateProgramNotesInput(BaseModel):
    set_: "ProgramNotePropertiesInput" = Field(alias=str("SET"))
    where: Optional["WhereProgramNote"] = Field(alias=str("WHERE"), default=None)
    limit: Optional[Any] = Field(alias=str("LIMIT"), default=None)
    include_deleted: Optional[bool] = Field(alias=str("includeDeleted"), default=False)


class UpdateProgramsInput(BaseModel):
    set_: "ProgramPropertiesInput" = Field(alias=str("SET"))
    where: Optional["WhereProgram"] = Field(alias=str("WHERE"), default=None)
    limit: Optional[Any] = Field(alias=str("LIMIT"), default=None)
    include_deleted: Optional[bool] = Field(alias=str("includeDeleted"), default=False)


class UpdateProposalInput(BaseModel):
    program_id: Optional[Any] = Field(alias=str("programId"), default=None)
    proposal_reference: Optional[Any] = Field(
        alias=str("proposalReference"), default=None
    )
    program_reference: Optional[Any] = Field(
        alias=str("programReference"), default=None
    )
    set_: "ProposalPropertiesInput" = Field(alias=str("SET"))


class UpdateTargetsInput(BaseModel):
    set_: "TargetPropertiesInput" = Field(alias=str("SET"))
    where: Optional["WhereTarget"] = Field(alias=str("WHERE"), default=None)
    limit: Optional[Any] = Field(alias=str("LIMIT"), default=None)
    include_deleted: Optional[bool] = Field(alias=str("includeDeleted"), default=False)


class WavelengthInput(BaseModel):
    picometers: Optional[Any] = None
    angstroms: Optional[Any] = None
    nanometers: Optional[Any] = None
    micrometers: Optional[Any] = None


class WavelengthDitherInput(BaseModel):
    picometers: Optional[int] = None
    angstroms: Optional[Any] = None
    nanometers: Optional[Any] = None
    micrometers: Optional[Any] = None


class AttachmentPropertiesInput(BaseModel):
    description: Optional[Any] = None
    checked: Optional[bool] = None


class WhereDatasetChronicleEntry(BaseModel):
    and_: Optional[list["WhereDatasetChronicleEntry"]] = Field(
        alias=str("AND"), default=None
    )
    or_: Optional[list["WhereDatasetChronicleEntry"]] = Field(
        alias=str("OR"), default=None
    )
    not_: Optional["WhereDatasetChronicleEntry"] = Field(alias=str("NOT"), default=None)
    id: Optional["WhereOrderChronicleId"] = None
    user: Optional["WhereUser"] = None
    operation: Optional["WhereEqDatabaseOperation"] = None
    timestamp: Optional["WhereOrderTimestamp"] = None
    dataset: Optional["WhereOrderDatasetId"] = None
    program: Optional["WhereProgram"] = None
    mod_dataset_id: Optional["WhereBoolean"] = Field(
        alias=str("modDatasetId"), default=None
    )
    mod_step_id: Optional["WhereBoolean"] = Field(alias=str("modStepId"), default=None)
    mod_observation_id: Optional["WhereBoolean"] = Field(
        alias=str("modObservationId"), default=None
    )
    mod_visit_id: Optional["WhereBoolean"] = Field(
        alias=str("modVisitId"), default=None
    )
    mod_reference: Optional["WhereBoolean"] = Field(
        alias=str("modReference"), default=None
    )
    mod_filename: Optional["WhereBoolean"] = Field(
        alias=str("modFilename"), default=None
    )
    mod_qa_state: Optional["WhereBoolean"] = Field(
        alias=str("modQaState"), default=None
    )
    mod_interval: Optional["WhereBoolean"] = Field(
        alias=str("modInterval"), default=None
    )
    mod_comment: Optional["WhereBoolean"] = Field(alias=str("modComment"), default=None)


class Flamingos2StaticInput(BaseModel):
    mos_pre_imaging: Optional[MosPreImaging] = Field(
        alias=str("mosPreImaging"), default=None
    )
    use_electronic_offsetting: Optional[bool] = Field(
        alias=str("useElectronicOffsetting"), default=None
    )


class RecordFlamingos2VisitInput(BaseModel):
    observation_id: Any = Field(alias=str("observationId"))
    flamingos_2: "Flamingos2StaticInput" = Field(alias=str("flamingos2"))
    time: Optional[Any] = None
    idempotency_key: Optional[Any] = Field(alias=str("idempotencyKey"), default=None)


class Igrins2StaticInput(BaseModel):
    save_svc_images: Optional[bool] = Field(alias=str("saveSVCImages"), default=None)
    offset_mode: Optional[SlitOffsetMode] = Field(alias=str("offsetMode"), default=None)


class RecordIgrins2VisitInput(BaseModel):
    observation_id: Any = Field(alias=str("observationId"))
    igrins_2: "Igrins2StaticInput" = Field(alias=str("igrins2"))
    time: Optional[Any] = None
    idempotency_key: Optional[Any] = Field(alias=str("idempotencyKey"), default=None)


class Flamingos2DynamicInput(BaseModel):
    exposure: "TimeSpanInput"
    disperser: Optional[Flamingos2Disperser] = None
    filter_: Flamingos2Filter = Field(alias=str("filter"))
    read_mode: Flamingos2ReadMode = Field(alias=str("readMode"))
    lyot_wheel: Flamingos2LyotWheel = Field(alias=str("lyotWheel"))
    fpu: Optional["Flamingos2FpuMaskInput"] = None
    decker: Flamingos2Decker
    readout_mode: Flamingos2ReadoutMode = Field(alias=str("readoutMode"))
    reads: Flamingos2Reads


class Flamingos2FpuMaskInput(BaseModel):
    custom_mask: Optional["Flamingos2CustomMaskInput"] = Field(
        alias=str("customMask"), default=None
    )
    builtin: Optional[Flamingos2Fpu] = None


class Flamingos2CustomMaskInput(BaseModel):
    attachment_id: Optional[Any] = Field(alias=str("attachmentId"), default=None)
    slit_width: Flamingos2CustomSlitWidth = Field(alias=str("slitWidth"))


class TelluricTypeInput(BaseModel):
    tag: TelluricTag
    star_types: Optional[list[str]] = Field(alias=str("starTypes"), default=None)


class Flamingos2LongSlitAcquisitionInput(BaseModel):
    explicit_filter: Optional[Flamingos2Filter] = Field(
        alias=str("explicitFilter"), default=None
    )
    exposure_time_mode: Optional["ExposureTimeModeInput"] = Field(
        alias=str("exposureTimeMode"), default=None
    )


class Flamingos2LongSlitInput(BaseModel):
    disperser: Optional[Flamingos2Disperser] = None
    filter_: Optional[Flamingos2Filter] = Field(alias=str("filter"), default=None)
    fpu: Optional[Flamingos2Fpu] = None
    exposure_time_mode: Optional["ExposureTimeModeInput"] = Field(
        alias=str("exposureTimeMode"), default=None
    )
    explicit_read_mode: Optional[Flamingos2ReadMode] = Field(
        alias=str("explicitReadMode"), default=None
    )
    explicit_reads: Optional[Flamingos2Reads] = Field(
        alias=str("explicitReads"), default=None
    )
    explicit_decker: Optional[Flamingos2Decker] = Field(
        alias=str("explicitDecker"), default=None
    )
    explicit_readout_mode: Optional[Flamingos2ReadoutMode] = Field(
        alias=str("explicitReadoutMode"), default=None
    )
    explicit_telescope_configs: Optional["SlitTelescopeConfigsInput"] = Field(
        alias=str("explicitTelescopeConfigs"), default=None
    )
    telluric_type: Optional["TelluricTypeInput"] = Field(
        alias=str("telluricType"), default=None
    )
    acquisition: Optional["Flamingos2LongSlitAcquisitionInput"] = None


class Flamingos2ImagingFilterInput(BaseModel):
    filter_: Flamingos2Filter = Field(alias=str("filter"))
    exposure_time_mode: Optional["ExposureTimeModeInput"] = Field(
        alias=str("exposureTimeMode"), default=None
    )


class Flamingos2ImagingInput(BaseModel):
    variant: Optional["ImagingVariantInput"] = None
    filters: Optional[list["Flamingos2ImagingFilterInput"]] = None
    explicit_read_mode: Optional[Flamingos2ReadMode] = Field(
        alias=str("explicitReadMode"), default=None
    )
    explicit_reads: Optional[Flamingos2Reads] = Field(
        alias=str("explicitReads"), default=None
    )
    explicit_decker: Optional[Flamingos2Decker] = Field(
        alias=str("explicitDecker"), default=None
    )
    explicit_readout_mode: Optional[Flamingos2ReadoutMode] = Field(
        alias=str("explicitReadoutMode"), default=None
    )


class GhostDetectorConfigInput(BaseModel):
    exposure_time_mode: Optional["ExposureTimeModeInput"] = Field(
        alias=str("exposureTimeMode"), default=None
    )
    explicit_binning: Optional[GhostBinning] = Field(
        alias=str("explicitBinning"), default=None
    )
    explicit_read_mode: Optional[GhostReadMode] = Field(
        alias=str("explicitReadMode"), default=None
    )


class GhostIfuInput(BaseModel):
    step_count: Optional[Any] = Field(alias=str("stepCount"), default=None)
    resolution_mode: Optional[GhostResolutionMode] = Field(
        alias=str("resolutionMode"), default=None
    )
    red: Optional["GhostDetectorConfigInput"] = None
    blue: Optional["GhostDetectorConfigInput"] = None
    sky_position: Optional["CoordinatesInput"] = Field(
        alias=str("skyPosition"), default=None
    )
    slit_viewing_camera_exposure_time: Optional["TimeSpanInput"] = Field(
        alias=str("slitViewingCameraExposureTime"), default=None
    )
    explicit_ifu_1_agitator: Optional[GhostIfu1FiberAgitator] = Field(
        alias=str("explicitIfu1Agitator"), default=None
    )
    explicit_ifu_2_agitator: Optional[GhostIfu2FiberAgitator] = Field(
        alias=str("explicitIfu2Agitator"), default=None
    )


class Igrins2LongSlitInput(BaseModel):
    exposure_time_mode: Optional["ExposureTimeModeInput"] = Field(
        alias=str("exposureTimeMode"), default=None
    )
    svc: Optional["Igrins2SvcInput"] = None
    explicit_telescope_configs: Optional["SlitTelescopeConfigsInput"] = Field(
        alias=str("explicitTelescopeConfigs"), default=None
    )
    telluric_type: Optional["TelluricTypeInput"] = Field(
        alias=str("telluricType"), default=None
    )


class Igrins2SvcInput(BaseModel):
    explicit_exposure: Optional["TimeSpanInput"] = Field(
        alias=str("explicitExposure"), default=None
    )
    explicit_telescope_configs: Optional[list["TelescopeConfigInput"]] = Field(
        alias=str("explicitTelescopeConfigs"), default=None
    )


class GnirsImagingFilterInput(BaseModel):
    filter_: GnirsFilter = Field(alias=str("filter"))
    exposure_time_mode: Optional["ExposureTimeModeInput"] = Field(
        alias=str("exposureTimeMode"), default=None
    )


class GnirsImagingAcquisitionInput(BaseModel):
    explicit_filter: Optional[GnirsFilter] = Field(
        alias=str("explicitFilter"), default=None
    )
    explicit_acquisition_type: Optional[GnirsAcquisitionType] = Field(
        alias=str("explicitAcquisitionType"), default=None
    )
    coadds: Optional[Any] = None
    sky_offset: Optional["OffsetInput"] = Field(alias=str("skyOffset"), default=None)
    exposure_time_mode: Optional["ExposureTimeModeInput"] = Field(
        alias=str("exposureTimeMode"), default=None
    )


class GnirsImagingInput(BaseModel):
    variant: Optional["ImagingVariantInput"] = None
    filters: Optional[list["GnirsImagingFilterInput"]] = None
    camera: Optional[GnirsCamera] = None
    coadds: Optional[Any] = None
    explicit_read_mode: Optional[GnirsReadMode] = Field(
        alias=str("explicitReadMode"), default=None
    )
    explicit_well_depth: Optional[GnirsWellDepth] = Field(
        alias=str("explicitWellDepth"), default=None
    )
    acquisition: Optional["GnirsImagingAcquisitionInput"] = None


class GnirsCentralWavelengthConfigInput(BaseModel):
    central_wavelength: "WavelengthInput" = Field(alias=str("centralWavelength"))
    exposure_time_mode: Optional["ExposureTimeModeInput"] = Field(
        alias=str("exposureTimeMode"), default=None
    )
    coadds: Optional[Any] = None


class GnirsSpectroscopyAcquisitionInput(BaseModel):
    explicit_filter: Optional[GnirsFilter] = Field(
        alias=str("explicitFilter"), default=None
    )
    explicit_acquisition_type: Optional[GnirsAcquisitionType] = Field(
        alias=str("explicitAcquisitionType"), default=None
    )
    coadds: Optional[Any] = None
    sky_offset: Optional["OffsetInput"] = Field(alias=str("skyOffset"), default=None)
    exposure_time_mode: Optional["ExposureTimeModeInput"] = Field(
        alias=str("exposureTimeMode"), default=None
    )


class TelescopeConfigAlongSlitInput(BaseModel):
    q: "OffsetComponentInput"
    guiding: GuideState


class SlitTelescopeConfigsInput(BaseModel):
    along_slit: Optional[list["TelescopeConfigAlongSlitInput"]] = Field(
        alias=str("alongSlit"), default=None
    )
    to_sky: Optional[list["TelescopeConfigInput"]] = Field(
        alias=str("toSky"), default=None
    )


class GnirsSlitInput(BaseModel):
    fpu: Optional[GnirsFpuSlit] = None
    explicit_telescope_configs: Optional["SlitTelescopeConfigsInput"] = Field(
        alias=str("explicitTelescopeConfigs"), default=None
    )


class GnirsIfuInput(BaseModel):
    fpu: Optional[GnirsFpuIfu] = None
    telescope_configs: Optional[list["TelescopeConfigInput"]] = Field(
        alias=str("telescopeConfigs"), default=None
    )


class GnirsSpectroscopyInput(BaseModel):
    central_wavelengths: Optional[list["GnirsCentralWavelengthConfigInput"]] = Field(
        alias=str("centralWavelengths"), default=None
    )
    filter_: Optional[GnirsFilter] = Field(alias=str("filter"), default=None)
    slit: Optional["GnirsSlitInput"] = None
    ifu: Optional["GnirsIfuInput"] = None
    camera: Optional[GnirsCamera] = None
    grating: Optional[GnirsGrating] = None
    prism: Optional[GnirsPrism] = None
    explicit_decker: Optional[GnirsDecker] = Field(
        alias=str("explicitDecker"), default=None
    )
    explicit_grating: Optional[GnirsGrating] = Field(
        alias=str("explicitGrating"), default=None
    )
    explicit_prism: Optional[GnirsPrism] = Field(
        alias=str("explicitPrism"), default=None
    )
    explicit_focus_motor_steps: Optional[int] = Field(
        alias=str("explicitFocusMotorSteps"), default=None
    )
    explicit_read_mode: Optional[GnirsReadMode] = Field(
        alias=str("explicitReadMode"), default=None
    )
    explicit_well_depth: Optional[GnirsWellDepth] = Field(
        alias=str("explicitWellDepth"), default=None
    )
    acquisition: Optional["GnirsSpectroscopyAcquisitionInput"] = None
    telluric_type: Optional["TelluricTypeInput"] = Field(
        alias=str("telluricType"), default=None
    )


class ImagingVariantInput(BaseModel):
    grouped: Optional["GroupedImagingVariantInput"] = None
    interleaved: Optional["InterleavedImagingVariantInput"] = None
    pre_imaging: Optional["PreImagingVariantInput"] = Field(
        alias=str("preImaging"), default=None
    )


class GroupedImagingVariantInput(BaseModel):
    order: Optional[WavelengthOrder] = None
    offsets: Optional["TelescopeConfigGeneratorInput"] = None
    sky_count: Optional[Any] = Field(alias=str("skyCount"), default=None)
    sky_offsets: Optional["TelescopeConfigGeneratorInput"] = Field(
        alias=str("skyOffsets"), default=None
    )


class InterleavedImagingVariantInput(BaseModel):
    offsets: Optional["TelescopeConfigGeneratorInput"] = None
    sky_count: Optional[Any] = Field(alias=str("skyCount"), default=None)
    sky_offsets: Optional["TelescopeConfigGeneratorInput"] = Field(
        alias=str("skyOffsets"), default=None
    )


class PreImagingVariantInput(BaseModel):
    offset_1: Optional["OffsetInput"] = Field(alias=str("offset1"), default=None)
    offset_2: Optional["OffsetInput"] = Field(alias=str("offset2"), default=None)
    offset_3: Optional["OffsetInput"] = Field(alias=str("offset3"), default=None)
    offset_4: Optional["OffsetInput"] = Field(alias=str("offset4"), default=None)


class GmosNorthImagingFilterInput(BaseModel):
    filter_: GmosNorthFilter = Field(alias=str("filter"))
    exposure_time_mode: Optional["ExposureTimeModeInput"] = Field(
        alias=str("exposureTimeMode"), default=None
    )


class GoaPropertiesInput(BaseModel):
    proprietary_months: Optional[Any] = Field(
        alias=str("proprietaryMonths"), default=None
    )
    should_notify: Optional[bool] = Field(alias=str("shouldNotify"), default=None)
    private_header: Optional[bool] = Field(alias=str("privateHeader"), default=None)


class GroupElementInput(BaseModel):
    group_id: Optional[Any] = Field(alias=str("groupId"), default=None)
    observation_id: Optional[Any] = Field(alias=str("observationId"), default=None)


class GroupPropertiesInput(BaseModel):
    name: Optional[Any] = None
    description: Optional[Any] = None
    minimum_required: Optional[Any] = Field(alias=str("minimumRequired"), default=None)
    ordered: Optional[bool] = None
    minimum_interval: Optional["TimeSpanInput"] = Field(
        alias=str("minimumInterval"), default=None
    )
    maximum_interval: Optional["TimeSpanInput"] = Field(
        alias=str("maximumInterval"), default=None
    )
    same_night: Optional[bool] = Field(alias=str("sameNight"), default=None)
    parent_group: Optional[Any] = Field(alias=str("parentGroup"), default=None)
    parent_group_index: Optional[Any] = Field(
        alias=str("parentGroupIndex"), default=None
    )
    existence: Optional[Existence] = None


class CreateGroupInput(BaseModel):
    program_id: Optional[Any] = Field(alias=str("programId"), default=None)
    proposal_reference: Optional[Any] = Field(
        alias=str("proposalReference"), default=None
    )
    program_reference: Optional[Any] = Field(
        alias=str("programReference"), default=None
    )
    set_: Optional["GroupPropertiesInput"] = Field(alias=str("SET"), default=None)
    initial_contents: Optional[list[Optional["GroupElementInput"]]] = Field(
        alias=str("initialContents"), default=None
    )


class ImagingScienceRequirementsInput(BaseModel):
    minimum_fov: Optional["AngleInput"] = Field(alias=str("minimumFov"), default=None)
    narrow_filters: Optional[bool] = Field(alias=str("narrowFilters"), default=None)
    broad_filters: Optional[bool] = Field(alias=str("broadFilters"), default=None)
    combined_filters: Optional[bool] = Field(alias=str("combinedFilters"), default=None)


class TooTriggerEditInput(BaseModel):
    program_id: Optional[Any] = Field(alias=str("programId"), default=None)
    observation_id: Optional[Any] = Field(alias=str("observationId"), default=None)
    too_trigger_id: Optional[Any] = Field(alias=str("tooTriggerId"), default=None)


class DeclineTooTriggerInput(BaseModel):
    too_trigger_id: Any = Field(alias=str("tooTriggerId"))
    reason: Optional[Any] = None


class WhereOrderTooTriggerId(BaseModel):
    eq: Optional[Any] = Field(alias=str("EQ"), default=None)
    neq: Optional[Any] = Field(alias=str("NEQ"), default=None)
    in_: Optional[list[Any]] = Field(alias=str("IN"), default=None)
    nin: Optional[list[Any]] = Field(alias=str("NIN"), default=None)
    gt: Optional[Any] = Field(alias=str("GT"), default=None)
    lt: Optional[Any] = Field(alias=str("LT"), default=None)
    gte: Optional[Any] = Field(alias=str("GTE"), default=None)
    lte: Optional[Any] = Field(alias=str("LTE"), default=None)


class WhereOrderTooTriggerStatus(BaseModel):
    eq: Optional[TooTriggerStatus] = Field(alias=str("EQ"), default=None)
    neq: Optional[TooTriggerStatus] = Field(alias=str("NEQ"), default=None)
    in_: Optional[list[TooTriggerStatus]] = Field(alias=str("IN"), default=None)
    nin: Optional[list[TooTriggerStatus]] = Field(alias=str("NIN"), default=None)
    gt: Optional[TooTriggerStatus] = Field(alias=str("GT"), default=None)
    lt: Optional[TooTriggerStatus] = Field(alias=str("LT"), default=None)
    gte: Optional[TooTriggerStatus] = Field(alias=str("GTE"), default=None)
    lte: Optional[TooTriggerStatus] = Field(alias=str("LTE"), default=None)


class WhereTooTrigger(BaseModel):
    and_: Optional[list["WhereTooTrigger"]] = Field(alias=str("AND"), default=None)
    or_: Optional[list["WhereTooTrigger"]] = Field(alias=str("OR"), default=None)
    not_: Optional["WhereTooTrigger"] = Field(alias=str("NOT"), default=None)
    id: Optional["WhereOrderTooTriggerId"] = None
    observation_id: Optional["WhereOrderObservationId"] = Field(
        alias=str("observationId"), default=None
    )
    program_id: Optional["WhereOrderProgramId"] = Field(
        alias=str("programId"), default=None
    )
    status: Optional["WhereOrderTooTriggerStatus"] = None
    requested_at: Optional["WhereOrderTimestamp"] = Field(
        alias=str("requestedAt"), default=None
    )
    requested_by: Optional["WhereUser"] = Field(alias=str("requestedBy"), default=None)
    updated_at: Optional["WhereOrderTimestamp"] = Field(
        alias=str("updatedAt"), default=None
    )


class WhereTooTriggerChronicleEntry(BaseModel):
    and_: Optional[list["WhereTooTriggerChronicleEntry"]] = Field(
        alias=str("AND"), default=None
    )
    or_: Optional[list["WhereTooTriggerChronicleEntry"]] = Field(
        alias=str("OR"), default=None
    )
    not_: Optional["WhereTooTriggerChronicleEntry"] = Field(
        alias=str("NOT"), default=None
    )
    id: Optional["WhereOrderChronicleId"] = None
    user: Optional["WhereUser"] = None
    operation: Optional["WhereEqDatabaseOperation"] = None
    timestamp: Optional["WhereOrderTimestamp"] = None
    too_trigger: Optional["WhereOrderTooTriggerId"] = Field(
        alias=str("tooTrigger"), default=None
    )
    mod_observation_id: Optional["WhereBoolean"] = Field(
        alias=str("modObservationId"), default=None
    )
    mod_program_id: Optional["WhereBoolean"] = Field(
        alias=str("modProgramId"), default=None
    )
    mod_status: Optional["WhereBoolean"] = Field(alias=str("modStatus"), default=None)
    mod_resolution_reason: Optional["WhereBoolean"] = Field(
        alias=str("modResolutionReason"), default=None
    )


class CreateConfigurationRequestInput(BaseModel):
    observation_id: Optional[Any] = Field(alias=str("observationId"), default=None)
    set_: Optional["ConfigurationRequestProperties"] = Field(
        alias=str("SET"), default=None
    )


class TimeChargeCorrectionInput(BaseModel):
    charge_class: ChargeClass = Field(alias=str("chargeClass"))
    op: TimeChargeCorrectionOp
    amount: "TimeSpanInput"
    comment: Optional[str] = None


class TimeSpanInput(BaseModel):
    microseconds: Optional[Any] = None
    milliseconds: Optional[Any] = None
    seconds: Optional[Any] = None
    minutes: Optional[Any] = None
    hours: Optional[Any] = None
    iso: Optional[str] = None


class UnlinkUserInput(BaseModel):
    program_user_id: Any = Field(alias=str("programUserId"))


class UserProfileInput(BaseModel):
    given_name: Optional[str] = Field(alias=str("givenName"), default=None)
    family_name: Optional[str] = Field(alias=str("familyName"), default=None)
    credit_name: Optional[str] = Field(alias=str("creditName"), default=None)
    email: Optional[str] = None


class WhereAngle(BaseModel):
    and_: Optional[list["WhereAngle"]] = Field(alias=str("AND"), default=None)
    or_: Optional[list["WhereAngle"]] = Field(alias=str("OR"), default=None)
    not_: Optional["WhereAngle"] = Field(alias=str("NOT"), default=None)
    microarcseconds: Optional["WhereOrderLong"] = None
    microseconds: Optional["WhereOrderBigDecimal"] = None
    milliarcseconds: Optional["WhereOrderBigDecimal"] = None
    milliseconds: Optional["WhereOrderBigDecimal"] = None
    arcseconds: Optional["WhereOrderBigDecimal"] = None
    seconds: Optional["WhereOrderBigDecimal"] = None
    arcminutes: Optional["WhereOrderBigDecimal"] = None
    minutes: Optional["WhereOrderBigDecimal"] = None
    degrees: Optional["WhereOrderBigDecimal"] = None
    hours: Optional["WhereOrderBigDecimal"] = None


class WhereBoolean(BaseModel):
    eq: Optional[bool] = Field(alias=str("EQ"), default=None)


class WhereOptionBoolean(BaseModel):
    is_null: Optional[bool] = Field(alias=str("IS_NULL"), default=None)
    eq: Optional[bool] = Field(alias=str("EQ"), default=None)


class WhereCallForProposals(BaseModel):
    and_: Optional[list["WhereCallForProposals"]] = Field(
        alias=str("AND"), default=None
    )
    or_: Optional[list["WhereCallForProposals"]] = Field(alias=str("OR"), default=None)
    not_: Optional["WhereCallForProposals"] = Field(alias=str("NOT"), default=None)
    id: Optional["WhereOrderCallForProposalsId"] = None
    semester: Optional["WhereOrderSemester"] = None
    active_start: Optional["WhereOrderDate"] = Field(
        alias=str("activeStart"), default=None
    )
    active_end: Optional["WhereOrderDate"] = Field(alias=str("activeEnd"), default=None)
    is_open: Optional["WhereBoolean"] = Field(alias=str("isOpen"), default=None)
    observatory: Optional["WhereObservatoryEq"] = None
    gemini: Optional["WhereGeminiCallProperties"] = None


class WhereObservatoryEq(BaseModel):
    eq: Optional[Observatory] = Field(alias=str("EQ"), default=None)
    neq: Optional[Observatory] = Field(alias=str("NEQ"), default=None)
    in_: Optional[list[Observatory]] = Field(alias=str("IN"), default=None)
    nin: Optional[list[Observatory]] = Field(alias=str("NIN"), default=None)


class WhereGeminiCallProperties(BaseModel):
    type_: Optional["WhereEqGeminiCallForProposalsType"] = Field(
        alias=str("type"), default=None
    )
    allows_non_partner_pi: Optional["WhereBoolean"] = Field(
        alias=str("allowsNonPartnerPi"), default=None
    )


class WhereAttachment(BaseModel):
    and_: Optional[list["WhereAttachment"]] = Field(alias=str("AND"), default=None)
    or_: Optional[list["WhereAttachment"]] = Field(alias=str("OR"), default=None)
    not_: Optional["WhereAttachment"] = Field(alias=str("NOT"), default=None)
    id: Optional["WhereOrderAttachmentId"] = None
    file_name: Optional["WhereString"] = Field(alias=str("fileName"), default=None)
    mask_name: Optional["WhereOptionString"] = Field(
        alias=str("maskName"), default=None
    )
    description: Optional["WhereOptionString"] = None
    attachment_type: Optional["WhereAttachmentType"] = Field(
        alias=str("attachmentType"), default=None
    )
    checked: Optional[bool] = None
    program: Optional["WhereProgram"] = None


class WhereAttachmentType(BaseModel):
    eq: Optional[AttachmentType] = Field(alias=str("EQ"), default=None)
    neq: Optional[AttachmentType] = Field(alias=str("NEQ"), default=None)
    in_: Optional[list[AttachmentType]] = Field(alias=str("IN"), default=None)
    nin: Optional[list[AttachmentType]] = Field(alias=str("NIN"), default=None)


class WhereOrderAttachmentId(BaseModel):
    eq: Optional[Any] = Field(alias=str("EQ"), default=None)
    neq: Optional[Any] = Field(alias=str("NEQ"), default=None)
    in_: Optional[list[Any]] = Field(alias=str("IN"), default=None)
    nin: Optional[list[Any]] = Field(alias=str("NIN"), default=None)
    gt: Optional[Any] = Field(alias=str("GT"), default=None)
    lt: Optional[Any] = Field(alias=str("LT"), default=None)
    gte: Optional[Any] = Field(alias=str("GTE"), default=None)
    lte: Optional[Any] = Field(alias=str("LTE"), default=None)


class WhereDataset(BaseModel):
    and_: Optional[list["WhereDataset"]] = Field(alias=str("AND"), default=None)
    or_: Optional[list["WhereDataset"]] = Field(alias=str("OR"), default=None)
    not_: Optional["WhereDataset"] = Field(alias=str("NOT"), default=None)
    id: Optional["WhereOrderDatasetId"] = None
    reference: Optional["WhereDatasetReference"] = None
    observation: Optional["WhereObservation"] = None
    program: Optional["WhereProgram"] = None
    step_id: Optional["WhereEqStepId"] = Field(alias=str("stepId"), default=None)
    index: Optional["WhereOrderPosInt"] = None
    filename: Optional["WhereString"] = None
    qa_state: Optional["WhereOptionEqQaState"] = Field(
        alias=str("qaState"), default=None
    )
    comment: Optional["WhereOptionString"] = None
    is_written: Optional["WhereBoolean"] = Field(alias=str("isWritten"), default=None)
    start: Optional["WhereOptionOrderTimestamp"] = None
    end: Optional["WhereOptionOrderTimestamp"] = None


class WhereDatasetReference(BaseModel):
    is_null: Optional[bool] = Field(alias=str("IS_NULL"), default=None)
    label: Optional["WhereString"] = None
    observation: Optional["WhereObservationReference"] = None
    step_index: Optional["WhereOrderPosInt"] = Field(
        alias=str("stepIndex"), default=None
    )
    exposure_index: Optional["WhereOrderPosInt"] = Field(
        alias=str("exposureIndex"), default=None
    )


class WhereEqGeminiCallForProposalsType(BaseModel):
    eq: Optional[GeminiCallForProposalsType] = Field(alias=str("EQ"), default=None)
    neq: Optional[GeminiCallForProposalsType] = Field(alias=str("NEQ"), default=None)
    in_: Optional[list[GeminiCallForProposalsType]] = Field(
        alias=str("IN"), default=None
    )
    nin: Optional[list[GeminiCallForProposalsType]] = Field(
        alias=str("NIN"), default=None
    )


class WhereEqDatabaseOperation(BaseModel):
    eq: Optional[DatabaseOperation] = Field(alias=str("EQ"), default=None)
    neq: Optional[DatabaseOperation] = Field(alias=str("NEQ"), default=None)
    in_: Optional[list[DatabaseOperation]] = Field(alias=str("IN"), default=None)
    nin: Optional[list[DatabaseOperation]] = Field(alias=str("NIN"), default=None)


class WhereOptionEqEducationalStatus(BaseModel):
    is_null: Optional[bool] = Field(alias=str("IS_NULL"), default=None)
    eq: Optional[EducationalStatus] = Field(alias=str("EQ"), default=None)
    neq: Optional[EducationalStatus] = Field(alias=str("NEQ"), default=None)
    in_: Optional[list[EducationalStatus]] = Field(alias=str("IN"), default=None)
    nin: Optional[list[EducationalStatus]] = Field(alias=str("NIN"), default=None)


class WhereEqExecutionEventType(BaseModel):
    eq: Optional[ExecutionEventType] = Field(alias=str("EQ"), default=None)
    neq: Optional[ExecutionEventType] = Field(alias=str("NEQ"), default=None)
    in_: Optional[list[ExecutionEventType]] = Field(alias=str("IN"), default=None)
    nin: Optional[list[ExecutionEventType]] = Field(alias=str("NIN"), default=None)


class WhereOptionEqGender(BaseModel):
    is_null: Optional[bool] = Field(alias=str("IS_NULL"), default=None)
    eq: Optional[Gender] = Field(alias=str("EQ"), default=None)
    neq: Optional[Gender] = Field(alias=str("NEQ"), default=None)
    in_: Optional[list[Gender]] = Field(alias=str("IN"), default=None)
    nin: Optional[list[Gender]] = Field(alias=str("NIN"), default=None)


class WhereOptionEqInstrument(BaseModel):
    is_null: Optional[bool] = Field(alias=str("IS_NULL"), default=None)
    eq: Optional[Instrument] = Field(alias=str("EQ"), default=None)
    neq: Optional[Instrument] = Field(alias=str("NEQ"), default=None)
    in_: Optional[list[Instrument]] = Field(alias=str("IN"), default=None)
    nin: Optional[list[Instrument]] = Field(alias=str("NIN"), default=None)


class WhereOptionEqObservingModeType(BaseModel):
    is_null: Optional[bool] = Field(alias=str("IS_NULL"), default=None)
    eq: Optional[ObservingModeType] = Field(alias=str("EQ"), default=None)
    neq: Optional[ObservingModeType] = Field(alias=str("NEQ"), default=None)
    in_: Optional[list[ObservingModeType]] = Field(alias=str("IN"), default=None)
    nin: Optional[list[ObservingModeType]] = Field(alias=str("NIN"), default=None)


class WhereEqPartner(BaseModel):
    eq: Optional[Partner] = Field(alias=str("EQ"), default=None)
    neq: Optional[Partner] = Field(alias=str("NEQ"), default=None)
    in_: Optional[list[Partner]] = Field(alias=str("IN"), default=None)
    nin: Optional[list[Partner]] = Field(alias=str("NIN"), default=None)


class WhereEqPartnerLinkType(BaseModel):
    eq: Optional[PartnerLinkType] = Field(alias=str("EQ"), default=None)
    neq: Optional[PartnerLinkType] = Field(alias=str("NEQ"), default=None)
    in_: Optional[list[PartnerLinkType]] = Field(alias=str("IN"), default=None)
    nin: Optional[list[PartnerLinkType]] = Field(alias=str("NIN"), default=None)


class WhereEqProgramUserRole(BaseModel):
    eq: Optional[ProgramUserRole] = Field(alias=str("EQ"), default=None)
    neq: Optional[ProgramUserRole] = Field(alias=str("NEQ"), default=None)
    in_: Optional[list[ProgramUserRole]] = Field(alias=str("IN"), default=None)
    nin: Optional[list[ProgramUserRole]] = Field(alias=str("NIN"), default=None)


class WhereEqProgramType(BaseModel):
    eq: Optional[ProgramType] = Field(alias=str("EQ"), default=None)
    neq: Optional[ProgramType] = Field(alias=str("NEQ"), default=None)
    in_: Optional[list[ProgramType]] = Field(alias=str("IN"), default=None)
    nin: Optional[list[ProgramType]] = Field(alias=str("NIN"), default=None)


class WhereEqProposalStatus(BaseModel):
    eq: Optional[ProposalStatus] = Field(alias=str("EQ"), default=None)
    neq: Optional[ProposalStatus] = Field(alias=str("NEQ"), default=None)
    in_: Optional[list[ProposalStatus]] = Field(alias=str("IN"), default=None)
    nin: Optional[list[ProposalStatus]] = Field(alias=str("NIN"), default=None)


class WhereEqSite(BaseModel):
    eq: Optional[Site] = Field(alias=str("EQ"), default=None)
    neq: Optional[Site] = Field(alias=str("NEQ"), default=None)
    in_: Optional[list[Site]] = Field(alias=str("IN"), default=None)
    nin: Optional[list[Site]] = Field(alias=str("NIN"), default=None)


class WhereOptionEqSite(BaseModel):
    is_null: Optional[bool] = Field(alias=str("IS_NULL"), default=None)
    eq: Optional[Site] = Field(alias=str("EQ"), default=None)
    neq: Optional[Site] = Field(alias=str("NEQ"), default=None)
    in_: Optional[list[Site]] = Field(alias=str("IN"), default=None)
    nin: Optional[list[Site]] = Field(alias=str("NIN"), default=None)


class WhereEqStepId(BaseModel):
    eq: Optional[Any] = Field(alias=str("EQ"), default=None)
    neq: Optional[Any] = Field(alias=str("NEQ"), default=None)
    in_: Optional[list[Any]] = Field(alias=str("IN"), default=None)
    nin: Optional[list[Any]] = Field(alias=str("NIN"), default=None)


class WhereEqTooActivation(BaseModel):
    eq: Optional[TooActivation] = Field(alias=str("EQ"), default=None)
    neq: Optional[TooActivation] = Field(alias=str("NEQ"), default=None)
    in_: Optional[list[TooActivation]] = Field(alias=str("IN"), default=None)
    nin: Optional[list[TooActivation]] = Field(alias=str("NIN"), default=None)


class WhereEqUserType(BaseModel):
    eq: Optional[UserType] = Field(alias=str("EQ"), default=None)
    neq: Optional[UserType] = Field(alias=str("NEQ"), default=None)
    in_: Optional[list[UserType]] = Field(alias=str("IN"), default=None)
    nin: Optional[list[UserType]] = Field(alias=str("NIN"), default=None)


class WhereEqVisitId(BaseModel):
    eq: Optional[Any] = Field(alias=str("EQ"), default=None)
    neq: Optional[Any] = Field(alias=str("NEQ"), default=None)
    in_: Optional[list[Any]] = Field(alias=str("IN"), default=None)
    nin: Optional[list[Any]] = Field(alias=str("NIN"), default=None)


class WhereExecutionEvent(BaseModel):
    and_: Optional[list["WhereExecutionEvent"]] = Field(alias=str("AND"), default=None)
    or_: Optional[list["WhereExecutionEvent"]] = Field(alias=str("OR"), default=None)
    not_: Optional["WhereExecutionEvent"] = Field(alias=str("NOT"), default=None)
    id: Optional["WhereOrderExecutionEventId"] = None
    visit_id: Optional["WhereEqVisitId"] = Field(alias=str("visitId"), default=None)
    observation: Optional["WhereObservation"] = None
    received: Optional["WhereOrderTimestamp"] = None
    event_type: Optional["WhereEqExecutionEventType"] = Field(
        alias=str("eventType"), default=None
    )
    slew_stage: Optional["WhereOrderSlewStage"] = Field(
        alias=str("slewStage"), default=None
    )
    sequence_command: Optional["WhereOrderSequenceCommand"] = Field(
        alias=str("sequenceCommand"), default=None
    )
    step_id: Optional["WhereEqStepId"] = Field(alias=str("stepId"), default=None)
    step_stage: Optional["WhereOrderStepStage"] = Field(
        alias=str("stepStage"), default=None
    )
    dataset_id: Optional["WhereOrderDatasetId"] = Field(
        alias=str("datasetId"), default=None
    )
    dataset_stage: Optional["WhereOrderDatasetStage"] = Field(
        alias=str("datasetStage"), default=None
    )


class WhereObservation(BaseModel):
    and_: Optional[list["WhereObservation"]] = Field(alias=str("AND"), default=None)
    or_: Optional[list["WhereObservation"]] = Field(alias=str("OR"), default=None)
    not_: Optional["WhereObservation"] = Field(alias=str("NOT"), default=None)
    id: Optional["WhereOrderObservationId"] = None
    reference: Optional["WhereObservationReference"] = None
    program: Optional["WhereProgram"] = None
    subtitle: Optional["WhereOptionString"] = None
    science_band: Optional["WhereOptionOrderScienceBand"] = Field(
        alias=str("scienceBand"), default=None
    )
    instrument: Optional["WhereOptionEqInstrument"] = None
    observing_mode_type: Optional["WhereOptionEqObservingModeType"] = Field(
        alias=str("observingModeType"), default=None
    )
    site: Optional["WhereOptionEqSite"] = None
    workflow: Optional["WhereCalculatedObservationWorkflow"] = None
    calibration_role: Optional["WhereOptionEqCalibrationRole"] = Field(
        alias=str("calibrationRole"), default=None
    )


class WhereConfigurationRequest(BaseModel):
    and_: Optional[list["WhereConfigurationRequest"]] = Field(
        alias=str("AND"), default=None
    )
    or_: Optional[list["WhereConfigurationRequest"]] = Field(
        alias=str("OR"), default=None
    )
    not_: Optional["WhereConfigurationRequest"] = Field(alias=str("NOT"), default=None)
    id: Optional["WhereOrderConfigurationRequestId"] = None
    program: Optional["WhereProgram"] = None
    status: Optional["WhereOrderConfigurationRequestStatus"] = None
    justification: Optional["WhereOptionString"] = None
    feedback: Optional["WhereOptionString"] = None
    created_at: Optional["WhereOrderTimestamp"] = Field(
        alias=str("createdAt"), default=None
    )
    updated_at: Optional["WhereOrderTimestamp"] = Field(
        alias=str("updatedAt"), default=None
    )


class WhereObservationReference(BaseModel):
    is_null: Optional[bool] = Field(alias=str("IS_NULL"), default=None)
    label: Optional["WhereString"] = None
    program: Optional["WhereProgramReference"] = None
    index: Optional["WhereOrderPosInt"] = None


class WhereGroup(BaseModel):
    and_: Optional[list["WhereGroup"]] = Field(alias=str("AND"), default=None)
    or_: Optional[list["WhereGroup"]] = Field(alias=str("OR"), default=None)
    not_: Optional["WhereGroup"] = Field(alias=str("NOT"), default=None)
    id: Optional["WhereOrderGroupId"] = None
    name: Optional["WhereOptionString"] = None
    description: Optional["WhereOptionString"] = None


class WhereOrderGroupId(BaseModel):
    eq: Optional[Any] = Field(alias=str("EQ"), default=None)
    neq: Optional[Any] = Field(alias=str("NEQ"), default=None)
    in_: Optional[list[Any]] = Field(alias=str("IN"), default=None)
    nin: Optional[list[Any]] = Field(alias=str("NIN"), default=None)
    gt: Optional[Any] = Field(alias=str("GT"), default=None)
    lt: Optional[Any] = Field(alias=str("LT"), default=None)
    gte: Optional[Any] = Field(alias=str("GTE"), default=None)
    lte: Optional[Any] = Field(alias=str("LTE"), default=None)


class WhereEqFocalPlane(BaseModel):
    eq: Optional[FocalPlane] = Field(alias=str("EQ"), default=None)
    neq: Optional[FocalPlane] = Field(alias=str("NEQ"), default=None)
    in_: Optional[list[FocalPlane]] = Field(alias=str("IN"), default=None)
    nin: Optional[list[FocalPlane]] = Field(alias=str("NIN"), default=None)


class WhereEqInstrument(BaseModel):
    eq: Optional[Instrument] = Field(alias=str("EQ"), default=None)
    neq: Optional[Instrument] = Field(alias=str("NEQ"), default=None)
    in_: Optional[list[Instrument]] = Field(alias=str("IN"), default=None)
    nin: Optional[list[Instrument]] = Field(alias=str("NIN"), default=None)


class WhereEqTargetDisposition(BaseModel):
    eq: Optional[TargetDisposition] = Field(alias=str("EQ"), default=None)
    neq: Optional[TargetDisposition] = Field(alias=str("NEQ"), default=None)
    in_: Optional[list[TargetDisposition]] = Field(alias=str("IN"), default=None)
    nin: Optional[list[TargetDisposition]] = Field(alias=str("NIN"), default=None)


class WhereOptionEqCalibrationRole(BaseModel):
    is_null: Optional[bool] = Field(alias=str("IS_NULL"), default=None)
    eq: Optional[CalibrationRole] = Field(alias=str("EQ"), default=None)
    neq: Optional[CalibrationRole] = Field(alias=str("NEQ"), default=None)
    in_: Optional[list[CalibrationRole]] = Field(alias=str("IN"), default=None)
    nin: Optional[list[CalibrationRole]] = Field(alias=str("NIN"), default=None)


class WhereOptionEqPartner(BaseModel):
    is_null: Optional[bool] = Field(alias=str("IS_NULL"), default=None)
    eq: Optional[Partner] = Field(alias=str("EQ"), default=None)
    neq: Optional[Partner] = Field(alias=str("NEQ"), default=None)
    in_: Optional[list[Partner]] = Field(alias=str("IN"), default=None)
    nin: Optional[list[Partner]] = Field(alias=str("NIN"), default=None)


class WhereOptionEqExchangePartner(BaseModel):
    is_null: Optional[bool] = Field(alias=str("IS_NULL"), default=None)
    eq: Optional[ExchangePartner] = Field(alias=str("EQ"), default=None)
    neq: Optional[ExchangePartner] = Field(alias=str("NEQ"), default=None)
    in_: Optional[list[ExchangePartner]] = Field(alias=str("IN"), default=None)
    nin: Optional[list[ExchangePartner]] = Field(alias=str("NIN"), default=None)


class WhereOptionEqQaState(BaseModel):
    is_null: Optional[bool] = Field(alias=str("IS_NULL"), default=None)
    eq: Optional[DatasetQaState] = Field(alias=str("EQ"), default=None)
    neq: Optional[DatasetQaState] = Field(alias=str("NEQ"), default=None)
    in_: Optional[list[DatasetQaState]] = Field(alias=str("IN"), default=None)
    nin: Optional[list[DatasetQaState]] = Field(alias=str("NIN"), default=None)


class WhereEqScienceSubtype(BaseModel):
    eq: Optional[ScienceSubtype] = Field(alias=str("EQ"), default=None)
    neq: Optional[ScienceSubtype] = Field(alias=str("NEQ"), default=None)
    in_: Optional[list[ScienceSubtype]] = Field(alias=str("IN"), default=None)
    nin: Optional[list[ScienceSubtype]] = Field(alias=str("NIN"), default=None)


class WhereOptionEqImagingCapability(BaseModel):
    is_null: Optional[bool] = Field(alias=str("IS_NULL"), default=None)
    eq: Optional[ImagingCapability] = Field(alias=str("EQ"), default=None)
    neq: Optional[ImagingCapability] = Field(alias=str("NEQ"), default=None)
    in_: Optional[list[ImagingCapability]] = Field(alias=str("IN"), default=None)
    nin: Optional[list[ImagingCapability]] = Field(alias=str("NIN"), default=None)


class WhereOptionEqSpectroscopyCapability(BaseModel):
    is_null: Optional[bool] = Field(alias=str("IS_NULL"), default=None)
    eq: Optional[SpectroscopyCapability] = Field(alias=str("EQ"), default=None)
    neq: Optional[SpectroscopyCapability] = Field(alias=str("NEQ"), default=None)
    in_: Optional[list[SpectroscopyCapability]] = Field(alias=str("IN"), default=None)
    nin: Optional[list[SpectroscopyCapability]] = Field(alias=str("NIN"), default=None)


class WhereOptionEqTacCategory(BaseModel):
    is_null: Optional[bool] = Field(alias=str("IS_NULL"), default=None)
    eq: Optional[TacCategory] = Field(alias=str("EQ"), default=None)
    neq: Optional[TacCategory] = Field(alias=str("NEQ"), default=None)
    in_: Optional[list[TacCategory]] = Field(alias=str("IN"), default=None)
    nin: Optional[list[TacCategory]] = Field(alias=str("NIN"), default=None)


class WhereOptionString(BaseModel):
    is_null: Optional[bool] = Field(alias=str("IS_NULL"), default=None)
    eq: Optional[Any] = Field(alias=str("EQ"), default=None)
    neq: Optional[Any] = Field(alias=str("NEQ"), default=None)
    in_: Optional[list[Any]] = Field(alias=str("IN"), default=None)
    nin: Optional[list[Any]] = Field(alias=str("NIN"), default=None)
    like: Optional[Any] = Field(alias=str("LIKE"), default=None)
    nlike: Optional[Any] = Field(alias=str("NLIKE"), default=None)
    match_case: Optional[bool] = Field(alias=str("MATCH_CASE"), default=True)


class WhereOrderBigDecimal(BaseModel):
    eq: Optional[Any] = Field(alias=str("EQ"), default=None)
    neq: Optional[Any] = Field(alias=str("NEQ"), default=None)
    in_: Optional[list[Any]] = Field(alias=str("IN"), default=None)
    nin: Optional[list[Any]] = Field(alias=str("NIN"), default=None)
    gt: Optional[Any] = Field(alias=str("GT"), default=None)
    lt: Optional[Any] = Field(alias=str("LT"), default=None)
    gte: Optional[Any] = Field(alias=str("GTE"), default=None)
    lte: Optional[Any] = Field(alias=str("LTE"), default=None)


class WhereOrderCallForProposalsId(BaseModel):
    eq: Optional[Any] = Field(alias=str("EQ"), default=None)
    neq: Optional[Any] = Field(alias=str("NEQ"), default=None)
    in_: Optional[list[Any]] = Field(alias=str("IN"), default=None)
    nin: Optional[list[Any]] = Field(alias=str("NIN"), default=None)
    gt: Optional[Any] = Field(alias=str("GT"), default=None)
    lt: Optional[Any] = Field(alias=str("LT"), default=None)
    gte: Optional[Any] = Field(alias=str("GTE"), default=None)
    lte: Optional[Any] = Field(alias=str("LTE"), default=None)


class WhereOrderChronicleId(BaseModel):
    eq: Optional[Any] = Field(alias=str("EQ"), default=None)
    neq: Optional[Any] = Field(alias=str("NEQ"), default=None)
    in_: Optional[list[Any]] = Field(alias=str("IN"), default=None)
    nin: Optional[list[Any]] = Field(alias=str("NIN"), default=None)
    gt: Optional[Any] = Field(alias=str("GT"), default=None)
    lt: Optional[Any] = Field(alias=str("LT"), default=None)
    gte: Optional[Any] = Field(alias=str("GTE"), default=None)
    lte: Optional[Any] = Field(alias=str("LTE"), default=None)


class WhereOrderDatasetId(BaseModel):
    eq: Optional[Any] = Field(alias=str("EQ"), default=None)
    neq: Optional[Any] = Field(alias=str("NEQ"), default=None)
    in_: Optional[list[Any]] = Field(alias=str("IN"), default=None)
    nin: Optional[list[Any]] = Field(alias=str("NIN"), default=None)
    gt: Optional[Any] = Field(alias=str("GT"), default=None)
    lt: Optional[Any] = Field(alias=str("LT"), default=None)
    gte: Optional[Any] = Field(alias=str("GTE"), default=None)
    lte: Optional[Any] = Field(alias=str("LTE"), default=None)


class WhereOrderDatasetStage(BaseModel):
    eq: Optional[DatasetStage] = Field(alias=str("EQ"), default=None)
    neq: Optional[DatasetStage] = Field(alias=str("NEQ"), default=None)
    in_: Optional[list[DatasetStage]] = Field(alias=str("IN"), default=None)
    nin: Optional[list[DatasetStage]] = Field(alias=str("NIN"), default=None)
    gt: Optional[DatasetStage] = Field(alias=str("GT"), default=None)
    lt: Optional[DatasetStage] = Field(alias=str("LT"), default=None)
    gte: Optional[DatasetStage] = Field(alias=str("GTE"), default=None)
    lte: Optional[DatasetStage] = Field(alias=str("LTE"), default=None)


class WhereOrderDate(BaseModel):
    eq: Optional[Any] = Field(alias=str("EQ"), default=None)
    neq: Optional[Any] = Field(alias=str("NEQ"), default=None)
    in_: Optional[list[Any]] = Field(alias=str("IN"), default=None)
    nin: Optional[list[Any]] = Field(alias=str("NIN"), default=None)
    gt: Optional[Any] = Field(alias=str("GT"), default=None)
    lt: Optional[Any] = Field(alias=str("LT"), default=None)
    gte: Optional[Any] = Field(alias=str("GTE"), default=None)
    lte: Optional[Any] = Field(alias=str("LTE"), default=None)


class WhereOrderExecutionEventId(BaseModel):
    eq: Optional[Any] = Field(alias=str("EQ"), default=None)
    neq: Optional[Any] = Field(alias=str("NEQ"), default=None)
    in_: Optional[list[Any]] = Field(alias=str("IN"), default=None)
    nin: Optional[list[Any]] = Field(alias=str("NIN"), default=None)
    gt: Optional[Any] = Field(alias=str("GT"), default=None)
    lt: Optional[Any] = Field(alias=str("LT"), default=None)
    gte: Optional[Any] = Field(alias=str("GTE"), default=None)
    lte: Optional[Any] = Field(alias=str("LTE"), default=None)


class WhereOrderTimestamp(BaseModel):
    eq: Optional[Any] = Field(alias=str("EQ"), default=None)
    neq: Optional[Any] = Field(alias=str("NEQ"), default=None)
    in_: Optional[list[Any]] = Field(alias=str("IN"), default=None)
    nin: Optional[list[Any]] = Field(alias=str("NIN"), default=None)
    gt: Optional[Any] = Field(alias=str("GT"), default=None)
    lt: Optional[Any] = Field(alias=str("LT"), default=None)
    gte: Optional[Any] = Field(alias=str("GTE"), default=None)
    lte: Optional[Any] = Field(alias=str("LTE"), default=None)


class WhereOptionOrderTimestamp(BaseModel):
    is_null: Optional[bool] = Field(alias=str("IS_NULL"), default=None)
    eq: Optional[Any] = Field(alias=str("EQ"), default=None)
    neq: Optional[Any] = Field(alias=str("NEQ"), default=None)
    in_: Optional[list[Any]] = Field(alias=str("IN"), default=None)
    nin: Optional[list[Any]] = Field(alias=str("NIN"), default=None)
    gt: Optional[Any] = Field(alias=str("GT"), default=None)
    lt: Optional[Any] = Field(alias=str("LT"), default=None)
    gte: Optional[Any] = Field(alias=str("GTE"), default=None)
    lte: Optional[Any] = Field(alias=str("LTE"), default=None)


class WhereOrderInt(BaseModel):
    eq: Optional[int] = Field(alias=str("EQ"), default=None)
    neq: Optional[int] = Field(alias=str("NEQ"), default=None)
    in_: Optional[list[int]] = Field(alias=str("IN"), default=None)
    nin: Optional[list[int]] = Field(alias=str("NIN"), default=None)
    gt: Optional[int] = Field(alias=str("GT"), default=None)
    lt: Optional[int] = Field(alias=str("LT"), default=None)
    gte: Optional[int] = Field(alias=str("GTE"), default=None)
    lte: Optional[int] = Field(alias=str("LTE"), default=None)


class WhereOrderLong(BaseModel):
    eq: Optional[Any] = Field(alias=str("EQ"), default=None)
    neq: Optional[Any] = Field(alias=str("NEQ"), default=None)
    in_: Optional[list[Any]] = Field(alias=str("IN"), default=None)
    nin: Optional[list[Any]] = Field(alias=str("NIN"), default=None)
    gt: Optional[Any] = Field(alias=str("GT"), default=None)
    lt: Optional[Any] = Field(alias=str("LT"), default=None)
    gte: Optional[Any] = Field(alias=str("GTE"), default=None)
    lte: Optional[Any] = Field(alias=str("LTE"), default=None)


class WhereOrderObservationId(BaseModel):
    eq: Optional[Any] = Field(alias=str("EQ"), default=None)
    neq: Optional[Any] = Field(alias=str("NEQ"), default=None)
    in_: Optional[list[Any]] = Field(alias=str("IN"), default=None)
    nin: Optional[list[Any]] = Field(alias=str("NIN"), default=None)
    gt: Optional[Any] = Field(alias=str("GT"), default=None)
    lt: Optional[Any] = Field(alias=str("LT"), default=None)
    gte: Optional[Any] = Field(alias=str("GTE"), default=None)
    lte: Optional[Any] = Field(alias=str("LTE"), default=None)


class WhereOrderConfigurationRequestId(BaseModel):
    eq: Optional[Any] = Field(alias=str("EQ"), default=None)
    neq: Optional[Any] = Field(alias=str("NEQ"), default=None)
    in_: Optional[list[Any]] = Field(alias=str("IN"), default=None)
    nin: Optional[list[Any]] = Field(alias=str("NIN"), default=None)
    gt: Optional[Any] = Field(alias=str("GT"), default=None)
    lt: Optional[Any] = Field(alias=str("LT"), default=None)
    gte: Optional[Any] = Field(alias=str("GTE"), default=None)
    lte: Optional[Any] = Field(alias=str("LTE"), default=None)


class WhereOrderConfigurationRequestStatus(BaseModel):
    eq: Optional[ConfigurationRequestStatus] = Field(alias=str("EQ"), default=None)
    neq: Optional[ConfigurationRequestStatus] = Field(alias=str("NEQ"), default=None)
    in_: Optional[list[ConfigurationRequestStatus]] = Field(
        alias=str("IN"), default=None
    )
    nin: Optional[list[ConfigurationRequestStatus]] = Field(
        alias=str("NIN"), default=None
    )
    gt: Optional[ConfigurationRequestStatus] = Field(alias=str("GT"), default=None)
    lt: Optional[ConfigurationRequestStatus] = Field(alias=str("LT"), default=None)
    gte: Optional[ConfigurationRequestStatus] = Field(alias=str("GTE"), default=None)
    lte: Optional[ConfigurationRequestStatus] = Field(alias=str("LTE"), default=None)


class WhereOrderPosBigDecimal(BaseModel):
    eq: Optional[Any] = Field(alias=str("EQ"), default=None)
    neq: Optional[Any] = Field(alias=str("NEQ"), default=None)
    in_: Optional[list[Any]] = Field(alias=str("IN"), default=None)
    nin: Optional[list[Any]] = Field(alias=str("NIN"), default=None)
    gt: Optional[Any] = Field(alias=str("GT"), default=None)
    lt: Optional[Any] = Field(alias=str("LT"), default=None)
    gte: Optional[Any] = Field(alias=str("GTE"), default=None)
    lte: Optional[Any] = Field(alias=str("LTE"), default=None)


class WhereOrderPosInt(BaseModel):
    eq: Optional[Any] = Field(alias=str("EQ"), default=None)
    neq: Optional[Any] = Field(alias=str("NEQ"), default=None)
    in_: Optional[list[Any]] = Field(alias=str("IN"), default=None)
    nin: Optional[list[Any]] = Field(alias=str("NIN"), default=None)
    gt: Optional[Any] = Field(alias=str("GT"), default=None)
    lt: Optional[Any] = Field(alias=str("LT"), default=None)
    gte: Optional[Any] = Field(alias=str("GTE"), default=None)
    lte: Optional[Any] = Field(alias=str("LTE"), default=None)


class WhereOrderProgramId(BaseModel):
    eq: Optional[Any] = Field(alias=str("EQ"), default=None)
    neq: Optional[Any] = Field(alias=str("NEQ"), default=None)
    in_: Optional[list[Any]] = Field(alias=str("IN"), default=None)
    nin: Optional[list[Any]] = Field(alias=str("NIN"), default=None)
    gt: Optional[Any] = Field(alias=str("GT"), default=None)
    lt: Optional[Any] = Field(alias=str("LT"), default=None)
    gte: Optional[Any] = Field(alias=str("GTE"), default=None)
    lte: Optional[Any] = Field(alias=str("LTE"), default=None)


class WhereOrderProgramNoteId(BaseModel):
    eq: Optional[Any] = Field(alias=str("EQ"), default=None)
    neq: Optional[Any] = Field(alias=str("NEQ"), default=None)
    in_: Optional[list[Any]] = Field(alias=str("IN"), default=None)
    nin: Optional[list[Any]] = Field(alias=str("NIN"), default=None)
    gt: Optional[Any] = Field(alias=str("GT"), default=None)
    lt: Optional[Any] = Field(alias=str("LT"), default=None)
    gte: Optional[Any] = Field(alias=str("GTE"), default=None)
    lte: Optional[Any] = Field(alias=str("LTE"), default=None)


class WhereOrderProgramUserId(BaseModel):
    eq: Optional[Any] = Field(alias=str("EQ"), default=None)
    neq: Optional[Any] = Field(alias=str("NEQ"), default=None)
    in_: Optional[list[Any]] = Field(alias=str("IN"), default=None)
    nin: Optional[list[Any]] = Field(alias=str("NIN"), default=None)
    gt: Optional[Any] = Field(alias=str("GT"), default=None)
    lt: Optional[Any] = Field(alias=str("LT"), default=None)
    gte: Optional[Any] = Field(alias=str("GTE"), default=None)
    lte: Optional[Any] = Field(alias=str("LTE"), default=None)


class WhereOrderUserId(BaseModel):
    eq: Optional[Any] = Field(alias=str("EQ"), default=None)
    neq: Optional[Any] = Field(alias=str("NEQ"), default=None)
    in_: Optional[list[Any]] = Field(alias=str("IN"), default=None)
    nin: Optional[list[Any]] = Field(alias=str("NIN"), default=None)
    gt: Optional[Any] = Field(alias=str("GT"), default=None)
    lt: Optional[Any] = Field(alias=str("LT"), default=None)
    gte: Optional[Any] = Field(alias=str("GTE"), default=None)
    lte: Optional[Any] = Field(alias=str("LTE"), default=None)


class WhereProposalReference(BaseModel):
    is_null: Optional[bool] = Field(alias=str("IS_NULL"), default=None)
    label: Optional["WhereString"] = None
    semester: Optional["WhereOrderSemester"] = None
    semester_index: Optional["WhereOrderPosInt"] = Field(
        alias=str("semesterIndex"), default=None
    )


class WhereOptionOrderScienceBand(BaseModel):
    is_null: Optional[bool] = Field(alias=str("IS_NULL"), default=None)
    eq: Optional[ScienceBand] = Field(alias=str("EQ"), default=None)
    neq: Optional[ScienceBand] = Field(alias=str("NEQ"), default=None)
    in_: Optional[list[ScienceBand]] = Field(alias=str("IN"), default=None)
    nin: Optional[list[ScienceBand]] = Field(alias=str("NIN"), default=None)
    gt: Optional[ScienceBand] = Field(alias=str("GT"), default=None)
    lt: Optional[ScienceBand] = Field(alias=str("LT"), default=None)
    gte: Optional[ScienceBand] = Field(alias=str("GTE"), default=None)
    lte: Optional[ScienceBand] = Field(alias=str("LTE"), default=None)


class WhereOrderSemester(BaseModel):
    eq: Optional[Any] = Field(alias=str("EQ"), default=None)
    neq: Optional[Any] = Field(alias=str("NEQ"), default=None)
    in_: Optional[list[Any]] = Field(alias=str("IN"), default=None)
    nin: Optional[list[Any]] = Field(alias=str("NIN"), default=None)
    gt: Optional[Any] = Field(alias=str("GT"), default=None)
    lt: Optional[Any] = Field(alias=str("LT"), default=None)
    gte: Optional[Any] = Field(alias=str("GTE"), default=None)
    lte: Optional[Any] = Field(alias=str("LTE"), default=None)


class WhereOrderSequenceCommand(BaseModel):
    eq: Optional[SequenceCommand] = Field(alias=str("EQ"), default=None)
    neq: Optional[SequenceCommand] = Field(alias=str("NEQ"), default=None)
    in_: Optional[list[SequenceCommand]] = Field(alias=str("IN"), default=None)
    nin: Optional[list[SequenceCommand]] = Field(alias=str("NIN"), default=None)
    gt: Optional[SequenceCommand] = Field(alias=str("GT"), default=None)
    lt: Optional[SequenceCommand] = Field(alias=str("LT"), default=None)
    gte: Optional[SequenceCommand] = Field(alias=str("GTE"), default=None)
    lte: Optional[SequenceCommand] = Field(alias=str("LTE"), default=None)


class WhereOrderSequenceType(BaseModel):
    eq: Optional[SequenceType] = Field(alias=str("EQ"), default=None)
    neq: Optional[SequenceType] = Field(alias=str("NEQ"), default=None)
    in_: Optional[list[SequenceType]] = Field(alias=str("IN"), default=None)
    nin: Optional[list[SequenceType]] = Field(alias=str("NIN"), default=None)
    gt: Optional[SequenceType] = Field(alias=str("GT"), default=None)
    lt: Optional[SequenceType] = Field(alias=str("LT"), default=None)
    gte: Optional[SequenceType] = Field(alias=str("GTE"), default=None)
    lte: Optional[SequenceType] = Field(alias=str("LTE"), default=None)


class WhereOrderSlewStage(BaseModel):
    eq: Optional[SlewStage] = Field(alias=str("EQ"), default=None)
    neq: Optional[SlewStage] = Field(alias=str("NEQ"), default=None)
    in_: Optional[list[SlewStage]] = Field(alias=str("IN"), default=None)
    nin: Optional[list[SlewStage]] = Field(alias=str("NIN"), default=None)
    gt: Optional[SlewStage] = Field(alias=str("GT"), default=None)
    lt: Optional[SlewStage] = Field(alias=str("LT"), default=None)
    gte: Optional[SlewStage] = Field(alias=str("GTE"), default=None)
    lte: Optional[SlewStage] = Field(alias=str("LTE"), default=None)


class WhereOrderStepStage(BaseModel):
    eq: Optional[StepStage] = Field(alias=str("EQ"), default=None)
    neq: Optional[StepStage] = Field(alias=str("NEQ"), default=None)
    in_: Optional[list[StepStage]] = Field(alias=str("IN"), default=None)
    nin: Optional[list[StepStage]] = Field(alias=str("NIN"), default=None)
    gt: Optional[StepStage] = Field(alias=str("GT"), default=None)
    lt: Optional[StepStage] = Field(alias=str("LT"), default=None)
    gte: Optional[StepStage] = Field(alias=str("GTE"), default=None)
    lte: Optional[StepStage] = Field(alias=str("LTE"), default=None)


class WhereOrderTargetId(BaseModel):
    eq: Optional[Any] = Field(alias=str("EQ"), default=None)
    neq: Optional[Any] = Field(alias=str("NEQ"), default=None)
    in_: Optional[list[Any]] = Field(alias=str("IN"), default=None)
    nin: Optional[list[Any]] = Field(alias=str("NIN"), default=None)
    gt: Optional[Any] = Field(alias=str("GT"), default=None)
    lt: Optional[Any] = Field(alias=str("LT"), default=None)
    gte: Optional[Any] = Field(alias=str("GTE"), default=None)
    lte: Optional[Any] = Field(alias=str("LTE"), default=None)


class WherePartnerLink(BaseModel):
    link_type: Optional["WhereEqPartnerLinkType"] = Field(
        alias=str("linkType"), default=None
    )
    gemini_partner: Optional["WhereOptionEqPartner"] = Field(
        alias=str("geminiPartner"), default=None
    )
    exchange_partner: Optional["WhereOptionEqExchangePartner"] = Field(
        alias=str("exchangePartner"), default=None
    )


class WhereProgram(BaseModel):
    and_: Optional[list["WhereProgram"]] = Field(alias=str("AND"), default=None)
    or_: Optional[list["WhereProgram"]] = Field(alias=str("OR"), default=None)
    not_: Optional["WhereProgram"] = Field(alias=str("NOT"), default=None)
    id: Optional["WhereOrderProgramId"] = None
    name: Optional["WhereOptionString"] = None
    type_: Optional["WhereEqProgramType"] = Field(alias=str("type"), default=None)
    reference: Optional["WhereProgramReference"] = None
    pi: Optional["WhereProgramUser"] = None
    proposal_status: Optional["WhereEqProposalStatus"] = Field(
        alias=str("proposalStatus"), default=None
    )
    proposal: Optional["WhereProposal"] = None
    calibration_role: Optional["WhereOptionEqCalibrationRole"] = Field(
        alias=str("calibrationRole"), default=None
    )
    active_start: Optional["WhereOrderDate"] = Field(
        alias=str("activeStart"), default=None
    )
    active_end: Optional["WhereOrderDate"] = Field(alias=str("activeEnd"), default=None)


class WhereProgramReference(BaseModel):
    is_null: Optional[bool] = Field(alias=str("IS_NULL"), default=None)
    label: Optional["WhereString"] = None
    semester: Optional["WhereOrderSemester"] = None
    semester_index: Optional["WhereOrderPosInt"] = Field(
        alias=str("semesterIndex"), default=None
    )
    instrument: Optional["WhereEqInstrument"] = None
    description: Optional["WhereString"] = None
    science_subtype: Optional["WhereEqScienceSubtype"] = Field(
        alias=str("scienceSubtype"), default=None
    )


class WhereProgramNote(BaseModel):
    and_: Optional[list["WhereProgramNote"]] = Field(alias=str("AND"), default=None)
    or_: Optional[list["WhereProgramNote"]] = Field(alias=str("OR"), default=None)
    not_: Optional["WhereProgramNote"] = Field(alias=str("NOT"), default=None)
    id: Optional["WhereOrderProgramNoteId"] = None
    program: Optional["WhereProgram"] = None
    title: Optional["WhereString"] = None
    text: Optional["WhereOptionString"] = None
    is_private: Optional["WhereBoolean"] = Field(alias=str("isPrivate"), default=None)


class WhereProgramUser(BaseModel):
    and_: Optional[list["WhereProgramUser"]] = Field(alias=str("AND"), default=None)
    or_: Optional[list["WhereProgramUser"]] = Field(alias=str("OR"), default=None)
    not_: Optional["WhereProgramUser"] = Field(alias=str("NOT"), default=None)
    id: Optional["WhereOrderProgramUserId"] = None
    program: Optional["WhereProgram"] = None
    user: Optional["WhereUser"] = None
    role: Optional["WhereEqProgramUserRole"] = None
    partner_link: Optional["WherePartnerLink"] = Field(
        alias=str("partnerLink"), default=None
    )
    preferred_profile: Optional["WhereUserProfile"] = Field(
        alias=str("preferredProfile"), default=None
    )
    educational_status: Optional["WhereOptionEqEducationalStatus"] = Field(
        alias=str("educationalStatus"), default=None
    )
    thesis: Optional["WhereOptionBoolean"] = None
    gender: Optional["WhereOptionEqGender"] = None
    has_data_access: Optional["WhereBoolean"] = Field(
        alias=str("hasDataAccess"), default=None
    )


class WhereProposal(BaseModel):
    is_null: Optional[bool] = Field(alias=str("IS_NULL"), default=None)
    and_: Optional[list["WhereProposal"]] = Field(alias=str("AND"), default=None)
    or_: Optional[list["WhereProposal"]] = Field(alias=str("OR"), default=None)
    not_: Optional["WhereProposal"] = Field(alias=str("NOT"), default=None)
    title: Optional["WhereOptionString"] = None
    reference: Optional["WhereProposalReference"] = None
    call: Optional["WhereCallForProposals"] = None


class WhereProposalPartnerEntry(BaseModel):
    and_: Optional[list["WhereProposalPartnerEntry"]] = Field(
        alias=str("AND"), default=None
    )
    or_: Optional[list["WhereProposalPartnerEntry"]] = Field(
        alias=str("OR"), default=None
    )
    not_: Optional["WhereProposalPartnerEntry"] = Field(alias=str("NOT"), default=None)
    partner: Optional["WhereEqPartner"] = None
    percent: Optional["WhereOrderInt"] = None


class WhereProposalPartners(BaseModel):
    match: Optional["WhereProposalPartnerEntry"] = Field(
        alias=str("MATCH"), default=None
    )
    eq: Optional[list[Partner]] = Field(alias=str("EQ"), default=None)
    is_joint: Optional[bool] = Field(alias=str("isJoint"), default=None)


class WhereSpectroscopyConfigOption(BaseModel):
    and_: Optional[list["WhereSpectroscopyConfigOption"]] = Field(
        alias=str("AND"), default=None
    )
    or_: Optional[list["WhereSpectroscopyConfigOption"]] = Field(
        alias=str("OR"), default=None
    )
    not_: Optional["WhereSpectroscopyConfigOption"] = Field(
        alias=str("NOT"), default=None
    )
    adaptive_optics: Optional["WhereBoolean"] = Field(
        alias=str("adaptiveOptics"), default=None
    )
    capability: Optional["WhereOptionEqSpectroscopyCapability"] = None
    focal_plane: Optional["WhereEqFocalPlane"] = Field(
        alias=str("focalPlane"), default=None
    )
    instrument: Optional["WhereEqInstrument"] = None
    resolution: Optional["WhereOrderPosInt"] = None
    site: Optional["WhereEqSite"] = None
    slit_length: Optional["WhereAngle"] = Field(alias=str("slitLength"), default=None)
    slit_width: Optional["WhereAngle"] = Field(alias=str("slitWidth"), default=None)
    range_includes: Optional["WavelengthInput"] = Field(
        alias=str("rangeIncludes"), default=None
    )
    wavelength_optimal: Optional["WhereWavelength"] = Field(
        alias=str("wavelengthOptimal"), default=None
    )
    wavelength_coverage: Optional["WhereWavelength"] = Field(
        alias=str("wavelengthCoverage"), default=None
    )


class WhereImagingConfigOption(BaseModel):
    and_: Optional[list["WhereImagingConfigOption"]] = Field(
        alias=str("AND"), default=None
    )
    or_: Optional[list["WhereImagingConfigOption"]] = Field(
        alias=str("OR"), default=None
    )
    not_: Optional["WhereImagingConfigOption"] = Field(alias=str("NOT"), default=None)
    adaptive_optics: Optional["WhereBoolean"] = Field(
        alias=str("adaptiveOptics"), default=None
    )
    instrument: Optional["WhereEqInstrument"] = None
    fov: Optional["WhereAngle"] = None
    site: Optional["WhereEqSite"] = None
    capability: Optional["WhereOptionEqImagingCapability"] = None


class WhereString(BaseModel):
    eq: Optional[Any] = Field(alias=str("EQ"), default=None)
    neq: Optional[Any] = Field(alias=str("NEQ"), default=None)
    in_: Optional[list[Any]] = Field(alias=str("IN"), default=None)
    nin: Optional[list[Any]] = Field(alias=str("NIN"), default=None)
    like: Optional[Any] = Field(alias=str("LIKE"), default=None)
    nlike: Optional[Any] = Field(alias=str("NLIKE"), default=None)
    match_case: Optional[bool] = Field(alias=str("MATCH_CASE"), default=True)


class WhereTarget(BaseModel):
    and_: Optional[list["WhereTarget"]] = Field(alias=str("AND"), default=None)
    or_: Optional[list["WhereTarget"]] = Field(alias=str("OR"), default=None)
    not_: Optional["WhereTarget"] = Field(alias=str("NOT"), default=None)
    id: Optional["WhereOrderTargetId"] = None
    program: Optional["WhereProgram"] = None
    name: Optional["WhereString"] = None
    disposition: Optional["WhereEqTargetDisposition"] = None
    calibration_role: Optional["WhereOptionEqCalibrationRole"] = Field(
        alias=str("calibrationRole"), default=None
    )


class WhereUser(BaseModel):
    is_null: Optional[bool] = Field(alias=str("IS_NULL"), default=None)
    and_: Optional[list["WhereUser"]] = Field(alias=str("AND"), default=None)
    or_: Optional[list["WhereUser"]] = Field(alias=str("OR"), default=None)
    not_: Optional["WhereUser"] = Field(alias=str("NOT"), default=None)
    id: Optional["WhereOrderUserId"] = None
    type_: Optional["WhereEqUserType"] = Field(alias=str("type"), default=None)
    orcid_id: Optional["WhereOptionString"] = Field(alias=str("orcidId"), default=None)
    profile: Optional["WhereUserProfile"] = None


class WhereUserProfile(BaseModel):
    given_name: Optional["WhereOptionString"] = Field(
        alias=str("givenName"), default=None
    )
    credit_name: Optional["WhereOptionString"] = Field(
        alias=str("creditName"), default=None
    )
    family_name: Optional["WhereOptionString"] = Field(
        alias=str("familyName"), default=None
    )
    email: Optional["WhereOptionString"] = None


class WhereWavelength(BaseModel):
    and_: Optional[list["WhereWavelength"]] = Field(alias=str("AND"), default=None)
    or_: Optional[list["WhereWavelength"]] = Field(alias=str("OR"), default=None)
    not_: Optional["WhereWavelength"] = Field(alias=str("NOT"), default=None)
    picometers: Optional["WhereOrderPosInt"] = None
    angstroms: Optional["WhereOrderPosBigDecimal"] = None
    nanometers: Optional["WhereOrderPosBigDecimal"] = None
    micrometers: Optional["WhereOrderPosBigDecimal"] = None


class WhereOrderObservationWorkflowState(BaseModel):
    eq: Optional[ObservationWorkflowState] = Field(alias=str("EQ"), default=None)
    neq: Optional[ObservationWorkflowState] = Field(alias=str("NEQ"), default=None)
    in_: Optional[list[ObservationWorkflowState]] = Field(alias=str("IN"), default=None)
    nin: Optional[list[ObservationWorkflowState]] = Field(
        alias=str("NIN"), default=None
    )
    gt: Optional[ObservationWorkflowState] = Field(alias=str("GT"), default=None)
    lt: Optional[ObservationWorkflowState] = Field(alias=str("LT"), default=None)
    gte: Optional[ObservationWorkflowState] = Field(alias=str("GTE"), default=None)
    lte: Optional[ObservationWorkflowState] = Field(alias=str("LTE"), default=None)


class WhereCalculatedObservationWorkflow(BaseModel):
    is_null: Optional[bool] = Field(alias=str("IS_NULL"), default=None)
    calculation_state: Optional["WhereOrderCalculationState"] = Field(
        alias=str("calculationState"), default=None
    )
    state: Optional["WhereOrderCalculationState"] = None
    workflow_state: Optional["WhereOrderObservationWorkflowState"] = Field(
        alias=str("workflowState"), default=None
    )


class Flamingos2StepInput(BaseModel):
    instrument_config: "Flamingos2DynamicInput" = Field(alias=str("instrumentConfig"))
    breakpoint: Optional[Breakpoint] = None
    step_config: "StepConfigInput" = Field(alias=str("stepConfig"))
    telescope_config: Optional["TelescopeConfigInput"] = Field(
        alias=str("telescopeConfig"), default=None
    )
    observe_class: ObserveClass = Field(alias=str("observeClass"))


class GmosNorthStepInput(BaseModel):
    instrument_config: "GmosNorthDynamicInput" = Field(alias=str("instrumentConfig"))
    breakpoint: Optional[Breakpoint] = None
    step_config: "StepConfigInput" = Field(alias=str("stepConfig"))
    telescope_config: Optional["TelescopeConfigInput"] = Field(
        alias=str("telescopeConfig"), default=None
    )
    observe_class: ObserveClass = Field(alias=str("observeClass"))


class GmosSouthStepInput(BaseModel):
    instrument_config: "GmosSouthDynamicInput" = Field(alias=str("instrumentConfig"))
    breakpoint: Optional[Breakpoint] = None
    step_config: "StepConfigInput" = Field(alias=str("stepConfig"))
    telescope_config: Optional["TelescopeConfigInput"] = Field(
        alias=str("telescopeConfig"), default=None
    )
    observe_class: ObserveClass = Field(alias=str("observeClass"))


class Igrins2DynamicInput(BaseModel):
    exposure: "TimeSpanInput"


class Igrins2StepInput(BaseModel):
    instrument_config: "Igrins2DynamicInput" = Field(alias=str("instrumentConfig"))
    breakpoint: Optional[Breakpoint] = None
    step_config: "StepConfigInput" = Field(alias=str("stepConfig"))
    telescope_config: Optional["TelescopeConfigInput"] = Field(
        alias=str("telescopeConfig"), default=None
    )
    observe_class: ObserveClass = Field(alias=str("observeClass"))


class Flamingos2AtomInput(BaseModel):
    description: Optional[Any] = None
    steps: list["Flamingos2StepInput"]


class GmosNorthAtomInput(BaseModel):
    description: Optional[Any] = None
    steps: list["GmosNorthStepInput"]


class GmosSouthAtomInput(BaseModel):
    description: Optional[Any] = None
    steps: list["GmosSouthStepInput"]


class Igrins2AtomInput(BaseModel):
    description: Optional[Any] = None
    steps: list["Igrins2StepInput"]


class GnirsAcquisitionMirrorOutInput(BaseModel):
    prism: GnirsPrism
    grating: GnirsGrating
    wavelength: "WavelengthInput"


class GnirsDynamicInput(BaseModel):
    exposure: "TimeSpanInput"
    coadds: Any
    filter_: GnirsFilter = Field(alias=str("filter"))
    decker: GnirsDecker
    fpu_slit: Optional[GnirsFpuSlit] = Field(alias=str("fpuSlit"), default=None)
    fpu_other: Optional[GnirsFpuOther] = Field(alias=str("fpuOther"), default=None)
    fpu_ifu: Optional[GnirsFpuIfu] = Field(alias=str("fpuIfu"), default=None)
    acquisition_mirror_out: Optional["GnirsAcquisitionMirrorOutInput"] = Field(
        alias=str("acquisitionMirrorOut"), default=None
    )
    camera: GnirsCamera
    focus_motor_steps: Optional[int] = Field(alias=str("focusMotorSteps"), default=None)
    read_mode: GnirsReadMode = Field(alias=str("readMode"))


class GnirsStepInput(BaseModel):
    instrument_config: "GnirsDynamicInput" = Field(alias=str("instrumentConfig"))
    breakpoint: Optional[Breakpoint] = None
    step_config: "StepConfigInput" = Field(alias=str("stepConfig"))
    telescope_config: Optional["TelescopeConfigInput"] = Field(
        alias=str("telescopeConfig"), default=None
    )
    observe_class: ObserveClass = Field(alias=str("observeClass"))


class GnirsAtomInput(BaseModel):
    description: Optional[Any] = None
    steps: list["GnirsStepInput"]


class GhostDetectorInput(BaseModel):
    exposure_time: "TimeSpanInput" = Field(alias=str("exposureTime"))
    exposure_count: Any = Field(alias=str("exposureCount"))
    binning: GhostBinning
    read_mode: GhostReadMode = Field(alias=str("readMode"))


class GhostDynamicInput(BaseModel):
    red: "GhostDetectorInput"
    blue: "GhostDetectorInput"
    ifu_1_fiber_agitator: GhostIfu1FiberAgitator = Field(alias=str("ifu1FiberAgitator"))
    ifu_2_fiber_agitator: GhostIfu2FiberAgitator = Field(alias=str("ifu2FiberAgitator"))


class GhostStepInput(BaseModel):
    instrument_config: "GhostDynamicInput" = Field(alias=str("instrumentConfig"))
    breakpoint: Optional[Breakpoint] = None
    step_config: "StepConfigInput" = Field(alias=str("stepConfig"))
    telescope_config: Optional["TelescopeConfigInput"] = Field(
        alias=str("telescopeConfig"), default=None
    )
    observe_class: ObserveClass = Field(alias=str("observeClass"))


class GhostAtomInput(BaseModel):
    description: Optional[Any] = None
    steps: list["GhostStepInput"]


class ReplaceFlamingos2SequenceInput(BaseModel):
    observation_id: Optional[Any] = Field(alias=str("observationId"), default=None)
    observation_reference: Optional[Any] = Field(
        alias=str("observationReference"), default=None
    )
    sequence_type: SequenceType = Field(alias=str("sequenceType"))
    sequence: Optional[list["Flamingos2AtomInput"]] = None


class ReplaceGmosNorthSequenceInput(BaseModel):
    observation_id: Optional[Any] = Field(alias=str("observationId"), default=None)
    observation_reference: Optional[Any] = Field(
        alias=str("observationReference"), default=None
    )
    sequence_type: SequenceType = Field(alias=str("sequenceType"))
    sequence: Optional[list["GmosNorthAtomInput"]] = None


class ReplaceGmosSouthSequenceInput(BaseModel):
    observation_id: Optional[Any] = Field(alias=str("observationId"), default=None)
    observation_reference: Optional[Any] = Field(
        alias=str("observationReference"), default=None
    )
    sequence_type: SequenceType = Field(alias=str("sequenceType"))
    sequence: Optional[list["GmosSouthAtomInput"]] = None


class ReplaceIgrins2SequenceInput(BaseModel):
    observation_id: Optional[Any] = Field(alias=str("observationId"), default=None)
    observation_reference: Optional[Any] = Field(
        alias=str("observationReference"), default=None
    )
    sequence_type: SequenceType = Field(alias=str("sequenceType"))
    sequence: Optional[list["Igrins2AtomInput"]] = None


class ReplaceGnirsSequenceInput(BaseModel):
    observation_id: Optional[Any] = Field(alias=str("observationId"), default=None)
    observation_reference: Optional[Any] = Field(
        alias=str("observationReference"), default=None
    )
    sequence_type: SequenceType = Field(alias=str("sequenceType"))
    sequence: Optional[list["GnirsAtomInput"]] = None


class ReplaceGhostSequenceInput(BaseModel):
    observation_id: Optional[Any] = Field(alias=str("observationId"), default=None)
    observation_reference: Optional[Any] = Field(
        alias=str("observationReference"), default=None
    )
    sequence_type: SequenceType = Field(alias=str("sequenceType"))
    sequence: Optional[list["GhostAtomInput"]] = None


AddProgramUserInput.model_rebuild()
AddEventBatchEntryInput.model_rebuild()
AddEventBatchInput.model_rebuild()
AddTimeChargeCorrectionInput.model_rebuild()
AllocationInput.model_rebuild()
BandNormalizedIntegratedInput.model_rebuild()
BandNormalizedSurfaceInput.model_rebuild()
GeminiCallPropertiesInput.model_rebuild()
KeckCallPropertiesInput.model_rebuild()
SubaruCallPropertiesInput.model_rebuild()
CallForProposalsPropertiesInput.model_rebuild()
SiteCoordinateLimitsInput.model_rebuild()
CoordinateLimitsInput.model_rebuild()
CloneObservationInput.model_rebuild()
CloneTargetInput.model_rebuild()
ConstraintSetInput.model_rebuild()
ConditionsEntryInput.model_rebuild()
ConditionsMeasurementInput.model_rebuild()
ConditionsIntuitionInput.model_rebuild()
ConditionsExpectationInput.model_rebuild()
CoordinatesInput.model_rebuild()
CreateCallForProposalsInput.model_rebuild()
CreateObservationInput.model_rebuild()
CreateProgramInput.model_rebuild()
CreateProgramNoteInput.model_rebuild()
CreateProposalInput.model_rebuild()
CreateTargetInput.model_rebuild()
ElevationRangeInput.model_rebuild()
EmissionLineIntegratedInput.model_rebuild()
EmissionLineSurfaceInput.model_rebuild()
EmissionLinesIntegratedInput.model_rebuild()
EmissionLinesSurfaceInput.model_rebuild()
ExposureTimeModeInput.model_rebuild()
TimeAndCountExposureTimeModeInput.model_rebuild()
FluxDensity.model_rebuild()
GaussianInput.model_rebuild()
GmosNodAndShuffleInput.model_rebuild()
GmosNorthDynamicInput.model_rebuild()
GmosNorthFpuInput.model_rebuild()
GmosNorthGratingConfigInput.model_rebuild()
GmosNorthLongSlitAcquisitionInput.model_rebuild()
GmosNorthLongSlitInput.model_rebuild()
GmosNorthImagingInput.model_rebuild()
GmosNorthStaticInput.model_rebuild()
GmosSouthDynamicInput.model_rebuild()
GmosSouthFpuInput.model_rebuild()
GmosSouthGratingConfigInput.model_rebuild()
GmosSouthLongSlitAcquisitionInput.model_rebuild()
GmosSouthLongSlitInput.model_rebuild()
GmosNorthMosInput.model_rebuild()
GmosNorthMosAcquisitionInput.model_rebuild()
GmosSouthMosInput.model_rebuild()
GmosSouthMosAcquisitionInput.model_rebuild()
GmosSouthImagingFilterInput.model_rebuild()
GmosSouthImagingInput.model_rebuild()
GmosSouthStaticInput.model_rebuild()
CloneGroupInput.model_rebuild()
UserSuppliedEphemerisElement.model_rebuild()
UserSuppliedEphemeris.model_rebuild()
NonsiderealInput.model_rebuild()
SchedulingConstraintsInput.model_rebuild()
ObservationPropertiesInput.model_rebuild()
ObservationTimesInput.model_rebuild()
OffsetInput.model_rebuild()
TelescopeConfigGeneratorInput.model_rebuild()
EnumeratedTelescopeConfigGeneratorInput.model_rebuild()
RandomTelescopeConfigGeneratorInput.model_rebuild()
SpiralTelescopeConfigGeneratorInput.model_rebuild()
UniformTelescopeConfigGeneratorInput.model_rebuild()
PosAngleConstraintInput.model_rebuild()
ProgramPropertiesInput.model_rebuild()
ProgramUserPropertiesInput.model_rebuild()
ProperMotionInput.model_rebuild()
GeminiProposalTypeInput.model_rebuild()
KeckProposalTypeInput.model_rebuild()
SubaruProposalTypeInput.model_rebuild()
ClassicalInput.model_rebuild()
LargeProgramInput.model_rebuild()
QueueInput.model_rebuild()
ProposalPropertiesInput.model_rebuild()
RecordGmosNorthVisitInput.model_rebuild()
RecordGmosSouthVisitInput.model_rebuild()
ObservingModeInput.model_rebuild()
VisitorInput.model_rebuild()
ExchangeInput.model_rebuild()
ScienceRequirementsInput.model_rebuild()
SetAllocationsInput.model_rebuild()
SetProgramReferenceInput.model_rebuild()
ProgramReferencePropertiesInput.model_rebuild()
SiderealInput.model_rebuild()
OpportunityInput.model_rebuild()
RegionInput.model_rebuild()
RightAscensionArcInput.model_rebuild()
DeclinationArcInput.model_rebuild()
SignalToNoiseExposureTimeModeInput.model_rebuild()
SourceProfileInput.model_rebuild()
SpectralDefinitionIntegratedInput.model_rebuild()
SpectralDefinitionSurfaceInput.model_rebuild()
SpectroscopyScienceRequirementsInput.model_rebuild()
StepConfigInput.model_rebuild()
ObscalcUpdateInput.model_rebuild()
ExecutionEventAddedInput.model_rebuild()
TargetEnvironmentInput.model_rebuild()
TargetPropertiesInput.model_rebuild()
TelescopeConfigInput.model_rebuild()
TimingWindowRepeatInput.model_rebuild()
TimingWindowEndInput.model_rebuild()
TimingWindowInput.model_rebuild()
UnnormalizedSedInput.model_rebuild()
UpdateAsterismsInput.model_rebuild()
UpdateAttachmentsInput.model_rebuild()
UpdateCallsForProposalsInput.model_rebuild()
UpdateDatasetsInput.model_rebuild()
UpdateGroupsInput.model_rebuild()
UpdateObservationsInput.model_rebuild()
UpdateConfigurationRequestsInput.model_rebuild()
UpdateObservationsTimesInput.model_rebuild()
UpdateProgramUsersInput.model_rebuild()
UpdateProgramNotesInput.model_rebuild()
UpdateProgramsInput.model_rebuild()
UpdateProposalInput.model_rebuild()
UpdateTargetsInput.model_rebuild()
WhereDatasetChronicleEntry.model_rebuild()
RecordFlamingos2VisitInput.model_rebuild()
RecordIgrins2VisitInput.model_rebuild()
Flamingos2DynamicInput.model_rebuild()
Flamingos2FpuMaskInput.model_rebuild()
Flamingos2LongSlitAcquisitionInput.model_rebuild()
Flamingos2LongSlitInput.model_rebuild()
Flamingos2ImagingFilterInput.model_rebuild()
Flamingos2ImagingInput.model_rebuild()
GhostDetectorConfigInput.model_rebuild()
GhostIfuInput.model_rebuild()
Igrins2LongSlitInput.model_rebuild()
Igrins2SvcInput.model_rebuild()
GnirsImagingFilterInput.model_rebuild()
GnirsImagingAcquisitionInput.model_rebuild()
GnirsImagingInput.model_rebuild()
GnirsCentralWavelengthConfigInput.model_rebuild()
GnirsSpectroscopyAcquisitionInput.model_rebuild()
TelescopeConfigAlongSlitInput.model_rebuild()
SlitTelescopeConfigsInput.model_rebuild()
GnirsSlitInput.model_rebuild()
GnirsIfuInput.model_rebuild()
GnirsSpectroscopyInput.model_rebuild()
ImagingVariantInput.model_rebuild()
GroupedImagingVariantInput.model_rebuild()
InterleavedImagingVariantInput.model_rebuild()
PreImagingVariantInput.model_rebuild()
GmosNorthImagingFilterInput.model_rebuild()
GroupPropertiesInput.model_rebuild()
CreateGroupInput.model_rebuild()
ImagingScienceRequirementsInput.model_rebuild()
WhereTooTrigger.model_rebuild()
WhereTooTriggerChronicleEntry.model_rebuild()
CreateConfigurationRequestInput.model_rebuild()
TimeChargeCorrectionInput.model_rebuild()
WhereAngle.model_rebuild()
WhereCallForProposals.model_rebuild()
WhereGeminiCallProperties.model_rebuild()
WhereAttachment.model_rebuild()
WhereDataset.model_rebuild()
WhereDatasetReference.model_rebuild()
WhereExecutionEvent.model_rebuild()
WhereObservation.model_rebuild()
WhereConfigurationRequest.model_rebuild()
WhereObservationReference.model_rebuild()
WhereGroup.model_rebuild()
WhereProposalReference.model_rebuild()
WherePartnerLink.model_rebuild()
WhereProgram.model_rebuild()
WhereProgramReference.model_rebuild()
WhereProgramNote.model_rebuild()
WhereProgramUser.model_rebuild()
WhereProposal.model_rebuild()
WhereProposalPartnerEntry.model_rebuild()
WhereProposalPartners.model_rebuild()
WhereSpectroscopyConfigOption.model_rebuild()
WhereImagingConfigOption.model_rebuild()
WhereTarget.model_rebuild()
WhereUser.model_rebuild()
WhereUserProfile.model_rebuild()
WhereWavelength.model_rebuild()
WhereCalculatedObservationWorkflow.model_rebuild()
Flamingos2StepInput.model_rebuild()
GmosNorthStepInput.model_rebuild()
GmosSouthStepInput.model_rebuild()
Igrins2DynamicInput.model_rebuild()
Igrins2StepInput.model_rebuild()
Flamingos2AtomInput.model_rebuild()
GmosNorthAtomInput.model_rebuild()
GmosSouthAtomInput.model_rebuild()
Igrins2AtomInput.model_rebuild()
GnirsAcquisitionMirrorOutInput.model_rebuild()
GnirsDynamicInput.model_rebuild()
GnirsStepInput.model_rebuild()
GnirsAtomInput.model_rebuild()
GhostDetectorInput.model_rebuild()
GhostDynamicInput.model_rebuild()
GhostStepInput.model_rebuild()
GhostAtomInput.model_rebuild()
ReplaceFlamingos2SequenceInput.model_rebuild()
ReplaceGmosNorthSequenceInput.model_rebuild()
ReplaceGmosSouthSequenceInput.model_rebuild()
ReplaceIgrins2SequenceInput.model_rebuild()
ReplaceGnirsSequenceInput.model_rebuild()
ReplaceGhostSequenceInput.model_rebuild()
