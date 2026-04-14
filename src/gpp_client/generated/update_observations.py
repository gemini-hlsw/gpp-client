from pydantic import Field

from .base_model import BaseModel
from .fragments import ObservationDetails


class UpdateObservations(BaseModel):
    update_observations: "UpdateObservationsUpdateObservations" = Field(
        alias="updateObservations"
    )


class UpdateObservationsUpdateObservations(BaseModel):
    has_more: bool = Field(alias="hasMore")
    observations: list["UpdateObservationsUpdateObservationsObservations"]


class UpdateObservationsUpdateObservationsObservations(ObservationDetails):
    pass


UpdateObservations.model_rebuild()
UpdateObservationsUpdateObservations.model_rebuild()
