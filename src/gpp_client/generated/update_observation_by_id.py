from pydantic import Field

from .base_model import BaseModel
from .fragments import ObservationDetails


class UpdateObservationById(BaseModel):
    update_observations: "UpdateObservationByIdUpdateObservations" = Field(
        alias="updateObservations"
    )


class UpdateObservationByIdUpdateObservations(BaseModel):
    has_more: bool = Field(alias="hasMore")
    observations: list["UpdateObservationByIdUpdateObservationsObservations"]


class UpdateObservationByIdUpdateObservationsObservations(ObservationDetails):
    pass


UpdateObservationById.model_rebuild()
UpdateObservationByIdUpdateObservations.model_rebuild()
