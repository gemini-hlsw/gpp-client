__all__ = [
    "ConditionsMeasurementSource",
    "SeeingTrend",
    "ConditionsExpectationType",
    "FilterType",
    "ProposalStatus",
    "AtomExecutionState",
    "AtomStage",
    "Breakpoint",
    "CallForProposalsType",
    "EditType",
    "EmailStatus",
    "ExecutionEventType",
    "GcalArc",
    "GcalContinuum",
    "GcalDiffuser",
    "GcalFilter",
    "GcalShutter",
    "GmosAmpCount",
    "GmosCustomSlitWidth",
    "GmosDtax",
    "GmosEOffsetting",
    "GmosGratingOrder",
    "GmosNorthDetector",
    "GmosNorthStageMode",
    "GmosSouthDetector",
    "GmosSouthStageMode",
    "GuideState",
    "UserInvitationStatus",
    "MosPreImaging",
    "Partner",
    "PartnerLinkType",
    "ProgramUserRole",
    "ProgramUserSupportRoleType",
    "Ignore",
    "SmartGcalType",
    "StepExecutionState",
    "StepType",
    "TimeAccountingCategory",
    "AttachmentType",
    "Band",
    "BrightnessIntegratedUnits",
    "BrightnessSurfaceUnits",
    "CatalogName",
    "ChargeClass",
    "CloudExtinction",
    "ObservingModeType",
    "CoolStarTemperature",
    "DatasetQaState",
    "DatasetStage",
    "EducationalStatus",
    "EphemerisKeyType",
    "Existence",
    "Flamingos2Disperser",
    "Flamingos2Filter",
    "Flamingos2Fpu",
    "FluxDensityContinuumIntegratedUnits",
    "FluxDensityContinuumSurfaceUnits",
    "FocalPlane",
    "GalaxySpectrum",
    "Gender",
    "GmosAmpGain",
    "GmosAmpReadMode",
    "GmosNorthBuiltinFpu",
    "GmosNorthFilter",
    "GmosNorthGrating",
    "GmosRoi",
    "GmosSouthBuiltinFpu",
    "GmosSouthFilter",
    "GmosSouthGrating",
    "GmosXBinning",
    "GmosYBinning",
    "GuideProbe",
    "HiiRegionSpectrum",
    "ImageQuality",
    "Instrument",
    "LineFluxIntegratedUnits",
    "LineFluxSurfaceUnits",
    "ObsActiveStatus",
    "ObsStatus",
    "TimingWindowInclusion",
    "ExecutionState",
    "ConfigurationRequestStatus",
    "ObservationValidationCode",
    "ObserveClass",
    "PlanetSpectrum",
    "PlanetaryNebulaSpectrum",
    "PosAngleConstraintMode",
    "ProgramType",
    "QuasarSpectrum",
    "ScienceMode",
    "ScienceBand",
    "ScienceSubtype",
    "SequenceCommand",
    "SequenceType",
    "Site",
    "SkyBackground",
    "SlewStage",
    "SpectroscopyCapabilities",
    "StellarLibrarySpectrum",
    "StepStage",
    "TacCategory",
    "CalibrationRole",
    "TimeChargeCorrectionOp",
    "ToOActivation",
    "UserType",
    "WaterVapor",
    "ObservationWorkflowState",
]

from enum import Enum


class ConditionsMeasurementSource(str, Enum):
    OBSERVER = "OBSERVER"


class SeeingTrend(str, Enum):
    GETTING_BETTER = "GETTING_BETTER"
    GETTING_WORSE = "GETTING_WORSE"
    STAYING_THE_SAME = "STAYING_THE_SAME"
    VARIABLE = "VARIABLE"


class ConditionsExpectationType(str, Enum):
    CLEAR_SKIES = "CLEAR_SKIES"
    FOG = "FOG"
    THICK_CLOUDS = "THICK_CLOUDS"
    THIN_CLOUDS = "THIN_CLOUDS"


