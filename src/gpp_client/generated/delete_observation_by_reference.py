from pydantic import Field

from .base_model import BaseModel
from .fragments import ObservationDetails


class DeleteObservationByReference(BaseModel):
    update_observations: "DeleteObservationByReferenceUpdateObservations" = Field(
        alias="updateObservations"
    )


class DeleteObservationByReferenceUpdateObservations(BaseModel):
    has_more: bool = Field(alias="hasMore")
    observations: list["DeleteObservationByReferenceUpdateObservationsObservations"]


class DeleteObservationByReferenceUpdateObservationsObservations(ObservationDetails):
    pass


DeleteObservationByReference.model_rebuild()
DeleteObservationByReferenceUpdateObservations.model_rebuild()
