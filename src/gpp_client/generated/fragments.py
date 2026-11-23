from typing import Annotated, Any, Literal, Optional, Union

from pydantic import Field

from .base_model import BaseModel
from .enums import (
    ArcType,
    AttachmentType,
    Band,
    BrightnessIntegratedUnits,
    CalculationState,
    CalibrationRole,
    CloudExtinctionPreset,
    ConfigurationRequestStatus,
    CoolStarTemperature,
    EphemerisKeyType,
    Existence,
    Flamingos2CustomSlitWidth,
    Flamingos2Decker,
    Flamingos2Disperser,
    Flamingos2Filter,
    Flamingos2Fpu,
    Flamingos2ReadMode,
    Flamingos2ReadoutMode,
    Flamingos2Reads,
    FocalPlane,
    GalaxySpectrum,
    GeminiCallForProposalsType,
    GhostBinning,
    GhostIfu1FiberAgitator,
    GhostIfu2FiberAgitator,
    GhostReadMode,
    GhostResolutionMode,
    GmosAmpGain,
    GmosAmpReadMode,
    GmosBinning,
    GmosCustomSlitWidth,
    GmosMosAcquisitionType,
    GmosNorthBuiltinFpu,
    GmosNorthFilter,
    GmosNorthGrating,
    GmosNorthIfuFpu,
    GmosRoi,
    GmosSouthBuiltinFpu,
    GmosSouthFilter,
    GmosSouthGrating,
    GmosSouthIfuFpu,
    GnirsAcquisitionType,
    GnirsCamera,
    GnirsDecker,
    GnirsFilter,
    GnirsFpuIfu,
    GnirsFpuSlit,
    GnirsGrating,
    GnirsPrism,
    GnirsReadMode,
    GnirsWellDepth,
    GuideState,
    HiiRegionSpectrum,
    ImageQualityPreset,
    ImagingVariantType,
    Instrument,
    KeckInstrument,
    MosDispersionDirection,
    ObservationPriority,
    ObservationValidationCode,
    ObservationWorkflowState,
    Observatory,
    ObservingModeType,
    PlanetaryNebulaSpectrum,
    PlanetSpectrum,
    PosAngleConstraintMode,
    ProgramType,
    ProposalStatus,
    QuasarSpectrum,
    SchedulingMode,
    ScienceBand,
    ScienceMode,
    ScienceSubtype,
    Site,
    SkyBackground,
    SlitOffsetMode,
    StellarLibrarySpectrum,
    SubaruCallForProposalsType,
    SubaruInstrument,
    TelescopeConfigGeneratorType,
    TelluricTag,
    TimingWindowInclusion,
    TooActivation,
    VisitorObservingModeType,
    WaterVapor,
    WavelengthOrder,
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
    observatory: Observatory
    gemini: Optional["CallForProposalsCoreGemini"]
    keck: Optional["CallForProposalsCoreKeck"]
    subaru: Optional["CallForProposalsCoreSubaru"]


class CallForProposalsCoreGemini(BaseModel):
    type_: GeminiCallForProposalsType = Field(alias="type")
    instruments: list[Instrument]


class CallForProposalsCoreKeck(BaseModel):
    instruments: list[KeckInstrument]


class CallForProposalsCoreSubaru(BaseModel):
    type_: SubaruCallForProposalsType = Field(alias="type")
    instruments: list[SubaruInstrument]


class CallForProposalsDetails(CallForProposalsCore):
    semester: Any
    active: "CallForProposalsDetailsActive"
    submission_deadline_default: Optional[Any] = Field(
        alias="submissionDeadlineDefault"
    )
    existence: Existence


class CallForProposalsDetailsActive(BaseModel):
    start: Any
    end: Any


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


class Flamingos2ImagingDetails(BaseModel):
    filters: list["Flamingos2ImagingDetailsFilters"]
    initial_filters: list["Flamingos2ImagingDetailsInitialFilters"] = Field(
        alias="initialFilters"
    )
    default_read_mode: Flamingos2ReadMode = Field(alias="defaultReadMode")
    explicit_read_mode: Optional[Flamingos2ReadMode] = Field(alias="explicitReadMode")
    default_reads: Flamingos2Reads = Field(alias="defaultReads")
    explicit_reads: Optional[Flamingos2Reads] = Field(alias="explicitReads")
    default_decker: Flamingos2Decker = Field(alias="defaultDecker")
    explicit_decker: Optional[Flamingos2Decker] = Field(alias="explicitDecker")
    readout_mode: Flamingos2ReadoutMode = Field(alias="readoutMode")
    default_readout_mode: Flamingos2ReadoutMode = Field(alias="defaultReadoutMode")
    explicit_readout_mode: Optional[Flamingos2ReadoutMode] = Field(
        alias="explicitReadoutMode"
    )


class Flamingos2ImagingDetailsFilters(BaseModel):
    filter_: Flamingos2Filter = Field(alias="filter")
    exposure_time_mode: "Flamingos2ImagingDetailsFiltersExposureTimeMode" = Field(
        alias="exposureTimeMode"
    )


class Flamingos2ImagingDetailsFiltersExposureTimeMode(BaseModel):
    signal_to_noise: Optional[
        "Flamingos2ImagingDetailsFiltersExposureTimeModeSignalToNoise"
    ] = Field(alias="signalToNoise")
    time_and_count: Optional[
        "Flamingos2ImagingDetailsFiltersExposureTimeModeTimeAndCount"
    ] = Field(alias="timeAndCount")


class Flamingos2ImagingDetailsFiltersExposureTimeModeSignalToNoise(BaseModel):
    at: "Flamingos2ImagingDetailsFiltersExposureTimeModeSignalToNoiseAt"
    value: Any


class Flamingos2ImagingDetailsFiltersExposureTimeModeSignalToNoiseAt(BaseModel):
    nanometers: Any


class Flamingos2ImagingDetailsFiltersExposureTimeModeTimeAndCount(BaseModel):
    time: "Flamingos2ImagingDetailsFiltersExposureTimeModeTimeAndCountTime"
    count: Any


class Flamingos2ImagingDetailsFiltersExposureTimeModeTimeAndCountTime(BaseModel):
    seconds: Any


class Flamingos2ImagingDetailsInitialFilters(BaseModel):
    filter_: Flamingos2Filter = Field(alias="filter")
    exposure_time_mode: "Flamingos2ImagingDetailsInitialFiltersExposureTimeMode" = (
        Field(alias="exposureTimeMode")
    )


class Flamingos2ImagingDetailsInitialFiltersExposureTimeMode(BaseModel):
    signal_to_noise: Optional[
        "Flamingos2ImagingDetailsInitialFiltersExposureTimeModeSignalToNoise"
    ] = Field(alias="signalToNoise")
    time_and_count: Optional[
        "Flamingos2ImagingDetailsInitialFiltersExposureTimeModeTimeAndCount"
    ] = Field(alias="timeAndCount")


class Flamingos2ImagingDetailsInitialFiltersExposureTimeModeSignalToNoise(BaseModel):
    at: "Flamingos2ImagingDetailsInitialFiltersExposureTimeModeSignalToNoiseAt"
    value: Any


class Flamingos2ImagingDetailsInitialFiltersExposureTimeModeSignalToNoiseAt(BaseModel):
    nanometers: Any


class Flamingos2ImagingDetailsInitialFiltersExposureTimeModeTimeAndCount(BaseModel):
    at: "Flamingos2ImagingDetailsInitialFiltersExposureTimeModeTimeAndCountAt"
    count: Any
    time: "Flamingos2ImagingDetailsInitialFiltersExposureTimeModeTimeAndCountTime"


class Flamingos2ImagingDetailsInitialFiltersExposureTimeModeTimeAndCountAt(BaseModel):
    nanometers: Any


class Flamingos2ImagingDetailsInitialFiltersExposureTimeModeTimeAndCountTime(BaseModel):
    seconds: Any


class Flamingos2LongSlitDetails(BaseModel):
    decker: Flamingos2Decker
    default_decker: Flamingos2Decker = Field(alias="defaultDecker")
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
    acquisition: "Flamingos2LongSlitDetailsAcquisition"
    initial_disperser: Flamingos2Disperser = Field(alias="initialDisperser")
    initial_filter: Flamingos2Filter = Field(alias="initialFilter")
    initial_fpu: Flamingos2Fpu = Field(alias="initialFpu")


class Flamingos2LongSlitDetailsTelluricType(BaseModel):
    tag: TelluricTag
    star_types: Optional[list[str]] = Field(alias="starTypes")


class Flamingos2LongSlitDetailsExposureTimeMode(BaseModel):
    signal_to_noise: Optional[
        "Flamingos2LongSlitDetailsExposureTimeModeSignalToNoise"
    ] = Field(alias="signalToNoise")
    time_and_count: Optional[
        "Flamingos2LongSlitDetailsExposureTimeModeTimeAndCount"
    ] = Field(alias="timeAndCount")


class Flamingos2LongSlitDetailsExposureTimeModeSignalToNoise(BaseModel):
    value: Any
    at: "Flamingos2LongSlitDetailsExposureTimeModeSignalToNoiseAt"


class Flamingos2LongSlitDetailsExposureTimeModeSignalToNoiseAt(BaseModel):
    nanometers: Any


class Flamingos2LongSlitDetailsExposureTimeModeTimeAndCount(BaseModel):
    time: "Flamingos2LongSlitDetailsExposureTimeModeTimeAndCountTime"
    count: Any
    at: "Flamingos2LongSlitDetailsExposureTimeModeTimeAndCountAt"


class Flamingos2LongSlitDetailsExposureTimeModeTimeAndCountTime(BaseModel):
    seconds: Any


class Flamingos2LongSlitDetailsExposureTimeModeTimeAndCountAt(BaseModel):
    nanometers: Any


class Flamingos2LongSlitDetailsAcquisition(BaseModel):
    exposure_time_mode: "Flamingos2LongSlitDetailsAcquisitionExposureTimeMode" = Field(
        alias="exposureTimeMode"
    )


class Flamingos2LongSlitDetailsAcquisitionExposureTimeMode(BaseModel):
    signal_to_noise: Optional[
        "Flamingos2LongSlitDetailsAcquisitionExposureTimeModeSignalToNoise"
    ] = Field(alias="signalToNoise")
    time_and_count: Optional[
        "Flamingos2LongSlitDetailsAcquisitionExposureTimeModeTimeAndCount"
    ] = Field(alias="timeAndCount")


class Flamingos2LongSlitDetailsAcquisitionExposureTimeModeSignalToNoise(BaseModel):
    value: Any
    at: "Flamingos2LongSlitDetailsAcquisitionExposureTimeModeSignalToNoiseAt"


class Flamingos2LongSlitDetailsAcquisitionExposureTimeModeSignalToNoiseAt(BaseModel):
    nanometers: Any


class Flamingos2LongSlitDetailsAcquisitionExposureTimeModeTimeAndCount(BaseModel):
    time: "Flamingos2LongSlitDetailsAcquisitionExposureTimeModeTimeAndCountTime"
    count: Any
    at: "Flamingos2LongSlitDetailsAcquisitionExposureTimeModeTimeAndCountAt"


class Flamingos2LongSlitDetailsAcquisitionExposureTimeModeTimeAndCountTime(BaseModel):
    seconds: Any


class Flamingos2LongSlitDetailsAcquisitionExposureTimeModeTimeAndCountAt(BaseModel):
    nanometers: Any


class GOATSConfigurationTarget(BaseModel):
    coordinates: Optional["GOATSConfigurationTargetCoordinates"]
    region: Optional["GOATSConfigurationTargetRegion"]


class GOATSConfigurationTargetCoordinates(BaseModel):
    ra: "GOATSConfigurationTargetCoordinatesRa"
    dec: "GOATSConfigurationTargetCoordinatesDec"


class GOATSConfigurationTargetCoordinatesRa(BaseModel):
    hms: Any
    degrees: Any


class GOATSConfigurationTargetCoordinatesDec(BaseModel):
    dms: Any
    degrees: Any


class GOATSConfigurationTargetRegion(BaseModel):
    right_ascension_arc: "GOATSConfigurationTargetRegionRightAscensionArc" = Field(
        alias="rightAscensionArc"
    )
    declination_arc: "GOATSConfigurationTargetRegionDeclinationArc" = Field(
        alias="declinationArc"
    )


class GOATSConfigurationTargetRegionRightAscensionArc(BaseModel):
    type_: ArcType = Field(alias="type")
    start: Optional["GOATSConfigurationTargetRegionRightAscensionArcStart"]
    end: Optional["GOATSConfigurationTargetRegionRightAscensionArcEnd"]


class GOATSConfigurationTargetRegionRightAscensionArcStart(BaseModel):
    hms: Any
    degrees: Any


class GOATSConfigurationTargetRegionRightAscensionArcEnd(BaseModel):
    hms: Any
    degrees: Any


class GOATSConfigurationTargetRegionDeclinationArc(BaseModel):
    type_: ArcType = Field(alias="type")
    start: Optional["GOATSConfigurationTargetRegionDeclinationArcStart"]
    end: Optional["GOATSConfigurationTargetRegionDeclinationArcEnd"]


class GOATSConfigurationTargetRegionDeclinationArcStart(BaseModel):
    dms: Any
    degrees: Any


class GOATSConfigurationTargetRegionDeclinationArcEnd(BaseModel):
    dms: Any
    degrees: Any


class GOATSConfigurationRequest(BaseModel):
    id: Any
    status: ConfigurationRequestStatus
    justification: Optional[Any]
    applicable_observations: list[Any] = Field(alias="applicableObservations")
    configuration: "GOATSConfigurationRequestConfiguration"


class GOATSConfigurationRequestConfiguration(BaseModel):
    conditions: "GOATSConfigurationRequestConfigurationConditions"
    target: Optional["GOATSConfigurationRequestConfigurationTarget"]
    observing_mode: Optional["GOATSConfigurationRequestConfigurationObservingMode"] = (
        Field(alias="observingMode")
    )


class GOATSConfigurationRequestConfigurationConditions(BaseModel):
    image_quality: ImageQualityPreset = Field(alias="imageQuality")
    cloud_extinction: CloudExtinctionPreset = Field(alias="cloudExtinction")
    sky_background: SkyBackground = Field(alias="skyBackground")
    water_vapor: WaterVapor = Field(alias="waterVapor")


class GOATSConfigurationRequestConfigurationTarget(GOATSConfigurationTarget):
    pass


class GOATSConfigurationRequestConfigurationObservingMode(BaseModel):
    instrument: Optional[Instrument]
    mode: ObservingModeType
    gmos_north_long_slit: Optional[
        "GOATSConfigurationRequestConfigurationObservingModeGmosNorthLongSlit"
    ] = Field(alias="gmosNorthLongSlit")
    gmos_south_long_slit: Optional[
        "GOATSConfigurationRequestConfigurationObservingModeGmosSouthLongSlit"
    ] = Field(alias="gmosSouthLongSlit")
    gmos_north_imaging: Optional[
        "GOATSConfigurationRequestConfigurationObservingModeGmosNorthImaging"
    ] = Field(alias="gmosNorthImaging")
    gmos_south_imaging: Optional[
        "GOATSConfigurationRequestConfigurationObservingModeGmosSouthImaging"
    ] = Field(alias="gmosSouthImaging")


class GOATSConfigurationRequestConfigurationObservingModeGmosNorthLongSlit(BaseModel):
    grating: GmosNorthGrating


class GOATSConfigurationRequestConfigurationObservingModeGmosSouthLongSlit(BaseModel):
    grating: GmosSouthGrating


class GOATSConfigurationRequestConfigurationObservingModeGmosNorthImaging(BaseModel):
    filters: list[GmosNorthFilter]


class GOATSConfigurationRequestConfigurationObservingModeGmosSouthImaging(BaseModel):
    filters: list[GmosSouthFilter]


class GOATSConstraintSet(BaseModel):
    image_quality: ImageQualityPreset = Field(alias="imageQuality")
    cloud_extinction: CloudExtinctionPreset = Field(alias="cloudExtinction")
    sky_background: SkyBackground = Field(alias="skyBackground")
    water_vapor: WaterVapor = Field(alias="waterVapor")
    elevation_range: "GOATSConstraintSetElevationRange" = Field(alias="elevationRange")


class GOATSConstraintSetElevationRange(BaseModel):
    air_mass: Optional["GOATSConstraintSetElevationRangeAirMass"] = Field(
        alias="airMass"
    )
    hour_angle: Optional["GOATSConstraintSetElevationRangeHourAngle"] = Field(
        alias="hourAngle"
    )


class GOATSConstraintSetElevationRangeAirMass(BaseModel):
    min: Any
    max: Any


class GOATSConstraintSetElevationRangeHourAngle(BaseModel):
    min_hours: Any = Field(alias="minHours")
    max_hours: Any = Field(alias="maxHours")


class GOATSExposureTimeMode(BaseModel):
    signal_to_noise: Optional["GOATSExposureTimeModeSignalToNoise"] = Field(
        alias="signalToNoise"
    )
    time_and_count: Optional["GOATSExposureTimeModeTimeAndCount"] = Field(
        alias="timeAndCount"
    )


class GOATSExposureTimeModeSignalToNoise(BaseModel):
    value: Any
    at: "GOATSExposureTimeModeSignalToNoiseAt"


class GOATSExposureTimeModeSignalToNoiseAt(BaseModel):
    nanometers: Any


class GOATSExposureTimeModeTimeAndCount(BaseModel):
    time: "GOATSExposureTimeModeTimeAndCountTime"
    count: Any
    at: "GOATSExposureTimeModeTimeAndCountAt"


class GOATSExposureTimeModeTimeAndCountTime(BaseModel):
    seconds: Any


class GOATSExposureTimeModeTimeAndCountAt(BaseModel):
    nanometers: Any


class GOATSOffset(BaseModel):
    p: "GOATSOffsetP"
    q: "GOATSOffsetQ"


class GOATSOffsetP(BaseModel):
    arcseconds: Any


class GOATSOffsetQ(BaseModel):
    arcseconds: Any


class GOATSTelescopeConfig(BaseModel):
    guiding: GuideState
    offset: "GOATSTelescopeConfigOffset"


class GOATSTelescopeConfigOffset(GOATSOffset):
    pass


class GOATSTelescopeConfigGenerator(BaseModel):
    generator_type: TelescopeConfigGeneratorType = Field(alias="generatorType")
    enumerated: Optional["GOATSTelescopeConfigGeneratorEnumerated"]
    random: Optional["GOATSTelescopeConfigGeneratorRandom"]
    spiral: Optional["GOATSTelescopeConfigGeneratorSpiral"]
    uniform: Optional["GOATSTelescopeConfigGeneratorUniform"]


class GOATSTelescopeConfigGeneratorEnumerated(BaseModel):
    values: list["GOATSTelescopeConfigGeneratorEnumeratedValues"]


class GOATSTelescopeConfigGeneratorEnumeratedValues(GOATSTelescopeConfig):
    pass


class GOATSTelescopeConfigGeneratorRandom(BaseModel):
    seed: Any
    size: "GOATSTelescopeConfigGeneratorRandomSize"
    center: "GOATSTelescopeConfigGeneratorRandomCenter"


class GOATSTelescopeConfigGeneratorRandomSize(BaseModel):
    arcseconds: Any


class GOATSTelescopeConfigGeneratorRandomCenter(GOATSOffset):
    pass


class GOATSTelescopeConfigGeneratorSpiral(BaseModel):
    seed: Any
    size: "GOATSTelescopeConfigGeneratorSpiralSize"
    center: "GOATSTelescopeConfigGeneratorSpiralCenter"


class GOATSTelescopeConfigGeneratorSpiralSize(BaseModel):
    arcseconds: Any


class GOATSTelescopeConfigGeneratorSpiralCenter(GOATSOffset):
    pass


class GOATSTelescopeConfigGeneratorUniform(BaseModel):
    corner_a: "GOATSTelescopeConfigGeneratorUniformCornerA" = Field(alias="cornerA")
    corner_b: "GOATSTelescopeConfigGeneratorUniformCornerB" = Field(alias="cornerB")


class GOATSTelescopeConfigGeneratorUniformCornerA(GOATSOffset):
    pass


class GOATSTelescopeConfigGeneratorUniformCornerB(GOATSOffset):
    pass


class GOATSImagingVariant(BaseModel):
    variant_type: ImagingVariantType = Field(alias="variantType")
    grouped: Optional["GOATSImagingVariantGrouped"]
    interleaved: Optional["GOATSImagingVariantInterleaved"]
    pre_imaging: Optional["GOATSImagingVariantPreImaging"] = Field(alias="preImaging")


class GOATSImagingVariantGrouped(BaseModel):
    sky_count: Any = Field(alias="skyCount")
    sky_offsets: "GOATSImagingVariantGroupedSkyOffsets" = Field(alias="skyOffsets")
    order: WavelengthOrder
    offsets: "GOATSImagingVariantGroupedOffsets"


class GOATSImagingVariantGroupedSkyOffsets(GOATSTelescopeConfigGenerator):
    pass


class GOATSImagingVariantGroupedOffsets(GOATSTelescopeConfigGenerator):
    pass


class GOATSImagingVariantInterleaved(BaseModel):
    offsets: "GOATSImagingVariantInterleavedOffsets"
    sky_count: Any = Field(alias="skyCount")
    sky_offsets: "GOATSImagingVariantInterleavedSkyOffsets" = Field(alias="skyOffsets")


class GOATSImagingVariantInterleavedOffsets(GOATSTelescopeConfigGenerator):
    pass


class GOATSImagingVariantInterleavedSkyOffsets(GOATSTelescopeConfigGenerator):
    pass


class GOATSImagingVariantPreImaging(BaseModel):
    offset_1: "GOATSImagingVariantPreImagingOffset1" = Field(alias="offset1")
    offset_2: "GOATSImagingVariantPreImagingOffset2" = Field(alias="offset2")
    offset_3: "GOATSImagingVariantPreImagingOffset3" = Field(alias="offset3")
    offset_4: "GOATSImagingVariantPreImagingOffset4" = Field(alias="offset4")


class GOATSImagingVariantPreImagingOffset1(GOATSOffset):
    pass


class GOATSImagingVariantPreImagingOffset2(GOATSOffset):
    pass


class GOATSImagingVariantPreImagingOffset3(GOATSOffset):
    pass


class GOATSImagingVariantPreImagingOffset4(GOATSOffset):
    pass


class GOATSGmosNorthImaging(BaseModel):
    filters: list["GOATSGmosNorthImagingFilters"]
    amp_read_mode: GmosAmpReadMode = Field(alias="ampReadMode")
    bin: GmosBinning
    roi: GmosRoi
    variant: "GOATSGmosNorthImagingVariant"


class GOATSGmosNorthImagingFilters(BaseModel):
    filter_: GmosNorthFilter = Field(alias="filter")
    exposure_time_mode: "GOATSGmosNorthImagingFiltersExposureTimeMode" = Field(
        alias="exposureTimeMode"
    )


class GOATSGmosNorthImagingFiltersExposureTimeMode(GOATSExposureTimeMode):
    pass


class GOATSGmosNorthImagingVariant(GOATSImagingVariant):
    pass


class GOATSSlitTelescopeConfigs(BaseModel):
    along_slit: Optional[list["GOATSSlitTelescopeConfigsAlongSlit"]] = Field(
        alias="alongSlit"
    )
    offset_mode: SlitOffsetMode = Field(alias="offsetMode")
    to_sky: Optional[list["GOATSSlitTelescopeConfigsToSky"]] = Field(alias="toSky")


class GOATSSlitTelescopeConfigsAlongSlit(BaseModel):
    guiding: GuideState
    q: "GOATSSlitTelescopeConfigsAlongSlitQ"


class GOATSSlitTelescopeConfigsAlongSlitQ(BaseModel):
    arcseconds: Any


class GOATSSlitTelescopeConfigsToSky(GOATSTelescopeConfig):
    pass


class GOATSGmosNorthLongSlit(BaseModel):
    grating: GmosNorthGrating
    filter_: Optional[GmosNorthFilter] = Field(alias="filter")
    fpu: GmosNorthBuiltinFpu
    central_wavelength: "GOATSGmosNorthLongSlitCentralWavelength" = Field(
        alias="centralWavelength"
    )
    wavelength_dithers: list["GOATSGmosNorthLongSlitWavelengthDithers"] = Field(
        alias="wavelengthDithers"
    )
    x_bin: GmosBinning = Field(alias="xBin")
    y_bin: GmosBinning = Field(alias="yBin")
    amp_read_mode: GmosAmpReadMode = Field(alias="ampReadMode")
    roi: GmosRoi
    exposure_time_mode: "GOATSGmosNorthLongSlitExposureTimeMode" = Field(
        alias="exposureTimeMode"
    )
    default_telescope_configs: "GOATSGmosNorthLongSlitDefaultTelescopeConfigs" = Field(
        alias="defaultTelescopeConfigs"
    )
    explicit_telescope_configs: Optional[
        "GOATSGmosNorthLongSlitExplicitTelescopeConfigs"
    ] = Field(alias="explicitTelescopeConfigs")


class GOATSGmosNorthLongSlitCentralWavelength(BaseModel):
    nanometers: Any


class GOATSGmosNorthLongSlitWavelengthDithers(BaseModel):
    nanometers: Any


class GOATSGmosNorthLongSlitExposureTimeMode(GOATSExposureTimeMode):
    pass


class GOATSGmosNorthLongSlitDefaultTelescopeConfigs(GOATSSlitTelescopeConfigs):
    pass


class GOATSGmosNorthLongSlitExplicitTelescopeConfigs(GOATSSlitTelescopeConfigs):
    pass


class GOATSGmosSouthImaging(BaseModel):
    filters: list["GOATSGmosSouthImagingFilters"]
    amp_read_mode: GmosAmpReadMode = Field(alias="ampReadMode")
    bin: GmosBinning
    roi: GmosRoi
    variant: "GOATSGmosSouthImagingVariant"


class GOATSGmosSouthImagingFilters(BaseModel):
    filter_: GmosSouthFilter = Field(alias="filter")
    exposure_time_mode: "GOATSGmosSouthImagingFiltersExposureTimeMode" = Field(
        alias="exposureTimeMode"
    )


class GOATSGmosSouthImagingFiltersExposureTimeMode(GOATSExposureTimeMode):
    pass


class GOATSGmosSouthImagingVariant(GOATSImagingVariant):
    pass


class GOATSGmosSouthLongSlit(BaseModel):
    grating: GmosSouthGrating
    filter_: Optional[GmosSouthFilter] = Field(alias="filter")
    fpu: GmosSouthBuiltinFpu
    central_wavelength: "GOATSGmosSouthLongSlitCentralWavelength" = Field(
        alias="centralWavelength"
    )
    wavelength_dithers: list["GOATSGmosSouthLongSlitWavelengthDithers"] = Field(
        alias="wavelengthDithers"
    )
    x_bin: GmosBinning = Field(alias="xBin")
    y_bin: GmosBinning = Field(alias="yBin")
    amp_read_mode: GmosAmpReadMode = Field(alias="ampReadMode")
    roi: GmosRoi
    exposure_time_mode: "GOATSGmosSouthLongSlitExposureTimeMode" = Field(
        alias="exposureTimeMode"
    )
    default_telescope_configs: "GOATSGmosSouthLongSlitDefaultTelescopeConfigs" = Field(
        alias="defaultTelescopeConfigs"
    )
    explicit_telescope_configs: Optional[
        "GOATSGmosSouthLongSlitExplicitTelescopeConfigs"
    ] = Field(alias="explicitTelescopeConfigs")


class GOATSGmosSouthLongSlitCentralWavelength(BaseModel):
    nanometers: Any


class GOATSGmosSouthLongSlitWavelengthDithers(BaseModel):
    nanometers: Any


class GOATSGmosSouthLongSlitExposureTimeMode(GOATSExposureTimeMode):
    pass


class GOATSGmosSouthLongSlitDefaultTelescopeConfigs(GOATSSlitTelescopeConfigs):
    pass


class GOATSGmosSouthLongSlitExplicitTelescopeConfigs(GOATSSlitTelescopeConfigs):
    pass


class GOATSImagingConfigOption(BaseModel):
    instrument: Instrument
    site: Site
    filter_label: Any = Field(alias="filterLabel")
    fov: "GOATSImagingConfigOptionFov"
    gmos_north: Optional["GOATSImagingConfigOptionGmosNorth"] = Field(alias="gmosNorth")
    gmos_south: Optional["GOATSImagingConfigOptionGmosSouth"] = Field(alias="gmosSouth")


class GOATSImagingConfigOptionFov(BaseModel):
    arcseconds: Any


class GOATSImagingConfigOptionGmosNorth(BaseModel):
    filter_: GmosNorthFilter = Field(alias="filter")


class GOATSImagingConfigOptionGmosSouth(BaseModel):
    filter_: GmosSouthFilter = Field(alias="filter")


class GOATSObservingMode(BaseModel):
    instrument: Optional[Instrument]
    mode: ObservingModeType
    gmos_north_long_slit: Optional["GOATSObservingModeGmosNorthLongSlit"] = Field(
        alias="gmosNorthLongSlit"
    )
    gmos_south_long_slit: Optional["GOATSObservingModeGmosSouthLongSlit"] = Field(
        alias="gmosSouthLongSlit"
    )
    gmos_north_imaging: Optional["GOATSObservingModeGmosNorthImaging"] = Field(
        alias="gmosNorthImaging"
    )
    gmos_south_imaging: Optional["GOATSObservingModeGmosSouthImaging"] = Field(
        alias="gmosSouthImaging"
    )


class GOATSObservingModeGmosNorthLongSlit(GOATSGmosNorthLongSlit):
    pass


class GOATSObservingModeGmosSouthLongSlit(GOATSGmosSouthLongSlit):
    pass


class GOATSObservingModeGmosNorthImaging(GOATSGmosNorthImaging):
    pass


class GOATSObservingModeGmosSouthImaging(GOATSGmosSouthImaging):
    pass


class GOATSSchedulingConstraints(BaseModel):
    scheduling_mode: SchedulingMode = Field(alias="schedulingMode")
    too_activation: TooActivation = Field(alias="tooActivation")
    timing_windows: list["GOATSSchedulingConstraintsTimingWindows"] = Field(
        alias="timingWindows"
    )


class GOATSSchedulingConstraintsTimingWindows(BaseModel):
    inclusion: TimingWindowInclusion
    start_utc: Any = Field(alias="startUtc")
    end: Optional[
        Annotated[
            Union[
                "GOATSSchedulingConstraintsTimingWindowsEndTimingWindowEndAt",
                "GOATSSchedulingConstraintsTimingWindowsEndTimingWindowEndAfter",
            ],
            Field(discriminator="typename__"),
        ]
    ]


class GOATSSchedulingConstraintsTimingWindowsEndTimingWindowEndAt(BaseModel):
    typename__: Literal["TimingWindowEndAt"] = Field(alias="__typename")
    at_utc: Any = Field(alias="atUtc")


class GOATSSchedulingConstraintsTimingWindowsEndTimingWindowEndAfter(BaseModel):
    typename__: Literal["TimingWindowEndAfter"] = Field(alias="__typename")
    after: "GOATSSchedulingConstraintsTimingWindowsEndTimingWindowEndAfterAfter"
    repeat: Optional[
        "GOATSSchedulingConstraintsTimingWindowsEndTimingWindowEndAfterRepeat"
    ]


class GOATSSchedulingConstraintsTimingWindowsEndTimingWindowEndAfterAfter(BaseModel):
    seconds: Any


class GOATSSchedulingConstraintsTimingWindowsEndTimingWindowEndAfterRepeat(BaseModel):
    period: "GOATSSchedulingConstraintsTimingWindowsEndTimingWindowEndAfterRepeatPeriod"
    times: Optional[Any]


class GOATSSchedulingConstraintsTimingWindowsEndTimingWindowEndAfterRepeatPeriod(
    BaseModel
):
    seconds: Any


class GOATSTarget(BaseModel):
    id: Any
    name: Any
    opportunity: Optional["GOATSTargetOpportunity"]
    sidereal: Optional["GOATSTargetSidereal"]
    source_profile: "GOATSTargetSourceProfile" = Field(alias="sourceProfile")


class GOATSTargetOpportunity(BaseModel):
    typename__: Literal["Opportunity"] = Field(alias="__typename")


class GOATSTargetSidereal(BaseModel):
    ra: "GOATSTargetSiderealRa"
    dec: "GOATSTargetSiderealDec"
    proper_motion: Optional["GOATSTargetSiderealProperMotion"] = Field(
        alias="properMotion"
    )
    parallax: Optional["GOATSTargetSiderealParallax"]
    radial_velocity: Optional["GOATSTargetSiderealRadialVelocity"] = Field(
        alias="radialVelocity"
    )


class GOATSTargetSiderealRa(BaseModel):
    hms: Any
    hours: Any
    degrees: Any


class GOATSTargetSiderealDec(BaseModel):
    dms: Any
    degrees: Any


class GOATSTargetSiderealProperMotion(BaseModel):
    ra: "GOATSTargetSiderealProperMotionRa"
    dec: "GOATSTargetSiderealProperMotionDec"


class GOATSTargetSiderealProperMotionRa(BaseModel):
    milliarcseconds_per_year: Any = Field(alias="milliarcsecondsPerYear")


class GOATSTargetSiderealProperMotionDec(BaseModel):
    milliarcseconds_per_year: Any = Field(alias="milliarcsecondsPerYear")


class GOATSTargetSiderealParallax(BaseModel):
    milliarcseconds: Any


class GOATSTargetSiderealRadialVelocity(BaseModel):
    kilometers_per_second: Any = Field(alias="kilometersPerSecond")


class GOATSTargetSourceProfile(BaseModel):
    point: Optional["GOATSTargetSourceProfilePoint"]


class GOATSTargetSourceProfilePoint(BaseModel):
    band_normalized: Optional["GOATSTargetSourceProfilePointBandNormalized"] = Field(
        alias="bandNormalized"
    )


class GOATSTargetSourceProfilePointBandNormalized(BaseModel):
    brightnesses: list["GOATSTargetSourceProfilePointBandNormalizedBrightnesses"]
    sed: Optional["GOATSTargetSourceProfilePointBandNormalizedSed"]


class GOATSTargetSourceProfilePointBandNormalizedBrightnesses(BaseModel):
    band: Band
    value: Any
    units: BrightnessIntegratedUnits


class GOATSTargetSourceProfilePointBandNormalizedSed(BaseModel):
    black_body_temp_k: Optional[Any] = Field(alias="blackBodyTempK")
    cool_star: Optional[CoolStarTemperature] = Field(alias="coolStar")
    flux_densities: Optional[
        list["GOATSTargetSourceProfilePointBandNormalizedSedFluxDensities"]
    ] = Field(alias="fluxDensities")
    flux_densities_attachment: Optional[Any] = Field(alias="fluxDensitiesAttachment")
    galaxy: Optional[GalaxySpectrum]
    hii_region: Optional[HiiRegionSpectrum] = Field(alias="hiiRegion")
    planet: Optional[PlanetSpectrum]
    planetary_nebula: Optional[PlanetaryNebulaSpectrum] = Field(alias="planetaryNebula")
    power_law: Optional[Any] = Field(alias="powerLaw")
    quasar: Optional[QuasarSpectrum]
    stellar_library: Optional[StellarLibrarySpectrum] = Field(alias="stellarLibrary")


class GOATSTargetSourceProfilePointBandNormalizedSedFluxDensities(BaseModel):
    wavelength: "GOATSTargetSourceProfilePointBandNormalizedSedFluxDensitiesWavelength"
    density: Any


class GOATSTargetSourceProfilePointBandNormalizedSedFluxDensitiesWavelength(BaseModel):
    nanometers: Any


class GOATSObservation(BaseModel):
    id: Any
    reference: Optional["GOATSObservationReference"]
    instrument: Optional[Instrument]
    calibration_role: Optional[CalibrationRole] = Field(alias="calibrationRole")
    configuration_requests: list["GOATSObservationConfigurationRequests"] = Field(
        alias="configurationRequests"
    )
    title: Any
    subtitle: Optional[Any]
    constraint_set: "GOATSObservationConstraintSet" = Field(alias="constraintSet")
    workflow: Optional["GOATSObservationWorkflow"]
    attachments: list["GOATSObservationAttachments"]
    target_environment: "GOATSObservationTargetEnvironment" = Field(
        alias="targetEnvironment"
    )
    pos_angle_constraint: "GOATSObservationPosAngleConstraint" = Field(
        alias="posAngleConstraint"
    )
    science_band: Optional[ScienceBand] = Field(alias="scienceBand")
    observation_duration: Optional["GOATSObservationObservationDuration"] = Field(
        alias="observationDuration"
    )
    observer_notes: Optional[Any] = Field(alias="observerNotes")
    science_requirements: "GOATSObservationScienceRequirements" = Field(
        alias="scienceRequirements"
    )
    observing_mode: Optional["GOATSObservationObservingMode"] = Field(
        alias="observingMode"
    )
    program: "GOATSObservationProgram"
    scheduling_constraints: "GOATSObservationSchedulingConstraints" = Field(
        alias="schedulingConstraints"
    )
    priority: ObservationPriority


class GOATSObservationReference(BaseModel):
    label: Any


class GOATSObservationConfigurationRequests(BaseModel):
    id: Any


class GOATSObservationConstraintSet(GOATSConstraintSet):
    pass


class GOATSObservationWorkflow(BaseModel):
    calculation_state: CalculationState = Field(alias="calculationState")
    value: "GOATSObservationWorkflowValue"


class GOATSObservationWorkflowValue(BaseModel):
    state: ObservationWorkflowState
    valid_transitions: list[ObservationWorkflowState] = Field(alias="validTransitions")
    validation_errors: list["GOATSObservationWorkflowValueValidationErrors"] = Field(
        alias="validationErrors"
    )


class GOATSObservationWorkflowValueValidationErrors(BaseModel):
    code: ObservationValidationCode


class GOATSObservationAttachments(BaseModel):
    id: Any
    attachment_type: AttachmentType = Field(alias="attachmentType")
    file_name: Any = Field(alias="fileName")
    description: Optional[Any]
    updated_at: Any = Field(alias="updatedAt")


class GOATSObservationTargetEnvironment(BaseModel):
    asterism: list["GOATSObservationTargetEnvironmentAsterism"]
    first_science_target: Optional[
        "GOATSObservationTargetEnvironmentFirstScienceTarget"
    ] = Field(alias="firstScienceTarget")


class GOATSObservationTargetEnvironmentAsterism(BaseModel):
    id: Any
    name: Any
    opportunity: Optional["GOATSObservationTargetEnvironmentAsterismOpportunity"]


class GOATSObservationTargetEnvironmentAsterismOpportunity(BaseModel):
    typename__: Literal["Opportunity"] = Field(alias="__typename")


class GOATSObservationTargetEnvironmentFirstScienceTarget(GOATSTarget):
    pass


class GOATSObservationPosAngleConstraint(BaseModel):
    mode: PosAngleConstraintMode
    angle: "GOATSObservationPosAngleConstraintAngle"


class GOATSObservationPosAngleConstraintAngle(BaseModel):
    degrees: Any


class GOATSObservationObservationDuration(BaseModel):
    seconds: Any
    minutes: Any
    hours: Any
    iso: str


class GOATSObservationScienceRequirements(BaseModel):
    mode: Optional[ScienceMode]
    spectroscopy: Optional["GOATSObservationScienceRequirementsSpectroscopy"]
    exposure_time_mode: Optional[
        "GOATSObservationScienceRequirementsExposureTimeMode"
    ] = Field(alias="exposureTimeMode")


class GOATSObservationScienceRequirementsSpectroscopy(BaseModel):
    wavelength: Optional["GOATSObservationScienceRequirementsSpectroscopyWavelength"]


class GOATSObservationScienceRequirementsSpectroscopyWavelength(BaseModel):
    nanometers: Any


class GOATSObservationScienceRequirementsExposureTimeMode(GOATSExposureTimeMode):
    pass


class GOATSObservationObservingMode(GOATSObservingMode):
    pass


class GOATSObservationProgram(BaseModel):
    allocations: list["GOATSObservationProgramAllocations"]
    time_charge: list["GOATSObservationProgramTimeCharge"] = Field(alias="timeCharge")


class GOATSObservationProgramAllocations(BaseModel):
    science_band: ScienceBand = Field(alias="scienceBand")
    duration: "GOATSObservationProgramAllocationsDuration"


class GOATSObservationProgramAllocationsDuration(BaseModel):
    hours: Any


class GOATSObservationProgramTimeCharge(BaseModel):
    band: Optional[ScienceBand]
    time: "GOATSObservationProgramTimeChargeTime"


class GOATSObservationProgramTimeChargeTime(BaseModel):
    program: "GOATSObservationProgramTimeChargeTimeProgram"


class GOATSObservationProgramTimeChargeTimeProgram(BaseModel):
    hours: Any


class GOATSObservationSchedulingConstraints(GOATSSchedulingConstraints):
    pass


class GOATSProgram(BaseModel):
    id: Any
    name: Optional[Any]
    description: Optional[Any]
    reference: Optional["GOATSProgramReference"]
    proposal_status: ProposalStatus = Field(alias="proposalStatus")
    type_: ProgramType = Field(alias="type")
    too_activation_ceiling: Optional[TooActivation] = Field(
        alias="tooActivationCeiling"
    )


class GOATSProgramReference(BaseModel):
    typename__: Literal[
        "CalibrationProgramReference",
        "CommissioningProgramReference",
        "EngineeringProgramReference",
        "ExampleProgramReference",
        "KeckProgramReference",
        "LibraryProgramReference",
        "MonitoringProgramReference",
        "ProgramReference",
        "ScienceProgramReference",
        "SubaruProgramReference",
        "SystemProgramReference",
    ] = Field(alias="__typename")
    label: Any


class GOATSSpectroscopyConfigOption(BaseModel):
    name: Any
    instrument: Instrument
    site: Site
    focal_plane: FocalPlane = Field(alias="focalPlane")
    fpu_label: Any = Field(alias="fpuLabel")
    disperser_label: Any = Field(alias="disperserLabel")
    filter_label: Optional[Any] = Field(alias="filterLabel")
    slit_width: "GOATSSpectroscopyConfigOptionSlitWidth" = Field(alias="slitWidth")
    resolution: Any
    wavelength_min: "GOATSSpectroscopyConfigOptionWavelengthMin" = Field(
        alias="wavelengthMin"
    )
    wavelength_max: "GOATSSpectroscopyConfigOptionWavelengthMax" = Field(
        alias="wavelengthMax"
    )
    wavelength_optimal: "GOATSSpectroscopyConfigOptionWavelengthOptimal" = Field(
        alias="wavelengthOptimal"
    )
    wavelength_coverage: "GOATSSpectroscopyConfigOptionWavelengthCoverage" = Field(
        alias="wavelengthCoverage"
    )
    gmos_north: Optional["GOATSSpectroscopyConfigOptionGmosNorth"] = Field(
        alias="gmosNorth"
    )
    gmos_south: Optional["GOATSSpectroscopyConfigOptionGmosSouth"] = Field(
        alias="gmosSouth"
    )


class GOATSSpectroscopyConfigOptionSlitWidth(BaseModel):
    arcseconds: Any


class GOATSSpectroscopyConfigOptionWavelengthMin(BaseModel):
    nanometers: Any


class GOATSSpectroscopyConfigOptionWavelengthMax(BaseModel):
    nanometers: Any


class GOATSSpectroscopyConfigOptionWavelengthOptimal(BaseModel):
    nanometers: Any


class GOATSSpectroscopyConfigOptionWavelengthCoverage(BaseModel):
    nanometers: Any


class GOATSSpectroscopyConfigOptionGmosNorth(BaseModel):
    fpu: Optional[GmosNorthBuiltinFpu]
    grating: GmosNorthGrating
    filter_: Optional[GmosNorthFilter] = Field(alias="filter")


class GOATSSpectroscopyConfigOptionGmosSouth(BaseModel):
    fpu: Optional[GmosSouthBuiltinFpu]
    grating: GmosSouthGrating
    filter_: Optional[GmosSouthFilter] = Field(alias="filter")


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
    x_bin: GmosBinning = Field(alias="xBin")
    y_bin: GmosBinning = Field(alias="yBin")


class GmosNorthLongSlitDetailsCentralWavelength(BaseModel):
    nanometers: Any


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
    x_bin: GmosBinning = Field(alias="xBin")
    y_bin: GmosBinning = Field(alias="yBin")


class GmosSouthLongSlitDetailsCentralWavelength(BaseModel):
    nanometers: Any


class GnirsImagingDetails(BaseModel):
    camera: GnirsCamera
    default_well_depth: GnirsWellDepth = Field(alias="defaultWellDepth")
    explicit_read_mode: Optional[GnirsReadMode] = Field(alias="explicitReadMode")
    explicit_well_depth: Optional[GnirsWellDepth] = Field(alias="explicitWellDepth")
    filters: list["GnirsImagingDetailsFilters"]
    initial_filters: list["GnirsImagingDetailsInitialFilters"] = Field(
        alias="initialFilters"
    )
    well_depth: GnirsWellDepth = Field(alias="wellDepth")


class GnirsImagingDetailsFilters(BaseModel):
    exposure_time_mode: "GnirsImagingDetailsFiltersExposureTimeMode" = Field(
        alias="exposureTimeMode"
    )
    filter_: GnirsFilter = Field(alias="filter")


class GnirsImagingDetailsFiltersExposureTimeMode(BaseModel):
    signal_to_noise: Optional[
        "GnirsImagingDetailsFiltersExposureTimeModeSignalToNoise"
    ] = Field(alias="signalToNoise")
    time_and_count: Optional[
        "GnirsImagingDetailsFiltersExposureTimeModeTimeAndCount"
    ] = Field(alias="timeAndCount")


class GnirsImagingDetailsFiltersExposureTimeModeSignalToNoise(BaseModel):
    at: "GnirsImagingDetailsFiltersExposureTimeModeSignalToNoiseAt"
    value: Any


class GnirsImagingDetailsFiltersExposureTimeModeSignalToNoiseAt(BaseModel):
    nanometers: Any


class GnirsImagingDetailsFiltersExposureTimeModeTimeAndCount(BaseModel):
    at: "GnirsImagingDetailsFiltersExposureTimeModeTimeAndCountAt"
    count: Any
    time: "GnirsImagingDetailsFiltersExposureTimeModeTimeAndCountTime"


class GnirsImagingDetailsFiltersExposureTimeModeTimeAndCountAt(BaseModel):
    nanometers: Any


class GnirsImagingDetailsFiltersExposureTimeModeTimeAndCountTime(BaseModel):
    seconds: Any


class GnirsImagingDetailsInitialFilters(BaseModel):
    exposure_time_mode: "GnirsImagingDetailsInitialFiltersExposureTimeMode" = Field(
        alias="exposureTimeMode"
    )
    filter_: GnirsFilter = Field(alias="filter")


class GnirsImagingDetailsInitialFiltersExposureTimeMode(BaseModel):
    signal_to_noise: Optional[
        "GnirsImagingDetailsInitialFiltersExposureTimeModeSignalToNoise"
    ] = Field(alias="signalToNoise")
    time_and_count: Optional[
        "GnirsImagingDetailsInitialFiltersExposureTimeModeTimeAndCount"
    ] = Field(alias="timeAndCount")


class GnirsImagingDetailsInitialFiltersExposureTimeModeSignalToNoise(BaseModel):
    at: "GnirsImagingDetailsInitialFiltersExposureTimeModeSignalToNoiseAt"
    value: Any


class GnirsImagingDetailsInitialFiltersExposureTimeModeSignalToNoiseAt(BaseModel):
    nanometers: Any


class GnirsImagingDetailsInitialFiltersExposureTimeModeTimeAndCount(BaseModel):
    at: "GnirsImagingDetailsInitialFiltersExposureTimeModeTimeAndCountAt"
    count: Any
    time: "GnirsImagingDetailsInitialFiltersExposureTimeModeTimeAndCountTime"


class GnirsImagingDetailsInitialFiltersExposureTimeModeTimeAndCountAt(BaseModel):
    nanometers: Any


class GnirsImagingDetailsInitialFiltersExposureTimeModeTimeAndCountTime(BaseModel):
    seconds: Any


class GnirsSpectroscopyDetails(BaseModel):
    acquisition: "GnirsSpectroscopyDetailsAcquisition"
    camera: GnirsCamera
    central_wavelengths: list["GnirsSpectroscopyDetailsCentralWavelengths"] = Field(
        alias="centralWavelengths"
    )
    decker: GnirsDecker
    default_decker: GnirsDecker = Field(alias="defaultDecker")
    default_well_depth: GnirsWellDepth = Field(alias="defaultWellDepth")
    explicit_decker: Optional[GnirsDecker] = Field(alias="explicitDecker")
    explicit_focus_motor_steps: Optional[int] = Field(alias="explicitFocusMotorSteps")
    explicit_grating: Optional[GnirsGrating] = Field(alias="explicitGrating")
    explicit_prism: Optional[GnirsPrism] = Field(alias="explicitPrism")
    explicit_read_mode: Optional[GnirsReadMode] = Field(alias="explicitReadMode")
    explicit_well_depth: Optional[GnirsWellDepth] = Field(alias="explicitWellDepth")
    filter_: GnirsFilter = Field(alias="filter")
    grating: GnirsGrating
    ifu: Optional["GnirsSpectroscopyDetailsIfu"]
    initial_camera: GnirsCamera = Field(alias="initialCamera")
    initial_filter: GnirsFilter = Field(alias="initialFilter")
    initial_grating: GnirsGrating = Field(alias="initialGrating")
    initial_prism: GnirsPrism = Field(alias="initialPrism")
    prism: GnirsPrism
    telluric_type: "GnirsSpectroscopyDetailsTelluricType" = Field(alias="telluricType")
    well_depth: GnirsWellDepth = Field(alias="wellDepth")
    slit: Optional["GnirsSpectroscopyDetailsSlit"]


class GnirsSpectroscopyDetailsAcquisition(BaseModel):
    explicit_acquisition_type: Optional[GnirsAcquisitionType] = Field(
        alias="explicitAcquisitionType"
    )
    explicit_filter: Optional[GnirsFilter] = Field(alias="explicitFilter")
    exposure_time_mode: "GnirsSpectroscopyDetailsAcquisitionExposureTimeMode" = Field(
        alias="exposureTimeMode"
    )
    sky_offset: Optional["GnirsSpectroscopyDetailsAcquisitionSkyOffset"] = Field(
        alias="skyOffset"
    )


class GnirsSpectroscopyDetailsAcquisitionExposureTimeMode(BaseModel):
    signal_to_noise: Optional[
        "GnirsSpectroscopyDetailsAcquisitionExposureTimeModeSignalToNoise"
    ] = Field(alias="signalToNoise")
    time_and_count: Optional[
        "GnirsSpectroscopyDetailsAcquisitionExposureTimeModeTimeAndCount"
    ] = Field(alias="timeAndCount")


class GnirsSpectroscopyDetailsAcquisitionExposureTimeModeSignalToNoise(BaseModel):
    at: "GnirsSpectroscopyDetailsAcquisitionExposureTimeModeSignalToNoiseAt"
    value: Any


class GnirsSpectroscopyDetailsAcquisitionExposureTimeModeSignalToNoiseAt(BaseModel):
    nanometers: Any


class GnirsSpectroscopyDetailsAcquisitionExposureTimeModeTimeAndCount(BaseModel):
    at: "GnirsSpectroscopyDetailsAcquisitionExposureTimeModeTimeAndCountAt"
    count: Any
    time: "GnirsSpectroscopyDetailsAcquisitionExposureTimeModeTimeAndCountTime"


class GnirsSpectroscopyDetailsAcquisitionExposureTimeModeTimeAndCountAt(BaseModel):
    nanometers: Any


class GnirsSpectroscopyDetailsAcquisitionExposureTimeModeTimeAndCountTime(BaseModel):
    seconds: Any


class GnirsSpectroscopyDetailsAcquisitionSkyOffset(BaseModel):
    p: "GnirsSpectroscopyDetailsAcquisitionSkyOffsetP"
    q: "GnirsSpectroscopyDetailsAcquisitionSkyOffsetQ"


class GnirsSpectroscopyDetailsAcquisitionSkyOffsetP(BaseModel):
    arcseconds: Any


class GnirsSpectroscopyDetailsAcquisitionSkyOffsetQ(BaseModel):
    arcseconds: Any


class GnirsSpectroscopyDetailsCentralWavelengths(BaseModel):
    central_wavelength: "GnirsSpectroscopyDetailsCentralWavelengthsCentralWavelength" = Field(
        alias="centralWavelength"
    )


class GnirsSpectroscopyDetailsCentralWavelengthsCentralWavelength(BaseModel):
    nanometers: Any


class GnirsSpectroscopyDetailsIfu(BaseModel):
    fpu: GnirsFpuIfu
    initial_fpu: GnirsFpuIfu = Field(alias="initialFpu")
    telescope_configs: list["GnirsSpectroscopyDetailsIfuTelescopeConfigs"] = Field(
        alias="telescopeConfigs"
    )


class GnirsSpectroscopyDetailsIfuTelescopeConfigs(BaseModel):
    guiding: GuideState
    offset: "GnirsSpectroscopyDetailsIfuTelescopeConfigsOffset"


class GnirsSpectroscopyDetailsIfuTelescopeConfigsOffset(BaseModel):
    p: "GnirsSpectroscopyDetailsIfuTelescopeConfigsOffsetP"
    q: "GnirsSpectroscopyDetailsIfuTelescopeConfigsOffsetQ"


class GnirsSpectroscopyDetailsIfuTelescopeConfigsOffsetP(BaseModel):
    arcseconds: Any


class GnirsSpectroscopyDetailsIfuTelescopeConfigsOffsetQ(BaseModel):
    arcseconds: Any


class GnirsSpectroscopyDetailsTelluricType(BaseModel):
    star_types: Optional[list[str]] = Field(alias="starTypes")
    tag: TelluricTag


class GnirsSpectroscopyDetailsSlit(BaseModel):
    fpu: GnirsFpuSlit
    initial_fpu: GnirsFpuSlit = Field(alias="initialFpu")
    default_telescope_configs: "GnirsSpectroscopyDetailsSlitDefaultTelescopeConfigs" = (
        Field(alias="defaultTelescopeConfigs")
    )
    explicit_telescope_configs: Optional[
        "GnirsSpectroscopyDetailsSlitExplicitTelescopeConfigs"
    ] = Field(alias="explicitTelescopeConfigs")
    telescope_configs: "GnirsSpectroscopyDetailsSlitTelescopeConfigs" = Field(
        alias="telescopeConfigs"
    )


class GnirsSpectroscopyDetailsSlitDefaultTelescopeConfigs(BaseModel):
    along_slit: Optional[
        list["GnirsSpectroscopyDetailsSlitDefaultTelescopeConfigsAlongSlit"]
    ] = Field(alias="alongSlit")
    offset_mode: SlitOffsetMode = Field(alias="offsetMode")
    to_sky: Optional[
        list["GnirsSpectroscopyDetailsSlitDefaultTelescopeConfigsToSky"]
    ] = Field(alias="toSky")


class GnirsSpectroscopyDetailsSlitDefaultTelescopeConfigsAlongSlit(BaseModel):
    guiding: GuideState
    q: "GnirsSpectroscopyDetailsSlitDefaultTelescopeConfigsAlongSlitQ"


class GnirsSpectroscopyDetailsSlitDefaultTelescopeConfigsAlongSlitQ(BaseModel):
    arcseconds: Any


class GnirsSpectroscopyDetailsSlitDefaultTelescopeConfigsToSky(BaseModel):
    guiding: GuideState
    offset: "GnirsSpectroscopyDetailsSlitDefaultTelescopeConfigsToSkyOffset"


class GnirsSpectroscopyDetailsSlitDefaultTelescopeConfigsToSkyOffset(BaseModel):
    p: "GnirsSpectroscopyDetailsSlitDefaultTelescopeConfigsToSkyOffsetP"
    q: "GnirsSpectroscopyDetailsSlitDefaultTelescopeConfigsToSkyOffsetQ"


class GnirsSpectroscopyDetailsSlitDefaultTelescopeConfigsToSkyOffsetP(BaseModel):
    arcseconds: Any


class GnirsSpectroscopyDetailsSlitDefaultTelescopeConfigsToSkyOffsetQ(BaseModel):
    arcseconds: Any


class GnirsSpectroscopyDetailsSlitExplicitTelescopeConfigs(BaseModel):
    along_slit: Optional[
        list["GnirsSpectroscopyDetailsSlitExplicitTelescopeConfigsAlongSlit"]
    ] = Field(alias="alongSlit")
    offset_mode: SlitOffsetMode = Field(alias="offsetMode")
    to_sky: Optional[
        list["GnirsSpectroscopyDetailsSlitExplicitTelescopeConfigsToSky"]
    ] = Field(alias="toSky")


class GnirsSpectroscopyDetailsSlitExplicitTelescopeConfigsAlongSlit(BaseModel):
    guiding: GuideState
    q: "GnirsSpectroscopyDetailsSlitExplicitTelescopeConfigsAlongSlitQ"


class GnirsSpectroscopyDetailsSlitExplicitTelescopeConfigsAlongSlitQ(BaseModel):
    arcseconds: Any


class GnirsSpectroscopyDetailsSlitExplicitTelescopeConfigsToSky(BaseModel):
    guiding: GuideState
    offset: "GnirsSpectroscopyDetailsSlitExplicitTelescopeConfigsToSkyOffset"


class GnirsSpectroscopyDetailsSlitExplicitTelescopeConfigsToSkyOffset(BaseModel):
    p: "GnirsSpectroscopyDetailsSlitExplicitTelescopeConfigsToSkyOffsetP"
    q: "GnirsSpectroscopyDetailsSlitExplicitTelescopeConfigsToSkyOffsetQ"


class GnirsSpectroscopyDetailsSlitExplicitTelescopeConfigsToSkyOffsetP(BaseModel):
    arcseconds: Any


class GnirsSpectroscopyDetailsSlitExplicitTelescopeConfigsToSkyOffsetQ(BaseModel):
    arcseconds: Any


class GnirsSpectroscopyDetailsSlitTelescopeConfigs(BaseModel):
    along_slit: Optional[
        list["GnirsSpectroscopyDetailsSlitTelescopeConfigsAlongSlit"]
    ] = Field(alias="alongSlit")
    offset_mode: SlitOffsetMode = Field(alias="offsetMode")
    to_sky: Optional[list["GnirsSpectroscopyDetailsSlitTelescopeConfigsToSky"]] = Field(
        alias="toSky"
    )


class GnirsSpectroscopyDetailsSlitTelescopeConfigsAlongSlit(BaseModel):
    guiding: GuideState
    q: "GnirsSpectroscopyDetailsSlitTelescopeConfigsAlongSlitQ"


class GnirsSpectroscopyDetailsSlitTelescopeConfigsAlongSlitQ(BaseModel):
    arcseconds: Any


class GnirsSpectroscopyDetailsSlitTelescopeConfigsToSky(BaseModel):
    guiding: GuideState
    offset: "GnirsSpectroscopyDetailsSlitTelescopeConfigsToSkyOffset"


class GnirsSpectroscopyDetailsSlitTelescopeConfigsToSkyOffset(BaseModel):
    p: "GnirsSpectroscopyDetailsSlitTelescopeConfigsToSkyOffsetP"
    q: "GnirsSpectroscopyDetailsSlitTelescopeConfigsToSkyOffsetQ"


class GnirsSpectroscopyDetailsSlitTelescopeConfigsToSkyOffsetP(BaseModel):
    arcseconds: Any


class GnirsSpectroscopyDetailsSlitTelescopeConfigsToSkyOffsetQ(BaseModel):
    arcseconds: Any


class Igrins2LongSlitDetails(BaseModel):
    exposure_time_mode: "Igrins2LongSlitDetailsExposureTimeMode" = Field(
        alias="exposureTimeMode"
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


class Igrins2LongSlitDetailsTelluricType(BaseModel):
    tag: TelluricTag
    star_types: Optional[list[str]] = Field(alias="starTypes")


class NonsiderealTargetDetails(BaseModel):
    des: str
    key_type: EphemerisKeyType = Field(alias="keyType")
    key: str


class ObservationAttachmentDetails(BaseModel):
    attachments: list["ObservationAttachmentDetailsAttachments"]


class ObservationAttachmentDetailsAttachments(BaseModel):
    id: Any
    file_name: Any = Field(alias="fileName")
    attachment_type: AttachmentType = Field(alias="attachmentType")
    mask: Optional["ObservationAttachmentDetailsAttachmentsMask"]


class ObservationAttachmentDetailsAttachmentsMask(BaseModel):
    name: Any
    instrument: Instrument
    pixel_scale: Any = Field(alias="pixelScale")
    dispersion_direction: MosDispersionDirection = Field(alias="dispersionDirection")
    science_slit_count: int = Field(alias="scienceSlitCount")
    acquisition_slit_count: int = Field(alias="acquisitionSlitCount")


class ObservationCore(BaseModel):
    id: Any
    existence: Existence
    reference: Optional["ObservationCoreReference"]
    title: Any
    instrument: Optional[Instrument]
    calibration_role: Optional[CalibrationRole] = Field(alias="calibrationRole")
    priority: ObservationPriority


class ObservationCoreReference(BaseModel):
    label: Any


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


class Flamingos2MosDetails(BaseModel):
    readout_mode: Flamingos2ReadoutMode = Field(alias="readoutMode")
    initial_slit_width: Flamingos2CustomSlitWidth = Field(alias="initialSlitWidth")
    initial_filter: Flamingos2Filter = Field(alias="initialFilter")
    initial_disperser: Flamingos2Disperser = Field(alias="initialDisperser")
    filter_: Flamingos2Filter = Field(alias="filter")
    explicit_reads: Optional[Flamingos2Reads] = Field(alias="explicitReads")
    explicit_readout_mode: Optional[Flamingos2ReadoutMode] = Field(
        alias="explicitReadoutMode"
    )
    explicit_read_mode: Optional[Flamingos2ReadMode] = Field(alias="explicitReadMode")
    explicit_decker: Optional[Flamingos2Decker] = Field(alias="explicitDecker")
    disperser: Flamingos2Disperser
    default_readout_mode: Flamingos2ReadoutMode = Field(alias="defaultReadoutMode")
    default_decker: Flamingos2Decker = Field(alias="defaultDecker")
    decker: Flamingos2Decker
    exposure_time_mode: "Flamingos2MosDetailsExposureTimeMode" = Field(
        alias="exposureTimeMode"
    )
    explicit_telescope_configs: Optional[
        "Flamingos2MosDetailsExplicitTelescopeConfigs"
    ] = Field(alias="explicitTelescopeConfigs")
    default_telescope_configs: "Flamingos2MosDetailsDefaultTelescopeConfigs" = Field(
        alias="defaultTelescopeConfigs"
    )
    telluric_type: "Flamingos2MosDetailsTelluricType" = Field(alias="telluricType")


class Flamingos2MosDetailsExposureTimeMode(BaseModel):
    time_and_count: Optional["Flamingos2MosDetailsExposureTimeModeTimeAndCount"] = (
        Field(alias="timeAndCount")
    )
    signal_to_noise: Optional["Flamingos2MosDetailsExposureTimeModeSignalToNoise"] = (
        Field(alias="signalToNoise")
    )


class Flamingos2MosDetailsExposureTimeModeTimeAndCount(BaseModel):
    at: "Flamingos2MosDetailsExposureTimeModeTimeAndCountAt"
    count: Any
    time: "Flamingos2MosDetailsExposureTimeModeTimeAndCountTime"


class Flamingos2MosDetailsExposureTimeModeTimeAndCountAt(BaseModel):
    nanometers: Any


class Flamingos2MosDetailsExposureTimeModeTimeAndCountTime(BaseModel):
    seconds: Any


class Flamingos2MosDetailsExposureTimeModeSignalToNoise(BaseModel):
    at: "Flamingos2MosDetailsExposureTimeModeSignalToNoiseAt"
    value: Any


class Flamingos2MosDetailsExposureTimeModeSignalToNoiseAt(BaseModel):
    nanometers: Any


class Flamingos2MosDetailsExplicitTelescopeConfigs(BaseModel):
    along_slit: Optional[
        list["Flamingos2MosDetailsExplicitTelescopeConfigsAlongSlit"]
    ] = Field(alias="alongSlit")
    offset_mode: SlitOffsetMode = Field(alias="offsetMode")
    to_sky: Optional[list["Flamingos2MosDetailsExplicitTelescopeConfigsToSky"]] = Field(
        alias="toSky"
    )


class Flamingos2MosDetailsExplicitTelescopeConfigsAlongSlit(BaseModel):
    guiding: GuideState
    q: "Flamingos2MosDetailsExplicitTelescopeConfigsAlongSlitQ"


class Flamingos2MosDetailsExplicitTelescopeConfigsAlongSlitQ(BaseModel):
    arcseconds: Any


class Flamingos2MosDetailsExplicitTelescopeConfigsToSky(BaseModel):
    guiding: GuideState
    offset: "Flamingos2MosDetailsExplicitTelescopeConfigsToSkyOffset"


class Flamingos2MosDetailsExplicitTelescopeConfigsToSkyOffset(BaseModel):
    p: "Flamingos2MosDetailsExplicitTelescopeConfigsToSkyOffsetP"
    q: "Flamingos2MosDetailsExplicitTelescopeConfigsToSkyOffsetQ"


class Flamingos2MosDetailsExplicitTelescopeConfigsToSkyOffsetP(BaseModel):
    arcseconds: Any


class Flamingos2MosDetailsExplicitTelescopeConfigsToSkyOffsetQ(BaseModel):
    arcseconds: Any


class Flamingos2MosDetailsDefaultTelescopeConfigs(BaseModel):
    along_slit: Optional[
        list["Flamingos2MosDetailsDefaultTelescopeConfigsAlongSlit"]
    ] = Field(alias="alongSlit")
    offset_mode: SlitOffsetMode = Field(alias="offsetMode")
    to_sky: Optional[list["Flamingos2MosDetailsDefaultTelescopeConfigsToSky"]] = Field(
        alias="toSky"
    )


class Flamingos2MosDetailsDefaultTelescopeConfigsAlongSlit(BaseModel):
    guiding: GuideState
    q: "Flamingos2MosDetailsDefaultTelescopeConfigsAlongSlitQ"


class Flamingos2MosDetailsDefaultTelescopeConfigsAlongSlitQ(BaseModel):
    arcseconds: Any


class Flamingos2MosDetailsDefaultTelescopeConfigsToSky(BaseModel):
    guiding: GuideState
    offset: "Flamingos2MosDetailsDefaultTelescopeConfigsToSkyOffset"


class Flamingos2MosDetailsDefaultTelescopeConfigsToSkyOffset(BaseModel):
    p: "Flamingos2MosDetailsDefaultTelescopeConfigsToSkyOffsetP"
    q: "Flamingos2MosDetailsDefaultTelescopeConfigsToSkyOffsetQ"


class Flamingos2MosDetailsDefaultTelescopeConfigsToSkyOffsetP(BaseModel):
    arcseconds: Any


class Flamingos2MosDetailsDefaultTelescopeConfigsToSkyOffsetQ(BaseModel):
    arcseconds: Any


class Flamingos2MosDetailsTelluricType(BaseModel):
    star_types: Optional[list[str]] = Field(alias="starTypes")
    tag: TelluricTag


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


class GmosNorthIfuDetails(BaseModel):
    y_bin: GmosBinning = Field(alias="yBin")
    x_bin: GmosBinning = Field(alias="xBin")
    roi: GmosRoi
    initial_grating: GmosNorthGrating = Field(alias="initialGrating")
    initial_fpu: GmosNorthIfuFpu = Field(alias="initialFpu")
    initial_filter: Optional[GmosNorthFilter] = Field(alias="initialFilter")
    grating: GmosNorthGrating
    fpu: GmosNorthIfuFpu
    filter_: Optional[GmosNorthFilter] = Field(alias="filter")
    explicit_y_bin: Optional[GmosBinning] = Field(alias="explicitYBin")
    explicit_x_bin: Optional[GmosBinning] = Field(alias="explicitXBin")
    explicit_roi: Optional[GmosRoi] = Field(alias="explicitRoi")
    amp_gain: GmosAmpGain = Field(alias="ampGain")
    amp_read_mode: GmosAmpReadMode = Field(alias="ampReadMode")
    default_amp_gain: GmosAmpGain = Field(alias="defaultAmpGain")
    default_amp_read_mode: GmosAmpReadMode = Field(alias="defaultAmpReadMode")
    default_roi: GmosRoi = Field(alias="defaultRoi")
    default_x_bin: GmosBinning = Field(alias="defaultXBin")
    default_y_bin: GmosBinning = Field(alias="defaultYBin")
    explicit_amp_gain: Optional[GmosAmpGain] = Field(alias="explicitAmpGain")
    explicit_amp_read_mode: Optional[GmosAmpReadMode] = Field(
        alias="explicitAmpReadMode"
    )
    central_wavelength: "GmosNorthIfuDetailsCentralWavelength" = Field(
        alias="centralWavelength"
    )
    acquisition: "GmosNorthIfuDetailsAcquisition"


class GmosNorthIfuDetailsCentralWavelength(BaseModel):
    nanometers: Any


class GmosNorthIfuDetailsAcquisition(BaseModel):
    exposure_time_mode: "GmosNorthIfuDetailsAcquisitionExposureTimeMode" = Field(
        alias="exposureTimeMode"
    )


class GmosNorthIfuDetailsAcquisitionExposureTimeMode(BaseModel):
    signal_to_noise: Optional[
        "GmosNorthIfuDetailsAcquisitionExposureTimeModeSignalToNoise"
    ] = Field(alias="signalToNoise")
    time_and_count: Optional[
        "GmosNorthIfuDetailsAcquisitionExposureTimeModeTimeAndCount"
    ] = Field(alias="timeAndCount")


class GmosNorthIfuDetailsAcquisitionExposureTimeModeSignalToNoise(BaseModel):
    at: "GmosNorthIfuDetailsAcquisitionExposureTimeModeSignalToNoiseAt"
    value: Any


class GmosNorthIfuDetailsAcquisitionExposureTimeModeSignalToNoiseAt(BaseModel):
    nanometers: Any


class GmosNorthIfuDetailsAcquisitionExposureTimeModeTimeAndCount(BaseModel):
    at: "GmosNorthIfuDetailsAcquisitionExposureTimeModeTimeAndCountAt"
    count: Any
    time: "GmosNorthIfuDetailsAcquisitionExposureTimeModeTimeAndCountTime"


class GmosNorthIfuDetailsAcquisitionExposureTimeModeTimeAndCountAt(BaseModel):
    nanometers: Any


class GmosNorthIfuDetailsAcquisitionExposureTimeModeTimeAndCountTime(BaseModel):
    seconds: Any


class GmosNorthMosDetails(BaseModel):
    acquisition: "GmosNorthMosDetailsAcquisition"
    acquisition_type: GmosMosAcquisitionType = Field(alias="acquisitionType")
    amp_gain: GmosAmpGain = Field(alias="ampGain")
    amp_read_mode: GmosAmpReadMode = Field(alias="ampReadMode")
    default_amp_gain: GmosAmpGain = Field(alias="defaultAmpGain")
    default_amp_read_mode: GmosAmpReadMode = Field(alias="defaultAmpReadMode")
    default_roi: GmosRoi = Field(alias="defaultRoi")
    default_x_bin: GmosBinning = Field(alias="defaultXBin")
    default_y_bin: GmosBinning = Field(alias="defaultYBin")
    explicit_amp_gain: Optional[GmosAmpGain] = Field(alias="explicitAmpGain")
    explicit_amp_read_mode: Optional[GmosAmpReadMode] = Field(
        alias="explicitAmpReadMode"
    )
    explicit_roi: Optional[GmosRoi] = Field(alias="explicitRoi")
    explicit_x_bin: Optional[GmosBinning] = Field(alias="explicitXBin")
    exposure_time_mode: "GmosNorthMosDetailsExposureTimeMode" = Field(
        alias="exposureTimeMode"
    )
    explicit_y_bin: Optional[GmosBinning] = Field(alias="explicitYBin")
    filter_: Optional[GmosNorthFilter] = Field(alias="filter")
    grating: GmosNorthGrating
    initial_filter: Optional[GmosNorthFilter] = Field(alias="initialFilter")
    initial_grating: GmosNorthGrating = Field(alias="initialGrating")
    initial_slit_width: GmosCustomSlitWidth = Field(alias="initialSlitWidth")
    roi: GmosRoi
    x_bin: GmosBinning = Field(alias="xBin")
    y_bin: GmosBinning = Field(alias="yBin")
    central_wavelength: "GmosNorthMosDetailsCentralWavelength" = Field(
        alias="centralWavelength"
    )
    custom_mask: "GmosNorthMosDetailsCustomMask" = Field(alias="customMask")


class GmosNorthMosDetailsAcquisition(BaseModel):
    filter_: GmosNorthFilter = Field(alias="filter")
    exposure_time_mode: "GmosNorthMosDetailsAcquisitionExposureTimeMode" = Field(
        alias="exposureTimeMode"
    )


class GmosNorthMosDetailsAcquisitionExposureTimeMode(BaseModel):
    signal_to_noise: Optional[
        "GmosNorthMosDetailsAcquisitionExposureTimeModeSignalToNoise"
    ] = Field(alias="signalToNoise")
    time_and_count: Optional[
        "GmosNorthMosDetailsAcquisitionExposureTimeModeTimeAndCount"
    ] = Field(alias="timeAndCount")


class GmosNorthMosDetailsAcquisitionExposureTimeModeSignalToNoise(BaseModel):
    at: "GmosNorthMosDetailsAcquisitionExposureTimeModeSignalToNoiseAt"
    value: Any


class GmosNorthMosDetailsAcquisitionExposureTimeModeSignalToNoiseAt(BaseModel):
    nanometers: Any


class GmosNorthMosDetailsAcquisitionExposureTimeModeTimeAndCount(BaseModel):
    at: "GmosNorthMosDetailsAcquisitionExposureTimeModeTimeAndCountAt"
    count: Any
    time: "GmosNorthMosDetailsAcquisitionExposureTimeModeTimeAndCountTime"


class GmosNorthMosDetailsAcquisitionExposureTimeModeTimeAndCountAt(BaseModel):
    nanometers: Any


class GmosNorthMosDetailsAcquisitionExposureTimeModeTimeAndCountTime(BaseModel):
    seconds: Any


class GmosNorthMosDetailsExposureTimeMode(BaseModel):
    signal_to_noise: Optional["GmosNorthMosDetailsExposureTimeModeSignalToNoise"] = (
        Field(alias="signalToNoise")
    )
    time_and_count: Optional["GmosNorthMosDetailsExposureTimeModeTimeAndCount"] = Field(
        alias="timeAndCount"
    )


class GmosNorthMosDetailsExposureTimeModeSignalToNoise(BaseModel):
    at: "GmosNorthMosDetailsExposureTimeModeSignalToNoiseAt"
    value: Any


class GmosNorthMosDetailsExposureTimeModeSignalToNoiseAt(BaseModel):
    nanometers: Any


class GmosNorthMosDetailsExposureTimeModeTimeAndCount(BaseModel):
    at: "GmosNorthMosDetailsExposureTimeModeTimeAndCountAt"
    count: Any
    time: "GmosNorthMosDetailsExposureTimeModeTimeAndCountTime"


class GmosNorthMosDetailsExposureTimeModeTimeAndCountAt(BaseModel):
    nanometers: Any


class GmosNorthMosDetailsExposureTimeModeTimeAndCountTime(BaseModel):
    seconds: Any


class GmosNorthMosDetailsCentralWavelength(BaseModel):
    nanometers: Any


class GmosNorthMosDetailsCustomMask(BaseModel):
    attachment_id: Optional[Any] = Field(alias="attachmentId")
    slit_width: GmosCustomSlitWidth = Field(alias="slitWidth")


class GmosSouthIfuDetails(BaseModel):
    acquisition: "GmosSouthIfuDetailsAcquisition"
    amp_gain: GmosAmpGain = Field(alias="ampGain")
    amp_read_mode: GmosAmpReadMode = Field(alias="ampReadMode")
    default_amp_gain: GmosAmpGain = Field(alias="defaultAmpGain")
    default_amp_read_mode: GmosAmpReadMode = Field(alias="defaultAmpReadMode")
    default_roi: GmosRoi = Field(alias="defaultRoi")
    default_x_bin: GmosBinning = Field(alias="defaultXBin")
    default_y_bin: GmosBinning = Field(alias="defaultYBin")
    explicit_amp_gain: Optional[GmosAmpGain] = Field(alias="explicitAmpGain")
    explicit_amp_read_mode: Optional[GmosAmpReadMode] = Field(
        alias="explicitAmpReadMode"
    )
    explicit_roi: Optional[GmosRoi] = Field(alias="explicitRoi")
    explicit_x_bin: Optional[GmosBinning] = Field(alias="explicitXBin")
    explicit_y_bin: Optional[GmosBinning] = Field(alias="explicitYBin")
    exposure_time_mode: "GmosSouthIfuDetailsExposureTimeMode" = Field(
        alias="exposureTimeMode"
    )
    filter_: Optional[GmosSouthFilter] = Field(alias="filter")
    fpu: GmosSouthIfuFpu
    grating: GmosSouthGrating
    initial_fpu: GmosSouthIfuFpu = Field(alias="initialFpu")
    initial_filter: Optional[GmosSouthFilter] = Field(alias="initialFilter")
    initial_grating: GmosSouthGrating = Field(alias="initialGrating")
    x_bin: GmosBinning = Field(alias="xBin")
    y_bin: GmosBinning = Field(alias="yBin")


class GmosSouthIfuDetailsAcquisition(BaseModel):
    exposure_time_mode: "GmosSouthIfuDetailsAcquisitionExposureTimeMode" = Field(
        alias="exposureTimeMode"
    )


class GmosSouthIfuDetailsAcquisitionExposureTimeMode(BaseModel):
    signal_to_noise: Optional[
        "GmosSouthIfuDetailsAcquisitionExposureTimeModeSignalToNoise"
    ] = Field(alias="signalToNoise")
    time_and_count: Optional[
        "GmosSouthIfuDetailsAcquisitionExposureTimeModeTimeAndCount"
    ] = Field(alias="timeAndCount")


class GmosSouthIfuDetailsAcquisitionExposureTimeModeSignalToNoise(BaseModel):
    at: "GmosSouthIfuDetailsAcquisitionExposureTimeModeSignalToNoiseAt"
    value: Any


class GmosSouthIfuDetailsAcquisitionExposureTimeModeSignalToNoiseAt(BaseModel):
    nanometers: Any


class GmosSouthIfuDetailsAcquisitionExposureTimeModeTimeAndCount(BaseModel):
    at: "GmosSouthIfuDetailsAcquisitionExposureTimeModeTimeAndCountAt"
    count: Any
    time: "GmosSouthIfuDetailsAcquisitionExposureTimeModeTimeAndCountTime"


class GmosSouthIfuDetailsAcquisitionExposureTimeModeTimeAndCountAt(BaseModel):
    nanometers: Any


class GmosSouthIfuDetailsAcquisitionExposureTimeModeTimeAndCountTime(BaseModel):
    seconds: Any


class GmosSouthIfuDetailsExposureTimeMode(BaseModel):
    signal_to_noise: Optional["GmosSouthIfuDetailsExposureTimeModeSignalToNoise"] = (
        Field(alias="signalToNoise")
    )
    time_and_count: Optional["GmosSouthIfuDetailsExposureTimeModeTimeAndCount"] = Field(
        alias="timeAndCount"
    )


class GmosSouthIfuDetailsExposureTimeModeSignalToNoise(BaseModel):
    at: "GmosSouthIfuDetailsExposureTimeModeSignalToNoiseAt"
    value: Any


class GmosSouthIfuDetailsExposureTimeModeSignalToNoiseAt(BaseModel):
    nanometers: Any


class GmosSouthIfuDetailsExposureTimeModeTimeAndCount(BaseModel):
    count: Any
    at: "GmosSouthIfuDetailsExposureTimeModeTimeAndCountAt"
    time: "GmosSouthIfuDetailsExposureTimeModeTimeAndCountTime"


class GmosSouthIfuDetailsExposureTimeModeTimeAndCountAt(BaseModel):
    nanometers: Any


class GmosSouthIfuDetailsExposureTimeModeTimeAndCountTime(BaseModel):
    seconds: Any


class GmosSouthMosDetails(BaseModel):
    acquisition: "GmosSouthMosDetailsAcquisition"
    acquisition_type: GmosMosAcquisitionType = Field(alias="acquisitionType")
    amp_gain: GmosAmpGain = Field(alias="ampGain")
    amp_read_mode: GmosAmpReadMode = Field(alias="ampReadMode")
    default_amp_gain: GmosAmpGain = Field(alias="defaultAmpGain")
    default_amp_read_mode: GmosAmpReadMode = Field(alias="defaultAmpReadMode")
    default_roi: GmosRoi = Field(alias="defaultRoi")
    default_x_bin: GmosBinning = Field(alias="defaultXBin")
    default_y_bin: GmosBinning = Field(alias="defaultYBin")
    explicit_amp_gain: Optional[GmosAmpGain] = Field(alias="explicitAmpGain")
    explicit_amp_read_mode: Optional[GmosAmpReadMode] = Field(
        alias="explicitAmpReadMode"
    )
    explicit_roi: Optional[GmosRoi] = Field(alias="explicitRoi")
    explicit_x_bin: Optional[GmosBinning] = Field(alias="explicitXBin")
    exposure_time_mode: "GmosSouthMosDetailsExposureTimeMode" = Field(
        alias="exposureTimeMode"
    )
    explicit_y_bin: Optional[GmosBinning] = Field(alias="explicitYBin")
    filter_: Optional[GmosSouthFilter] = Field(alias="filter")
    grating: GmosSouthGrating
    initial_filter: Optional[GmosSouthFilter] = Field(alias="initialFilter")
    initial_grating: GmosSouthGrating = Field(alias="initialGrating")
    initial_slit_width: GmosCustomSlitWidth = Field(alias="initialSlitWidth")
    roi: GmosRoi
    x_bin: GmosBinning = Field(alias="xBin")
    y_bin: GmosBinning = Field(alias="yBin")
    custom_mask: "GmosSouthMosDetailsCustomMask" = Field(alias="customMask")


class GmosSouthMosDetailsAcquisition(BaseModel):
    filter_: GmosSouthFilter = Field(alias="filter")
    exposure_time_mode: "GmosSouthMosDetailsAcquisitionExposureTimeMode" = Field(
        alias="exposureTimeMode"
    )


class GmosSouthMosDetailsAcquisitionExposureTimeMode(BaseModel):
    signal_to_noise: Optional[
        "GmosSouthMosDetailsAcquisitionExposureTimeModeSignalToNoise"
    ] = Field(alias="signalToNoise")
    time_and_count: Optional[
        "GmosSouthMosDetailsAcquisitionExposureTimeModeTimeAndCount"
    ] = Field(alias="timeAndCount")


class GmosSouthMosDetailsAcquisitionExposureTimeModeSignalToNoise(BaseModel):
    at: "GmosSouthMosDetailsAcquisitionExposureTimeModeSignalToNoiseAt"
    value: Any


class GmosSouthMosDetailsAcquisitionExposureTimeModeSignalToNoiseAt(BaseModel):
    nanometers: Any


class GmosSouthMosDetailsAcquisitionExposureTimeModeTimeAndCount(BaseModel):
    at: "GmosSouthMosDetailsAcquisitionExposureTimeModeTimeAndCountAt"
    count: Any
    time: "GmosSouthMosDetailsAcquisitionExposureTimeModeTimeAndCountTime"


class GmosSouthMosDetailsAcquisitionExposureTimeModeTimeAndCountAt(BaseModel):
    nanometers: Any


class GmosSouthMosDetailsAcquisitionExposureTimeModeTimeAndCountTime(BaseModel):
    seconds: Any


class GmosSouthMosDetailsExposureTimeMode(BaseModel):
    signal_to_noise: Optional["GmosSouthMosDetailsExposureTimeModeSignalToNoise"] = (
        Field(alias="signalToNoise")
    )
    time_and_count: Optional["GmosSouthMosDetailsExposureTimeModeTimeAndCount"] = Field(
        alias="timeAndCount"
    )


class GmosSouthMosDetailsExposureTimeModeSignalToNoise(BaseModel):
    at: "GmosSouthMosDetailsExposureTimeModeSignalToNoiseAt"
    value: Any


class GmosSouthMosDetailsExposureTimeModeSignalToNoiseAt(BaseModel):
    nanometers: Any


class GmosSouthMosDetailsExposureTimeModeTimeAndCount(BaseModel):
    at: "GmosSouthMosDetailsExposureTimeModeTimeAndCountAt"
    count: Any
    time: "GmosSouthMosDetailsExposureTimeModeTimeAndCountTime"


class GmosSouthMosDetailsExposureTimeModeTimeAndCountAt(BaseModel):
    nanometers: Any


class GmosSouthMosDetailsExposureTimeModeTimeAndCountTime(BaseModel):
    seconds: Any


class GmosSouthMosDetailsCustomMask(BaseModel):
    attachment_id: Optional[Any] = Field(alias="attachmentId")
    slit_width: GmosCustomSlitWidth = Field(alias="slitWidth")


class ObservingModeDetails(BaseModel):
    instrument: Optional[Instrument]
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
    flamingos_2_imaging: Optional["ObservingModeDetailsFlamingos2Imaging"] = Field(
        alias="flamingos2Imaging"
    )
    igrins_2_long_slit: Optional["ObservingModeDetailsIgrins2LongSlit"] = Field(
        alias="igrins2LongSlit"
    )
    visitor: Optional["ObservingModeDetailsVisitor"]
    ghost_ifu: Optional["ObservingModeDetailsGhostIfu"] = Field(alias="ghostIfu")
    gnirs_spectroscopy: Optional["ObservingModeDetailsGnirsSpectroscopy"] = Field(
        alias="gnirsSpectroscopy"
    )
    gnirs_imaging: Optional["ObservingModeDetailsGnirsImaging"] = Field(
        alias="gnirsImaging"
    )
    gmos_south_mos: Optional["ObservingModeDetailsGmosSouthMos"] = Field(
        alias="gmosSouthMos"
    )
    gmos_south_ifu: Optional["ObservingModeDetailsGmosSouthIfu"] = Field(
        alias="gmosSouthIfu"
    )
    gmos_north_mos: Optional["ObservingModeDetailsGmosNorthMos"] = Field(
        alias="gmosNorthMos"
    )
    gmos_north_ifu: Optional["ObservingModeDetailsGmosNorthIfu"] = Field(
        alias="gmosNorthIfu"
    )
    flamingos_2_mos: Optional["ObservingModeDetailsFlamingos2Mos"] = Field(
        alias="flamingos2Mos"
    )


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


class ObservingModeDetailsFlamingos2Imaging(Flamingos2ImagingDetails):
    pass


class ObservingModeDetailsIgrins2LongSlit(Igrins2LongSlitDetails):
    pass


class ObservingModeDetailsVisitor(VisitorDetails):
    pass


class ObservingModeDetailsGhostIfu(GhostIfuDetails):
    pass


class ObservingModeDetailsGnirsSpectroscopy(GnirsSpectroscopyDetails):
    pass


class ObservingModeDetailsGnirsImaging(GnirsImagingDetails):
    pass


class ObservingModeDetailsGmosSouthMos(GmosSouthMosDetails):
    pass


class ObservingModeDetailsGmosSouthIfu(GmosSouthIfuDetails):
    pass


class ObservingModeDetailsGmosNorthMos(GmosNorthMosDetails):
    pass


class ObservingModeDetailsGmosNorthIfu(GmosNorthIfuDetails):
    pass


class ObservingModeDetailsFlamingos2Mos(Flamingos2MosDetails):
    pass


class ProgramCore(BaseModel):
    id: Any
    name: Optional[Any]
    existence: Existence
    description: Optional[Any]
    too_activation_ceiling: Optional[TooActivation] = Field(
        alias="tooActivationCeiling"
    )


class SchedulingConstraintsDetails(BaseModel):
    too_activation: TooActivation = Field(alias="tooActivation")
    scheduling_mode: SchedulingMode = Field(alias="schedulingMode")
    timing_windows: list["SchedulingConstraintsDetailsTimingWindows"] = Field(
        alias="timingWindows"
    )


class SchedulingConstraintsDetailsTimingWindows(BaseModel):
    inclusion: TimingWindowInclusion
    start_utc: Any = Field(alias="startUtc")
    end: Optional[
        Annotated[
            Union[
                "SchedulingConstraintsDetailsTimingWindowsEndTimingWindowEndAt",
                "SchedulingConstraintsDetailsTimingWindowsEndTimingWindowEndAfter",
            ],
            Field(discriminator="typename__"),
        ]
    ]


class SchedulingConstraintsDetailsTimingWindowsEndTimingWindowEndAt(BaseModel):
    typename__: Literal["TimingWindowEndAt"] = Field(alias="__typename")
    at_utc: Any = Field(alias="atUtc")


class SchedulingConstraintsDetailsTimingWindowsEndTimingWindowEndAfter(BaseModel):
    typename__: Literal["TimingWindowEndAfter"] = Field(alias="__typename")
    after: "SchedulingConstraintsDetailsTimingWindowsEndTimingWindowEndAfterAfter"
    repeat: Optional[
        "SchedulingConstraintsDetailsTimingWindowsEndTimingWindowEndAfterRepeat"
    ]


class SchedulingConstraintsDetailsTimingWindowsEndTimingWindowEndAfterAfter(BaseModel):
    seconds: Any


class SchedulingConstraintsDetailsTimingWindowsEndTimingWindowEndAfterRepeat(BaseModel):
    period: (
        "SchedulingConstraintsDetailsTimingWindowsEndTimingWindowEndAfterRepeatPeriod"
    )
    times: Optional[Any]


class SchedulingConstraintsDetailsTimingWindowsEndTimingWindowEndAfterRepeatPeriod(
    BaseModel
):
    seconds: Any


class ScienceRequirementsDetails(BaseModel):
    mode: Optional[ScienceMode]
    exposure_time_mode: Optional["ScienceRequirementsDetailsExposureTimeMode"] = Field(
        alias="exposureTimeMode"
    )


class ScienceRequirementsDetailsExposureTimeMode(BaseModel):
    signal_to_noise: Optional[
        "ScienceRequirementsDetailsExposureTimeModeSignalToNoise"
    ] = Field(alias="signalToNoise")
    time_and_count: Optional[
        "ScienceRequirementsDetailsExposureTimeModeTimeAndCount"
    ] = Field(alias="timeAndCount")


class ScienceRequirementsDetailsExposureTimeModeSignalToNoise(BaseModel):
    at: "ScienceRequirementsDetailsExposureTimeModeSignalToNoiseAt"


class ScienceRequirementsDetailsExposureTimeModeSignalToNoiseAt(BaseModel):
    nanometers: Any


class ScienceRequirementsDetailsExposureTimeModeTimeAndCount(BaseModel):
    at: "ScienceRequirementsDetailsExposureTimeModeTimeAndCountAt"
    count: Any
    time: "ScienceRequirementsDetailsExposureTimeModeTimeAndCountTime"


class ScienceRequirementsDetailsExposureTimeModeTimeAndCountAt(BaseModel):
    nanometers: Any


class ScienceRequirementsDetailsExposureTimeModeTimeAndCountTime(BaseModel):
    seconds: Any


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
    scheduling_constraints: "ObservationDetailsSchedulingConstraints" = Field(
        alias="schedulingConstraints"
    )
    execution: "ObservationDetailsExecution"
    attachments: list["ObservationDetailsAttachments"]


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


class ObservationDetailsSchedulingConstraints(SchedulingConstraintsDetails):
    pass


class ObservationDetailsExecution(BaseModel):
    digest: Optional["ObservationDetailsExecutionDigest"]


class ObservationDetailsExecutionDigest(BaseModel):
    value: Optional["ObservationDetailsExecutionDigestValue"]


class ObservationDetailsExecutionDigestValue(BaseModel):
    acquisition: Optional["ObservationDetailsExecutionDigestValueAcquisition"]
    setup: "ObservationDetailsExecutionDigestValueSetup"


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


class ObservationDetailsExecutionDigestValueSetup(BaseModel):
    full: "ObservationDetailsExecutionDigestValueSetupFull"
    reacquisition: "ObservationDetailsExecutionDigestValueSetupReacquisition"


class ObservationDetailsExecutionDigestValueSetupFull(BaseModel):
    seconds: Any


class ObservationDetailsExecutionDigestValueSetupReacquisition(BaseModel):
    seconds: Any


class ObservationDetailsAttachments(BaseModel):
    id: Any
    file_name: Any = Field(alias="fileName")
    attachment_type: AttachmentType = Field(alias="attachmentType")
    mask: Optional["ObservationDetailsAttachmentsMask"]


class ObservationDetailsAttachmentsMask(BaseModel):
    name: Any
    instrument: Instrument
    pixel_scale: Any = Field(alias="pixelScale")
    dispersion_direction: MosDispersionDirection = Field(alias="dispersionDirection")
    science_slit_count: int = Field(alias="scienceSlitCount")
    acquisition_slit_count: int = Field(alias="acquisitionSlitCount")


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
    gemini: Optional["ProgramDetailProposalGemini"]


class ProgramDetailProposalCall(BaseModel):
    semester: Any
    active: "ProgramDetailProposalCallActive"
    observatory: Observatory
    gemini: Optional["ProgramDetailProposalCallGemini"]
    keck: Optional["ProgramDetailProposalCallKeck"]
    subaru: Optional["ProgramDetailProposalCallSubaru"]


class ProgramDetailProposalCallActive(BaseModel):
    start: Any
    end: Any


class ProgramDetailProposalCallGemini(BaseModel):
    type_: GeminiCallForProposalsType = Field(alias="type")
    instruments: list[Instrument]


class ProgramDetailProposalCallKeck(BaseModel):
    instruments: list[KeckInstrument]


class ProgramDetailProposalCallSubaru(BaseModel):
    type_: SubaruCallForProposalsType = Field(alias="type")
    instruments: list[SubaruInstrument]


class ProgramDetailProposalGemini(BaseModel):
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
    semester: Any
    active: "SchedulerProposalCallActive"
    observatory: Observatory
    gemini: Optional["SchedulerProposalCallGemini"]
    keck: Optional["SchedulerProposalCallKeck"]
    subaru: Optional["SchedulerProposalCallSubaru"]


class SchedulerProposalCallActive(BaseModel):
    start: Any
    end: Any


class SchedulerProposalCallGemini(BaseModel):
    type_: GeminiCallForProposalsType = Field(alias="type")
    instruments: list[Instrument]


class SchedulerProposalCallKeck(BaseModel):
    instruments: list[KeckInstrument]


class SchedulerProposalCallSubaru(BaseModel):
    type_: SubaruCallForProposalsType = Field(alias="type")
    instruments: list[SubaruInstrument]


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
ConstraintSetDetails.model_rebuild()
Flamingos2ImagingDetails.model_rebuild()
Flamingos2LongSlitDetails.model_rebuild()
GOATSConfigurationTarget.model_rebuild()
GOATSConfigurationRequest.model_rebuild()
GOATSConstraintSet.model_rebuild()
GOATSExposureTimeMode.model_rebuild()
GOATSOffset.model_rebuild()
GOATSTelescopeConfig.model_rebuild()
GOATSTelescopeConfigGenerator.model_rebuild()
GOATSImagingVariant.model_rebuild()
GOATSGmosNorthImaging.model_rebuild()
GOATSSlitTelescopeConfigs.model_rebuild()
GOATSGmosNorthLongSlit.model_rebuild()
GOATSGmosSouthImaging.model_rebuild()
GOATSGmosSouthLongSlit.model_rebuild()
GOATSImagingConfigOption.model_rebuild()
GOATSObservingMode.model_rebuild()
GOATSSchedulingConstraints.model_rebuild()
GOATSTarget.model_rebuild()
GOATSObservation.model_rebuild()
GOATSProgram.model_rebuild()
GOATSSpectroscopyConfigOption.model_rebuild()
GmosNorthImagingDetails.model_rebuild()
GmosNorthLongSlitDetails.model_rebuild()
GmosSouthImagingDetails.model_rebuild()
GmosSouthLongSlitDetails.model_rebuild()
GnirsImagingDetails.model_rebuild()
GnirsSpectroscopyDetails.model_rebuild()
Igrins2LongSlitDetails.model_rebuild()
NonsiderealTargetDetails.model_rebuild()
ObservationAttachmentDetails.model_rebuild()
ObservationCore.model_rebuild()
VisitorDetails.model_rebuild()
Flamingos2MosDetails.model_rebuild()
GhostDetectorConfigDetails.model_rebuild()
GhostIfuDetails.model_rebuild()
GmosNorthIfuDetails.model_rebuild()
GmosNorthMosDetails.model_rebuild()
GmosSouthIfuDetails.model_rebuild()
GmosSouthMosDetails.model_rebuild()
ObservingModeDetails.model_rebuild()
ProgramCore.model_rebuild()
SchedulingConstraintsDetails.model_rebuild()
ScienceRequirementsDetails.model_rebuild()
SiderealTargetDetails.model_rebuild()
TargetEnvironmentDetails.model_rebuild()
TimingWindowDetails.model_rebuild()
WorkflowCore.model_rebuild()
WorkflowDetails.model_rebuild()
ObservationDetails.model_rebuild()
ObservationWorkflowCore.model_rebuild()
ObservationWorkflowDetails.model_rebuild()
OpportunityTargetDetails.model_rebuild()
ProgramDetail.model_rebuild()
ProgramGroupElements.model_rebuild()
SchedulerProposal.model_rebuild()
TargetCore.model_rebuild()
TargetDetails.model_rebuild()
TargetProgramSummary.model_rebuild()