class FilterType(str, Enum):
    BroadBand = "BroadBand"
    Combination = "Combination"
    Engineering = "Engineering"
    NarrowBand = "NarrowBand"
    Spectroscopic = "Spectroscopic"


class ProposalStatus(str, Enum):
    NOT_SUBMITTED = "NOT_SUBMITTED"
    SUBMITTED = "SUBMITTED"
    ACCEPTED = "ACCEPTED"
    NOT_ACCEPTED = "NOT_ACCEPTED"


class AtomExecutionState(str, Enum):
    NOT_STARTED = "NOT_STARTED"
    ONGOING = "ONGOING"
    COMPLETED = "COMPLETED"
    ABANDONED = "ABANDONED"


class AtomStage(str, Enum):
    END_ATOM = "END_ATOM"
    START_ATOM = "START_ATOM"


class Breakpoint(str, Enum):
    ENABLED = "ENABLED"
    DISABLED = "DISABLED"


class CallForProposalsType(str, Enum):
    DEMO_SCIENCE = "DEMO_SCIENCE"
    DIRECTORS_TIME = "DIRECTORS_TIME"
    FAST_TURNAROUND = "FAST_TURNAROUND"
    LARGE_PROGRAM = "LARGE_PROGRAM"
    POOR_WEATHER = "POOR_WEATHER"
    REGULAR_SEMESTER = "REGULAR_SEMESTER"
    SYSTEM_VERIFICATION = "SYSTEM_VERIFICATION"


class EditType(str, Enum):
    CREATED = "CREATED"
    UPDATED = "UPDATED"
    DELETED_CAL = "DELETED_CAL"


class EmailStatus(str, Enum):
    QUEUED = "QUEUED"
    REJECTED = "REJECTED"
    ACCEPTED = "ACCEPTED"
    DELIVERED = "DELIVERED"
    PERMANENT_FAILURE = "PERMANENT_FAILURE"
    TEMPORARY_FAILURE = "TEMPORARY_FAILURE"


class ExecutionEventType(str, Enum):
    SEQUENCE = "SEQUENCE"
    SLEW = "SLEW"
    ATOM = "ATOM"
    STEP = "STEP"
    DATASET = "DATASET"


class GcalArc(str, Enum):
    AR_ARC = "AR_ARC"
    TH_AR_ARC = "TH_AR_ARC"
    CU_AR_ARC = "CU_AR_ARC"
    XE_ARC = "XE_ARC"


class GcalContinuum(str, Enum):
    IR_GREY_BODY_LOW = "IR_GREY_BODY_LOW"
    IR_GREY_BODY_HIGH = "IR_GREY_BODY_HIGH"
    QUARTZ_HALOGEN5 = "QUARTZ_HALOGEN5"
    QUARTZ_HALOGEN100 = "QUARTZ_HALOGEN100"


class GcalDiffuser(str, Enum):
    IR = "IR"
    VISIBLE = "VISIBLE"


class GcalFilter(str, Enum):
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


class GcalShutter(str, Enum):
    OPEN = "OPEN"
    CLOSED = "CLOSED"


class GmosAmpCount(str, Enum):
    THREE = "THREE"
    SIX = "SIX"
    TWELVE = "TWELVE"


class GmosCustomSlitWidth(str, Enum):
    CUSTOM_WIDTH_0_25 = "CUSTOM_WIDTH_0_25"
    CUSTOM_WIDTH_0_50 = "CUSTOM_WIDTH_0_50"
    CUSTOM_WIDTH_0_75 = "CUSTOM_WIDTH_0_75"
    CUSTOM_WIDTH_1_00 = "CUSTOM_WIDTH_1_00"
    CUSTOM_WIDTH_1_50 = "CUSTOM_WIDTH_1_50"
    CUSTOM_WIDTH_2_00 = "CUSTOM_WIDTH_2_00"
    CUSTOM_WIDTH_5_00 = "CUSTOM_WIDTH_5_00"


class GmosDtax(str, Enum):
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


class GmosEOffsetting(str, Enum):
    ON = "ON"
    OFF = "OFF"


