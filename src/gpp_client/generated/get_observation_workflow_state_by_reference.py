from typing import Optional

from pydantic import Field

from .base_model import BaseModel
from .enums import ObservationValidationCode
from .fragments import ObservationCore, ProgramCore, WorkflowDetails


class GetObservationWorkflowStateByReference(BaseModel):
    observation: Optional["GetObservationWorkflowStateByReferenceObservation"]


class GetObservationWorkflowStateByReferenceObservation(ObservationCore):
    program: "GetObservationWorkflowStateByReferenceObservationProgram"
    workflow: Optional["GetObservationWorkflowStateByReferenceObservationWorkflow"]


class GetObservationWorkflowStateByReferenceObservationProgram(ProgramCore):
    dismissed_warnings: list[ObservationValidationCode] = Field(
        alias="dismissedWarnings"
    )


class GetObservationWorkflowStateByReferenceObservationWorkflow(WorkflowDetails):
    pass


GetObservationWorkflowStateByReference.model_rebuild()
GetObservationWorkflowStateByReferenceObservation.model_rebuild()
