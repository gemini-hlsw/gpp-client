from enum import Enum


class _TolerantEnum(str, Enum):
    """Keep a value this build does not know as a member carrying the raw value."""

    @classmethod
    def _missing_(cls, value: object) -> "_TolerantEnum | None":
        if not isinstance(value, str):
            return None
        member = str.__new__(cls, value)
        member._name_ = value
        member._value_ = value
        known = cls._value2member_map_.setdefault(value, member)
        return known if isinstance(known, cls) else None


class AtomExecutionState(_TolerantEnum):
    NOT_STARTED = "NOT_STARTED"
    ONGOING = "ONGOING"
    COMPLETED = "COMPLETED"
    ABANDONED = "ABANDONED"


class AtomStage(_TolerantEnum):
    END_ATOM = "END_ATOM"
    START_ATOM = "START_ATOM"


class BlindOffsetType(_TolerantEnum):
    AUTOMATIC = "AUTOMATIC"
    MANUAL = "MANUAL"


class Breakpoint(_TolerantEnum):
    ENABLED = "ENABLED"
    DISABLED = "DISABLED"


class Observatory(_TolerantEnum):
    GEMINI = "GEMINI"
    KECK = "KECK"
    SUBARU = "SUBARU"


class ExchangePartner(_TolerantEnum):
    KECK = "KECK"
    SUBARU = "SUBARU"


class KeckInstrument(_TolerantEnum):
    HIRES = "HIRES"
    OTHER = "OTHER"


class SubaruInstrument(_TolerantEnum):
    FOCAS = "FOCAS"
    HDS = "HDS"
    HSC = "HSC"
    IRCS = "IRCS"
    MOIRCS = "MOIRCS"
    PFS = "PFS"
    VISITOR = "VISITOR"


class SubaruCallForProposalsType(_TolerantEnum):
    NORMAL = "NORMAL"
    INTENSIVE = "INTENSIVE"


class GeminiCallForProposalsType(_TolerantEnum):
    DEMO_SCIENCE = "DEMO_SCIENCE"
    DIRECTORS_TIME = "DIRECTORS_TIME"
    FAST_TURNAROUND = "FAST_TURNAROUND"
    LARGE_PROGRAM = "LARGE_PROGRAM"
    POOR_WEATHER = "POOR_WEATHER"
    REGULAR_SEMESTER = "REGULAR_SEMESTER"
    SYSTEM_VERIFICATION = "SYSTEM_VERIFICATION"


class CloneSequenceMode(_TolerantEnum):
    """Available on: development."""

    NONE = "NONE"
    ALL_STEPS = "ALL_STEPS"
    PENDING_STEPS = "PENDING_STEPS"


class ConditionsMeasurementSource(_TolerantEnum):
    OBSERVER = "OBSERVER"


class SeeingTrend(_TolerantEnum):
    GETTING_BETTER = "GETTING_BETTER"
    GETTING_WORSE = "GETTING_WORSE"
    STAYING_THE_SAME = "STAYING_THE_SAME"
    VARIABLE = "VARIABLE"


class ConditionsExpectationType(_TolerantEnum):
    CLEAR_SKIES = "CLEAR_SKIES"
    FOG = "FOG"
    THICK_CLOUDS = "THICK_CLOUDS"
    THIN_CLOUDS = "THIN_CLOUDS"


class EditType(_TolerantEnum):
    CREATED = "CREATED"
    UPDATED = "UPDATED"
    HARD_DELETE = "HARD_DELETE"


class EmailStatus(_TolerantEnum):
    QUEUED = "QUEUED"
    REJECTED = "REJECTED"
    ACCEPTED = "ACCEPTED"
    DELIVERED = "DELIVERED"
    PERMANENT_FAILURE = "PERMANENT_FAILURE"
    TEMPORARY_FAILURE = "TEMPORARY_FAILURE"


class ExecutionEventType(_TolerantEnum):
    SEQUENCE = "SEQUENCE"
    SLEW = "SLEW"
    ATOM = "ATOM"
    STEP = "STEP"
    DATASET = "DATASET"


class GcalArc(_TolerantEnum):
    AR_ARC = "AR_ARC"
    TH_AR_ARC = "TH_AR_ARC"
    CU_AR_ARC = "CU_AR_ARC"
    XE_ARC = "XE_ARC"


class GcalContinuum(_TolerantEnum):
    IR_GREY_BODY_LOW = "IR_GREY_BODY_LOW"
    IR_GREY_BODY_HIGH = "IR_GREY_BODY_HIGH"
    QUARTZ_HALOGEN5 = "QUARTZ_HALOGEN5"
    QUARTZ_HALOGEN100 = "QUARTZ_HALOGEN100"


class GcalDiffuser(_TolerantEnum):
    IR = "IR"
    VISIBLE = "VISIBLE"


class GcalFilter(_TolerantEnum):
    NONE = "NONE"
    GMOS = "GMOS"
    HROS = "HROS"
    NIR = "NIR"
    ND10 = "ND10"
    ND16 = "ND16"
    ND20 = "ND20"
    ND30 = "ND30"
    ND40 = "ND40"
    ND45 = "ND45"
    ND50 = "ND50"


class GcalShutter(_TolerantEnum):
    OPEN = "OPEN"
    CLOSED = "CLOSED"


class GhostResolutionMode(_TolerantEnum):
    STANDARD = "STANDARD"
    HIGH = "HIGH"


class GhostBinning(_TolerantEnum):
    ONE_BY_ONE = "ONE_BY_ONE"
    ONE_BY_TWO = "ONE_BY_TWO"
    ONE_BY_FOUR = "ONE_BY_FOUR"
    ONE_BY_EIGHT = "ONE_BY_EIGHT"
    TWO_BY_TWO = "TWO_BY_TWO"
    TWO_BY_FOUR = "TWO_BY_FOUR"
    TWO_BY_EIGHT = "TWO_BY_EIGHT"
    FOUR_BY_FOUR = "FOUR_BY_FOUR"


class GhostReadMode(_TolerantEnum):
    SLOW = "SLOW"
    MEDIUM = "MEDIUM"
    FAST = "FAST"


class GmosAmpCount(_TolerantEnum):
    THREE = "THREE"
    SIX = "SIX"
    TWELVE = "TWELVE"


class GmosCustomSlitWidth(_TolerantEnum):
    CUSTOM_WIDTH_0_25 = "CUSTOM_WIDTH_0_25"
    CUSTOM_WIDTH_0_50 = "CUSTOM_WIDTH_0_50"
    CUSTOM_WIDTH_0_75 = "CUSTOM_WIDTH_0_75"
    CUSTOM_WIDTH_1_00 = "CUSTOM_WIDTH_1_00"
    CUSTOM_WIDTH_1_50 = "CUSTOM_WIDTH_1_50"
    CUSTOM_WIDTH_2_00 = "CUSTOM_WIDTH_2_00"
    CUSTOM_WIDTH_5_00 = "CUSTOM_WIDTH_5_00"


class GmosMosAcquisitionType(_TolerantEnum):
    MASK_IN = "MASK_IN"
    MASK_OUT = "MASK_OUT"


class GmosDtax(_TolerantEnum):
    MINUS_SIX = "MINUS_SIX"
    MINUS_FIVE = "MINUS_FIVE"
    MINUS_FOUR = "MINUS_FOUR"
    MINUS_THREE = "MINUS_THREE"
    MINUS_TWO = "MINUS_TWO"
    MINUS_ONE = "MINUS_ONE"
    ZERO = "ZERO"
    ONE = "ONE"
    TWO = "TWO"
    THREE = "THREE"
    FOUR = "FOUR"
    FIVE = "FIVE"
    SIX = "SIX"


class GmosEOffsetting(_TolerantEnum):
    ON = "ON"
    OFF = "OFF"


class GmosGratingOrder(_TolerantEnum):
    ZERO = "ZERO"
    ONE = "ONE"
    TWO = "TWO"