class GmosGratingOrder(str, Enum):
    ZERO = "ZERO"
    ONE = "ONE"
    TWO = "TWO"


class GmosNorthDetector(str, Enum):
    E2_V = "E2_V"
    HAMAMATSU = "HAMAMATSU"


class GmosNorthStageMode(str, Enum):
    NO_FOLLOW = "NO_FOLLOW"
    FOLLOW_XYZ = "FOLLOW_XYZ"
    FOLLOW_XY = "FOLLOW_XY"
    FOLLOW_Z = "FOLLOW_Z"


class GmosSouthDetector(str, Enum):
    E2_V = "E2_V"
    HAMAMATSU = "HAMAMATSU"


class GmosSouthStageMode(str, Enum):
    NO_FOLLOW = "NO_FOLLOW"
    FOLLOW_XYZ = "FOLLOW_XYZ"
    FOLLOW_XY = "FOLLOW_XY"
    FOLLOW_Z = "FOLLOW_Z"


class GuideState(str, Enum):
    ENABLED = "ENABLED"
    DISABLED = "DISABLED"


class UserInvitationStatus(str, Enum):
    PENDING = "PENDING"
    REDEEMED = "REDEEMED"
    DECLINED = "DECLINED"
    REVOKED = "REVOKED"


class MosPreImaging(str, Enum):
    IS_MOS_PRE_IMAGING = "IS_MOS_PRE_IMAGING"
    IS_NOT_MOS_PRE_IMAGING = "IS_NOT_MOS_PRE_IMAGING"


class Partner(str, Enum):
    AR = "AR"
    BR = "BR"
    CA = "CA"
    CL = "CL"
    KR = "KR"
    UH = "UH"
    US = "US"


class PartnerLinkType(str, Enum):
    HAS_PARTNER = "HAS_PARTNER"
    HAS_NON_PARTNER = "HAS_NON_PARTNER"
    HAS_UNSPECIFIED_PARTNER = "HAS_UNSPECIFIED_PARTNER"


class ProgramUserRole(str, Enum):
    PI = "PI"
    COI = "COI"
    COI_RO = "COI_RO"
    EXTERNAL = "EXTERNAL"
    SUPPORT_PRIMARY = "SUPPORT_PRIMARY"
    SUPPORT_SECONDARY = "SUPPORT_SECONDARY"


class ProgramUserSupportRoleType(str, Enum):
    STAFF = "STAFF"
    PARTNER = "PARTNER"


class Ignore(str, Enum):
    IGNORE = "IGNORE"


class SmartGcalType(str, Enum):
    ARC = "ARC"
    FLAT = "FLAT"
    DAY_BASELINE = "DAY_BASELINE"
    NIGHT_BASELINE = "NIGHT_BASELINE"


class StepExecutionState(str, Enum):
    NOT_STARTED = "NOT_STARTED"
    ONGOING = "ONGOING"
    ABORTED = "ABORTED"
    COMPLETED = "COMPLETED"
    STOPPED = "STOPPED"
    ABANDONED = "ABANDONED"


class StepType(str, Enum):
    BIAS = "BIAS"
    DARK = "DARK"
    GCAL = "GCAL"
    SCIENCE = "SCIENCE"
    SMART_GCAL = "SMART_GCAL"


class TimeAccountingCategory(str, Enum):
    AR = "AR"
    BR = "BR"
    CA = "CA"
    CFHT = "CFHT"
    CL = "CL"
    DD = "DD"
    DS = "DS"
    GT = "GT"
    JP = "JP"
    KECK = "KECK"
    KR = "KR"
    LP = "LP"
    LTP = "LTP"
    SV = "SV"
    UH = "UH"
    US = "US"


class AttachmentType(str, Enum):
    SCIENCE = "SCIENCE"
    TEAM = "TEAM"
    FINDER = "FINDER"
    MOS_MASK = "MOS_MASK"
    PRE_IMAGING = "PRE_IMAGING"
    CUSTOM_SED = "CUSTOM_SED"


class Band(str, Enum):
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


