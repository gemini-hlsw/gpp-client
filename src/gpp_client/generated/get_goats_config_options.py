from typing import Any, Optional

from pydantic import Field

from .base_model import BaseModel
from .enums import (
    FocalPlane,
    GmosNorthBuiltinFpu,
    GmosNorthFilter,
    GmosNorthGrating,
    GmosSouthBuiltinFpu,
    GmosSouthFilter,
    GmosSouthGrating,
    Instrument,
    Site,
)


class GetGOATSConfigOptions(BaseModel):
    spectroscopy_config_options: list[
        "GetGOATSConfigOptionsSpectroscopyConfigOptions"
    ] = Field(alias="spectroscopyConfigOptions")
    imaging_config_options: list["GetGOATSConfigOptionsImagingConfigOptions"] = Field(
        alias="imagingConfigOptions"
    )


class GetGOATSConfigOptionsSpectroscopyConfigOptions(BaseModel):
    name: Any
    instrument: Instrument
    site: Site
    focal_plane: FocalPlane = Field(alias="focalPlane")
    fpu_label: Any = Field(alias="fpuLabel")
    disperser_label: Any = Field(alias="disperserLabel")
    filter_label: Optional[Any] = Field(alias="filterLabel")
    slit_width: "GetGOATSConfigOptionsSpectroscopyConfigOptionsSlitWidth" = Field(
        alias="slitWidth"
    )
    resolution: Any
    wavelength_min: "GetGOATSConfigOptionsSpectroscopyConfigOptionsWavelengthMin" = (
        Field(alias="wavelengthMin")
    )
    wavelength_max: "GetGOATSConfigOptionsSpectroscopyConfigOptionsWavelengthMax" = (
        Field(alias="wavelengthMax")
    )
    wavelength_optimal: "GetGOATSConfigOptionsSpectroscopyConfigOptionsWavelengthOptimal" = Field(
        alias="wavelengthOptimal"
    )
    wavelength_coverage: "GetGOATSConfigOptionsSpectroscopyConfigOptionsWavelengthCoverage" = Field(
        alias="wavelengthCoverage"
    )
    gmos_north: Optional["GetGOATSConfigOptionsSpectroscopyConfigOptionsGmosNorth"] = (
        Field(alias="gmosNorth")
    )
    gmos_south: Optional["GetGOATSConfigOptionsSpectroscopyConfigOptionsGmosSouth"] = (
        Field(alias="gmosSouth")
    )


class GetGOATSConfigOptionsSpectroscopyConfigOptionsSlitWidth(BaseModel):
    arcseconds: Any


class GetGOATSConfigOptionsSpectroscopyConfigOptionsWavelengthMin(BaseModel):
    nanometers: Any


class GetGOATSConfigOptionsSpectroscopyConfigOptionsWavelengthMax(BaseModel):
    nanometers: Any


class GetGOATSConfigOptionsSpectroscopyConfigOptionsWavelengthOptimal(BaseModel):
    nanometers: Any


class GetGOATSConfigOptionsSpectroscopyConfigOptionsWavelengthCoverage(BaseModel):
    nanometers: Any


class GetGOATSConfigOptionsSpectroscopyConfigOptionsGmosNorth(BaseModel):
    fpu: Optional[GmosNorthBuiltinFpu]
    grating: GmosNorthGrating
    filter_: Optional[GmosNorthFilter] = Field(alias="filter")


class GetGOATSConfigOptionsSpectroscopyConfigOptionsGmosSouth(BaseModel):
    fpu: Optional[GmosSouthBuiltinFpu]
    grating: GmosSouthGrating
    filter_: Optional[GmosSouthFilter] = Field(alias="filter")


class GetGOATSConfigOptionsImagingConfigOptions(BaseModel):
    instrument: Instrument
    site: Site
    filter_label: Any = Field(alias="filterLabel")
    fov: "GetGOATSConfigOptionsImagingConfigOptionsFov"
    gmos_north: Optional["GetGOATSConfigOptionsImagingConfigOptionsGmosNorth"] = Field(
        alias="gmosNorth"
    )
    gmos_south: Optional["GetGOATSConfigOptionsImagingConfigOptionsGmosSouth"] = Field(
        alias="gmosSouth"
    )


class GetGOATSConfigOptionsImagingConfigOptionsFov(BaseModel):
    arcseconds: Any


class GetGOATSConfigOptionsImagingConfigOptionsGmosNorth(BaseModel):
    filter_: GmosNorthFilter = Field(alias="filter")


class GetGOATSConfigOptionsImagingConfigOptionsGmosSouth(BaseModel):
    filter_: GmosSouthFilter = Field(alias="filter")


GetGOATSConfigOptions.model_rebuild()
GetGOATSConfigOptionsSpectroscopyConfigOptions.model_rebuild()
GetGOATSConfigOptionsImagingConfigOptions.model_rebuild()