class GmosNorthDetector(_TolerantEnum):
    E2_V = "E2_V"
    HAMAMATSU = "HAMAMATSU"


class GmosNorthStageMode(_TolerantEnum):
    NO_FOLLOW = "NO_FOLLOW"
    FOLLOW_XY = "FOLLOW_XY"


class GmosSouthDetector(_TolerantEnum):
    E2_V = "E2_V"
    HAMAMATSU = "HAMAMATSU"


class GmosSouthStageMode(_TolerantEnum):
    NO_FOLLOW = "NO_FOLLOW"
    FOLLOW_XYZ = "FOLLOW_XYZ"
    FOLLOW_Z = "FOLLOW_Z"


class GuideState(_TolerantEnum):
    ENABLED = "ENABLED"
    DISABLED = "DISABLED"


class UserInvitationStatus(_TolerantEnum):
    PENDING = "PENDING"
    REDEEMED = "REDEEMED"
    DECLINED = "DECLINED"
    REVOKED = "REVOKED"


class MosPreImaging(_TolerantEnum):
    IS_MOS_PRE_IMAGING = "IS_MOS_PRE_IMAGING"
    IS_NOT_MOS_PRE_IMAGING = "IS_NOT_MOS_PRE_IMAGING"


class SchedulingMode(_TolerantEnum):
    UNCONSTRAINED = "UNCONSTRAINED"
    NO_SPLITTING = "NO_SPLITTING"
    UNINTERRUPTIBLE = "UNINTERRUPTIBLE"


class TelescopeConfigGeneratorType(_TolerantEnum):
    NONE = "NONE"
    ENUMERATED = "ENUMERATED"
    RANDOM = "RANDOM"
    SPIRAL = "SPIRAL"
    UNIFORM = "UNIFORM"


class Partner(_TolerantEnum):
    AR = "AR"
    BR = "BR"
    CA = "CA"
    CL = "CL"
    KR = "KR"
    UH = "UH"
    US = "US"


class PartnerLinkType(_TolerantEnum):
    HAS_GEMINI_PARTNER = "HAS_GEMINI_PARTNER"
    HAS_EXCHANGE_PARTNER = "HAS_EXCHANGE_PARTNER"
    HAS_NON_PARTNER = "HAS_NON_PARTNER"
    HAS_UNSPECIFIED_PARTNER = "HAS_UNSPECIFIED_PARTNER"


class ProgramUserRole(_TolerantEnum):
    PI = "PI"
    COI = "COI"
    COI_RO = "COI_RO"
    EXTERNAL = "EXTERNAL"
    SUPPORT_PRIMARY = "SUPPORT_PRIMARY"
    SUPPORT_SECONDARY = "SUPPORT_SECONDARY"


class ProgramUserSupportRoleType(_TolerantEnum):
    STAFF = "STAFF"
    PARTNER = "PARTNER"


class Ignore(_TolerantEnum):
    IGNORE = "IGNORE"


class SmartGcalType(_TolerantEnum):
    ARC = "ARC"
    FLAT = "FLAT"
    DAY_BASELINE = "DAY_BASELINE"
    NIGHT_BASELINE = "NIGHT_BASELINE"


class StepExecutionState(_TolerantEnum):
    NOT_STARTED = "NOT_STARTED"
    ONGOING = "ONGOING"
    ABORTED = "ABORTED"
    COMPLETED = "COMPLETED"
    STOPPED = "STOPPED"
    ABANDONED = "ABANDONED"


class StepType(_TolerantEnum):
    BIAS = "BIAS"
    DARK = "DARK"
    GCAL = "GCAL"
    SCIENCE = "SCIENCE"
    SMART_GCAL = "SMART_GCAL"


class CalculationState(_TolerantEnum):
    RETRY = "RETRY"
    PENDING = "PENDING"
    CALCULATING = "CALCULATING"
    READY = "READY"


class TimeAccountingCategory(_TolerantEnum):
    AR = "AR"
    BR = "BR"
    CA = "CA"
    CAL = "CAL"
    CFHT = "CFHT"
    CL = "CL"
    DD = "DD"
    DS = "DS"
    ENG = "ENG"
    GT = "GT"
    JP = "JP"
    KECK = "KECK"
    KR = "KR"
    LP = "LP"
    LTP = "LTP"
    SV = "SV"
    UH = "UH"
    US = "US"


class AttachmentType(_TolerantEnum):
    SCIENCE = "SCIENCE"
    TEAM = "TEAM"
    FINDER = "FINDER"
    MOS_MASK = "MOS_MASK"
    PRE_IMAGING = "PRE_IMAGING"
    CUSTOM_SED = "CUSTOM_SED"
    SUMMARY = "SUMMARY"


class ProposalSummaryGenerationState(_TolerantEnum):
    IDLE = "IDLE"
    GENERATING = "GENERATING"
    FAILED = "FAILED"


class ProposalSummaryStyle(_TolerantEnum):
    GEMINI_STANDARD = "GEMINI_STANDARD"
    GEMINI_DARP = "GEMINI_DARP"
    GEMINI_NO_INVESTIGATORS = "GEMINI_NO_INVESTIGATORS"
    GEMINI_INVESTIGATORS_AT_END = "GEMINI_INVESTIGATORS_AT_END"
    CHILE = "CHILE"
    NOIRLAB_DARP = "NOIRLAB_DARP"


class MosDispersionDirection(_TolerantEnum):
    HORIZONTAL = "HORIZONTAL"
    VERTICAL = "VERTICAL"


class MosSlitPriority(_TolerantEnum):
    ACQUISITION = "ACQUISITION"
    HIGH = "HIGH"
    MEDIUM = "MEDIUM"
    LOW = "LOW"
    IGNORE = "IGNORE"


class Band(_TolerantEnum):
    SLOAN_U = "SLOAN_U"
    SLOAN_G = "SLOAN_G"
    SLOAN_R = "SLOAN_R"
    SLOAN_I = "SLOAN_I"
    SLOAN_Z = "SLOAN_Z"
    U = "U"
    B = "B"
    V = "V"
    R = "R"
    I = "I"
    Y = "Y"
    J = "J"
    H = "H"
    K = "K"
    L = "L"
    M = "M"
    N = "N"
    Q = "Q"
    AP = "AP"
    GAIA = "GAIA"
    GAIA_BP = "GAIA_BP"
    GAIA_RP = "GAIA_RP"


class BrightnessIntegratedUnits(_TolerantEnum):
    VEGA_MAGNITUDE = "VEGA_MAGNITUDE"
    AB_MAGNITUDE = "AB_MAGNITUDE"
    JANSKY = "JANSKY"
    W_PER_M_SQUARED_PER_UM = "W_PER_M_SQUARED_PER_UM"
    ERG_PER_S_PER_CM_SQUARED_PER_A = "ERG_PER_S_PER_CM_SQUARED_PER_A"
    ERG_PER_S_PER_CM_SQUARED_PER_HZ = "ERG_PER_S_PER_CM_SQUARED_PER_HZ"


class BrightnessSurfaceUnits(_TolerantEnum):
    VEGA_MAG_PER_ARCSEC_SQUARED = "VEGA_MAG_PER_ARCSEC_SQUARED"
    AB_MAG_PER_ARCSEC_SQUARED = "AB_MAG_PER_ARCSEC_SQUARED"
    JY_PER_ARCSEC_SQUARED = "JY_PER_ARCSEC_SQUARED"
    W_PER_M_SQUARED_PER_UM_PER_ARCSEC_SQUARED = (
        "W_PER_M_SQUARED_PER_UM_PER_ARCSEC_SQUARED"
    )
    ERG_PER_S_PER_CM_SQUARED_PER_A_PER_ARCSEC_SQUARED = (
        "ERG_PER_S_PER_CM_SQUARED_PER_A_PER_ARCSEC_SQUARED"
    )
    ERG_PER_S_PER_CM_SQUARED_PER_HZ_PER_ARCSEC_SQUARED = (
        "ERG_PER_S_PER_CM_SQUARED_PER_HZ_PER_ARCSEC_SQUARED"
    )