class BrightnessIntegratedUnits(str, Enum):
    VEGA_MAGNITUDE = "VEGA_MAGNITUDE"
    AB_MAGNITUDE = "AB_MAGNITUDE"
    JANSKY = "JANSKY"
    W_PER_M_SQUARED_PER_UM = "W_PER_M_SQUARED_PER_UM"
    ERG_PER_S_PER_CM_SQUARED_PER_A = "ERG_PER_S_PER_CM_SQUARED_PER_A"
    ERG_PER_S_PER_CM_SQUARED_PER_HZ = "ERG_PER_S_PER_CM_SQUARED_PER_HZ"


class BrightnessSurfaceUnits(str, Enum):
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


class CatalogName(str, Enum):
    SIMBAD = "SIMBAD"
    IMPORT = "IMPORT"
    GAIA = "GAIA"


class ChargeClass(str, Enum):
    NON_CHARGED = "NON_CHARGED"
    PARTNER = "PARTNER"
    PROGRAM = "PROGRAM"


class CloudExtinction(str, Enum):
    POINT_ONE = "POINT_ONE"
    POINT_THREE = "POINT_THREE"
    POINT_FIVE = "POINT_FIVE"
    ONE_POINT_ZERO = "ONE_POINT_ZERO"
    ONE_POINT_FIVE = "ONE_POINT_FIVE"
    TWO_POINT_ZERO = "TWO_POINT_ZERO"
    THREE_POINT_ZERO = "THREE_POINT_ZERO"


class ObservingModeType(str, Enum):
    GMOS_NORTH_LONG_SLIT = "GMOS_NORTH_LONG_SLIT"
    GMOS_SOUTH_LONG_SLIT = "GMOS_SOUTH_LONG_SLIT"


class CoolStarTemperature(str, Enum):
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


class DatasetQaState(str, Enum):
    PASS = "PASS"
    USABLE = "USABLE"
    FAIL = "FAIL"


class DatasetStage(str, Enum):
    END_EXPOSE = "END_EXPOSE"
    END_READOUT = "END_READOUT"
    END_WRITE = "END_WRITE"
    START_EXPOSE = "START_EXPOSE"
    START_READOUT = "START_READOUT"
    START_WRITE = "START_WRITE"


class EducationalStatus(str, Enum):
    PHD = "PHD"
    GRAD_STUDENT = "GRAD_STUDENT"
    UNDERGRAD_STUDENT = "UNDERGRAD_STUDENT"
    OTHER = "OTHER"


class EphemerisKeyType(str, Enum):
    COMET = "COMET"
    ASTEROID_NEW = "ASTEROID_NEW"
    ASTEROID_OLD = "ASTEROID_OLD"
    MAJOR_BODY = "MAJOR_BODY"
    USER_SUPPLIED = "USER_SUPPLIED"


class Existence(str, Enum):
    PRESENT = "PRESENT"
    DELETED = "DELETED"


class Flamingos2Disperser(str, Enum):
    R1200JH = "R1200JH"
    R1200HK = "R1200HK"
    R3000 = "R3000"


class Flamingos2Filter(str, Enum):
    Y = "Y"
    J = "J"
    H = "H"
    JH = "JH"
    HK = "HK"
    J_LOW = "J_LOW"
    K_LONG = "K_LONG"
    K_SHORT = "K_SHORT"
    K_BLUE = "K_BLUE"


class Flamingos2Fpu(str, Enum):
    PINHOLE = "PINHOLE"
    SUB_PIX_PINHOLE = "SUB_PIX_PINHOLE"
    LONG_SLIT_1 = "LONG_SLIT_1"
    LONG_SLIT_2 = "LONG_SLIT_2"
    LONG_SLIT_3 = "LONG_SLIT_3"
    LONG_SLIT_4 = "LONG_SLIT_4"
    LONG_SLIT_6 = "LONG_SLIT_6"
    LONG_SLIT_8 = "LONG_SLIT_8"


