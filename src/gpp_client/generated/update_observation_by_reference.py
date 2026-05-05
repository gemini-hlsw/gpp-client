from pydantic import Field

from .base_model import BaseModel
from .fragments import ObservationDetails


class UpdateObservationByReference(BaseModel):
    update_observations: "UpdateObservationByReferenceUpdateObservations" = Field(
        alias="updateObservations"
    )


class UpdateObservationByReferenceUpdateObservations(BaseModel):
    has_more: bool = Field(alias="hasMore")
    observations: list["UpdateObservationByReferenceUpdateObservationsObservations"]


class UpdateObservationByReferenceUpdateObservationsObservations(ObservationDetails):
    pass


UpdateObservationByReference.model_rebuild()
UpdateObservationByReferenceUpdateObservations.model_rebuild()
