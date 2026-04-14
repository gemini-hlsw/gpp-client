from typing import Optional

from .base_model import BaseModel
from .fragments import ObservationCore, ProgramCore, WorkflowDetails


class GetObservationWorkflowStateByReference(BaseModel):
    observation: Optional["GetObservationWorkflowStateByReferenceObservation"]


class GetObservationWorkflowStateByReferenceObservation(ObservationCore):
    program: "GetObservationWorkflowStateByReferenceObservationProgram"
    workflow: Optional["GetObservationWorkflowStateByReferenceObservationWorkflow"]


class GetObservationWorkflowStateByReferenceObservationProgram(ProgramCore):
    pass


class GetObservationWorkflowStateByReferenceObservationWorkflow(WorkflowDetails):
    pass


GetObservationWorkflowStateByReference.model_rebuild()
GetObservationWorkflowStateByReferenceObservation.model_rebuild()