class CassRotator(_TolerantEnum):
    FIXED = "FIXED"
    FOLLOWING = "FOLLOWING"


class CatalogName(_TolerantEnum):
    SIMBAD = "SIMBAD"
    IMPORT = "IMPORT"
    GAIA = "GAIA"
    TELLURIC = "TELLURIC"


class ChargeClass(_TolerantEnum):
    NON_CHARGED = "NON_CHARGED"
    PROGRAM = "PROGRAM"


class CloudExtinctionPreset(_TolerantEnum):
    ZERO = "ZERO"
    POINT_ONE = "POINT_ONE"
    POINT_THREE = "POINT_THREE"
    POINT_FIVE = "POINT_FIVE"
    ONE_POINT_ZERO = "ONE_POINT_ZERO"
    TWO_POINT_ZERO = "TWO_POINT_ZERO"
    THREE_POINT_ZERO = "THREE_POINT_ZERO"


class ObservingModeType(_TolerantEnum):
    ALOPEKE_SPECKLE = "ALOPEKE_SPECKLE"
    ALOPEKE_WIDE_FIELD = "ALOPEKE_WIDE_FIELD"
    EXCHANGE_KECK = "EXCHANGE_KECK"
    EXCHANGE_SUBARU = "EXCHANGE_SUBARU"
    FLAMINGOS_2_IMAGING = "FLAMINGOS_2_IMAGING"
    FLAMINGOS_2_LONG_SLIT = "FLAMINGOS_2_LONG_SLIT"
    FLAMINGOS_2_MOS = "FLAMINGOS_2_MOS"
    GHOST_IFU = "GHOST_IFU"
    GMOS_NORTH_IFU = "GMOS_NORTH_IFU"
    GMOS_NORTH_IMAGING = "GMOS_NORTH_IMAGING"
    GMOS_NORTH_LONG_SLIT = "GMOS_NORTH_LONG_SLIT"
    GMOS_NORTH_MOS = "GMOS_NORTH_MOS"
    GMOS_SOUTH_IFU = "GMOS_SOUTH_IFU"
    GMOS_SOUTH_IMAGING = "GMOS_SOUTH_IMAGING"
    GMOS_SOUTH_LONG_SLIT = "GMOS_SOUTH_LONG_SLIT"
    GMOS_SOUTH_MOS = "GMOS_SOUTH_MOS"
    GNIRS_IMAGING = "GNIRS_IMAGING"
    GNIRS_LONG_SLIT = "GNIRS_LONG_SLIT"
    GNIRS_IFU = "GNIRS_IFU"
    IGRINS_2_LONG_SLIT = "IGRINS_2_LONG_SLIT"
    MAROON_X = "MAROON_X"
    VISITOR_NORTH = "VISITOR_NORTH"
    VISITOR_SOUTH = "VISITOR_SOUTH"
    ZORRO_SPECKLE = "ZORRO_SPECKLE"
    ZORRO_WIDE_FIELD = "ZORRO_WIDE_FIELD"


class VisitorObservingModeType(_TolerantEnum):
    ALOPEKE_SPECKLE = "ALOPEKE_SPECKLE"
    ALOPEKE_WIDE_FIELD = "ALOPEKE_WIDE_FIELD"
    MAROON_X = "MAROON_X"
    VISITOR_NORTH = "VISITOR_NORTH"
    VISITOR_SOUTH = "VISITOR_SOUTH"
    ZORRO_SPECKLE = "ZORRO_SPECKLE"
    ZORRO_WIDE_FIELD = "ZORRO_WIDE_FIELD"


class ExchangeObservingModeType(_TolerantEnum):
    EXCHANGE_KECK = "EXCHANGE_KECK"
    EXCHANGE_SUBARU = "EXCHANGE_SUBARU"


class CoolStarTemperature(_TolerantEnum):
    T400_K = "T400_K"
    T600_K = "T600_K"
    T800_K = "T800_K"
    T900_K = "T900_K"
    T1000_K = "T1000_K"
    T1200_K = "T1200_K"
    T1400_K = "T1400_K"
    T1600_K = "T1600_K"
    T1800_K = "T1800_K"
    T2000_K = "T2000_K"
    T2200_K = "T2200_K"
    T2400_K = "T2400_K"
    T2600_K = "T2600_K"
    T2800_K = "T2800_K"


class DatabaseOperation(_TolerantEnum):
    INSERT = "INSERT"
    UPDATE = "UPDATE"
    DELETE = "DELETE"
    TRUNCATE = "TRUNCATE"


class DatasetQaState(_TolerantEnum):
    PASS = "PASS"
    USABLE = "USABLE"
    FAIL = "FAIL"


class DatasetStage(_TolerantEnum):
    END_EXPOSE = "END_EXPOSE"
    END_READOUT = "END_READOUT"
    END_WRITE = "END_WRITE"
    START_EXPOSE = "START_EXPOSE"
    START_READOUT = "START_READOUT"
    START_WRITE = "START_WRITE"


class EducationalStatus(_TolerantEnum):
    PHD = "PHD"
    GRAD_STUDENT = "GRAD_STUDENT"
    UNDERGRAD_STUDENT = "UNDERGRAD_STUDENT"
    OTHER = "OTHER"


class EphemerisKeyType(_TolerantEnum):
    COMET = "COMET"
    ASTEROID_NEW = "ASTEROID_NEW"
    ASTEROID_OLD = "ASTEROID_OLD"
    MAJOR_BODY = "MAJOR_BODY"
    USER_SUPPLIED = "USER_SUPPLIED"


class Existence(_TolerantEnum):
    PRESENT = "PRESENT"
    DELETED = "DELETED"


class Flamingos2CustomSlitWidth(_TolerantEnum):
    CUSTOM_WIDTH_1_PIX = "CUSTOM_WIDTH_1_PIX"
    CUSTOM_WIDTH_2_PIX = "CUSTOM_WIDTH_2_PIX"
    CUSTOM_WIDTH_3_PIX = "CUSTOM_WIDTH_3_PIX"
    CUSTOM_WIDTH_4_PIX = "CUSTOM_WIDTH_4_PIX"
    CUSTOM_WIDTH_6_PIX = "CUSTOM_WIDTH_6_PIX"
    CUSTOM_WIDTH_8_PIX = "CUSTOM_WIDTH_8_PIX"
    OTHER = "OTHER"


class Flamingos2LyotWheel(_TolerantEnum):
    F16 = "F16"
    GEMS_UNDER = "GEMS_UNDER"
    GEMS_OVER = "GEMS_OVER"
    HARTMANN_A = "HARTMANN_A"
    HARTMANN_B = "HARTMANN_B"


class Flamingos2Disperser(_TolerantEnum):
    R1200_JH = "R1200_JH"
    R1200_HK = "R1200_HK"
    R3000 = "R3000"


class Flamingos2Filter(_TolerantEnum):
    Y = "Y"
    J = "J"
    H = "H"
    JH = "JH"
    HK = "HK"
    J_LOW = "J_LOW"
    K_LONG = "K_LONG"
    K_SHORT = "K_SHORT"
    K_BLUE = "K_BLUE"
    K_RED = "K_RED"


class Flamingos2Fpu(_TolerantEnum):
    PINHOLE = "PINHOLE"
    SUB_PIX_PINHOLE = "SUB_PIX_PINHOLE"
    LONG_SLIT_1 = "LONG_SLIT_1"
    LONG_SLIT_2 = "LONG_SLIT_2"
    LONG_SLIT_3 = "LONG_SLIT_3"
    LONG_SLIT_4 = "LONG_SLIT_4"
    LONG_SLIT_6 = "LONG_SLIT_6"
    LONG_SLIT_8 = "LONG_SLIT_8"


