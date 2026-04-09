from typing import Optional

from .base_model import BaseModel
from .fragments import ObservationCore, ProgramCore, WorkflowDetails


class GetObservationWorkflowStateById(BaseModel):
    observation: Optional["GetObservationWorkflowStateByIdObservation"]


class GetObservationWorkflowStateByIdObservation(ObservationCore):
    program: "GetObservationWorkflowStateByIdObservationProgram"
    workflow: Optional["GetObservationWorkflowStateByIdObservationWorkflow"]


class GetObservationWorkflowStateByIdObservationProgram(ProgramCore):
    pass


class GetObservationWorkflowStateByIdObservationWorkflow(WorkflowDetails):
    pass


GetObservationWorkflowStateById.model_rebuild()
GetObservationWorkflowStateByIdObservation.model_rebuild()
