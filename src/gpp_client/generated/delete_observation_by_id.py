from pydantic import Field

from .base_model import BaseModel
from .fragments import ObservationDetails


class DeleteObservationById(BaseModel):
    update_observations: "DeleteObservationByIdUpdateObservations" = Field(
        alias="updateObservations"
    )


class DeleteObservationByIdUpdateObservations(BaseModel):
    has_more: bool = Field(alias="hasMore")
    observations: list["DeleteObservationByIdUpdateObservationsObservations"]


class DeleteObservationByIdUpdateObservationsObservations(ObservationDetails):
    pass


DeleteObservationById.model_rebuild()
DeleteObservationByIdUpdateObservations.model_rebuild()
