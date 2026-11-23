from typing import Optional

from pydantic import Field

from .base_model import BaseModel
from .enums import ObservationValidationCode
from .fragments import ObservationCore, ProgramCore, WorkflowDetails


class GetObservationWorkflowStateById(BaseModel):
    observation: Optional["GetObservationWorkflowStateByIdObservation"]


class GetObservationWorkflowStateByIdObservation(ObservationCore):
    program: "GetObservationWorkflowStateByIdObservationProgram"
    workflow: Optional["GetObservationWorkflowStateByIdObservationWorkflow"]


class GetObservationWorkflowStateByIdObservationProgram(ProgramCore):
    dismissed_warnings: list[ObservationValidationCode] = Field(
        alias="dismissedWarnings"
    )


class GetObservationWorkflowStateByIdObservationWorkflow(WorkflowDetails):
    pass


GetObservationWorkflowStateById.model_rebuild()
GetObservationWorkflowStateByIdObservation.model_rebuild()
