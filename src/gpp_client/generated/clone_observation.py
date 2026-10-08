from pydantic import Field

from .base_model import BaseModel
from .fragments import ObservationDetails


class CloneObservation(BaseModel):
    clone_observation: "CloneObservationCloneObservation" = Field(
        alias="cloneObservation"
    )


class CloneObservationCloneObservation(BaseModel):
    new_observation: "CloneObservationCloneObservationNewObservation" = Field(
        alias="newObservation"
    )


CloneObservationCloneObservationNewObservation = ObservationDetails
CloneObservation.model_rebuild()
CloneObservationCloneObservation.model_rebuild()
