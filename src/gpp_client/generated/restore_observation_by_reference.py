from pydantic import Field

from .base_model import BaseModel
from .fragments import ObservationDetails


class RestoreObservationByReference(BaseModel):
    update_observations: "RestoreObservationByReferenceUpdateObservations" = Field(
        alias="updateObservations"
    )


class RestoreObservationByReferenceUpdateObservations(BaseModel):
    has_more: bool = Field(alias="hasMore")
    observations: list["RestoreObservationByReferenceUpdateObservationsObservations"]


RestoreObservationByReferenceUpdateObservationsObservations = ObservationDetails
RestoreObservationByReference.model_rebuild()
RestoreObservationByReferenceUpdateObservations.model_rebuild()
