from pydantic import Field

from .base_model import BaseModel
from .fragments import ObservationDetails


class RestoreObservationById(BaseModel):
    update_observations: "RestoreObservationByIdUpdateObservations" = Field(
        alias="updateObservations"
    )


class RestoreObservationByIdUpdateObservations(BaseModel):
    has_more: bool = Field(alias="hasMore")
    observations: list["RestoreObservationByIdUpdateObservationsObservations"]


RestoreObservationByIdUpdateObservationsObservations = ObservationDetails
RestoreObservationById.model_rebuild()
RestoreObservationByIdUpdateObservations.model_rebuild()
