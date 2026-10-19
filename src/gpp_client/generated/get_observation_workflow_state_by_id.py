from typing import Optional

from .base_model import BaseModel
from .fragments import (
    ObservationCore,
    ObservationCoreReference,  # noqa: F401
    ProgramCore,
    WorkflowDetails,
)


class GetObservationWorkflowStateById(BaseModel):
    observation: Optional["GetObservationWorkflowStateByIdObservation"]


class GetObservationWorkflowStateByIdObservation(ObservationCore):
    program: "GetObservationWorkflowStateByIdObservationProgram"
    workflow: Optional["GetObservationWorkflowStateByIdObservationWorkflow"]


GetObservationWorkflowStateByIdObservationProgram = ProgramCore
GetObservationWorkflowStateByIdObservationWorkflow = WorkflowDetails
GetObservationWorkflowStateById.model_rebuild()
GetObservationWorkflowStateByIdObservation.model_rebuild()
