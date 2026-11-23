from pydantic import Field

from .base_model import BaseModel
from .fragments import GOATSObservation


class GetGOATSObservations(BaseModel):
    observations: "GetGOATSObservationsObservations"


class GetGOATSObservationsObservations(BaseModel):
    matches: list["GetGOATSObservationsObservationsMatches"]
    has_more: bool = Field(alias="hasMore")


class GetGOATSObservationsObservationsMatches(GOATSObservation):
    pass


GetGOATSObservations.model_rebuild()
GetGOATSObservationsObservations.model_rebuild()
