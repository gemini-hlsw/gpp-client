from typing import Optional

from pydantic import Field

from .base_model import BaseModel
from .fragments import ObservationWorkflowDetails


class SetObservationWorkflowState(BaseModel):
    set_observation_workflow_state: Optional[
        "SetObservationWorkflowStateSetObservationWorkflowState"
    ] = Field(alias="setObservationWorkflowState")


SetObservationWorkflowStateSetObservationWorkflowState = ObservationWorkflowDetails
SetObservationWorkflowState.model_rebuild()
