from pydantic import Field

from .base_model import BaseModel
from .fragments import GOATSImagingConfigOption, GOATSSpectroscopyConfigOption


class GetGOATSConfigOptions(BaseModel):
    spectroscopy_config_options: list[
        "GetGOATSConfigOptionsSpectroscopyConfigOptions"
    ] = Field(alias="spectroscopyConfigOptions")
    imaging_config_options: list["GetGOATSConfigOptionsImagingConfigOptions"] = Field(
        alias="imagingConfigOptions"
    )


class GetGOATSConfigOptionsSpectroscopyConfigOptions(GOATSSpectroscopyConfigOption):
    pass


class GetGOATSConfigOptionsImagingConfigOptions(GOATSImagingConfigOption):
    pass


GetGOATSConfigOptions.model_rebuild()
