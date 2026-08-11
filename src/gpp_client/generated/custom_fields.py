from typing import Any, Optional, Union

from .base_operation import GraphQLField
from .custom_typing_fields import (
    AddConditionsEntryResultGraphQLField,
    AddDatasetEventResultGraphQLField,
    AddEventBatchResultGraphQLField,
    AddProgramUserResultGraphQLField,
    AddSequenceEventResultGraphQLField,
    AddSlewEventResultGraphQLField,
    AddStepEventResultGraphQLField,
    AddTimeChargeCorrectionResultGraphQLField,
    AirMassRangeGraphQLField,
    AllConfigChangeEstimatesGraphQLField,
    AllDetectorEstimatesGraphQLField,
    AllocationGraphQLField,
    AngleGraphQLField,
    ArchiveDuplicationGraphQLField,
    ArchiveMatchGraphQLField,
    AsterismGroupGraphQLField,
    AsterismGroupSelectResultGraphQLField,
    AtomEventGraphQLField,
    AtomRecordGraphQLField,
    AtomRecordSelectResultGraphQLField,
    AttachmentGraphQLField,
    BandBrightnessIntegratedGraphQLField,
    BandBrightnessSurfaceGraphQLField,
    BandedTimeGraphQLField,
    BandNormalizedGraphQLField,
    BandNormalizedIntegratedGraphQLField,
    BandNormalizedSurfaceGraphQLField,
    BasePositionGraphQLField,
    BiasGraphQLField,
    CalculatedBandedTimeGraphQLField,
    CalculatedCategorizedTimeRangeGraphQLField,
    CalculatedExecutionDigestGraphQLField,
    CalculatedObservationWorkflowGraphQLField,
    CalibrationProgramReferenceGraphQLField,
    CallForProposalsExchangePartnerGraphQLField,
    CallForProposalsGraphQLField,
    CallForProposalsPartnerGraphQLField,
    CallsForProposalsSelectResultGraphQLField,
    CatalogInfoGraphQLField,
    CategorizedTimeGraphQLField,
    CategorizedTimeRangeGraphQLField,
    ChangePrincipalInvestigatorResultGraphQLField,
    ChangeProgramUserRoleResultGraphQLField,
    ClassicalGraphQLField,
    CloneGroupResultGraphQLField,
    CloneObservationResultGraphQLField,
    CloneTargetResultGraphQLField,
    CommissioningProgramReferenceGraphQLField,
    ConditionsEntryGraphQLField,
    ConditionsExpectationGraphQLField,
    ConditionsIntuitionGraphQLField,
    ConditionsMeasurementGraphQLField,
    ConfigChangeEstimateGraphQLField,
    ConfigurationConditionsGraphQLField,
    ConfigurationFlamingos2LongSlitGraphQLField,
    ConfigurationGmosNorthImagingGraphQLField,
    ConfigurationGmosNorthLongSlitGraphQLField,
    ConfigurationGmosNorthMosGraphQLField,
    ConfigurationGmosSouthImagingGraphQLField,
    ConfigurationGmosSouthLongSlitGraphQLField,
    ConfigurationGmosSouthMosGraphQLField,
    ConfigurationGnirsIfuGraphQLField,
    ConfigurationGnirsLongSlitGraphQLField,
    ConfigurationGraphQLField,
    ConfigurationIgrins2LongSlitGraphQLField,
    ConfigurationObservingModeGraphQLField,
    ConfigurationRequestGraphQLField,
    ConfigurationRequestSelectResultGraphQLField,
    ConfigurationTargetGraphQLField,
    ConfigurationVisitorGraphQLField,
    ConstraintSetGraphQLField,
    ConstraintSetGroupGraphQLField,
    ConstraintSetGroupSelectResultGraphQLField,
    CoordinateLimitsGraphQLField,
    CoordinatesGraphQLField,
    CreateCallForProposalsResultGraphQLField,
    CreateGroupResultGraphQLField,
    CreateObservationResultGraphQLField,
    CreateProgramNoteResultGraphQLField,
    CreateProgramResultGraphQLField,
    CreateProposalResultGraphQLField,
    CreateTargetResultGraphQLField,
    CreateUserInvitationResultGraphQLField,
    DarkGraphQLField,
    DatasetChronicleEntryGraphQLField,
    DatasetChronicleEntrySelectResultGraphQLField,
    DatasetEstimateGraphQLField,
    DatasetEventGraphQLField,
    DatasetGraphQLField,
    DatasetReferenceGraphQLField,
    DatasetSelectResultGraphQLField,
    DateIntervalGraphQLField,
    DeclinationArcGraphQLField,
    DeclinationGraphQLField,
    DeclineTooTriggerResultGraphQLField,
    DeleteProgramUserResultGraphQLField,
    DeleteProposalResultGraphQLField,
    DeleteSequenceResultGraphQLField,
    DemoScienceGraphQLField,
    DetectorEstimateGraphQLField,
    DirectorsTimeGraphQLField,
    ElevationRangeGraphQLField,
    EmailGraphQLField,
    EmissionLineIntegratedGraphQLField,
    EmissionLinesIntegratedGraphQLField,
    EmissionLinesSurfaceGraphQLField,
    EmissionLineSurfaceGraphQLField,
    EngineeringProgramReferenceGraphQLField,
    EnumeratedTelescopeConfigGeneratorGraphQLField,
    ExampleProgramReferenceGraphQLField,
    ExchangeGraphQLField,
    ExecutionConfigGraphQLField,
    ExecutionDigestGraphQLField,
    ExecutionEventGraphQLField,
    ExecutionEventSelectResultGraphQLField,
    ExecutionGraphQLField,
    ExposureTimeModeGraphQLField,
    FastTurnaroundGraphQLField,
    Flamingos2AtomGraphQLField,
    Flamingos2CustomMaskGraphQLField,
    Flamingos2DynamicGraphQLField,
    Flamingos2ExecutionConfigGraphQLField,
    Flamingos2ExecutionSequenceGraphQLField,
    Flamingos2FpuMaskGraphQLField,
    Flamingos2ImagingFilterGraphQLField,
    Flamingos2ImagingGraphQLField,
    Flamingos2LongSlitAcquisitionGraphQLField,
    Flamingos2LongSlitGraphQLField,
    Flamingos2StaticGraphQLField,
    Flamingos2StepGraphQLField,
    FluxDensityContinuumIntegratedGraphQLField,
    FluxDensityContinuumSurfaceGraphQLField,
    FluxDensityEntryGraphQLField,
    GaussianSourceGraphQLField,
    GcalGraphQLField,
    GeminiCallPropertiesGraphQLField,
    GeminiProposalTypeGraphQLField,
    GhostAtomGraphQLField,
    GhostDetectorConfigGraphQLField,
    GhostDetectorGraphQLField,
    GhostDualTargetGraphQLField,
    GhostDynamicGraphQLField,
    GhostExecutionConfigGraphQLField,
    GhostExecutionSequenceGraphQLField,
    GhostIfuGraphQLField,
    GhostIfuMappingGraphQLField,
    GhostSingleTargetGraphQLField,
    GhostSkyPlusTargetGraphQLField,
    GhostStaticGraphQLField,
    GhostStepGraphQLField,
    GhostTargetPlusSkyGraphQLField,
    GmosCcdModeGraphQLField,
    GmosCustomMaskGraphQLField,
    GmosNodAndShuffleGraphQLField,
    GmosNorthAtomGraphQLField,
    GmosNorthDynamicGraphQLField,
    GmosNorthExecutionConfigGraphQLField,
    GmosNorthExecutionSequenceGraphQLField,
    GmosNorthFpuGraphQLField,
    GmosNorthGratingConfigGraphQLField,
    GmosNorthImagingFilterGraphQLField,
    GmosNorthImagingGraphQLField,
    GmosNorthLongSlitAcquisitionGraphQLField,
    GmosNorthLongSlitGraphQLField,
    GmosNorthMosAcquisitionGraphQLField,
    GmosNorthMosGraphQLField,
    GmosNorthStaticGraphQLField,
    GmosNorthStepGraphQLField,
    GmosSouthAtomGraphQLField,
    GmosSouthDynamicGraphQLField,
    GmosSouthExecutionConfigGraphQLField,
    GmosSouthExecutionSequenceGraphQLField,
    GmosSouthFpuGraphQLField,
    GmosSouthGratingConfigGraphQLField,
    GmosSouthImagingFilterGraphQLField,
    GmosSouthImagingGraphQLField,
    GmosSouthLongSlitAcquisitionGraphQLField,
    GmosSouthLongSlitGraphQLField,
    GmosSouthMosAcquisitionGraphQLField,
    GmosSouthMosGraphQLField,
    GmosSouthStaticGraphQLField,
    GmosSouthStepGraphQLField,
    GnirsAcquisitionMirrorOutGraphQLField,
    GnirsAtomGraphQLField,
    GnirsCentralWavelengthConfigGraphQLField,
    GnirsDynamicGraphQLField,
    GnirsExecutionConfigGraphQLField,
    GnirsExecutionSequenceGraphQLField,
    GnirsIfuGraphQLField,
    GnirsImagingAcquisitionGraphQLField,
    GnirsImagingFilterGraphQLField,
    GnirsImagingGraphQLField,
    GnirsSlitGraphQLField,
    GnirsSpectroscopyAcquisitionGraphQLField,
    GnirsSpectroscopyGraphQLField,
    GnirsStaticGraphQLField,
    GnirsStepGraphQLField,
    GoaPropertiesGraphQLField,
    GroupedImagingVariantGraphQLField,
    GroupElementGraphQLField,
    GroupGraphQLField,
    GuideAvailabilityPeriodGraphQLField,
    GuideEnvironmentGraphQLField,
    GuideTargetGraphQLField,
    HasExchangePartnerGraphQLField,
    HasGeminiPartnerGraphQLField,
    HasNonPartnerGraphQLField,
    HasUnspecifiedPartnerGraphQLField,
    HourAngleRangeGraphQLField,
    Igrins2AtomGraphQLField,
    Igrins2DynamicGraphQLField,
    Igrins2ExecutionConfigGraphQLField,
    Igrins2ExecutionSequenceGraphQLField,
    Igrins2LongSlitGraphQLField,
    Igrins2StaticGraphQLField,
    Igrins2StepGraphQLField,
    Igrins2SvcConfigGraphQLField,
    ImagingConfigOptionFlamingos2GraphQLField,
    ImagingConfigOptionGmosNorthGraphQLField,
    ImagingConfigOptionGmosSouthGraphQLField,
    ImagingConfigOptionGnirsGraphQLField,
    ImagingConfigOptionGraphQLField,
    ImagingScienceRequirementsGraphQLField,
    ImagingVariantGraphQLField,
    InterleavedImagingVariantGraphQLField,
    ItcFlamingos2ImagingGraphQLField,
    ItcFlamingos2ImagingResultSetGraphQLField,
    ItcGhostIfuGraphQLField,
    ItcGmosNorthImagingGraphQLField,
    ItcGmosNorthImagingResultSetGraphQLField,
    ItcGmosSouthImagingGraphQLField,
    ItcGmosSouthImagingResultSetGraphQLField,
    ItcGnirsImagingGraphQLField,
    ItcGnirsImagingResultSetGraphQLField,
    ItcGnirsSpectroscopyGraphQLField,
    ItcGnirsSpectroscopyResultSetGraphQLField,
    ItcGraphQLField,
    ItcIgrins2SpectroscopyGraphQLField,
    ItcResultGraphQLField,
    ItcResultSetGraphQLField,
    ItcSpectroscopyGraphQLField,
    KeckCallPropertiesGraphQLField,
    KeckProgramReferenceGraphQLField,
    KeckProposalTypeGraphQLField,
    LargeProgramGraphQLField,
    LibraryProgramReferenceGraphQLField,
    LineFluxIntegratedGraphQLField,
    LineFluxSurfaceGraphQLField,
    LinkUserResultGraphQLField,
    MonitoringProgramReferenceGraphQLField,
    NonsiderealGraphQLField,
    ObservationGraphQLField,
    ObservationReferenceGraphQLField,
    ObservationSelectResultGraphQLField,
    ObservationTimeEstimateGraphQLField,
    ObservationValidationGraphQLField,
    ObservationWorkflowGraphQLField,
    ObservingModeGraphQLField,
    ObservingModeGroupGraphQLField,
    ObservingModeGroupSelectResultGraphQLField,
    OffsetGraphQLField,
    OffsetPGraphQLField,
    OffsetQGraphQLField,
    OpportunityGraphQLField,
    ParallaxGraphQLField,
    PartnerLinkGraphQLField,
    PartnerSplitGraphQLField,
    PoorWeatherGraphQLField,
    PosAngleConstraintGraphQLField,
    PreImagingVariantGraphQLField,
    ProgramGraphQLField,
    ProgramNoteGraphQLField,
    ProgramNoteSelectResultGraphQLField,
    ProgramReferenceGraphQLField,
    ProgramSelectResultGraphQLField,
    ProgramUserGraphQLField,
    ProgramUserSelectResultGraphQLField,
    ProperMotionDeclinationGraphQLField,
    ProperMotionGraphQLField,
    ProperMotionRAGraphQLField,
    ProposalGraphQLField,
    ProposalReferenceGraphQLField,
    QueueGraphQLField,
    RadialVelocityGraphQLField,
    RandomTelescopeConfigGeneratorGraphQLField,
    RecordDatasetResultGraphQLField,
    RecordFlamingos2VisitResultGraphQLField,
    RecordGmosNorthVisitResultGraphQLField,
    RecordGmosSouthVisitResultGraphQLField,
    RecordIgrins2VisitResultGraphQLField,
    RecordVisitResultGraphQLField,
    RedeemUserInvitationResultGraphQLField,
    RefreshArchiveDuplicationResultGraphQLField,
    RegionGraphQLField,
    ReplaceFlamingos2SequenceResultGraphQLField,
    ReplaceGhostSequenceResultGraphQLField,
    ReplaceGmosNorthSequenceResultGraphQLField,
    ReplaceGmosSouthSequenceResultGraphQLField,
    ReplaceGnirsSequenceResultGraphQLField,
    ReplaceIgrins2SequenceResultGraphQLField,
    ResetAcquisitionResultGraphQLField,
    RevokeUserInvitationResultGraphQLField,
    RightAscensionArcGraphQLField,
    RightAscensionGraphQLField,
    SchedulingConstraintsGraphQLField,
    ScienceGraphQLField,
    ScienceProgramReferenceGraphQLField,
    ScienceRequirementsGraphQLField,
    SequenceDigestGraphQLField,
    SequenceEventGraphQLField,
    SetAllocationsResultGraphQLField,
    SetGuideTargetNameResultGraphQLField,
    SetProgramReferenceResultGraphQLField,
    SetProgramResourceLimitResultGraphQLField,
    SetProposalStatusResultGraphQLField,
    SetupTimeGraphQLField,
    SiderealGraphQLField,
    SignalToNoiseAtGraphQLField,
    SignalToNoiseExposureTimeModeGraphQLField,
    SiteCoordinateLimitsGraphQLField,
    SlewEventGraphQLField,
    SlitTelescopeConfigsGraphQLField,
    SmartGcalGraphQLField,
    SourceProfileGraphQLField,
    SpectralDefinitionIntegratedGraphQLField,
    SpectralDefinitionSurfaceGraphQLField,
    SpectroscopyConfigOptionFlamingos2GraphQLField,
    SpectroscopyConfigOptionGhostGraphQLField,
    SpectroscopyConfigOptionGmosNorthGraphQLField,
    SpectroscopyConfigOptionGmosSouthGraphQLField,
    SpectroscopyConfigOptionGnirsGraphQLField,
    SpectroscopyConfigOptionGraphQLField,
    SpectroscopyScienceRequirementsGraphQLField,
    SpiralTelescopeConfigGeneratorGraphQLField,
    StepConfigGraphQLField,
    StepEstimateGraphQLField,
    StepEventGraphQLField,
    StepRecordGraphQLField,
    StepRecordSelectResultGraphQLField,
    SubaruCallPropertiesGraphQLField,
    SubaruProgramReferenceGraphQLField,
    SubaruProposalTypeGraphQLField,
    SystemProgramReferenceGraphQLField,
    SystemVerificationGraphQLField,
    TargetEnvironmentGraphQLField,
    TargetGraphQLField,
    TargetGroupGraphQLField,
    TargetGroupSelectResultGraphQLField,
    TargetSelectResultGraphQLField,
    TelescopeConfigAlongSlitGraphQLField,
    TelescopeConfigGeneratorGraphQLField,
    TelescopeConfigGraphQLField,
    TelluricTypeGraphQLField,
    TimeAndCountExposureTimeModeGraphQLField,
    TimeChargeCorrectionGraphQLField,
    TimeChargeDaylightDiscountGraphQLField,
    TimeChargeDiscountGraphQLField,
    TimeChargeInvoiceGraphQLField,
    TimeChargeNoDataDiscountGraphQLField,
    TimeChargeOverlapDiscountGraphQLField,
    TimeChargeQaDiscountGraphQLField,
    TimeSpanGraphQLField,
    TimestampIntervalGraphQLField,
    TimingWindowEndAfterGraphQLField,
    TimingWindowEndAtGraphQLField,
    TimingWindowEndUnion,
    TimingWindowGraphQLField,
    TimingWindowRepeatGraphQLField,
    TooTriggerChronicleEntryGraphQLField,
    TooTriggerChronicleEntrySelectResultGraphQLField,
    TooTriggerGraphQLField,
    TooTriggerSelectResultGraphQLField,
    UniformTelescopeConfigGeneratorGraphQLField,
    UnlinkUserResultGraphQLField,
    UnnormalizedSedGraphQLField,
    UpdateAsterismsResultGraphQLField,
    UpdateAttachmentsResultGraphQLField,
    UpdateCallsForProposalsResultGraphQLField,
    UpdateConfigurationRequestsResultGraphQLField,
    UpdateDatasetsResultGraphQLField,
    UpdateGroupsResultGraphQLField,
    UpdateObservationsResultGraphQLField,
    UpdateProgramNotesResultGraphQLField,
    UpdateProgramsResultGraphQLField,
    UpdateProgramUsersResultGraphQLField,
    UpdateProposalResultGraphQLField,
    UpdateTargetsResultGraphQLField,
    UserGraphQLField,
    UserInvitationGraphQLField,
    UserProfileGraphQLField,
    VisitGraphQLField,
    VisitorGraphQLField,
    VisitSelectResultGraphQLField,
    WavelengthDitherGraphQLField,
    WavelengthGraphQLField,
)


class AddConditionsEntryResultFields(GraphQLField):
    @classmethod
    def conditions_entry(cls) -> "ConditionsEntryFields":
        return ConditionsEntryFields("conditionsEntry")

    def fields(
        self,
        *subfields: Union[
            AddConditionsEntryResultGraphQLField, "ConditionsEntryFields"
        ],
    ) -> "AddConditionsEntryResultFields":
        """Subfields should come from the AddConditionsEntryResultFields class"""
        self._subfields.extend(subfields)
        return self

    def alias(self, alias: str) -> "AddConditionsEntryResultFields":
        self._alias = alias
        return self


class AddDatasetEventResultFields(GraphQLField):
    @classmethod
    def event(cls) -> "DatasetEventFields":
        return DatasetEventFields("event")

    def fields(
        self, *subfields: Union[AddDatasetEventResultGraphQLField, "DatasetEventFields"]
    ) -> "AddDatasetEventResultFields":
        """Subfields should come from the AddDatasetEventResultFields class"""
        self._subfields.extend(subfields)
        return self

    def alias(self, alias: str) -> "AddDatasetEventResultFields":
        self._alias = alias
        return self


class AddEventBatchResultFields(GraphQLField):
    @classmethod
    def events(cls) -> "ExecutionEventInterface":
        return ExecutionEventInterface("events")

    has_more: "AddEventBatchResultGraphQLField" = AddEventBatchResultGraphQLField(
        "hasMore"
    )

    def fields(
        self,
        *subfields: Union[AddEventBatchResultGraphQLField, "ExecutionEventInterface"],
    ) -> "AddEventBatchResultFields":
        """Subfields should come from the AddEventBatchResultFields class"""
        self._subfields.extend(subfields)
        return self

    def alias(self, alias: str) -> "AddEventBatchResultFields":
        self._alias = alias
        return self


class AddProgramUserResultFields(GraphQLField):
    @classmethod
    def program_user(cls) -> "ProgramUserFields":
        return ProgramUserFields("programUser")

    def fields(
        self, *subfields: Union[AddProgramUserResultGraphQLField, "ProgramUserFields"]
    ) -> "AddProgramUserResultFields":
        """Subfields should come from the AddProgramUserResultFields class"""
        self._subfields.extend(subfields)
        return self

    def alias(self, alias: str) -> "AddProgramUserResultFields":
        self._alias = alias
        return self


class AddSequenceEventResultFields(GraphQLField):
    @classmethod
    def event(cls) -> "SequenceEventFields":
        return SequenceEventFields("event")

    def fields(
        self,
        *subfields: Union[AddSequenceEventResultGraphQLField, "SequenceEventFields"],
    ) -> "AddSequenceEventResultFields":
        """Subfields should come from the AddSequenceEventResultFields class"""
        self._subfields.extend(subfields)
        return self

    def alias(self, alias: str) -> "AddSequenceEventResultFields":
        self._alias = alias
        return self


class AddSlewEventResultFields(GraphQLField):
    @classmethod
    def event(cls) -> "SlewEventFields":
        return SlewEventFields("event")

    def fields(
        self, *subfields: Union[AddSlewEventResultGraphQLField, "SlewEventFields"]
    ) -> "AddSlewEventResultFields":
        """Subfields should come from the AddSlewEventResultFields class"""
        self._subfields.extend(subfields)
        return self

    def alias(self, alias: str) -> "AddSlewEventResultFields":
        self._alias = alias
        return self


class AddStepEventResultFields(GraphQLField):
    @classmethod
    def event(cls) -> "StepEventFields":
        return StepEventFields("event")

    def fields(
        self, *subfields: Union[AddStepEventResultGraphQLField, "StepEventFields"]
    ) -> "AddStepEventResultFields":
        """Subfields should come from the AddStepEventResultFields class"""
        self._subfields.extend(subfields)
        return self

    def alias(self, alias: str) -> "AddStepEventResultFields":
        self._alias = alias
        return self


class AddTimeChargeCorrectionResultFields(GraphQLField):
    @classmethod
    def time_charge_invoice(cls) -> "TimeChargeInvoiceFields":
        return TimeChargeInvoiceFields("timeChargeInvoice")

    def fields(
        self,
        *subfields: Union[
            AddTimeChargeCorrectionResultGraphQLField, "TimeChargeInvoiceFields"
        ],
    ) -> "AddTimeChargeCorrectionResultFields":
        """Subfields should come from the AddTimeChargeCorrectionResultFields class"""
        self._subfields.extend(subfields)
        return self

    def alias(self, alias: str) -> "AddTimeChargeCorrectionResultFields":
        self._alias = alias
        return self


class AirMassRangeFields(GraphQLField):
    min: "AirMassRangeGraphQLField" = AirMassRangeGraphQLField("min")
    max: "AirMassRangeGraphQLField" = AirMassRangeGraphQLField("max")

    def fields(self, *subfields: AirMassRangeGraphQLField) -> "AirMassRangeFields":
        """Subfields should come from the AirMassRangeFields class"""
        self._subfields.extend(subfields)
        return self

    def alias(self, alias: str) -> "AirMassRangeFields":
        self._alias = alias
        return self


class AllConfigChangeEstimatesFields(GraphQLField):
    @classmethod
    def selected(cls) -> "ConfigChangeEstimateFields":
        return ConfigChangeEstimateFields("selected")

    index: "AllConfigChangeEstimatesGraphQLField" = (
        AllConfigChangeEstimatesGraphQLField("index")
    )

    @classmethod
    def all(cls) -> "ConfigChangeEstimateFields":
        return ConfigChangeEstimateFields("all")

    @classmethod
    def estimate(cls) -> "TimeSpanFields":
        return TimeSpanFields("estimate")

    def fields(
        self,
        *subfields: Union[
            AllConfigChangeEstimatesGraphQLField,
            "ConfigChangeEstimateFields",
            "TimeSpanFields",
        ],
    ) -> "AllConfigChangeEstimatesFields":
        """Subfields should come from the AllConfigChangeEstimatesFields class"""
        self._subfields.extend(subfields)
        return self

    def alias(self, alias: str) -> "AllConfigChangeEstimatesFields":
        self._alias = alias
        return self


class AllDetectorEstimatesFields(GraphQLField):
    @classmethod
    def selected(cls) -> "DetectorEstimateFields":
        return DetectorEstimateFields("selected")

    index: "AllDetectorEstimatesGraphQLField" = AllDetectorEstimatesGraphQLField(
        "index"
    )

    @classmethod
    def all(cls) -> "DetectorEstimateFields":
        return DetectorEstimateFields("all")

    @classmethod
    def estimate(cls) -> "TimeSpanFields":
        return TimeSpanFields("estimate")

    def fields(
        self,
        *subfields: Union[
            AllDetectorEstimatesGraphQLField, "DetectorEstimateFields", "TimeSpanFields"
        ],
    ) -> "AllDetectorEstimatesFields":
        """Subfields should come from the AllDetectorEstimatesFields class"""
        self._subfields.extend(subfields)
        return self

    def alias(self, alias: str) -> "AllDetectorEstimatesFields":
        self._alias = alias
        return self


class AllocationFields(GraphQLField):
    category: "AllocationGraphQLField" = AllocationGraphQLField("category")
    science_band: "AllocationGraphQLField" = AllocationGraphQLField("scienceBand")

    @classmethod
    def duration(cls) -> "TimeSpanFields":
        return TimeSpanFields("duration")

    def fields(
        self, *subfields: Union[AllocationGraphQLField, "TimeSpanFields"]
    ) -> "AllocationFields":
        """Subfields should come from the AllocationFields class"""
        self._subfields.extend(subfields)
        return self

    def alias(self, alias: str) -> "AllocationFields":
        self._alias = alias
        return self


class AngleFields(GraphQLField):
    microarcseconds: "AngleGraphQLField" = AngleGraphQLField("microarcseconds")
    microseconds: "AngleGraphQLField" = AngleGraphQLField("microseconds")
    milliarcseconds: "AngleGraphQLField" = AngleGraphQLField("milliarcseconds")
    milliseconds: "AngleGraphQLField" = AngleGraphQLField("milliseconds")
    arcseconds: "AngleGraphQLField" = AngleGraphQLField("arcseconds")
    seconds: "AngleGraphQLField" = AngleGraphQLField("seconds")
    arcminutes: "AngleGraphQLField" = AngleGraphQLField("arcminutes")
    minutes: "AngleGraphQLField" = AngleGraphQLField("minutes")
    degrees: "AngleGraphQLField" = AngleGraphQLField("degrees")
    hours: "AngleGraphQLField" = AngleGraphQLField("hours")
    hms: "AngleGraphQLField" = AngleGraphQLField("hms")
    dms: "AngleGraphQLField" = AngleGraphQLField("dms")

    def fields(self, *subfields: AngleGraphQLField) -> "AngleFields":
        """Subfields should come from the AngleFields class"""
        self._subfields.extend(subfields)
        return self

    def alias(self, alias: str) -> "AngleFields":
        self._alias = alias
        return self


class ArchiveDuplicationFields(GraphQLField):
    state: "ArchiveDuplicationGraphQLField" = ArchiveDuplicationGraphQLField("state")
    match_count: "ArchiveDuplicationGraphQLField" = ArchiveDuplicationGraphQLField(
        "matchCount"
    )
    saturated: "ArchiveDuplicationGraphQLField" = ArchiveDuplicationGraphQLField(
        "saturated"
    )
    last_checked_at: "ArchiveDuplicationGraphQLField" = ArchiveDuplicationGraphQLField(
        "lastCheckedAt"
    )
    error: "ArchiveDuplicationGraphQLField" = ArchiveDuplicationGraphQLField("error")

    @classmethod
    def search_coordinates(cls) -> "CoordinatesFields":
        return CoordinatesFields("searchCoordinates")

    search_target_name: "ArchiveDuplicationGraphQLField" = (
        ArchiveDuplicationGraphQLField("searchTargetName")
    )

    @classmethod
    def search_radius(cls) -> "AngleFields":
        return AngleFields("searchRadius")

    query_urls: "ArchiveDuplicationGraphQLField" = ArchiveDuplicationGraphQLField(
        "queryUrls"
    )

    @classmethod
    def matches(cls) -> "ArchiveMatchFields":
        return ArchiveMatchFields("matches")

    def fields(
        self,
        *subfields: Union[
            ArchiveDuplicationGraphQLField,
            "AngleFields",
            "ArchiveMatchFields",
            "CoordinatesFields",
        ],
    ) -> "ArchiveDuplicationFields":
        """Subfields should come from the ArchiveDuplicationFields class"""
        self._subfields.extend(subfields)
        return self

    def alias(self, alias: str) -> "ArchiveDuplicationFields":
        self._alias = alias
        return self


class ArchiveMatchFields(GraphQLField):
    name: "ArchiveMatchGraphQLField" = ArchiveMatchGraphQLField("name")
    data_label: "ArchiveMatchGraphQLField" = ArchiveMatchGraphQLField("dataLabel")

    @classmethod
    def coordinates(cls) -> "CoordinatesFields":
        return CoordinatesFields("coordinates")

    instrument_string: "ArchiveMatchGraphQLField" = ArchiveMatchGraphQLField(
        "instrumentString"
    )
    instrument: "ArchiveMatchGraphQLField" = ArchiveMatchGraphQLField("instrument")
    observation_type: "ArchiveMatchGraphQLField" = ArchiveMatchGraphQLField(
        "observationType"
    )
    observe_class_string: "ArchiveMatchGraphQLField" = ArchiveMatchGraphQLField(
        "observeClassString"
    )
    observe_class: "ArchiveMatchGraphQLField" = ArchiveMatchGraphQLField("observeClass")
    qa_state_string: "ArchiveMatchGraphQLField" = ArchiveMatchGraphQLField(
        "qaStateString"
    )
    qa_state: "ArchiveMatchGraphQLField" = ArchiveMatchGraphQLField("qaState")
    ut_date_time: "ArchiveMatchGraphQLField" = ArchiveMatchGraphQLField("utDateTime")
    release_date: "ArchiveMatchGraphQLField" = ArchiveMatchGraphQLField("releaseDate")
    program_reference: "ArchiveMatchGraphQLField" = ArchiveMatchGraphQLField(
        "programReference"
    )
    observation_reference: "ArchiveMatchGraphQLField" = ArchiveMatchGraphQLField(
        "observationReference"
    )
    object_name: "ArchiveMatchGraphQLField" = ArchiveMatchGraphQLField("objectName")

    @classmethod
    def exposure(cls) -> "TimeSpanFields":
        return TimeSpanFields("exposure")

    disperser: "ArchiveMatchGraphQLField" = ArchiveMatchGraphQLField("disperser")
    filter_: "ArchiveMatchGraphQLField" = ArchiveMatchGraphQLField("filter")

    @classmethod
    def wavelength(cls) -> "WavelengthFields":
        return WavelengthFields("wavelength")

    airmass: "ArchiveMatchGraphQLField" = ArchiveMatchGraphQLField("airmass")

    @classmethod
    def azimuth(cls) -> "AngleFields":
        return AngleFields("azimuth")

    @classmethod
    def elevation(cls) -> "AngleFields":
        return AngleFields("elevation")

    @classmethod
    def distance(cls) -> "AngleFields":
        return AngleFields("distance")

    def fields(
        self,
        *subfields: Union[
            ArchiveMatchGraphQLField,
            "AngleFields",
            "CoordinatesFields",
            "TimeSpanFields",
            "WavelengthFields",
        ],
    ) -> "ArchiveMatchFields":
        """Subfields should come from the ArchiveMatchFields class"""
        self._subfields.extend(subfields)
        return self

    def alias(self, alias: str) -> "ArchiveMatchFields":
        self._alias = alias
        return self


class AsterismGroupFields(GraphQLField):
    @classmethod
    def program(cls) -> "ProgramFields":
        return ProgramFields("program")

    @classmethod
    def observations(
        cls,
        include_deleted: bool,
        *,
        offset: Optional[Any] = None,
        limit: Optional[Any] = None,
    ) -> "ObservationSelectResultFields":
        arguments: dict[str, dict[str, Any]] = {
            "includeDeleted": {"type": "Boolean!", "value": include_deleted},
            "OFFSET": {"type": "ObservationId", "value": offset},
            "LIMIT": {"type": "NonNegInt", "value": limit},
        }
        cleared_arguments = {
            key: value for key, value in arguments.items() if value["value"] is not None
        }
        return ObservationSelectResultFields(
            "observations", arguments=cleared_arguments
        )

    @classmethod
    def asterism(cls) -> "TargetFields":
        return TargetFields("asterism")

    def fields(
        self,
        *subfields: Union[
            AsterismGroupGraphQLField,
            "ObservationSelectResultFields",
            "ProgramFields",
            "TargetFields",
        ],
    ) -> "AsterismGroupFields":
        """Subfields should come from the AsterismGroupFields class"""
        self._subfields.extend(subfields)
        return self

    def alias(self, alias: str) -> "AsterismGroupFields":
        self._alias = alias
        return self


class AsterismGroupSelectResultFields(GraphQLField):
    @classmethod
    def matches(cls) -> "AsterismGroupFields":
        return AsterismGroupFields("matches")

    has_more: "AsterismGroupSelectResultGraphQLField" = (
        AsterismGroupSelectResultGraphQLField("hasMore")
    )

    def fields(
        self,
        *subfields: Union[AsterismGroupSelectResultGraphQLField, "AsterismGroupFields"],
    ) -> "AsterismGroupSelectResultFields":
        """Subfields should come from the AsterismGroupSelectResultFields class"""
        self._subfields.extend(subfields)
        return self

    def alias(self, alias: str) -> "AsterismGroupSelectResultFields":
        self._alias = alias
        return self


class AtomEventFields(GraphQLField):
    id: "AtomEventGraphQLField" = AtomEventGraphQLField("id")

    @classmethod
    def visit(cls) -> "VisitFields":
        return VisitFields("visit")

    @classmethod
    def observation(cls) -> "ObservationFields":
        return ObservationFields("observation")

    recorded_time: "AtomEventGraphQLField" = AtomEventGraphQLField("recordedTime")
    received: "AtomEventGraphQLField" = AtomEventGraphQLField("received")
    client_time: "AtomEventGraphQLField" = AtomEventGraphQLField("clientTime")
    effective_time: "AtomEventGraphQLField" = AtomEventGraphQLField("effectiveTime")
    event_type: "AtomEventGraphQLField" = AtomEventGraphQLField("eventType")

    @classmethod
    def atom(cls) -> "AtomRecordFields":
        return AtomRecordFields("atom")

    atom_stage: "AtomEventGraphQLField" = AtomEventGraphQLField("atomStage")
    idempotency_key: "AtomEventGraphQLField" = AtomEventGraphQLField("idempotencyKey")

    def fields(
        self,
        *subfields: Union[
            AtomEventGraphQLField,
            "AtomRecordFields",
            "ObservationFields",
            "VisitFields",
        ],
    ) -> "AtomEventFields":
        """Subfields should come from the AtomEventFields class"""
        self._subfields.extend(subfields)
        return self

    def alias(self, alias: str) -> "AtomEventFields":
        self._alias = alias
        return self


class AtomRecordFields(GraphQLField):
    id: "AtomRecordGraphQLField" = AtomRecordGraphQLField("id")

    @classmethod
    def visit(cls) -> "VisitFields":
        return VisitFields("visit")

    index: "AtomRecordGraphQLField" = AtomRecordGraphQLField("index")
    description: "AtomRecordGraphQLField" = AtomRecordGraphQLField("description")
    instrument: "AtomRecordGraphQLField" = AtomRecordGraphQLField("instrument")

    @classmethod
    def observation(cls) -> "ObservationFields":
        return ObservationFields("observation")

    execution_state: "AtomRecordGraphQLField" = AtomRecordGraphQLField("executionState")

    @classmethod
    def interval(cls) -> "TimestampIntervalFields":
        return TimestampIntervalFields("interval")

    sequence_type: "AtomRecordGraphQLField" = AtomRecordGraphQLField("sequenceType")

    @classmethod
    def steps(
        cls, *, offset: Optional[Any] = None, limit: Optional[Any] = None
    ) -> "StepRecordSelectResultFields":
        arguments: dict[str, dict[str, Any]] = {
            "OFFSET": {"type": "PosInt", "value": offset},
            "LIMIT": {"type": "NonNegInt", "value": limit},
        }
        cleared_arguments = {
            key: value for key, value in arguments.items() if value["value"] is not None
        }
        return StepRecordSelectResultFields("steps", arguments=cleared_arguments)

    def fields(
        self,
        *subfields: Union[
            AtomRecordGraphQLField,
            "ObservationFields",
            "StepRecordSelectResultFields",
            "TimestampIntervalFields",
            "VisitFields",
        ],
    ) -> "AtomRecordFields":
        """Subfields should come from the AtomRecordFields class"""
        self._subfields.extend(subfields)
        return self

    def alias(self, alias: str) -> "AtomRecordFields":
        self._alias = alias
        return self


class AtomRecordSelectResultFields(GraphQLField):
    @classmethod
    def matches(cls) -> "AtomRecordFields":
        return AtomRecordFields("matches")

    has_more: "AtomRecordSelectResultGraphQLField" = AtomRecordSelectResultGraphQLField(
        "hasMore"
    )

    def fields(
        self, *subfields: Union[AtomRecordSelectResultGraphQLField, "AtomRecordFields"]
    ) -> "AtomRecordSelectResultFields":
        """Subfields should come from the AtomRecordSelectResultFields class"""
        self._subfields.extend(subfields)
        return self

    def alias(self, alias: str) -> "AtomRecordSelectResultFields":
        self._alias = alias
        return self


class AttachmentFields(GraphQLField):
    id: "AttachmentGraphQLField" = AttachmentGraphQLField("id")
    attachment_type: "AttachmentGraphQLField" = AttachmentGraphQLField("attachmentType")
    file_name: "AttachmentGraphQLField" = AttachmentGraphQLField("fileName")
    mask_name: "AttachmentGraphQLField" = AttachmentGraphQLField("maskName")
    description: "AttachmentGraphQLField" = AttachmentGraphQLField("description")
    checked: "AttachmentGraphQLField" = AttachmentGraphQLField("checked")
    file_size: "AttachmentGraphQLField" = AttachmentGraphQLField("fileSize")
    updated_at: "AttachmentGraphQLField" = AttachmentGraphQLField("updatedAt")

    @classmethod
    def program(cls) -> "ProgramFields":
        return ProgramFields("program")

    def fields(
        self, *subfields: Union[AttachmentGraphQLField, "ProgramFields"]
    ) -> "AttachmentFields":
        """Subfields should come from the AttachmentFields class"""
        self._subfields.extend(subfields)
        return self

    def alias(self, alias: str) -> "AttachmentFields":
        self._alias = alias
        return self


class BandBrightnessIntegratedFields(GraphQLField):
    band: "BandBrightnessIntegratedGraphQLField" = BandBrightnessIntegratedGraphQLField(
        "band"
    )
    value: "BandBrightnessIntegratedGraphQLField" = (
        BandBrightnessIntegratedGraphQLField("value")
    )
    units: "BandBrightnessIntegratedGraphQLField" = (
        BandBrightnessIntegratedGraphQLField("units")
    )
    error: "BandBrightnessIntegratedGraphQLField" = (
        BandBrightnessIntegratedGraphQLField("error")
    )

    def fields(
        self, *subfields: BandBrightnessIntegratedGraphQLField
    ) -> "BandBrightnessIntegratedFields":
        """Subfields should come from the BandBrightnessIntegratedFields class"""
        self._subfields.extend(subfields)
        return self

    def alias(self, alias: str) -> "BandBrightnessIntegratedFields":
        self._alias = alias
        return self


class BandBrightnessSurfaceFields(GraphQLField):
    band: "BandBrightnessSurfaceGraphQLField" = BandBrightnessSurfaceGraphQLField(
        "band"
    )
    value: "BandBrightnessSurfaceGraphQLField" = BandBrightnessSurfaceGraphQLField(
        "value"
    )
    units: "BandBrightnessSurfaceGraphQLField" = BandBrightnessSurfaceGraphQLField(
        "units"
    )
    error: "BandBrightnessSurfaceGraphQLField" = BandBrightnessSurfaceGraphQLField(
        "error"
    )

    def fields(
        self, *subfields: BandBrightnessSurfaceGraphQLField
    ) -> "BandBrightnessSurfaceFields":
        """Subfields should come from the BandBrightnessSurfaceFields class"""
        self._subfields.extend(subfields)
        return self

    def alias(self, alias: str) -> "BandBrightnessSurfaceFields":
        self._alias = alias
        return self


class BandNormalizedInterface(GraphQLField):
    @classmethod
    def sed(cls) -> "UnnormalizedSedFields":
        return UnnormalizedSedFields("sed")

    def fields(
        self, *subfields: Union[BandNormalizedGraphQLField, "UnnormalizedSedFields"]
    ) -> "BandNormalizedInterface":
        """Subfields should come from the BandNormalizedInterface class"""
        self._subfields.extend(subfields)
        return self

    def alias(self, alias: str) -> "BandNormalizedInterface":
        self._alias = alias
        return self

    def on(self, type_name: str, *subfields: GraphQLField) -> "BandNormalizedInterface":
        self._inline_fragments[type_name] = subfields
        return self


class BandNormalizedIntegratedFields(GraphQLField):
    @classmethod
    def brightnesses(cls) -> "BandBrightnessIntegratedFields":
        return BandBrightnessIntegratedFields("brightnesses")

    @classmethod
    def sed(cls) -> "UnnormalizedSedFields":
        return UnnormalizedSedFields("sed")

    def fields(
        self,
        *subfields: Union[
            BandNormalizedIntegratedGraphQLField,
            "BandBrightnessIntegratedFields",
            "UnnormalizedSedFields",
        ],
    ) -> "BandNormalizedIntegratedFields":
        """Subfields should come from the BandNormalizedIntegratedFields class"""
        self._subfields.extend(subfields)
        return self

    def alias(self, alias: str) -> "BandNormalizedIntegratedFields":
        self._alias = alias
        return self


class BandNormalizedSurfaceFields(GraphQLField):
    @classmethod
    def brightnesses(cls) -> "BandBrightnessSurfaceFields":
        return BandBrightnessSurfaceFields("brightnesses")

    @classmethod
    def sed(cls) -> "UnnormalizedSedFields":
        return UnnormalizedSedFields("sed")

    def fields(
        self,
        *subfields: Union[
            BandNormalizedSurfaceGraphQLField,
            "BandBrightnessSurfaceFields",
            "UnnormalizedSedFields",
        ],
    ) -> "BandNormalizedSurfaceFields":
        """Subfields should come from the BandNormalizedSurfaceFields class"""
        self._subfields.extend(subfields)
        return self

    def alias(self, alias: str) -> "BandNormalizedSurfaceFields":
        self._alias = alias
        return self


class BandedTimeFields(GraphQLField):
    band: "BandedTimeGraphQLField" = BandedTimeGraphQLField("band")

    @classmethod
    def time(cls) -> "CategorizedTimeFields":
        return CategorizedTimeFields("time")

    def fields(
        self, *subfields: Union[BandedTimeGraphQLField, "CategorizedTimeFields"]
    ) -> "BandedTimeFields":
        """Subfields should come from the BandedTimeFields class"""
        self._subfields.extend(subfields)
        return self

    def alias(self, alias: str) -> "BandedTimeFields":
        self._alias = alias
        return self


class BasePositionFields(GraphQLField):
    type_: "BasePositionGraphQLField" = BasePositionGraphQLField("type")
    name: "BasePositionGraphQLField" = BasePositionGraphQLField("name")

    @classmethod
    def sidereal(cls) -> "SiderealFields":
        return SiderealFields("sidereal")

    @classmethod
    def nonsidereal(cls) -> "NonsiderealFields":
        return NonsiderealFields("nonsidereal")

    @classmethod
    def coordinates(cls) -> "CoordinatesFields":
        return CoordinatesFields("coordinates")

    def fields(
        self,
        *subfields: Union[
            BasePositionGraphQLField,
            "CoordinatesFields",
            "NonsiderealFields",
            "SiderealFields",
        ],
    ) -> "BasePositionFields":
        """Subfields should come from the BasePositionFields class"""
        self._subfields.extend(subfields)
        return self

    def alias(self, alias: str) -> "BasePositionFields":
        self._alias = alias
        return self


class BiasFields(GraphQLField):
    step_type: "BiasGraphQLField" = BiasGraphQLField("stepType")

    def fields(self, *subfields: BiasGraphQLField) -> "BiasFields":
        """Subfields should come from the BiasFields class"""
        self._subfields.extend(subfields)
        return self

    def alias(self, alias: str) -> "BiasFields":
        self._alias = alias
        return self


class CalculatedBandedTimeFields(GraphQLField):
    calculation_state: "CalculatedBandedTimeGraphQLField" = (
        CalculatedBandedTimeGraphQLField("calculationState")
    )
    state: "CalculatedBandedTimeGraphQLField" = CalculatedBandedTimeGraphQLField(
        "state"
    )

    @classmethod
    def value(cls) -> "BandedTimeFields":
        return BandedTimeFields("value")

    def fields(
        self, *subfields: Union[CalculatedBandedTimeGraphQLField, "BandedTimeFields"]
    ) -> "CalculatedBandedTimeFields":
        """Subfields should come from the CalculatedBandedTimeFields class"""
        self._subfields.extend(subfields)
        return self

    def alias(self, alias: str) -> "CalculatedBandedTimeFields":
        self._alias = alias
        return self


class CalculatedCategorizedTimeRangeFields(GraphQLField):
    calculation_state: "CalculatedCategorizedTimeRangeGraphQLField" = (
        CalculatedCategorizedTimeRangeGraphQLField("calculationState")
    )
    state: "CalculatedCategorizedTimeRangeGraphQLField" = (
        CalculatedCategorizedTimeRangeGraphQLField("state")
    )

    @classmethod
    def value(cls) -> "CategorizedTimeRangeFields":
        return CategorizedTimeRangeFields("value")

    def fields(
        self,
        *subfields: Union[
            CalculatedCategorizedTimeRangeGraphQLField, "CategorizedTimeRangeFields"
        ],
    ) -> "CalculatedCategorizedTimeRangeFields":
        """Subfields should come from the CalculatedCategorizedTimeRangeFields class"""
        self._subfields.extend(subfields)
        return self

    def alias(self, alias: str) -> "CalculatedCategorizedTimeRangeFields":
        self._alias = alias
        return self


class CalculatedExecutionDigestFields(GraphQLField):
    calculation_state: "CalculatedExecutionDigestGraphQLField" = (
        CalculatedExecutionDigestGraphQLField("calculationState")
    )
    state: "CalculatedExecutionDigestGraphQLField" = (
        CalculatedExecutionDigestGraphQLField("state")
    )

    @classmethod
    def value(cls) -> "ExecutionDigestFields":
        return ExecutionDigestFields("value")

    def fields(
        self,
        *subfields: Union[
            CalculatedExecutionDigestGraphQLField, "ExecutionDigestFields"
        ],
    ) -> "CalculatedExecutionDigestFields":
        """Subfields should come from the CalculatedExecutionDigestFields class"""
        self._subfields.extend(subfields)
        return self

    def alias(self, alias: str) -> "CalculatedExecutionDigestFields":
        self._alias = alias
        return self


class CalculatedObservationWorkflowFields(GraphQLField):
    calculation_state: "CalculatedObservationWorkflowGraphQLField" = (
        CalculatedObservationWorkflowGraphQLField("calculationState")
    )
    state: "CalculatedObservationWorkflowGraphQLField" = (
        CalculatedObservationWorkflowGraphQLField("state")
    )

    @classmethod
    def value(cls) -> "ObservationWorkflowFields":
        return ObservationWorkflowFields("value")

    def fields(
        self,
        *subfields: Union[
            CalculatedObservationWorkflowGraphQLField, "ObservationWorkflowFields"
        ],
    ) -> "CalculatedObservationWorkflowFields":
        """Subfields should come from the CalculatedObservationWorkflowFields class"""
        self._subfields.extend(subfields)
        return self

    def alias(self, alias: str) -> "CalculatedObservationWorkflowFields":
        self._alias = alias
        return self


class CalibrationProgramReferenceFields(GraphQLField):
    label: "CalibrationProgramReferenceGraphQLField" = (
        CalibrationProgramReferenceGraphQLField("label")
    )
    type_: "CalibrationProgramReferenceGraphQLField" = (
        CalibrationProgramReferenceGraphQLField("type")
    )
    instrument: "CalibrationProgramReferenceGraphQLField" = (
        CalibrationProgramReferenceGraphQLField("instrument")
    )
    semester: "CalibrationProgramReferenceGraphQLField" = (
        CalibrationProgramReferenceGraphQLField("semester")
    )
    semester_index: "CalibrationProgramReferenceGraphQLField" = (
        CalibrationProgramReferenceGraphQLField("semesterIndex")
    )

    def fields(
        self, *subfields: CalibrationProgramReferenceGraphQLField
    ) -> "CalibrationProgramReferenceFields":
        """Subfields should come from the CalibrationProgramReferenceFields class"""
        self._subfields.extend(subfields)
        return self

    def alias(self, alias: str) -> "CalibrationProgramReferenceFields":
        self._alias = alias
        return self


class CallForProposalsFields(GraphQLField):
    id: "CallForProposalsGraphQLField" = CallForProposalsGraphQLField("id")
    title: "CallForProposalsGraphQLField" = CallForProposalsGraphQLField("title")
    semester: "CallForProposalsGraphQLField" = CallForProposalsGraphQLField("semester")

    @classmethod
    def active(cls) -> "DateIntervalFields":
        return DateIntervalFields("active")

    @classmethod
    def partners(cls) -> "CallForProposalsPartnerFields":
        return CallForProposalsPartnerFields("partners")

    submission_deadline_default: "CallForProposalsGraphQLField" = (
        CallForProposalsGraphQLField("submissionDeadlineDefault")
    )
    existence: "CallForProposalsGraphQLField" = CallForProposalsGraphQLField(
        "existence"
    )
    observatory: "CallForProposalsGraphQLField" = CallForProposalsGraphQLField(
        "observatory"
    )

    @classmethod
    def gemini(cls) -> "GeminiCallPropertiesFields":
        return GeminiCallPropertiesFields("gemini")

    @classmethod
    def keck(cls) -> "KeckCallPropertiesFields":
        return KeckCallPropertiesFields("keck")

    @classmethod
    def subaru(cls) -> "SubaruCallPropertiesFields":
        return SubaruCallPropertiesFields("subaru")

    def fields(
        self,
        *subfields: Union[
            CallForProposalsGraphQLField,
            "CallForProposalsPartnerFields",
            "DateIntervalFields",
            "GeminiCallPropertiesFields",
            "KeckCallPropertiesFields",
            "SubaruCallPropertiesFields",
        ],
    ) -> "CallForProposalsFields":
        """Subfields should come from the CallForProposalsFields class"""
        self._subfields.extend(subfields)
        return self

    def alias(self, alias: str) -> "CallForProposalsFields":
        self._alias = alias
        return self


class CallForProposalsExchangePartnerFields(GraphQLField):
    exchange_partner: "CallForProposalsExchangePartnerGraphQLField" = (
        CallForProposalsExchangePartnerGraphQLField("exchangePartner")
    )
    submission_deadline_override: "CallForProposalsExchangePartnerGraphQLField" = (
        CallForProposalsExchangePartnerGraphQLField("submissionDeadlineOverride")
    )
    submission_deadline: "CallForProposalsExchangePartnerGraphQLField" = (
        CallForProposalsExchangePartnerGraphQLField("submissionDeadline")
    )

    def fields(
        self, *subfields: CallForProposalsExchangePartnerGraphQLField
    ) -> "CallForProposalsExchangePartnerFields":
        """Subfields should come from the CallForProposalsExchangePartnerFields class"""
        self._subfields.extend(subfields)
        return self

    def alias(self, alias: str) -> "CallForProposalsExchangePartnerFields":
        self._alias = alias
        return self


class CallForProposalsPartnerFields(GraphQLField):
    gemini_partner: "CallForProposalsPartnerGraphQLField" = (
        CallForProposalsPartnerGraphQLField("geminiPartner")
    )
    submission_deadline_override: "CallForProposalsPartnerGraphQLField" = (
        CallForProposalsPartnerGraphQLField("submissionDeadlineOverride")
    )
    submission_deadline: "CallForProposalsPartnerGraphQLField" = (
        CallForProposalsPartnerGraphQLField("submissionDeadline")
    )

    def fields(
        self, *subfields: CallForProposalsPartnerGraphQLField
    ) -> "CallForProposalsPartnerFields":
        """Subfields should come from the CallForProposalsPartnerFields class"""
        self._subfields.extend(subfields)
        return self

    def alias(self, alias: str) -> "CallForProposalsPartnerFields":
        self._alias = alias
        return self


class CallsForProposalsSelectResultFields(GraphQLField):
    @classmethod
    def matches(cls) -> "CallForProposalsFields":
        return CallForProposalsFields("matches")

    has_more: "CallsForProposalsSelectResultGraphQLField" = (
        CallsForProposalsSelectResultGraphQLField("hasMore")
    )

    def fields(
        self,
        *subfields: Union[
            CallsForProposalsSelectResultGraphQLField, "CallForProposalsFields"
        ],
    ) -> "CallsForProposalsSelectResultFields":
        """Subfields should come from the CallsForProposalsSelectResultFields class"""
        self._subfields.extend(subfields)
        return self

    def alias(self, alias: str) -> "CallsForProposalsSelectResultFields":
        self._alias = alias
        return self


class CatalogInfoFields(GraphQLField):
    name: "CatalogInfoGraphQLField" = CatalogInfoGraphQLField("name")
    id: "CatalogInfoGraphQLField" = CatalogInfoGraphQLField("id")
    object_type: "CatalogInfoGraphQLField" = CatalogInfoGraphQLField("objectType")

    def fields(self, *subfields: CatalogInfoGraphQLField) -> "CatalogInfoFields":
        """Subfields should come from the CatalogInfoFields class"""
        self._subfields.extend(subfields)
        return self

    def alias(self, alias: str) -> "CatalogInfoFields":
        self._alias = alias
        return self


class CategorizedTimeFields(GraphQLField):
    @classmethod
    def program(cls) -> "TimeSpanFields":
        return TimeSpanFields("program")

    @classmethod
    def non_charged(cls) -> "TimeSpanFields":
        return TimeSpanFields("nonCharged")

    @classmethod
    def total(cls) -> "TimeSpanFields":
        return TimeSpanFields("total")

    def fields(
        self, *subfields: Union[CategorizedTimeGraphQLField, "TimeSpanFields"]
    ) -> "CategorizedTimeFields":
        """Subfields should come from the CategorizedTimeFields class"""
        self._subfields.extend(subfields)
        return self

    def alias(self, alias: str) -> "CategorizedTimeFields":
        self._alias = alias
        return self


class CategorizedTimeRangeFields(GraphQLField):
    @classmethod
    def minimum(cls) -> "CategorizedTimeFields":
        return CategorizedTimeFields("minimum")

    @classmethod
    def maximum(cls) -> "CategorizedTimeFields":
        return CategorizedTimeFields("maximum")

    def fields(
        self,
        *subfields: Union[CategorizedTimeRangeGraphQLField, "CategorizedTimeFields"],
    ) -> "CategorizedTimeRangeFields":
        """Subfields should come from the CategorizedTimeRangeFields class"""
        self._subfields.extend(subfields)
        return self

    def alias(self, alias: str) -> "CategorizedTimeRangeFields":
        self._alias = alias
        return self


class ChangePrincipalInvestigatorResultFields(GraphQLField):
    @classmethod
    def program_user(cls) -> "ProgramUserFields":
        return ProgramUserFields("programUser")

    def fields(
        self,
        *subfields: Union[
            ChangePrincipalInvestigatorResultGraphQLField, "ProgramUserFields"
        ],
    ) -> "ChangePrincipalInvestigatorResultFields":
        """Subfields should come from the ChangePrincipalInvestigatorResultFields class"""
        self._subfields.extend(subfields)
        return self

    def alias(self, alias: str) -> "ChangePrincipalInvestigatorResultFields":
        self._alias = alias
        return self


class ChangeProgramUserRoleResultFields(GraphQLField):
    @classmethod
    def program_user(cls) -> "ProgramUserFields":
        return ProgramUserFields("programUser")

    def fields(
        self,
        *subfields: Union[ChangeProgramUserRoleResultGraphQLField, "ProgramUserFields"],
    ) -> "ChangeProgramUserRoleResultFields":
        """Subfields should come from the ChangeProgramUserRoleResultFields class"""
        self._subfields.extend(subfields)
        return self

    def alias(self, alias: str) -> "ChangeProgramUserRoleResultFields":
        self._alias = alias
        return self


class ClassicalFields(GraphQLField):
    science_subtype: "ClassicalGraphQLField" = ClassicalGraphQLField("scienceSubtype")
    min_percent_time: "ClassicalGraphQLField" = ClassicalGraphQLField("minPercentTime")

    @classmethod
    def partner_splits(cls) -> "PartnerSplitFields":
        return PartnerSplitFields("partnerSplits")

    exchange_partner: "ClassicalGraphQLField" = ClassicalGraphQLField("exchangePartner")
    aeon_multi_facility: "ClassicalGraphQLField" = ClassicalGraphQLField(
        "aeonMultiFacility"
    )
    jwst_synergy: "ClassicalGraphQLField" = ClassicalGraphQLField("jwstSynergy")
    us_long_term: "ClassicalGraphQLField" = ClassicalGraphQLField("usLongTerm")

    def fields(
        self, *subfields: Union[ClassicalGraphQLField, "PartnerSplitFields"]
    ) -> "ClassicalFields":
        """Subfields should come from the ClassicalFields class"""
        self._subfields.extend(subfields)
        return self

    def alias(self, alias: str) -> "ClassicalFields":
        self._alias = alias
        return self


class CloneGroupResultFields(GraphQLField):
    @classmethod
    def new_group(cls) -> "GroupFields":
        return GroupFields("newGroup")

    def fields(
        self, *subfields: Union[CloneGroupResultGraphQLField, "GroupFields"]
    ) -> "CloneGroupResultFields":
        """Subfields should come from the CloneGroupResultFields class"""
        self._subfields.extend(subfields)
        return self

    def alias(self, alias: str) -> "CloneGroupResultFields":
        self._alias = alias
        return self


class CloneObservationResultFields(GraphQLField):
    @classmethod
    def new_observation(cls) -> "ObservationFields":
        return ObservationFields("newObservation")

    def fields(
        self, *subfields: Union[CloneObservationResultGraphQLField, "ObservationFields"]
    ) -> "CloneObservationResultFields":
        """Subfields should come from the CloneObservationResultFields class"""
        self._subfields.extend(subfields)
        return self

    def alias(self, alias: str) -> "CloneObservationResultFields":
        self._alias = alias
        return self


class CloneTargetResultFields(GraphQLField):
    @classmethod
    def new_target(cls) -> "TargetFields":
        return TargetFields("newTarget")

    def fields(
        self, *subfields: Union[CloneTargetResultGraphQLField, "TargetFields"]
    ) -> "CloneTargetResultFields":
        """Subfields should come from the CloneTargetResultFields class"""
        self._subfields.extend(subfields)
        return self

    def alias(self, alias: str) -> "CloneTargetResultFields":
        self._alias = alias
        return self


class CommissioningProgramReferenceFields(GraphQLField):
    label: "CommissioningProgramReferenceGraphQLField" = (
        CommissioningProgramReferenceGraphQLField("label")
    )
    type_: "CommissioningProgramReferenceGraphQLField" = (
        CommissioningProgramReferenceGraphQLField("type")
    )
    instrument: "CommissioningProgramReferenceGraphQLField" = (
        CommissioningProgramReferenceGraphQLField("instrument")
    )
    semester: "CommissioningProgramReferenceGraphQLField" = (
        CommissioningProgramReferenceGraphQLField("semester")
    )
    semester_index: "CommissioningProgramReferenceGraphQLField" = (
        CommissioningProgramReferenceGraphQLField("semesterIndex")
    )

    def fields(
        self, *subfields: CommissioningProgramReferenceGraphQLField
    ) -> "CommissioningProgramReferenceFields":
        """Subfields should come from the CommissioningProgramReferenceFields class"""
        self._subfields.extend(subfields)
        return self

    def alias(self, alias: str) -> "CommissioningProgramReferenceFields":
        self._alias = alias
        return self


class ConditionsEntryFields(GraphQLField):
    id: "ConditionsEntryGraphQLField" = ConditionsEntryGraphQLField("id")
    transaction_id: "ConditionsEntryGraphQLField" = ConditionsEntryGraphQLField(
        "transactionId"
    )

    @classmethod
    def user(cls) -> "UserFields":
        return UserFields("user")

    timestamp: "ConditionsEntryGraphQLField" = ConditionsEntryGraphQLField("timestamp")

    @classmethod
    def measurement(cls) -> "ConditionsMeasurementFields":
        return ConditionsMeasurementFields("measurement")

    @classmethod
    def intuition(cls) -> "ConditionsIntuitionFields":
        return ConditionsIntuitionFields("intuition")

    def fields(
        self,
        *subfields: Union[
            ConditionsEntryGraphQLField,
            "ConditionsIntuitionFields",
            "ConditionsMeasurementFields",
            "UserFields",
        ],
    ) -> "ConditionsEntryFields":
        """Subfields should come from the ConditionsEntryFields class"""
        self._subfields.extend(subfields)
        return self

    def alias(self, alias: str) -> "ConditionsEntryFields":
        self._alias = alias
        return self


class ConditionsExpectationFields(GraphQLField):
    type_: "ConditionsExpectationGraphQLField" = ConditionsExpectationGraphQLField(
        "type"
    )

    @classmethod
    def timeframe(cls) -> "TimeSpanFields":
        return TimeSpanFields("timeframe")

    def fields(
        self, *subfields: Union[ConditionsExpectationGraphQLField, "TimeSpanFields"]
    ) -> "ConditionsExpectationFields":
        """Subfields should come from the ConditionsExpectationFields class"""
        self._subfields.extend(subfields)
        return self

    def alias(self, alias: str) -> "ConditionsExpectationFields":
        self._alias = alias
        return self


class ConditionsIntuitionFields(GraphQLField):
    @classmethod
    def expectation(cls) -> "ConditionsExpectationFields":
        return ConditionsExpectationFields("expectation")

    seeing_trend: "ConditionsIntuitionGraphQLField" = ConditionsIntuitionGraphQLField(
        "seeingTrend"
    )

    def fields(
        self,
        *subfields: Union[
            ConditionsIntuitionGraphQLField, "ConditionsExpectationFields"
        ],
    ) -> "ConditionsIntuitionFields":
        """Subfields should come from the ConditionsIntuitionFields class"""
        self._subfields.extend(subfields)
        return self

    def alias(self, alias: str) -> "ConditionsIntuitionFields":
        self._alias = alias
        return self


class ConditionsMeasurementFields(GraphQLField):
    source: "ConditionsMeasurementGraphQLField" = ConditionsMeasurementGraphQLField(
        "source"
    )

    @classmethod
    def seeing(cls) -> "AngleFields":
        return AngleFields("seeing")

    extinction: "ConditionsMeasurementGraphQLField" = ConditionsMeasurementGraphQLField(
        "extinction"
    )

    @classmethod
    def wavelength(cls) -> "WavelengthFields":
        return WavelengthFields("wavelength")

    @classmethod
    def azimuth(cls) -> "AngleFields":
        return AngleFields("azimuth")

    @classmethod
    def elevation(cls) -> "AngleFields":
        return AngleFields("elevation")

    def fields(
        self,
        *subfields: Union[
            ConditionsMeasurementGraphQLField, "AngleFields", "WavelengthFields"
        ],
    ) -> "ConditionsMeasurementFields":
        """Subfields should come from the ConditionsMeasurementFields class"""
        self._subfields.extend(subfields)
        return self

    def alias(self, alias: str) -> "ConditionsMeasurementFields":
        self._alias = alias
        return self


class ConfigChangeEstimateFields(GraphQLField):
    name: "ConfigChangeEstimateGraphQLField" = ConfigChangeEstimateGraphQLField("name")
    description: "ConfigChangeEstimateGraphQLField" = ConfigChangeEstimateGraphQLField(
        "description"
    )

    @classmethod
    def estimate(cls) -> "TimeSpanFields":
        return TimeSpanFields("estimate")

    def fields(
        self, *subfields: Union[ConfigChangeEstimateGraphQLField, "TimeSpanFields"]
    ) -> "ConfigChangeEstimateFields":
        """Subfields should come from the ConfigChangeEstimateFields class"""
        self._subfields.extend(subfields)
        return self

    def alias(self, alias: str) -> "ConfigChangeEstimateFields":
        self._alias = alias
        return self


class ConfigurationFields(GraphQLField):
    @classmethod
    def conditions(cls) -> "ConfigurationConditionsFields":
        return ConfigurationConditionsFields("conditions")

    @classmethod
    def target(cls) -> "ConfigurationTargetFields":
        return ConfigurationTargetFields("target")

    @classmethod
    def observing_mode(cls) -> "ConfigurationObservingModeFields":
        return ConfigurationObservingModeFields("observingMode")

    def fields(
        self,
        *subfields: Union[
            ConfigurationGraphQLField,
            "ConfigurationConditionsFields",
            "ConfigurationObservingModeFields",
            "ConfigurationTargetFields",
        ],
    ) -> "ConfigurationFields":
        """Subfields should come from the ConfigurationFields class"""
        self._subfields.extend(subfields)
        return self

    def alias(self, alias: str) -> "ConfigurationFields":
        self._alias = alias
        return self


class ConfigurationConditionsFields(GraphQLField):
    image_quality: "ConfigurationConditionsGraphQLField" = (
        ConfigurationConditionsGraphQLField("imageQuality")
    )
    cloud_extinction: "ConfigurationConditionsGraphQLField" = (
        ConfigurationConditionsGraphQLField("cloudExtinction")
    )
    sky_background: "ConfigurationConditionsGraphQLField" = (
        ConfigurationConditionsGraphQLField("skyBackground")
    )
    water_vapor: "ConfigurationConditionsGraphQLField" = (
        ConfigurationConditionsGraphQLField("waterVapor")
    )

    def fields(
        self, *subfields: ConfigurationConditionsGraphQLField
    ) -> "ConfigurationConditionsFields":
        """Subfields should come from the ConfigurationConditionsFields class"""
        self._subfields.extend(subfields)
        return self

    def alias(self, alias: str) -> "ConfigurationConditionsFields":
        self._alias = alias
        return self


class ConfigurationFlamingos2LongSlitFields(GraphQLField):
    disperser: "ConfigurationFlamingos2LongSlitGraphQLField" = (
        ConfigurationFlamingos2LongSlitGraphQLField("disperser")
    )

    def fields(
        self, *subfields: ConfigurationFlamingos2LongSlitGraphQLField
    ) -> "ConfigurationFlamingos2LongSlitFields":
        """Subfields should come from the ConfigurationFlamingos2LongSlitFields class"""
        self._subfields.extend(subfields)
        return self

    def alias(self, alias: str) -> "ConfigurationFlamingos2LongSlitFields":
        self._alias = alias
        return self


class ConfigurationGmosNorthImagingFields(GraphQLField):
    filters: "ConfigurationGmosNorthImagingGraphQLField" = (
        ConfigurationGmosNorthImagingGraphQLField("filters")
    )

    def fields(
        self, *subfields: ConfigurationGmosNorthImagingGraphQLField
    ) -> "ConfigurationGmosNorthImagingFields":
        """Subfields should come from the ConfigurationGmosNorthImagingFields class"""
        self._subfields.extend(subfields)
        return self

    def alias(self, alias: str) -> "ConfigurationGmosNorthImagingFields":
        self._alias = alias
        return self


class ConfigurationGmosNorthLongSlitFields(GraphQLField):
    grating: "ConfigurationGmosNorthLongSlitGraphQLField" = (
        ConfigurationGmosNorthLongSlitGraphQLField("grating")
    )

    def fields(
        self, *subfields: ConfigurationGmosNorthLongSlitGraphQLField
    ) -> "ConfigurationGmosNorthLongSlitFields":
        """Subfields should come from the ConfigurationGmosNorthLongSlitFields class"""
        self._subfields.extend(subfields)
        return self

    def alias(self, alias: str) -> "ConfigurationGmosNorthLongSlitFields":
        self._alias = alias
        return self


class ConfigurationGmosNorthMosFields(GraphQLField):
    grating: "ConfigurationGmosNorthMosGraphQLField" = (
        ConfigurationGmosNorthMosGraphQLField("grating")
    )

    def fields(
        self, *subfields: ConfigurationGmosNorthMosGraphQLField
    ) -> "ConfigurationGmosNorthMosFields":
        """Subfields should come from the ConfigurationGmosNorthMosFields class"""
        self._subfields.extend(subfields)
        return self

    def alias(self, alias: str) -> "ConfigurationGmosNorthMosFields":
        self._alias = alias
        return self


class ConfigurationGmosSouthImagingFields(GraphQLField):
    filters: "ConfigurationGmosSouthImagingGraphQLField" = (
        ConfigurationGmosSouthImagingGraphQLField("filters")
    )

    def fields(
        self, *subfields: ConfigurationGmosSouthImagingGraphQLField
    ) -> "ConfigurationGmosSouthImagingFields":
        """Subfields should come from the ConfigurationGmosSouthImagingFields class"""
        self._subfields.extend(subfields)
        return self

    def alias(self, alias: str) -> "ConfigurationGmosSouthImagingFields":
        self._alias = alias
        return self


class ConfigurationGmosSouthLongSlitFields(GraphQLField):
    grating: "ConfigurationGmosSouthLongSlitGraphQLField" = (
        ConfigurationGmosSouthLongSlitGraphQLField("grating")
    )

    def fields(
        self, *subfields: ConfigurationGmosSouthLongSlitGraphQLField
    ) -> "ConfigurationGmosSouthLongSlitFields":
        """Subfields should come from the ConfigurationGmosSouthLongSlitFields class"""
        self._subfields.extend(subfields)
        return self

    def alias(self, alias: str) -> "ConfigurationGmosSouthLongSlitFields":
        self._alias = alias
        return self


class ConfigurationGmosSouthMosFields(GraphQLField):
    grating: "ConfigurationGmosSouthMosGraphQLField" = (
        ConfigurationGmosSouthMosGraphQLField("grating")
    )

    def fields(
        self, *subfields: ConfigurationGmosSouthMosGraphQLField
    ) -> "ConfigurationGmosSouthMosFields":
        """Subfields should come from the ConfigurationGmosSouthMosFields class"""
        self._subfields.extend(subfields)
        return self

    def alias(self, alias: str) -> "ConfigurationGmosSouthMosFields":
        self._alias = alias
        return self


class ConfigurationGnirsIfuFields(GraphQLField):
    grating: "ConfigurationGnirsIfuGraphQLField" = ConfigurationGnirsIfuGraphQLField(
        "grating"
    )
    fpu: "ConfigurationGnirsIfuGraphQLField" = ConfigurationGnirsIfuGraphQLField("fpu")

    def fields(
        self, *subfields: ConfigurationGnirsIfuGraphQLField
    ) -> "ConfigurationGnirsIfuFields":
        """Subfields should come from the ConfigurationGnirsIfuFields class"""
        self._subfields.extend(subfields)
        return self

    def alias(self, alias: str) -> "ConfigurationGnirsIfuFields":
        self._alias = alias
        return self


class ConfigurationGnirsLongSlitFields(GraphQLField):
    grating: "ConfigurationGnirsLongSlitGraphQLField" = (
        ConfigurationGnirsLongSlitGraphQLField("grating")
    )
    camera: "ConfigurationGnirsLongSlitGraphQLField" = (
        ConfigurationGnirsLongSlitGraphQLField("camera")
    )
    prism: "ConfigurationGnirsLongSlitGraphQLField" = (
        ConfigurationGnirsLongSlitGraphQLField("prism")
    )

    def fields(
        self, *subfields: ConfigurationGnirsLongSlitGraphQLField
    ) -> "ConfigurationGnirsLongSlitFields":
        """Subfields should come from the ConfigurationGnirsLongSlitFields class"""
        self._subfields.extend(subfields)
        return self

    def alias(self, alias: str) -> "ConfigurationGnirsLongSlitFields":
        self._alias = alias
        return self


class ConfigurationIgrins2LongSlitFields(GraphQLField):
    ignore: "ConfigurationIgrins2LongSlitGraphQLField" = (
        ConfigurationIgrins2LongSlitGraphQLField("ignore")
    )

    def fields(
        self, *subfields: ConfigurationIgrins2LongSlitGraphQLField
    ) -> "ConfigurationIgrins2LongSlitFields":
        """Subfields should come from the ConfigurationIgrins2LongSlitFields class"""
        self._subfields.extend(subfields)
        return self

    def alias(self, alias: str) -> "ConfigurationIgrins2LongSlitFields":
        self._alias = alias
        return self


class ConfigurationObservingModeFields(GraphQLField):
    instrument: "ConfigurationObservingModeGraphQLField" = (
        ConfigurationObservingModeGraphQLField("instrument")
    )
    mode: "ConfigurationObservingModeGraphQLField" = (
        ConfigurationObservingModeGraphQLField("mode")
    )

    @classmethod
    def gmos_north_long_slit(cls) -> "ConfigurationGmosNorthLongSlitFields":
        return ConfigurationGmosNorthLongSlitFields("gmosNorthLongSlit")

    @classmethod
    def gmos_south_long_slit(cls) -> "ConfigurationGmosSouthLongSlitFields":
        return ConfigurationGmosSouthLongSlitFields("gmosSouthLongSlit")

    @classmethod
    def gmos_north_mos(cls) -> "ConfigurationGmosNorthMosFields":
        return ConfigurationGmosNorthMosFields("gmosNorthMos")

    @classmethod
    def gmos_south_mos(cls) -> "ConfigurationGmosSouthMosFields":
        return ConfigurationGmosSouthMosFields("gmosSouthMos")

    @classmethod
    def gmos_north_imaging(cls) -> "ConfigurationGmosNorthImagingFields":
        return ConfigurationGmosNorthImagingFields("gmosNorthImaging")

    @classmethod
    def gmos_south_imaging(cls) -> "ConfigurationGmosSouthImagingFields":
        return ConfigurationGmosSouthImagingFields("gmosSouthImaging")

    @classmethod
    def flamingos_2_long_slit(cls) -> "ConfigurationFlamingos2LongSlitFields":
        return ConfigurationFlamingos2LongSlitFields("flamingos2LongSlit")

    @classmethod
    def gnirs_long_slit(cls) -> "ConfigurationGnirsLongSlitFields":
        return ConfigurationGnirsLongSlitFields("gnirsLongSlit")

    @classmethod
    def gnirs_ifu(cls) -> "ConfigurationGnirsIfuFields":
        return ConfigurationGnirsIfuFields("gnirsIfu")

    @classmethod
    def igrins_2_long_slit(cls) -> "ConfigurationIgrins2LongSlitFields":
        return ConfigurationIgrins2LongSlitFields("igrins2LongSlit")

    @classmethod
    def visitor(cls) -> "ConfigurationVisitorFields":
        return ConfigurationVisitorFields("visitor")

    def fields(
        self,
        *subfields: Union[
            ConfigurationObservingModeGraphQLField,
            "ConfigurationFlamingos2LongSlitFields",
            "ConfigurationGmosNorthImagingFields",
            "ConfigurationGmosNorthLongSlitFields",
            "ConfigurationGmosNorthMosFields",
            "ConfigurationGmosSouthImagingFields",
            "ConfigurationGmosSouthLongSlitFields",
            "ConfigurationGmosSouthMosFields",
            "ConfigurationGnirsIfuFields",
            "ConfigurationGnirsLongSlitFields",
            "ConfigurationIgrins2LongSlitFields",
            "ConfigurationVisitorFields",
        ],
    ) -> "ConfigurationObservingModeFields":
        """Subfields should come from the ConfigurationObservingModeFields class"""
        self._subfields.extend(subfields)
        return self

    def alias(self, alias: str) -> "ConfigurationObservingModeFields":
        self._alias = alias
        return self


class ConfigurationRequestFields(GraphQLField):
    id: "ConfigurationRequestGraphQLField" = ConfigurationRequestGraphQLField("id")

    @classmethod
    def program(cls) -> "ProgramFields":
        return ProgramFields("program")

    status: "ConfigurationRequestGraphQLField" = ConfigurationRequestGraphQLField(
        "status"
    )
    justification: "ConfigurationRequestGraphQLField" = (
        ConfigurationRequestGraphQLField("justification")
    )
    feedback: "ConfigurationRequestGraphQLField" = ConfigurationRequestGraphQLField(
        "feedback"
    )
    created_at: "ConfigurationRequestGraphQLField" = ConfigurationRequestGraphQLField(
        "createdAt"
    )
    updated_at: "ConfigurationRequestGraphQLField" = ConfigurationRequestGraphQLField(
        "updatedAt"
    )

    @classmethod
    def configuration(cls) -> "ConfigurationFields":
        return ConfigurationFields("configuration")

    applicable_observations: "ConfigurationRequestGraphQLField" = (
        ConfigurationRequestGraphQLField("applicableObservations")
    )

    def fields(
        self,
        *subfields: Union[
            ConfigurationRequestGraphQLField, "ConfigurationFields", "ProgramFields"
        ],
    ) -> "ConfigurationRequestFields":
        """Subfields should come from the ConfigurationRequestFields class"""
        self._subfields.extend(subfields)
        return self

    def alias(self, alias: str) -> "ConfigurationRequestFields":
        self._alias = alias
        return self


class ConfigurationRequestSelectResultFields(GraphQLField):
    @classmethod
    def matches(cls) -> "ConfigurationRequestFields":
        return ConfigurationRequestFields("matches")

    has_more: "ConfigurationRequestSelectResultGraphQLField" = (
        ConfigurationRequestSelectResultGraphQLField("hasMore")
    )

    def fields(
        self,
        *subfields: Union[
            ConfigurationRequestSelectResultGraphQLField, "ConfigurationRequestFields"
        ],
    ) -> "ConfigurationRequestSelectResultFields":
        """Subfields should come from the ConfigurationRequestSelectResultFields class"""
        self._subfields.extend(subfields)
        return self

    def alias(self, alias: str) -> "ConfigurationRequestSelectResultFields":
        self._alias = alias
        return self


class ConfigurationTargetFields(GraphQLField):
    @classmethod
    def coordinates(cls) -> "CoordinatesFields":
        return CoordinatesFields("coordinates")

    @classmethod
    def region(cls) -> "RegionFields":
        return RegionFields("region")

    def fields(
        self,
        *subfields: Union[
            ConfigurationTargetGraphQLField, "CoordinatesFields", "RegionFields"
        ],
    ) -> "ConfigurationTargetFields":
        """Subfields should come from the ConfigurationTargetFields class"""
        self._subfields.extend(subfields)
        return self

    def alias(self, alias: str) -> "ConfigurationTargetFields":
        self._alias = alias
        return self


class ConfigurationVisitorFields(GraphQLField):
    mode: "ConfigurationVisitorGraphQLField" = ConfigurationVisitorGraphQLField("mode")

    @classmethod
    def radius(cls) -> "AngleFields":
        return AngleFields("radius")

    def fields(
        self, *subfields: Union[ConfigurationVisitorGraphQLField, "AngleFields"]
    ) -> "ConfigurationVisitorFields":
        """Subfields should come from the ConfigurationVisitorFields class"""
        self._subfields.extend(subfields)
        return self

    def alias(self, alias: str) -> "ConfigurationVisitorFields":
        self._alias = alias
        return self


class ConstraintSetFields(GraphQLField):
    image_quality: "ConstraintSetGraphQLField" = ConstraintSetGraphQLField(
        "imageQuality"
    )
    cloud_extinction: "ConstraintSetGraphQLField" = ConstraintSetGraphQLField(
        "cloudExtinction"
    )
    sky_background: "ConstraintSetGraphQLField" = ConstraintSetGraphQLField(
        "skyBackground"
    )
    water_vapor: "ConstraintSetGraphQLField" = ConstraintSetGraphQLField("waterVapor")

    @classmethod
    def elevation_range(cls) -> "ElevationRangeFields":
        return ElevationRangeFields("elevationRange")

    def fields(
        self, *subfields: Union[ConstraintSetGraphQLField, "ElevationRangeFields"]
    ) -> "ConstraintSetFields":
        """Subfields should come from the ConstraintSetFields class"""
        self._subfields.extend(subfields)
        return self

    def alias(self, alias: str) -> "ConstraintSetFields":
        self._alias = alias
        return self


class ConstraintSetGroupFields(GraphQLField):
    @classmethod
    def observations(
        cls,
        include_deleted: bool,
        *,
        offset: Optional[Any] = None,
        limit: Optional[Any] = None,
    ) -> "ObservationSelectResultFields":
        arguments: dict[str, dict[str, Any]] = {
            "includeDeleted": {"type": "Boolean!", "value": include_deleted},
            "OFFSET": {"type": "ObservationId", "value": offset},
            "LIMIT": {"type": "NonNegInt", "value": limit},
        }
        cleared_arguments = {
            key: value for key, value in arguments.items() if value["value"] is not None
        }
        return ObservationSelectResultFields(
            "observations", arguments=cleared_arguments
        )

    @classmethod
    def constraint_set(cls) -> "ConstraintSetFields":
        return ConstraintSetFields("constraintSet")

    @classmethod
    def program(cls) -> "ProgramFields":
        return ProgramFields("program")

    def fields(
        self,
        *subfields: Union[
            ConstraintSetGroupGraphQLField,
            "ConstraintSetFields",
            "ObservationSelectResultFields",
            "ProgramFields",
        ],
    ) -> "ConstraintSetGroupFields":
        """Subfields should come from the ConstraintSetGroupFields class"""
        self._subfields.extend(subfields)
        return self

    def alias(self, alias: str) -> "ConstraintSetGroupFields":
        self._alias = alias
        return self


class ConstraintSetGroupSelectResultFields(GraphQLField):
    @classmethod
    def matches(cls) -> "ConstraintSetGroupFields":
        return ConstraintSetGroupFields("matches")

    has_more: "ConstraintSetGroupSelectResultGraphQLField" = (
        ConstraintSetGroupSelectResultGraphQLField("hasMore")
    )

    def fields(
        self,
        *subfields: Union[
            ConstraintSetGroupSelectResultGraphQLField, "ConstraintSetGroupFields"
        ],
    ) -> "ConstraintSetGroupSelectResultFields":
        """Subfields should come from the ConstraintSetGroupSelectResultFields class"""
        self._subfields.extend(subfields)
        return self

    def alias(self, alias: str) -> "ConstraintSetGroupSelectResultFields":
        self._alias = alias
        return self


class CoordinateLimitsFields(GraphQLField):
    @classmethod
    def ra_start(cls) -> "RightAscensionFields":
        return RightAscensionFields("raStart")

    @classmethod
    def ra_end(cls) -> "RightAscensionFields":
        return RightAscensionFields("raEnd")

    @classmethod
    def dec_start(cls) -> "DeclinationFields":
        return DeclinationFields("decStart")

    @classmethod
    def dec_end(cls) -> "DeclinationFields":
        return DeclinationFields("decEnd")

    def fields(
        self,
        *subfields: Union[
            CoordinateLimitsGraphQLField, "DeclinationFields", "RightAscensionFields"
        ],
    ) -> "CoordinateLimitsFields":
        """Subfields should come from the CoordinateLimitsFields class"""
        self._subfields.extend(subfields)
        return self

    def alias(self, alias: str) -> "CoordinateLimitsFields":
        self._alias = alias
        return self


class CoordinatesFields(GraphQLField):
    @classmethod
    def ra(cls) -> "RightAscensionFields":
        return RightAscensionFields("ra")

    @classmethod
    def dec(cls) -> "DeclinationFields":
        return DeclinationFields("dec")

    def fields(
        self,
        *subfields: Union[
            CoordinatesGraphQLField, "DeclinationFields", "RightAscensionFields"
        ],
    ) -> "CoordinatesFields":
        """Subfields should come from the CoordinatesFields class"""
        self._subfields.extend(subfields)
        return self

    def alias(self, alias: str) -> "CoordinatesFields":
        self._alias = alias
        return self


class CreateCallForProposalsResultFields(GraphQLField):
    @classmethod
    def call_for_proposals(cls) -> "CallForProposalsFields":
        return CallForProposalsFields("callForProposals")

    def fields(
        self,
        *subfields: Union[
            CreateCallForProposalsResultGraphQLField, "CallForProposalsFields"
        ],
    ) -> "CreateCallForProposalsResultFields":
        """Subfields should come from the CreateCallForProposalsResultFields class"""
        self._subfields.extend(subfields)
        return self

    def alias(self, alias: str) -> "CreateCallForProposalsResultFields":
        self._alias = alias
        return self


class CreateGroupResultFields(GraphQLField):
    @classmethod
    def group(cls) -> "GroupFields":
        return GroupFields("group")

    def fields(
        self, *subfields: Union[CreateGroupResultGraphQLField, "GroupFields"]
    ) -> "CreateGroupResultFields":
        """Subfields should come from the CreateGroupResultFields class"""
        self._subfields.extend(subfields)
        return self

    def alias(self, alias: str) -> "CreateGroupResultFields":
        self._alias = alias
        return self


class CreateObservationResultFields(GraphQLField):
    @classmethod
    def observation(cls) -> "ObservationFields":
        return ObservationFields("observation")

    def fields(
        self,
        *subfields: Union[CreateObservationResultGraphQLField, "ObservationFields"],
    ) -> "CreateObservationResultFields":
        """Subfields should come from the CreateObservationResultFields class"""
        self._subfields.extend(subfields)
        return self

    def alias(self, alias: str) -> "CreateObservationResultFields":
        self._alias = alias
        return self


class CreateProgramNoteResultFields(GraphQLField):
    @classmethod
    def program_note(cls) -> "ProgramNoteFields":
        return ProgramNoteFields("programNote")

    def fields(
        self,
        *subfields: Union[CreateProgramNoteResultGraphQLField, "ProgramNoteFields"],
    ) -> "CreateProgramNoteResultFields":
        """Subfields should come from the CreateProgramNoteResultFields class"""
        self._subfields.extend(subfields)
        return self

    def alias(self, alias: str) -> "CreateProgramNoteResultFields":
        self._alias = alias
        return self


class CreateProgramResultFields(GraphQLField):
    @classmethod
    def program(cls) -> "ProgramFields":
        return ProgramFields("program")

    def fields(
        self, *subfields: Union[CreateProgramResultGraphQLField, "ProgramFields"]
    ) -> "CreateProgramResultFields":
        """Subfields should come from the CreateProgramResultFields class"""
        self._subfields.extend(subfields)
        return self

    def alias(self, alias: str) -> "CreateProgramResultFields":
        self._alias = alias
        return self


class CreateProposalResultFields(GraphQLField):
    @classmethod
    def proposal(cls) -> "ProposalFields":
        return ProposalFields("proposal")

    def fields(
        self, *subfields: Union[CreateProposalResultGraphQLField, "ProposalFields"]
    ) -> "CreateProposalResultFields":
        """Subfields should come from the CreateProposalResultFields class"""
        self._subfields.extend(subfields)
        return self

    def alias(self, alias: str) -> "CreateProposalResultFields":
        self._alias = alias
        return self


class CreateTargetResultFields(GraphQLField):
    @classmethod
    def target(cls) -> "TargetFields":
        return TargetFields("target")

    def fields(
        self, *subfields: Union[CreateTargetResultGraphQLField, "TargetFields"]
    ) -> "CreateTargetResultFields":
        """Subfields should come from the CreateTargetResultFields class"""
        self._subfields.extend(subfields)
        return self

    def alias(self, alias: str) -> "CreateTargetResultFields":
        self._alias = alias
        return self


class CreateUserInvitationResultFields(GraphQLField):
    @classmethod
    def invitation(cls) -> "UserInvitationFields":
        return UserInvitationFields("invitation")

    key: "CreateUserInvitationResultGraphQLField" = (
        CreateUserInvitationResultGraphQLField("key")
    )

    def fields(
        self,
        *subfields: Union[
            CreateUserInvitationResultGraphQLField, "UserInvitationFields"
        ],
    ) -> "CreateUserInvitationResultFields":
        """Subfields should come from the CreateUserInvitationResultFields class"""
        self._subfields.extend(subfields)
        return self

    def alias(self, alias: str) -> "CreateUserInvitationResultFields":
        self._alias = alias
        return self


class DarkFields(GraphQLField):
    step_type: "DarkGraphQLField" = DarkGraphQLField("stepType")

    def fields(self, *subfields: DarkGraphQLField) -> "DarkFields":
        """Subfields should come from the DarkFields class"""
        self._subfields.extend(subfields)
        return self

    def alias(self, alias: str) -> "DarkFields":
        self._alias = alias
        return self


class DatasetFields(GraphQLField):
    id: "DatasetGraphQLField" = DatasetGraphQLField("id")

    @classmethod
    def step(cls) -> "StepRecordFields":
        return StepRecordFields("step")

    index: "DatasetGraphQLField" = DatasetGraphQLField("index")

    @classmethod
    def reference(cls) -> "DatasetReferenceFields":
        return DatasetReferenceFields("reference")

    @classmethod
    def observation(cls) -> "ObservationFields":
        return ObservationFields("observation")

    @classmethod
    def visit(cls) -> "VisitFields":
        return VisitFields("visit")

    @classmethod
    def events(
        cls, *, offset: Optional[Any] = None, limit: Optional[Any] = None
    ) -> "ExecutionEventSelectResultFields":
        arguments: dict[str, dict[str, Any]] = {
            "OFFSET": {"type": "ExecutionEventId", "value": offset},
            "LIMIT": {"type": "NonNegInt", "value": limit},
        }
        cleared_arguments = {
            key: value for key, value in arguments.items() if value["value"] is not None
        }
        return ExecutionEventSelectResultFields("events", arguments=cleared_arguments)

    filename: "DatasetGraphQLField" = DatasetGraphQLField("filename")
    qa_state: "DatasetGraphQLField" = DatasetGraphQLField("qaState")
    comment: "DatasetGraphQLField" = DatasetGraphQLField("comment")
    idempotency_key: "DatasetGraphQLField" = DatasetGraphQLField("idempotencyKey")

    @classmethod
    def interval(cls) -> "TimestampIntervalFields":
        return TimestampIntervalFields("interval")

    is_written: "DatasetGraphQLField" = DatasetGraphQLField("isWritten")

    def fields(
        self,
        *subfields: Union[
            DatasetGraphQLField,
            "DatasetReferenceFields",
            "ExecutionEventSelectResultFields",
            "ObservationFields",
            "StepRecordFields",
            "TimestampIntervalFields",
            "VisitFields",
        ],
    ) -> "DatasetFields":
        """Subfields should come from the DatasetFields class"""
        self._subfields.extend(subfields)
        return self

    def alias(self, alias: str) -> "DatasetFields":
        self._alias = alias
        return self


class DatasetChronicleEntryFields(GraphQLField):
    id: "DatasetChronicleEntryGraphQLField" = DatasetChronicleEntryGraphQLField("id")
    transaction_id: "DatasetChronicleEntryGraphQLField" = (
        DatasetChronicleEntryGraphQLField("transactionId")
    )

    @classmethod
    def user(cls) -> "UserFields":
        return UserFields("user")

    timestamp: "DatasetChronicleEntryGraphQLField" = DatasetChronicleEntryGraphQLField(
        "timestamp"
    )
    operation: "DatasetChronicleEntryGraphQLField" = DatasetChronicleEntryGraphQLField(
        "operation"
    )

    @classmethod
    def dataset(cls) -> "DatasetFields":
        return DatasetFields("dataset")

    mod_dataset_id: "DatasetChronicleEntryGraphQLField" = (
        DatasetChronicleEntryGraphQLField("modDatasetId")
    )
    mod_step_id: "DatasetChronicleEntryGraphQLField" = (
        DatasetChronicleEntryGraphQLField("modStepId")
    )
    mod_observation_id: "DatasetChronicleEntryGraphQLField" = (
        DatasetChronicleEntryGraphQLField("modObservationId")
    )
    mod_visit_id: "DatasetChronicleEntryGraphQLField" = (
        DatasetChronicleEntryGraphQLField("modVisitId")
    )
    mod_reference: "DatasetChronicleEntryGraphQLField" = (
        DatasetChronicleEntryGraphQLField("modReference")
    )
    mod_filename: "DatasetChronicleEntryGraphQLField" = (
        DatasetChronicleEntryGraphQLField("modFilename")
    )
    mod_qa_state: "DatasetChronicleEntryGraphQLField" = (
        DatasetChronicleEntryGraphQLField("modQaState")
    )
    mod_interval: "DatasetChronicleEntryGraphQLField" = (
        DatasetChronicleEntryGraphQLField("modInterval")
    )
    mod_comment: "DatasetChronicleEntryGraphQLField" = (
        DatasetChronicleEntryGraphQLField("modComment")
    )
    new_dataset_id: "DatasetChronicleEntryGraphQLField" = (
        DatasetChronicleEntryGraphQLField("newDatasetId")
    )
    new_step_id: "DatasetChronicleEntryGraphQLField" = (
        DatasetChronicleEntryGraphQLField("newStepId")
    )
    new_observation_id: "DatasetChronicleEntryGraphQLField" = (
        DatasetChronicleEntryGraphQLField("newObservationId")
    )
    new_visit_id: "DatasetChronicleEntryGraphQLField" = (
        DatasetChronicleEntryGraphQLField("newVisitId")
    )
    new_reference: "DatasetChronicleEntryGraphQLField" = (
        DatasetChronicleEntryGraphQLField("newReference")
    )
    new_filename: "DatasetChronicleEntryGraphQLField" = (
        DatasetChronicleEntryGraphQLField("newFilename")
    )
    new_qa_state: "DatasetChronicleEntryGraphQLField" = (
        DatasetChronicleEntryGraphQLField("newQaState")
    )

    @classmethod
    def new_interval(cls) -> "TimestampIntervalFields":
        return TimestampIntervalFields("newInterval")

    new_comment: "DatasetChronicleEntryGraphQLField" = (
        DatasetChronicleEntryGraphQLField("newComment")
    )

    def fields(
        self,
        *subfields: Union[
            DatasetChronicleEntryGraphQLField,
            "DatasetFields",
            "TimestampIntervalFields",
            "UserFields",
        ],
    ) -> "DatasetChronicleEntryFields":
        """Subfields should come from the DatasetChronicleEntryFields class"""
        self._subfields.extend(subfields)
        return self

    def alias(self, alias: str) -> "DatasetChronicleEntryFields":
        self._alias = alias
        return self


class DatasetChronicleEntrySelectResultFields(GraphQLField):
    @classmethod
    def matches(cls) -> "DatasetChronicleEntryFields":
        return DatasetChronicleEntryFields("matches")

    has_more: "DatasetChronicleEntrySelectResultGraphQLField" = (
        DatasetChronicleEntrySelectResultGraphQLField("hasMore")
    )

    def fields(
        self,
        *subfields: Union[
            DatasetChronicleEntrySelectResultGraphQLField, "DatasetChronicleEntryFields"
        ],
    ) -> "DatasetChronicleEntrySelectResultFields":
        """Subfields should come from the DatasetChronicleEntrySelectResultFields class"""
        self._subfields.extend(subfields)
        return self

    def alias(self, alias: str) -> "DatasetChronicleEntrySelectResultFields":
        self._alias = alias
        return self


class DatasetEstimateFields(GraphQLField):
    @classmethod
    def exposure(cls) -> "TimeSpanFields":
        return TimeSpanFields("exposure")

    @classmethod
    def readout(cls) -> "TimeSpanFields":
        return TimeSpanFields("readout")

    @classmethod
    def write(cls) -> "TimeSpanFields":
        return TimeSpanFields("write")

    @classmethod
    def estimate(cls) -> "TimeSpanFields":
        return TimeSpanFields("estimate")

    def fields(
        self, *subfields: Union[DatasetEstimateGraphQLField, "TimeSpanFields"]
    ) -> "DatasetEstimateFields":
        """Subfields should come from the DatasetEstimateFields class"""
        self._subfields.extend(subfields)
        return self

    def alias(self, alias: str) -> "DatasetEstimateFields":
        self._alias = alias
        return self


class DatasetEventFields(GraphQLField):
    id: "DatasetEventGraphQLField" = DatasetEventGraphQLField("id")

    @classmethod
    def visit(cls) -> "VisitFields":
        return VisitFields("visit")

    @classmethod
    def observation(cls) -> "ObservationFields":
        return ObservationFields("observation")

    recorded_time: "DatasetEventGraphQLField" = DatasetEventGraphQLField("recordedTime")
    received: "DatasetEventGraphQLField" = DatasetEventGraphQLField("received")
    client_time: "DatasetEventGraphQLField" = DatasetEventGraphQLField("clientTime")
    effective_time: "DatasetEventGraphQLField" = DatasetEventGraphQLField(
        "effectiveTime"
    )
    event_type: "DatasetEventGraphQLField" = DatasetEventGraphQLField("eventType")

    @classmethod
    def atom(cls) -> "AtomRecordFields":
        return AtomRecordFields("atom")

    @classmethod
    def step(cls) -> "StepRecordFields":
        return StepRecordFields("step")

    dataset_stage: "DatasetEventGraphQLField" = DatasetEventGraphQLField("datasetStage")

    @classmethod
    def dataset(cls) -> "DatasetFields":
        return DatasetFields("dataset")

    idempotency_key: "DatasetEventGraphQLField" = DatasetEventGraphQLField(
        "idempotencyKey"
    )

    def fields(
        self,
        *subfields: Union[
            DatasetEventGraphQLField,
            "AtomRecordFields",
            "DatasetFields",
            "ObservationFields",
            "StepRecordFields",
            "VisitFields",
        ],
    ) -> "DatasetEventFields":
        """Subfields should come from the DatasetEventFields class"""
        self._subfields.extend(subfields)
        return self

    def alias(self, alias: str) -> "DatasetEventFields":
        self._alias = alias
        return self


class DatasetReferenceFields(GraphQLField):
    label: "DatasetReferenceGraphQLField" = DatasetReferenceGraphQLField("label")

    @classmethod
    def observation(cls) -> "ObservationReferenceFields":
        return ObservationReferenceFields("observation")

    step_index: "DatasetReferenceGraphQLField" = DatasetReferenceGraphQLField(
        "stepIndex"
    )
    exposure_index: "DatasetReferenceGraphQLField" = DatasetReferenceGraphQLField(
        "exposureIndex"
    )

    def fields(
        self,
        *subfields: Union[DatasetReferenceGraphQLField, "ObservationReferenceFields"],
    ) -> "DatasetReferenceFields":
        """Subfields should come from the DatasetReferenceFields class"""
        self._subfields.extend(subfields)
        return self

    def alias(self, alias: str) -> "DatasetReferenceFields":
        self._alias = alias
        return self


class DatasetSelectResultFields(GraphQLField):
    @classmethod
    def matches(cls) -> "DatasetFields":
        return DatasetFields("matches")

    has_more: "DatasetSelectResultGraphQLField" = DatasetSelectResultGraphQLField(
        "hasMore"
    )

    def fields(
        self, *subfields: Union[DatasetSelectResultGraphQLField, "DatasetFields"]
    ) -> "DatasetSelectResultFields":
        """Subfields should come from the DatasetSelectResultFields class"""
        self._subfields.extend(subfields)
        return self

    def alias(self, alias: str) -> "DatasetSelectResultFields":
        self._alias = alias
        return self


class DateIntervalFields(GraphQLField):
    start: "DateIntervalGraphQLField" = DateIntervalGraphQLField("start")
    end: "DateIntervalGraphQLField" = DateIntervalGraphQLField("end")

    def fields(self, *subfields: DateIntervalGraphQLField) -> "DateIntervalFields":
        """Subfields should come from the DateIntervalFields class"""
        self._subfields.extend(subfields)
        return self

    def alias(self, alias: str) -> "DateIntervalFields":
        self._alias = alias
        return self


class DeclinationFields(GraphQLField):
    dms: "DeclinationGraphQLField" = DeclinationGraphQLField("dms")
    degrees: "DeclinationGraphQLField" = DeclinationGraphQLField("degrees")
    microarcseconds: "DeclinationGraphQLField" = DeclinationGraphQLField(
        "microarcseconds"
    )

    def fields(self, *subfields: DeclinationGraphQLField) -> "DeclinationFields":
        """Subfields should come from the DeclinationFields class"""
        self._subfields.extend(subfields)
        return self

    def alias(self, alias: str) -> "DeclinationFields":
        self._alias = alias
        return self


class DeclinationArcFields(GraphQLField):
    type_: "DeclinationArcGraphQLField" = DeclinationArcGraphQLField("type")

    @classmethod
    def start(cls) -> "DeclinationFields":
        return DeclinationFields("start")

    @classmethod
    def end(cls) -> "DeclinationFields":
        return DeclinationFields("end")

    def fields(
        self, *subfields: Union[DeclinationArcGraphQLField, "DeclinationFields"]
    ) -> "DeclinationArcFields":
        """Subfields should come from the DeclinationArcFields class"""
        self._subfields.extend(subfields)
        return self

    def alias(self, alias: str) -> "DeclinationArcFields":
        self._alias = alias
        return self


class DeclineTooTriggerResultFields(GraphQLField):
    @classmethod
    def too_trigger(cls) -> "TooTriggerFields":
        return TooTriggerFields("tooTrigger")

    def fields(
        self, *subfields: Union[DeclineTooTriggerResultGraphQLField, "TooTriggerFields"]
    ) -> "DeclineTooTriggerResultFields":
        """Subfields should come from the DeclineTooTriggerResultFields class"""
        self._subfields.extend(subfields)
        return self

    def alias(self, alias: str) -> "DeclineTooTriggerResultFields":
        self._alias = alias
        return self


class DeleteProgramUserResultFields(GraphQLField):
    result: "DeleteProgramUserResultGraphQLField" = DeleteProgramUserResultGraphQLField(
        "result"
    )

    def fields(
        self, *subfields: DeleteProgramUserResultGraphQLField
    ) -> "DeleteProgramUserResultFields":
        """Subfields should come from the DeleteProgramUserResultFields class"""
        self._subfields.extend(subfields)
        return self

    def alias(self, alias: str) -> "DeleteProgramUserResultFields":
        self._alias = alias
        return self


class DeleteProposalResultFields(GraphQLField):
    result: "DeleteProposalResultGraphQLField" = DeleteProposalResultGraphQLField(
        "result"
    )

    def fields(
        self, *subfields: DeleteProposalResultGraphQLField
    ) -> "DeleteProposalResultFields":
        """Subfields should come from the DeleteProposalResultFields class"""
        self._subfields.extend(subfields)
        return self

    def alias(self, alias: str) -> "DeleteProposalResultFields":
        self._alias = alias
        return self


class DeleteSequenceResultFields(GraphQLField):
    @classmethod
    def observation(cls) -> "ObservationFields":
        return ObservationFields("observation")

    def fields(
        self, *subfields: Union[DeleteSequenceResultGraphQLField, "ObservationFields"]
    ) -> "DeleteSequenceResultFields":
        """Subfields should come from the DeleteSequenceResultFields class"""
        self._subfields.extend(subfields)
        return self

    def alias(self, alias: str) -> "DeleteSequenceResultFields":
        self._alias = alias
        return self


class DemoScienceFields(GraphQLField):
    science_subtype: "DemoScienceGraphQLField" = DemoScienceGraphQLField(
        "scienceSubtype"
    )
    too_activation_ceiling: "DemoScienceGraphQLField" = DemoScienceGraphQLField(
        "tooActivationCeiling"
    )
    default_too_activation_ceiling: "DemoScienceGraphQLField" = DemoScienceGraphQLField(
        "defaultTooActivationCeiling"
    )
    explicit_too_activation_ceiling: "DemoScienceGraphQLField" = (
        DemoScienceGraphQLField("explicitTooActivationCeiling")
    )
    min_percent_time: "DemoScienceGraphQLField" = DemoScienceGraphQLField(
        "minPercentTime"
    )

    def fields(self, *subfields: DemoScienceGraphQLField) -> "DemoScienceFields":
        """Subfields should come from the DemoScienceFields class"""
        self._subfields.extend(subfields)
        return self

    def alias(self, alias: str) -> "DemoScienceFields":
        self._alias = alias
        return self


class DetectorEstimateFields(GraphQLField):
    name: "DetectorEstimateGraphQLField" = DetectorEstimateGraphQLField("name")
    description: "DetectorEstimateGraphQLField" = DetectorEstimateGraphQLField(
        "description"
    )

    @classmethod
    def dataset(cls) -> "DatasetEstimateFields":
        return DatasetEstimateFields("dataset")

    count: "DetectorEstimateGraphQLField" = DetectorEstimateGraphQLField("count")

    @classmethod
    def estimate(cls) -> "TimeSpanFields":
        return TimeSpanFields("estimate")

    def fields(
        self,
        *subfields: Union[
            DetectorEstimateGraphQLField, "DatasetEstimateFields", "TimeSpanFields"
        ],
    ) -> "DetectorEstimateFields":
        """Subfields should come from the DetectorEstimateFields class"""
        self._subfields.extend(subfields)
        return self

    def alias(self, alias: str) -> "DetectorEstimateFields":
        self._alias = alias
        return self


class DirectorsTimeFields(GraphQLField):
    science_subtype: "DirectorsTimeGraphQLField" = DirectorsTimeGraphQLField(
        "scienceSubtype"
    )
    too_activation_ceiling: "DirectorsTimeGraphQLField" = DirectorsTimeGraphQLField(
        "tooActivationCeiling"
    )
    default_too_activation_ceiling: "DirectorsTimeGraphQLField" = (
        DirectorsTimeGraphQLField("defaultTooActivationCeiling")
    )
    explicit_too_activation_ceiling: "DirectorsTimeGraphQLField" = (
        DirectorsTimeGraphQLField("explicitTooActivationCeiling")
    )
    min_percent_time: "DirectorsTimeGraphQLField" = DirectorsTimeGraphQLField(
        "minPercentTime"
    )

    def fields(self, *subfields: DirectorsTimeGraphQLField) -> "DirectorsTimeFields":
        """Subfields should come from the DirectorsTimeFields class"""
        self._subfields.extend(subfields)
        return self

    def alias(self, alias: str) -> "DirectorsTimeFields":
        self._alias = alias
        return self


class ElevationRangeFields(GraphQLField):
    @classmethod
    def air_mass(cls) -> "AirMassRangeFields":
        return AirMassRangeFields("airMass")

    @classmethod
    def hour_angle(cls) -> "HourAngleRangeFields":
        return HourAngleRangeFields("hourAngle")

    def fields(
        self,
        *subfields: Union[
            ElevationRangeGraphQLField, "AirMassRangeFields", "HourAngleRangeFields"
        ],
    ) -> "ElevationRangeFields":
        """Subfields should come from the ElevationRangeFields class"""
        self._subfields.extend(subfields)
        return self

    def alias(self, alias: str) -> "ElevationRangeFields":
        self._alias = alias
        return self


class EmailFields(GraphQLField):
    sender_email: "EmailGraphQLField" = EmailGraphQLField("senderEmail")
    recipient_email: "EmailGraphQLField" = EmailGraphQLField("recipientEmail")
    subject: "EmailGraphQLField" = EmailGraphQLField("subject")
    text_message: "EmailGraphQLField" = EmailGraphQLField("textMessage")
    html_message: "EmailGraphQLField" = EmailGraphQLField("htmlMessage")
    original_time: "EmailGraphQLField" = EmailGraphQLField("originalTime")
    status: "EmailGraphQLField" = EmailGraphQLField("status")
    status_time: "EmailGraphQLField" = EmailGraphQLField("statusTime")

    def fields(self, *subfields: EmailGraphQLField) -> "EmailFields":
        """Subfields should come from the EmailFields class"""
        self._subfields.extend(subfields)
        return self

    def alias(self, alias: str) -> "EmailFields":
        self._alias = alias
        return self


class EmissionLineIntegratedFields(GraphQLField):
    @classmethod
    def wavelength(cls) -> "WavelengthFields":
        return WavelengthFields("wavelength")

    line_width: "EmissionLineIntegratedGraphQLField" = (
        EmissionLineIntegratedGraphQLField("lineWidth")
    )

    @classmethod
    def line_flux(cls) -> "LineFluxIntegratedFields":
        return LineFluxIntegratedFields("lineFlux")

    def fields(
        self,
        *subfields: Union[
            EmissionLineIntegratedGraphQLField,
            "LineFluxIntegratedFields",
            "WavelengthFields",
        ],
    ) -> "EmissionLineIntegratedFields":
        """Subfields should come from the EmissionLineIntegratedFields class"""
        self._subfields.extend(subfields)
        return self

    def alias(self, alias: str) -> "EmissionLineIntegratedFields":
        self._alias = alias
        return self


class EmissionLineSurfaceFields(GraphQLField):
    @classmethod
    def wavelength(cls) -> "WavelengthFields":
        return WavelengthFields("wavelength")

    line_width: "EmissionLineSurfaceGraphQLField" = EmissionLineSurfaceGraphQLField(
        "lineWidth"
    )

    @classmethod
    def line_flux(cls) -> "LineFluxSurfaceFields":
        return LineFluxSurfaceFields("lineFlux")

    def fields(
        self,
        *subfields: Union[
            EmissionLineSurfaceGraphQLField, "LineFluxSurfaceFields", "WavelengthFields"
        ],
    ) -> "EmissionLineSurfaceFields":
        """Subfields should come from the EmissionLineSurfaceFields class"""
        self._subfields.extend(subfields)
        return self

    def alias(self, alias: str) -> "EmissionLineSurfaceFields":
        self._alias = alias
        return self


class EmissionLinesIntegratedFields(GraphQLField):
    @classmethod
    def lines(cls) -> "EmissionLineIntegratedFields":
        return EmissionLineIntegratedFields("lines")

    @classmethod
    def flux_density_continuum(cls) -> "FluxDensityContinuumIntegratedFields":
        return FluxDensityContinuumIntegratedFields("fluxDensityContinuum")

    def fields(
        self,
        *subfields: Union[
            EmissionLinesIntegratedGraphQLField,
            "EmissionLineIntegratedFields",
            "FluxDensityContinuumIntegratedFields",
        ],
    ) -> "EmissionLinesIntegratedFields":
        """Subfields should come from the EmissionLinesIntegratedFields class"""
        self._subfields.extend(subfields)
        return self

    def alias(self, alias: str) -> "EmissionLinesIntegratedFields":
        self._alias = alias
        return self


class EmissionLinesSurfaceFields(GraphQLField):
    @classmethod
    def lines(cls) -> "EmissionLineSurfaceFields":
        return EmissionLineSurfaceFields("lines")

    @classmethod
    def flux_density_continuum(cls) -> "FluxDensityContinuumSurfaceFields":
        return FluxDensityContinuumSurfaceFields("fluxDensityContinuum")

    def fields(
        self,
        *subfields: Union[
            EmissionLinesSurfaceGraphQLField,
            "EmissionLineSurfaceFields",
            "FluxDensityContinuumSurfaceFields",
        ],
    ) -> "EmissionLinesSurfaceFields":
        """Subfields should come from the EmissionLinesSurfaceFields class"""
        self._subfields.extend(subfields)
        return self

    def alias(self, alias: str) -> "EmissionLinesSurfaceFields":
        self._alias = alias
        return self


class EngineeringProgramReferenceFields(GraphQLField):
    label: "EngineeringProgramReferenceGraphQLField" = (
        EngineeringProgramReferenceGraphQLField("label")
    )
    type_: "EngineeringProgramReferenceGraphQLField" = (
        EngineeringProgramReferenceGraphQLField("type")
    )
    instrument: "EngineeringProgramReferenceGraphQLField" = (
        EngineeringProgramReferenceGraphQLField("instrument")
    )
    semester: "EngineeringProgramReferenceGraphQLField" = (
        EngineeringProgramReferenceGraphQLField("semester")
    )
    semester_index: "EngineeringProgramReferenceGraphQLField" = (
        EngineeringProgramReferenceGraphQLField("semesterIndex")
    )

    def fields(
        self, *subfields: EngineeringProgramReferenceGraphQLField
    ) -> "EngineeringProgramReferenceFields":
        """Subfields should come from the EngineeringProgramReferenceFields class"""
        self._subfields.extend(subfields)
        return self

    def alias(self, alias: str) -> "EngineeringProgramReferenceFields":
        self._alias = alias
        return self


class EnumeratedTelescopeConfigGeneratorFields(GraphQLField):
    @classmethod
    def values(cls) -> "TelescopeConfigFields":
        return TelescopeConfigFields("values")

    def fields(
        self,
        *subfields: Union[
            EnumeratedTelescopeConfigGeneratorGraphQLField, "TelescopeConfigFields"
        ],
    ) -> "EnumeratedTelescopeConfigGeneratorFields":
        """Subfields should come from the EnumeratedTelescopeConfigGeneratorFields class"""
        self._subfields.extend(subfields)
        return self

    def alias(self, alias: str) -> "EnumeratedTelescopeConfigGeneratorFields":
        self._alias = alias
        return self


class ExampleProgramReferenceFields(GraphQLField):
    label: "ExampleProgramReferenceGraphQLField" = ExampleProgramReferenceGraphQLField(
        "label"
    )
    type_: "ExampleProgramReferenceGraphQLField" = ExampleProgramReferenceGraphQLField(
        "type"
    )
    instrument: "ExampleProgramReferenceGraphQLField" = (
        ExampleProgramReferenceGraphQLField("instrument")
    )

    def fields(
        self, *subfields: ExampleProgramReferenceGraphQLField
    ) -> "ExampleProgramReferenceFields":
        """Subfields should come from the ExampleProgramReferenceFields class"""
        self._subfields.extend(subfields)
        return self

    def alias(self, alias: str) -> "ExampleProgramReferenceFields":
        self._alias = alias
        return self


class ExchangeFields(GraphQLField):
    mode: "ExchangeGraphQLField" = ExchangeGraphQLField("mode")
    keck_instrument: "ExchangeGraphQLField" = ExchangeGraphQLField("keckInstrument")
    subaru_instrument: "ExchangeGraphQLField" = ExchangeGraphQLField("subaruInstrument")

    @classmethod
    def total_request_time(cls) -> "TimeSpanFields":
        return TimeSpanFields("totalRequestTime")

    def fields(
        self, *subfields: Union[ExchangeGraphQLField, "TimeSpanFields"]
    ) -> "ExchangeFields":
        """Subfields should come from the ExchangeFields class"""
        self._subfields.extend(subfields)
        return self

    def alias(self, alias: str) -> "ExchangeFields":
        self._alias = alias
        return self


class ExecutionFields(GraphQLField):
    @classmethod
    def digest(cls) -> "CalculatedExecutionDigestFields":
        return CalculatedExecutionDigestFields("digest")

    execution_state: "ExecutionGraphQLField" = ExecutionGraphQLField("executionState")

    @classmethod
    def atom_records(
        cls, *, offset: Optional[Any] = None, limit: Optional[Any] = None
    ) -> "AtomRecordSelectResultFields":
        arguments: dict[str, dict[str, Any]] = {
            "OFFSET": {"type": "PosInt", "value": offset},
            "LIMIT": {"type": "NonNegInt", "value": limit},
        }
        cleared_arguments = {
            key: value for key, value in arguments.items() if value["value"] is not None
        }
        return AtomRecordSelectResultFields("atomRecords", arguments=cleared_arguments)

    @classmethod
    def datasets(
        cls, *, offset: Optional[Any] = None, limit: Optional[Any] = None
    ) -> "DatasetSelectResultFields":
        arguments: dict[str, dict[str, Any]] = {
            "OFFSET": {"type": "DatasetId", "value": offset},
            "LIMIT": {"type": "NonNegInt", "value": limit},
        }
        cleared_arguments = {
            key: value for key, value in arguments.items() if value["value"] is not None
        }
        return DatasetSelectResultFields("datasets", arguments=cleared_arguments)

    @classmethod
    def events(
        cls, *, offset: Optional[Any] = None, limit: Optional[Any] = None
    ) -> "ExecutionEventSelectResultFields":
        arguments: dict[str, dict[str, Any]] = {
            "OFFSET": {"type": "ExecutionEventId", "value": offset},
            "LIMIT": {"type": "NonNegInt", "value": limit},
        }
        cleared_arguments = {
            key: value for key, value in arguments.items() if value["value"] is not None
        }
        return ExecutionEventSelectResultFields("events", arguments=cleared_arguments)

    @classmethod
    def visits(
        cls, *, offset: Optional[Any] = None, limit: Optional[Any] = None
    ) -> "VisitSelectResultFields":
        arguments: dict[str, dict[str, Any]] = {
            "OFFSET": {"type": "VisitId", "value": offset},
            "LIMIT": {"type": "NonNegInt", "value": limit},
        }
        cleared_arguments = {
            key: value for key, value in arguments.items() if value["value"] is not None
        }
        return VisitSelectResultFields("visits", arguments=cleared_arguments)

    @classmethod
    def original_estimate(cls) -> "ObservationTimeEstimateFields":
        return ObservationTimeEstimateFields("originalEstimate")

    @classmethod
    def time_charge(cls) -> "CategorizedTimeFields":
        return CategorizedTimeFields("timeCharge")

    science_sequence_is_materialized: "ExecutionGraphQLField" = ExecutionGraphQLField(
        "scienceSequenceIsMaterialized"
    )
    acquisition_sequence_is_materialized: "ExecutionGraphQLField" = (
        ExecutionGraphQLField("acquisitionSequenceIsMaterialized")
    )

    def fields(
        self,
        *subfields: Union[
            ExecutionGraphQLField,
            "AtomRecordSelectResultFields",
            "CalculatedExecutionDigestFields",
            "CategorizedTimeFields",
            "DatasetSelectResultFields",
            "ExecutionEventSelectResultFields",
            "ObservationTimeEstimateFields",
            "VisitSelectResultFields",
        ],
    ) -> "ExecutionFields":
        """Subfields should come from the ExecutionFields class"""
        self._subfields.extend(subfields)
        return self

    def alias(self, alias: str) -> "ExecutionFields":
        self._alias = alias
        return self


class ExecutionConfigFields(GraphQLField):
    instrument: "ExecutionConfigGraphQLField" = ExecutionConfigGraphQLField(
        "instrument"
    )

    @classmethod
    def flamingos_2(cls) -> "Flamingos2ExecutionConfigFields":
        return Flamingos2ExecutionConfigFields("flamingos2")

    @classmethod
    def ghost(cls) -> "GhostExecutionConfigFields":
        return GhostExecutionConfigFields("ghost")

    @classmethod
    def gmos_north(cls) -> "GmosNorthExecutionConfigFields":
        return GmosNorthExecutionConfigFields("gmosNorth")

    @classmethod
    def gmos_south(cls) -> "GmosSouthExecutionConfigFields":
        return GmosSouthExecutionConfigFields("gmosSouth")

    @classmethod
    def gnirs(cls) -> "GnirsExecutionConfigFields":
        return GnirsExecutionConfigFields("gnirs")

    @classmethod
    def igrins_2(cls) -> "Igrins2ExecutionConfigFields":
        return Igrins2ExecutionConfigFields("igrins2")

    def fields(
        self,
        *subfields: Union[
            ExecutionConfigGraphQLField,
            "Flamingos2ExecutionConfigFields",
            "GhostExecutionConfigFields",
            "GmosNorthExecutionConfigFields",
            "GmosSouthExecutionConfigFields",
            "GnirsExecutionConfigFields",
            "Igrins2ExecutionConfigFields",
        ],
    ) -> "ExecutionConfigFields":
        """Subfields should come from the ExecutionConfigFields class"""
        self._subfields.extend(subfields)
        return self

    def alias(self, alias: str) -> "ExecutionConfigFields":
        self._alias = alias
        return self


class ExecutionDigestFields(GraphQLField):
    @classmethod
    def estimate(cls) -> "ObservationTimeEstimateFields":
        return ObservationTimeEstimateFields("estimate")

    @classmethod
    def setup(cls) -> "SetupTimeFields":
        return SetupTimeFields("setup")

    setup_count: "ExecutionDigestGraphQLField" = ExecutionDigestGraphQLField(
        "setupCount"
    )

    @classmethod
    def acquisition(cls) -> "SequenceDigestFields":
        return SequenceDigestFields("acquisition")

    @classmethod
    def science(cls) -> "SequenceDigestFields":
        return SequenceDigestFields("science")

    @classmethod
    def full_time_estimate(cls) -> "CategorizedTimeFields":
        return CategorizedTimeFields("fullTimeEstimate")

    def fields(
        self,
        *subfields: Union[
            ExecutionDigestGraphQLField,
            "CategorizedTimeFields",
            "ObservationTimeEstimateFields",
            "SequenceDigestFields",
            "SetupTimeFields",
        ],
    ) -> "ExecutionDigestFields":
        """Subfields should come from the ExecutionDigestFields class"""
        self._subfields.extend(subfields)
        return self

    def alias(self, alias: str) -> "ExecutionDigestFields":
        self._alias = alias
        return self


class ExecutionEventInterface(GraphQLField):
    id: "ExecutionEventGraphQLField" = ExecutionEventGraphQLField("id")

    @classmethod
    def visit(cls) -> "VisitFields":
        return VisitFields("visit")

    @classmethod
    def observation(cls) -> "ObservationFields":
        return ObservationFields("observation")

    recorded_time: "ExecutionEventGraphQLField" = ExecutionEventGraphQLField(
        "recordedTime"
    )
    received: "ExecutionEventGraphQLField" = ExecutionEventGraphQLField("received")
    client_time: "ExecutionEventGraphQLField" = ExecutionEventGraphQLField("clientTime")
    effective_time: "ExecutionEventGraphQLField" = ExecutionEventGraphQLField(
        "effectiveTime"
    )
    event_type: "ExecutionEventGraphQLField" = ExecutionEventGraphQLField("eventType")
    idempotency_key: "ExecutionEventGraphQLField" = ExecutionEventGraphQLField(
        "idempotencyKey"
    )

    def fields(
        self,
        *subfields: Union[
            ExecutionEventGraphQLField, "ObservationFields", "VisitFields"
        ],
    ) -> "ExecutionEventInterface":
        """Subfields should come from the ExecutionEventInterface class"""
        self._subfields.extend(subfields)
        return self

    def alias(self, alias: str) -> "ExecutionEventInterface":
        self._alias = alias
        return self

    def on(self, type_name: str, *subfields: GraphQLField) -> "ExecutionEventInterface":
        self._inline_fragments[type_name] = subfields
        return self


class ExecutionEventSelectResultFields(GraphQLField):
    @classmethod
    def matches(cls) -> "ExecutionEventInterface":
        return ExecutionEventInterface("matches")

    has_more: "ExecutionEventSelectResultGraphQLField" = (
        ExecutionEventSelectResultGraphQLField("hasMore")
    )

    def fields(
        self,
        *subfields: Union[
            ExecutionEventSelectResultGraphQLField, "ExecutionEventInterface"
        ],
    ) -> "ExecutionEventSelectResultFields":
        """Subfields should come from the ExecutionEventSelectResultFields class"""
        self._subfields.extend(subfields)
        return self

    def alias(self, alias: str) -> "ExecutionEventSelectResultFields":
        self._alias = alias
        return self


class ExposureTimeModeFields(GraphQLField):
    @classmethod
    def signal_to_noise(cls) -> "SignalToNoiseExposureTimeModeFields":
        return SignalToNoiseExposureTimeModeFields("signalToNoise")

    @classmethod
    def time_and_count(cls) -> "TimeAndCountExposureTimeModeFields":
        return TimeAndCountExposureTimeModeFields("timeAndCount")

    def fields(
        self,
        *subfields: Union[
            ExposureTimeModeGraphQLField,
            "SignalToNoiseExposureTimeModeFields",
            "TimeAndCountExposureTimeModeFields",
        ],
    ) -> "ExposureTimeModeFields":
        """Subfields should come from the ExposureTimeModeFields class"""
        self._subfields.extend(subfields)
        return self

    def alias(self, alias: str) -> "ExposureTimeModeFields":
        self._alias = alias
        return self


class FastTurnaroundFields(GraphQLField):
    science_subtype: "FastTurnaroundGraphQLField" = FastTurnaroundGraphQLField(
        "scienceSubtype"
    )
    too_activation_ceiling: "FastTurnaroundGraphQLField" = FastTurnaroundGraphQLField(
        "tooActivationCeiling"
    )
    default_too_activation_ceiling: "FastTurnaroundGraphQLField" = (
        FastTurnaroundGraphQLField("defaultTooActivationCeiling")
    )
    explicit_too_activation_ceiling: "FastTurnaroundGraphQLField" = (
        FastTurnaroundGraphQLField("explicitTooActivationCeiling")
    )
    min_percent_time: "FastTurnaroundGraphQLField" = FastTurnaroundGraphQLField(
        "minPercentTime"
    )

    @classmethod
    def reviewer(cls) -> "ProgramUserFields":
        return ProgramUserFields("reviewer")

    @classmethod
    def mentor(cls) -> "ProgramUserFields":
        return ProgramUserFields("mentor")

    def fields(
        self, *subfields: Union[FastTurnaroundGraphQLField, "ProgramUserFields"]
    ) -> "FastTurnaroundFields":
        """Subfields should come from the FastTurnaroundFields class"""
        self._subfields.extend(subfields)
        return self

    def alias(self, alias: str) -> "FastTurnaroundFields":
        self._alias = alias
        return self


class Flamingos2AtomFields(GraphQLField):
    id: "Flamingos2AtomGraphQLField" = Flamingos2AtomGraphQLField("id")
    description: "Flamingos2AtomGraphQLField" = Flamingos2AtomGraphQLField(
        "description"
    )
    observe_class: "Flamingos2AtomGraphQLField" = Flamingos2AtomGraphQLField(
        "observeClass"
    )

    @classmethod
    def steps(cls) -> "Flamingos2StepFields":
        return Flamingos2StepFields("steps")

    def fields(
        self, *subfields: Union[Flamingos2AtomGraphQLField, "Flamingos2StepFields"]
    ) -> "Flamingos2AtomFields":
        """Subfields should come from the Flamingos2AtomFields class"""
        self._subfields.extend(subfields)
        return self

    def alias(self, alias: str) -> "Flamingos2AtomFields":
        self._alias = alias
        return self


class Flamingos2CustomMaskFields(GraphQLField):
    attachment_id: "Flamingos2CustomMaskGraphQLField" = (
        Flamingos2CustomMaskGraphQLField("attachmentId")
    )
    slit_width: "Flamingos2CustomMaskGraphQLField" = Flamingos2CustomMaskGraphQLField(
        "slitWidth"
    )

    def fields(
        self, *subfields: Flamingos2CustomMaskGraphQLField
    ) -> "Flamingos2CustomMaskFields":
        """Subfields should come from the Flamingos2CustomMaskFields class"""
        self._subfields.extend(subfields)
        return self

    def alias(self, alias: str) -> "Flamingos2CustomMaskFields":
        self._alias = alias
        return self


class Flamingos2DynamicFields(GraphQLField):
    @classmethod
    def exposure(cls) -> "TimeSpanFields":
        return TimeSpanFields("exposure")

    disperser: "Flamingos2DynamicGraphQLField" = Flamingos2DynamicGraphQLField(
        "disperser"
    )
    filter_: "Flamingos2DynamicGraphQLField" = Flamingos2DynamicGraphQLField("filter")
    read_mode: "Flamingos2DynamicGraphQLField" = Flamingos2DynamicGraphQLField(
        "readMode"
    )
    lyot_wheel: "Flamingos2DynamicGraphQLField" = Flamingos2DynamicGraphQLField(
        "lyotWheel"
    )

    @classmethod
    def fpu(cls) -> "Flamingos2FpuMaskFields":
        return Flamingos2FpuMaskFields("fpu")

    decker: "Flamingos2DynamicGraphQLField" = Flamingos2DynamicGraphQLField("decker")
    readout_mode: "Flamingos2DynamicGraphQLField" = Flamingos2DynamicGraphQLField(
        "readoutMode"
    )
    reads: "Flamingos2DynamicGraphQLField" = Flamingos2DynamicGraphQLField("reads")

    @classmethod
    def central_wavelength(cls) -> "WavelengthFields":
        return WavelengthFields("centralWavelength")

    def fields(
        self,
        *subfields: Union[
            Flamingos2DynamicGraphQLField,
            "Flamingos2FpuMaskFields",
            "TimeSpanFields",
            "WavelengthFields",
        ],
    ) -> "Flamingos2DynamicFields":
        """Subfields should come from the Flamingos2DynamicFields class"""
        self._subfields.extend(subfields)
        return self

    def alias(self, alias: str) -> "Flamingos2DynamicFields":
        self._alias = alias
        return self


class Flamingos2ExecutionConfigFields(GraphQLField):
    @classmethod
    def static(cls) -> "Flamingos2StaticFields":
        return Flamingos2StaticFields("static")

    @classmethod
    def acquisition(cls) -> "Flamingos2ExecutionSequenceFields":
        return Flamingos2ExecutionSequenceFields("acquisition")

    @classmethod
    def science(cls) -> "Flamingos2ExecutionSequenceFields":
        return Flamingos2ExecutionSequenceFields("science")

    def fields(
        self,
        *subfields: Union[
            Flamingos2ExecutionConfigGraphQLField,
            "Flamingos2ExecutionSequenceFields",
            "Flamingos2StaticFields",
        ],
    ) -> "Flamingos2ExecutionConfigFields":
        """Subfields should come from the Flamingos2ExecutionConfigFields class"""
        self._subfields.extend(subfields)
        return self

    def alias(self, alias: str) -> "Flamingos2ExecutionConfigFields":
        self._alias = alias
        return self


class Flamingos2ExecutionSequenceFields(GraphQLField):
    @classmethod
    def next_atom(cls) -> "Flamingos2AtomFields":
        return Flamingos2AtomFields("nextAtom")

    @classmethod
    def possible_future(cls) -> "Flamingos2AtomFields":
        return Flamingos2AtomFields("possibleFuture")

    has_more: "Flamingos2ExecutionSequenceGraphQLField" = (
        Flamingos2ExecutionSequenceGraphQLField("hasMore")
    )

    def fields(
        self,
        *subfields: Union[
            Flamingos2ExecutionSequenceGraphQLField, "Flamingos2AtomFields"
        ],
    ) -> "Flamingos2ExecutionSequenceFields":
        """Subfields should come from the Flamingos2ExecutionSequenceFields class"""
        self._subfields.extend(subfields)
        return self

    def alias(self, alias: str) -> "Flamingos2ExecutionSequenceFields":
        self._alias = alias
        return self


class Flamingos2FpuMaskFields(GraphQLField):
    @classmethod
    def custom_mask(cls) -> "Flamingos2CustomMaskFields":
        return Flamingos2CustomMaskFields("customMask")

    builtin: "Flamingos2FpuMaskGraphQLField" = Flamingos2FpuMaskGraphQLField("builtin")

    def fields(
        self,
        *subfields: Union[Flamingos2FpuMaskGraphQLField, "Flamingos2CustomMaskFields"],
    ) -> "Flamingos2FpuMaskFields":
        """Subfields should come from the Flamingos2FpuMaskFields class"""
        self._subfields.extend(subfields)
        return self

    def alias(self, alias: str) -> "Flamingos2FpuMaskFields":
        self._alias = alias
        return self


class Flamingos2ImagingFields(GraphQLField):
    @classmethod
    def variant(cls) -> "ImagingVariantFields":
        return ImagingVariantFields("variant")

    @classmethod
    def filters(cls) -> "Flamingos2ImagingFilterFields":
        return Flamingos2ImagingFilterFields("filters")

    @classmethod
    def initial_filters(cls) -> "Flamingos2ImagingFilterFields":
        return Flamingos2ImagingFilterFields("initialFilters")

    default_read_mode: "Flamingos2ImagingGraphQLField" = Flamingos2ImagingGraphQLField(
        "defaultReadMode"
    )
    explicit_read_mode: "Flamingos2ImagingGraphQLField" = Flamingos2ImagingGraphQLField(
        "explicitReadMode"
    )
    default_reads: "Flamingos2ImagingGraphQLField" = Flamingos2ImagingGraphQLField(
        "defaultReads"
    )
    explicit_reads: "Flamingos2ImagingGraphQLField" = Flamingos2ImagingGraphQLField(
        "explicitReads"
    )
    decker: "Flamingos2ImagingGraphQLField" = Flamingos2ImagingGraphQLField("decker")
    default_decker: "Flamingos2ImagingGraphQLField" = Flamingos2ImagingGraphQLField(
        "defaultDecker"
    )
    explicit_decker: "Flamingos2ImagingGraphQLField" = Flamingos2ImagingGraphQLField(
        "explicitDecker"
    )
    readout_mode: "Flamingos2ImagingGraphQLField" = Flamingos2ImagingGraphQLField(
        "readoutMode"
    )
    default_readout_mode: "Flamingos2ImagingGraphQLField" = (
        Flamingos2ImagingGraphQLField("defaultReadoutMode")
    )
    explicit_readout_mode: "Flamingos2ImagingGraphQLField" = (
        Flamingos2ImagingGraphQLField("explicitReadoutMode")
    )

    def fields(
        self,
        *subfields: Union[
            Flamingos2ImagingGraphQLField,
            "Flamingos2ImagingFilterFields",
            "ImagingVariantFields",
        ],
    ) -> "Flamingos2ImagingFields":
        """Subfields should come from the Flamingos2ImagingFields class"""
        self._subfields.extend(subfields)
        return self

    def alias(self, alias: str) -> "Flamingos2ImagingFields":
        self._alias = alias
        return self


class Flamingos2ImagingFilterFields(GraphQLField):
    filter_: "Flamingos2ImagingFilterGraphQLField" = (
        Flamingos2ImagingFilterGraphQLField("filter")
    )

    @classmethod
    def exposure_time_mode(cls) -> "ExposureTimeModeFields":
        return ExposureTimeModeFields("exposureTimeMode")

    def fields(
        self,
        *subfields: Union[
            Flamingos2ImagingFilterGraphQLField, "ExposureTimeModeFields"
        ],
    ) -> "Flamingos2ImagingFilterFields":
        """Subfields should come from the Flamingos2ImagingFilterFields class"""
        self._subfields.extend(subfields)
        return self

    def alias(self, alias: str) -> "Flamingos2ImagingFilterFields":
        self._alias = alias
        return self


class Flamingos2LongSlitFields(GraphQLField):
    disperser: "Flamingos2LongSlitGraphQLField" = Flamingos2LongSlitGraphQLField(
        "disperser"
    )
    filter_: "Flamingos2LongSlitGraphQLField" = Flamingos2LongSlitGraphQLField("filter")
    fpu: "Flamingos2LongSlitGraphQLField" = Flamingos2LongSlitGraphQLField("fpu")

    @classmethod
    def exposure_time_mode(cls) -> "ExposureTimeModeFields":
        return ExposureTimeModeFields("exposureTimeMode")

    explicit_read_mode: "Flamingos2LongSlitGraphQLField" = (
        Flamingos2LongSlitGraphQLField("explicitReadMode")
    )
    explicit_reads: "Flamingos2LongSlitGraphQLField" = Flamingos2LongSlitGraphQLField(
        "explicitReads"
    )
    decker: "Flamingos2LongSlitGraphQLField" = Flamingos2LongSlitGraphQLField("decker")
    default_decker: "Flamingos2LongSlitGraphQLField" = Flamingos2LongSlitGraphQLField(
        "defaultDecker"
    )
    explicit_decker: "Flamingos2LongSlitGraphQLField" = Flamingos2LongSlitGraphQLField(
        "explicitDecker"
    )
    readout_mode: "Flamingos2LongSlitGraphQLField" = Flamingos2LongSlitGraphQLField(
        "readoutMode"
    )
    default_readout_mode: "Flamingos2LongSlitGraphQLField" = (
        Flamingos2LongSlitGraphQLField("defaultReadoutMode")
    )
    explicit_readout_mode: "Flamingos2LongSlitGraphQLField" = (
        Flamingos2LongSlitGraphQLField("explicitReadoutMode")
    )

    @classmethod
    def telescope_configs(cls) -> "SlitTelescopeConfigsFields":
        return SlitTelescopeConfigsFields("telescopeConfigs")

    @classmethod
    def default_telescope_configs(cls) -> "SlitTelescopeConfigsFields":
        return SlitTelescopeConfigsFields("defaultTelescopeConfigs")

    @classmethod
    def explicit_telescope_configs(cls) -> "SlitTelescopeConfigsFields":
        return SlitTelescopeConfigsFields("explicitTelescopeConfigs")

    @classmethod
    def telluric_type(cls) -> "TelluricTypeFields":
        return TelluricTypeFields("telluricType")

    @classmethod
    def acquisition(cls) -> "Flamingos2LongSlitAcquisitionFields":
        return Flamingos2LongSlitAcquisitionFields("acquisition")

    initial_disperser: "Flamingos2LongSlitGraphQLField" = (
        Flamingos2LongSlitGraphQLField("initialDisperser")
    )
    initial_filter: "Flamingos2LongSlitGraphQLField" = Flamingos2LongSlitGraphQLField(
        "initialFilter"
    )
    initial_fpu: "Flamingos2LongSlitGraphQLField" = Flamingos2LongSlitGraphQLField(
        "initialFpu"
    )

    def fields(
        self,
        *subfields: Union[
            Flamingos2LongSlitGraphQLField,
            "ExposureTimeModeFields",
            "Flamingos2LongSlitAcquisitionFields",
            "SlitTelescopeConfigsFields",
            "TelluricTypeFields",
        ],
    ) -> "Flamingos2LongSlitFields":
        """Subfields should come from the Flamingos2LongSlitFields class"""
        self._subfields.extend(subfields)
        return self

    def alias(self, alias: str) -> "Flamingos2LongSlitFields":
        self._alias = alias
        return self


class Flamingos2LongSlitAcquisitionFields(GraphQLField):
    filter_: "Flamingos2LongSlitAcquisitionGraphQLField" = (
        Flamingos2LongSlitAcquisitionGraphQLField("filter")
    )
    default_filter: "Flamingos2LongSlitAcquisitionGraphQLField" = (
        Flamingos2LongSlitAcquisitionGraphQLField("defaultFilter")
    )
    explicit_filter: "Flamingos2LongSlitAcquisitionGraphQLField" = (
        Flamingos2LongSlitAcquisitionGraphQLField("explicitFilter")
    )

    @classmethod
    def exposure_time_mode(cls) -> "ExposureTimeModeFields":
        return ExposureTimeModeFields("exposureTimeMode")

    def fields(
        self,
        *subfields: Union[
            Flamingos2LongSlitAcquisitionGraphQLField, "ExposureTimeModeFields"
        ],
    ) -> "Flamingos2LongSlitAcquisitionFields":
        """Subfields should come from the Flamingos2LongSlitAcquisitionFields class"""
        self._subfields.extend(subfields)
        return self

    def alias(self, alias: str) -> "Flamingos2LongSlitAcquisitionFields":
        self._alias = alias
        return self


class Flamingos2StaticFields(GraphQLField):
    mos_pre_imaging: "Flamingos2StaticGraphQLField" = Flamingos2StaticGraphQLField(
        "mosPreImaging"
    )
    use_electronic_offsetting: "Flamingos2StaticGraphQLField" = (
        Flamingos2StaticGraphQLField("useElectronicOffsetting")
    )

    def fields(
        self, *subfields: Flamingos2StaticGraphQLField
    ) -> "Flamingos2StaticFields":
        """Subfields should come from the Flamingos2StaticFields class"""
        self._subfields.extend(subfields)
        return self

    def alias(self, alias: str) -> "Flamingos2StaticFields":
        self._alias = alias
        return self


class Flamingos2StepFields(GraphQLField):
    @classmethod
    def instrument_config(cls) -> "Flamingos2DynamicFields":
        return Flamingos2DynamicFields("instrumentConfig")

    id: "Flamingos2StepGraphQLField" = Flamingos2StepGraphQLField("id")
    breakpoint: "Flamingos2StepGraphQLField" = Flamingos2StepGraphQLField("breakpoint")

    @classmethod
    def step_config(cls) -> "StepConfigInterface":
        return StepConfigInterface("stepConfig")

    @classmethod
    def telescope_config(cls) -> "TelescopeConfigFields":
        return TelescopeConfigFields("telescopeConfig")

    @classmethod
    def estimate(cls) -> "StepEstimateFields":
        return StepEstimateFields("estimate")

    observe_class: "Flamingos2StepGraphQLField" = Flamingos2StepGraphQLField(
        "observeClass"
    )

    def fields(
        self,
        *subfields: Union[
            Flamingos2StepGraphQLField,
            "Flamingos2DynamicFields",
            "StepConfigInterface",
            "StepEstimateFields",
            "TelescopeConfigFields",
        ],
    ) -> "Flamingos2StepFields":
        """Subfields should come from the Flamingos2StepFields class"""
        self._subfields.extend(subfields)
        return self

    def alias(self, alias: str) -> "Flamingos2StepFields":
        self._alias = alias
        return self


class FluxDensityContinuumIntegratedFields(GraphQLField):
    value: "FluxDensityContinuumIntegratedGraphQLField" = (
        FluxDensityContinuumIntegratedGraphQLField("value")
    )
    units: "FluxDensityContinuumIntegratedGraphQLField" = (
        FluxDensityContinuumIntegratedGraphQLField("units")
    )
    error: "FluxDensityContinuumIntegratedGraphQLField" = (
        FluxDensityContinuumIntegratedGraphQLField("error")
    )

    def fields(
        self, *subfields: FluxDensityContinuumIntegratedGraphQLField
    ) -> "FluxDensityContinuumIntegratedFields":
        """Subfields should come from the FluxDensityContinuumIntegratedFields class"""
        self._subfields.extend(subfields)
        return self

    def alias(self, alias: str) -> "FluxDensityContinuumIntegratedFields":
        self._alias = alias
        return self


class FluxDensityContinuumSurfaceFields(GraphQLField):
    value: "FluxDensityContinuumSurfaceGraphQLField" = (
        FluxDensityContinuumSurfaceGraphQLField("value")
    )
    units: "FluxDensityContinuumSurfaceGraphQLField" = (
        FluxDensityContinuumSurfaceGraphQLField("units")
    )
    error: "FluxDensityContinuumSurfaceGraphQLField" = (
        FluxDensityContinuumSurfaceGraphQLField("error")
    )

    def fields(
        self, *subfields: FluxDensityContinuumSurfaceGraphQLField
    ) -> "FluxDensityContinuumSurfaceFields":
        """Subfields should come from the FluxDensityContinuumSurfaceFields class"""
        self._subfields.extend(subfields)
        return self

    def alias(self, alias: str) -> "FluxDensityContinuumSurfaceFields":
        self._alias = alias
        return self


class FluxDensityEntryFields(GraphQLField):
    @classmethod
    def wavelength(cls) -> "WavelengthFields":
        return WavelengthFields("wavelength")

    density: "FluxDensityEntryGraphQLField" = FluxDensityEntryGraphQLField("density")

    def fields(
        self, *subfields: Union[FluxDensityEntryGraphQLField, "WavelengthFields"]
    ) -> "FluxDensityEntryFields":
        """Subfields should come from the FluxDensityEntryFields class"""
        self._subfields.extend(subfields)
        return self

    def alias(self, alias: str) -> "FluxDensityEntryFields":
        self._alias = alias
        return self


class GaussianSourceFields(GraphQLField):
    @classmethod
    def fwhm(cls) -> "AngleFields":
        return AngleFields("fwhm")

    @classmethod
    def band_normalized(cls) -> "BandNormalizedIntegratedFields":
        return BandNormalizedIntegratedFields("bandNormalized")

    @classmethod
    def emission_lines(cls) -> "EmissionLinesIntegratedFields":
        return EmissionLinesIntegratedFields("emissionLines")

    def fields(
        self,
        *subfields: Union[
            GaussianSourceGraphQLField,
            "AngleFields",
            "BandNormalizedIntegratedFields",
            "EmissionLinesIntegratedFields",
        ],
    ) -> "GaussianSourceFields":
        """Subfields should come from the GaussianSourceFields class"""
        self._subfields.extend(subfields)
        return self

    def alias(self, alias: str) -> "GaussianSourceFields":
        self._alias = alias
        return self


class GcalFields(GraphQLField):
    continuum: "GcalGraphQLField" = GcalGraphQLField("continuum")
    arcs: "GcalGraphQLField" = GcalGraphQLField("arcs")
    filter_: "GcalGraphQLField" = GcalGraphQLField("filter")
    diffuser: "GcalGraphQLField" = GcalGraphQLField("diffuser")
    shutter: "GcalGraphQLField" = GcalGraphQLField("shutter")
    step_type: "GcalGraphQLField" = GcalGraphQLField("stepType")

    def fields(self, *subfields: GcalGraphQLField) -> "GcalFields":
        """Subfields should come from the GcalFields class"""
        self._subfields.extend(subfields)
        return self

    def alias(self, alias: str) -> "GcalFields":
        self._alias = alias
        return self


class GeminiCallPropertiesFields(GraphQLField):
    type_: "GeminiCallPropertiesGraphQLField" = GeminiCallPropertiesGraphQLField("type")

    @classmethod
    def coordinate_limits(cls) -> "SiteCoordinateLimitsFields":
        return SiteCoordinateLimitsFields("coordinateLimits")

    instruments: "GeminiCallPropertiesGraphQLField" = GeminiCallPropertiesGraphQLField(
        "instruments"
    )
    proprietary_months: "GeminiCallPropertiesGraphQLField" = (
        GeminiCallPropertiesGraphQLField("proprietaryMonths")
    )
    allows_non_partner_pi: "GeminiCallPropertiesGraphQLField" = (
        GeminiCallPropertiesGraphQLField("allowsNonPartnerPi")
    )
    non_partner_deadline: "GeminiCallPropertiesGraphQLField" = (
        GeminiCallPropertiesGraphQLField("nonPartnerDeadline")
    )

    @classmethod
    def exchange_partners(cls) -> "CallForProposalsExchangePartnerFields":
        return CallForProposalsExchangePartnerFields("exchangePartners")

    def fields(
        self,
        *subfields: Union[
            GeminiCallPropertiesGraphQLField,
            "CallForProposalsExchangePartnerFields",
            "SiteCoordinateLimitsFields",
        ],
    ) -> "GeminiCallPropertiesFields":
        """Subfields should come from the GeminiCallPropertiesFields class"""
        self._subfields.extend(subfields)
        return self

    def alias(self, alias: str) -> "GeminiCallPropertiesFields":
        self._alias = alias
        return self


class GeminiProposalTypeInterface(GraphQLField):
    science_subtype: "GeminiProposalTypeGraphQLField" = GeminiProposalTypeGraphQLField(
        "scienceSubtype"
    )

    def fields(
        self, *subfields: GeminiProposalTypeGraphQLField
    ) -> "GeminiProposalTypeInterface":
        """Subfields should come from the GeminiProposalTypeInterface class"""
        self._subfields.extend(subfields)
        return self

    def alias(self, alias: str) -> "GeminiProposalTypeInterface":
        self._alias = alias
        return self

    def on(
        self, type_name: str, *subfields: GraphQLField
    ) -> "GeminiProposalTypeInterface":
        self._inline_fragments[type_name] = subfields
        return self


class GhostAtomFields(GraphQLField):
    id: "GhostAtomGraphQLField" = GhostAtomGraphQLField("id")
    description: "GhostAtomGraphQLField" = GhostAtomGraphQLField("description")
    observe_class: "GhostAtomGraphQLField" = GhostAtomGraphQLField("observeClass")

    @classmethod
    def steps(cls) -> "GhostStepFields":
        return GhostStepFields("steps")

    def fields(
        self, *subfields: Union[GhostAtomGraphQLField, "GhostStepFields"]
    ) -> "GhostAtomFields":
        """Subfields should come from the GhostAtomFields class"""
        self._subfields.extend(subfields)
        return self

    def alias(self, alias: str) -> "GhostAtomFields":
        self._alias = alias
        return self


class GhostDetectorFields(GraphQLField):
    @classmethod
    def exposure_time(cls) -> "TimeSpanFields":
        return TimeSpanFields("exposureTime")

    exposure_count: "GhostDetectorGraphQLField" = GhostDetectorGraphQLField(
        "exposureCount"
    )
    binning: "GhostDetectorGraphQLField" = GhostDetectorGraphQLField("binning")
    read_mode: "GhostDetectorGraphQLField" = GhostDetectorGraphQLField("readMode")

    def fields(
        self, *subfields: Union[GhostDetectorGraphQLField, "TimeSpanFields"]
    ) -> "GhostDetectorFields":
        """Subfields should come from the GhostDetectorFields class"""
        self._subfields.extend(subfields)
        return self

    def alias(self, alias: str) -> "GhostDetectorFields":
        self._alias = alias
        return self


class GhostDetectorConfigFields(GraphQLField):
    @classmethod
    def exposure_time_mode(cls) -> "ExposureTimeModeFields":
        return ExposureTimeModeFields("exposureTimeMode")

    binning: "GhostDetectorConfigGraphQLField" = GhostDetectorConfigGraphQLField(
        "binning"
    )
    default_binning: "GhostDetectorConfigGraphQLField" = (
        GhostDetectorConfigGraphQLField("defaultBinning")
    )
    explicit_binning: "GhostDetectorConfigGraphQLField" = (
        GhostDetectorConfigGraphQLField("explicitBinning")
    )
    read_mode: "GhostDetectorConfigGraphQLField" = GhostDetectorConfigGraphQLField(
        "readMode"
    )
    default_read_mode: "GhostDetectorConfigGraphQLField" = (
        GhostDetectorConfigGraphQLField("defaultReadMode")
    )
    explicit_read_mode: "GhostDetectorConfigGraphQLField" = (
        GhostDetectorConfigGraphQLField("explicitReadMode")
    )

    def fields(
        self,
        *subfields: Union[GhostDetectorConfigGraphQLField, "ExposureTimeModeFields"],
    ) -> "GhostDetectorConfigFields":
        """Subfields should come from the GhostDetectorConfigFields class"""
        self._subfields.extend(subfields)
        return self

    def alias(self, alias: str) -> "GhostDetectorConfigFields":
        self._alias = alias
        return self


class GhostDualTargetFields(GraphQLField):
    ifu_1: "GhostDualTargetGraphQLField" = GhostDualTargetGraphQLField("ifu1")
    ifu_2: "GhostDualTargetGraphQLField" = GhostDualTargetGraphQLField("ifu2")

    def fields(
        self, *subfields: GhostDualTargetGraphQLField
    ) -> "GhostDualTargetFields":
        """Subfields should come from the GhostDualTargetFields class"""
        self._subfields.extend(subfields)
        return self

    def alias(self, alias: str) -> "GhostDualTargetFields":
        self._alias = alias
        return self


class GhostDynamicFields(GraphQLField):
    @classmethod
    def red(cls) -> "GhostDetectorFields":
        return GhostDetectorFields("red")

    @classmethod
    def blue(cls) -> "GhostDetectorFields":
        return GhostDetectorFields("blue")

    ifu_1_fiber_agitator: "GhostDynamicGraphQLField" = GhostDynamicGraphQLField(
        "ifu1FiberAgitator"
    )
    ifu_2_fiber_agitator: "GhostDynamicGraphQLField" = GhostDynamicGraphQLField(
        "ifu2FiberAgitator"
    )

    @classmethod
    def central_wavelength(cls) -> "WavelengthFields":
        return WavelengthFields("centralWavelength")

    def fields(
        self,
        *subfields: Union[
            GhostDynamicGraphQLField, "GhostDetectorFields", "WavelengthFields"
        ],
    ) -> "GhostDynamicFields":
        """Subfields should come from the GhostDynamicFields class"""
        self._subfields.extend(subfields)
        return self

    def alias(self, alias: str) -> "GhostDynamicFields":
        self._alias = alias
        return self


class GhostExecutionConfigFields(GraphQLField):
    @classmethod
    def static(cls) -> "GhostStaticFields":
        return GhostStaticFields("static")

    @classmethod
    def science(cls) -> "GhostExecutionSequenceFields":
        return GhostExecutionSequenceFields("science")

    def fields(
        self,
        *subfields: Union[
            GhostExecutionConfigGraphQLField,
            "GhostExecutionSequenceFields",
            "GhostStaticFields",
        ],
    ) -> "GhostExecutionConfigFields":
        """Subfields should come from the GhostExecutionConfigFields class"""
        self._subfields.extend(subfields)
        return self

    def alias(self, alias: str) -> "GhostExecutionConfigFields":
        self._alias = alias
        return self


class GhostExecutionSequenceFields(GraphQLField):
    @classmethod
    def next_atom(cls) -> "GhostAtomFields":
        return GhostAtomFields("nextAtom")

    @classmethod
    def possible_future(cls) -> "GhostAtomFields":
        return GhostAtomFields("possibleFuture")

    has_more: "GhostExecutionSequenceGraphQLField" = GhostExecutionSequenceGraphQLField(
        "hasMore"
    )

    def fields(
        self, *subfields: Union[GhostExecutionSequenceGraphQLField, "GhostAtomFields"]
    ) -> "GhostExecutionSequenceFields":
        """Subfields should come from the GhostExecutionSequenceFields class"""
        self._subfields.extend(subfields)
        return self

    def alias(self, alias: str) -> "GhostExecutionSequenceFields":
        self._alias = alias
        return self


class GhostIfuFields(GraphQLField):
    step_count: "GhostIfuGraphQLField" = GhostIfuGraphQLField("stepCount")
    resolution_mode: "GhostIfuGraphQLField" = GhostIfuGraphQLField("resolutionMode")

    @classmethod
    def red(cls) -> "GhostDetectorConfigFields":
        return GhostDetectorConfigFields("red")

    @classmethod
    def blue(cls) -> "GhostDetectorConfigFields":
        return GhostDetectorConfigFields("blue")

    @classmethod
    def sky_position(cls) -> "CoordinatesFields":
        return CoordinatesFields("skyPosition")

    @classmethod
    def slit_viewing_camera_exposure_time(cls) -> "TimeSpanFields":
        return TimeSpanFields("slitViewingCameraExposureTime")

    ifu_1_agitator: "GhostIfuGraphQLField" = GhostIfuGraphQLField("ifu1Agitator")
    default_ifu_1_agitator: "GhostIfuGraphQLField" = GhostIfuGraphQLField(
        "defaultIfu1Agitator"
    )
    explicit_ifu_1_agitator: "GhostIfuGraphQLField" = GhostIfuGraphQLField(
        "explicitIfu1Agitator"
    )
    ifu_2_agitator: "GhostIfuGraphQLField" = GhostIfuGraphQLField("ifu2Agitator")
    default_ifu_2_agitator: "GhostIfuGraphQLField" = GhostIfuGraphQLField(
        "defaultIfu2Agitator"
    )
    explicit_ifu_2_agitator: "GhostIfuGraphQLField" = GhostIfuGraphQLField(
        "explicitIfu2Agitator"
    )

    def fields(
        self,
        *subfields: Union[
            GhostIfuGraphQLField,
            "CoordinatesFields",
            "GhostDetectorConfigFields",
            "TimeSpanFields",
        ],
    ) -> "GhostIfuFields":
        """Subfields should come from the GhostIfuFields class"""
        self._subfields.extend(subfields)
        return self

    def alias(self, alias: str) -> "GhostIfuFields":
        self._alias = alias
        return self


class GhostIfuMappingFields(GraphQLField):
    mapping_type: "GhostIfuMappingGraphQLField" = GhostIfuMappingGraphQLField(
        "mappingType"
    )

    @classmethod
    def single_target(cls) -> "GhostSingleTargetFields":
        return GhostSingleTargetFields("singleTarget")

    @classmethod
    def target_plus_sky(cls) -> "GhostTargetPlusSkyFields":
        return GhostTargetPlusSkyFields("targetPlusSky")

    @classmethod
    def sky_plus_target(cls) -> "GhostSkyPlusTargetFields":
        return GhostSkyPlusTargetFields("skyPlusTarget")

    @classmethod
    def dual_target(cls) -> "GhostDualTargetFields":
        return GhostDualTargetFields("dualTarget")

    def fields(
        self,
        *subfields: Union[
            GhostIfuMappingGraphQLField,
            "GhostDualTargetFields",
            "GhostSingleTargetFields",
            "GhostSkyPlusTargetFields",
            "GhostTargetPlusSkyFields",
        ],
    ) -> "GhostIfuMappingFields":
        """Subfields should come from the GhostIfuMappingFields class"""
        self._subfields.extend(subfields)
        return self

    def alias(self, alias: str) -> "GhostIfuMappingFields":
        self._alias = alias
        return self


class GhostSingleTargetFields(GraphQLField):
    ifu_1: "GhostSingleTargetGraphQLField" = GhostSingleTargetGraphQLField("ifu1")

    def fields(
        self, *subfields: GhostSingleTargetGraphQLField
    ) -> "GhostSingleTargetFields":
        """Subfields should come from the GhostSingleTargetFields class"""
        self._subfields.extend(subfields)
        return self

    def alias(self, alias: str) -> "GhostSingleTargetFields":
        self._alias = alias
        return self


class GhostSkyPlusTargetFields(GraphQLField):
    @classmethod
    def ifu_1(cls) -> "CoordinatesFields":
        return CoordinatesFields("ifu1")

    ifu_2: "GhostSkyPlusTargetGraphQLField" = GhostSkyPlusTargetGraphQLField("ifu2")

    def fields(
        self, *subfields: Union[GhostSkyPlusTargetGraphQLField, "CoordinatesFields"]
    ) -> "GhostSkyPlusTargetFields":
        """Subfields should come from the GhostSkyPlusTargetFields class"""
        self._subfields.extend(subfields)
        return self

    def alias(self, alias: str) -> "GhostSkyPlusTargetFields":
        self._alias = alias
        return self


class GhostStaticFields(GraphQLField):
    resolution_mode: "GhostStaticGraphQLField" = GhostStaticGraphQLField(
        "resolutionMode"
    )

    @classmethod
    def ifu_mapping(cls) -> "GhostIfuMappingFields":
        return GhostIfuMappingFields("ifuMapping")

    @classmethod
    def slit_viewing_camera_exposure_time(cls) -> "TimeSpanFields":
        return TimeSpanFields("slitViewingCameraExposureTime")

    def fields(
        self,
        *subfields: Union[
            GhostStaticGraphQLField, "GhostIfuMappingFields", "TimeSpanFields"
        ],
    ) -> "GhostStaticFields":
        """Subfields should come from the GhostStaticFields class"""
        self._subfields.extend(subfields)
        return self

    def alias(self, alias: str) -> "GhostStaticFields":
        self._alias = alias
        return self


class GhostStepFields(GraphQLField):
    @classmethod
    def instrument_config(cls) -> "GhostDynamicFields":
        return GhostDynamicFields("instrumentConfig")

    id: "GhostStepGraphQLField" = GhostStepGraphQLField("id")
    breakpoint: "GhostStepGraphQLField" = GhostStepGraphQLField("breakpoint")

    @classmethod
    def step_config(cls) -> "StepConfigInterface":
        return StepConfigInterface("stepConfig")

    @classmethod
    def telescope_config(cls) -> "TelescopeConfigFields":
        return TelescopeConfigFields("telescopeConfig")

    @classmethod
    def estimate(cls) -> "StepEstimateFields":
        return StepEstimateFields("estimate")

    observe_class: "GhostStepGraphQLField" = GhostStepGraphQLField("observeClass")

    def fields(
        self,
        *subfields: Union[
            GhostStepGraphQLField,
            "GhostDynamicFields",
            "StepConfigInterface",
            "StepEstimateFields",
            "TelescopeConfigFields",
        ],
    ) -> "GhostStepFields":
        """Subfields should come from the GhostStepFields class"""
        self._subfields.extend(subfields)
        return self

    def alias(self, alias: str) -> "GhostStepFields":
        self._alias = alias
        return self


class GhostTargetPlusSkyFields(GraphQLField):
    ifu_1: "GhostTargetPlusSkyGraphQLField" = GhostTargetPlusSkyGraphQLField("ifu1")

    @classmethod
    def ifu_2(cls) -> "CoordinatesFields":
        return CoordinatesFields("ifu2")

    def fields(
        self, *subfields: Union[GhostTargetPlusSkyGraphQLField, "CoordinatesFields"]
    ) -> "GhostTargetPlusSkyFields":
        """Subfields should come from the GhostTargetPlusSkyFields class"""
        self._subfields.extend(subfields)
        return self

    def alias(self, alias: str) -> "GhostTargetPlusSkyFields":
        self._alias = alias
        return self


class GmosCcdModeFields(GraphQLField):
    x_bin: "GmosCcdModeGraphQLField" = GmosCcdModeGraphQLField("xBin")
    y_bin: "GmosCcdModeGraphQLField" = GmosCcdModeGraphQLField("yBin")
    amp_count: "GmosCcdModeGraphQLField" = GmosCcdModeGraphQLField("ampCount")
    amp_gain: "GmosCcdModeGraphQLField" = GmosCcdModeGraphQLField("ampGain")
    amp_read_mode: "GmosCcdModeGraphQLField" = GmosCcdModeGraphQLField("ampReadMode")

    def fields(self, *subfields: GmosCcdModeGraphQLField) -> "GmosCcdModeFields":
        """Subfields should come from the GmosCcdModeFields class"""
        self._subfields.extend(subfields)
        return self

    def alias(self, alias: str) -> "GmosCcdModeFields":
        self._alias = alias
        return self


class GmosCustomMaskFields(GraphQLField):
    attachment_id: "GmosCustomMaskGraphQLField" = GmosCustomMaskGraphQLField(
        "attachmentId"
    )
    slit_width: "GmosCustomMaskGraphQLField" = GmosCustomMaskGraphQLField("slitWidth")

    def fields(self, *subfields: GmosCustomMaskGraphQLField) -> "GmosCustomMaskFields":
        """Subfields should come from the GmosCustomMaskFields class"""
        self._subfields.extend(subfields)
        return self

    def alias(self, alias: str) -> "GmosCustomMaskFields":
        self._alias = alias
        return self


class GmosNodAndShuffleFields(GraphQLField):
    @classmethod
    def pos_a(cls) -> "OffsetFields":
        return OffsetFields("posA")

    @classmethod
    def pos_b(cls) -> "OffsetFields":
        return OffsetFields("posB")

    e_offset: "GmosNodAndShuffleGraphQLField" = GmosNodAndShuffleGraphQLField("eOffset")
    shuffle_offset: "GmosNodAndShuffleGraphQLField" = GmosNodAndShuffleGraphQLField(
        "shuffleOffset"
    )
    shuffle_cycles: "GmosNodAndShuffleGraphQLField" = GmosNodAndShuffleGraphQLField(
        "shuffleCycles"
    )

    def fields(
        self, *subfields: Union[GmosNodAndShuffleGraphQLField, "OffsetFields"]
    ) -> "GmosNodAndShuffleFields":
        """Subfields should come from the GmosNodAndShuffleFields class"""
        self._subfields.extend(subfields)
        return self

    def alias(self, alias: str) -> "GmosNodAndShuffleFields":
        self._alias = alias
        return self


class GmosNorthAtomFields(GraphQLField):
    id: "GmosNorthAtomGraphQLField" = GmosNorthAtomGraphQLField("id")
    description: "GmosNorthAtomGraphQLField" = GmosNorthAtomGraphQLField("description")
    observe_class: "GmosNorthAtomGraphQLField" = GmosNorthAtomGraphQLField(
        "observeClass"
    )

    @classmethod
    def steps(cls) -> "GmosNorthStepFields":
        return GmosNorthStepFields("steps")

    def fields(
        self, *subfields: Union[GmosNorthAtomGraphQLField, "GmosNorthStepFields"]
    ) -> "GmosNorthAtomFields":
        """Subfields should come from the GmosNorthAtomFields class"""
        self._subfields.extend(subfields)
        return self

    def alias(self, alias: str) -> "GmosNorthAtomFields":
        self._alias = alias
        return self


class GmosNorthDynamicFields(GraphQLField):
    @classmethod
    def exposure(cls) -> "TimeSpanFields":
        return TimeSpanFields("exposure")

    @classmethod
    def readout(cls) -> "GmosCcdModeFields":
        return GmosCcdModeFields("readout")

    dtax: "GmosNorthDynamicGraphQLField" = GmosNorthDynamicGraphQLField("dtax")
    roi: "GmosNorthDynamicGraphQLField" = GmosNorthDynamicGraphQLField("roi")

    @classmethod
    def grating_config(cls) -> "GmosNorthGratingConfigFields":
        return GmosNorthGratingConfigFields("gratingConfig")

    filter_: "GmosNorthDynamicGraphQLField" = GmosNorthDynamicGraphQLField("filter")

    @classmethod
    def fpu(cls) -> "GmosNorthFpuFields":
        return GmosNorthFpuFields("fpu")

    @classmethod
    def central_wavelength(cls) -> "WavelengthFields":
        return WavelengthFields("centralWavelength")

    def fields(
        self,
        *subfields: Union[
            GmosNorthDynamicGraphQLField,
            "GmosCcdModeFields",
            "GmosNorthFpuFields",
            "GmosNorthGratingConfigFields",
            "TimeSpanFields",
            "WavelengthFields",
        ],
    ) -> "GmosNorthDynamicFields":
        """Subfields should come from the GmosNorthDynamicFields class"""
        self._subfields.extend(subfields)
        return self

    def alias(self, alias: str) -> "GmosNorthDynamicFields":
        self._alias = alias
        return self


class GmosNorthExecutionConfigFields(GraphQLField):
    @classmethod
    def static(cls) -> "GmosNorthStaticFields":
        return GmosNorthStaticFields("static")

    @classmethod
    def acquisition(cls) -> "GmosNorthExecutionSequenceFields":
        return GmosNorthExecutionSequenceFields("acquisition")

    @classmethod
    def science(cls) -> "GmosNorthExecutionSequenceFields":
        return GmosNorthExecutionSequenceFields("science")

    def fields(
        self,
        *subfields: Union[
            GmosNorthExecutionConfigGraphQLField,
            "GmosNorthExecutionSequenceFields",
            "GmosNorthStaticFields",
        ],
    ) -> "GmosNorthExecutionConfigFields":
        """Subfields should come from the GmosNorthExecutionConfigFields class"""
        self._subfields.extend(subfields)
        return self

    def alias(self, alias: str) -> "GmosNorthExecutionConfigFields":
        self._alias = alias
        return self


class GmosNorthExecutionSequenceFields(GraphQLField):
    @classmethod
    def next_atom(cls) -> "GmosNorthAtomFields":
        return GmosNorthAtomFields("nextAtom")

    @classmethod
    def possible_future(cls) -> "GmosNorthAtomFields":
        return GmosNorthAtomFields("possibleFuture")

    has_more: "GmosNorthExecutionSequenceGraphQLField" = (
        GmosNorthExecutionSequenceGraphQLField("hasMore")
    )

    def fields(
        self,
        *subfields: Union[
            GmosNorthExecutionSequenceGraphQLField, "GmosNorthAtomFields"
        ],
    ) -> "GmosNorthExecutionSequenceFields":
        """Subfields should come from the GmosNorthExecutionSequenceFields class"""
        self._subfields.extend(subfields)
        return self

    def alias(self, alias: str) -> "GmosNorthExecutionSequenceFields":
        self._alias = alias
        return self


class GmosNorthFpuFields(GraphQLField):
    @classmethod
    def custom_mask(cls) -> "GmosCustomMaskFields":
        return GmosCustomMaskFields("customMask")

    builtin: "GmosNorthFpuGraphQLField" = GmosNorthFpuGraphQLField("builtin")

    def fields(
        self, *subfields: Union[GmosNorthFpuGraphQLField, "GmosCustomMaskFields"]
    ) -> "GmosNorthFpuFields":
        """Subfields should come from the GmosNorthFpuFields class"""
        self._subfields.extend(subfields)
        return self

    def alias(self, alias: str) -> "GmosNorthFpuFields":
        self._alias = alias
        return self


class GmosNorthGratingConfigFields(GraphQLField):
    grating: "GmosNorthGratingConfigGraphQLField" = GmosNorthGratingConfigGraphQLField(
        "grating"
    )
    order: "GmosNorthGratingConfigGraphQLField" = GmosNorthGratingConfigGraphQLField(
        "order"
    )

    @classmethod
    def wavelength(cls) -> "WavelengthFields":
        return WavelengthFields("wavelength")

    def fields(
        self, *subfields: Union[GmosNorthGratingConfigGraphQLField, "WavelengthFields"]
    ) -> "GmosNorthGratingConfigFields":
        """Subfields should come from the GmosNorthGratingConfigFields class"""
        self._subfields.extend(subfields)
        return self

    def alias(self, alias: str) -> "GmosNorthGratingConfigFields":
        self._alias = alias
        return self


class GmosNorthImagingFields(GraphQLField):
    @classmethod
    def variant(cls) -> "ImagingVariantFields":
        return ImagingVariantFields("variant")

    @classmethod
    def filters(cls) -> "GmosNorthImagingFilterFields":
        return GmosNorthImagingFilterFields("filters")

    @classmethod
    def initial_filters(cls) -> "GmosNorthImagingFilterFields":
        return GmosNorthImagingFilterFields("initialFilters")

    bin: "GmosNorthImagingGraphQLField" = GmosNorthImagingGraphQLField("bin")
    default_bin: "GmosNorthImagingGraphQLField" = GmosNorthImagingGraphQLField(
        "defaultBin"
    )
    explicit_bin: "GmosNorthImagingGraphQLField" = GmosNorthImagingGraphQLField(
        "explicitBin"
    )
    amp_read_mode: "GmosNorthImagingGraphQLField" = GmosNorthImagingGraphQLField(
        "ampReadMode"
    )
    default_amp_read_mode: "GmosNorthImagingGraphQLField" = (
        GmosNorthImagingGraphQLField("defaultAmpReadMode")
    )
    explicit_amp_read_mode: "GmosNorthImagingGraphQLField" = (
        GmosNorthImagingGraphQLField("explicitAmpReadMode")
    )
    amp_gain: "GmosNorthImagingGraphQLField" = GmosNorthImagingGraphQLField("ampGain")
    default_amp_gain: "GmosNorthImagingGraphQLField" = GmosNorthImagingGraphQLField(
        "defaultAmpGain"
    )
    explicit_amp_gain: "GmosNorthImagingGraphQLField" = GmosNorthImagingGraphQLField(
        "explicitAmpGain"
    )
    roi: "GmosNorthImagingGraphQLField" = GmosNorthImagingGraphQLField("roi")
    default_roi: "GmosNorthImagingGraphQLField" = GmosNorthImagingGraphQLField(
        "defaultRoi"
    )
    explicit_roi: "GmosNorthImagingGraphQLField" = GmosNorthImagingGraphQLField(
        "explicitRoi"
    )

    def fields(
        self,
        *subfields: Union[
            GmosNorthImagingGraphQLField,
            "GmosNorthImagingFilterFields",
            "ImagingVariantFields",
        ],
    ) -> "GmosNorthImagingFields":
        """Subfields should come from the GmosNorthImagingFields class"""
        self._subfields.extend(subfields)
        return self

    def alias(self, alias: str) -> "GmosNorthImagingFields":
        self._alias = alias
        return self


class GmosNorthImagingFilterFields(GraphQLField):
    filter_: "GmosNorthImagingFilterGraphQLField" = GmosNorthImagingFilterGraphQLField(
        "filter"
    )

    @classmethod
    def exposure_time_mode(cls) -> "ExposureTimeModeFields":
        return ExposureTimeModeFields("exposureTimeMode")

    def fields(
        self,
        *subfields: Union[GmosNorthImagingFilterGraphQLField, "ExposureTimeModeFields"],
    ) -> "GmosNorthImagingFilterFields":
        """Subfields should come from the GmosNorthImagingFilterFields class"""
        self._subfields.extend(subfields)
        return self

    def alias(self, alias: str) -> "GmosNorthImagingFilterFields":
        self._alias = alias
        return self


class GmosNorthLongSlitFields(GraphQLField):
    grating: "GmosNorthLongSlitGraphQLField" = GmosNorthLongSlitGraphQLField("grating")
    filter_: "GmosNorthLongSlitGraphQLField" = GmosNorthLongSlitGraphQLField("filter")
    fpu: "GmosNorthLongSlitGraphQLField" = GmosNorthLongSlitGraphQLField("fpu")

    @classmethod
    def central_wavelength(cls) -> "WavelengthFields":
        return WavelengthFields("centralWavelength")

    @classmethod
    def exposure_time_mode(cls) -> "ExposureTimeModeFields":
        return ExposureTimeModeFields("exposureTimeMode")

    x_bin: "GmosNorthLongSlitGraphQLField" = GmosNorthLongSlitGraphQLField("xBin")
    default_x_bin: "GmosNorthLongSlitGraphQLField" = GmosNorthLongSlitGraphQLField(
        "defaultXBin"
    )
    explicit_x_bin: "GmosNorthLongSlitGraphQLField" = GmosNorthLongSlitGraphQLField(
        "explicitXBin"
    )
    y_bin: "GmosNorthLongSlitGraphQLField" = GmosNorthLongSlitGraphQLField("yBin")
    default_y_bin: "GmosNorthLongSlitGraphQLField" = GmosNorthLongSlitGraphQLField(
        "defaultYBin"
    )
    explicit_y_bin: "GmosNorthLongSlitGraphQLField" = GmosNorthLongSlitGraphQLField(
        "explicitYBin"
    )
    amp_read_mode: "GmosNorthLongSlitGraphQLField" = GmosNorthLongSlitGraphQLField(
        "ampReadMode"
    )
    default_amp_read_mode: "GmosNorthLongSlitGraphQLField" = (
        GmosNorthLongSlitGraphQLField("defaultAmpReadMode")
    )
    explicit_amp_read_mode: "GmosNorthLongSlitGraphQLField" = (
        GmosNorthLongSlitGraphQLField("explicitAmpReadMode")
    )
    amp_gain: "GmosNorthLongSlitGraphQLField" = GmosNorthLongSlitGraphQLField("ampGain")
    default_amp_gain: "GmosNorthLongSlitGraphQLField" = GmosNorthLongSlitGraphQLField(
        "defaultAmpGain"
    )
    explicit_amp_gain: "GmosNorthLongSlitGraphQLField" = GmosNorthLongSlitGraphQLField(
        "explicitAmpGain"
    )
    roi: "GmosNorthLongSlitGraphQLField" = GmosNorthLongSlitGraphQLField("roi")
    default_roi: "GmosNorthLongSlitGraphQLField" = GmosNorthLongSlitGraphQLField(
        "defaultRoi"
    )
    explicit_roi: "GmosNorthLongSlitGraphQLField" = GmosNorthLongSlitGraphQLField(
        "explicitRoi"
    )

    @classmethod
    def wavelength_dithers(cls) -> "WavelengthDitherFields":
        return WavelengthDitherFields("wavelengthDithers")

    @classmethod
    def default_wavelength_dithers(cls) -> "WavelengthDitherFields":
        return WavelengthDitherFields("defaultWavelengthDithers")

    @classmethod
    def explicit_wavelength_dithers(cls) -> "WavelengthDitherFields":
        return WavelengthDitherFields("explicitWavelengthDithers")

    @classmethod
    def offsets(cls) -> "OffsetQFields":
        return OffsetQFields("offsets")

    @classmethod
    def default_offsets(cls) -> "OffsetQFields":
        return OffsetQFields("defaultOffsets")

    @classmethod
    def explicit_offsets(cls) -> "OffsetQFields":
        return OffsetQFields("explicitOffsets")

    @classmethod
    def spatial_offsets(cls) -> "OffsetQFields":
        return OffsetQFields("spatialOffsets")

    @classmethod
    def default_spatial_offsets(cls) -> "OffsetQFields":
        return OffsetQFields("defaultSpatialOffsets")

    @classmethod
    def explicit_spatial_offsets(cls) -> "OffsetQFields":
        return OffsetQFields("explicitSpatialOffsets")

    @classmethod
    def acquisition(cls) -> "GmosNorthLongSlitAcquisitionFields":
        return GmosNorthLongSlitAcquisitionFields("acquisition")

    initial_grating: "GmosNorthLongSlitGraphQLField" = GmosNorthLongSlitGraphQLField(
        "initialGrating"
    )
    initial_filter: "GmosNorthLongSlitGraphQLField" = GmosNorthLongSlitGraphQLField(
        "initialFilter"
    )
    initial_fpu: "GmosNorthLongSlitGraphQLField" = GmosNorthLongSlitGraphQLField(
        "initialFpu"
    )

    @classmethod
    def initial_central_wavelength(cls) -> "WavelengthFields":
        return WavelengthFields("initialCentralWavelength")

    def fields(
        self,
        *subfields: Union[
            GmosNorthLongSlitGraphQLField,
            "ExposureTimeModeFields",
            "GmosNorthLongSlitAcquisitionFields",
            "OffsetQFields",
            "WavelengthDitherFields",
            "WavelengthFields",
        ],
    ) -> "GmosNorthLongSlitFields":
        """Subfields should come from the GmosNorthLongSlitFields class"""
        self._subfields.extend(subfields)
        return self

    def alias(self, alias: str) -> "GmosNorthLongSlitFields":
        self._alias = alias
        return self


class GmosNorthLongSlitAcquisitionFields(GraphQLField):
    filter_: "GmosNorthLongSlitAcquisitionGraphQLField" = (
        GmosNorthLongSlitAcquisitionGraphQLField("filter")
    )
    default_filter: "GmosNorthLongSlitAcquisitionGraphQLField" = (
        GmosNorthLongSlitAcquisitionGraphQLField("defaultFilter")
    )
    explicit_filter: "GmosNorthLongSlitAcquisitionGraphQLField" = (
        GmosNorthLongSlitAcquisitionGraphQLField("explicitFilter")
    )
    roi: "GmosNorthLongSlitAcquisitionGraphQLField" = (
        GmosNorthLongSlitAcquisitionGraphQLField("roi")
    )
    default_roi: "GmosNorthLongSlitAcquisitionGraphQLField" = (
        GmosNorthLongSlitAcquisitionGraphQLField("defaultRoi")
    )
    explicit_roi: "GmosNorthLongSlitAcquisitionGraphQLField" = (
        GmosNorthLongSlitAcquisitionGraphQLField("explicitRoi")
    )

    @classmethod
    def exposure_time_mode(cls) -> "ExposureTimeModeFields":
        return ExposureTimeModeFields("exposureTimeMode")

    def fields(
        self,
        *subfields: Union[
            GmosNorthLongSlitAcquisitionGraphQLField, "ExposureTimeModeFields"
        ],
    ) -> "GmosNorthLongSlitAcquisitionFields":
        """Subfields should come from the GmosNorthLongSlitAcquisitionFields class"""
        self._subfields.extend(subfields)
        return self

    def alias(self, alias: str) -> "GmosNorthLongSlitAcquisitionFields":
        self._alias = alias
        return self


class GmosNorthMosFields(GraphQLField):
    grating: "GmosNorthMosGraphQLField" = GmosNorthMosGraphQLField("grating")
    filter_: "GmosNorthMosGraphQLField" = GmosNorthMosGraphQLField("filter")

    @classmethod
    def custom_mask(cls) -> "GmosCustomMaskFields":
        return GmosCustomMaskFields("customMask")

    @classmethod
    def central_wavelength(cls) -> "WavelengthFields":
        return WavelengthFields("centralWavelength")

    acquisition_type: "GmosNorthMosGraphQLField" = GmosNorthMosGraphQLField(
        "acquisitionType"
    )

    @classmethod
    def exposure_time_mode(cls) -> "ExposureTimeModeFields":
        return ExposureTimeModeFields("exposureTimeMode")

    x_bin: "GmosNorthMosGraphQLField" = GmosNorthMosGraphQLField("xBin")
    default_x_bin: "GmosNorthMosGraphQLField" = GmosNorthMosGraphQLField("defaultXBin")
    explicit_x_bin: "GmosNorthMosGraphQLField" = GmosNorthMosGraphQLField(
        "explicitXBin"
    )
    y_bin: "GmosNorthMosGraphQLField" = GmosNorthMosGraphQLField("yBin")
    default_y_bin: "GmosNorthMosGraphQLField" = GmosNorthMosGraphQLField("defaultYBin")
    explicit_y_bin: "GmosNorthMosGraphQLField" = GmosNorthMosGraphQLField(
        "explicitYBin"
    )
    amp_read_mode: "GmosNorthMosGraphQLField" = GmosNorthMosGraphQLField("ampReadMode")
    default_amp_read_mode: "GmosNorthMosGraphQLField" = GmosNorthMosGraphQLField(
        "defaultAmpReadMode"
    )
    explicit_amp_read_mode: "GmosNorthMosGraphQLField" = GmosNorthMosGraphQLField(
        "explicitAmpReadMode"
    )
    amp_gain: "GmosNorthMosGraphQLField" = GmosNorthMosGraphQLField("ampGain")
    default_amp_gain: "GmosNorthMosGraphQLField" = GmosNorthMosGraphQLField(
        "defaultAmpGain"
    )
    explicit_amp_gain: "GmosNorthMosGraphQLField" = GmosNorthMosGraphQLField(
        "explicitAmpGain"
    )
    roi: "GmosNorthMosGraphQLField" = GmosNorthMosGraphQLField("roi")
    default_roi: "GmosNorthMosGraphQLField" = GmosNorthMosGraphQLField("defaultRoi")
    explicit_roi: "GmosNorthMosGraphQLField" = GmosNorthMosGraphQLField("explicitRoi")

    @classmethod
    def wavelength_dithers(cls) -> "WavelengthDitherFields":
        return WavelengthDitherFields("wavelengthDithers")

    @classmethod
    def default_wavelength_dithers(cls) -> "WavelengthDitherFields":
        return WavelengthDitherFields("defaultWavelengthDithers")

    @classmethod
    def explicit_wavelength_dithers(cls) -> "WavelengthDitherFields":
        return WavelengthDitherFields("explicitWavelengthDithers")

    @classmethod
    def offsets(cls) -> "OffsetQFields":
        return OffsetQFields("offsets")

    @classmethod
    def default_offsets(cls) -> "OffsetQFields":
        return OffsetQFields("defaultOffsets")

    @classmethod
    def explicit_offsets(cls) -> "OffsetQFields":
        return OffsetQFields("explicitOffsets")

    initial_grating: "GmosNorthMosGraphQLField" = GmosNorthMosGraphQLField(
        "initialGrating"
    )
    initial_filter: "GmosNorthMosGraphQLField" = GmosNorthMosGraphQLField(
        "initialFilter"
    )
    initial_slit_width: "GmosNorthMosGraphQLField" = GmosNorthMosGraphQLField(
        "initialSlitWidth"
    )

    @classmethod
    def initial_central_wavelength(cls) -> "WavelengthFields":
        return WavelengthFields("initialCentralWavelength")

    @classmethod
    def acquisition(cls) -> "GmosNorthMosAcquisitionFields":
        return GmosNorthMosAcquisitionFields("acquisition")

    def fields(
        self,
        *subfields: Union[
            GmosNorthMosGraphQLField,
            "ExposureTimeModeFields",
            "GmosCustomMaskFields",
            "GmosNorthMosAcquisitionFields",
            "OffsetQFields",
            "WavelengthDitherFields",
            "WavelengthFields",
        ],
    ) -> "GmosNorthMosFields":
        """Subfields should come from the GmosNorthMosFields class"""
        self._subfields.extend(subfields)
        return self

    def alias(self, alias: str) -> "GmosNorthMosFields":
        self._alias = alias
        return self


class GmosNorthMosAcquisitionFields(GraphQLField):
    filter_: "GmosNorthMosAcquisitionGraphQLField" = (
        GmosNorthMosAcquisitionGraphQLField("filter")
    )
    default_filter: "GmosNorthMosAcquisitionGraphQLField" = (
        GmosNorthMosAcquisitionGraphQLField("defaultFilter")
    )
    explicit_filter: "GmosNorthMosAcquisitionGraphQLField" = (
        GmosNorthMosAcquisitionGraphQLField("explicitFilter")
    )

    @classmethod
    def exposure_time_mode(cls) -> "ExposureTimeModeFields":
        return ExposureTimeModeFields("exposureTimeMode")

    def fields(
        self,
        *subfields: Union[
            GmosNorthMosAcquisitionGraphQLField, "ExposureTimeModeFields"
        ],
    ) -> "GmosNorthMosAcquisitionFields":
        """Subfields should come from the GmosNorthMosAcquisitionFields class"""
        self._subfields.extend(subfields)
        return self

    def alias(self, alias: str) -> "GmosNorthMosAcquisitionFields":
        self._alias = alias
        return self


class GmosNorthStaticFields(GraphQLField):
    stage_mode: "GmosNorthStaticGraphQLField" = GmosNorthStaticGraphQLField("stageMode")
    detector: "GmosNorthStaticGraphQLField" = GmosNorthStaticGraphQLField("detector")
    mos_pre_imaging: "GmosNorthStaticGraphQLField" = GmosNorthStaticGraphQLField(
        "mosPreImaging"
    )

    @classmethod
    def nod_and_shuffle(cls) -> "GmosNodAndShuffleFields":
        return GmosNodAndShuffleFields("nodAndShuffle")

    def fields(
        self, *subfields: Union[GmosNorthStaticGraphQLField, "GmosNodAndShuffleFields"]
    ) -> "GmosNorthStaticFields":
        """Subfields should come from the GmosNorthStaticFields class"""
        self._subfields.extend(subfields)
        return self

    def alias(self, alias: str) -> "GmosNorthStaticFields":
        self._alias = alias
        return self


class GmosNorthStepFields(GraphQLField):
    @classmethod
    def instrument_config(cls) -> "GmosNorthDynamicFields":
        return GmosNorthDynamicFields("instrumentConfig")

    id: "GmosNorthStepGraphQLField" = GmosNorthStepGraphQLField("id")
    breakpoint: "GmosNorthStepGraphQLField" = GmosNorthStepGraphQLField("breakpoint")

    @classmethod
    def step_config(cls) -> "StepConfigInterface":
        return StepConfigInterface("stepConfig")

    @classmethod
    def telescope_config(cls) -> "TelescopeConfigFields":
        return TelescopeConfigFields("telescopeConfig")

    @classmethod
    def estimate(cls) -> "StepEstimateFields":
        return StepEstimateFields("estimate")

    observe_class: "GmosNorthStepGraphQLField" = GmosNorthStepGraphQLField(
        "observeClass"
    )

    def fields(
        self,
        *subfields: Union[
            GmosNorthStepGraphQLField,
            "GmosNorthDynamicFields",
            "StepConfigInterface",
            "StepEstimateFields",
            "TelescopeConfigFields",
        ],
    ) -> "GmosNorthStepFields":
        """Subfields should come from the GmosNorthStepFields class"""
        self._subfields.extend(subfields)
        return self

    def alias(self, alias: str) -> "GmosNorthStepFields":
        self._alias = alias
        return self


class GmosSouthAtomFields(GraphQLField):
    id: "GmosSouthAtomGraphQLField" = GmosSouthAtomGraphQLField("id")
    description: "GmosSouthAtomGraphQLField" = GmosSouthAtomGraphQLField("description")
    observe_class: "GmosSouthAtomGraphQLField" = GmosSouthAtomGraphQLField(
        "observeClass"
    )

    @classmethod
    def steps(cls) -> "GmosSouthStepFields":
        return GmosSouthStepFields("steps")

    def fields(
        self, *subfields: Union[GmosSouthAtomGraphQLField, "GmosSouthStepFields"]
    ) -> "GmosSouthAtomFields":
        """Subfields should come from the GmosSouthAtomFields class"""
        self._subfields.extend(subfields)
        return self

    def alias(self, alias: str) -> "GmosSouthAtomFields":
        self._alias = alias
        return self


class GmosSouthDynamicFields(GraphQLField):
    @classmethod
    def exposure(cls) -> "TimeSpanFields":
        return TimeSpanFields("exposure")

    @classmethod
    def readout(cls) -> "GmosCcdModeFields":
        return GmosCcdModeFields("readout")

    dtax: "GmosSouthDynamicGraphQLField" = GmosSouthDynamicGraphQLField("dtax")
    roi: "GmosSouthDynamicGraphQLField" = GmosSouthDynamicGraphQLField("roi")

    @classmethod
    def grating_config(cls) -> "GmosSouthGratingConfigFields":
        return GmosSouthGratingConfigFields("gratingConfig")

    filter_: "GmosSouthDynamicGraphQLField" = GmosSouthDynamicGraphQLField("filter")

    @classmethod
    def fpu(cls) -> "GmosSouthFpuFields":
        return GmosSouthFpuFields("fpu")

    @classmethod
    def central_wavelength(cls) -> "WavelengthFields":
        return WavelengthFields("centralWavelength")

    def fields(
        self,
        *subfields: Union[
            GmosSouthDynamicGraphQLField,
            "GmosCcdModeFields",
            "GmosSouthFpuFields",
            "GmosSouthGratingConfigFields",
            "TimeSpanFields",
            "WavelengthFields",
        ],
    ) -> "GmosSouthDynamicFields":
        """Subfields should come from the GmosSouthDynamicFields class"""
        self._subfields.extend(subfields)
        return self

    def alias(self, alias: str) -> "GmosSouthDynamicFields":
        self._alias = alias
        return self


class GmosSouthExecutionConfigFields(GraphQLField):
    @classmethod
    def static(cls) -> "GmosSouthStaticFields":
        return GmosSouthStaticFields("static")

    @classmethod
    def acquisition(cls) -> "GmosSouthExecutionSequenceFields":
        return GmosSouthExecutionSequenceFields("acquisition")

    @classmethod
    def science(cls) -> "GmosSouthExecutionSequenceFields":
        return GmosSouthExecutionSequenceFields("science")

    def fields(
        self,
        *subfields: Union[
            GmosSouthExecutionConfigGraphQLField,
            "GmosSouthExecutionSequenceFields",
            "GmosSouthStaticFields",
        ],
    ) -> "GmosSouthExecutionConfigFields":
        """Subfields should come from the GmosSouthExecutionConfigFields class"""
        self._subfields.extend(subfields)
        return self

    def alias(self, alias: str) -> "GmosSouthExecutionConfigFields":
        self._alias = alias
        return self


class GmosSouthExecutionSequenceFields(GraphQLField):
    @classmethod
    def next_atom(cls) -> "GmosSouthAtomFields":
        return GmosSouthAtomFields("nextAtom")

    @classmethod
    def possible_future(cls) -> "GmosSouthAtomFields":
        return GmosSouthAtomFields("possibleFuture")

    has_more: "GmosSouthExecutionSequenceGraphQLField" = (
        GmosSouthExecutionSequenceGraphQLField("hasMore")
    )

    def fields(
        self,
        *subfields: Union[
            GmosSouthExecutionSequenceGraphQLField, "GmosSouthAtomFields"
        ],
    ) -> "GmosSouthExecutionSequenceFields":
        """Subfields should come from the GmosSouthExecutionSequenceFields class"""
        self._subfields.extend(subfields)
        return self

    def alias(self, alias: str) -> "GmosSouthExecutionSequenceFields":
        self._alias = alias
        return self


class GmosSouthFpuFields(GraphQLField):
    @classmethod
    def custom_mask(cls) -> "GmosCustomMaskFields":
        return GmosCustomMaskFields("customMask")

    builtin: "GmosSouthFpuGraphQLField" = GmosSouthFpuGraphQLField("builtin")

    def fields(
        self, *subfields: Union[GmosSouthFpuGraphQLField, "GmosCustomMaskFields"]
    ) -> "GmosSouthFpuFields":
        """Subfields should come from the GmosSouthFpuFields class"""
        self._subfields.extend(subfields)
        return self

    def alias(self, alias: str) -> "GmosSouthFpuFields":
        self._alias = alias
        return self


class GmosSouthGratingConfigFields(GraphQLField):
    grating: "GmosSouthGratingConfigGraphQLField" = GmosSouthGratingConfigGraphQLField(
        "grating"
    )
    order: "GmosSouthGratingConfigGraphQLField" = GmosSouthGratingConfigGraphQLField(
        "order"
    )

    @classmethod
    def wavelength(cls) -> "WavelengthFields":
        return WavelengthFields("wavelength")

    def fields(
        self, *subfields: Union[GmosSouthGratingConfigGraphQLField, "WavelengthFields"]
    ) -> "GmosSouthGratingConfigFields":
        """Subfields should come from the GmosSouthGratingConfigFields class"""
        self._subfields.extend(subfields)
        return self

    def alias(self, alias: str) -> "GmosSouthGratingConfigFields":
        self._alias = alias
        return self


class GmosSouthImagingFields(GraphQLField):
    @classmethod
    def variant(cls) -> "ImagingVariantFields":
        return ImagingVariantFields("variant")

    @classmethod
    def filters(cls) -> "GmosSouthImagingFilterFields":
        return GmosSouthImagingFilterFields("filters")

    @classmethod
    def initial_filters(cls) -> "GmosSouthImagingFilterFields":
        return GmosSouthImagingFilterFields("initialFilters")

    bin: "GmosSouthImagingGraphQLField" = GmosSouthImagingGraphQLField("bin")
    default_bin: "GmosSouthImagingGraphQLField" = GmosSouthImagingGraphQLField(
        "defaultBin"
    )
    explicit_bin: "GmosSouthImagingGraphQLField" = GmosSouthImagingGraphQLField(
        "explicitBin"
    )
    amp_read_mode: "GmosSouthImagingGraphQLField" = GmosSouthImagingGraphQLField(
        "ampReadMode"
    )
    default_amp_read_mode: "GmosSouthImagingGraphQLField" = (
        GmosSouthImagingGraphQLField("defaultAmpReadMode")
    )
    explicit_amp_read_mode: "GmosSouthImagingGraphQLField" = (
        GmosSouthImagingGraphQLField("explicitAmpReadMode")
    )
    amp_gain: "GmosSouthImagingGraphQLField" = GmosSouthImagingGraphQLField("ampGain")
    default_amp_gain: "GmosSouthImagingGraphQLField" = GmosSouthImagingGraphQLField(
        "defaultAmpGain"
    )
    explicit_amp_gain: "GmosSouthImagingGraphQLField" = GmosSouthImagingGraphQLField(
        "explicitAmpGain"
    )
    roi: "GmosSouthImagingGraphQLField" = GmosSouthImagingGraphQLField("roi")
    default_roi: "GmosSouthImagingGraphQLField" = GmosSouthImagingGraphQLField(
        "defaultRoi"
    )
    explicit_roi: "GmosSouthImagingGraphQLField" = GmosSouthImagingGraphQLField(
        "explicitRoi"
    )

    def fields(
        self,
        *subfields: Union[
            GmosSouthImagingGraphQLField,
            "GmosSouthImagingFilterFields",
            "ImagingVariantFields",
        ],
    ) -> "GmosSouthImagingFields":
        """Subfields should come from the GmosSouthImagingFields class"""
        self._subfields.extend(subfields)
        return self

    def alias(self, alias: str) -> "GmosSouthImagingFields":
        self._alias = alias
        return self


class GmosSouthImagingFilterFields(GraphQLField):
    filter_: "GmosSouthImagingFilterGraphQLField" = GmosSouthImagingFilterGraphQLField(
        "filter"
    )

    @classmethod
    def exposure_time_mode(cls) -> "ExposureTimeModeFields":
        return ExposureTimeModeFields("exposureTimeMode")

    def fields(
        self,
        *subfields: Union[GmosSouthImagingFilterGraphQLField, "ExposureTimeModeFields"],
    ) -> "GmosSouthImagingFilterFields":
        """Subfields should come from the GmosSouthImagingFilterFields class"""
        self._subfields.extend(subfields)
        return self

    def alias(self, alias: str) -> "GmosSouthImagingFilterFields":
        self._alias = alias
        return self


class GmosSouthLongSlitFields(GraphQLField):
    grating: "GmosSouthLongSlitGraphQLField" = GmosSouthLongSlitGraphQLField("grating")
    filter_: "GmosSouthLongSlitGraphQLField" = GmosSouthLongSlitGraphQLField("filter")
    fpu: "GmosSouthLongSlitGraphQLField" = GmosSouthLongSlitGraphQLField("fpu")

    @classmethod
    def central_wavelength(cls) -> "WavelengthFields":
        return WavelengthFields("centralWavelength")

    @classmethod
    def exposure_time_mode(cls) -> "ExposureTimeModeFields":
        return ExposureTimeModeFields("exposureTimeMode")

    x_bin: "GmosSouthLongSlitGraphQLField" = GmosSouthLongSlitGraphQLField("xBin")
    default_x_bin: "GmosSouthLongSlitGraphQLField" = GmosSouthLongSlitGraphQLField(
        "defaultXBin"
    )
    explicit_x_bin: "GmosSouthLongSlitGraphQLField" = GmosSouthLongSlitGraphQLField(
        "explicitXBin"
    )
    y_bin: "GmosSouthLongSlitGraphQLField" = GmosSouthLongSlitGraphQLField("yBin")
    default_y_bin: "GmosSouthLongSlitGraphQLField" = GmosSouthLongSlitGraphQLField(
        "defaultYBin"
    )
    explicit_y_bin: "GmosSouthLongSlitGraphQLField" = GmosSouthLongSlitGraphQLField(
        "explicitYBin"
    )
    amp_read_mode: "GmosSouthLongSlitGraphQLField" = GmosSouthLongSlitGraphQLField(
        "ampReadMode"
    )
    default_amp_read_mode: "GmosSouthLongSlitGraphQLField" = (
        GmosSouthLongSlitGraphQLField("defaultAmpReadMode")
    )
    explicit_amp_read_mode: "GmosSouthLongSlitGraphQLField" = (
        GmosSouthLongSlitGraphQLField("explicitAmpReadMode")
    )
    amp_gain: "GmosSouthLongSlitGraphQLField" = GmosSouthLongSlitGraphQLField("ampGain")
    default_amp_gain: "GmosSouthLongSlitGraphQLField" = GmosSouthLongSlitGraphQLField(
        "defaultAmpGain"
    )
    explicit_amp_gain: "GmosSouthLongSlitGraphQLField" = GmosSouthLongSlitGraphQLField(
        "explicitAmpGain"
    )
    roi: "GmosSouthLongSlitGraphQLField" = GmosSouthLongSlitGraphQLField("roi")
    default_roi: "GmosSouthLongSlitGraphQLField" = GmosSouthLongSlitGraphQLField(
        "defaultRoi"
    )
    explicit_roi: "GmosSouthLongSlitGraphQLField" = GmosSouthLongSlitGraphQLField(
        "explicitRoi"
    )

    @classmethod
    def wavelength_dithers(cls) -> "WavelengthDitherFields":
        return WavelengthDitherFields("wavelengthDithers")

    @classmethod
    def default_wavelength_dithers(cls) -> "WavelengthDitherFields":
        return WavelengthDitherFields("defaultWavelengthDithers")

    @classmethod
    def explicit_wavelength_dithers(cls) -> "WavelengthDitherFields":
        return WavelengthDitherFields("explicitWavelengthDithers")

    @classmethod
    def offsets(cls) -> "OffsetQFields":
        return OffsetQFields("offsets")

    @classmethod
    def default_offsets(cls) -> "OffsetQFields":
        return OffsetQFields("defaultOffsets")

    @classmethod
    def explicit_offsets(cls) -> "OffsetQFields":
        return OffsetQFields("explicitOffsets")

    @classmethod
    def spatial_offsets(cls) -> "OffsetQFields":
        return OffsetQFields("spatialOffsets")

    @classmethod
    def default_spatial_offsets(cls) -> "OffsetQFields":
        return OffsetQFields("defaultSpatialOffsets")

    @classmethod
    def explicit_spatial_offsets(cls) -> "OffsetQFields":
        return OffsetQFields("explicitSpatialOffsets")

    @classmethod
    def acquisition(cls) -> "GmosSouthLongSlitAcquisitionFields":
        return GmosSouthLongSlitAcquisitionFields("acquisition")

    initial_grating: "GmosSouthLongSlitGraphQLField" = GmosSouthLongSlitGraphQLField(
        "initialGrating"
    )
    initial_filter: "GmosSouthLongSlitGraphQLField" = GmosSouthLongSlitGraphQLField(
        "initialFilter"
    )
    initial_fpu: "GmosSouthLongSlitGraphQLField" = GmosSouthLongSlitGraphQLField(
        "initialFpu"
    )

    @classmethod
    def initial_central_wavelength(cls) -> "WavelengthFields":
        return WavelengthFields("initialCentralWavelength")

    def fields(
        self,
        *subfields: Union[
            GmosSouthLongSlitGraphQLField,
            "ExposureTimeModeFields",
            "GmosSouthLongSlitAcquisitionFields",
            "OffsetQFields",
            "WavelengthDitherFields",
            "WavelengthFields",
        ],
    ) -> "GmosSouthLongSlitFields":
        """Subfields should come from the GmosSouthLongSlitFields class"""
        self._subfields.extend(subfields)
        return self

    def alias(self, alias: str) -> "GmosSouthLongSlitFields":
        self._alias = alias
        return self


class GmosSouthLongSlitAcquisitionFields(GraphQLField):
    filter_: "GmosSouthLongSlitAcquisitionGraphQLField" = (
        GmosSouthLongSlitAcquisitionGraphQLField("filter")
    )
    default_filter: "GmosSouthLongSlitAcquisitionGraphQLField" = (
        GmosSouthLongSlitAcquisitionGraphQLField("defaultFilter")
    )
    explicit_filter: "GmosSouthLongSlitAcquisitionGraphQLField" = (
        GmosSouthLongSlitAcquisitionGraphQLField("explicitFilter")
    )
    roi: "GmosSouthLongSlitAcquisitionGraphQLField" = (
        GmosSouthLongSlitAcquisitionGraphQLField("roi")
    )
    default_roi: "GmosSouthLongSlitAcquisitionGraphQLField" = (
        GmosSouthLongSlitAcquisitionGraphQLField("defaultRoi")
    )
    explicit_roi: "GmosSouthLongSlitAcquisitionGraphQLField" = (
        GmosSouthLongSlitAcquisitionGraphQLField("explicitRoi")
    )

    @classmethod
    def exposure_time_mode(cls) -> "ExposureTimeModeFields":
        return ExposureTimeModeFields("exposureTimeMode")

    def fields(
        self,
        *subfields: Union[
            GmosSouthLongSlitAcquisitionGraphQLField, "ExposureTimeModeFields"
        ],
    ) -> "GmosSouthLongSlitAcquisitionFields":
        """Subfields should come from the GmosSouthLongSlitAcquisitionFields class"""
        self._subfields.extend(subfields)
        return self

    def alias(self, alias: str) -> "GmosSouthLongSlitAcquisitionFields":
        self._alias = alias
        return self


class GmosSouthMosFields(GraphQLField):
    grating: "GmosSouthMosGraphQLField" = GmosSouthMosGraphQLField("grating")
    filter_: "GmosSouthMosGraphQLField" = GmosSouthMosGraphQLField("filter")

    @classmethod
    def custom_mask(cls) -> "GmosCustomMaskFields":
        return GmosCustomMaskFields("customMask")

    @classmethod
    def central_wavelength(cls) -> "WavelengthFields":
        return WavelengthFields("centralWavelength")

    acquisition_type: "GmosSouthMosGraphQLField" = GmosSouthMosGraphQLField(
        "acquisitionType"
    )

    @classmethod
    def exposure_time_mode(cls) -> "ExposureTimeModeFields":
        return ExposureTimeModeFields("exposureTimeMode")

    x_bin: "GmosSouthMosGraphQLField" = GmosSouthMosGraphQLField("xBin")
    default_x_bin: "GmosSouthMosGraphQLField" = GmosSouthMosGraphQLField("defaultXBin")
    explicit_x_bin: "GmosSouthMosGraphQLField" = GmosSouthMosGraphQLField(
        "explicitXBin"
    )
    y_bin: "GmosSouthMosGraphQLField" = GmosSouthMosGraphQLField("yBin")
    default_y_bin: "GmosSouthMosGraphQLField" = GmosSouthMosGraphQLField("defaultYBin")
    explicit_y_bin: "GmosSouthMosGraphQLField" = GmosSouthMosGraphQLField(
        "explicitYBin"
    )
    amp_read_mode: "GmosSouthMosGraphQLField" = GmosSouthMosGraphQLField("ampReadMode")
    default_amp_read_mode: "GmosSouthMosGraphQLField" = GmosSouthMosGraphQLField(
        "defaultAmpReadMode"
    )
    explicit_amp_read_mode: "GmosSouthMosGraphQLField" = GmosSouthMosGraphQLField(
        "explicitAmpReadMode"
    )
    amp_gain: "GmosSouthMosGraphQLField" = GmosSouthMosGraphQLField("ampGain")
    default_amp_gain: "GmosSouthMosGraphQLField" = GmosSouthMosGraphQLField(
        "defaultAmpGain"
    )
    explicit_amp_gain: "GmosSouthMosGraphQLField" = GmosSouthMosGraphQLField(
        "explicitAmpGain"
    )
    roi: "GmosSouthMosGraphQLField" = GmosSouthMosGraphQLField("roi")
    default_roi: "GmosSouthMosGraphQLField" = GmosSouthMosGraphQLField("defaultRoi")
    explicit_roi: "GmosSouthMosGraphQLField" = GmosSouthMosGraphQLField("explicitRoi")

    @classmethod
    def wavelength_dithers(cls) -> "WavelengthDitherFields":
        return WavelengthDitherFields("wavelengthDithers")

    @classmethod
    def default_wavelength_dithers(cls) -> "WavelengthDitherFields":
        return WavelengthDitherFields("defaultWavelengthDithers")

    @classmethod
    def explicit_wavelength_dithers(cls) -> "WavelengthDitherFields":
        return WavelengthDitherFields("explicitWavelengthDithers")

    @classmethod
    def offsets(cls) -> "OffsetQFields":
        return OffsetQFields("offsets")

    @classmethod
    def default_offsets(cls) -> "OffsetQFields":
        return OffsetQFields("defaultOffsets")

    @classmethod
    def explicit_offsets(cls) -> "OffsetQFields":
        return OffsetQFields("explicitOffsets")

    initial_grating: "GmosSouthMosGraphQLField" = GmosSouthMosGraphQLField(
        "initialGrating"
    )
    initial_filter: "GmosSouthMosGraphQLField" = GmosSouthMosGraphQLField(
        "initialFilter"
    )
    initial_slit_width: "GmosSouthMosGraphQLField" = GmosSouthMosGraphQLField(
        "initialSlitWidth"
    )

    @classmethod
    def initial_central_wavelength(cls) -> "WavelengthFields":
        return WavelengthFields("initialCentralWavelength")

    @classmethod
    def acquisition(cls) -> "GmosSouthMosAcquisitionFields":
        return GmosSouthMosAcquisitionFields("acquisition")

    def fields(
        self,
        *subfields: Union[
            GmosSouthMosGraphQLField,
            "ExposureTimeModeFields",
            "GmosCustomMaskFields",
            "GmosSouthMosAcquisitionFields",
            "OffsetQFields",
            "WavelengthDitherFields",
            "WavelengthFields",
        ],
    ) -> "GmosSouthMosFields":
        """Subfields should come from the GmosSouthMosFields class"""
        self._subfields.extend(subfields)
        return self

    def alias(self, alias: str) -> "GmosSouthMosFields":
        self._alias = alias
        return self


class GmosSouthMosAcquisitionFields(GraphQLField):
    filter_: "GmosSouthMosAcquisitionGraphQLField" = (
        GmosSouthMosAcquisitionGraphQLField("filter")
    )
    default_filter: "GmosSouthMosAcquisitionGraphQLField" = (
        GmosSouthMosAcquisitionGraphQLField("defaultFilter")
    )
    explicit_filter: "GmosSouthMosAcquisitionGraphQLField" = (
        GmosSouthMosAcquisitionGraphQLField("explicitFilter")
    )

    @classmethod
    def exposure_time_mode(cls) -> "ExposureTimeModeFields":
        return ExposureTimeModeFields("exposureTimeMode")

    def fields(
        self,
        *subfields: Union[
            GmosSouthMosAcquisitionGraphQLField, "ExposureTimeModeFields"
        ],
    ) -> "GmosSouthMosAcquisitionFields":
        """Subfields should come from the GmosSouthMosAcquisitionFields class"""
        self._subfields.extend(subfields)
        return self

    def alias(self, alias: str) -> "GmosSouthMosAcquisitionFields":
        self._alias = alias
        return self


class GmosSouthStaticFields(GraphQLField):
    stage_mode: "GmosSouthStaticGraphQLField" = GmosSouthStaticGraphQLField("stageMode")
    detector: "GmosSouthStaticGraphQLField" = GmosSouthStaticGraphQLField("detector")
    mos_pre_imaging: "GmosSouthStaticGraphQLField" = GmosSouthStaticGraphQLField(
        "mosPreImaging"
    )

    @classmethod
    def nod_and_shuffle(cls) -> "GmosNodAndShuffleFields":
        return GmosNodAndShuffleFields("nodAndShuffle")

    def fields(
        self, *subfields: Union[GmosSouthStaticGraphQLField, "GmosNodAndShuffleFields"]
    ) -> "GmosSouthStaticFields":
        """Subfields should come from the GmosSouthStaticFields class"""
        self._subfields.extend(subfields)
        return self

    def alias(self, alias: str) -> "GmosSouthStaticFields":
        self._alias = alias
        return self


class GmosSouthStepFields(GraphQLField):
    @classmethod
    def instrument_config(cls) -> "GmosSouthDynamicFields":
        return GmosSouthDynamicFields("instrumentConfig")

    id: "GmosSouthStepGraphQLField" = GmosSouthStepGraphQLField("id")
    breakpoint: "GmosSouthStepGraphQLField" = GmosSouthStepGraphQLField("breakpoint")

    @classmethod
    def step_config(cls) -> "StepConfigInterface":
        return StepConfigInterface("stepConfig")

    @classmethod
    def telescope_config(cls) -> "TelescopeConfigFields":
        return TelescopeConfigFields("telescopeConfig")

    @classmethod
    def estimate(cls) -> "StepEstimateFields":
        return StepEstimateFields("estimate")

    observe_class: "GmosSouthStepGraphQLField" = GmosSouthStepGraphQLField(
        "observeClass"
    )

    def fields(
        self,
        *subfields: Union[
            GmosSouthStepGraphQLField,
            "GmosSouthDynamicFields",
            "StepConfigInterface",
            "StepEstimateFields",
            "TelescopeConfigFields",
        ],
    ) -> "GmosSouthStepFields":
        """Subfields should come from the GmosSouthStepFields class"""
        self._subfields.extend(subfields)
        return self

    def alias(self, alias: str) -> "GmosSouthStepFields":
        self._alias = alias
        return self


class GnirsAcquisitionMirrorOutFields(GraphQLField):
    prism: "GnirsAcquisitionMirrorOutGraphQLField" = (
        GnirsAcquisitionMirrorOutGraphQLField("prism")
    )
    grating: "GnirsAcquisitionMirrorOutGraphQLField" = (
        GnirsAcquisitionMirrorOutGraphQLField("grating")
    )

    @classmethod
    def wavelength(cls) -> "WavelengthFields":
        return WavelengthFields("wavelength")

    def fields(
        self,
        *subfields: Union[GnirsAcquisitionMirrorOutGraphQLField, "WavelengthFields"],
    ) -> "GnirsAcquisitionMirrorOutFields":
        """Subfields should come from the GnirsAcquisitionMirrorOutFields class"""
        self._subfields.extend(subfields)
        return self

    def alias(self, alias: str) -> "GnirsAcquisitionMirrorOutFields":
        self._alias = alias
        return self


class GnirsAtomFields(GraphQLField):
    id: "GnirsAtomGraphQLField" = GnirsAtomGraphQLField("id")
    description: "GnirsAtomGraphQLField" = GnirsAtomGraphQLField("description")
    observe_class: "GnirsAtomGraphQLField" = GnirsAtomGraphQLField("observeClass")

    @classmethod
    def steps(cls) -> "GnirsStepFields":
        return GnirsStepFields("steps")

    def fields(
        self, *subfields: Union[GnirsAtomGraphQLField, "GnirsStepFields"]
    ) -> "GnirsAtomFields":
        """Subfields should come from the GnirsAtomFields class"""
        self._subfields.extend(subfields)
        return self

    def alias(self, alias: str) -> "GnirsAtomFields":
        self._alias = alias
        return self


class GnirsCentralWavelengthConfigFields(GraphQLField):
    @classmethod
    def central_wavelength(cls) -> "WavelengthFields":
        return WavelengthFields("centralWavelength")

    @classmethod
    def exposure_time_mode(cls) -> "ExposureTimeModeFields":
        return ExposureTimeModeFields("exposureTimeMode")

    coadds: "GnirsCentralWavelengthConfigGraphQLField" = (
        GnirsCentralWavelengthConfigGraphQLField("coadds")
    )

    def fields(
        self,
        *subfields: Union[
            GnirsCentralWavelengthConfigGraphQLField,
            "ExposureTimeModeFields",
            "WavelengthFields",
        ],
    ) -> "GnirsCentralWavelengthConfigFields":
        """Subfields should come from the GnirsCentralWavelengthConfigFields class"""
        self._subfields.extend(subfields)
        return self

    def alias(self, alias: str) -> "GnirsCentralWavelengthConfigFields":
        self._alias = alias
        return self


class GnirsDynamicFields(GraphQLField):
    @classmethod
    def exposure(cls) -> "TimeSpanFields":
        return TimeSpanFields("exposure")

    coadds: "GnirsDynamicGraphQLField" = GnirsDynamicGraphQLField("coadds")

    @classmethod
    def central_wavelength(cls) -> "WavelengthFields":
        return WavelengthFields("centralWavelength")

    filter_: "GnirsDynamicGraphQLField" = GnirsDynamicGraphQLField("filter")
    decker: "GnirsDynamicGraphQLField" = GnirsDynamicGraphQLField("decker")
    fpu_slit: "GnirsDynamicGraphQLField" = GnirsDynamicGraphQLField("fpuSlit")
    fpu_other: "GnirsDynamicGraphQLField" = GnirsDynamicGraphQLField("fpuOther")
    fpu_ifu: "GnirsDynamicGraphQLField" = GnirsDynamicGraphQLField("fpuIfu")

    @classmethod
    def acquisition_mirror_out(cls) -> "GnirsAcquisitionMirrorOutFields":
        return GnirsAcquisitionMirrorOutFields("acquisitionMirrorOut")

    camera: "GnirsDynamicGraphQLField" = GnirsDynamicGraphQLField("camera")
    focus_motor_steps: "GnirsDynamicGraphQLField" = GnirsDynamicGraphQLField(
        "focusMotorSteps"
    )
    read_mode: "GnirsDynamicGraphQLField" = GnirsDynamicGraphQLField("readMode")

    def fields(
        self,
        *subfields: Union[
            GnirsDynamicGraphQLField,
            "GnirsAcquisitionMirrorOutFields",
            "TimeSpanFields",
            "WavelengthFields",
        ],
    ) -> "GnirsDynamicFields":
        """Subfields should come from the GnirsDynamicFields class"""
        self._subfields.extend(subfields)
        return self

    def alias(self, alias: str) -> "GnirsDynamicFields":
        self._alias = alias
        return self


class GnirsExecutionConfigFields(GraphQLField):
    @classmethod
    def static(cls) -> "GnirsStaticFields":
        return GnirsStaticFields("static")

    @classmethod
    def acquisition(cls) -> "GnirsExecutionSequenceFields":
        return GnirsExecutionSequenceFields("acquisition")

    @classmethod
    def science(cls) -> "GnirsExecutionSequenceFields":
        return GnirsExecutionSequenceFields("science")

    def fields(
        self,
        *subfields: Union[
            GnirsExecutionConfigGraphQLField,
            "GnirsExecutionSequenceFields",
            "GnirsStaticFields",
        ],
    ) -> "GnirsExecutionConfigFields":
        """Subfields should come from the GnirsExecutionConfigFields class"""
        self._subfields.extend(subfields)
        return self

    def alias(self, alias: str) -> "GnirsExecutionConfigFields":
        self._alias = alias
        return self


class GnirsExecutionSequenceFields(GraphQLField):
    @classmethod
    def next_atom(cls) -> "GnirsAtomFields":
        return GnirsAtomFields("nextAtom")

    @classmethod
    def possible_future(cls) -> "GnirsAtomFields":
        return GnirsAtomFields("possibleFuture")

    has_more: "GnirsExecutionSequenceGraphQLField" = GnirsExecutionSequenceGraphQLField(
        "hasMore"
    )

    def fields(
        self, *subfields: Union[GnirsExecutionSequenceGraphQLField, "GnirsAtomFields"]
    ) -> "GnirsExecutionSequenceFields":
        """Subfields should come from the GnirsExecutionSequenceFields class"""
        self._subfields.extend(subfields)
        return self

    def alias(self, alias: str) -> "GnirsExecutionSequenceFields":
        self._alias = alias
        return self


class GnirsIfuFields(GraphQLField):
    fpu: "GnirsIfuGraphQLField" = GnirsIfuGraphQLField("fpu")
    initial_fpu: "GnirsIfuGraphQLField" = GnirsIfuGraphQLField("initialFpu")

    @classmethod
    def telescope_configs(cls) -> "TelescopeConfigFields":
        return TelescopeConfigFields("telescopeConfigs")

    def fields(
        self, *subfields: Union[GnirsIfuGraphQLField, "TelescopeConfigFields"]
    ) -> "GnirsIfuFields":
        """Subfields should come from the GnirsIfuFields class"""
        self._subfields.extend(subfields)
        return self

    def alias(self, alias: str) -> "GnirsIfuFields":
        self._alias = alias
        return self


class GnirsImagingFields(GraphQLField):
    @classmethod
    def variant(cls) -> "ImagingVariantFields":
        return ImagingVariantFields("variant")

    @classmethod
    def filters(cls) -> "GnirsImagingFilterFields":
        return GnirsImagingFilterFields("filters")

    @classmethod
    def initial_filters(cls) -> "GnirsImagingFilterFields":
        return GnirsImagingFilterFields("initialFilters")

    camera: "GnirsImagingGraphQLField" = GnirsImagingGraphQLField("camera")
    coadds: "GnirsImagingGraphQLField" = GnirsImagingGraphQLField("coadds")
    explicit_read_mode: "GnirsImagingGraphQLField" = GnirsImagingGraphQLField(
        "explicitReadMode"
    )
    well_depth: "GnirsImagingGraphQLField" = GnirsImagingGraphQLField("wellDepth")
    explicit_well_depth: "GnirsImagingGraphQLField" = GnirsImagingGraphQLField(
        "explicitWellDepth"
    )
    default_well_depth: "GnirsImagingGraphQLField" = GnirsImagingGraphQLField(
        "defaultWellDepth"
    )

    @classmethod
    def acquisition(cls) -> "GnirsImagingAcquisitionFields":
        return GnirsImagingAcquisitionFields("acquisition")

    def fields(
        self,
        *subfields: Union[
            GnirsImagingGraphQLField,
            "GnirsImagingAcquisitionFields",
            "GnirsImagingFilterFields",
            "ImagingVariantFields",
        ],
    ) -> "GnirsImagingFields":
        """Subfields should come from the GnirsImagingFields class"""
        self._subfields.extend(subfields)
        return self

    def alias(self, alias: str) -> "GnirsImagingFields":
        self._alias = alias
        return self


class GnirsImagingAcquisitionFields(GraphQLField):
    @classmethod
    def exposure_time_mode(cls) -> "ExposureTimeModeFields":
        return ExposureTimeModeFields("exposureTimeMode")

    coadds: "GnirsImagingAcquisitionGraphQLField" = GnirsImagingAcquisitionGraphQLField(
        "coadds"
    )
    explicit_acquisition_type: "GnirsImagingAcquisitionGraphQLField" = (
        GnirsImagingAcquisitionGraphQLField("explicitAcquisitionType")
    )
    explicit_filter: "GnirsImagingAcquisitionGraphQLField" = (
        GnirsImagingAcquisitionGraphQLField("explicitFilter")
    )

    @classmethod
    def sky_offset(cls) -> "OffsetFields":
        return OffsetFields("skyOffset")

    def fields(
        self,
        *subfields: Union[
            GnirsImagingAcquisitionGraphQLField,
            "ExposureTimeModeFields",
            "OffsetFields",
        ],
    ) -> "GnirsImagingAcquisitionFields":
        """Subfields should come from the GnirsImagingAcquisitionFields class"""
        self._subfields.extend(subfields)
        return self

    def alias(self, alias: str) -> "GnirsImagingAcquisitionFields":
        self._alias = alias
        return self


class GnirsImagingFilterFields(GraphQLField):
    filter_: "GnirsImagingFilterGraphQLField" = GnirsImagingFilterGraphQLField("filter")

    @classmethod
    def exposure_time_mode(cls) -> "ExposureTimeModeFields":
        return ExposureTimeModeFields("exposureTimeMode")

    def fields(
        self,
        *subfields: Union[GnirsImagingFilterGraphQLField, "ExposureTimeModeFields"],
    ) -> "GnirsImagingFilterFields":
        """Subfields should come from the GnirsImagingFilterFields class"""
        self._subfields.extend(subfields)
        return self

    def alias(self, alias: str) -> "GnirsImagingFilterFields":
        self._alias = alias
        return self


class GnirsSlitFields(GraphQLField):
    fpu: "GnirsSlitGraphQLField" = GnirsSlitGraphQLField("fpu")
    initial_fpu: "GnirsSlitGraphQLField" = GnirsSlitGraphQLField("initialFpu")

    @classmethod
    def telescope_configs(cls) -> "SlitTelescopeConfigsFields":
        return SlitTelescopeConfigsFields("telescopeConfigs")

    @classmethod
    def default_telescope_configs(cls) -> "SlitTelescopeConfigsFields":
        return SlitTelescopeConfigsFields("defaultTelescopeConfigs")

    @classmethod
    def explicit_telescope_configs(cls) -> "SlitTelescopeConfigsFields":
        return SlitTelescopeConfigsFields("explicitTelescopeConfigs")

    def fields(
        self, *subfields: Union[GnirsSlitGraphQLField, "SlitTelescopeConfigsFields"]
    ) -> "GnirsSlitFields":
        """Subfields should come from the GnirsSlitFields class"""
        self._subfields.extend(subfields)
        return self

    def alias(self, alias: str) -> "GnirsSlitFields":
        self._alias = alias
        return self


class GnirsSpectroscopyFields(GraphQLField):
    grating: "GnirsSpectroscopyGraphQLField" = GnirsSpectroscopyGraphQLField("grating")
    explicit_grating: "GnirsSpectroscopyGraphQLField" = GnirsSpectroscopyGraphQLField(
        "explicitGrating"
    )
    initial_grating: "GnirsSpectroscopyGraphQLField" = GnirsSpectroscopyGraphQLField(
        "initialGrating"
    )
    prism: "GnirsSpectroscopyGraphQLField" = GnirsSpectroscopyGraphQLField("prism")
    explicit_prism: "GnirsSpectroscopyGraphQLField" = GnirsSpectroscopyGraphQLField(
        "explicitPrism"
    )
    initial_prism: "GnirsSpectroscopyGraphQLField" = GnirsSpectroscopyGraphQLField(
        "initialPrism"
    )

    @classmethod
    def central_wavelengths(cls) -> "GnirsCentralWavelengthConfigFields":
        return GnirsCentralWavelengthConfigFields("centralWavelengths")

    @classmethod
    def initial_central_wavelengths(cls) -> "GnirsCentralWavelengthConfigFields":
        return GnirsCentralWavelengthConfigFields("initialCentralWavelengths")

    camera: "GnirsSpectroscopyGraphQLField" = GnirsSpectroscopyGraphQLField("camera")
    initial_camera: "GnirsSpectroscopyGraphQLField" = GnirsSpectroscopyGraphQLField(
        "initialCamera"
    )

    @classmethod
    def slit(cls) -> "GnirsSlitFields":
        return GnirsSlitFields("slit")

    @classmethod
    def ifu(cls) -> "GnirsIfuFields":
        return GnirsIfuFields("ifu")

    filter_: "GnirsSpectroscopyGraphQLField" = GnirsSpectroscopyGraphQLField("filter")
    initial_filter: "GnirsSpectroscopyGraphQLField" = GnirsSpectroscopyGraphQLField(
        "initialFilter"
    )
    decker: "GnirsSpectroscopyGraphQLField" = GnirsSpectroscopyGraphQLField("decker")
    explicit_decker: "GnirsSpectroscopyGraphQLField" = GnirsSpectroscopyGraphQLField(
        "explicitDecker"
    )
    default_decker: "GnirsSpectroscopyGraphQLField" = GnirsSpectroscopyGraphQLField(
        "defaultDecker"
    )
    explicit_read_mode: "GnirsSpectroscopyGraphQLField" = GnirsSpectroscopyGraphQLField(
        "explicitReadMode"
    )
    well_depth: "GnirsSpectroscopyGraphQLField" = GnirsSpectroscopyGraphQLField(
        "wellDepth"
    )
    explicit_well_depth: "GnirsSpectroscopyGraphQLField" = (
        GnirsSpectroscopyGraphQLField("explicitWellDepth")
    )
    default_well_depth: "GnirsSpectroscopyGraphQLField" = GnirsSpectroscopyGraphQLField(
        "defaultWellDepth"
    )
    explicit_focus_motor_steps: "GnirsSpectroscopyGraphQLField" = (
        GnirsSpectroscopyGraphQLField("explicitFocusMotorSteps")
    )

    @classmethod
    def acquisition(cls) -> "GnirsSpectroscopyAcquisitionFields":
        return GnirsSpectroscopyAcquisitionFields("acquisition")

    @classmethod
    def telluric_type(cls) -> "TelluricTypeFields":
        return TelluricTypeFields("telluricType")

    def fields(
        self,
        *subfields: Union[
            GnirsSpectroscopyGraphQLField,
            "GnirsCentralWavelengthConfigFields",
            "GnirsIfuFields",
            "GnirsSlitFields",
            "GnirsSpectroscopyAcquisitionFields",
            "TelluricTypeFields",
        ],
    ) -> "GnirsSpectroscopyFields":
        """Subfields should come from the GnirsSpectroscopyFields class"""
        self._subfields.extend(subfields)
        return self

    def alias(self, alias: str) -> "GnirsSpectroscopyFields":
        self._alias = alias
        return self


class GnirsSpectroscopyAcquisitionFields(GraphQLField):
    @classmethod
    def exposure_time_mode(cls) -> "ExposureTimeModeFields":
        return ExposureTimeModeFields("exposureTimeMode")

    coadds: "GnirsSpectroscopyAcquisitionGraphQLField" = (
        GnirsSpectroscopyAcquisitionGraphQLField("coadds")
    )
    explicit_acquisition_type: "GnirsSpectroscopyAcquisitionGraphQLField" = (
        GnirsSpectroscopyAcquisitionGraphQLField("explicitAcquisitionType")
    )
    explicit_filter: "GnirsSpectroscopyAcquisitionGraphQLField" = (
        GnirsSpectroscopyAcquisitionGraphQLField("explicitFilter")
    )

    @classmethod
    def sky_offset(cls) -> "OffsetFields":
        return OffsetFields("skyOffset")

    def fields(
        self,
        *subfields: Union[
            GnirsSpectroscopyAcquisitionGraphQLField,
            "ExposureTimeModeFields",
            "OffsetFields",
        ],
    ) -> "GnirsSpectroscopyAcquisitionFields":
        """Subfields should come from the GnirsSpectroscopyAcquisitionFields class"""
        self._subfields.extend(subfields)
        return self

    def alias(self, alias: str) -> "GnirsSpectroscopyAcquisitionFields":
        self._alias = alias
        return self


class GnirsStaticFields(GraphQLField):
    well_depth: "GnirsStaticGraphQLField" = GnirsStaticGraphQLField("wellDepth")

    def fields(self, *subfields: GnirsStaticGraphQLField) -> "GnirsStaticFields":
        """Subfields should come from the GnirsStaticFields class"""
        self._subfields.extend(subfields)
        return self

    def alias(self, alias: str) -> "GnirsStaticFields":
        self._alias = alias
        return self


class GnirsStepFields(GraphQLField):
    @classmethod
    def instrument_config(cls) -> "GnirsDynamicFields":
        return GnirsDynamicFields("instrumentConfig")

    id: "GnirsStepGraphQLField" = GnirsStepGraphQLField("id")
    breakpoint: "GnirsStepGraphQLField" = GnirsStepGraphQLField("breakpoint")

    @classmethod
    def step_config(cls) -> "StepConfigInterface":
        return StepConfigInterface("stepConfig")

    @classmethod
    def telescope_config(cls) -> "TelescopeConfigFields":
        return TelescopeConfigFields("telescopeConfig")

    @classmethod
    def estimate(cls) -> "StepEstimateFields":
        return StepEstimateFields("estimate")

    observe_class: "GnirsStepGraphQLField" = GnirsStepGraphQLField("observeClass")

    def fields(
        self,
        *subfields: Union[
            GnirsStepGraphQLField,
            "GnirsDynamicFields",
            "StepConfigInterface",
            "StepEstimateFields",
            "TelescopeConfigFields",
        ],
    ) -> "GnirsStepFields":
        """Subfields should come from the GnirsStepFields class"""
        self._subfields.extend(subfields)
        return self

    def alias(self, alias: str) -> "GnirsStepFields":
        self._alias = alias
        return self


class GoaPropertiesFields(GraphQLField):
    proprietary_months: "GoaPropertiesGraphQLField" = GoaPropertiesGraphQLField(
        "proprietaryMonths"
    )
    should_notify: "GoaPropertiesGraphQLField" = GoaPropertiesGraphQLField(
        "shouldNotify"
    )
    private_header: "GoaPropertiesGraphQLField" = GoaPropertiesGraphQLField(
        "privateHeader"
    )

    def fields(self, *subfields: GoaPropertiesGraphQLField) -> "GoaPropertiesFields":
        """Subfields should come from the GoaPropertiesFields class"""
        self._subfields.extend(subfields)
        return self

    def alias(self, alias: str) -> "GoaPropertiesFields":
        self._alias = alias
        return self


class GroupFields(GraphQLField):
    id: "GroupGraphQLField" = GroupGraphQLField("id")
    parent_id: "GroupGraphQLField" = GroupGraphQLField("parentId")
    parent_index: "GroupGraphQLField" = GroupGraphQLField("parentIndex")

    @classmethod
    def program(cls) -> "ProgramFields":
        return ProgramFields("program")

    name: "GroupGraphQLField" = GroupGraphQLField("name")
    description: "GroupGraphQLField" = GroupGraphQLField("description")
    minimum_required: "GroupGraphQLField" = GroupGraphQLField("minimumRequired")
    ordered: "GroupGraphQLField" = GroupGraphQLField("ordered")

    @classmethod
    def minimum_interval(cls) -> "TimeSpanFields":
        return TimeSpanFields("minimumInterval")

    @classmethod
    def maximum_interval(cls) -> "TimeSpanFields":
        return TimeSpanFields("maximumInterval")

    same_night: "GroupGraphQLField" = GroupGraphQLField("sameNight")

    @classmethod
    def elements(cls, include_deleted: bool) -> "GroupElementFields":
        arguments: dict[str, dict[str, Any]] = {
            "includeDeleted": {"type": "Boolean!", "value": include_deleted}
        }
        cleared_arguments = {
            key: value for key, value in arguments.items() if value["value"] is not None
        }
        return GroupElementFields("elements", arguments=cleared_arguments)

    @classmethod
    def time_estimate_range(cls) -> "CalculatedCategorizedTimeRangeFields":
        return CalculatedCategorizedTimeRangeFields("timeEstimateRange")

    @classmethod
    def time_estimate_banded(cls) -> "CalculatedBandedTimeFields":
        return CalculatedBandedTimeFields("timeEstimateBanded")

    existence: "GroupGraphQLField" = GroupGraphQLField("existence")
    system: "GroupGraphQLField" = GroupGraphQLField("system")
    calibration_roles: "GroupGraphQLField" = GroupGraphQLField("calibrationRoles")

    def fields(
        self,
        *subfields: Union[
            GroupGraphQLField,
            "CalculatedBandedTimeFields",
            "CalculatedCategorizedTimeRangeFields",
            "GroupElementFields",
            "ProgramFields",
            "TimeSpanFields",
        ],
    ) -> "GroupFields":
        """Subfields should come from the GroupFields class"""
        self._subfields.extend(subfields)
        return self

    def alias(self, alias: str) -> "GroupFields":
        self._alias = alias
        return self


class GroupElementFields(GraphQLField):
    parent_group_id: "GroupElementGraphQLField" = GroupElementGraphQLField(
        "parentGroupId"
    )
    parent_index: "GroupElementGraphQLField" = GroupElementGraphQLField("parentIndex")

    @classmethod
    def group(cls) -> "GroupFields":
        return GroupFields("group")

    @classmethod
    def observation(cls) -> "ObservationFields":
        return ObservationFields("observation")

    existence: "GroupElementGraphQLField" = GroupElementGraphQLField("existence")

    def fields(
        self,
        *subfields: Union[GroupElementGraphQLField, "GroupFields", "ObservationFields"],
    ) -> "GroupElementFields":
        """Subfields should come from the GroupElementFields class"""
        self._subfields.extend(subfields)
        return self

    def alias(self, alias: str) -> "GroupElementFields":
        self._alias = alias
        return self


class GroupedImagingVariantFields(GraphQLField):
    order: "GroupedImagingVariantGraphQLField" = GroupedImagingVariantGraphQLField(
        "order"
    )

    @classmethod
    def offsets(cls) -> "TelescopeConfigGeneratorFields":
        return TelescopeConfigGeneratorFields("offsets")

    sky_count: "GroupedImagingVariantGraphQLField" = GroupedImagingVariantGraphQLField(
        "skyCount"
    )

    @classmethod
    def sky_offsets(cls) -> "TelescopeConfigGeneratorFields":
        return TelescopeConfigGeneratorFields("skyOffsets")

    def fields(
        self,
        *subfields: Union[
            GroupedImagingVariantGraphQLField, "TelescopeConfigGeneratorFields"
        ],
    ) -> "GroupedImagingVariantFields":
        """Subfields should come from the GroupedImagingVariantFields class"""
        self._subfields.extend(subfields)
        return self

    def alias(self, alias: str) -> "GroupedImagingVariantFields":
        self._alias = alias
        return self


class GuideAvailabilityPeriodFields(GraphQLField):
    start: "GuideAvailabilityPeriodGraphQLField" = GuideAvailabilityPeriodGraphQLField(
        "start"
    )
    end: "GuideAvailabilityPeriodGraphQLField" = GuideAvailabilityPeriodGraphQLField(
        "end"
    )

    @classmethod
    def pos_angles(cls) -> "AngleFields":
        return AngleFields("posAngles")

    def fields(
        self, *subfields: Union[GuideAvailabilityPeriodGraphQLField, "AngleFields"]
    ) -> "GuideAvailabilityPeriodFields":
        """Subfields should come from the GuideAvailabilityPeriodFields class"""
        self._subfields.extend(subfields)
        return self

    def alias(self, alias: str) -> "GuideAvailabilityPeriodFields":
        self._alias = alias
        return self


class GuideEnvironmentFields(GraphQLField):
    @classmethod
    def pos_angle(cls) -> "AngleFields":
        return AngleFields("posAngle")

    @classmethod
    def guide_targets(cls) -> "GuideTargetFields":
        return GuideTargetFields("guideTargets")

    def fields(
        self,
        *subfields: Union[
            GuideEnvironmentGraphQLField, "AngleFields", "GuideTargetFields"
        ],
    ) -> "GuideEnvironmentFields":
        """Subfields should come from the GuideEnvironmentFields class"""
        self._subfields.extend(subfields)
        return self

    def alias(self, alias: str) -> "GuideEnvironmentFields":
        self._alias = alias
        return self


class GuideTargetFields(GraphQLField):
    probe: "GuideTargetGraphQLField" = GuideTargetGraphQLField("probe")
    name: "GuideTargetGraphQLField" = GuideTargetGraphQLField("name")

    @classmethod
    def source_profile(cls) -> "SourceProfileFields":
        return SourceProfileFields("sourceProfile")

    @classmethod
    def sidereal(cls) -> "SiderealFields":
        return SiderealFields("sidereal")

    @classmethod
    def nonsidereal(cls) -> "NonsiderealFields":
        return NonsiderealFields("nonsidereal")

    def fields(
        self,
        *subfields: Union[
            GuideTargetGraphQLField,
            "NonsiderealFields",
            "SiderealFields",
            "SourceProfileFields",
        ],
    ) -> "GuideTargetFields":
        """Subfields should come from the GuideTargetFields class"""
        self._subfields.extend(subfields)
        return self

    def alias(self, alias: str) -> "GuideTargetFields":
        self._alias = alias
        return self


class HasExchangePartnerFields(GraphQLField):
    link_type: "HasExchangePartnerGraphQLField" = HasExchangePartnerGraphQLField(
        "linkType"
    )
    exchange_partner: "HasExchangePartnerGraphQLField" = HasExchangePartnerGraphQLField(
        "exchangePartner"
    )

    def fields(
        self, *subfields: HasExchangePartnerGraphQLField
    ) -> "HasExchangePartnerFields":
        """Subfields should come from the HasExchangePartnerFields class"""
        self._subfields.extend(subfields)
        return self

    def alias(self, alias: str) -> "HasExchangePartnerFields":
        self._alias = alias
        return self


class HasGeminiPartnerFields(GraphQLField):
    link_type: "HasGeminiPartnerGraphQLField" = HasGeminiPartnerGraphQLField("linkType")
    gemini_partner: "HasGeminiPartnerGraphQLField" = HasGeminiPartnerGraphQLField(
        "geminiPartner"
    )

    def fields(
        self, *subfields: HasGeminiPartnerGraphQLField
    ) -> "HasGeminiPartnerFields":
        """Subfields should come from the HasGeminiPartnerFields class"""
        self._subfields.extend(subfields)
        return self

    def alias(self, alias: str) -> "HasGeminiPartnerFields":
        self._alias = alias
        return self


class HasNonPartnerFields(GraphQLField):
    link_type: "HasNonPartnerGraphQLField" = HasNonPartnerGraphQLField("linkType")

    def fields(self, *subfields: HasNonPartnerGraphQLField) -> "HasNonPartnerFields":
        """Subfields should come from the HasNonPartnerFields class"""
        self._subfields.extend(subfields)
        return self

    def alias(self, alias: str) -> "HasNonPartnerFields":
        self._alias = alias
        return self


class HasUnspecifiedPartnerFields(GraphQLField):
    link_type: "HasUnspecifiedPartnerGraphQLField" = HasUnspecifiedPartnerGraphQLField(
        "linkType"
    )

    def fields(
        self, *subfields: HasUnspecifiedPartnerGraphQLField
    ) -> "HasUnspecifiedPartnerFields":
        """Subfields should come from the HasUnspecifiedPartnerFields class"""
        self._subfields.extend(subfields)
        return self

    def alias(self, alias: str) -> "HasUnspecifiedPartnerFields":
        self._alias = alias
        return self


class HourAngleRangeFields(GraphQLField):
    min_hours: "HourAngleRangeGraphQLField" = HourAngleRangeGraphQLField("minHours")
    max_hours: "HourAngleRangeGraphQLField" = HourAngleRangeGraphQLField("maxHours")

    def fields(self, *subfields: HourAngleRangeGraphQLField) -> "HourAngleRangeFields":
        """Subfields should come from the HourAngleRangeFields class"""
        self._subfields.extend(subfields)
        return self

    def alias(self, alias: str) -> "HourAngleRangeFields":
        self._alias = alias
        return self


class Igrins2AtomFields(GraphQLField):
    id: "Igrins2AtomGraphQLField" = Igrins2AtomGraphQLField("id")
    description: "Igrins2AtomGraphQLField" = Igrins2AtomGraphQLField("description")
    observe_class: "Igrins2AtomGraphQLField" = Igrins2AtomGraphQLField("observeClass")

    @classmethod
    def steps(cls) -> "Igrins2StepFields":
        return Igrins2StepFields("steps")

    def fields(
        self, *subfields: Union[Igrins2AtomGraphQLField, "Igrins2StepFields"]
    ) -> "Igrins2AtomFields":
        """Subfields should come from the Igrins2AtomFields class"""
        self._subfields.extend(subfields)
        return self

    def alias(self, alias: str) -> "Igrins2AtomFields":
        self._alias = alias
        return self


class Igrins2DynamicFields(GraphQLField):
    @classmethod
    def exposure(cls) -> "TimeSpanFields":
        return TimeSpanFields("exposure")

    @classmethod
    def central_wavelength(cls) -> "WavelengthFields":
        return WavelengthFields("centralWavelength")

    def fields(
        self,
        *subfields: Union[
            Igrins2DynamicGraphQLField, "TimeSpanFields", "WavelengthFields"
        ],
    ) -> "Igrins2DynamicFields":
        """Subfields should come from the Igrins2DynamicFields class"""
        self._subfields.extend(subfields)
        return self

    def alias(self, alias: str) -> "Igrins2DynamicFields":
        self._alias = alias
        return self


class Igrins2ExecutionConfigFields(GraphQLField):
    @classmethod
    def static(cls) -> "Igrins2StaticFields":
        return Igrins2StaticFields("static")

    @classmethod
    def acquisition(cls) -> "Igrins2ExecutionSequenceFields":
        return Igrins2ExecutionSequenceFields("acquisition")

    @classmethod
    def science(cls) -> "Igrins2ExecutionSequenceFields":
        return Igrins2ExecutionSequenceFields("science")

    def fields(
        self,
        *subfields: Union[
            Igrins2ExecutionConfigGraphQLField,
            "Igrins2ExecutionSequenceFields",
            "Igrins2StaticFields",
        ],
    ) -> "Igrins2ExecutionConfigFields":
        """Subfields should come from the Igrins2ExecutionConfigFields class"""
        self._subfields.extend(subfields)
        return self

    def alias(self, alias: str) -> "Igrins2ExecutionConfigFields":
        self._alias = alias
        return self


class Igrins2ExecutionSequenceFields(GraphQLField):
    @classmethod
    def next_atom(cls) -> "Igrins2AtomFields":
        return Igrins2AtomFields("nextAtom")

    @classmethod
    def possible_future(cls) -> "Igrins2AtomFields":
        return Igrins2AtomFields("possibleFuture")

    has_more: "Igrins2ExecutionSequenceGraphQLField" = (
        Igrins2ExecutionSequenceGraphQLField("hasMore")
    )

    def fields(
        self,
        *subfields: Union[Igrins2ExecutionSequenceGraphQLField, "Igrins2AtomFields"],
    ) -> "Igrins2ExecutionSequenceFields":
        """Subfields should come from the Igrins2ExecutionSequenceFields class"""
        self._subfields.extend(subfields)
        return self

    def alias(self, alias: str) -> "Igrins2ExecutionSequenceFields":
        self._alias = alias
        return self


class Igrins2LongSlitFields(GraphQLField):
    @classmethod
    def exposure_time_mode(cls) -> "ExposureTimeModeFields":
        return ExposureTimeModeFields("exposureTimeMode")

    @classmethod
    def svc(cls) -> "Igrins2SvcConfigFields":
        return Igrins2SvcConfigFields("svc")

    @classmethod
    def telescope_configs(cls) -> "SlitTelescopeConfigsFields":
        return SlitTelescopeConfigsFields("telescopeConfigs")

    @classmethod
    def default_telescope_configs(cls) -> "SlitTelescopeConfigsFields":
        return SlitTelescopeConfigsFields("defaultTelescopeConfigs")

    @classmethod
    def explicit_telescope_configs(cls) -> "SlitTelescopeConfigsFields":
        return SlitTelescopeConfigsFields("explicitTelescopeConfigs")

    @classmethod
    def telluric_type(cls) -> "TelluricTypeFields":
        return TelluricTypeFields("telluricType")

    def fields(
        self,
        *subfields: Union[
            Igrins2LongSlitGraphQLField,
            "ExposureTimeModeFields",
            "Igrins2SvcConfigFields",
            "SlitTelescopeConfigsFields",
            "TelluricTypeFields",
        ],
    ) -> "Igrins2LongSlitFields":
        """Subfields should come from the Igrins2LongSlitFields class"""
        self._subfields.extend(subfields)
        return self

    def alias(self, alias: str) -> "Igrins2LongSlitFields":
        self._alias = alias
        return self


class Igrins2StaticFields(GraphQLField):
    save_svc_images: "Igrins2StaticGraphQLField" = Igrins2StaticGraphQLField(
        "saveSVCImages"
    )
    offset_mode: "Igrins2StaticGraphQLField" = Igrins2StaticGraphQLField("offsetMode")

    def fields(self, *subfields: Igrins2StaticGraphQLField) -> "Igrins2StaticFields":
        """Subfields should come from the Igrins2StaticFields class"""
        self._subfields.extend(subfields)
        return self

    def alias(self, alias: str) -> "Igrins2StaticFields":
        self._alias = alias
        return self


class Igrins2StepFields(GraphQLField):
    @classmethod
    def instrument_config(cls) -> "Igrins2DynamicFields":
        return Igrins2DynamicFields("instrumentConfig")

    id: "Igrins2StepGraphQLField" = Igrins2StepGraphQLField("id")
    breakpoint: "Igrins2StepGraphQLField" = Igrins2StepGraphQLField("breakpoint")

    @classmethod
    def step_config(cls) -> "StepConfigInterface":
        return StepConfigInterface("stepConfig")

    @classmethod
    def telescope_config(cls) -> "TelescopeConfigFields":
        return TelescopeConfigFields("telescopeConfig")

    @classmethod
    def estimate(cls) -> "StepEstimateFields":
        return StepEstimateFields("estimate")

    observe_class: "Igrins2StepGraphQLField" = Igrins2StepGraphQLField("observeClass")

    def fields(
        self,
        *subfields: Union[
            Igrins2StepGraphQLField,
            "Igrins2DynamicFields",
            "StepConfigInterface",
            "StepEstimateFields",
            "TelescopeConfigFields",
        ],
    ) -> "Igrins2StepFields":
        """Subfields should come from the Igrins2StepFields class"""
        self._subfields.extend(subfields)
        return self

    def alias(self, alias: str) -> "Igrins2StepFields":
        self._alias = alias
        return self


class Igrins2SvcConfigFields(GraphQLField):
    @classmethod
    def exposure(cls) -> "TimeSpanFields":
        return TimeSpanFields("exposure")

    @classmethod
    def default_exposure(cls) -> "TimeSpanFields":
        return TimeSpanFields("defaultExposure")

    @classmethod
    def explicit_exposure(cls) -> "TimeSpanFields":
        return TimeSpanFields("explicitExposure")

    @classmethod
    def telescope_configs(cls) -> "TelescopeConfigFields":
        return TelescopeConfigFields("telescopeConfigs")

    @classmethod
    def default_telescope_configs(cls) -> "TelescopeConfigFields":
        return TelescopeConfigFields("defaultTelescopeConfigs")

    @classmethod
    def explicit_telescope_configs(cls) -> "TelescopeConfigFields":
        return TelescopeConfigFields("explicitTelescopeConfigs")

    def fields(
        self,
        *subfields: Union[
            Igrins2SvcConfigGraphQLField, "TelescopeConfigFields", "TimeSpanFields"
        ],
    ) -> "Igrins2SvcConfigFields":
        """Subfields should come from the Igrins2SvcConfigFields class"""
        self._subfields.extend(subfields)
        return self

    def alias(self, alias: str) -> "Igrins2SvcConfigFields":
        self._alias = alias
        return self


class ImagingConfigOptionFields(GraphQLField):
    instrument: "ImagingConfigOptionGraphQLField" = ImagingConfigOptionGraphQLField(
        "instrument"
    )
    filter_label: "ImagingConfigOptionGraphQLField" = ImagingConfigOptionGraphQLField(
        "filterLabel"
    )
    adaptive_optics: "ImagingConfigOptionGraphQLField" = (
        ImagingConfigOptionGraphQLField("adaptiveOptics")
    )
    capability: "ImagingConfigOptionGraphQLField" = ImagingConfigOptionGraphQLField(
        "capability"
    )
    site: "ImagingConfigOptionGraphQLField" = ImagingConfigOptionGraphQLField("site")

    @classmethod
    def fov(cls) -> "AngleFields":
        return AngleFields("fov")

    @classmethod
    def gmos_north(cls) -> "ImagingConfigOptionGmosNorthFields":
        return ImagingConfigOptionGmosNorthFields("gmosNorth")

    @classmethod
    def gmos_south(cls) -> "ImagingConfigOptionGmosSouthFields":
        return ImagingConfigOptionGmosSouthFields("gmosSouth")

    @classmethod
    def flamingos_2(cls) -> "ImagingConfigOptionFlamingos2Fields":
        return ImagingConfigOptionFlamingos2Fields("flamingos2")

    @classmethod
    def gnirs(cls) -> "ImagingConfigOptionGnirsFields":
        return ImagingConfigOptionGnirsFields("gnirs")

    def fields(
        self,
        *subfields: Union[
            ImagingConfigOptionGraphQLField,
            "AngleFields",
            "ImagingConfigOptionFlamingos2Fields",
            "ImagingConfigOptionGmosNorthFields",
            "ImagingConfigOptionGmosSouthFields",
            "ImagingConfigOptionGnirsFields",
        ],
    ) -> "ImagingConfigOptionFields":
        """Subfields should come from the ImagingConfigOptionFields class"""
        self._subfields.extend(subfields)
        return self

    def alias(self, alias: str) -> "ImagingConfigOptionFields":
        self._alias = alias
        return self


class ImagingConfigOptionFlamingos2Fields(GraphQLField):
    filter_: "ImagingConfigOptionFlamingos2GraphQLField" = (
        ImagingConfigOptionFlamingos2GraphQLField("filter")
    )

    def fields(
        self, *subfields: ImagingConfigOptionFlamingos2GraphQLField
    ) -> "ImagingConfigOptionFlamingos2Fields":
        """Subfields should come from the ImagingConfigOptionFlamingos2Fields class"""
        self._subfields.extend(subfields)
        return self

    def alias(self, alias: str) -> "ImagingConfigOptionFlamingos2Fields":
        self._alias = alias
        return self


class ImagingConfigOptionGmosNorthFields(GraphQLField):
    filter_: "ImagingConfigOptionGmosNorthGraphQLField" = (
        ImagingConfigOptionGmosNorthGraphQLField("filter")
    )

    def fields(
        self, *subfields: ImagingConfigOptionGmosNorthGraphQLField
    ) -> "ImagingConfigOptionGmosNorthFields":
        """Subfields should come from the ImagingConfigOptionGmosNorthFields class"""
        self._subfields.extend(subfields)
        return self

    def alias(self, alias: str) -> "ImagingConfigOptionGmosNorthFields":
        self._alias = alias
        return self


class ImagingConfigOptionGmosSouthFields(GraphQLField):
    filter_: "ImagingConfigOptionGmosSouthGraphQLField" = (
        ImagingConfigOptionGmosSouthGraphQLField("filter")
    )

    def fields(
        self, *subfields: ImagingConfigOptionGmosSouthGraphQLField
    ) -> "ImagingConfigOptionGmosSouthFields":
        """Subfields should come from the ImagingConfigOptionGmosSouthFields class"""
        self._subfields.extend(subfields)
        return self

    def alias(self, alias: str) -> "ImagingConfigOptionGmosSouthFields":
        self._alias = alias
        return self


class ImagingConfigOptionGnirsFields(GraphQLField):
    filter_: "ImagingConfigOptionGnirsGraphQLField" = (
        ImagingConfigOptionGnirsGraphQLField("filter")
    )
    camera: "ImagingConfigOptionGnirsGraphQLField" = (
        ImagingConfigOptionGnirsGraphQLField("camera")
    )

    def fields(
        self, *subfields: ImagingConfigOptionGnirsGraphQLField
    ) -> "ImagingConfigOptionGnirsFields":
        """Subfields should come from the ImagingConfigOptionGnirsFields class"""
        self._subfields.extend(subfields)
        return self

    def alias(self, alias: str) -> "ImagingConfigOptionGnirsFields":
        self._alias = alias
        return self


class ImagingScienceRequirementsFields(GraphQLField):
    @classmethod
    def minimum_fov(cls) -> "AngleFields":
        return AngleFields("minimumFov")

    narrow_filters: "ImagingScienceRequirementsGraphQLField" = (
        ImagingScienceRequirementsGraphQLField("narrowFilters")
    )
    broad_filters: "ImagingScienceRequirementsGraphQLField" = (
        ImagingScienceRequirementsGraphQLField("broadFilters")
    )
    combined_filters: "ImagingScienceRequirementsGraphQLField" = (
        ImagingScienceRequirementsGraphQLField("combinedFilters")
    )

    def fields(
        self, *subfields: Union[ImagingScienceRequirementsGraphQLField, "AngleFields"]
    ) -> "ImagingScienceRequirementsFields":
        """Subfields should come from the ImagingScienceRequirementsFields class"""
        self._subfields.extend(subfields)
        return self

    def alias(self, alias: str) -> "ImagingScienceRequirementsFields":
        self._alias = alias
        return self


class ImagingVariantFields(GraphQLField):
    variant_type: "ImagingVariantGraphQLField" = ImagingVariantGraphQLField(
        "variantType"
    )

    @classmethod
    def grouped(cls) -> "GroupedImagingVariantFields":
        return GroupedImagingVariantFields("grouped")

    @classmethod
    def interleaved(cls) -> "InterleavedImagingVariantFields":
        return InterleavedImagingVariantFields("interleaved")

    @classmethod
    def pre_imaging(cls) -> "PreImagingVariantFields":
        return PreImagingVariantFields("preImaging")

    def fields(
        self,
        *subfields: Union[
            ImagingVariantGraphQLField,
            "GroupedImagingVariantFields",
            "InterleavedImagingVariantFields",
            "PreImagingVariantFields",
        ],
    ) -> "ImagingVariantFields":
        """Subfields should come from the ImagingVariantFields class"""
        self._subfields.extend(subfields)
        return self

    def alias(self, alias: str) -> "ImagingVariantFields":
        self._alias = alias
        return self


class InterleavedImagingVariantFields(GraphQLField):
    @classmethod
    def offsets(cls) -> "TelescopeConfigGeneratorFields":
        return TelescopeConfigGeneratorFields("offsets")

    sky_count: "InterleavedImagingVariantGraphQLField" = (
        InterleavedImagingVariantGraphQLField("skyCount")
    )

    @classmethod
    def sky_offsets(cls) -> "TelescopeConfigGeneratorFields":
        return TelescopeConfigGeneratorFields("skyOffsets")

    def fields(
        self,
        *subfields: Union[
            InterleavedImagingVariantGraphQLField, "TelescopeConfigGeneratorFields"
        ],
    ) -> "InterleavedImagingVariantFields":
        """Subfields should come from the InterleavedImagingVariantFields class"""
        self._subfields.extend(subfields)
        return self

    def alias(self, alias: str) -> "InterleavedImagingVariantFields":
        self._alias = alias
        return self


class ItcInterface(GraphQLField):
    itc_type: "ItcGraphQLField" = ItcGraphQLField("itcType")

    def fields(self, *subfields: ItcGraphQLField) -> "ItcInterface":
        """Subfields should come from the ItcInterface class"""
        self._subfields.extend(subfields)
        return self

    def alias(self, alias: str) -> "ItcInterface":
        self._alias = alias
        return self

    def on(self, type_name: str, *subfields: GraphQLField) -> "ItcInterface":
        self._inline_fragments[type_name] = subfields
        return self


class ItcFlamingos2ImagingFields(GraphQLField):
    itc_type: "ItcFlamingos2ImagingGraphQLField" = ItcFlamingos2ImagingGraphQLField(
        "itcType"
    )

    @classmethod
    def flamingos_2_imaging_science(cls) -> "ItcFlamingos2ImagingResultSetFields":
        return ItcFlamingos2ImagingResultSetFields("flamingos2ImagingScience")

    def fields(
        self,
        *subfields: Union[
            ItcFlamingos2ImagingGraphQLField, "ItcFlamingos2ImagingResultSetFields"
        ],
    ) -> "ItcFlamingos2ImagingFields":
        """Subfields should come from the ItcFlamingos2ImagingFields class"""
        self._subfields.extend(subfields)
        return self

    def alias(self, alias: str) -> "ItcFlamingos2ImagingFields":
        self._alias = alias
        return self


class ItcFlamingos2ImagingResultSetFields(GraphQLField):
    filter_: "ItcFlamingos2ImagingResultSetGraphQLField" = (
        ItcFlamingos2ImagingResultSetGraphQLField("filter")
    )

    @classmethod
    def results(cls) -> "ItcResultSetFields":
        return ItcResultSetFields("results")

    def fields(
        self,
        *subfields: Union[
            ItcFlamingos2ImagingResultSetGraphQLField, "ItcResultSetFields"
        ],
    ) -> "ItcFlamingos2ImagingResultSetFields":
        """Subfields should come from the ItcFlamingos2ImagingResultSetFields class"""
        self._subfields.extend(subfields)
        return self

    def alias(self, alias: str) -> "ItcFlamingos2ImagingResultSetFields":
        self._alias = alias
        return self


class ItcGhostIfuFields(GraphQLField):
    itc_type: "ItcGhostIfuGraphQLField" = ItcGhostIfuGraphQLField("itcType")

    @classmethod
    def red(cls) -> "ItcResultSetFields":
        return ItcResultSetFields("red")

    @classmethod
    def blue(cls) -> "ItcResultSetFields":
        return ItcResultSetFields("blue")

    def fields(
        self, *subfields: Union[ItcGhostIfuGraphQLField, "ItcResultSetFields"]
    ) -> "ItcGhostIfuFields":
        """Subfields should come from the ItcGhostIfuFields class"""
        self._subfields.extend(subfields)
        return self

    def alias(self, alias: str) -> "ItcGhostIfuFields":
        self._alias = alias
        return self


class ItcGmosNorthImagingFields(GraphQLField):
    itc_type: "ItcGmosNorthImagingGraphQLField" = ItcGmosNorthImagingGraphQLField(
        "itcType"
    )

    @classmethod
    def gmos_north_imaging_science(cls) -> "ItcGmosNorthImagingResultSetFields":
        return ItcGmosNorthImagingResultSetFields("gmosNorthImagingScience")

    def fields(
        self,
        *subfields: Union[
            ItcGmosNorthImagingGraphQLField, "ItcGmosNorthImagingResultSetFields"
        ],
    ) -> "ItcGmosNorthImagingFields":
        """Subfields should come from the ItcGmosNorthImagingFields class"""
        self._subfields.extend(subfields)
        return self

    def alias(self, alias: str) -> "ItcGmosNorthImagingFields":
        self._alias = alias
        return self


class ItcGmosNorthImagingResultSetFields(GraphQLField):
    filter_: "ItcGmosNorthImagingResultSetGraphQLField" = (
        ItcGmosNorthImagingResultSetGraphQLField("filter")
    )

    @classmethod
    def results(cls) -> "ItcResultSetFields":
        return ItcResultSetFields("results")

    def fields(
        self,
        *subfields: Union[
            ItcGmosNorthImagingResultSetGraphQLField, "ItcResultSetFields"
        ],
    ) -> "ItcGmosNorthImagingResultSetFields":
        """Subfields should come from the ItcGmosNorthImagingResultSetFields class"""
        self._subfields.extend(subfields)
        return self

    def alias(self, alias: str) -> "ItcGmosNorthImagingResultSetFields":
        self._alias = alias
        return self


class ItcGmosSouthImagingFields(GraphQLField):
    itc_type: "ItcGmosSouthImagingGraphQLField" = ItcGmosSouthImagingGraphQLField(
        "itcType"
    )

    @classmethod
    def gmos_south_imaging_science(cls) -> "ItcGmosSouthImagingResultSetFields":
        return ItcGmosSouthImagingResultSetFields("gmosSouthImagingScience")

    def fields(
        self,
        *subfields: Union[
            ItcGmosSouthImagingGraphQLField, "ItcGmosSouthImagingResultSetFields"
        ],
    ) -> "ItcGmosSouthImagingFields":
        """Subfields should come from the ItcGmosSouthImagingFields class"""
        self._subfields.extend(subfields)
        return self

    def alias(self, alias: str) -> "ItcGmosSouthImagingFields":
        self._alias = alias
        return self


class ItcGmosSouthImagingResultSetFields(GraphQLField):
    filter_: "ItcGmosSouthImagingResultSetGraphQLField" = (
        ItcGmosSouthImagingResultSetGraphQLField("filter")
    )

    @classmethod
    def results(cls) -> "ItcResultSetFields":
        return ItcResultSetFields("results")

    def fields(
        self,
        *subfields: Union[
            ItcGmosSouthImagingResultSetGraphQLField, "ItcResultSetFields"
        ],
    ) -> "ItcGmosSouthImagingResultSetFields":
        """Subfields should come from the ItcGmosSouthImagingResultSetFields class"""
        self._subfields.extend(subfields)
        return self

    def alias(self, alias: str) -> "ItcGmosSouthImagingResultSetFields":
        self._alias = alias
        return self


class ItcGnirsImagingFields(GraphQLField):
    itc_type: "ItcGnirsImagingGraphQLField" = ItcGnirsImagingGraphQLField("itcType")

    @classmethod
    def gnirs_imaging_science(cls) -> "ItcGnirsImagingResultSetFields":
        return ItcGnirsImagingResultSetFields("gnirsImagingScience")

    def fields(
        self,
        *subfields: Union[
            ItcGnirsImagingGraphQLField, "ItcGnirsImagingResultSetFields"
        ],
    ) -> "ItcGnirsImagingFields":
        """Subfields should come from the ItcGnirsImagingFields class"""
        self._subfields.extend(subfields)
        return self

    def alias(self, alias: str) -> "ItcGnirsImagingFields":
        self._alias = alias
        return self


class ItcGnirsImagingResultSetFields(GraphQLField):
    filter_: "ItcGnirsImagingResultSetGraphQLField" = (
        ItcGnirsImagingResultSetGraphQLField("filter")
    )

    @classmethod
    def results(cls) -> "ItcResultSetFields":
        return ItcResultSetFields("results")

    def fields(
        self,
        *subfields: Union[ItcGnirsImagingResultSetGraphQLField, "ItcResultSetFields"],
    ) -> "ItcGnirsImagingResultSetFields":
        """Subfields should come from the ItcGnirsImagingResultSetFields class"""
        self._subfields.extend(subfields)
        return self

    def alias(self, alias: str) -> "ItcGnirsImagingResultSetFields":
        self._alias = alias
        return self


class ItcGnirsSpectroscopyFields(GraphQLField):
    itc_type: "ItcGnirsSpectroscopyGraphQLField" = ItcGnirsSpectroscopyGraphQLField(
        "itcType"
    )

    @classmethod
    def acquisition(cls) -> "ItcResultSetFields":
        return ItcResultSetFields("acquisition")

    @classmethod
    def gnirs_spectroscopy_science(cls) -> "ItcGnirsSpectroscopyResultSetFields":
        return ItcGnirsSpectroscopyResultSetFields("gnirsSpectroscopyScience")

    def fields(
        self,
        *subfields: Union[
            ItcGnirsSpectroscopyGraphQLField,
            "ItcGnirsSpectroscopyResultSetFields",
            "ItcResultSetFields",
        ],
    ) -> "ItcGnirsSpectroscopyFields":
        """Subfields should come from the ItcGnirsSpectroscopyFields class"""
        self._subfields.extend(subfields)
        return self

    def alias(self, alias: str) -> "ItcGnirsSpectroscopyFields":
        self._alias = alias
        return self


class ItcGnirsSpectroscopyResultSetFields(GraphQLField):
    @classmethod
    def central_wavelength(cls) -> "WavelengthFields":
        return WavelengthFields("centralWavelength")

    @classmethod
    def results(cls) -> "ItcResultSetFields":
        return ItcResultSetFields("results")

    def fields(
        self,
        *subfields: Union[
            ItcGnirsSpectroscopyResultSetGraphQLField,
            "ItcResultSetFields",
            "WavelengthFields",
        ],
    ) -> "ItcGnirsSpectroscopyResultSetFields":
        """Subfields should come from the ItcGnirsSpectroscopyResultSetFields class"""
        self._subfields.extend(subfields)
        return self

    def alias(self, alias: str) -> "ItcGnirsSpectroscopyResultSetFields":
        self._alias = alias
        return self


class ItcIgrins2SpectroscopyFields(GraphQLField):
    itc_type: "ItcIgrins2SpectroscopyGraphQLField" = ItcIgrins2SpectroscopyGraphQLField(
        "itcType"
    )

    @classmethod
    def spectroscopy_science(cls) -> "ItcResultSetFields":
        return ItcResultSetFields("spectroscopyScience")

    def fields(
        self,
        *subfields: Union[ItcIgrins2SpectroscopyGraphQLField, "ItcResultSetFields"],
    ) -> "ItcIgrins2SpectroscopyFields":
        """Subfields should come from the ItcIgrins2SpectroscopyFields class"""
        self._subfields.extend(subfields)
        return self

    def alias(self, alias: str) -> "ItcIgrins2SpectroscopyFields":
        self._alias = alias
        return self


class ItcResultFields(GraphQLField):
    target_id: "ItcResultGraphQLField" = ItcResultGraphQLField("targetId")

    @classmethod
    def exposure_time(cls) -> "TimeSpanFields":
        return TimeSpanFields("exposureTime")

    exposure_count: "ItcResultGraphQLField" = ItcResultGraphQLField("exposureCount")

    @classmethod
    def signal_to_noise_at(cls) -> "SignalToNoiseAtFields":
        return SignalToNoiseAtFields("signalToNoiseAt")

    def fields(
        self,
        *subfields: Union[
            ItcResultGraphQLField, "SignalToNoiseAtFields", "TimeSpanFields"
        ],
    ) -> "ItcResultFields":
        """Subfields should come from the ItcResultFields class"""
        self._subfields.extend(subfields)
        return self

    def alias(self, alias: str) -> "ItcResultFields":
        self._alias = alias
        return self


class ItcResultSetFields(GraphQLField):
    @classmethod
    def selected(cls) -> "ItcResultFields":
        return ItcResultFields("selected")

    @classmethod
    def all(cls) -> "ItcResultFields":
        return ItcResultFields("all")

    index: "ItcResultSetGraphQLField" = ItcResultSetGraphQLField("index")

    def fields(
        self, *subfields: Union[ItcResultSetGraphQLField, "ItcResultFields"]
    ) -> "ItcResultSetFields":
        """Subfields should come from the ItcResultSetFields class"""
        self._subfields.extend(subfields)
        return self

    def alias(self, alias: str) -> "ItcResultSetFields":
        self._alias = alias
        return self


class ItcSpectroscopyFields(GraphQLField):
    itc_type: "ItcSpectroscopyGraphQLField" = ItcSpectroscopyGraphQLField("itcType")

    @classmethod
    def acquisition(cls) -> "ItcResultSetFields":
        return ItcResultSetFields("acquisition")

    @classmethod
    def spectroscopy_science(cls) -> "ItcResultSetFields":
        return ItcResultSetFields("spectroscopyScience")

    def fields(
        self, *subfields: Union[ItcSpectroscopyGraphQLField, "ItcResultSetFields"]
    ) -> "ItcSpectroscopyFields":
        """Subfields should come from the ItcSpectroscopyFields class"""
        self._subfields.extend(subfields)
        return self

    def alias(self, alias: str) -> "ItcSpectroscopyFields":
        self._alias = alias
        return self


class KeckCallPropertiesFields(GraphQLField):
    instruments: "KeckCallPropertiesGraphQLField" = KeckCallPropertiesGraphQLField(
        "instruments"
    )

    @classmethod
    def coordinate_limits(cls) -> "CoordinateLimitsFields":
        return CoordinateLimitsFields("coordinateLimits")

    def fields(
        self,
        *subfields: Union[KeckCallPropertiesGraphQLField, "CoordinateLimitsFields"],
    ) -> "KeckCallPropertiesFields":
        """Subfields should come from the KeckCallPropertiesFields class"""
        self._subfields.extend(subfields)
        return self

    def alias(self, alias: str) -> "KeckCallPropertiesFields":
        self._alias = alias
        return self


class KeckProgramReferenceFields(GraphQLField):
    label: "KeckProgramReferenceGraphQLField" = KeckProgramReferenceGraphQLField(
        "label"
    )
    type_: "KeckProgramReferenceGraphQLField" = KeckProgramReferenceGraphQLField("type")
    semester: "KeckProgramReferenceGraphQLField" = KeckProgramReferenceGraphQLField(
        "semester"
    )
    semester_index: "KeckProgramReferenceGraphQLField" = (
        KeckProgramReferenceGraphQLField("semesterIndex")
    )

    def fields(
        self, *subfields: KeckProgramReferenceGraphQLField
    ) -> "KeckProgramReferenceFields":
        """Subfields should come from the KeckProgramReferenceFields class"""
        self._subfields.extend(subfields)
        return self

    def alias(self, alias: str) -> "KeckProgramReferenceFields":
        self._alias = alias
        return self


class KeckProposalTypeFields(GraphQLField):
    min_percent_time: "KeckProposalTypeGraphQLField" = KeckProposalTypeGraphQLField(
        "minPercentTime"
    )

    @classmethod
    def partner_splits(cls) -> "PartnerSplitFields":
        return PartnerSplitFields("partnerSplits")

    def fields(
        self, *subfields: Union[KeckProposalTypeGraphQLField, "PartnerSplitFields"]
    ) -> "KeckProposalTypeFields":
        """Subfields should come from the KeckProposalTypeFields class"""
        self._subfields.extend(subfields)
        return self

    def alias(self, alias: str) -> "KeckProposalTypeFields":
        self._alias = alias
        return self


class LargeProgramFields(GraphQLField):
    science_subtype: "LargeProgramGraphQLField" = LargeProgramGraphQLField(
        "scienceSubtype"
    )
    too_activation_ceiling: "LargeProgramGraphQLField" = LargeProgramGraphQLField(
        "tooActivationCeiling"
    )
    default_too_activation_ceiling: "LargeProgramGraphQLField" = (
        LargeProgramGraphQLField("defaultTooActivationCeiling")
    )
    explicit_too_activation_ceiling: "LargeProgramGraphQLField" = (
        LargeProgramGraphQLField("explicitTooActivationCeiling")
    )
    min_percent_time: "LargeProgramGraphQLField" = LargeProgramGraphQLField(
        "minPercentTime"
    )
    min_percent_total_time: "LargeProgramGraphQLField" = LargeProgramGraphQLField(
        "minPercentTotalTime"
    )

    @classmethod
    def total_time(cls) -> "TimeSpanFields":
        return TimeSpanFields("totalTime")

    aeon_multi_facility: "LargeProgramGraphQLField" = LargeProgramGraphQLField(
        "aeonMultiFacility"
    )
    jwst_synergy: "LargeProgramGraphQLField" = LargeProgramGraphQLField("jwstSynergy")

    def fields(
        self, *subfields: Union[LargeProgramGraphQLField, "TimeSpanFields"]
    ) -> "LargeProgramFields":
        """Subfields should come from the LargeProgramFields class"""
        self._subfields.extend(subfields)
        return self

    def alias(self, alias: str) -> "LargeProgramFields":
        self._alias = alias
        return self


class LibraryProgramReferenceFields(GraphQLField):
    label: "LibraryProgramReferenceGraphQLField" = LibraryProgramReferenceGraphQLField(
        "label"
    )
    type_: "LibraryProgramReferenceGraphQLField" = LibraryProgramReferenceGraphQLField(
        "type"
    )
    description: "LibraryProgramReferenceGraphQLField" = (
        LibraryProgramReferenceGraphQLField("description")
    )
    instrument: "LibraryProgramReferenceGraphQLField" = (
        LibraryProgramReferenceGraphQLField("instrument")
    )

    def fields(
        self, *subfields: LibraryProgramReferenceGraphQLField
    ) -> "LibraryProgramReferenceFields":
        """Subfields should come from the LibraryProgramReferenceFields class"""
        self._subfields.extend(subfields)
        return self

    def alias(self, alias: str) -> "LibraryProgramReferenceFields":
        self._alias = alias
        return self


class LineFluxIntegratedFields(GraphQLField):
    value: "LineFluxIntegratedGraphQLField" = LineFluxIntegratedGraphQLField("value")
    units: "LineFluxIntegratedGraphQLField" = LineFluxIntegratedGraphQLField("units")

    def fields(
        self, *subfields: LineFluxIntegratedGraphQLField
    ) -> "LineFluxIntegratedFields":
        """Subfields should come from the LineFluxIntegratedFields class"""
        self._subfields.extend(subfields)
        return self

    def alias(self, alias: str) -> "LineFluxIntegratedFields":
        self._alias = alias
        return self


class LineFluxSurfaceFields(GraphQLField):
    value: "LineFluxSurfaceGraphQLField" = LineFluxSurfaceGraphQLField("value")
    units: "LineFluxSurfaceGraphQLField" = LineFluxSurfaceGraphQLField("units")

    def fields(
        self, *subfields: LineFluxSurfaceGraphQLField
    ) -> "LineFluxSurfaceFields":
        """Subfields should come from the LineFluxSurfaceFields class"""
        self._subfields.extend(subfields)
        return self

    def alias(self, alias: str) -> "LineFluxSurfaceFields":
        self._alias = alias
        return self


class LinkUserResultFields(GraphQLField):
    @classmethod
    def user(cls) -> "ProgramUserFields":
        return ProgramUserFields("user")

    def fields(
        self, *subfields: Union[LinkUserResultGraphQLField, "ProgramUserFields"]
    ) -> "LinkUserResultFields":
        """Subfields should come from the LinkUserResultFields class"""
        self._subfields.extend(subfields)
        return self

    def alias(self, alias: str) -> "LinkUserResultFields":
        self._alias = alias
        return self


class MonitoringProgramReferenceFields(GraphQLField):
    label: "MonitoringProgramReferenceGraphQLField" = (
        MonitoringProgramReferenceGraphQLField("label")
    )
    type_: "MonitoringProgramReferenceGraphQLField" = (
        MonitoringProgramReferenceGraphQLField("type")
    )
    instrument: "MonitoringProgramReferenceGraphQLField" = (
        MonitoringProgramReferenceGraphQLField("instrument")
    )
    semester: "MonitoringProgramReferenceGraphQLField" = (
        MonitoringProgramReferenceGraphQLField("semester")
    )
    semester_index: "MonitoringProgramReferenceGraphQLField" = (
        MonitoringProgramReferenceGraphQLField("semesterIndex")
    )

    def fields(
        self, *subfields: MonitoringProgramReferenceGraphQLField
    ) -> "MonitoringProgramReferenceFields":
        """Subfields should come from the MonitoringProgramReferenceFields class"""
        self._subfields.extend(subfields)
        return self

    def alias(self, alias: str) -> "MonitoringProgramReferenceFields":
        self._alias = alias
        return self


class NonsiderealFields(GraphQLField):
    des: "NonsiderealGraphQLField" = NonsiderealGraphQLField("des")
    key_type: "NonsiderealGraphQLField" = NonsiderealGraphQLField("keyType")
    key: "NonsiderealGraphQLField" = NonsiderealGraphQLField("key")

    def fields(self, *subfields: NonsiderealGraphQLField) -> "NonsiderealFields":
        """Subfields should come from the NonsiderealFields class"""
        self._subfields.extend(subfields)
        return self

    def alias(self, alias: str) -> "NonsiderealFields":
        self._alias = alias
        return self


class ObservationFields(GraphQLField):
    id: "ObservationGraphQLField" = ObservationGraphQLField("id")
    existence: "ObservationGraphQLField" = ObservationGraphQLField("existence")

    @classmethod
    def reference(cls) -> "ObservationReferenceFields":
        return ObservationReferenceFields("reference")

    index: "ObservationGraphQLField" = ObservationGraphQLField("index")
    title: "ObservationGraphQLField" = ObservationGraphQLField("title")
    subtitle: "ObservationGraphQLField" = ObservationGraphQLField("subtitle")
    science_band: "ObservationGraphQLField" = ObservationGraphQLField("scienceBand")
    observation_time: "ObservationGraphQLField" = ObservationGraphQLField(
        "observationTime"
    )

    @classmethod
    def observation_duration(cls) -> "TimeSpanFields":
        return TimeSpanFields("observationDuration")

    @classmethod
    def pos_angle_constraint(cls) -> "PosAngleConstraintFields":
        return PosAngleConstraintFields("posAngleConstraint")

    @classmethod
    def program(cls) -> "ProgramFields":
        return ProgramFields("program")

    @classmethod
    def target_environment(cls) -> "TargetEnvironmentFields":
        return TargetEnvironmentFields("targetEnvironment")

    @classmethod
    def constraint_set(cls) -> "ConstraintSetFields":
        return ConstraintSetFields("constraintSet")

    @classmethod
    def timing_windows(cls) -> "TimingWindowFields":
        return TimingWindowFields("timingWindows")

    @classmethod
    def scheduling_constraints(cls) -> "SchedulingConstraintsFields":
        return SchedulingConstraintsFields("schedulingConstraints")

    @classmethod
    def attachments(cls) -> "AttachmentFields":
        return AttachmentFields("attachments")

    @classmethod
    def science_requirements(cls) -> "ScienceRequirementsFields":
        return ScienceRequirementsFields("scienceRequirements")

    @classmethod
    def observing_mode(cls) -> "ObservingModeFields":
        return ObservingModeFields("observingMode")

    instrument: "ObservationGraphQLField" = ObservationGraphQLField("instrument")

    @classmethod
    def execution(cls) -> "ExecutionFields":
        return ExecutionFields("execution")

    @classmethod
    def itc(cls) -> "ItcInterface":
        return ItcInterface("itc")

    group_id: "ObservationGraphQLField" = ObservationGraphQLField("groupId")
    group_index: "ObservationGraphQLField" = ObservationGraphQLField("groupIndex")
    calibration_role: "ObservationGraphQLField" = ObservationGraphQLField(
        "calibrationRole"
    )
    observer_notes: "ObservationGraphQLField" = ObservationGraphQLField("observerNotes")

    @classmethod
    def configuration(cls) -> "ConfigurationFields":
        return ConfigurationFields("configuration")

    @classmethod
    def configuration_requests(cls) -> "ConfigurationRequestFields":
        return ConfigurationRequestFields("configurationRequests")

    @classmethod
    def workflow(cls) -> "CalculatedObservationWorkflowFields":
        return CalculatedObservationWorkflowFields("workflow")

    @classmethod
    def archive_duplication(cls) -> "ArchiveDuplicationFields":
        return ArchiveDuplicationFields("archiveDuplication")

    def fields(
        self,
        *subfields: Union[
            ObservationGraphQLField,
            "ArchiveDuplicationFields",
            "AttachmentFields",
            "CalculatedObservationWorkflowFields",
            "ConfigurationFields",
            "ConfigurationRequestFields",
            "ConstraintSetFields",
            "ExecutionFields",
            "ItcInterface",
            "ObservationReferenceFields",
            "ObservingModeFields",
            "PosAngleConstraintFields",
            "ProgramFields",
            "SchedulingConstraintsFields",
            "ScienceRequirementsFields",
            "TargetEnvironmentFields",
            "TimeSpanFields",
            "TimingWindowFields",
        ],
    ) -> "ObservationFields":
        """Subfields should come from the ObservationFields class"""
        self._subfields.extend(subfields)
        return self

    def alias(self, alias: str) -> "ObservationFields":
        self._alias = alias
        return self


class ObservationReferenceFields(GraphQLField):
    label: "ObservationReferenceGraphQLField" = ObservationReferenceGraphQLField(
        "label"
    )

    @classmethod
    def program(cls) -> "ProgramReferenceInterface":
        return ProgramReferenceInterface("program")

    index: "ObservationReferenceGraphQLField" = ObservationReferenceGraphQLField(
        "index"
    )

    def fields(
        self,
        *subfields: Union[
            ObservationReferenceGraphQLField, "ProgramReferenceInterface"
        ],
    ) -> "ObservationReferenceFields":
        """Subfields should come from the ObservationReferenceFields class"""
        self._subfields.extend(subfields)
        return self

    def alias(self, alias: str) -> "ObservationReferenceFields":
        self._alias = alias
        return self


class ObservationSelectResultFields(GraphQLField):
    @classmethod
    def matches(cls) -> "ObservationFields":
        return ObservationFields("matches")

    has_more: "ObservationSelectResultGraphQLField" = (
        ObservationSelectResultGraphQLField("hasMore")
    )

    def fields(
        self,
        *subfields: Union[ObservationSelectResultGraphQLField, "ObservationFields"],
    ) -> "ObservationSelectResultFields":
        """Subfields should come from the ObservationSelectResultFields class"""
        self._subfields.extend(subfields)
        return self

    def alias(self, alias: str) -> "ObservationSelectResultFields":
        self._alias = alias
        return self


class ObservationTimeEstimateFields(GraphQLField):
    @classmethod
    def setup(cls) -> "SetupTimeFields":
        return SetupTimeFields("setup")

    setup_count: "ObservationTimeEstimateGraphQLField" = (
        ObservationTimeEstimateGraphQLField("setupCount")
    )

    @classmethod
    def science(cls) -> "CategorizedTimeFields":
        return CategorizedTimeFields("science")

    @classmethod
    def total(cls) -> "CategorizedTimeFields":
        return CategorizedTimeFields("total")

    def fields(
        self,
        *subfields: Union[
            ObservationTimeEstimateGraphQLField,
            "CategorizedTimeFields",
            "SetupTimeFields",
        ],
    ) -> "ObservationTimeEstimateFields":
        """Subfields should come from the ObservationTimeEstimateFields class"""
        self._subfields.extend(subfields)
        return self

    def alias(self, alias: str) -> "ObservationTimeEstimateFields":
        self._alias = alias
        return self


class ObservationValidationFields(GraphQLField):
    code: "ObservationValidationGraphQLField" = ObservationValidationGraphQLField(
        "code"
    )
    messages: "ObservationValidationGraphQLField" = ObservationValidationGraphQLField(
        "messages"
    )

    def fields(
        self, *subfields: ObservationValidationGraphQLField
    ) -> "ObservationValidationFields":
        """Subfields should come from the ObservationValidationFields class"""
        self._subfields.extend(subfields)
        return self

    def alias(self, alias: str) -> "ObservationValidationFields":
        self._alias = alias
        return self


class ObservationWorkflowFields(GraphQLField):
    state: "ObservationWorkflowGraphQLField" = ObservationWorkflowGraphQLField("state")
    valid_transitions: "ObservationWorkflowGraphQLField" = (
        ObservationWorkflowGraphQLField("validTransitions")
    )

    @classmethod
    def validation_errors(cls) -> "ObservationValidationFields":
        return ObservationValidationFields("validationErrors")

    def fields(
        self,
        *subfields: Union[
            ObservationWorkflowGraphQLField, "ObservationValidationFields"
        ],
    ) -> "ObservationWorkflowFields":
        """Subfields should come from the ObservationWorkflowFields class"""
        self._subfields.extend(subfields)
        return self

    def alias(self, alias: str) -> "ObservationWorkflowFields":
        self._alias = alias
        return self


class ObservingModeFields(GraphQLField):
    instrument: "ObservingModeGraphQLField" = ObservingModeGraphQLField("instrument")
    mode: "ObservingModeGraphQLField" = ObservingModeGraphQLField("mode")

    @classmethod
    def exchange(cls) -> "ExchangeFields":
        return ExchangeFields("exchange")

    @classmethod
    def flamingos_2_imaging(cls) -> "Flamingos2ImagingFields":
        return Flamingos2ImagingFields("flamingos2Imaging")

    @classmethod
    def flamingos_2_long_slit(cls) -> "Flamingos2LongSlitFields":
        return Flamingos2LongSlitFields("flamingos2LongSlit")

    @classmethod
    def ghost_ifu(cls) -> "GhostIfuFields":
        return GhostIfuFields("ghostIfu")

    @classmethod
    def gmos_north_imaging(cls) -> "GmosNorthImagingFields":
        return GmosNorthImagingFields("gmosNorthImaging")

    @classmethod
    def gmos_north_long_slit(cls) -> "GmosNorthLongSlitFields":
        return GmosNorthLongSlitFields("gmosNorthLongSlit")

    @classmethod
    def gmos_north_mos(cls) -> "GmosNorthMosFields":
        return GmosNorthMosFields("gmosNorthMos")

    @classmethod
    def gmos_south_imaging(cls) -> "GmosSouthImagingFields":
        return GmosSouthImagingFields("gmosSouthImaging")

    @classmethod
    def gmos_south_long_slit(cls) -> "GmosSouthLongSlitFields":
        return GmosSouthLongSlitFields("gmosSouthLongSlit")

    @classmethod
    def gmos_south_mos(cls) -> "GmosSouthMosFields":
        return GmosSouthMosFields("gmosSouthMos")

    @classmethod
    def gnirs_imaging(cls) -> "GnirsImagingFields":
        return GnirsImagingFields("gnirsImaging")

    @classmethod
    def gnirs_spectroscopy(cls) -> "GnirsSpectroscopyFields":
        return GnirsSpectroscopyFields("gnirsSpectroscopy")

    @classmethod
    def igrins_2_long_slit(cls) -> "Igrins2LongSlitFields":
        return Igrins2LongSlitFields("igrins2LongSlit")

    @classmethod
    def visitor(cls) -> "VisitorFields":
        return VisitorFields("visitor")

    def fields(
        self,
        *subfields: Union[
            ObservingModeGraphQLField,
            "ExchangeFields",
            "Flamingos2ImagingFields",
            "Flamingos2LongSlitFields",
            "GhostIfuFields",
            "GmosNorthImagingFields",
            "GmosNorthLongSlitFields",
            "GmosNorthMosFields",
            "GmosSouthImagingFields",
            "GmosSouthLongSlitFields",
            "GmosSouthMosFields",
            "GnirsImagingFields",
            "GnirsSpectroscopyFields",
            "Igrins2LongSlitFields",
            "VisitorFields",
        ],
    ) -> "ObservingModeFields":
        """Subfields should come from the ObservingModeFields class"""
        self._subfields.extend(subfields)
        return self

    def alias(self, alias: str) -> "ObservingModeFields":
        self._alias = alias
        return self


class ObservingModeGroupFields(GraphQLField):
    @classmethod
    def observations(
        cls,
        include_deleted: bool,
        *,
        offset: Optional[Any] = None,
        limit: Optional[Any] = None,
    ) -> "ObservationSelectResultFields":
        arguments: dict[str, dict[str, Any]] = {
            "includeDeleted": {"type": "Boolean!", "value": include_deleted},
            "OFFSET": {"type": "ObservationId", "value": offset},
            "LIMIT": {"type": "NonNegInt", "value": limit},
        }
        cleared_arguments = {
            key: value for key, value in arguments.items() if value["value"] is not None
        }
        return ObservationSelectResultFields(
            "observations", arguments=cleared_arguments
        )

    @classmethod
    def observing_mode(cls) -> "ObservingModeFields":
        return ObservingModeFields("observingMode")

    @classmethod
    def program(cls) -> "ProgramFields":
        return ProgramFields("program")

    def fields(
        self,
        *subfields: Union[
            ObservingModeGroupGraphQLField,
            "ObservationSelectResultFields",
            "ObservingModeFields",
            "ProgramFields",
        ],
    ) -> "ObservingModeGroupFields":
        """Subfields should come from the ObservingModeGroupFields class"""
        self._subfields.extend(subfields)
        return self

    def alias(self, alias: str) -> "ObservingModeGroupFields":
        self._alias = alias
        return self


class ObservingModeGroupSelectResultFields(GraphQLField):
    @classmethod
    def matches(cls) -> "ObservingModeGroupFields":
        return ObservingModeGroupFields("matches")

    has_more: "ObservingModeGroupSelectResultGraphQLField" = (
        ObservingModeGroupSelectResultGraphQLField("hasMore")
    )

    def fields(
        self,
        *subfields: Union[
            ObservingModeGroupSelectResultGraphQLField, "ObservingModeGroupFields"
        ],
    ) -> "ObservingModeGroupSelectResultFields":
        """Subfields should come from the ObservingModeGroupSelectResultFields class"""
        self._subfields.extend(subfields)
        return self

    def alias(self, alias: str) -> "ObservingModeGroupSelectResultFields":
        self._alias = alias
        return self


class OffsetFields(GraphQLField):
    @classmethod
    def p(cls) -> "OffsetPFields":
        return OffsetPFields("p")

    @classmethod
    def q(cls) -> "OffsetQFields":
        return OffsetQFields("q")

    def fields(
        self, *subfields: Union[OffsetGraphQLField, "OffsetPFields", "OffsetQFields"]
    ) -> "OffsetFields":
        """Subfields should come from the OffsetFields class"""
        self._subfields.extend(subfields)
        return self

    def alias(self, alias: str) -> "OffsetFields":
        self._alias = alias
        return self


class OffsetPFields(GraphQLField):
    microarcseconds: "OffsetPGraphQLField" = OffsetPGraphQLField("microarcseconds")
    milliarcseconds: "OffsetPGraphQLField" = OffsetPGraphQLField("milliarcseconds")
    arcseconds: "OffsetPGraphQLField" = OffsetPGraphQLField("arcseconds")

    def fields(self, *subfields: OffsetPGraphQLField) -> "OffsetPFields":
        """Subfields should come from the OffsetPFields class"""
        self._subfields.extend(subfields)
        return self

    def alias(self, alias: str) -> "OffsetPFields":
        self._alias = alias
        return self


class OffsetQFields(GraphQLField):
    microarcseconds: "OffsetQGraphQLField" = OffsetQGraphQLField("microarcseconds")
    milliarcseconds: "OffsetQGraphQLField" = OffsetQGraphQLField("milliarcseconds")
    arcseconds: "OffsetQGraphQLField" = OffsetQGraphQLField("arcseconds")

    def fields(self, *subfields: OffsetQGraphQLField) -> "OffsetQFields":
        """Subfields should come from the OffsetQFields class"""
        self._subfields.extend(subfields)
        return self

    def alias(self, alias: str) -> "OffsetQFields":
        self._alias = alias
        return self


class OpportunityFields(GraphQLField):
    @classmethod
    def region(cls) -> "RegionFields":
        return RegionFields("region")

    def fields(
        self, *subfields: Union[OpportunityGraphQLField, "RegionFields"]
    ) -> "OpportunityFields":
        """Subfields should come from the OpportunityFields class"""
        self._subfields.extend(subfields)
        return self

    def alias(self, alias: str) -> "OpportunityFields":
        self._alias = alias
        return self


class ParallaxFields(GraphQLField):
    microarcseconds: "ParallaxGraphQLField" = ParallaxGraphQLField("microarcseconds")
    milliarcseconds: "ParallaxGraphQLField" = ParallaxGraphQLField("milliarcseconds")

    def fields(self, *subfields: ParallaxGraphQLField) -> "ParallaxFields":
        """Subfields should come from the ParallaxFields class"""
        self._subfields.extend(subfields)
        return self

    def alias(self, alias: str) -> "ParallaxFields":
        self._alias = alias
        return self


class PartnerLinkInterface(GraphQLField):
    link_type: "PartnerLinkGraphQLField" = PartnerLinkGraphQLField("linkType")

    def fields(self, *subfields: PartnerLinkGraphQLField) -> "PartnerLinkInterface":
        """Subfields should come from the PartnerLinkInterface class"""
        self._subfields.extend(subfields)
        return self

    def alias(self, alias: str) -> "PartnerLinkInterface":
        self._alias = alias
        return self

    def on(self, type_name: str, *subfields: GraphQLField) -> "PartnerLinkInterface":
        self._inline_fragments[type_name] = subfields
        return self


class PartnerSplitFields(GraphQLField):
    partner: "PartnerSplitGraphQLField" = PartnerSplitGraphQLField("partner")
    percent: "PartnerSplitGraphQLField" = PartnerSplitGraphQLField("percent")

    def fields(self, *subfields: PartnerSplitGraphQLField) -> "PartnerSplitFields":
        """Subfields should come from the PartnerSplitFields class"""
        self._subfields.extend(subfields)
        return self

    def alias(self, alias: str) -> "PartnerSplitFields":
        self._alias = alias
        return self


class PoorWeatherFields(GraphQLField):
    science_subtype: "PoorWeatherGraphQLField" = PoorWeatherGraphQLField(
        "scienceSubtype"
    )

    def fields(self, *subfields: PoorWeatherGraphQLField) -> "PoorWeatherFields":
        """Subfields should come from the PoorWeatherFields class"""
        self._subfields.extend(subfields)
        return self

    def alias(self, alias: str) -> "PoorWeatherFields":
        self._alias = alias
        return self


class PosAngleConstraintFields(GraphQLField):
    mode: "PosAngleConstraintGraphQLField" = PosAngleConstraintGraphQLField("mode")

    @classmethod
    def angle(cls) -> "AngleFields":
        return AngleFields("angle")

    def fields(
        self, *subfields: Union[PosAngleConstraintGraphQLField, "AngleFields"]
    ) -> "PosAngleConstraintFields":
        """Subfields should come from the PosAngleConstraintFields class"""
        self._subfields.extend(subfields)
        return self

    def alias(self, alias: str) -> "PosAngleConstraintFields":
        self._alias = alias
        return self


class PreImagingVariantFields(GraphQLField):
    @classmethod
    def offset_1(cls) -> "OffsetFields":
        return OffsetFields("offset1")

    @classmethod
    def offset_2(cls) -> "OffsetFields":
        return OffsetFields("offset2")

    @classmethod
    def offset_3(cls) -> "OffsetFields":
        return OffsetFields("offset3")

    @classmethod
    def offset_4(cls) -> "OffsetFields":
        return OffsetFields("offset4")

    def fields(
        self, *subfields: Union[PreImagingVariantGraphQLField, "OffsetFields"]
    ) -> "PreImagingVariantFields":
        """Subfields should come from the PreImagingVariantFields class"""
        self._subfields.extend(subfields)
        return self

    def alias(self, alias: str) -> "PreImagingVariantFields":
        self._alias = alias
        return self


class ProgramFields(GraphQLField):
    id: "ProgramGraphQLField" = ProgramGraphQLField("id")
    existence: "ProgramGraphQLField" = ProgramGraphQLField("existence")
    name: "ProgramGraphQLField" = ProgramGraphQLField("name")
    description: "ProgramGraphQLField" = ProgramGraphQLField("description")

    @classmethod
    def notes(cls, include_deleted: bool) -> "ProgramNoteFields":
        arguments: dict[str, dict[str, Any]] = {
            "includeDeleted": {"type": "Boolean!", "value": include_deleted}
        }
        cleared_arguments = {
            key: value for key, value in arguments.items() if value["value"] is not None
        }
        return ProgramNoteFields("notes", arguments=cleared_arguments)

    type_: "ProgramGraphQLField" = ProgramGraphQLField("type")

    @classmethod
    def reference(cls) -> "ProgramReferenceInterface":
        return ProgramReferenceInterface("reference")

    @classmethod
    def proposal(cls) -> "ProposalFields":
        return ProposalFields("proposal")

    @classmethod
    def active(cls) -> "DateIntervalFields":
        return DateIntervalFields("active")

    proposal_status: "ProgramGraphQLField" = ProgramGraphQLField("proposalStatus")

    @classmethod
    def pi(cls) -> "ProgramUserFields":
        return ProgramUserFields("pi")

    @classmethod
    def users(cls) -> "ProgramUserFields":
        return ProgramUserFields("users")

    @classmethod
    def observations(
        cls,
        include_deleted: bool,
        *,
        offset: Optional[Any] = None,
        limit: Optional[Any] = None,
    ) -> "ObservationSelectResultFields":
        arguments: dict[str, dict[str, Any]] = {
            "includeDeleted": {"type": "Boolean!", "value": include_deleted},
            "OFFSET": {"type": "ObservationId", "value": offset},
            "LIMIT": {"type": "NonNegInt", "value": limit},
        }
        cleared_arguments = {
            key: value for key, value in arguments.items() if value["value"] is not None
        }
        return ObservationSelectResultFields(
            "observations", arguments=cleared_arguments
        )

    @classmethod
    def configuration_requests(
        cls, *, offset: Optional[Any] = None, limit: Optional[Any] = None
    ) -> "ConfigurationRequestSelectResultFields":
        arguments: dict[str, dict[str, Any]] = {
            "OFFSET": {"type": "ConfigurationRequestId", "value": offset},
            "LIMIT": {"type": "NonNegInt", "value": limit},
        }
        cleared_arguments = {
            key: value for key, value in arguments.items() if value["value"] is not None
        }
        return ConfigurationRequestSelectResultFields(
            "configurationRequests", arguments=cleared_arguments
        )

    @classmethod
    def attachments(cls) -> "AttachmentFields":
        return AttachmentFields("attachments")

    @classmethod
    def group_elements(cls, include_deleted: bool) -> "GroupElementFields":
        arguments: dict[str, dict[str, Any]] = {
            "includeDeleted": {"type": "Boolean!", "value": include_deleted}
        }
        cleared_arguments = {
            key: value for key, value in arguments.items() if value["value"] is not None
        }
        return GroupElementFields("groupElements", arguments=cleared_arguments)

    @classmethod
    def all_group_elements(cls, include_deleted: bool) -> "GroupElementFields":
        arguments: dict[str, dict[str, Any]] = {
            "includeDeleted": {"type": "Boolean!", "value": include_deleted}
        }
        cleared_arguments = {
            key: value for key, value in arguments.items() if value["value"] is not None
        }
        return GroupElementFields("allGroupElements", arguments=cleared_arguments)

    @classmethod
    def time_estimate_range(cls) -> "CalculatedCategorizedTimeRangeFields":
        return CalculatedCategorizedTimeRangeFields("timeEstimateRange")

    @classmethod
    def time_estimate_banded(cls) -> "CalculatedBandedTimeFields":
        return CalculatedBandedTimeFields("timeEstimateBanded")

    @classmethod
    def time_charge(cls) -> "BandedTimeFields":
        return BandedTimeFields("timeCharge")

    @classmethod
    def user_invitations(cls) -> "UserInvitationFields":
        return UserInvitationFields("userInvitations")

    @classmethod
    def allocations(cls) -> "AllocationFields":
        return AllocationFields("allocations")

    calibration_role: "ProgramGraphQLField" = ProgramGraphQLField("calibrationRole")

    @classmethod
    def goa(cls) -> "GoaPropertiesFields":
        return GoaPropertiesFields("goa")

    resource_limit: "ProgramGraphQLField" = ProgramGraphQLField("resourceLimit")
    resource_count: "ProgramGraphQLField" = ProgramGraphQLField("resourceCount")

    def fields(
        self,
        *subfields: Union[
            ProgramGraphQLField,
            "AllocationFields",
            "AttachmentFields",
            "BandedTimeFields",
            "CalculatedBandedTimeFields",
            "CalculatedCategorizedTimeRangeFields",
            "ConfigurationRequestSelectResultFields",
            "DateIntervalFields",
            "GoaPropertiesFields",
            "GroupElementFields",
            "ObservationSelectResultFields",
            "ProgramNoteFields",
            "ProgramReferenceInterface",
            "ProgramUserFields",
            "ProposalFields",
            "UserInvitationFields",
        ],
    ) -> "ProgramFields":
        """Subfields should come from the ProgramFields class"""
        self._subfields.extend(subfields)
        return self

    def alias(self, alias: str) -> "ProgramFields":
        self._alias = alias
        return self


class ProgramNoteFields(GraphQLField):
    id: "ProgramNoteGraphQLField" = ProgramNoteGraphQLField("id")

    @classmethod
    def program(cls) -> "ProgramFields":
        return ProgramFields("program")

    title: "ProgramNoteGraphQLField" = ProgramNoteGraphQLField("title")
    text: "ProgramNoteGraphQLField" = ProgramNoteGraphQLField("text")
    is_private: "ProgramNoteGraphQLField" = ProgramNoteGraphQLField("isPrivate")
    existence: "ProgramNoteGraphQLField" = ProgramNoteGraphQLField("existence")

    def fields(
        self, *subfields: Union[ProgramNoteGraphQLField, "ProgramFields"]
    ) -> "ProgramNoteFields":
        """Subfields should come from the ProgramNoteFields class"""
        self._subfields.extend(subfields)
        return self

    def alias(self, alias: str) -> "ProgramNoteFields":
        self._alias = alias
        return self


class ProgramNoteSelectResultFields(GraphQLField):
    @classmethod
    def matches(cls) -> "ProgramNoteFields":
        return ProgramNoteFields("matches")

    has_more: "ProgramNoteSelectResultGraphQLField" = (
        ProgramNoteSelectResultGraphQLField("hasMore")
    )

    def fields(
        self,
        *subfields: Union[ProgramNoteSelectResultGraphQLField, "ProgramNoteFields"],
    ) -> "ProgramNoteSelectResultFields":
        """Subfields should come from the ProgramNoteSelectResultFields class"""
        self._subfields.extend(subfields)
        return self

    def alias(self, alias: str) -> "ProgramNoteSelectResultFields":
        self._alias = alias
        return self


class ProgramReferenceInterface(GraphQLField):
    label: "ProgramReferenceGraphQLField" = ProgramReferenceGraphQLField("label")
    type_: "ProgramReferenceGraphQLField" = ProgramReferenceGraphQLField("type")

    def fields(
        self, *subfields: ProgramReferenceGraphQLField
    ) -> "ProgramReferenceInterface":
        """Subfields should come from the ProgramReferenceInterface class"""
        self._subfields.extend(subfields)
        return self

    def alias(self, alias: str) -> "ProgramReferenceInterface":
        self._alias = alias
        return self

    def on(
        self, type_name: str, *subfields: GraphQLField
    ) -> "ProgramReferenceInterface":
        self._inline_fragments[type_name] = subfields
        return self


class ProgramSelectResultFields(GraphQLField):
    @classmethod
    def matches(cls) -> "ProgramFields":
        return ProgramFields("matches")

    has_more: "ProgramSelectResultGraphQLField" = ProgramSelectResultGraphQLField(
        "hasMore"
    )

    def fields(
        self, *subfields: Union[ProgramSelectResultGraphQLField, "ProgramFields"]
    ) -> "ProgramSelectResultFields":
        """Subfields should come from the ProgramSelectResultFields class"""
        self._subfields.extend(subfields)
        return self

    def alias(self, alias: str) -> "ProgramSelectResultFields":
        self._alias = alias
        return self


class ProgramUserFields(GraphQLField):
    id: "ProgramUserGraphQLField" = ProgramUserGraphQLField("id")
    role: "ProgramUserGraphQLField" = ProgramUserGraphQLField("role")

    @classmethod
    def program(cls) -> "ProgramFields":
        return ProgramFields("program")

    @classmethod
    def user(cls) -> "UserFields":
        return UserFields("user")

    @classmethod
    def partner_link(cls) -> "PartnerLinkInterface":
        return PartnerLinkInterface("partnerLink")

    @classmethod
    def preferred_profile(cls) -> "UserProfileFields":
        return UserProfileFields("preferredProfile")

    educational_status: "ProgramUserGraphQLField" = ProgramUserGraphQLField(
        "educationalStatus"
    )
    gender: "ProgramUserGraphQLField" = ProgramUserGraphQLField("gender")
    thesis: "ProgramUserGraphQLField" = ProgramUserGraphQLField("thesis")

    @classmethod
    def invitations(cls) -> "UserInvitationFields":
        return UserInvitationFields("invitations")

    affiliation: "ProgramUserGraphQLField" = ProgramUserGraphQLField("affiliation")
    has_data_access: "ProgramUserGraphQLField" = ProgramUserGraphQLField(
        "hasDataAccess"
    )
    classical_visitor: "ProgramUserGraphQLField" = ProgramUserGraphQLField(
        "classicalVisitor"
    )
    display_name: "ProgramUserGraphQLField" = ProgramUserGraphQLField("displayName")
    email: "ProgramUserGraphQLField" = ProgramUserGraphQLField("email")

    def fields(
        self,
        *subfields: Union[
            ProgramUserGraphQLField,
            "PartnerLinkInterface",
            "ProgramFields",
            "UserFields",
            "UserInvitationFields",
            "UserProfileFields",
        ],
    ) -> "ProgramUserFields":
        """Subfields should come from the ProgramUserFields class"""
        self._subfields.extend(subfields)
        return self

    def alias(self, alias: str) -> "ProgramUserFields":
        self._alias = alias
        return self


class ProgramUserSelectResultFields(GraphQLField):
    @classmethod
    def matches(cls) -> "ProgramUserFields":
        return ProgramUserFields("matches")

    has_more: "ProgramUserSelectResultGraphQLField" = (
        ProgramUserSelectResultGraphQLField("hasMore")
    )

    def fields(
        self,
        *subfields: Union[ProgramUserSelectResultGraphQLField, "ProgramUserFields"],
    ) -> "ProgramUserSelectResultFields":
        """Subfields should come from the ProgramUserSelectResultFields class"""
        self._subfields.extend(subfields)
        return self

    def alias(self, alias: str) -> "ProgramUserSelectResultFields":
        self._alias = alias
        return self


class ProperMotionFields(GraphQLField):
    @classmethod
    def ra(cls) -> "ProperMotionRAFields":
        return ProperMotionRAFields("ra")

    @classmethod
    def dec(cls) -> "ProperMotionDeclinationFields":
        return ProperMotionDeclinationFields("dec")

    def fields(
        self,
        *subfields: Union[
            ProperMotionGraphQLField,
            "ProperMotionDeclinationFields",
            "ProperMotionRAFields",
        ],
    ) -> "ProperMotionFields":
        """Subfields should come from the ProperMotionFields class"""
        self._subfields.extend(subfields)
        return self

    def alias(self, alias: str) -> "ProperMotionFields":
        self._alias = alias
        return self


class ProperMotionDeclinationFields(GraphQLField):
    microarcseconds_per_year: "ProperMotionDeclinationGraphQLField" = (
        ProperMotionDeclinationGraphQLField("microarcsecondsPerYear")
    )
    milliarcseconds_per_year: "ProperMotionDeclinationGraphQLField" = (
        ProperMotionDeclinationGraphQLField("milliarcsecondsPerYear")
    )

    def fields(
        self, *subfields: ProperMotionDeclinationGraphQLField
    ) -> "ProperMotionDeclinationFields":
        """Subfields should come from the ProperMotionDeclinationFields class"""
        self._subfields.extend(subfields)
        return self

    def alias(self, alias: str) -> "ProperMotionDeclinationFields":
        self._alias = alias
        return self


class ProperMotionRAFields(GraphQLField):
    microarcseconds_per_year: "ProperMotionRAGraphQLField" = ProperMotionRAGraphQLField(
        "microarcsecondsPerYear"
    )
    milliarcseconds_per_year: "ProperMotionRAGraphQLField" = ProperMotionRAGraphQLField(
        "milliarcsecondsPerYear"
    )

    def fields(self, *subfields: ProperMotionRAGraphQLField) -> "ProperMotionRAFields":
        """Subfields should come from the ProperMotionRAFields class"""
        self._subfields.extend(subfields)
        return self

    def alias(self, alias: str) -> "ProperMotionRAFields":
        self._alias = alias
        return self


class ProposalFields(GraphQLField):
    @classmethod
    def reference(cls) -> "ProposalReferenceFields":
        return ProposalReferenceFields("reference")

    @classmethod
    def call(cls) -> "CallForProposalsFields":
        return CallForProposalsFields("call")

    category: "ProposalGraphQLField" = ProposalGraphQLField("category")

    @classmethod
    def gemini(cls) -> "GeminiProposalTypeInterface":
        return GeminiProposalTypeInterface("gemini")

    @classmethod
    def keck(cls) -> "KeckProposalTypeFields":
        return KeckProposalTypeFields("keck")

    @classmethod
    def subaru(cls) -> "SubaruProposalTypeFields":
        return SubaruProposalTypeFields("subaru")

    def fields(
        self,
        *subfields: Union[
            ProposalGraphQLField,
            "CallForProposalsFields",
            "GeminiProposalTypeInterface",
            "KeckProposalTypeFields",
            "ProposalReferenceFields",
            "SubaruProposalTypeFields",
        ],
    ) -> "ProposalFields":
        """Subfields should come from the ProposalFields class"""
        self._subfields.extend(subfields)
        return self

    def alias(self, alias: str) -> "ProposalFields":
        self._alias = alias
        return self


class ProposalReferenceFields(GraphQLField):
    label: "ProposalReferenceGraphQLField" = ProposalReferenceGraphQLField("label")
    semester: "ProposalReferenceGraphQLField" = ProposalReferenceGraphQLField(
        "semester"
    )
    semester_index: "ProposalReferenceGraphQLField" = ProposalReferenceGraphQLField(
        "semesterIndex"
    )

    def fields(
        self, *subfields: ProposalReferenceGraphQLField
    ) -> "ProposalReferenceFields":
        """Subfields should come from the ProposalReferenceFields class"""
        self._subfields.extend(subfields)
        return self

    def alias(self, alias: str) -> "ProposalReferenceFields":
        self._alias = alias
        return self


class QueueFields(GraphQLField):
    science_subtype: "QueueGraphQLField" = QueueGraphQLField("scienceSubtype")
    too_activation_ceiling: "QueueGraphQLField" = QueueGraphQLField(
        "tooActivationCeiling"
    )
    default_too_activation_ceiling: "QueueGraphQLField" = QueueGraphQLField(
        "defaultTooActivationCeiling"
    )
    explicit_too_activation_ceiling: "QueueGraphQLField" = QueueGraphQLField(
        "explicitTooActivationCeiling"
    )
    min_percent_time: "QueueGraphQLField" = QueueGraphQLField("minPercentTime")

    @classmethod
    def partner_splits(cls) -> "PartnerSplitFields":
        return PartnerSplitFields("partnerSplits")

    exchange_partner: "QueueGraphQLField" = QueueGraphQLField("exchangePartner")
    consider_for_band_3: "QueueGraphQLField" = QueueGraphQLField("considerForBand3")
    aeon_multi_facility: "QueueGraphQLField" = QueueGraphQLField("aeonMultiFacility")
    jwst_synergy: "QueueGraphQLField" = QueueGraphQLField("jwstSynergy")
    us_long_term: "QueueGraphQLField" = QueueGraphQLField("usLongTerm")

    def fields(
        self, *subfields: Union[QueueGraphQLField, "PartnerSplitFields"]
    ) -> "QueueFields":
        """Subfields should come from the QueueFields class"""
        self._subfields.extend(subfields)
        return self

    def alias(self, alias: str) -> "QueueFields":
        self._alias = alias
        return self


class RadialVelocityFields(GraphQLField):
    centimeters_per_second: "RadialVelocityGraphQLField" = RadialVelocityGraphQLField(
        "centimetersPerSecond"
    )
    meters_per_second: "RadialVelocityGraphQLField" = RadialVelocityGraphQLField(
        "metersPerSecond"
    )
    kilometers_per_second: "RadialVelocityGraphQLField" = RadialVelocityGraphQLField(
        "kilometersPerSecond"
    )

    def fields(self, *subfields: RadialVelocityGraphQLField) -> "RadialVelocityFields":
        """Subfields should come from the RadialVelocityFields class"""
        self._subfields.extend(subfields)
        return self

    def alias(self, alias: str) -> "RadialVelocityFields":
        self._alias = alias
        return self


class RandomTelescopeConfigGeneratorFields(GraphQLField):
    @classmethod
    def size(cls) -> "AngleFields":
        return AngleFields("size")

    @classmethod
    def center(cls) -> "OffsetFields":
        return OffsetFields("center")

    seed: "RandomTelescopeConfigGeneratorGraphQLField" = (
        RandomTelescopeConfigGeneratorGraphQLField("seed")
    )

    def fields(
        self,
        *subfields: Union[
            RandomTelescopeConfigGeneratorGraphQLField, "AngleFields", "OffsetFields"
        ],
    ) -> "RandomTelescopeConfigGeneratorFields":
        """Subfields should come from the RandomTelescopeConfigGeneratorFields class"""
        self._subfields.extend(subfields)
        return self

    def alias(self, alias: str) -> "RandomTelescopeConfigGeneratorFields":
        self._alias = alias
        return self


class RecordDatasetResultFields(GraphQLField):
    @classmethod
    def dataset(cls) -> "DatasetFields":
        return DatasetFields("dataset")

    def fields(
        self, *subfields: Union[RecordDatasetResultGraphQLField, "DatasetFields"]
    ) -> "RecordDatasetResultFields":
        """Subfields should come from the RecordDatasetResultFields class"""
        self._subfields.extend(subfields)
        return self

    def alias(self, alias: str) -> "RecordDatasetResultFields":
        self._alias = alias
        return self


class RecordFlamingos2VisitResultFields(GraphQLField):
    @classmethod
    def visit(cls) -> "VisitFields":
        return VisitFields("visit")

    def fields(
        self, *subfields: Union[RecordFlamingos2VisitResultGraphQLField, "VisitFields"]
    ) -> "RecordFlamingos2VisitResultFields":
        """Subfields should come from the RecordFlamingos2VisitResultFields class"""
        self._subfields.extend(subfields)
        return self

    def alias(self, alias: str) -> "RecordFlamingos2VisitResultFields":
        self._alias = alias
        return self


class RecordGmosNorthVisitResultFields(GraphQLField):
    @classmethod
    def visit(cls) -> "VisitFields":
        return VisitFields("visit")

    def fields(
        self, *subfields: Union[RecordGmosNorthVisitResultGraphQLField, "VisitFields"]
    ) -> "RecordGmosNorthVisitResultFields":
        """Subfields should come from the RecordGmosNorthVisitResultFields class"""
        self._subfields.extend(subfields)
        return self

    def alias(self, alias: str) -> "RecordGmosNorthVisitResultFields":
        self._alias = alias
        return self


class RecordGmosSouthVisitResultFields(GraphQLField):
    @classmethod
    def visit(cls) -> "VisitFields":
        return VisitFields("visit")

    def fields(
        self, *subfields: Union[RecordGmosSouthVisitResultGraphQLField, "VisitFields"]
    ) -> "RecordGmosSouthVisitResultFields":
        """Subfields should come from the RecordGmosSouthVisitResultFields class"""
        self._subfields.extend(subfields)
        return self

    def alias(self, alias: str) -> "RecordGmosSouthVisitResultFields":
        self._alias = alias
        return self


class RecordIgrins2VisitResultFields(GraphQLField):
    @classmethod
    def visit(cls) -> "VisitFields":
        return VisitFields("visit")

    def fields(
        self, *subfields: Union[RecordIgrins2VisitResultGraphQLField, "VisitFields"]
    ) -> "RecordIgrins2VisitResultFields":
        """Subfields should come from the RecordIgrins2VisitResultFields class"""
        self._subfields.extend(subfields)
        return self

    def alias(self, alias: str) -> "RecordIgrins2VisitResultFields":
        self._alias = alias
        return self


class RecordVisitResultFields(GraphQLField):
    @classmethod
    def visit(cls) -> "VisitFields":
        return VisitFields("visit")

    def fields(
        self, *subfields: Union[RecordVisitResultGraphQLField, "VisitFields"]
    ) -> "RecordVisitResultFields":
        """Subfields should come from the RecordVisitResultFields class"""
        self._subfields.extend(subfields)
        return self

    def alias(self, alias: str) -> "RecordVisitResultFields":
        self._alias = alias
        return self


class RedeemUserInvitationResultFields(GraphQLField):
    @classmethod
    def invitation(cls) -> "UserInvitationFields":
        return UserInvitationFields("invitation")

    def fields(
        self,
        *subfields: Union[
            RedeemUserInvitationResultGraphQLField, "UserInvitationFields"
        ],
    ) -> "RedeemUserInvitationResultFields":
        """Subfields should come from the RedeemUserInvitationResultFields class"""
        self._subfields.extend(subfields)
        return self

    def alias(self, alias: str) -> "RedeemUserInvitationResultFields":
        self._alias = alias
        return self


class RefreshArchiveDuplicationResultFields(GraphQLField):
    @classmethod
    def archive_duplication(cls) -> "ArchiveDuplicationFields":
        return ArchiveDuplicationFields("archiveDuplication")

    @classmethod
    def observation(cls) -> "ObservationFields":
        return ObservationFields("observation")

    def fields(
        self,
        *subfields: Union[
            RefreshArchiveDuplicationResultGraphQLField,
            "ArchiveDuplicationFields",
            "ObservationFields",
        ],
    ) -> "RefreshArchiveDuplicationResultFields":
        """Subfields should come from the RefreshArchiveDuplicationResultFields class"""
        self._subfields.extend(subfields)
        return self

    def alias(self, alias: str) -> "RefreshArchiveDuplicationResultFields":
        self._alias = alias
        return self


class RegionFields(GraphQLField):
    @classmethod
    def right_ascension_arc(cls) -> "RightAscensionArcFields":
        return RightAscensionArcFields("rightAscensionArc")

    @classmethod
    def declination_arc(cls) -> "DeclinationArcFields":
        return DeclinationArcFields("declinationArc")

    def fields(
        self,
        *subfields: Union[
            RegionGraphQLField, "DeclinationArcFields", "RightAscensionArcFields"
        ],
    ) -> "RegionFields":
        """Subfields should come from the RegionFields class"""
        self._subfields.extend(subfields)
        return self

    def alias(self, alias: str) -> "RegionFields":
        self._alias = alias
        return self


class ReplaceFlamingos2SequenceResultFields(GraphQLField):
    @classmethod
    def sequence(cls) -> "Flamingos2AtomFields":
        return Flamingos2AtomFields("sequence")

    def fields(
        self,
        *subfields: Union[
            ReplaceFlamingos2SequenceResultGraphQLField, "Flamingos2AtomFields"
        ],
    ) -> "ReplaceFlamingos2SequenceResultFields":
        """Subfields should come from the ReplaceFlamingos2SequenceResultFields class"""
        self._subfields.extend(subfields)
        return self

    def alias(self, alias: str) -> "ReplaceFlamingos2SequenceResultFields":
        self._alias = alias
        return self


class ReplaceGhostSequenceResultFields(GraphQLField):
    @classmethod
    def sequence(cls) -> "GhostAtomFields":
        return GhostAtomFields("sequence")

    def fields(
        self,
        *subfields: Union[ReplaceGhostSequenceResultGraphQLField, "GhostAtomFields"],
    ) -> "ReplaceGhostSequenceResultFields":
        """Subfields should come from the ReplaceGhostSequenceResultFields class"""
        self._subfields.extend(subfields)
        return self

    def alias(self, alias: str) -> "ReplaceGhostSequenceResultFields":
        self._alias = alias
        return self


class ReplaceGmosNorthSequenceResultFields(GraphQLField):
    @classmethod
    def sequence(cls) -> "GmosNorthAtomFields":
        return GmosNorthAtomFields("sequence")

    def fields(
        self,
        *subfields: Union[
            ReplaceGmosNorthSequenceResultGraphQLField, "GmosNorthAtomFields"
        ],
    ) -> "ReplaceGmosNorthSequenceResultFields":
        """Subfields should come from the ReplaceGmosNorthSequenceResultFields class"""
        self._subfields.extend(subfields)
        return self

    def alias(self, alias: str) -> "ReplaceGmosNorthSequenceResultFields":
        self._alias = alias
        return self


class ReplaceGmosSouthSequenceResultFields(GraphQLField):
    @classmethod
    def sequence(cls) -> "GmosSouthAtomFields":
        return GmosSouthAtomFields("sequence")

    def fields(
        self,
        *subfields: Union[
            ReplaceGmosSouthSequenceResultGraphQLField, "GmosSouthAtomFields"
        ],
    ) -> "ReplaceGmosSouthSequenceResultFields":
        """Subfields should come from the ReplaceGmosSouthSequenceResultFields class"""
        self._subfields.extend(subfields)
        return self

    def alias(self, alias: str) -> "ReplaceGmosSouthSequenceResultFields":
        self._alias = alias
        return self


class ReplaceGnirsSequenceResultFields(GraphQLField):
    @classmethod
    def sequence(cls) -> "GnirsAtomFields":
        return GnirsAtomFields("sequence")

    def fields(
        self,
        *subfields: Union[ReplaceGnirsSequenceResultGraphQLField, "GnirsAtomFields"],
    ) -> "ReplaceGnirsSequenceResultFields":
        """Subfields should come from the ReplaceGnirsSequenceResultFields class"""
        self._subfields.extend(subfields)
        return self

    def alias(self, alias: str) -> "ReplaceGnirsSequenceResultFields":
        self._alias = alias
        return self


class ReplaceIgrins2SequenceResultFields(GraphQLField):
    @classmethod
    def sequence(cls) -> "Igrins2AtomFields":
        return Igrins2AtomFields("sequence")

    def fields(
        self,
        *subfields: Union[
            ReplaceIgrins2SequenceResultGraphQLField, "Igrins2AtomFields"
        ],
    ) -> "ReplaceIgrins2SequenceResultFields":
        """Subfields should come from the ReplaceIgrins2SequenceResultFields class"""
        self._subfields.extend(subfields)
        return self

    def alias(self, alias: str) -> "ReplaceIgrins2SequenceResultFields":
        self._alias = alias
        return self


class ResetAcquisitionResultFields(GraphQLField):
    @classmethod
    def observation(cls) -> "ObservationFields":
        return ObservationFields("observation")

    def fields(
        self, *subfields: Union[ResetAcquisitionResultGraphQLField, "ObservationFields"]
    ) -> "ResetAcquisitionResultFields":
        """Subfields should come from the ResetAcquisitionResultFields class"""
        self._subfields.extend(subfields)
        return self

    def alias(self, alias: str) -> "ResetAcquisitionResultFields":
        self._alias = alias
        return self


class RevokeUserInvitationResultFields(GraphQLField):
    @classmethod
    def invitation(cls) -> "UserInvitationFields":
        return UserInvitationFields("invitation")

    def fields(
        self,
        *subfields: Union[
            RevokeUserInvitationResultGraphQLField, "UserInvitationFields"
        ],
    ) -> "RevokeUserInvitationResultFields":
        """Subfields should come from the RevokeUserInvitationResultFields class"""
        self._subfields.extend(subfields)
        return self

    def alias(self, alias: str) -> "RevokeUserInvitationResultFields":
        self._alias = alias
        return self


class RightAscensionFields(GraphQLField):
    hms: "RightAscensionGraphQLField" = RightAscensionGraphQLField("hms")
    hours: "RightAscensionGraphQLField" = RightAscensionGraphQLField("hours")
    degrees: "RightAscensionGraphQLField" = RightAscensionGraphQLField("degrees")
    microseconds: "RightAscensionGraphQLField" = RightAscensionGraphQLField(
        "microseconds"
    )

    def fields(self, *subfields: RightAscensionGraphQLField) -> "RightAscensionFields":
        """Subfields should come from the RightAscensionFields class"""
        self._subfields.extend(subfields)
        return self

    def alias(self, alias: str) -> "RightAscensionFields":
        self._alias = alias
        return self


class RightAscensionArcFields(GraphQLField):
    type_: "RightAscensionArcGraphQLField" = RightAscensionArcGraphQLField("type")

    @classmethod
    def start(cls) -> "RightAscensionFields":
        return RightAscensionFields("start")

    @classmethod
    def end(cls) -> "RightAscensionFields":
        return RightAscensionFields("end")

    def fields(
        self, *subfields: Union[RightAscensionArcGraphQLField, "RightAscensionFields"]
    ) -> "RightAscensionArcFields":
        """Subfields should come from the RightAscensionArcFields class"""
        self._subfields.extend(subfields)
        return self

    def alias(self, alias: str) -> "RightAscensionArcFields":
        self._alias = alias
        return self


class SchedulingConstraintsFields(GraphQLField):
    too_activation: "SchedulingConstraintsGraphQLField" = (
        SchedulingConstraintsGraphQLField("tooActivation")
    )
    execution_requirement: "SchedulingConstraintsGraphQLField" = (
        SchedulingConstraintsGraphQLField("executionRequirement")
    )
    default_execution_requirement: "SchedulingConstraintsGraphQLField" = (
        SchedulingConstraintsGraphQLField("defaultExecutionRequirement")
    )
    explicit_execution_requirement: "SchedulingConstraintsGraphQLField" = (
        SchedulingConstraintsGraphQLField("explicitExecutionRequirement")
    )
    is_splittable: "SchedulingConstraintsGraphQLField" = (
        SchedulingConstraintsGraphQLField("isSplittable")
    )

    @classmethod
    def timing_windows(cls) -> "TimingWindowFields":
        return TimingWindowFields("timingWindows")

    def fields(
        self, *subfields: Union[SchedulingConstraintsGraphQLField, "TimingWindowFields"]
    ) -> "SchedulingConstraintsFields":
        """Subfields should come from the SchedulingConstraintsFields class"""
        self._subfields.extend(subfields)
        return self

    def alias(self, alias: str) -> "SchedulingConstraintsFields":
        self._alias = alias
        return self


class ScienceFields(GraphQLField):
    step_type: "ScienceGraphQLField" = ScienceGraphQLField("stepType")

    def fields(self, *subfields: ScienceGraphQLField) -> "ScienceFields":
        """Subfields should come from the ScienceFields class"""
        self._subfields.extend(subfields)
        return self

    def alias(self, alias: str) -> "ScienceFields":
        self._alias = alias
        return self


class ScienceProgramReferenceFields(GraphQLField):
    label: "ScienceProgramReferenceGraphQLField" = ScienceProgramReferenceGraphQLField(
        "label"
    )
    type_: "ScienceProgramReferenceGraphQLField" = ScienceProgramReferenceGraphQLField(
        "type"
    )
    science_subtype: "ScienceProgramReferenceGraphQLField" = (
        ScienceProgramReferenceGraphQLField("scienceSubtype")
    )
    semester: "ScienceProgramReferenceGraphQLField" = (
        ScienceProgramReferenceGraphQLField("semester")
    )
    semester_index: "ScienceProgramReferenceGraphQLField" = (
        ScienceProgramReferenceGraphQLField("semesterIndex")
    )

    def fields(
        self, *subfields: ScienceProgramReferenceGraphQLField
    ) -> "ScienceProgramReferenceFields":
        """Subfields should come from the ScienceProgramReferenceFields class"""
        self._subfields.extend(subfields)
        return self

    def alias(self, alias: str) -> "ScienceProgramReferenceFields":
        self._alias = alias
        return self


class ScienceRequirementsFields(GraphQLField):
    mode: "ScienceRequirementsGraphQLField" = ScienceRequirementsGraphQLField("mode")

    @classmethod
    def exposure_time_mode(cls) -> "ExposureTimeModeFields":
        return ExposureTimeModeFields("exposureTimeMode")

    @classmethod
    def spectroscopy(cls) -> "SpectroscopyScienceRequirementsFields":
        return SpectroscopyScienceRequirementsFields("spectroscopy")

    @classmethod
    def imaging(cls) -> "ImagingScienceRequirementsFields":
        return ImagingScienceRequirementsFields("imaging")

    def fields(
        self,
        *subfields: Union[
            ScienceRequirementsGraphQLField,
            "ExposureTimeModeFields",
            "ImagingScienceRequirementsFields",
            "SpectroscopyScienceRequirementsFields",
        ],
    ) -> "ScienceRequirementsFields":
        """Subfields should come from the ScienceRequirementsFields class"""
        self._subfields.extend(subfields)
        return self

    def alias(self, alias: str) -> "ScienceRequirementsFields":
        self._alias = alias
        return self


class SequenceDigestFields(GraphQLField):
    observe_class: "SequenceDigestGraphQLField" = SequenceDigestGraphQLField(
        "observeClass"
    )

    @classmethod
    def time_estimate(cls) -> "CategorizedTimeFields":
        return CategorizedTimeFields("timeEstimate")

    @classmethod
    def telescope_configs(cls) -> "TelescopeConfigFields":
        return TelescopeConfigFields("telescopeConfigs")

    atom_count: "SequenceDigestGraphQLField" = SequenceDigestGraphQLField("atomCount")
    execution_state: "SequenceDigestGraphQLField" = SequenceDigestGraphQLField(
        "executionState"
    )

    def fields(
        self,
        *subfields: Union[
            SequenceDigestGraphQLField, "CategorizedTimeFields", "TelescopeConfigFields"
        ],
    ) -> "SequenceDigestFields":
        """Subfields should come from the SequenceDigestFields class"""
        self._subfields.extend(subfields)
        return self

    def alias(self, alias: str) -> "SequenceDigestFields":
        self._alias = alias
        return self


class SequenceEventFields(GraphQLField):
    id: "SequenceEventGraphQLField" = SequenceEventGraphQLField("id")

    @classmethod
    def visit(cls) -> "VisitFields":
        return VisitFields("visit")

    @classmethod
    def observation(cls) -> "ObservationFields":
        return ObservationFields("observation")

    recorded_time: "SequenceEventGraphQLField" = SequenceEventGraphQLField(
        "recordedTime"
    )
    received: "SequenceEventGraphQLField" = SequenceEventGraphQLField("received")
    client_time: "SequenceEventGraphQLField" = SequenceEventGraphQLField("clientTime")
    effective_time: "SequenceEventGraphQLField" = SequenceEventGraphQLField(
        "effectiveTime"
    )
    event_type: "SequenceEventGraphQLField" = SequenceEventGraphQLField("eventType")
    command: "SequenceEventGraphQLField" = SequenceEventGraphQLField("command")
    idempotency_key: "SequenceEventGraphQLField" = SequenceEventGraphQLField(
        "idempotencyKey"
    )

    def fields(
        self,
        *subfields: Union[
            SequenceEventGraphQLField, "ObservationFields", "VisitFields"
        ],
    ) -> "SequenceEventFields":
        """Subfields should come from the SequenceEventFields class"""
        self._subfields.extend(subfields)
        return self

    def alias(self, alias: str) -> "SequenceEventFields":
        self._alias = alias
        return self


class SetAllocationsResultFields(GraphQLField):
    @classmethod
    def allocations(cls) -> "AllocationFields":
        return AllocationFields("allocations")

    def fields(
        self, *subfields: Union[SetAllocationsResultGraphQLField, "AllocationFields"]
    ) -> "SetAllocationsResultFields":
        """Subfields should come from the SetAllocationsResultFields class"""
        self._subfields.extend(subfields)
        return self

    def alias(self, alias: str) -> "SetAllocationsResultFields":
        self._alias = alias
        return self


class SetGuideTargetNameResultFields(GraphQLField):
    @classmethod
    def observation(cls) -> "ObservationFields":
        return ObservationFields("observation")

    def fields(
        self,
        *subfields: Union[SetGuideTargetNameResultGraphQLField, "ObservationFields"],
    ) -> "SetGuideTargetNameResultFields":
        """Subfields should come from the SetGuideTargetNameResultFields class"""
        self._subfields.extend(subfields)
        return self

    def alias(self, alias: str) -> "SetGuideTargetNameResultFields":
        self._alias = alias
        return self


class SetProgramReferenceResultFields(GraphQLField):
    @classmethod
    def reference(cls) -> "ProgramReferenceInterface":
        return ProgramReferenceInterface("reference")

    def fields(
        self,
        *subfields: Union[
            SetProgramReferenceResultGraphQLField, "ProgramReferenceInterface"
        ],
    ) -> "SetProgramReferenceResultFields":
        """Subfields should come from the SetProgramReferenceResultFields class"""
        self._subfields.extend(subfields)
        return self

    def alias(self, alias: str) -> "SetProgramReferenceResultFields":
        self._alias = alias
        return self


class SetProgramResourceLimitResultFields(GraphQLField):
    @classmethod
    def program(cls) -> "ProgramFields":
        return ProgramFields("program")

    def fields(
        self,
        *subfields: Union[SetProgramResourceLimitResultGraphQLField, "ProgramFields"],
    ) -> "SetProgramResourceLimitResultFields":
        """Subfields should come from the SetProgramResourceLimitResultFields class"""
        self._subfields.extend(subfields)
        return self

    def alias(self, alias: str) -> "SetProgramResourceLimitResultFields":
        self._alias = alias
        return self


class SetProposalStatusResultFields(GraphQLField):
    @classmethod
    def program(cls) -> "ProgramFields":
        return ProgramFields("program")

    def fields(
        self, *subfields: Union[SetProposalStatusResultGraphQLField, "ProgramFields"]
    ) -> "SetProposalStatusResultFields":
        """Subfields should come from the SetProposalStatusResultFields class"""
        self._subfields.extend(subfields)
        return self

    def alias(self, alias: str) -> "SetProposalStatusResultFields":
        self._alias = alias
        return self


class SetupTimeFields(GraphQLField):
    @classmethod
    def full(cls) -> "TimeSpanFields":
        return TimeSpanFields("full")

    @classmethod
    def reacquisition(cls) -> "TimeSpanFields":
        return TimeSpanFields("reacquisition")

    def fields(
        self, *subfields: Union[SetupTimeGraphQLField, "TimeSpanFields"]
    ) -> "SetupTimeFields":
        """Subfields should come from the SetupTimeFields class"""
        self._subfields.extend(subfields)
        return self

    def alias(self, alias: str) -> "SetupTimeFields":
        self._alias = alias
        return self


class SiderealFields(GraphQLField):
    @classmethod
    def ra(cls) -> "RightAscensionFields":
        return RightAscensionFields("ra")

    @classmethod
    def dec(cls) -> "DeclinationFields":
        return DeclinationFields("dec")

    epoch: "SiderealGraphQLField" = SiderealGraphQLField("epoch")

    @classmethod
    def proper_motion(cls) -> "ProperMotionFields":
        return ProperMotionFields("properMotion")

    @classmethod
    def radial_velocity(cls) -> "RadialVelocityFields":
        return RadialVelocityFields("radialVelocity")

    @classmethod
    def parallax(cls) -> "ParallaxFields":
        return ParallaxFields("parallax")

    @classmethod
    def catalog_info(cls) -> "CatalogInfoFields":
        return CatalogInfoFields("catalogInfo")

    def fields(
        self,
        *subfields: Union[
            SiderealGraphQLField,
            "CatalogInfoFields",
            "DeclinationFields",
            "ParallaxFields",
            "ProperMotionFields",
            "RadialVelocityFields",
            "RightAscensionFields",
        ],
    ) -> "SiderealFields":
        """Subfields should come from the SiderealFields class"""
        self._subfields.extend(subfields)
        return self

    def alias(self, alias: str) -> "SiderealFields":
        self._alias = alias
        return self


class SignalToNoiseAtFields(GraphQLField):
    single: "SignalToNoiseAtGraphQLField" = SignalToNoiseAtGraphQLField("single")
    total: "SignalToNoiseAtGraphQLField" = SignalToNoiseAtGraphQLField("total")

    @classmethod
    def wavelength(cls) -> "WavelengthFields":
        return WavelengthFields("wavelength")

    def fields(
        self, *subfields: Union[SignalToNoiseAtGraphQLField, "WavelengthFields"]
    ) -> "SignalToNoiseAtFields":
        """Subfields should come from the SignalToNoiseAtFields class"""
        self._subfields.extend(subfields)
        return self

    def alias(self, alias: str) -> "SignalToNoiseAtFields":
        self._alias = alias
        return self


class SignalToNoiseExposureTimeModeFields(GraphQLField):
    value: "SignalToNoiseExposureTimeModeGraphQLField" = (
        SignalToNoiseExposureTimeModeGraphQLField("value")
    )

    @classmethod
    def at(cls) -> "WavelengthFields":
        return WavelengthFields("at")

    def fields(
        self,
        *subfields: Union[
            SignalToNoiseExposureTimeModeGraphQLField, "WavelengthFields"
        ],
    ) -> "SignalToNoiseExposureTimeModeFields":
        """Subfields should come from the SignalToNoiseExposureTimeModeFields class"""
        self._subfields.extend(subfields)
        return self

    def alias(self, alias: str) -> "SignalToNoiseExposureTimeModeFields":
        self._alias = alias
        return self


class SiteCoordinateLimitsFields(GraphQLField):
    @classmethod
    def north(cls) -> "CoordinateLimitsFields":
        return CoordinateLimitsFields("north")

    @classmethod
    def south(cls) -> "CoordinateLimitsFields":
        return CoordinateLimitsFields("south")

    def fields(
        self,
        *subfields: Union[SiteCoordinateLimitsGraphQLField, "CoordinateLimitsFields"],
    ) -> "SiteCoordinateLimitsFields":
        """Subfields should come from the SiteCoordinateLimitsFields class"""
        self._subfields.extend(subfields)
        return self

    def alias(self, alias: str) -> "SiteCoordinateLimitsFields":
        self._alias = alias
        return self


class SlewEventFields(GraphQLField):
    id: "SlewEventGraphQLField" = SlewEventGraphQLField("id")

    @classmethod
    def visit(cls) -> "VisitFields":
        return VisitFields("visit")

    @classmethod
    def observation(cls) -> "ObservationFields":
        return ObservationFields("observation")

    recorded_time: "SlewEventGraphQLField" = SlewEventGraphQLField("recordedTime")
    received: "SlewEventGraphQLField" = SlewEventGraphQLField("received")
    client_time: "SlewEventGraphQLField" = SlewEventGraphQLField("clientTime")
    effective_time: "SlewEventGraphQLField" = SlewEventGraphQLField("effectiveTime")
    event_type: "SlewEventGraphQLField" = SlewEventGraphQLField("eventType")
    slew_stage: "SlewEventGraphQLField" = SlewEventGraphQLField("slewStage")
    idempotency_key: "SlewEventGraphQLField" = SlewEventGraphQLField("idempotencyKey")

    def fields(
        self,
        *subfields: Union[SlewEventGraphQLField, "ObservationFields", "VisitFields"],
    ) -> "SlewEventFields":
        """Subfields should come from the SlewEventFields class"""
        self._subfields.extend(subfields)
        return self

    def alias(self, alias: str) -> "SlewEventFields":
        self._alias = alias
        return self


class SlitTelescopeConfigsFields(GraphQLField):
    offset_mode: "SlitTelescopeConfigsGraphQLField" = SlitTelescopeConfigsGraphQLField(
        "offsetMode"
    )

    @classmethod
    def along_slit(cls) -> "TelescopeConfigAlongSlitFields":
        return TelescopeConfigAlongSlitFields("alongSlit")

    @classmethod
    def to_sky(cls) -> "TelescopeConfigFields":
        return TelescopeConfigFields("toSky")

    def fields(
        self,
        *subfields: Union[
            SlitTelescopeConfigsGraphQLField,
            "TelescopeConfigAlongSlitFields",
            "TelescopeConfigFields",
        ],
    ) -> "SlitTelescopeConfigsFields":
        """Subfields should come from the SlitTelescopeConfigsFields class"""
        self._subfields.extend(subfields)
        return self

    def alias(self, alias: str) -> "SlitTelescopeConfigsFields":
        self._alias = alias
        return self


class SmartGcalFields(GraphQLField):
    smart_gcal_type: "SmartGcalGraphQLField" = SmartGcalGraphQLField("smartGcalType")
    step_type: "SmartGcalGraphQLField" = SmartGcalGraphQLField("stepType")

    def fields(self, *subfields: SmartGcalGraphQLField) -> "SmartGcalFields":
        """Subfields should come from the SmartGcalFields class"""
        self._subfields.extend(subfields)
        return self

    def alias(self, alias: str) -> "SmartGcalFields":
        self._alias = alias
        return self


class SourceProfileFields(GraphQLField):
    @classmethod
    def point(cls) -> "SpectralDefinitionIntegratedFields":
        return SpectralDefinitionIntegratedFields("point")

    @classmethod
    def uniform(cls) -> "SpectralDefinitionSurfaceFields":
        return SpectralDefinitionSurfaceFields("uniform")

    @classmethod
    def gaussian(cls) -> "GaussianSourceFields":
        return GaussianSourceFields("gaussian")

    def fields(
        self,
        *subfields: Union[
            SourceProfileGraphQLField,
            "GaussianSourceFields",
            "SpectralDefinitionIntegratedFields",
            "SpectralDefinitionSurfaceFields",
        ],
    ) -> "SourceProfileFields":
        """Subfields should come from the SourceProfileFields class"""
        self._subfields.extend(subfields)
        return self

    def alias(self, alias: str) -> "SourceProfileFields":
        self._alias = alias
        return self


class SpectralDefinitionIntegratedFields(GraphQLField):
    @classmethod
    def band_normalized(cls) -> "BandNormalizedIntegratedFields":
        return BandNormalizedIntegratedFields("bandNormalized")

    @classmethod
    def emission_lines(cls) -> "EmissionLinesIntegratedFields":
        return EmissionLinesIntegratedFields("emissionLines")

    def fields(
        self,
        *subfields: Union[
            SpectralDefinitionIntegratedGraphQLField,
            "BandNormalizedIntegratedFields",
            "EmissionLinesIntegratedFields",
        ],
    ) -> "SpectralDefinitionIntegratedFields":
        """Subfields should come from the SpectralDefinitionIntegratedFields class"""
        self._subfields.extend(subfields)
        return self

    def alias(self, alias: str) -> "SpectralDefinitionIntegratedFields":
        self._alias = alias
        return self


class SpectralDefinitionSurfaceFields(GraphQLField):
    @classmethod
    def band_normalized(cls) -> "BandNormalizedSurfaceFields":
        return BandNormalizedSurfaceFields("bandNormalized")

    @classmethod
    def emission_lines(cls) -> "EmissionLinesSurfaceFields":
        return EmissionLinesSurfaceFields("emissionLines")

    def fields(
        self,
        *subfields: Union[
            SpectralDefinitionSurfaceGraphQLField,
            "BandNormalizedSurfaceFields",
            "EmissionLinesSurfaceFields",
        ],
    ) -> "SpectralDefinitionSurfaceFields":
        """Subfields should come from the SpectralDefinitionSurfaceFields class"""
        self._subfields.extend(subfields)
        return self

    def alias(self, alias: str) -> "SpectralDefinitionSurfaceFields":
        self._alias = alias
        return self


class SpectroscopyConfigOptionFields(GraphQLField):
    name: "SpectroscopyConfigOptionGraphQLField" = SpectroscopyConfigOptionGraphQLField(
        "name"
    )
    instrument: "SpectroscopyConfigOptionGraphQLField" = (
        SpectroscopyConfigOptionGraphQLField("instrument")
    )
    focal_plane: "SpectroscopyConfigOptionGraphQLField" = (
        SpectroscopyConfigOptionGraphQLField("focalPlane")
    )
    fpu_label: "SpectroscopyConfigOptionGraphQLField" = (
        SpectroscopyConfigOptionGraphQLField("fpuLabel")
    )

    @classmethod
    def slit_width(cls) -> "AngleFields":
        return AngleFields("slitWidth")

    @classmethod
    def slit_length(cls) -> "AngleFields":
        return AngleFields("slitLength")

    disperser_label: "SpectroscopyConfigOptionGraphQLField" = (
        SpectroscopyConfigOptionGraphQLField("disperserLabel")
    )
    filter_label: "SpectroscopyConfigOptionGraphQLField" = (
        SpectroscopyConfigOptionGraphQLField("filterLabel")
    )

    @classmethod
    def wavelength_min(cls) -> "WavelengthFields":
        return WavelengthFields("wavelengthMin")

    @classmethod
    def wavelength_max(cls) -> "WavelengthFields":
        return WavelengthFields("wavelengthMax")

    @classmethod
    def wavelength_optimal(cls) -> "WavelengthFields":
        return WavelengthFields("wavelengthOptimal")

    @classmethod
    def wavelength_coverage(cls) -> "WavelengthFields":
        return WavelengthFields("wavelengthCoverage")

    resolution: "SpectroscopyConfigOptionGraphQLField" = (
        SpectroscopyConfigOptionGraphQLField("resolution")
    )
    adaptive_optics: "SpectroscopyConfigOptionGraphQLField" = (
        SpectroscopyConfigOptionGraphQLField("adaptiveOptics")
    )
    capability: "SpectroscopyConfigOptionGraphQLField" = (
        SpectroscopyConfigOptionGraphQLField("capability")
    )
    site: "SpectroscopyConfigOptionGraphQLField" = SpectroscopyConfigOptionGraphQLField(
        "site"
    )

    @classmethod
    def flamingos_2(cls) -> "SpectroscopyConfigOptionFlamingos2Fields":
        return SpectroscopyConfigOptionFlamingos2Fields("flamingos2")

    @classmethod
    def ghost(cls) -> "SpectroscopyConfigOptionGhostFields":
        return SpectroscopyConfigOptionGhostFields("ghost")

    @classmethod
    def gmos_north(cls) -> "SpectroscopyConfigOptionGmosNorthFields":
        return SpectroscopyConfigOptionGmosNorthFields("gmosNorth")

    @classmethod
    def gmos_south(cls) -> "SpectroscopyConfigOptionGmosSouthFields":
        return SpectroscopyConfigOptionGmosSouthFields("gmosSouth")

    @classmethod
    def gnirs(cls) -> "SpectroscopyConfigOptionGnirsFields":
        return SpectroscopyConfigOptionGnirsFields("gnirs")

    def fields(
        self,
        *subfields: Union[
            SpectroscopyConfigOptionGraphQLField,
            "AngleFields",
            "SpectroscopyConfigOptionFlamingos2Fields",
            "SpectroscopyConfigOptionGhostFields",
            "SpectroscopyConfigOptionGmosNorthFields",
            "SpectroscopyConfigOptionGmosSouthFields",
            "SpectroscopyConfigOptionGnirsFields",
            "WavelengthFields",
        ],
    ) -> "SpectroscopyConfigOptionFields":
        """Subfields should come from the SpectroscopyConfigOptionFields class"""
        self._subfields.extend(subfields)
        return self

    def alias(self, alias: str) -> "SpectroscopyConfigOptionFields":
        self._alias = alias
        return self


class SpectroscopyConfigOptionFlamingos2Fields(GraphQLField):
    fpu: "SpectroscopyConfigOptionFlamingos2GraphQLField" = (
        SpectroscopyConfigOptionFlamingos2GraphQLField("fpu")
    )
    disperser: "SpectroscopyConfigOptionFlamingos2GraphQLField" = (
        SpectroscopyConfigOptionFlamingos2GraphQLField("disperser")
    )
    filter_: "SpectroscopyConfigOptionFlamingos2GraphQLField" = (
        SpectroscopyConfigOptionFlamingos2GraphQLField("filter")
    )

    def fields(
        self, *subfields: SpectroscopyConfigOptionFlamingos2GraphQLField
    ) -> "SpectroscopyConfigOptionFlamingos2Fields":
        """Subfields should come from the SpectroscopyConfigOptionFlamingos2Fields class"""
        self._subfields.extend(subfields)
        return self

    def alias(self, alias: str) -> "SpectroscopyConfigOptionFlamingos2Fields":
        self._alias = alias
        return self


class SpectroscopyConfigOptionGhostFields(GraphQLField):
    resolution_mode: "SpectroscopyConfigOptionGhostGraphQLField" = (
        SpectroscopyConfigOptionGhostGraphQLField("resolutionMode")
    )
    binning: "SpectroscopyConfigOptionGhostGraphQLField" = (
        SpectroscopyConfigOptionGhostGraphQLField("binning")
    )

    def fields(
        self, *subfields: SpectroscopyConfigOptionGhostGraphQLField
    ) -> "SpectroscopyConfigOptionGhostFields":
        """Subfields should come from the SpectroscopyConfigOptionGhostFields class"""
        self._subfields.extend(subfields)
        return self

    def alias(self, alias: str) -> "SpectroscopyConfigOptionGhostFields":
        self._alias = alias
        return self


class SpectroscopyConfigOptionGmosNorthFields(GraphQLField):
    fpu: "SpectroscopyConfigOptionGmosNorthGraphQLField" = (
        SpectroscopyConfigOptionGmosNorthGraphQLField("fpu")
    )
    grating: "SpectroscopyConfigOptionGmosNorthGraphQLField" = (
        SpectroscopyConfigOptionGmosNorthGraphQLField("grating")
    )
    filter_: "SpectroscopyConfigOptionGmosNorthGraphQLField" = (
        SpectroscopyConfigOptionGmosNorthGraphQLField("filter")
    )

    def fields(
        self, *subfields: SpectroscopyConfigOptionGmosNorthGraphQLField
    ) -> "SpectroscopyConfigOptionGmosNorthFields":
        """Subfields should come from the SpectroscopyConfigOptionGmosNorthFields class"""
        self._subfields.extend(subfields)
        return self

    def alias(self, alias: str) -> "SpectroscopyConfigOptionGmosNorthFields":
        self._alias = alias
        return self


class SpectroscopyConfigOptionGmosSouthFields(GraphQLField):
    fpu: "SpectroscopyConfigOptionGmosSouthGraphQLField" = (
        SpectroscopyConfigOptionGmosSouthGraphQLField("fpu")
    )
    grating: "SpectroscopyConfigOptionGmosSouthGraphQLField" = (
        SpectroscopyConfigOptionGmosSouthGraphQLField("grating")
    )
    filter_: "SpectroscopyConfigOptionGmosSouthGraphQLField" = (
        SpectroscopyConfigOptionGmosSouthGraphQLField("filter")
    )

    def fields(
        self, *subfields: SpectroscopyConfigOptionGmosSouthGraphQLField
    ) -> "SpectroscopyConfigOptionGmosSouthFields":
        """Subfields should come from the SpectroscopyConfigOptionGmosSouthFields class"""
        self._subfields.extend(subfields)
        return self

    def alias(self, alias: str) -> "SpectroscopyConfigOptionGmosSouthFields":
        self._alias = alias
        return self


class SpectroscopyConfigOptionGnirsFields(GraphQLField):
    grating: "SpectroscopyConfigOptionGnirsGraphQLField" = (
        SpectroscopyConfigOptionGnirsGraphQLField("grating")
    )
    filter_: "SpectroscopyConfigOptionGnirsGraphQLField" = (
        SpectroscopyConfigOptionGnirsGraphQLField("filter")
    )
    fpu_slit: "SpectroscopyConfigOptionGnirsGraphQLField" = (
        SpectroscopyConfigOptionGnirsGraphQLField("fpuSlit")
    )
    fpu_ifu: "SpectroscopyConfigOptionGnirsGraphQLField" = (
        SpectroscopyConfigOptionGnirsGraphQLField("fpuIfu")
    )
    prism: "SpectroscopyConfigOptionGnirsGraphQLField" = (
        SpectroscopyConfigOptionGnirsGraphQLField("prism")
    )
    camera: "SpectroscopyConfigOptionGnirsGraphQLField" = (
        SpectroscopyConfigOptionGnirsGraphQLField("camera")
    )

    def fields(
        self, *subfields: SpectroscopyConfigOptionGnirsGraphQLField
    ) -> "SpectroscopyConfigOptionGnirsFields":
        """Subfields should come from the SpectroscopyConfigOptionGnirsFields class"""
        self._subfields.extend(subfields)
        return self

    def alias(self, alias: str) -> "SpectroscopyConfigOptionGnirsFields":
        self._alias = alias
        return self


class SpectroscopyScienceRequirementsFields(GraphQLField):
    @classmethod
    def wavelength(cls) -> "WavelengthFields":
        return WavelengthFields("wavelength")

    resolution: "SpectroscopyScienceRequirementsGraphQLField" = (
        SpectroscopyScienceRequirementsGraphQLField("resolution")
    )

    @classmethod
    def wavelength_coverage(cls) -> "WavelengthFields":
        return WavelengthFields("wavelengthCoverage")

    focal_plane: "SpectroscopyScienceRequirementsGraphQLField" = (
        SpectroscopyScienceRequirementsGraphQLField("focalPlane")
    )

    @classmethod
    def focal_plane_angle(cls) -> "AngleFields":
        return AngleFields("focalPlaneAngle")

    capability: "SpectroscopyScienceRequirementsGraphQLField" = (
        SpectroscopyScienceRequirementsGraphQLField("capability")
    )

    def fields(
        self,
        *subfields: Union[
            SpectroscopyScienceRequirementsGraphQLField,
            "AngleFields",
            "WavelengthFields",
        ],
    ) -> "SpectroscopyScienceRequirementsFields":
        """Subfields should come from the SpectroscopyScienceRequirementsFields class"""
        self._subfields.extend(subfields)
        return self

    def alias(self, alias: str) -> "SpectroscopyScienceRequirementsFields":
        self._alias = alias
        return self


class SpiralTelescopeConfigGeneratorFields(GraphQLField):
    @classmethod
    def size(cls) -> "AngleFields":
        return AngleFields("size")

    @classmethod
    def center(cls) -> "OffsetFields":
        return OffsetFields("center")

    seed: "SpiralTelescopeConfigGeneratorGraphQLField" = (
        SpiralTelescopeConfigGeneratorGraphQLField("seed")
    )

    def fields(
        self,
        *subfields: Union[
            SpiralTelescopeConfigGeneratorGraphQLField, "AngleFields", "OffsetFields"
        ],
    ) -> "SpiralTelescopeConfigGeneratorFields":
        """Subfields should come from the SpiralTelescopeConfigGeneratorFields class"""
        self._subfields.extend(subfields)
        return self

    def alias(self, alias: str) -> "SpiralTelescopeConfigGeneratorFields":
        self._alias = alias
        return self


class StepConfigInterface(GraphQLField):
    step_type: "StepConfigGraphQLField" = StepConfigGraphQLField("stepType")

    def fields(self, *subfields: StepConfigGraphQLField) -> "StepConfigInterface":
        """Subfields should come from the StepConfigInterface class"""
        self._subfields.extend(subfields)
        return self

    def alias(self, alias: str) -> "StepConfigInterface":
        self._alias = alias
        return self

    def on(self, type_name: str, *subfields: GraphQLField) -> "StepConfigInterface":
        self._inline_fragments[type_name] = subfields
        return self


class StepEstimateFields(GraphQLField):
    @classmethod
    def config_change(cls) -> "AllConfigChangeEstimatesFields":
        return AllConfigChangeEstimatesFields("configChange")

    @classmethod
    def detector(cls) -> "AllDetectorEstimatesFields":
        return AllDetectorEstimatesFields("detector")

    @classmethod
    def total(cls) -> "TimeSpanFields":
        return TimeSpanFields("total")

    def fields(
        self,
        *subfields: Union[
            StepEstimateGraphQLField,
            "AllConfigChangeEstimatesFields",
            "AllDetectorEstimatesFields",
            "TimeSpanFields",
        ],
    ) -> "StepEstimateFields":
        """Subfields should come from the StepEstimateFields class"""
        self._subfields.extend(subfields)
        return self

    def alias(self, alias: str) -> "StepEstimateFields":
        self._alias = alias
        return self


class StepEventFields(GraphQLField):
    id: "StepEventGraphQLField" = StepEventGraphQLField("id")

    @classmethod
    def visit(cls) -> "VisitFields":
        return VisitFields("visit")

    @classmethod
    def observation(cls) -> "ObservationFields":
        return ObservationFields("observation")

    recorded_time: "StepEventGraphQLField" = StepEventGraphQLField("recordedTime")
    received: "StepEventGraphQLField" = StepEventGraphQLField("received")
    client_time: "StepEventGraphQLField" = StepEventGraphQLField("clientTime")
    effective_time: "StepEventGraphQLField" = StepEventGraphQLField("effectiveTime")
    event_type: "StepEventGraphQLField" = StepEventGraphQLField("eventType")

    @classmethod
    def atom(cls) -> "AtomRecordFields":
        return AtomRecordFields("atom")

    @classmethod
    def step(cls) -> "StepRecordFields":
        return StepRecordFields("step")

    step_stage: "StepEventGraphQLField" = StepEventGraphQLField("stepStage")
    idempotency_key: "StepEventGraphQLField" = StepEventGraphQLField("idempotencyKey")

    def fields(
        self,
        *subfields: Union[
            StepEventGraphQLField,
            "AtomRecordFields",
            "ObservationFields",
            "StepRecordFields",
            "VisitFields",
        ],
    ) -> "StepEventFields":
        """Subfields should come from the StepEventFields class"""
        self._subfields.extend(subfields)
        return self

    def alias(self, alias: str) -> "StepEventFields":
        self._alias = alias
        return self


class StepRecordFields(GraphQLField):
    id: "StepRecordGraphQLField" = StepRecordGraphQLField("id")
    index: "StepRecordGraphQLField" = StepRecordGraphQLField("index")
    instrument: "StepRecordGraphQLField" = StepRecordGraphQLField("instrument")

    @classmethod
    def atom(cls) -> "AtomRecordFields":
        return AtomRecordFields("atom")

    execution_state: "StepRecordGraphQLField" = StepRecordGraphQLField("executionState")

    @classmethod
    def interval(cls) -> "TimestampIntervalFields":
        return TimestampIntervalFields("interval")

    @classmethod
    def step_config(cls) -> "StepConfigInterface":
        return StepConfigInterface("stepConfig")

    @classmethod
    def telescope_config(cls) -> "TelescopeConfigFields":
        return TelescopeConfigFields("telescopeConfig")

    observe_class: "StepRecordGraphQLField" = StepRecordGraphQLField("observeClass")

    @classmethod
    def estimate(cls) -> "TimeSpanFields":
        return TimeSpanFields("estimate")

    qa_state: "StepRecordGraphQLField" = StepRecordGraphQLField("qaState")

    @classmethod
    def datasets(
        cls, *, offset: Optional[Any] = None, limit: Optional[Any] = None
    ) -> "DatasetSelectResultFields":
        arguments: dict[str, dict[str, Any]] = {
            "OFFSET": {"type": "DatasetId", "value": offset},
            "LIMIT": {"type": "NonNegInt", "value": limit},
        }
        cleared_arguments = {
            key: value for key, value in arguments.items() if value["value"] is not None
        }
        return DatasetSelectResultFields("datasets", arguments=cleared_arguments)

    @classmethod
    def events(
        cls, *, offset: Optional[Any] = None, limit: Optional[Any] = None
    ) -> "ExecutionEventSelectResultFields":
        arguments: dict[str, dict[str, Any]] = {
            "OFFSET": {"type": "ExecutionEventId", "value": offset},
            "LIMIT": {"type": "NonNegInt", "value": limit},
        }
        cleared_arguments = {
            key: value for key, value in arguments.items() if value["value"] is not None
        }
        return ExecutionEventSelectResultFields("events", arguments=cleared_arguments)

    @classmethod
    def flamingos_2(cls) -> "Flamingos2DynamicFields":
        return Flamingos2DynamicFields("flamingos2")

    @classmethod
    def ghost(cls) -> "GhostDynamicFields":
        return GhostDynamicFields("ghost")

    @classmethod
    def gmos_north(cls) -> "GmosNorthDynamicFields":
        return GmosNorthDynamicFields("gmosNorth")

    @classmethod
    def gmos_south(cls) -> "GmosSouthDynamicFields":
        return GmosSouthDynamicFields("gmosSouth")

    @classmethod
    def igrins_2(cls) -> "Igrins2DynamicFields":
        return Igrins2DynamicFields("igrins2")

    @classmethod
    def gnirs(cls) -> "GnirsDynamicFields":
        return GnirsDynamicFields("gnirs")

    def fields(
        self,
        *subfields: Union[
            StepRecordGraphQLField,
            "AtomRecordFields",
            "DatasetSelectResultFields",
            "ExecutionEventSelectResultFields",
            "Flamingos2DynamicFields",
            "GhostDynamicFields",
            "GmosNorthDynamicFields",
            "GmosSouthDynamicFields",
            "GnirsDynamicFields",
            "Igrins2DynamicFields",
            "StepConfigInterface",
            "TelescopeConfigFields",
            "TimeSpanFields",
            "TimestampIntervalFields",
        ],
    ) -> "StepRecordFields":
        """Subfields should come from the StepRecordFields class"""
        self._subfields.extend(subfields)
        return self

    def alias(self, alias: str) -> "StepRecordFields":
        self._alias = alias
        return self


class StepRecordSelectResultFields(GraphQLField):
    @classmethod
    def matches(cls) -> "StepRecordFields":
        return StepRecordFields("matches")

    has_more: "StepRecordSelectResultGraphQLField" = StepRecordSelectResultGraphQLField(
        "hasMore"
    )

    def fields(
        self, *subfields: Union[StepRecordSelectResultGraphQLField, "StepRecordFields"]
    ) -> "StepRecordSelectResultFields":
        """Subfields should come from the StepRecordSelectResultFields class"""
        self._subfields.extend(subfields)
        return self

    def alias(self, alias: str) -> "StepRecordSelectResultFields":
        self._alias = alias
        return self


class SubaruCallPropertiesFields(GraphQLField):
    type_: "SubaruCallPropertiesGraphQLField" = SubaruCallPropertiesGraphQLField("type")
    instruments: "SubaruCallPropertiesGraphQLField" = SubaruCallPropertiesGraphQLField(
        "instruments"
    )

    @classmethod
    def coordinate_limits(cls) -> "CoordinateLimitsFields":
        return CoordinateLimitsFields("coordinateLimits")

    def fields(
        self,
        *subfields: Union[SubaruCallPropertiesGraphQLField, "CoordinateLimitsFields"],
    ) -> "SubaruCallPropertiesFields":
        """Subfields should come from the SubaruCallPropertiesFields class"""
        self._subfields.extend(subfields)
        return self

    def alias(self, alias: str) -> "SubaruCallPropertiesFields":
        self._alias = alias
        return self


class SubaruProgramReferenceFields(GraphQLField):
    label: "SubaruProgramReferenceGraphQLField" = SubaruProgramReferenceGraphQLField(
        "label"
    )
    type_: "SubaruProgramReferenceGraphQLField" = SubaruProgramReferenceGraphQLField(
        "type"
    )
    semester: "SubaruProgramReferenceGraphQLField" = SubaruProgramReferenceGraphQLField(
        "semester"
    )
    semester_index: "SubaruProgramReferenceGraphQLField" = (
        SubaruProgramReferenceGraphQLField("semesterIndex")
    )
    subaru_type: "SubaruProgramReferenceGraphQLField" = (
        SubaruProgramReferenceGraphQLField("subaruType")
    )

    def fields(
        self, *subfields: SubaruProgramReferenceGraphQLField
    ) -> "SubaruProgramReferenceFields":
        """Subfields should come from the SubaruProgramReferenceFields class"""
        self._subfields.extend(subfields)
        return self

    def alias(self, alias: str) -> "SubaruProgramReferenceFields":
        self._alias = alias
        return self


class SubaruProposalTypeFields(GraphQLField):
    min_percent_time: "SubaruProposalTypeGraphQLField" = SubaruProposalTypeGraphQLField(
        "minPercentTime"
    )

    @classmethod
    def partner_splits(cls) -> "PartnerSplitFields":
        return PartnerSplitFields("partnerSplits")

    def fields(
        self, *subfields: Union[SubaruProposalTypeGraphQLField, "PartnerSplitFields"]
    ) -> "SubaruProposalTypeFields":
        """Subfields should come from the SubaruProposalTypeFields class"""
        self._subfields.extend(subfields)
        return self

    def alias(self, alias: str) -> "SubaruProposalTypeFields":
        self._alias = alias
        return self


class SystemProgramReferenceFields(GraphQLField):
    label: "SystemProgramReferenceGraphQLField" = SystemProgramReferenceGraphQLField(
        "label"
    )
    type_: "SystemProgramReferenceGraphQLField" = SystemProgramReferenceGraphQLField(
        "type"
    )

    def fields(
        self, *subfields: SystemProgramReferenceGraphQLField
    ) -> "SystemProgramReferenceFields":
        """Subfields should come from the SystemProgramReferenceFields class"""
        self._subfields.extend(subfields)
        return self

    def alias(self, alias: str) -> "SystemProgramReferenceFields":
        self._alias = alias
        return self


class SystemVerificationFields(GraphQLField):
    science_subtype: "SystemVerificationGraphQLField" = SystemVerificationGraphQLField(
        "scienceSubtype"
    )
    too_activation_ceiling: "SystemVerificationGraphQLField" = (
        SystemVerificationGraphQLField("tooActivationCeiling")
    )
    default_too_activation_ceiling: "SystemVerificationGraphQLField" = (
        SystemVerificationGraphQLField("defaultTooActivationCeiling")
    )
    explicit_too_activation_ceiling: "SystemVerificationGraphQLField" = (
        SystemVerificationGraphQLField("explicitTooActivationCeiling")
    )
    min_percent_time: "SystemVerificationGraphQLField" = SystemVerificationGraphQLField(
        "minPercentTime"
    )

    def fields(
        self, *subfields: SystemVerificationGraphQLField
    ) -> "SystemVerificationFields":
        """Subfields should come from the SystemVerificationFields class"""
        self._subfields.extend(subfields)
        return self

    def alias(self, alias: str) -> "SystemVerificationFields":
        self._alias = alias
        return self


class TargetFields(GraphQLField):
    id: "TargetGraphQLField" = TargetGraphQLField("id")
    existence: "TargetGraphQLField" = TargetGraphQLField("existence")

    @classmethod
    def program(cls, include_deleted: bool) -> "ProgramFields":
        arguments: dict[str, dict[str, Any]] = {
            "includeDeleted": {"type": "Boolean!", "value": include_deleted}
        }
        cleared_arguments = {
            key: value for key, value in arguments.items() if value["value"] is not None
        }
        return ProgramFields("program", arguments=cleared_arguments)

    name: "TargetGraphQLField" = TargetGraphQLField("name")
    disposition: "TargetGraphQLField" = TargetGraphQLField("disposition")
    calibration_role: "TargetGraphQLField" = TargetGraphQLField("calibrationRole")

    @classmethod
    def source_profile(cls) -> "SourceProfileFields":
        return SourceProfileFields("sourceProfile")

    @classmethod
    def sidereal(cls) -> "SiderealFields":
        return SiderealFields("sidereal")

    @classmethod
    def nonsidereal(cls) -> "NonsiderealFields":
        return NonsiderealFields("nonsidereal")

    @classmethod
    def opportunity(cls) -> "OpportunityFields":
        return OpportunityFields("opportunity")

    def fields(
        self,
        *subfields: Union[
            TargetGraphQLField,
            "NonsiderealFields",
            "OpportunityFields",
            "ProgramFields",
            "SiderealFields",
            "SourceProfileFields",
        ],
    ) -> "TargetFields":
        """Subfields should come from the TargetFields class"""
        self._subfields.extend(subfields)
        return self

    def alias(self, alias: str) -> "TargetFields":
        self._alias = alias
        return self


class TargetEnvironmentFields(GraphQLField):
    @classmethod
    def asterism(cls, include_deleted: bool) -> "TargetFields":
        arguments: dict[str, dict[str, Any]] = {
            "includeDeleted": {"type": "Boolean!", "value": include_deleted}
        }
        cleared_arguments = {
            key: value for key, value in arguments.items() if value["value"] is not None
        }
        return TargetFields("asterism", arguments=cleared_arguments)

    @classmethod
    def first_science_target(cls, include_deleted: bool) -> "TargetFields":
        arguments: dict[str, dict[str, Any]] = {
            "includeDeleted": {"type": "Boolean!", "value": include_deleted}
        }
        cleared_arguments = {
            key: value for key, value in arguments.items() if value["value"] is not None
        }
        return TargetFields("firstScienceTarget", arguments=cleared_arguments)

    @classmethod
    def explicit_signal_to_noise_target(cls) -> "TargetFields":
        return TargetFields("explicitSignalToNoiseTarget")

    @classmethod
    def base_position(cls) -> "BasePositionFields":
        return BasePositionFields("basePosition")

    @classmethod
    def guide_environment(cls) -> "GuideEnvironmentFields":
        return GuideEnvironmentFields("guideEnvironment")

    @classmethod
    def guide_availability(
        cls, start: Any, end: Any
    ) -> "GuideAvailabilityPeriodFields":
        arguments: dict[str, dict[str, Any]] = {
            "start": {"type": "Timestamp!", "value": start},
            "end": {"type": "Timestamp!", "value": end},
        }
        cleared_arguments = {
            key: value for key, value in arguments.items() if value["value"] is not None
        }
        return GuideAvailabilityPeriodFields(
            "guideAvailability", arguments=cleared_arguments
        )

    @classmethod
    def explicit_base(cls) -> "CoordinatesFields":
        return CoordinatesFields("explicitBase")

    guide_target_name: "TargetEnvironmentGraphQLField" = TargetEnvironmentGraphQLField(
        "guideTargetName"
    )
    use_blind_offset: "TargetEnvironmentGraphQLField" = TargetEnvironmentGraphQLField(
        "useBlindOffset"
    )

    @classmethod
    def blind_offset_target(cls) -> "TargetFields":
        return TargetFields("blindOffsetTarget")

    blind_offset_type: "TargetEnvironmentGraphQLField" = TargetEnvironmentGraphQLField(
        "blindOffsetType"
    )
    cass_rotator: "TargetEnvironmentGraphQLField" = TargetEnvironmentGraphQLField(
        "cassRotator"
    )

    def fields(
        self,
        *subfields: Union[
            TargetEnvironmentGraphQLField,
            "BasePositionFields",
            "CoordinatesFields",
            "GuideAvailabilityPeriodFields",
            "GuideEnvironmentFields",
            "TargetFields",
        ],
    ) -> "TargetEnvironmentFields":
        """Subfields should come from the TargetEnvironmentFields class"""
        self._subfields.extend(subfields)
        return self

    def alias(self, alias: str) -> "TargetEnvironmentFields":
        self._alias = alias
        return self


class TargetGroupFields(GraphQLField):
    @classmethod
    def observations(
        cls,
        include_deleted: bool,
        *,
        offset: Optional[Any] = None,
        limit: Optional[Any] = None,
    ) -> "ObservationSelectResultFields":
        arguments: dict[str, dict[str, Any]] = {
            "includeDeleted": {"type": "Boolean!", "value": include_deleted},
            "OFFSET": {"type": "ObservationId", "value": offset},
            "LIMIT": {"type": "NonNegInt", "value": limit},
        }
        cleared_arguments = {
            key: value for key, value in arguments.items() if value["value"] is not None
        }
        return ObservationSelectResultFields(
            "observations", arguments=cleared_arguments
        )

    @classmethod
    def target(cls) -> "TargetFields":
        return TargetFields("target")

    @classmethod
    def program(cls) -> "ProgramFields":
        return ProgramFields("program")

    def fields(
        self,
        *subfields: Union[
            TargetGroupGraphQLField,
            "ObservationSelectResultFields",
            "ProgramFields",
            "TargetFields",
        ],
    ) -> "TargetGroupFields":
        """Subfields should come from the TargetGroupFields class"""
        self._subfields.extend(subfields)
        return self

    def alias(self, alias: str) -> "TargetGroupFields":
        self._alias = alias
        return self


class TargetGroupSelectResultFields(GraphQLField):
    @classmethod
    def matches(cls) -> "TargetGroupFields":
        return TargetGroupFields("matches")

    has_more: "TargetGroupSelectResultGraphQLField" = (
        TargetGroupSelectResultGraphQLField("hasMore")
    )

    def fields(
        self,
        *subfields: Union[TargetGroupSelectResultGraphQLField, "TargetGroupFields"],
    ) -> "TargetGroupSelectResultFields":
        """Subfields should come from the TargetGroupSelectResultFields class"""
        self._subfields.extend(subfields)
        return self

    def alias(self, alias: str) -> "TargetGroupSelectResultFields":
        self._alias = alias
        return self


class TargetSelectResultFields(GraphQLField):
    @classmethod
    def matches(cls) -> "TargetFields":
        return TargetFields("matches")

    has_more: "TargetSelectResultGraphQLField" = TargetSelectResultGraphQLField(
        "hasMore"
    )

    def fields(
        self, *subfields: Union[TargetSelectResultGraphQLField, "TargetFields"]
    ) -> "TargetSelectResultFields":
        """Subfields should come from the TargetSelectResultFields class"""
        self._subfields.extend(subfields)
        return self

    def alias(self, alias: str) -> "TargetSelectResultFields":
        self._alias = alias
        return self


class TelescopeConfigFields(GraphQLField):
    @classmethod
    def offset(cls) -> "OffsetFields":
        return OffsetFields("offset")

    guiding: "TelescopeConfigGraphQLField" = TelescopeConfigGraphQLField("guiding")

    def fields(
        self, *subfields: Union[TelescopeConfigGraphQLField, "OffsetFields"]
    ) -> "TelescopeConfigFields":
        """Subfields should come from the TelescopeConfigFields class"""
        self._subfields.extend(subfields)
        return self

    def alias(self, alias: str) -> "TelescopeConfigFields":
        self._alias = alias
        return self


class TelescopeConfigAlongSlitFields(GraphQLField):
    @classmethod
    def q(cls) -> "OffsetQFields":
        return OffsetQFields("q")

    guiding: "TelescopeConfigAlongSlitGraphQLField" = (
        TelescopeConfigAlongSlitGraphQLField("guiding")
    )

    def fields(
        self, *subfields: Union[TelescopeConfigAlongSlitGraphQLField, "OffsetQFields"]
    ) -> "TelescopeConfigAlongSlitFields":
        """Subfields should come from the TelescopeConfigAlongSlitFields class"""
        self._subfields.extend(subfields)
        return self

    def alias(self, alias: str) -> "TelescopeConfigAlongSlitFields":
        self._alias = alias
        return self


class TelescopeConfigGeneratorFields(GraphQLField):
    generator_type: "TelescopeConfigGeneratorGraphQLField" = (
        TelescopeConfigGeneratorGraphQLField("generatorType")
    )

    @classmethod
    def enumerated(cls) -> "EnumeratedTelescopeConfigGeneratorFields":
        return EnumeratedTelescopeConfigGeneratorFields("enumerated")

    @classmethod
    def random(cls) -> "RandomTelescopeConfigGeneratorFields":
        return RandomTelescopeConfigGeneratorFields("random")

    @classmethod
    def spiral(cls) -> "SpiralTelescopeConfigGeneratorFields":
        return SpiralTelescopeConfigGeneratorFields("spiral")

    @classmethod
    def uniform(cls) -> "UniformTelescopeConfigGeneratorFields":
        return UniformTelescopeConfigGeneratorFields("uniform")

    def fields(
        self,
        *subfields: Union[
            TelescopeConfigGeneratorGraphQLField,
            "EnumeratedTelescopeConfigGeneratorFields",
            "RandomTelescopeConfigGeneratorFields",
            "SpiralTelescopeConfigGeneratorFields",
            "UniformTelescopeConfigGeneratorFields",
        ],
    ) -> "TelescopeConfigGeneratorFields":
        """Subfields should come from the TelescopeConfigGeneratorFields class"""
        self._subfields.extend(subfields)
        return self

    def alias(self, alias: str) -> "TelescopeConfigGeneratorFields":
        self._alias = alias
        return self


class TelluricTypeFields(GraphQLField):
    tag: "TelluricTypeGraphQLField" = TelluricTypeGraphQLField("tag")
    star_types: "TelluricTypeGraphQLField" = TelluricTypeGraphQLField("starTypes")

    def fields(self, *subfields: TelluricTypeGraphQLField) -> "TelluricTypeFields":
        """Subfields should come from the TelluricTypeFields class"""
        self._subfields.extend(subfields)
        return self

    def alias(self, alias: str) -> "TelluricTypeFields":
        self._alias = alias
        return self


class TimeAndCountExposureTimeModeFields(GraphQLField):
    @classmethod
    def time(cls) -> "TimeSpanFields":
        return TimeSpanFields("time")

    count: "TimeAndCountExposureTimeModeGraphQLField" = (
        TimeAndCountExposureTimeModeGraphQLField("count")
    )

    @classmethod
    def at(cls) -> "WavelengthFields":
        return WavelengthFields("at")

    def fields(
        self,
        *subfields: Union[
            TimeAndCountExposureTimeModeGraphQLField,
            "TimeSpanFields",
            "WavelengthFields",
        ],
    ) -> "TimeAndCountExposureTimeModeFields":
        """Subfields should come from the TimeAndCountExposureTimeModeFields class"""
        self._subfields.extend(subfields)
        return self

    def alias(self, alias: str) -> "TimeAndCountExposureTimeModeFields":
        self._alias = alias
        return self


class TimeChargeCorrectionFields(GraphQLField):
    created: "TimeChargeCorrectionGraphQLField" = TimeChargeCorrectionGraphQLField(
        "created"
    )
    charge_class: "TimeChargeCorrectionGraphQLField" = TimeChargeCorrectionGraphQLField(
        "chargeClass"
    )
    op: "TimeChargeCorrectionGraphQLField" = TimeChargeCorrectionGraphQLField("op")

    @classmethod
    def amount(cls) -> "TimeSpanFields":
        return TimeSpanFields("amount")

    @classmethod
    def user(cls) -> "UserFields":
        return UserFields("user")

    comment: "TimeChargeCorrectionGraphQLField" = TimeChargeCorrectionGraphQLField(
        "comment"
    )

    def fields(
        self,
        *subfields: Union[
            TimeChargeCorrectionGraphQLField, "TimeSpanFields", "UserFields"
        ],
    ) -> "TimeChargeCorrectionFields":
        """Subfields should come from the TimeChargeCorrectionFields class"""
        self._subfields.extend(subfields)
        return self

    def alias(self, alias: str) -> "TimeChargeCorrectionFields":
        self._alias = alias
        return self


class TimeChargeDaylightDiscountFields(GraphQLField):
    @classmethod
    def interval(cls) -> "TimestampIntervalFields":
        return TimestampIntervalFields("interval")

    @classmethod
    def amount(cls) -> "TimeSpanFields":
        return TimeSpanFields("amount")

    comment: "TimeChargeDaylightDiscountGraphQLField" = (
        TimeChargeDaylightDiscountGraphQLField("comment")
    )
    site: "TimeChargeDaylightDiscountGraphQLField" = (
        TimeChargeDaylightDiscountGraphQLField("site")
    )

    def fields(
        self,
        *subfields: Union[
            TimeChargeDaylightDiscountGraphQLField,
            "TimeSpanFields",
            "TimestampIntervalFields",
        ],
    ) -> "TimeChargeDaylightDiscountFields":
        """Subfields should come from the TimeChargeDaylightDiscountFields class"""
        self._subfields.extend(subfields)
        return self

    def alias(self, alias: str) -> "TimeChargeDaylightDiscountFields":
        self._alias = alias
        return self


class TimeChargeDiscountInterface(GraphQLField):
    @classmethod
    def interval(cls) -> "TimestampIntervalFields":
        return TimestampIntervalFields("interval")

    @classmethod
    def amount(cls) -> "TimeSpanFields":
        return TimeSpanFields("amount")

    comment: "TimeChargeDiscountGraphQLField" = TimeChargeDiscountGraphQLField(
        "comment"
    )

    def fields(
        self,
        *subfields: Union[
            TimeChargeDiscountGraphQLField, "TimeSpanFields", "TimestampIntervalFields"
        ],
    ) -> "TimeChargeDiscountInterface":
        """Subfields should come from the TimeChargeDiscountInterface class"""
        self._subfields.extend(subfields)
        return self

    def alias(self, alias: str) -> "TimeChargeDiscountInterface":
        self._alias = alias
        return self

    def on(
        self, type_name: str, *subfields: GraphQLField
    ) -> "TimeChargeDiscountInterface":
        self._inline_fragments[type_name] = subfields
        return self


class TimeChargeInvoiceFields(GraphQLField):
    @classmethod
    def execution_time(cls) -> "CategorizedTimeFields":
        return CategorizedTimeFields("executionTime")

    @classmethod
    def discounts(cls) -> "TimeChargeDiscountInterface":
        return TimeChargeDiscountInterface("discounts")

    @classmethod
    def corrections(cls) -> "TimeChargeCorrectionFields":
        return TimeChargeCorrectionFields("corrections")

    @classmethod
    def final_charge(cls) -> "CategorizedTimeFields":
        return CategorizedTimeFields("finalCharge")

    def fields(
        self,
        *subfields: Union[
            TimeChargeInvoiceGraphQLField,
            "CategorizedTimeFields",
            "TimeChargeCorrectionFields",
            "TimeChargeDiscountInterface",
        ],
    ) -> "TimeChargeInvoiceFields":
        """Subfields should come from the TimeChargeInvoiceFields class"""
        self._subfields.extend(subfields)
        return self

    def alias(self, alias: str) -> "TimeChargeInvoiceFields":
        self._alias = alias
        return self


class TimeChargeNoDataDiscountFields(GraphQLField):
    @classmethod
    def interval(cls) -> "TimestampIntervalFields":
        return TimestampIntervalFields("interval")

    @classmethod
    def amount(cls) -> "TimeSpanFields":
        return TimeSpanFields("amount")

    comment: "TimeChargeNoDataDiscountGraphQLField" = (
        TimeChargeNoDataDiscountGraphQLField("comment")
    )

    def fields(
        self,
        *subfields: Union[
            TimeChargeNoDataDiscountGraphQLField,
            "TimeSpanFields",
            "TimestampIntervalFields",
        ],
    ) -> "TimeChargeNoDataDiscountFields":
        """Subfields should come from the TimeChargeNoDataDiscountFields class"""
        self._subfields.extend(subfields)
        return self

    def alias(self, alias: str) -> "TimeChargeNoDataDiscountFields":
        self._alias = alias
        return self


class TimeChargeOverlapDiscountFields(GraphQLField):
    @classmethod
    def interval(cls) -> "TimestampIntervalFields":
        return TimestampIntervalFields("interval")

    @classmethod
    def amount(cls) -> "TimeSpanFields":
        return TimeSpanFields("amount")

    comment: "TimeChargeOverlapDiscountGraphQLField" = (
        TimeChargeOverlapDiscountGraphQLField("comment")
    )

    @classmethod
    def observation(cls) -> "ObservationFields":
        return ObservationFields("observation")

    def fields(
        self,
        *subfields: Union[
            TimeChargeOverlapDiscountGraphQLField,
            "ObservationFields",
            "TimeSpanFields",
            "TimestampIntervalFields",
        ],
    ) -> "TimeChargeOverlapDiscountFields":
        """Subfields should come from the TimeChargeOverlapDiscountFields class"""
        self._subfields.extend(subfields)
        return self

    def alias(self, alias: str) -> "TimeChargeOverlapDiscountFields":
        self._alias = alias
        return self


class TimeChargeQaDiscountFields(GraphQLField):
    @classmethod
    def interval(cls) -> "TimestampIntervalFields":
        return TimestampIntervalFields("interval")

    @classmethod
    def amount(cls) -> "TimeSpanFields":
        return TimeSpanFields("amount")

    comment: "TimeChargeQaDiscountGraphQLField" = TimeChargeQaDiscountGraphQLField(
        "comment"
    )

    @classmethod
    def datasets(cls) -> "DatasetFields":
        return DatasetFields("datasets")

    def fields(
        self,
        *subfields: Union[
            TimeChargeQaDiscountGraphQLField,
            "DatasetFields",
            "TimeSpanFields",
            "TimestampIntervalFields",
        ],
    ) -> "TimeChargeQaDiscountFields":
        """Subfields should come from the TimeChargeQaDiscountFields class"""
        self._subfields.extend(subfields)
        return self

    def alias(self, alias: str) -> "TimeChargeQaDiscountFields":
        self._alias = alias
        return self


class TimeSpanFields(GraphQLField):
    microseconds: "TimeSpanGraphQLField" = TimeSpanGraphQLField("microseconds")
    milliseconds: "TimeSpanGraphQLField" = TimeSpanGraphQLField("milliseconds")
    seconds: "TimeSpanGraphQLField" = TimeSpanGraphQLField("seconds")
    minutes: "TimeSpanGraphQLField" = TimeSpanGraphQLField("minutes")
    hours: "TimeSpanGraphQLField" = TimeSpanGraphQLField("hours")
    iso: "TimeSpanGraphQLField" = TimeSpanGraphQLField("iso")

    def fields(self, *subfields: TimeSpanGraphQLField) -> "TimeSpanFields":
        """Subfields should come from the TimeSpanFields class"""
        self._subfields.extend(subfields)
        return self

    def alias(self, alias: str) -> "TimeSpanFields":
        self._alias = alias
        return self


class TimestampIntervalFields(GraphQLField):
    start: "TimestampIntervalGraphQLField" = TimestampIntervalGraphQLField("start")
    end: "TimestampIntervalGraphQLField" = TimestampIntervalGraphQLField("end")

    @classmethod
    def duration(cls) -> "TimeSpanFields":
        return TimeSpanFields("duration")

    def fields(
        self, *subfields: Union[TimestampIntervalGraphQLField, "TimeSpanFields"]
    ) -> "TimestampIntervalFields":
        """Subfields should come from the TimestampIntervalFields class"""
        self._subfields.extend(subfields)
        return self

    def alias(self, alias: str) -> "TimestampIntervalFields":
        self._alias = alias
        return self


class TimingWindowFields(GraphQLField):
    inclusion: "TimingWindowGraphQLField" = TimingWindowGraphQLField("inclusion")
    start_utc: "TimingWindowGraphQLField" = TimingWindowGraphQLField("startUtc")
    end: "TimingWindowEndUnion" = TimingWindowEndUnion("end")

    def fields(
        self, *subfields: Union[TimingWindowGraphQLField, "TimingWindowEndUnion"]
    ) -> "TimingWindowFields":
        """Subfields should come from the TimingWindowFields class"""
        self._subfields.extend(subfields)
        return self

    def alias(self, alias: str) -> "TimingWindowFields":
        self._alias = alias
        return self


class TimingWindowEndAfterFields(GraphQLField):
    @classmethod
    def after(cls) -> "TimeSpanFields":
        return TimeSpanFields("after")

    @classmethod
    def repeat(cls) -> "TimingWindowRepeatFields":
        return TimingWindowRepeatFields("repeat")

    def fields(
        self,
        *subfields: Union[
            TimingWindowEndAfterGraphQLField,
            "TimeSpanFields",
            "TimingWindowRepeatFields",
        ],
    ) -> "TimingWindowEndAfterFields":
        """Subfields should come from the TimingWindowEndAfterFields class"""
        self._subfields.extend(subfields)
        return self

    def alias(self, alias: str) -> "TimingWindowEndAfterFields":
        self._alias = alias
        return self


class TimingWindowEndAtFields(GraphQLField):
    at_utc: "TimingWindowEndAtGraphQLField" = TimingWindowEndAtGraphQLField("atUtc")

    def fields(
        self, *subfields: TimingWindowEndAtGraphQLField
    ) -> "TimingWindowEndAtFields":
        """Subfields should come from the TimingWindowEndAtFields class"""
        self._subfields.extend(subfields)
        return self

    def alias(self, alias: str) -> "TimingWindowEndAtFields":
        self._alias = alias
        return self


class TimingWindowRepeatFields(GraphQLField):
    @classmethod
    def period(cls) -> "TimeSpanFields":
        return TimeSpanFields("period")

    times: "TimingWindowRepeatGraphQLField" = TimingWindowRepeatGraphQLField("times")

    def fields(
        self, *subfields: Union[TimingWindowRepeatGraphQLField, "TimeSpanFields"]
    ) -> "TimingWindowRepeatFields":
        """Subfields should come from the TimingWindowRepeatFields class"""
        self._subfields.extend(subfields)
        return self

    def alias(self, alias: str) -> "TimingWindowRepeatFields":
        self._alias = alias
        return self


class TooTriggerFields(GraphQLField):
    id: "TooTriggerGraphQLField" = TooTriggerGraphQLField("id")

    @classmethod
    def observation(cls) -> "ObservationFields":
        return ObservationFields("observation")

    status: "TooTriggerGraphQLField" = TooTriggerGraphQLField("status")
    resolution_reason: "TooTriggerGraphQLField" = TooTriggerGraphQLField(
        "resolutionReason"
    )
    requested_at: "TooTriggerGraphQLField" = TooTriggerGraphQLField("requestedAt")

    @classmethod
    def requested_by(cls) -> "UserFields":
        return UserFields("requestedBy")

    updated_at: "TooTriggerGraphQLField" = TooTriggerGraphQLField("updatedAt")

    def fields(
        self,
        *subfields: Union[TooTriggerGraphQLField, "ObservationFields", "UserFields"],
    ) -> "TooTriggerFields":
        """Subfields should come from the TooTriggerFields class"""
        self._subfields.extend(subfields)
        return self

    def alias(self, alias: str) -> "TooTriggerFields":
        self._alias = alias
        return self


class TooTriggerChronicleEntryFields(GraphQLField):
    id: "TooTriggerChronicleEntryGraphQLField" = TooTriggerChronicleEntryGraphQLField(
        "id"
    )
    transaction_id: "TooTriggerChronicleEntryGraphQLField" = (
        TooTriggerChronicleEntryGraphQLField("transactionId")
    )

    @classmethod
    def user(cls) -> "UserFields":
        return UserFields("user")

    timestamp: "TooTriggerChronicleEntryGraphQLField" = (
        TooTriggerChronicleEntryGraphQLField("timestamp")
    )
    operation: "TooTriggerChronicleEntryGraphQLField" = (
        TooTriggerChronicleEntryGraphQLField("operation")
    )

    @classmethod
    def too_trigger(cls) -> "TooTriggerFields":
        return TooTriggerFields("tooTrigger")

    mod_observation_id: "TooTriggerChronicleEntryGraphQLField" = (
        TooTriggerChronicleEntryGraphQLField("modObservationId")
    )
    mod_program_id: "TooTriggerChronicleEntryGraphQLField" = (
        TooTriggerChronicleEntryGraphQLField("modProgramId")
    )
    mod_status: "TooTriggerChronicleEntryGraphQLField" = (
        TooTriggerChronicleEntryGraphQLField("modStatus")
    )
    mod_resolution_reason: "TooTriggerChronicleEntryGraphQLField" = (
        TooTriggerChronicleEntryGraphQLField("modResolutionReason")
    )
    new_observation_id: "TooTriggerChronicleEntryGraphQLField" = (
        TooTriggerChronicleEntryGraphQLField("newObservationId")
    )
    new_program_id: "TooTriggerChronicleEntryGraphQLField" = (
        TooTriggerChronicleEntryGraphQLField("newProgramId")
    )
    new_status: "TooTriggerChronicleEntryGraphQLField" = (
        TooTriggerChronicleEntryGraphQLField("newStatus")
    )
    new_resolution_reason: "TooTriggerChronicleEntryGraphQLField" = (
        TooTriggerChronicleEntryGraphQLField("newResolutionReason")
    )

    def fields(
        self,
        *subfields: Union[
            TooTriggerChronicleEntryGraphQLField, "TooTriggerFields", "UserFields"
        ],
    ) -> "TooTriggerChronicleEntryFields":
        """Subfields should come from the TooTriggerChronicleEntryFields class"""
        self._subfields.extend(subfields)
        return self

    def alias(self, alias: str) -> "TooTriggerChronicleEntryFields":
        self._alias = alias
        return self


class TooTriggerChronicleEntrySelectResultFields(GraphQLField):
    @classmethod
    def matches(cls) -> "TooTriggerChronicleEntryFields":
        return TooTriggerChronicleEntryFields("matches")

    has_more: "TooTriggerChronicleEntrySelectResultGraphQLField" = (
        TooTriggerChronicleEntrySelectResultGraphQLField("hasMore")
    )

    def fields(
        self,
        *subfields: Union[
            TooTriggerChronicleEntrySelectResultGraphQLField,
            "TooTriggerChronicleEntryFields",
        ],
    ) -> "TooTriggerChronicleEntrySelectResultFields":
        """Subfields should come from the TooTriggerChronicleEntrySelectResultFields class"""
        self._subfields.extend(subfields)
        return self

    def alias(self, alias: str) -> "TooTriggerChronicleEntrySelectResultFields":
        self._alias = alias
        return self


class TooTriggerSelectResultFields(GraphQLField):
    @classmethod
    def matches(cls) -> "TooTriggerFields":
        return TooTriggerFields("matches")

    has_more: "TooTriggerSelectResultGraphQLField" = TooTriggerSelectResultGraphQLField(
        "hasMore"
    )

    def fields(
        self, *subfields: Union[TooTriggerSelectResultGraphQLField, "TooTriggerFields"]
    ) -> "TooTriggerSelectResultFields":
        """Subfields should come from the TooTriggerSelectResultFields class"""
        self._subfields.extend(subfields)
        return self

    def alias(self, alias: str) -> "TooTriggerSelectResultFields":
        self._alias = alias
        return self


class UniformTelescopeConfigGeneratorFields(GraphQLField):
    @classmethod
    def corner_a(cls) -> "OffsetFields":
        return OffsetFields("cornerA")

    @classmethod
    def corner_b(cls) -> "OffsetFields":
        return OffsetFields("cornerB")

    def fields(
        self,
        *subfields: Union[UniformTelescopeConfigGeneratorGraphQLField, "OffsetFields"],
    ) -> "UniformTelescopeConfigGeneratorFields":
        """Subfields should come from the UniformTelescopeConfigGeneratorFields class"""
        self._subfields.extend(subfields)
        return self

    def alias(self, alias: str) -> "UniformTelescopeConfigGeneratorFields":
        self._alias = alias
        return self


class UnlinkUserResultFields(GraphQLField):
    result: "UnlinkUserResultGraphQLField" = UnlinkUserResultGraphQLField("result")

    def fields(
        self, *subfields: UnlinkUserResultGraphQLField
    ) -> "UnlinkUserResultFields":
        """Subfields should come from the UnlinkUserResultFields class"""
        self._subfields.extend(subfields)
        return self

    def alias(self, alias: str) -> "UnlinkUserResultFields":
        self._alias = alias
        return self


class UnnormalizedSedFields(GraphQLField):
    stellar_library: "UnnormalizedSedGraphQLField" = UnnormalizedSedGraphQLField(
        "stellarLibrary"
    )
    cool_star: "UnnormalizedSedGraphQLField" = UnnormalizedSedGraphQLField("coolStar")
    galaxy: "UnnormalizedSedGraphQLField" = UnnormalizedSedGraphQLField("galaxy")
    planet: "UnnormalizedSedGraphQLField" = UnnormalizedSedGraphQLField("planet")
    quasar: "UnnormalizedSedGraphQLField" = UnnormalizedSedGraphQLField("quasar")
    hii_region: "UnnormalizedSedGraphQLField" = UnnormalizedSedGraphQLField("hiiRegion")
    planetary_nebula: "UnnormalizedSedGraphQLField" = UnnormalizedSedGraphQLField(
        "planetaryNebula"
    )
    power_law: "UnnormalizedSedGraphQLField" = UnnormalizedSedGraphQLField("powerLaw")
    black_body_temp_k: "UnnormalizedSedGraphQLField" = UnnormalizedSedGraphQLField(
        "blackBodyTempK"
    )

    @classmethod
    def flux_densities(cls) -> "FluxDensityEntryFields":
        return FluxDensityEntryFields("fluxDensities")

    flux_densities_attachment: "UnnormalizedSedGraphQLField" = (
        UnnormalizedSedGraphQLField("fluxDensitiesAttachment")
    )

    def fields(
        self, *subfields: Union[UnnormalizedSedGraphQLField, "FluxDensityEntryFields"]
    ) -> "UnnormalizedSedFields":
        """Subfields should come from the UnnormalizedSedFields class"""
        self._subfields.extend(subfields)
        return self

    def alias(self, alias: str) -> "UnnormalizedSedFields":
        self._alias = alias
        return self


class UpdateAsterismsResultFields(GraphQLField):
    @classmethod
    def observations(cls) -> "ObservationFields":
        return ObservationFields("observations")

    has_more: "UpdateAsterismsResultGraphQLField" = UpdateAsterismsResultGraphQLField(
        "hasMore"
    )

    def fields(
        self, *subfields: Union[UpdateAsterismsResultGraphQLField, "ObservationFields"]
    ) -> "UpdateAsterismsResultFields":
        """Subfields should come from the UpdateAsterismsResultFields class"""
        self._subfields.extend(subfields)
        return self

    def alias(self, alias: str) -> "UpdateAsterismsResultFields":
        self._alias = alias
        return self


class UpdateAttachmentsResultFields(GraphQLField):
    @classmethod
    def attachments(cls) -> "AttachmentFields":
        return AttachmentFields("attachments")

    has_more: "UpdateAttachmentsResultGraphQLField" = (
        UpdateAttachmentsResultGraphQLField("hasMore")
    )

    def fields(
        self, *subfields: Union[UpdateAttachmentsResultGraphQLField, "AttachmentFields"]
    ) -> "UpdateAttachmentsResultFields":
        """Subfields should come from the UpdateAttachmentsResultFields class"""
        self._subfields.extend(subfields)
        return self

    def alias(self, alias: str) -> "UpdateAttachmentsResultFields":
        self._alias = alias
        return self


class UpdateCallsForProposalsResultFields(GraphQLField):
    @classmethod
    def calls_for_proposals(cls) -> "CallForProposalsFields":
        return CallForProposalsFields("callsForProposals")

    has_more: "UpdateCallsForProposalsResultGraphQLField" = (
        UpdateCallsForProposalsResultGraphQLField("hasMore")
    )

    def fields(
        self,
        *subfields: Union[
            UpdateCallsForProposalsResultGraphQLField, "CallForProposalsFields"
        ],
    ) -> "UpdateCallsForProposalsResultFields":
        """Subfields should come from the UpdateCallsForProposalsResultFields class"""
        self._subfields.extend(subfields)
        return self

    def alias(self, alias: str) -> "UpdateCallsForProposalsResultFields":
        self._alias = alias
        return self


class UpdateConfigurationRequestsResultFields(GraphQLField):
    @classmethod
    def requests(cls) -> "ConfigurationRequestFields":
        return ConfigurationRequestFields("requests")

    has_more: "UpdateConfigurationRequestsResultGraphQLField" = (
        UpdateConfigurationRequestsResultGraphQLField("hasMore")
    )

    def fields(
        self,
        *subfields: Union[
            UpdateConfigurationRequestsResultGraphQLField, "ConfigurationRequestFields"
        ],
    ) -> "UpdateConfigurationRequestsResultFields":
        """Subfields should come from the UpdateConfigurationRequestsResultFields class"""
        self._subfields.extend(subfields)
        return self

    def alias(self, alias: str) -> "UpdateConfigurationRequestsResultFields":
        self._alias = alias
        return self


class UpdateDatasetsResultFields(GraphQLField):
    @classmethod
    def datasets(cls) -> "DatasetFields":
        return DatasetFields("datasets")

    has_more: "UpdateDatasetsResultGraphQLField" = UpdateDatasetsResultGraphQLField(
        "hasMore"
    )

    def fields(
        self, *subfields: Union[UpdateDatasetsResultGraphQLField, "DatasetFields"]
    ) -> "UpdateDatasetsResultFields":
        """Subfields should come from the UpdateDatasetsResultFields class"""
        self._subfields.extend(subfields)
        return self

    def alias(self, alias: str) -> "UpdateDatasetsResultFields":
        self._alias = alias
        return self


class UpdateGroupsResultFields(GraphQLField):
    @classmethod
    def groups(cls) -> "GroupFields":
        return GroupFields("groups")

    has_more: "UpdateGroupsResultGraphQLField" = UpdateGroupsResultGraphQLField(
        "hasMore"
    )

    def fields(
        self, *subfields: Union[UpdateGroupsResultGraphQLField, "GroupFields"]
    ) -> "UpdateGroupsResultFields":
        """Subfields should come from the UpdateGroupsResultFields class"""
        self._subfields.extend(subfields)
        return self

    def alias(self, alias: str) -> "UpdateGroupsResultFields":
        self._alias = alias
        return self


class UpdateObservationsResultFields(GraphQLField):
    @classmethod
    def observations(cls) -> "ObservationFields":
        return ObservationFields("observations")

    has_more: "UpdateObservationsResultGraphQLField" = (
        UpdateObservationsResultGraphQLField("hasMore")
    )

    def fields(
        self,
        *subfields: Union[UpdateObservationsResultGraphQLField, "ObservationFields"],
    ) -> "UpdateObservationsResultFields":
        """Subfields should come from the UpdateObservationsResultFields class"""
        self._subfields.extend(subfields)
        return self

    def alias(self, alias: str) -> "UpdateObservationsResultFields":
        self._alias = alias
        return self


class UpdateProgramNotesResultFields(GraphQLField):
    @classmethod
    def program_notes(cls) -> "ProgramNoteFields":
        return ProgramNoteFields("programNotes")

    has_more: "UpdateProgramNotesResultGraphQLField" = (
        UpdateProgramNotesResultGraphQLField("hasMore")
    )

    def fields(
        self,
        *subfields: Union[UpdateProgramNotesResultGraphQLField, "ProgramNoteFields"],
    ) -> "UpdateProgramNotesResultFields":
        """Subfields should come from the UpdateProgramNotesResultFields class"""
        self._subfields.extend(subfields)
        return self

    def alias(self, alias: str) -> "UpdateProgramNotesResultFields":
        self._alias = alias
        return self


class UpdateProgramUsersResultFields(GraphQLField):
    @classmethod
    def program_users(cls) -> "ProgramUserFields":
        return ProgramUserFields("programUsers")

    has_more: "UpdateProgramUsersResultGraphQLField" = (
        UpdateProgramUsersResultGraphQLField("hasMore")
    )

    def fields(
        self,
        *subfields: Union[UpdateProgramUsersResultGraphQLField, "ProgramUserFields"],
    ) -> "UpdateProgramUsersResultFields":
        """Subfields should come from the UpdateProgramUsersResultFields class"""
        self._subfields.extend(subfields)
        return self

    def alias(self, alias: str) -> "UpdateProgramUsersResultFields":
        self._alias = alias
        return self


class UpdateProgramsResultFields(GraphQLField):
    @classmethod
    def programs(cls) -> "ProgramFields":
        return ProgramFields("programs")

    has_more: "UpdateProgramsResultGraphQLField" = UpdateProgramsResultGraphQLField(
        "hasMore"
    )

    def fields(
        self, *subfields: Union[UpdateProgramsResultGraphQLField, "ProgramFields"]
    ) -> "UpdateProgramsResultFields":
        """Subfields should come from the UpdateProgramsResultFields class"""
        self._subfields.extend(subfields)
        return self

    def alias(self, alias: str) -> "UpdateProgramsResultFields":
        self._alias = alias
        return self


class UpdateProposalResultFields(GraphQLField):
    @classmethod
    def proposal(cls) -> "ProposalFields":
        return ProposalFields("proposal")

    def fields(
        self, *subfields: Union[UpdateProposalResultGraphQLField, "ProposalFields"]
    ) -> "UpdateProposalResultFields":
        """Subfields should come from the UpdateProposalResultFields class"""
        self._subfields.extend(subfields)
        return self

    def alias(self, alias: str) -> "UpdateProposalResultFields":
        self._alias = alias
        return self


class UpdateTargetsResultFields(GraphQLField):
    @classmethod
    def targets(cls) -> "TargetFields":
        return TargetFields("targets")

    has_more: "UpdateTargetsResultGraphQLField" = UpdateTargetsResultGraphQLField(
        "hasMore"
    )

    def fields(
        self, *subfields: Union[UpdateTargetsResultGraphQLField, "TargetFields"]
    ) -> "UpdateTargetsResultFields":
        """Subfields should come from the UpdateTargetsResultFields class"""
        self._subfields.extend(subfields)
        return self

    def alias(self, alias: str) -> "UpdateTargetsResultFields":
        self._alias = alias
        return self


class UserFields(GraphQLField):
    id: "UserGraphQLField" = UserGraphQLField("id")
    type_: "UserGraphQLField" = UserGraphQLField("type")
    service_name: "UserGraphQLField" = UserGraphQLField("serviceName")
    orcid_id: "UserGraphQLField" = UserGraphQLField("orcidId")

    @classmethod
    def profile(cls) -> "UserProfileFields":
        return UserProfileFields("profile")

    def fields(
        self, *subfields: Union[UserGraphQLField, "UserProfileFields"]
    ) -> "UserFields":
        """Subfields should come from the UserFields class"""
        self._subfields.extend(subfields)
        return self

    def alias(self, alias: str) -> "UserFields":
        self._alias = alias
        return self


class UserInvitationFields(GraphQLField):
    id: "UserInvitationGraphQLField" = UserInvitationGraphQLField("id")
    status: "UserInvitationGraphQLField" = UserInvitationGraphQLField("status")

    @classmethod
    def issuer(cls) -> "UserFields":
        return UserFields("issuer")

    recipient_email: "UserInvitationGraphQLField" = UserInvitationGraphQLField(
        "recipientEmail"
    )

    @classmethod
    def program_user(cls) -> "ProgramUserFields":
        return ProgramUserFields("programUser")

    @classmethod
    def email(cls) -> "EmailFields":
        return EmailFields("email")

    def fields(
        self,
        *subfields: Union[
            UserInvitationGraphQLField, "EmailFields", "ProgramUserFields", "UserFields"
        ],
    ) -> "UserInvitationFields":
        """Subfields should come from the UserInvitationFields class"""
        self._subfields.extend(subfields)
        return self

    def alias(self, alias: str) -> "UserInvitationFields":
        self._alias = alias
        return self


class UserProfileFields(GraphQLField):
    given_name: "UserProfileGraphQLField" = UserProfileGraphQLField("givenName")
    family_name: "UserProfileGraphQLField" = UserProfileGraphQLField("familyName")
    credit_name: "UserProfileGraphQLField" = UserProfileGraphQLField("creditName")
    email: "UserProfileGraphQLField" = UserProfileGraphQLField("email")

    def fields(self, *subfields: UserProfileGraphQLField) -> "UserProfileFields":
        """Subfields should come from the UserProfileFields class"""
        self._subfields.extend(subfields)
        return self

    def alias(self, alias: str) -> "UserProfileFields":
        self._alias = alias
        return self


class VisitFields(GraphQLField):
    id: "VisitGraphQLField" = VisitGraphQLField("id")
    instrument: "VisitGraphQLField" = VisitGraphQLField("instrument")

    @classmethod
    def observation(cls) -> "ObservationFields":
        return ObservationFields("observation")

    recorded_time: "VisitGraphQLField" = VisitGraphQLField("recordedTime")
    created: "VisitGraphQLField" = VisitGraphQLField("created")
    client_time: "VisitGraphQLField" = VisitGraphQLField("clientTime")
    effective_time: "VisitGraphQLField" = VisitGraphQLField("effectiveTime")
    site: "VisitGraphQLField" = VisitGraphQLField("site")

    @classmethod
    def interval(cls) -> "TimestampIntervalFields":
        return TimestampIntervalFields("interval")

    @classmethod
    def atom_records(
        cls, *, offset: Optional[Any] = None, limit: Optional[Any] = None
    ) -> "AtomRecordSelectResultFields":
        arguments: dict[str, dict[str, Any]] = {
            "OFFSET": {"type": "PosInt", "value": offset},
            "LIMIT": {"type": "NonNegInt", "value": limit},
        }
        cleared_arguments = {
            key: value for key, value in arguments.items() if value["value"] is not None
        }
        return AtomRecordSelectResultFields("atomRecords", arguments=cleared_arguments)

    @classmethod
    def datasets(
        cls, *, offset: Optional[Any] = None, limit: Optional[Any] = None
    ) -> "DatasetSelectResultFields":
        arguments: dict[str, dict[str, Any]] = {
            "OFFSET": {"type": "DatasetId", "value": offset},
            "LIMIT": {"type": "NonNegInt", "value": limit},
        }
        cleared_arguments = {
            key: value for key, value in arguments.items() if value["value"] is not None
        }
        return DatasetSelectResultFields("datasets", arguments=cleared_arguments)

    @classmethod
    def events(
        cls, *, offset: Optional[Any] = None, limit: Optional[Any] = None
    ) -> "ExecutionEventSelectResultFields":
        arguments: dict[str, dict[str, Any]] = {
            "OFFSET": {"type": "ExecutionEventId", "value": offset},
            "LIMIT": {"type": "NonNegInt", "value": limit},
        }
        cleared_arguments = {
            key: value for key, value in arguments.items() if value["value"] is not None
        }
        return ExecutionEventSelectResultFields("events", arguments=cleared_arguments)

    @classmethod
    def time_charge_invoice(cls) -> "TimeChargeInvoiceFields":
        return TimeChargeInvoiceFields("timeChargeInvoice")

    idempotency_key: "VisitGraphQLField" = VisitGraphQLField("idempotencyKey")

    @classmethod
    def flamingos_2(cls) -> "Flamingos2StaticFields":
        return Flamingos2StaticFields("flamingos2")

    @classmethod
    def gmos_north(cls) -> "GmosNorthStaticFields":
        return GmosNorthStaticFields("gmosNorth")

    @classmethod
    def gmos_south(cls) -> "GmosSouthStaticFields":
        return GmosSouthStaticFields("gmosSouth")

    @classmethod
    def igrins_2(cls) -> "Igrins2StaticFields":
        return Igrins2StaticFields("igrins2")

    @classmethod
    def gnirs(cls) -> "GnirsStaticFields":
        return GnirsStaticFields("gnirs")

    def fields(
        self,
        *subfields: Union[
            VisitGraphQLField,
            "AtomRecordSelectResultFields",
            "DatasetSelectResultFields",
            "ExecutionEventSelectResultFields",
            "Flamingos2StaticFields",
            "GmosNorthStaticFields",
            "GmosSouthStaticFields",
            "GnirsStaticFields",
            "Igrins2StaticFields",
            "ObservationFields",
            "TimeChargeInvoiceFields",
            "TimestampIntervalFields",
        ],
    ) -> "VisitFields":
        """Subfields should come from the VisitFields class"""
        self._subfields.extend(subfields)
        return self

    def alias(self, alias: str) -> "VisitFields":
        self._alias = alias
        return self


class VisitSelectResultFields(GraphQLField):
    @classmethod
    def matches(cls) -> "VisitFields":
        return VisitFields("matches")

    has_more: "VisitSelectResultGraphQLField" = VisitSelectResultGraphQLField("hasMore")

    def fields(
        self, *subfields: Union[VisitSelectResultGraphQLField, "VisitFields"]
    ) -> "VisitSelectResultFields":
        """Subfields should come from the VisitSelectResultFields class"""
        self._subfields.extend(subfields)
        return self

    def alias(self, alias: str) -> "VisitSelectResultFields":
        self._alias = alias
        return self


class VisitorFields(GraphQLField):
    mode: "VisitorGraphQLField" = VisitorGraphQLField("mode")

    @classmethod
    def central_wavelength(cls) -> "WavelengthFields":
        return WavelengthFields("centralWavelength")

    @classmethod
    def ags_diameter(cls) -> "AngleFields":
        return AngleFields("agsDiameter")

    @classmethod
    def science_fov_diameter(cls) -> "AngleFields":
        return AngleFields("scienceFovDiameter")

    name: "VisitorGraphQLField" = VisitorGraphQLField("name")

    @classmethod
    def total_request_time(cls) -> "TimeSpanFields":
        return TimeSpanFields("totalRequestTime")

    def fields(
        self,
        *subfields: Union[
            VisitorGraphQLField, "AngleFields", "TimeSpanFields", "WavelengthFields"
        ],
    ) -> "VisitorFields":
        """Subfields should come from the VisitorFields class"""
        self._subfields.extend(subfields)
        return self

    def alias(self, alias: str) -> "VisitorFields":
        self._alias = alias
        return self


class WavelengthFields(GraphQLField):
    picometers: "WavelengthGraphQLField" = WavelengthGraphQLField("picometers")
    angstroms: "WavelengthGraphQLField" = WavelengthGraphQLField("angstroms")
    nanometers: "WavelengthGraphQLField" = WavelengthGraphQLField("nanometers")
    micrometers: "WavelengthGraphQLField" = WavelengthGraphQLField("micrometers")

    def fields(self, *subfields: WavelengthGraphQLField) -> "WavelengthFields":
        """Subfields should come from the WavelengthFields class"""
        self._subfields.extend(subfields)
        return self

    def alias(self, alias: str) -> "WavelengthFields":
        self._alias = alias
        return self


class WavelengthDitherFields(GraphQLField):
    picometers: "WavelengthDitherGraphQLField" = WavelengthDitherGraphQLField(
        "picometers"
    )
    angstroms: "WavelengthDitherGraphQLField" = WavelengthDitherGraphQLField(
        "angstroms"
    )
    nanometers: "WavelengthDitherGraphQLField" = WavelengthDitherGraphQLField(
        "nanometers"
    )
    micrometers: "WavelengthDitherGraphQLField" = WavelengthDitherGraphQLField(
        "micrometers"
    )

    def fields(
        self, *subfields: WavelengthDitherGraphQLField
    ) -> "WavelengthDitherFields":
        """Subfields should come from the WavelengthDitherFields class"""
        self._subfields.extend(subfields)
        return self

    def alias(self, alias: str) -> "WavelengthDitherFields":
        self._alias = alias
        return self
