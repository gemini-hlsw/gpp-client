from pydantic import Field

from .base_model import BaseModel
from .fragments import ObservationDetails


class CreateObservation(BaseModel):
    create_observation: "CreateObservationCreateObservation" = Field(
        alias="createObservation"
    )


class CreateObservationCreateObservation(BaseModel):
    observation: "CreateObservationCreateObservationObservation"


CreateObservationCreateObservationObservation = ObservationDetails
CreateObservation.model_rebuild()
CreateObservationCreateObservation.model_rebuild()