class Flamingos2ReadMode(_TolerantEnum):
    BRIGHT = "BRIGHT"
    MEDIUM = "MEDIUM"
    FAINT = "FAINT"


class Flamingos2Decker(_TolerantEnum):
    IMAGING = "IMAGING"
    LONG_SLIT = "LONG_SLIT"
    MOS = "MOS"


class Flamingos2ReadoutMode(_TolerantEnum):
    SCIENCE = "SCIENCE"
    ENGINEERING = "ENGINEERING"


class Flamingos2Reads(_TolerantEnum):
    READS_1 = "READS_1"
    READS_3 = "READS_3"
    READS_4 = "READS_4"
    READS_5 = "READS_5"
    READS_6 = "READS_6"
    READS_7 = "READS_7"
    READS_8 = "READS_8"
    READS_9 = "READS_9"
    READS_10 = "READS_10"
    READS_11 = "READS_11"
    READS_12 = "READS_12"
    READS_13 = "READS_13"
    READS_14 = "READS_14"
    READS_15 = "READS_15"
    READS_16 = "READS_16"


class TelluricTag(_TolerantEnum):
    HOT = "HOT"
    A0V = "A0V"
    SOLAR = "SOLAR"
    MANUAL = "MANUAL"
    NO_TELLURIC = "NO_TELLURIC"


class GhostIfu1FiberAgitator(_TolerantEnum):
    DISABLED = "DISABLED"
    ENABLED = "ENABLED"


class GhostIfu2FiberAgitator(_TolerantEnum):
    DISABLED = "DISABLED"
    ENABLED = "ENABLED"


class GhostIfuMappingType(_TolerantEnum):
    SINGLE_TARGET = "SINGLE_TARGET"
    TARGET_PLUS_SKY = "TARGET_PLUS_SKY"
    SKY_PLUS_TARGET = "SKY_PLUS_TARGET"
    DUAL_TARGET = "DUAL_TARGET"


class SlitOffsetMode(_TolerantEnum):
    NOD_ALONG_SLIT = "NOD_ALONG_SLIT"
    NOD_TO_SKY = "NOD_TO_SKY"


class FluxDensityContinuumIntegratedUnits(_TolerantEnum):
    W_PER_M_SQUARED_PER_UM = "W_PER_M_SQUARED_PER_UM"
    ERG_PER_S_PER_CM_SQUARED_PER_A = "ERG_PER_S_PER_CM_SQUARED_PER_A"


class FluxDensityContinuumSurfaceUnits(_TolerantEnum):
    W_PER_M_SQUARED_PER_UM_PER_ARCSEC_SQUARED = (
        "W_PER_M_SQUARED_PER_UM_PER_ARCSEC_SQUARED"
    )
    ERG_PER_S_PER_CM_SQUARED_PER_A_PER_ARCSEC_SQUARED = (
        "ERG_PER_S_PER_CM_SQUARED_PER_A_PER_ARCSEC_SQUARED"
    )


class FocalPlane(_TolerantEnum):
    SINGLE_SLIT = "SINGLE_SLIT"
    MULTIPLE_SLIT = "MULTIPLE_SLIT"
    IFU = "IFU"


class GalaxySpectrum(_TolerantEnum):
    ELLIPTICAL = "ELLIPTICAL"
    SPIRAL = "SPIRAL"


class Gender(_TolerantEnum):
    MALE = "MALE"
    FEMALE = "FEMALE"
    OTHER = "OTHER"
    NOT_SPECIFIED = "NOT_SPECIFIED"


class GmosAmpGain(_TolerantEnum):
    LOW = "LOW"
    HIGH = "HIGH"


class GmosAmpReadMode(_TolerantEnum):
    SLOW = "SLOW"
    FAST = "FAST"


class GmosIfuAcquisitionRoi(_TolerantEnum):
    CCD2_FULL_FRAME = "CCD2_FULL_FRAME"
    STAMP_FULL_FRAME = "STAMP_FULL_FRAME"
    FULL_FRAME = "FULL_FRAME"


class GmosLongSlitAcquisitionRoi(_TolerantEnum):
    CCD2_STAMP = "CCD2_STAMP"
    CCD2 = "CCD2"
    STAMP = "STAMP"
    FULL_CCD2 = "FULL_CCD2"


class GmosNorthIfuFpu(_TolerantEnum):
    TWO_SLITS = "TWO_SLITS"
    ONE_SLIT_BLUE = "ONE_SLIT_BLUE"
    ONE_SLIT_RED = "ONE_SLIT_RED"


class GmosSouthIfuFpu(_TolerantEnum):
    TWO_SLITS = "TWO_SLITS"
    ONE_SLIT_BLUE = "ONE_SLIT_BLUE"
    ONE_SLIT_RED = "ONE_SLIT_RED"


class GmosNorthBuiltinFpu(_TolerantEnum):
    NS0 = "NS0"
    NS1 = "NS1"
    NS2 = "NS2"
    NS3 = "NS3"
    NS4 = "NS4"
    NS5 = "NS5"
    LONG_SLIT_0_25 = "LONG_SLIT_0_25"
    LONG_SLIT_0_50 = "LONG_SLIT_0_50"
    LONG_SLIT_0_75 = "LONG_SLIT_0_75"
    LONG_SLIT_1_00 = "LONG_SLIT_1_00"
    LONG_SLIT_1_50 = "LONG_SLIT_1_50"
    LONG_SLIT_2_00 = "LONG_SLIT_2_00"
    LONG_SLIT_5_00 = "LONG_SLIT_5_00"
    IFU2_SLITS = "IFU2_SLITS"
    IFU_BLUE = "IFU_BLUE"
    IFU_RED = "IFU_RED"


class GmosNorthFilter(_TolerantEnum):
    G_PRIME = "G_PRIME"
    R_PRIME = "R_PRIME"
    I_PRIME = "I_PRIME"
    Z_PRIME = "Z_PRIME"
    Z = "Z"
    Y = "Y"
    RI = "RI"
    GG455 = "GG455"
    OG515 = "OG515"
    RG610 = "RG610"
    CA_T = "CA_T"
    HA = "HA"
    HA_C = "HA_C"
    DS920 = "DS920"
    SII = "SII"
    OIII = "OIII"
    OIIIC = "OIIIC"
    OVI = "OVI"
    OVIC = "OVIC"
    HE_II = "HE_II"
    HE_IIC = "HE_IIC"
    HARTMANN_A_R_PRIME = "HARTMANN_A_R_PRIME"
    HARTMANN_B_R_PRIME = "HARTMANN_B_R_PRIME"
    G_PRIME_GG455 = "G_PRIME_GG455"
    G_PRIME_OG515 = "G_PRIME_OG515"
    R_PRIME_RG610 = "R_PRIME_RG610"
    I_PRIME_CA_T = "I_PRIME_CA_T"
    Z_PRIME_CA_T = "Z_PRIME_CA_T"


class GmosNorthGrating(_TolerantEnum):
    B1200_G5301 = "B1200_G5301"
    R831_G5302 = "R831_G5302"
    R600_G5304 = "R600_G5304"
    B480_G5309 = "B480_G5309"
    R400_G5310 = "R400_G5310"
    R150_G5308 = "R150_G5308"


class WavelengthOrder(_TolerantEnum):
    DECREASING = "DECREASING"
    INCREASING = "INCREASING"


class ImagingVariantType(_TolerantEnum):
    GROUPED = "GROUPED"
    INTERLEAVED = "INTERLEAVED"
    PRE_IMAGING = "PRE_IMAGING"


class GmosRoi(_TolerantEnum):
    FULL_FRAME = "FULL_FRAME"
    CCD2 = "CCD2"
    CENTRAL_SPECTRUM = "CENTRAL_SPECTRUM"
    CENTRAL_STAMP = "CENTRAL_STAMP"
    CUSTOM = "CUSTOM"


