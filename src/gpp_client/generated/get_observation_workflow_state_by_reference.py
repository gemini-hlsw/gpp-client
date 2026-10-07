from typing import Optional

from .base_model import BaseModel
from .fragments import (
    ObservationCore,
    ObservationCoreReference,  # noqa: F401
    ProgramCore,
    WorkflowDetails,
)


class GetObservationWorkflowStateByReference(BaseModel):
    observation: Optional["GetObservationWorkflowStateByReferenceObservation"]


class GetObservationWorkflowStateByReferenceObservation(ObservationCore):
    program: "GetObservationWorkflowStateByReferenceObservationProgram"
    workflow: Optional["GetObservationWorkflowStateByReferenceObservationWorkflow"]


GetObservationWorkflowStateByReferenceObservationProgram = ProgramCore
GetObservationWorkflowStateByReferenceObservationWorkflow = WorkflowDetails
GetObservationWorkflowStateByReference.model_rebuild()
GetObservationWorkflowStateByReferenceObservation.model_rebuild()
