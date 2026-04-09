from typing import Optional

from .base_model import BaseModel
from .fragments import ObservationDetails


class GetObservation(BaseModel):
    observation: Optional["GetObservationObservation"]


class GetObservationObservation(ObservationDetails):
    pass


GetObservation.model_rebuild()