class GmosSouthBuiltinFpu(_TolerantEnum):
    NS1 = "NS1"
    NS2 = "NS2"
    NS3 = "NS3"
    NS4 = "NS4"
    NS5 = "NS5"
    LONG_SLIT_0_25 = "LONG_SLIT_0_25"
    LONG_SLIT_0_50 = "LONG_SLIT_0_50"
    LONG_SLIT_0_75 = "LONG_SLIT_0_75"
    LONG_SLIT_1_00 = "LONG_SLIT_1_00"
    LONG_SLIT_1_50 = "LONG_SLIT_1_50"
    LONG_SLIT_2_00 = "LONG_SLIT_2_00"
    LONG_SLIT_5_00 = "LONG_SLIT_5_00"
    IFU2_SLITS = "IFU2_SLITS"
    IFU_BLUE = "IFU_BLUE"
    IFU_RED = "IFU_RED"
    IFU_NS2_SLITS = "IFU_NS2_SLITS"
    IFU_NS_BLUE = "IFU_NS_BLUE"
    IFU_NS_RED = "IFU_NS_RED"


class GmosSouthFilter(_TolerantEnum):
    U_PRIME = "U_PRIME"
    G_PRIME = "G_PRIME"
    R_PRIME = "R_PRIME"
    I_PRIME = "I_PRIME"
    Z_PRIME = "Z_PRIME"
    Z = "Z"
    Y = "Y"
    GG455 = "GG455"
    OG515 = "OG515"
    RG610 = "RG610"
    RG780 = "RG780"
    CA_T = "CA_T"
    HARTMANN_A_R_PRIME = "HARTMANN_A_R_PRIME"
    HARTMANN_B_R_PRIME = "HARTMANN_B_R_PRIME"
    G_PRIME_GG455 = "G_PRIME_GG455"
    G_PRIME_OG515 = "G_PRIME_OG515"
    R_PRIME_RG610 = "R_PRIME_RG610"
    I_PRIME_RG780 = "I_PRIME_RG780"
    I_PRIME_CA_T = "I_PRIME_CA_T"
    Z_PRIME_CA_T = "Z_PRIME_CA_T"
    HA = "HA"
    SII = "SII"
    HA_C = "HA_C"
    OIII = "OIII"
    OIIIC = "OIIIC"
    OVI = "OVI"
    OVIC = "OVIC"
    HE_II = "HE_II"
    HE_IIC = "HE_IIC"


class GmosSouthGrating(_TolerantEnum):
    B1200_G5321 = "B1200_G5321"
    R831_G5322 = "R831_G5322"
    R600_G5324 = "R600_G5324"
    B480_G5327 = "B480_G5327"
    R400_G5325 = "R400_G5325"
    R150_G5326 = "R150_G5326"


class GmosBinning(_TolerantEnum):
    ONE = "ONE"
    TWO = "TWO"
    FOUR = "FOUR"


class AltairMode(_TolerantEnum):
    NGS = "NGS"
    LGS = "LGS"
    LGS_P1 = "LGS_P1"


class FieldLens(_TolerantEnum):
    IN = "IN"
    OUT = "OUT"


class AltairNdFilter(_TolerantEnum):
    IN = "IN"
    OUT = "OUT"


class GuideProbe(_TolerantEnum):
    PWFS1 = "PWFS1"
    PWFS2 = "PWFS2"
    GMOS_OIWFS = "GMOS_OIWFS"
    FLAMINGOS2_OIWFS = "FLAMINGOS2_OIWFS"
    ALTAIR_AOWFS = "ALTAIR_AOWFS"


class HiiRegionSpectrum(_TolerantEnum):
    ORION_NEBULA = "ORION_NEBULA"


class ImageQualityPreset(_TolerantEnum):
    POINT_ONE = "POINT_ONE"
    POINT_TWO = "POINT_TWO"
    POINT_THREE = "POINT_THREE"
    POINT_FOUR = "POINT_FOUR"
    POINT_SIX = "POINT_SIX"
    POINT_EIGHT = "POINT_EIGHT"
    ONE_POINT_ZERO = "ONE_POINT_ZERO"
    ONE_POINT_TWO = "ONE_POINT_TWO"
    ONE_POINT_FIVE = "ONE_POINT_FIVE"
    TWO_POINT_ZERO = "TWO_POINT_ZERO"


class PortDisposition(_TolerantEnum):
    SIDE = "SIDE"
    BOTTOM = "BOTTOM"


class Instrument(_TolerantEnum):
    ACQ_CAM_NORTH = "ACQ_CAM_NORTH"
    ACQ_CAM_SOUTH = "ACQ_CAM_SOUTH"
    FLAMINGOS2 = "FLAMINGOS2"
    GHOST = "GHOST"
    GMOS_NORTH = "GMOS_NORTH"
    GMOS_SOUTH = "GMOS_SOUTH"
    GNIRS = "GNIRS"
    GPI = "GPI"
    GSAOI = "GSAOI"
    IGRINS2 = "IGRINS2"
    NIRI = "NIRI"
    VISITOR_NORTH = "VISITOR_NORTH"
    VISITOR_SOUTH = "VISITOR_SOUTH"
    SCORPIO = "SCORPIO"
    ALOPEKE = "ALOPEKE"
    ZORRO = "ZORRO"
    MAROON_X = "MAROON_X"


class GnirsPrism(_TolerantEnum):
    MIRROR = "MIRROR"
    SXD = "SXD"
    LXD = "LXD"


class GnirsCamera(_TolerantEnum):
    LONG_BLUE = "LONG_BLUE"
    LONG_RED = "LONG_RED"
    SHORT_BLUE = "SHORT_BLUE"
    SHORT_RED = "SHORT_RED"


class GnirsGrating(_TolerantEnum):
    D10 = "D10"
    D32 = "D32"
    D111 = "D111"


class GnirsFilter(_TolerantEnum):
    CROSS_DISPERSED = "CROSS_DISPERSED"
    ORDER6 = "ORDER6"
    ORDER5 = "ORDER5"
    ORDER4 = "ORDER4"
    ORDER3 = "ORDER3"
    ORDER2 = "ORDER2"
    ORDER1 = "ORDER1"
    H2 = "H2"
    H_ND100X = "H_ND100X"
    H2_ND100X = "H2_ND100X"
    PAH = "PAH"
    Y = "Y"
    J = "J"
    K = "K"


class GnirsFpuSlit(_TolerantEnum):
    LONG_SLIT_0_10 = "LONG_SLIT_0_10"
    LONG_SLIT_0_15 = "LONG_SLIT_0_15"
    LONG_SLIT_0_20 = "LONG_SLIT_0_20"
    LONG_SLIT_0_30 = "LONG_SLIT_0_30"
    LONG_SLIT_0_45 = "LONG_SLIT_0_45"
    LONG_SLIT_0_675 = "LONG_SLIT_0_675"
    LONG_SLIT_1_00 = "LONG_SLIT_1_00"


class GnirsFpuIfu(_TolerantEnum):
    LOW_RESOLUTION = "LOW_RESOLUTION"
    HIGH_RESOLUTION = "HIGH_RESOLUTION"


class GnirsFpuOther(_TolerantEnum):
    ACQUISITION = "ACQUISITION"
    PUPIL_VIEWER = "PUPIL_VIEWER"
    PINHOLE1 = "PINHOLE1"
    PINHOLE3 = "PINHOLE3"


class GnirsReadMode(_TolerantEnum):
    VERY_BRIGHT = "VERY_BRIGHT"
    BRIGHT = "BRIGHT"
    FAINT = "FAINT"
    VERY_FAINT = "VERY_FAINT"


class GnirsWellDepth(_TolerantEnum):
    SHALLOW = "SHALLOW"
    DEEP = "DEEP"


