from typing import Optional

from .base_model import BaseModel
from .fragments import ObservationDetails


class GetObservation(BaseModel):
    observation: Optional["GetObservationObservation"]


GetObservationObservation = ObservationDetails
GetObservation.model_rebuild()