class FluxDensityContinuumIntegratedUnits(str, Enum):
    W_PER_M_SQUARED_PER_UM = "W_PER_M_SQUARED_PER_UM"
    ERG_PER_S_PER_CM_SQUARED_PER_A = "ERG_PER_S_PER_CM_SQUARED_PER_A"


class FluxDensityContinuumSurfaceUnits(str, Enum):
    W_PER_M_SQUARED_PER_UM_PER_ARCSEC_SQUARED = (
        "W_PER_M_SQUARED_PER_UM_PER_ARCSEC_SQUARED"
    )
    ERG_PER_S_PER_CM_SQUARED_PER_A_PER_ARCSEC_SQUARED = (
        "ERG_PER_S_PER_CM_SQUARED_PER_A_PER_ARCSEC_SQUARED"
    )


class FocalPlane(str, Enum):
    SINGLE_SLIT = "SINGLE_SLIT"
    MULTIPLE_SLIT = "MULTIPLE_SLIT"
    IFU = "IFU"


class GalaxySpectrum(str, Enum):
    ELLIPTICAL = "ELLIPTICAL"
    SPIRAL = "SPIRAL"


class Gender(str, Enum):
    MALE = "MALE"
    FEMALE = "FEMALE"
    OTHER = "OTHER"
    NOT_SPECIFIED = "NOT_SPECIFIED"


class GmosAmpGain(str, Enum):
    LOW = "LOW"
    HIGH = "HIGH"


class GmosAmpReadMode(str, Enum):
    SLOW = "SLOW"
    FAST = "FAST"


class GmosNorthBuiltinFpu(str, Enum):
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


class GmosNorthFilter(str, Enum):
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
    U_PRIME = "U_PRIME"


class GmosNorthGrating(str, Enum):
    B1200_G5301 = "B1200_G5301"
    R831_G5302 = "R831_G5302"
    B600_G5303 = "B600_G5303"
    R600_G5304 = "R600_G5304"
    B480_G5309 = "B480_G5309"
    R400_G5305 = "R400_G5305"
    R150_G5306 = "R150_G5306"
    R150_G5308 = "R150_G5308"


class GmosRoi(str, Enum):
    FULL_FRAME = "FULL_FRAME"
    CCD2 = "CCD2"
    CENTRAL_SPECTRUM = "CENTRAL_SPECTRUM"
    CENTRAL_STAMP = "CENTRAL_STAMP"
    TOP_SPECTRUM = "TOP_SPECTRUM"
    BOTTOM_SPECTRUM = "BOTTOM_SPECTRUM"
    CUSTOM = "CUSTOM"


class GmosSouthBuiltinFpu(str, Enum):
    BHROS = "BHROS"
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


class GmosSouthFilter(str, Enum):
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
    LYA395 = "LYA395"


class GmosSouthGrating(str, Enum):
    B1200_G5321 = "B1200_G5321"
    R831_G5322 = "R831_G5322"
    B600_G5323 = "B600_G5323"
    R600_G5324 = "R600_G5324"
    B480_G5327 = "B480_G5327"
    R400_G5325 = "R400_G5325"
    R150_G5326 = "R150_G5326"


class GmosXBinning(str, Enum):
    ONE = "ONE"
    TWO = "TWO"
    FOUR = "FOUR"


class GmosYBinning(str, Enum):
    ONE = "ONE"
    TWO = "TWO"
    FOUR = "FOUR"


class GuideProbe(str, Enum):
    PWFS_1 = "PWFS_1"
    PWFS_2 = "PWFS_2"
    GMOS_OIWFS = "GMOS_OIWFS"


class HiiRegionSpectrum(str, Enum):
    ORION_NEBULA = "ORION_NEBULA"


class ImageQuality(str, Enum):
    POINT_ONE = "POINT_ONE"
    POINT_TWO = "POINT_TWO"
    POINT_THREE = "POINT_THREE"
    POINT_FOUR = "POINT_FOUR"
    POINT_SIX = "POINT_SIX"
    POINT_EIGHT = "POINT_EIGHT"
    ONE_POINT_ZERO = "ONE_POINT_ZERO"
    ONE_POINT_FIVE = "ONE_POINT_FIVE"
    TWO_POINT_ZERO = "TWO_POINT_ZERO"