class GnirsAcquisitionType(_TolerantEnum):
    VERY_BRIGHT = "VERY_BRIGHT"
    BRIGHT = "BRIGHT"
    FAINT = "FAINT"


class GnirsDecker(_TolerantEnum):
    ACQUISITION = "ACQUISITION"
    PUPIL_VIEWER = "PUPIL_VIEWER"
    SHORT_CAM_CROSS_DISPERSED = "SHORT_CAM_CROSS_DISPERSED"
    LONG_CAM_LONG_SLIT = "LONG_CAM_LONG_SLIT"
    SHORT_CAM_LONG_SLIT = "SHORT_CAM_LONG_SLIT"
    LONG_CAM_CROSS_DISPERSED = "LONG_CAM_CROSS_DISPERSED"
    LOW_RESOLUTION_IFU = "LOW_RESOLUTION_IFU"
    HIGH_RESOLUTION_IFU = "HIGH_RESOLUTION_IFU"


class ItcType(_TolerantEnum):
    FLAMINGOS_2_IMAGING = "FLAMINGOS_2_IMAGING"
    GHOST_IFU = "GHOST_IFU"
    GMOS_NORTH_IMAGING = "GMOS_NORTH_IMAGING"
    GMOS_SOUTH_IMAGING = "GMOS_SOUTH_IMAGING"
    GNIRS_IMAGING = "GNIRS_IMAGING"
    SCIENCE_ONLY_SPECTROSCOPY = "SCIENCE_ONLY_SPECTROSCOPY"
    GNIRS_SPECTROSCOPY = "GNIRS_SPECTROSCOPY"
    SPECTROSCOPY = "SPECTROSCOPY"


class LineFluxIntegratedUnits(_TolerantEnum):
    W_PER_M_SQUARED = "W_PER_M_SQUARED"
    ERG_PER_S_PER_CM_SQUARED = "ERG_PER_S_PER_CM_SQUARED"


class LineFluxSurfaceUnits(_TolerantEnum):
    W_PER_M_SQUARED_PER_ARCSEC_SQUARED = "W_PER_M_SQUARED_PER_ARCSEC_SQUARED"
    ERG_PER_S_PER_CM_SQUARED_PER_ARCSEC_SQUARED = (
        "ERG_PER_S_PER_CM_SQUARED_PER_ARCSEC_SQUARED"
    )


class ObsActiveStatus(_TolerantEnum):
    ACTIVE = "ACTIVE"
    INACTIVE = "INACTIVE"


class ObsStatus(_TolerantEnum):
    NEW = "NEW"
    INCLUDED = "INCLUDED"
    PROPOSED = "PROPOSED"
    APPROVED = "APPROVED"
    READY = "READY"
    ONGOING = "ONGOING"
    OBSERVED = "OBSERVED"


class TimingWindowInclusion(_TolerantEnum):
    INCLUDE = "INCLUDE"
    EXCLUDE = "EXCLUDE"


class ArchiveDuplicationState(_TolerantEnum):
    NOT_CHECKED = "NOT_CHECKED"
    NOT_APPLICABLE = "NOT_APPLICABLE"
    CHECKED = "CHECKED"
    ERROR = "ERROR"


class ExecutionState(_TolerantEnum):
    NOT_DEFINED = "NOT_DEFINED"
    NOT_STARTED = "NOT_STARTED"
    ONGOING = "ONGOING"
    COMPLETED = "COMPLETED"
    DECLARED_COMPLETE = "DECLARED_COMPLETE"
    DECLARED_ONGOING = "DECLARED_ONGOING"


class ConfigurationRequestStatus(_TolerantEnum):
    REQUESTED = "REQUESTED"
    APPROVED = "APPROVED"
    DENIED = "DENIED"
    WITHDRAWN = "WITHDRAWN"


class TooTriggerStatus(_TolerantEnum):
    REQUESTED = "REQUESTED"
    ACCEPTED = "ACCEPTED"
    DECLINED = "DECLINED"
    WITHDRAWN = "WITHDRAWN"
    SUPERSEDED = "SUPERSEDED"


class ObservationPriority(_TolerantEnum):
    LOW = "LOW"
    MEDIUM = "MEDIUM"
    HIGH = "HIGH"


class ObservationValidationCode(_TolerantEnum):
    CONFIGURATION_ERROR = "CONFIGURATION_ERROR"
    CFP_ERROR = "CFP_ERROR"
    ITC_ERROR = "ITC_ERROR"
    CONFIG_REQUEST_UNAVAILABLE = "CONFIG_REQUEST_UNAVAILABLE"
    CONFIG_REQUEST_NOT_REQUESTED = "CONFIG_REQUEST_NOT_REQUESTED"
    CONFIG_REQUEST_DENIED = "CONFIG_REQUEST_DENIED"
    CONFIG_REQUEST_PENDING = "CONFIG_REQUEST_PENDING"
    TOO_ACTIVATION_UNAPPROVED = "TOO_ACTIVATION_UNAPPROVED"
    GENERIC_WARNING = "GENERIC_WARNING"
    LOW_TOTAL_SIGNAL_TO_NOISE = "LOW_TOTAL_SIGNAL_TO_NOISE"
    CONDITIONS_UNLIKELY = "CONDITIONS_UNLIKELY"
    CONFIGURATION_WARNING = "CONFIGURATION_WARNING"
    TOO_ACTIVATION_UNEXPECTED = "TOO_ACTIVATION_UNEXPECTED"
    CFP_WARNING = "CFP_WARNING"
    "Available on: development."


class ObserveClass(_TolerantEnum):
    SCIENCE = "SCIENCE"
    NIGHT_CAL = "NIGHT_CAL"
    ACQUISITION = "ACQUISITION"
    DAY_CAL = "DAY_CAL"


class PlanetSpectrum(_TolerantEnum):
    MARS = "MARS"
    JUPITER = "JUPITER"
    SATURN = "SATURN"
    URANUS = "URANUS"
    NEPTUNE = "NEPTUNE"


class PlanetaryNebulaSpectrum(_TolerantEnum):
    NGC7009 = "NGC7009"
    IC5117 = "IC5117"


class PosAngleConstraintMode(_TolerantEnum):
    UNBOUNDED = "UNBOUNDED"
    FIXED = "FIXED"
    ALLOW_FLIP = "ALLOW_FLIP"
    AVERAGE_PARALLACTIC = "AVERAGE_PARALLACTIC"
    PARALLACTIC_OVERRIDE = "PARALLACTIC_OVERRIDE"


class ProgramStatus(_TolerantEnum):
    ACTIVE = "ACTIVE"
    INACTIVE = "INACTIVE"
    COMPLETE = "COMPLETE"
    INCOMPLETE = "INCOMPLETE"


class ProgramType(_TolerantEnum):
    CALIBRATION = "CALIBRATION"
    COMMISSIONING = "COMMISSIONING"
    ENGINEERING = "ENGINEERING"
    EXAMPLE = "EXAMPLE"
    KECK = "KECK"
    LIBRARY = "LIBRARY"
    MONITORING = "MONITORING"
    SCIENCE = "SCIENCE"
    SUBARU = "SUBARU"
    SYSTEM = "SYSTEM"


class ProposalStatus(_TolerantEnum):
    NOT_SUBMITTED = "NOT_SUBMITTED"
    SUBMITTED = "SUBMITTED"
    ACCEPTED = "ACCEPTED"
    NOT_ACCEPTED = "NOT_ACCEPTED"


class QuasarSpectrum(_TolerantEnum):
    QS0 = "QS0"
    QS02 = "QS02"


class ScienceMode(_TolerantEnum):
    IMAGING = "IMAGING"
    SPECTROSCOPY = "SPECTROSCOPY"


class ScienceBand(_TolerantEnum):
    BAND1 = "BAND1"
    BAND2 = "BAND2"
    BAND3 = "BAND3"
    BAND4 = "BAND4"


