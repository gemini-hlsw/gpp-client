from pydantic import Field

from .base_model import BaseModel
from .fragments import GOATSConfigurationRequest


class GetGOATSConfigurationRequests(BaseModel):
    configuration_requests: "GetGOATSConfigurationRequestsConfigurationRequests" = (
        Field(alias="configurationRequests")
    )


class GetGOATSConfigurationRequestsConfigurationRequests(BaseModel):
    matches: list["GetGOATSConfigurationRequestsConfigurationRequestsMatches"]
    has_more: bool = Field(alias="hasMore")


class GetGOATSConfigurationRequestsConfigurationRequestsMatches(
    GOATSConfigurationRequest
):
    pass


GetGOATSConfigurationRequests.model_rebuild()
GetGOATSConfigurationRequestsConfigurationRequests.model_rebuild()