class Instrument(str, Enum):
    ACQ_CAM = "ACQ_CAM"
    BHROS = "BHROS"
    FLAMINGOS2 = "FLAMINGOS2"
    GHOST = "GHOST"
    GMOS_NORTH = "GMOS_NORTH"
    GMOS_SOUTH = "GMOS_SOUTH"
    GNIRS = "GNIRS"
    GPI = "GPI"
    GSAOI = "GSAOI"
    MICHELLE = "MICHELLE"
    NICI = "NICI"
    NIFS = "NIFS"
    NIRI = "NIRI"
    PHOENIX = "PHOENIX"
    TRECS = "TRECS"
    VISITOR = "VISITOR"
    SCORPIO = "SCORPIO"
    ALOPEKE = "ALOPEKE"
    ZORRO = "ZORRO"


class LineFluxIntegratedUnits(str, Enum):
    W_PER_M_SQUARED = "W_PER_M_SQUARED"
    ERG_PER_S_PER_CM_SQUARED = "ERG_PER_S_PER_CM_SQUARED"


class LineFluxSurfaceUnits(str, Enum):
    W_PER_M_SQUARED_PER_ARCSEC_SQUARED = "W_PER_M_SQUARED_PER_ARCSEC_SQUARED"
    ERG_PER_S_PER_CM_SQUARED_PER_ARCSEC_SQUARED = (
        "ERG_PER_S_PER_CM_SQUARED_PER_ARCSEC_SQUARED"
    )


class ObsActiveStatus(str, Enum):
    ACTIVE = "ACTIVE"
    INACTIVE = "INACTIVE"


class ObsStatus(str, Enum):
    NEW = "NEW"
    INCLUDED = "INCLUDED"
    PROPOSED = "PROPOSED"
    APPROVED = "APPROVED"
    FOR_REVIEW = "FOR_REVIEW"
    READY = "READY"
    ONGOING = "ONGOING"
    OBSERVED = "OBSERVED"


class TimingWindowInclusion(str, Enum):
    INCLUDE = "INCLUDE"
    EXCLUDE = "EXCLUDE"


class ExecutionState(str, Enum):
    NOT_DEFINED = "NOT_DEFINED"
    NOT_STARTED = "NOT_STARTED"
    ONGOING = "ONGOING"
    COMPLETED = "COMPLETED"


class ConfigurationRequestStatus(str, Enum):
    REQUESTED = "REQUESTED"
    APPROVED = "APPROVED"
    DENIED = "DENIED"
    WITHDRAWN = "WITHDRAWN"


class ObservationValidationCode(str, Enum):
    CONFIGURATION_ERROR = "CONFIGURATION_ERROR"
    CFP_ERROR = "CFP_ERROR"
    ITC_ERROR = "ITC_ERROR"
    CONFIG_REQUEST_UNAVAILABLE = "CONFIG_REQUEST_UNAVAILABLE"
    CONFIG_REQUEST_NOT_REQUESTED = "CONFIG_REQUEST_NOT_REQUESTED"
    CONFIG_REQUEST_DENIED = "CONFIG_REQUEST_DENIED"
    CONFIG_REQUEST_PENDING = "CONFIG_REQUEST_PENDING"


class ObserveClass(str, Enum):
    SCIENCE = "SCIENCE"
    PROGRAM_CAL = "PROGRAM_CAL"
    PARTNER_CAL = "PARTNER_CAL"
    ACQUISITION = "ACQUISITION"
    ACQUISITION_CAL = "ACQUISITION_CAL"
    DAY_CAL = "DAY_CAL"


class PlanetSpectrum(str, Enum):
    MARS = "MARS"
    JUPITER = "JUPITER"
    SATURN = "SATURN"
    URANUS = "URANUS"
    NEPTUNE = "NEPTUNE"