class ScienceSubtype(_TolerantEnum):
    CLASSICAL = "CLASSICAL"
    DIRECTORS_TIME = "DIRECTORS_TIME"
    FAST_TURNAROUND = "FAST_TURNAROUND"
    LARGE_PROGRAM = "LARGE_PROGRAM"
    POOR_WEATHER = "POOR_WEATHER"
    QUEUE = "QUEUE"
    DEMO_SCIENCE = "DEMO_SCIENCE"
    SYSTEM_VERIFICATION = "SYSTEM_VERIFICATION"


class SequenceCommand(_TolerantEnum):
    ABORT = "ABORT"
    CONTINUE = "CONTINUE"
    PAUSE = "PAUSE"
    START = "START"
    STOP = "STOP"


class SequenceType(_TolerantEnum):
    ACQUISITION = "ACQUISITION"
    SCIENCE = "SCIENCE"


class Site(_TolerantEnum):
    GN = "GN"
    GS = "GS"


class SkyBackground(_TolerantEnum):
    DARKEST = "DARKEST"
    DARK = "DARK"
    GRAY = "GRAY"
    BRIGHT = "BRIGHT"


class SlewStage(_TolerantEnum):
    START_SLEW = "START_SLEW"
    END_SLEW = "END_SLEW"


class ImagingCapability(_TolerantEnum):
    SPECKLE = "SPECKLE"
    WIDE_FIELD = "WIDE_FIELD"


class SpectroscopyCapability(_TolerantEnum):
    NOD_AND_SHUFFLE = "NOD_AND_SHUFFLE"
    POLARIMETRY = "POLARIMETRY"
    CORONAGRAPHY = "CORONAGRAPHY"


class StellarLibrarySpectrum(_TolerantEnum):
    O5_V = "O5_V"
    O8_III = "O8_III"
    O9_V_CALSPEC = "O9_V_CALSPEC"
    O9_5_V_CALSPEC = "O9_5_V_CALSPEC"
    B0_V = "B0_V"
    B0_5_V_CALSPEC = "B0_5_V_CALSPEC"
    B3_V_CALSPEC = "B3_V_CALSPEC"
    B5_7_V = "B5_7_V"
    B5_III = "B5_III"
    B5_I = "B5_I"
    B9_III_CALSPEC = "B9_III_CALSPEC"
    A0_I = "A0_I"
    A0_III = "A0_III"
    A0_III_CALSPEC = "A0_III_CALSPEC"
    A0_V = "A0_V"
    A0_V_CALSPEC = "A0_V_CALSPEC"
    A1_V_CALSPEC = "A1_V_CALSPEC"
    A2_V_CALSPEC = "A2_V_CALSPEC"
    A3_V_CALSPEC = "A3_V_CALSPEC"
    A4_V_CALSPEC = "A4_V_CALSPEC"
    A5_III = "A5_III"
    A5_V = "A5_V"
    A5_V_CALSPEC = "A5_V_CALSPEC"
    A6_V_CALSPEC = "A6_V_CALSPEC"
    A8_III_CALSPEC = "A8_III_CALSPEC"
    F0_I = "F0_I"
    F0_I_PICKLES_IRTF = "F0_I_PICKLES_IRTF"
    F0_II_PICKLES_IRTF = "F0_II_PICKLES_IRTF"
    F0_III = "F0_III"
    F0_III_PICKLES_IRTF = "F0_III_PICKLES_IRTF"
    F0_IV_PICKLES_IRTF = "F0_IV_PICKLES_IRTF"
    F0_V = "F0_V"
    F0_V_PICKLES_IRTF = "F0_V_PICKLES_IRTF"
    F2_II_PICKLES_IRTF = "F2_II_PICKLES_IRTF"
    F2_III_PICKLES_IRTF = "F2_III_PICKLES_IRTF"
    F2_V_PICKLES_IRTF = "F2_V_PICKLES_IRTF"
    F4_V_CALSPEC = "F4_V_CALSPEC"
    F5_I = "F5_I"
    F5_I_PICKLES_IRTF = "F5_I_PICKLES_IRTF"
    F5_III = "F5_III"
    F5_III_PICKLES_IRTF = "F5_III_PICKLES_IRTF"
    F5_V = "F5_V"
    F5_V_PICKLES_IRTF = "F5_V_PICKLES_IRTF"
    F5_V_W = "F5_V_W"
    F6_V_R = "F6_V_R"
    F7_V_CALSPEC = "F7_V_CALSPEC"
    F8_I_PICKLES_IRTF = "F8_I_PICKLES_IRTF"
    F8_IV_CALSPEC = "F8_IV_CALSPEC"
    F8_V_PICKLES_IRTF = "F8_V_PICKLES_IRTF"
    G0_I = "G0_I"
    G0_I_PICKLES_IRTF = "G0_I_PICKLES_IRTF"
    G0_III = "G0_III"
    G0_V = "G0_V"
    G0_V_CALSPEC = "G0_V_CALSPEC"
    G0_V_W = "G0_V_W"
    G0_V_R = "G0_V_R"
    G1_V_CALSPEC = "G1_V_CALSPEC"
    G2_I_PICKLES_IRTF = "G2_I_PICKLES_IRTF"
    G2_IV_PICKLES_IRTF = "G2_IV_PICKLES_IRTF"
    G2_V = "G2_V"
    G2_V_CALSPEC = "G2_V_CALSPEC"
    G3_V_CALSPEC = "G3_V_CALSPEC"
    G5_I = "G5_I"
    G5_I_PICKLES_IRTF = "G5_I_PICKLES_IRTF"
    G5_III = "G5_III"
    G5_III_PICKLES_IRTF = "G5_III_PICKLES_IRTF"
    G5_III_W = "G5_III_W"
    G5_III_R = "G5_III_R"
    G5_V = "G5_V"
    G5_V_CALSPEC = "G5_V_CALSPEC"
    G5_V_W = "G5_V_W"
    G5_V_R = "G5_V_R"
    G7_III_CALSPEC = "G7_III_CALSPEC"
    G8_I_PICKLES_IRTF = "G8_I_PICKLES_IRTF"
    G8_III_PICKLES_IRTF = "G8_III_PICKLES_IRTF"
    G8_V_PICKLES_IRTF = "G8_V_PICKLES_IRTF"
    K0_III = "K0_III"
    K0_III_PICKLES_IRTF = "K0_III_PICKLES_IRTF"
    K0_III_W = "K0_III_W"
    K0_III_R = "K0_III_R"
    K0_IV_PICKLES_IRTF = "K0_IV_PICKLES_IRTF"
    K0_V = "K0_V"
    K0_V_PICKLES_IRTF = "K0_V_PICKLES_IRTF"
    K0_V_R = "K0_V_R"
    K0_5_III_CALSPEC = "K0_5_III_CALSPEC"
    K0_1_II = "K0_1_II"
    K1_5_III_CALSPEC = "K1_5_III_CALSPEC"
    K2_I_PICKLES_IRTF = "K2_I_PICKLES_IRTF"
    K2_III_PICKLES_IRTF = "K2_III_PICKLES_IRTF"
    K2_V_PICKLES_IRTF = "K2_V_PICKLES_IRTF"
    K3_II_PICKLES_IRTF = "K3_II_PICKLES_IRTF"
    K3_III_PICKLES_IRTF = "K3_III_PICKLES_IRTF"
    K3_V_PICKLES_IRTF = "K3_V_PICKLES_IRTF"
    K4_I = "K4_I"
    K4_I_PICKLES_IRTF = "K4_I_PICKLES_IRTF"
    K4_III = "K4_III"
    K4_III_PICKLES_IRTF = "K4_III_PICKLES_IRTF"
    K4_III_W = "K4_III_W"
    K4_III_R = "K4_III_R"
    K4_V = "K4_V"
    K5_III_PICKLES_IRTF = "K5_III_PICKLES_IRTF"
    K5_V_PICKLES_IRTF = "K5_V_PICKLES_IRTF"
    M0_III = "M0_III"
    M0_III_PICKLES_IRTF = "M0_III_PICKLES_IRTF"
    M0_V = "M0_V"
    M0_V_PICKLES_IRTF = "M0_V_PICKLES_IRTF"
    M1_III_PICKLES_IRTF = "M1_III_PICKLES_IRTF"
    M1_V_PICKLES_IRTF = "M1_V_PICKLES_IRTF"
    M2_I_PICKLES_IRTF = "M2_I_PICKLES_IRTF"
    M2_III_PICKLES_IRTF = "M2_III_PICKLES_IRTF"
    M2_V_PICKLES_IRTF = "M2_V_PICKLES_IRTF"
    M3_III = "M3_III"
    M3_III_PICKLES_IRTF = "M3_III_PICKLES_IRTF"
    M3_V = "M3_V"
    M3_V_PICKLES_IRTF = "M3_V_PICKLES_IRTF"
    M4_III_PICKLES_IRTF = "M4_III_PICKLES_IRTF"
    M4_V_PICKLES_IRTF = "M4_V_PICKLES_IRTF"
    M5_V_PICKLES_IRTF = "M5_V_PICKLES_IRTF"
    M6_III = "M6_III"
    M6_III_PICKLES_IRTF = "M6_III_PICKLES_IRTF"
    M6_V = "M6_V"
    M7_III_PICKLES_IRTF = "M7_III_PICKLES_IRTF"
    M8_III_PICKLES_IRTF = "M8_III_PICKLES_IRTF"
    M9_III = "M9_III"
    SD_B_CALSPEC = "SD_B_CALSPEC"
    SD_F8_CALSPEC = "SD_F8_CALSPEC"
    SD_O_CALSPEC = "SD_O_CALSPEC"
    DA08_CALSPEC = "DA08_CALSPEC"
    DA09_CALSPEC = "DA09_CALSPEC"
    DA12_CALSPEC = "DA12_CALSPEC"
    DA15_CALSPEC = "DA15_CALSPEC"
    DA18_CALSPEC = "DA18_CALSPEC"
    DA24_CALSPEC = "DA24_CALSPEC"
    DA28_CALSPEC = "DA28_CALSPEC"
    DA30_CALSPEC = "DA30_CALSPEC"
    DA31_CALSPEC = "DA31_CALSPEC"
    DA33_CALSPEC = "DA33_CALSPEC"
    DA36_CALSPEC = "DA36_CALSPEC"
    DA38_CALSPEC = "DA38_CALSPEC"
    DA48_CALSPEC = "DA48_CALSPEC"
    DA57_CALSPEC = "DA57_CALSPEC"
    DBQ40_CALSPEC = "DBQ40_CALSPEC"
    DBQA50_CALSPEC = "DBQA50_CALSPEC"
    DO20_CALSPEC = "DO20_CALSPEC"
    T2800_K = "T2800_K"
    T2600_K = "T2600_K"
    T2400_K = "T2400_K"
    T2200_K = "T2200_K"
    T2000_K = "T2000_K"
    T1800_K = "T1800_K"
    T1600_K = "T1600_K"
    T1400_K = "T1400_K"
    T1200_K = "T1200_K"
    T1000_K = "T1000_K"
    T0900_K = "T0900_K"
    T0800_K = "T0800_K"
    T0600_K = "T0600_K"
    T0400_K = "T0400_K"


