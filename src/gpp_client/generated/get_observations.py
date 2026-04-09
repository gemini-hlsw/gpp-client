from pydantic import Field

from .base_model import BaseModel
from .fragments import ObservationDetails


class GetObservations(BaseModel):
    observations: "GetObservationsObservations"


class GetObservationsObservations(BaseModel):
    has_more: bool = Field(alias="hasMore")
    matches: list["GetObservationsObservationsMatches"]


class GetObservationsObservationsMatches(ObservationDetails):
    pass


GetObservations.model_rebuild()
GetObservationsObservations.model_rebuild()