class PlanetaryNebulaSpectrum(str, Enum):
    NGC7009 = "NGC7009"
    IC5117 = "IC5117"


class PosAngleConstraintMode(str, Enum):
    UNBOUNDED = "UNBOUNDED"
    FIXED = "FIXED"
    ALLOW_FLIP = "ALLOW_FLIP"
    AVERAGE_PARALLACTIC = "AVERAGE_PARALLACTIC"
    PARALLACTIC_OVERRIDE = "PARALLACTIC_OVERRIDE"


class ProgramType(str, Enum):
    CALIBRATION = "CALIBRATION"
    ENGINEERING = "ENGINEERING"
    EXAMPLE = "EXAMPLE"
    LIBRARY = "LIBRARY"
    SCIENCE = "SCIENCE"
    SYSTEM = "SYSTEM"


class QuasarSpectrum(str, Enum):
    QS0 = "QS0"
    QS02 = "QS02"


class ScienceMode(str, Enum):
    IMAGING = "IMAGING"
    SPECTROSCOPY = "SPECTROSCOPY"


class ScienceBand(str, Enum):
    BAND1 = "BAND1"
    BAND2 = "BAND2"
    BAND3 = "BAND3"
    BAND4 = "BAND4"


class ScienceSubtype(str, Enum):
    CLASSICAL = "CLASSICAL"
    DIRECTORS_TIME = "DIRECTORS_TIME"
    FAST_TURNAROUND = "FAST_TURNAROUND"
    LARGE_PROGRAM = "LARGE_PROGRAM"
    POOR_WEATHER = "POOR_WEATHER"
    QUEUE = "QUEUE"
    DEMO_SCIENCE = "DEMO_SCIENCE"
    SYSTEM_VERIFICATION = "SYSTEM_VERIFICATION"


class SequenceCommand(str, Enum):
    ABORT = "ABORT"
    CONTINUE = "CONTINUE"
    PAUSE = "PAUSE"
    START = "START"
    STOP = "STOP"


class SequenceType(str, Enum):
    ACQUISITION = "ACQUISITION"
    SCIENCE = "SCIENCE"


class Site(str, Enum):
    GN = "GN"
    GS = "GS"


class SkyBackground(str, Enum):
    DARKEST = "DARKEST"
    DARK = "DARK"
    GRAY = "GRAY"
    BRIGHT = "BRIGHT"


class SlewStage(str, Enum):
    START_SLEW = "START_SLEW"
    END_SLEW = "END_SLEW"


class SpectroscopyCapabilities(str, Enum):
    NOD_AND_SHUFFLE = "NOD_AND_SHUFFLE"
    POLARIMETRY = "POLARIMETRY"
    CORONAGRAPHY = "CORONAGRAPHY"


class StellarLibrarySpectrum(str, Enum):
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


class StepStage(str, Enum):
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


class TacCategory(str, Enum):
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


class CalibrationRole(str, Enum):
    TWILIGHT = "TWILIGHT"
    PHOTOMETRIC = "PHOTOMETRIC"
    SPECTROPHOTOMETRIC = "SPECTROPHOTOMETRIC"
    TELLURIC = "TELLURIC"


class TimeChargeCorrectionOp(str, Enum):
    ADD = "ADD"
    SUBTRACT = "SUBTRACT"


class ToOActivation(str, Enum):
    NONE = "NONE"
    STANDARD = "STANDARD"
    RAPID = "RAPID"


class UserType(str, Enum):
    GUEST = "GUEST"
    STANDARD = "STANDARD"
    SERVICE = "SERVICE"


class WaterVapor(str, Enum):
    VERY_DRY = "VERY_DRY"
    DRY = "DRY"
    MEDIAN = "MEDIAN"
    WET = "WET"


class ObservationWorkflowState(str, Enum):
    INACTIVE = "INACTIVE"
    UNDEFINED = "UNDEFINED"
    UNAPPROVED = "UNAPPROVED"
    DEFINED = "DEFINED"
    READY = "READY"
    ONGOING = "ONGOING"
    COMPLETED = "COMPLETED"