class StepStage(_TolerantEnum):
    ABORT = "ABORT"
    CONTINUE = "CONTINUE"
    END_CONFIGURE = "END_CONFIGURE"
    END_OBSERVE = "END_OBSERVE"
    END_STEP = "END_STEP"
    PAUSE = "PAUSE"
    START_CONFIGURE = "START_CONFIGURE"
    START_OBSERVE = "START_OBSERVE"
    START_STEP = "START_STEP"
    STOP = "STOP"


class TacCategory(_TolerantEnum):
    SMALL_BODIES = "SMALL_BODIES"
    PLANETARY_ATMOSPHERES = "PLANETARY_ATMOSPHERES"
    PLANETARY_SURFACES = "PLANETARY_SURFACES"
    SOLAR_SYSTEM_OTHER = "SOLAR_SYSTEM_OTHER"
    EXOPLANET_RADIAL_VELOCITIES = "EXOPLANET_RADIAL_VELOCITIES"
    EXOPLANET_ATMOSPHERES_ACTIVITY = "EXOPLANET_ATMOSPHERES_ACTIVITY"
    EXOPLANET_TRANSITS = "EXOPLANET_TRANSITS"
    EXOPLANET_HOST_STAR = "EXOPLANET_HOST_STAR"
    EXOPLANET_OTHER = "EXOPLANET_OTHER"
    STELLAR_ASTROPHYSICS = "STELLAR_ASTROPHYSICS"
    STELLAR_POPULATIONS = "STELLAR_POPULATIONS"
    STAR_FORMATION = "STAR_FORMATION"
    GASEOUS_ASTROPHYSICS = "GASEOUS_ASTROPHYSICS"
    STELLAR_REMNANTS = "STELLAR_REMNANTS"
    GALACTIC_OTHER = "GALACTIC_OTHER"
    COSMOLOGY = "COSMOLOGY"
    CLUSTERS_OF_GALAXIES = "CLUSTERS_OF_GALAXIES"
    HIGH_Z_UNIVERSE = "HIGH_Z_UNIVERSE"
    LOW_Z_UNIVERSE = "LOW_Z_UNIVERSE"
    ACTIVE_GALAXIES = "ACTIVE_GALAXIES"
    EXTRAGALACTIC_OTHER = "EXTRAGALACTIC_OTHER"


class TargetDisposition(_TolerantEnum):
    SCIENCE = "SCIENCE"
    CALIBRATION = "CALIBRATION"
    BLIND_OFFSET = "BLIND_OFFSET"


class CalibrationRole(_TolerantEnum):
    TWILIGHT = "TWILIGHT"
    PHOTOMETRIC = "PHOTOMETRIC"
    SPECTROPHOTOMETRIC = "SPECTROPHOTOMETRIC"
    TELLURIC = "TELLURIC"
    DAYTIME_PINHOLE = "DAYTIME_PINHOLE"


class ArcType(_TolerantEnum):
    EMPTY = "EMPTY"
    FULL = "FULL"
    PARTIAL = "PARTIAL"


class BasePositionType(_TolerantEnum):
    SINGLE_TARGET = "SINGLE_TARGET"
    ASTERISM = "ASTERISM"
    EXPLICIT_BASE = "EXPLICIT_BASE"


class TimeChargeCorrectionOp(_TolerantEnum):
    ADD = "ADD"
    SUBTRACT = "SUBTRACT"


class ConsiderForBand3(_TolerantEnum):
    UNSET = "UNSET"
    CONSIDER = "CONSIDER"
    DO_NOT_CONSIDER = "DO_NOT_CONSIDER"


class TooActivation(_TolerantEnum):
    NONE = "NONE"
    RAPID = "RAPID"
    INTERRUPTING = "INTERRUPTING"


class UserType(_TolerantEnum):
    GUEST = "GUEST"
    STANDARD = "STANDARD"
    SERVICE = "SERVICE"


class WaterVapor(_TolerantEnum):
    VERY_DRY = "VERY_DRY"
    DRY = "DRY"
    MEDIAN = "MEDIAN"
    WET = "WET"


class ObservationWorkflowState(_TolerantEnum):
    INACTIVE = "INACTIVE"
    UNDEFINED = "UNDEFINED"
    UNAPPROVED = "UNAPPROVED"
    DEFINED = "DEFINED"
    READY = "READY"
    ONGOING = "ONGOING"
    COMPLETED = "COMPLETED"
