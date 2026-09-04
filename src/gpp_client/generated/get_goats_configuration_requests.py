from typing import Any, Optional

from pydantic import Field

from .base_model import BaseModel
from .enums import (
    CloudExtinctionPreset,
    ConfigurationRequestStatus,
    GmosNorthFilter,
    GmosNorthGrating,
    GmosSouthFilter,
    GmosSouthGrating,
    ImageQualityPreset,
    Instrument,
    ObservingModeType,
    SkyBackground,
    WaterVapor,
)


class GetGOATSConfigurationRequests(BaseModel):
    configuration_requests: "GetGOATSConfigurationRequestsConfigurationRequests" = (
        Field(alias="configurationRequests")
    )


class GetGOATSConfigurationRequestsConfigurationRequests(BaseModel):
    matches: list["GetGOATSConfigurationRequestsConfigurationRequestsMatches"]
    has_more: bool = Field(alias="hasMore")


class GetGOATSConfigurationRequestsConfigurationRequestsMatches(BaseModel):
    id: Any
    status: ConfigurationRequestStatus
    justification: Optional[Any]
    applicable_observations: list[Any] = Field(alias="applicableObservations")
    configuration: (
        "GetGOATSConfigurationRequestsConfigurationRequestsMatchesConfiguration"
    )


class GetGOATSConfigurationRequestsConfigurationRequestsMatchesConfiguration(BaseModel):
    conditions: "GetGOATSConfigurationRequestsConfigurationRequestsMatchesConfigurationConditions"
    target: Optional[
        "GetGOATSConfigurationRequestsConfigurationRequestsMatchesConfigurationTarget"
    ]
    observing_mode: Optional[
        "GetGOATSConfigurationRequestsConfigurationRequestsMatchesConfigurationObservingMode"
    ] = Field(alias="observingMode")


class GetGOATSConfigurationRequestsConfigurationRequestsMatchesConfigurationConditions(
    BaseModel
):
    image_quality: ImageQualityPreset = Field(alias="imageQuality")
    cloud_extinction: CloudExtinctionPreset = Field(alias="cloudExtinction")
    sky_background: SkyBackground = Field(alias="skyBackground")
    water_vapor: WaterVapor = Field(alias="waterVapor")


class GetGOATSConfigurationRequestsConfigurationRequestsMatchesConfigurationTarget(
    BaseModel
):
    coordinates: Optional[
        "GetGOATSConfigurationRequestsConfigurationRequestsMatchesConfigurationTargetCoordinates"
    ]


class GetGOATSConfigurationRequestsConfigurationRequestsMatchesConfigurationTargetCoordinates(
    BaseModel
):
    ra: "GetGOATSConfigurationRequestsConfigurationRequestsMatchesConfigurationTargetCoordinatesRa"
    dec: "GetGOATSConfigurationRequestsConfigurationRequestsMatchesConfigurationTargetCoordinatesDec"


class GetGOATSConfigurationRequestsConfigurationRequestsMatchesConfigurationTargetCoordinatesRa(
    BaseModel
):
    hms: Any
    degrees: Any


class GetGOATSConfigurationRequestsConfigurationRequestsMatchesConfigurationTargetCoordinatesDec(
    BaseModel
):
    dms: Any
    degrees: Any


class GetGOATSConfigurationRequestsConfigurationRequestsMatchesConfigurationObservingMode(
    BaseModel
):
    instrument: Optional[Instrument]
    mode: ObservingModeType
    gmos_north_long_slit: Optional[
        "GetGOATSConfigurationRequestsConfigurationRequestsMatchesConfigurationObservingModeGmosNorthLongSlit"
    ] = Field(alias="gmosNorthLongSlit")
    gmos_south_long_slit: Optional[
        "GetGOATSConfigurationRequestsConfigurationRequestsMatchesConfigurationObservingModeGmosSouthLongSlit"
    ] = Field(alias="gmosSouthLongSlit")
    gmos_north_imaging: Optional[
        "GetGOATSConfigurationRequestsConfigurationRequestsMatchesConfigurationObservingModeGmosNorthImaging"
    ] = Field(alias="gmosNorthImaging")
    gmos_south_imaging: Optional[
        "GetGOATSConfigurationRequestsConfigurationRequestsMatchesConfigurationObservingModeGmosSouthImaging"
    ] = Field(alias="gmosSouthImaging")


class GetGOATSConfigurationRequestsConfigurationRequestsMatchesConfigurationObservingModeGmosNorthLongSlit(
    BaseModel
):
    grating: GmosNorthGrating


class GetGOATSConfigurationRequestsConfigurationRequestsMatchesConfigurationObservingModeGmosSouthLongSlit(
    BaseModel
):
    grating: GmosSouthGrating


class GetGOATSConfigurationRequestsConfigurationRequestsMatchesConfigurationObservingModeGmosNorthImaging(
    BaseModel
):
    filters: list[GmosNorthFilter]


class GetGOATSConfigurationRequestsConfigurationRequestsMatchesConfigurationObservingModeGmosSouthImaging(
    BaseModel
):
    filters: list[GmosSouthFilter]


GetGOATSConfigurationRequests.model_rebuild()
GetGOATSConfigurationRequestsConfigurationRequests.model_rebuild()
GetGOATSConfigurationRequestsConfigurationRequestsMatches.model_rebuild()
GetGOATSConfigurationRequestsConfigurationRequestsMatchesConfiguration.model_rebuild()
GetGOATSConfigurationRequestsConfigurationRequestsMatchesConfigurationTarget.model_rebuild()
GetGOATSConfigurationRequestsConfigurationRequestsMatchesConfigurationTargetCoordinates.model_rebuild()
GetGOATSConfigurationRequestsConfigurationRequestsMatchesConfigurationObservingMode.model_rebuild()
