from typing import Any, Literal, Optional, Union

from pydantic import Field

from .base_model import BaseModel
from .enums import ExecutionEventType, SequenceCommand, Site, SlewStage


class SchedulerExecutedEvents(BaseModel):
    execution_event_added: "SchedulerExecutedEventsExecutionEventAdded" = Field(
        alias="executionEventAdded"
    )


class SchedulerExecutedEventsExecutionEventAdded(BaseModel):
    value: Union[
        "SchedulerExecutedEventsExecutionEventAddedValueExecutionEvent",
        "SchedulerExecutedEventsExecutionEventAddedValueSequenceEvent",
        "SchedulerExecutedEventsExecutionEventAddedValueSlewEvent",
    ] = Field(discriminator="typename__")


class SchedulerExecutedEventsExecutionEventAddedValueExecutionEvent(BaseModel):
    typename__: Literal["AtomEvent", "DatasetEvent", "ExecutionEvent", "StepEvent"] = (
        Field(alias="__typename")
    )
    event_type: ExecutionEventType = Field(alias="eventType")
    id: Any


class SchedulerExecutedEventsExecutionEventAddedValueSequenceEvent(BaseModel):
    typename__: Literal["SequenceEvent"] = Field(alias="__typename")
    event_type: ExecutionEventType = Field(alias="eventType")
    id: Any
    id: Any
    observation: (
        "SchedulerExecutedEventsExecutionEventAddedValueSequenceEventObservation"
    )
    effective_time: Any = Field(alias="effectiveTime")
    command: SequenceCommand
    visit: "SchedulerExecutedEventsExecutionEventAddedValueSequenceEventVisit"


class SchedulerExecutedEventsExecutionEventAddedValueSequenceEventObservation(
    BaseModel
):
    id: Any
    reference: Optional[
        "SchedulerExecutedEventsExecutionEventAddedValueSequenceEventObservationReference"
    ]
    execution: "SchedulerExecutedEventsExecutionEventAddedValueSequenceEventObservationExecution"


class SchedulerExecutedEventsExecutionEventAddedValueSequenceEventObservationReference(
    BaseModel
):
    label: Any


class SchedulerExecutedEventsExecutionEventAddedValueSequenceEventObservationExecution(
    BaseModel
):
    digest: Optional[
        "SchedulerExecutedEventsExecutionEventAddedValueSequenceEventObservationExecutionDigest"
    ]


class SchedulerExecutedEventsExecutionEventAddedValueSequenceEventObservationExecutionDigest(
    BaseModel
):
    value: Optional[
        "SchedulerExecutedEventsExecutionEventAddedValueSequenceEventObservationExecutionDigestValue"
    ]


class SchedulerExecutedEventsExecutionEventAddedValueSequenceEventObservationExecutionDigestValue(
    BaseModel
):
    estimate: "SchedulerExecutedEventsExecutionEventAddedValueSequenceEventObservationExecutionDigestValueEstimate"


class SchedulerExecutedEventsExecutionEventAddedValueSequenceEventObservationExecutionDigestValueEstimate(
    BaseModel
):
    total: "SchedulerExecutedEventsExecutionEventAddedValueSequenceEventObservationExecutionDigestValueEstimateTotal"


class SchedulerExecutedEventsExecutionEventAddedValueSequenceEventObservationExecutionDigestValueEstimateTotal(
    BaseModel
):
    total: "SchedulerExecutedEventsExecutionEventAddedValueSequenceEventObservationExecutionDigestValueEstimateTotalTotal"


class SchedulerExecutedEventsExecutionEventAddedValueSequenceEventObservationExecutionDigestValueEstimateTotalTotal(
    BaseModel
):
    seconds: Any


class SchedulerExecutedEventsExecutionEventAddedValueSequenceEventVisit(BaseModel):
    site: Site


class SchedulerExecutedEventsExecutionEventAddedValueSlewEvent(BaseModel):
    typename__: Literal["SlewEvent"] = Field(alias="__typename")
    event_type: ExecutionEventType = Field(alias="eventType")
    id: Any
    id: Any
    recorded_time: Any = Field(alias="recordedTime")
    slew_stage: SlewStage = Field(alias="slewStage")
    observation: "SchedulerExecutedEventsExecutionEventAddedValueSlewEventObservation"
    visit: "SchedulerExecutedEventsExecutionEventAddedValueSlewEventVisit"


class SchedulerExecutedEventsExecutionEventAddedValueSlewEventObservation(BaseModel):
    id: Any
    reference: Optional[
        "SchedulerExecutedEventsExecutionEventAddedValueSlewEventObservationReference"
    ]
    execution: (
        "SchedulerExecutedEventsExecutionEventAddedValueSlewEventObservationExecution"
    )


class SchedulerExecutedEventsExecutionEventAddedValueSlewEventObservationReference(
    BaseModel
):
    label: Any


class SchedulerExecutedEventsExecutionEventAddedValueSlewEventObservationExecution(
    BaseModel
):
    digest: Optional[
        "SchedulerExecutedEventsExecutionEventAddedValueSlewEventObservationExecutionDigest"
    ]


class SchedulerExecutedEventsExecutionEventAddedValueSlewEventObservationExecutionDigest(
    BaseModel
):
    value: Optional[
        "SchedulerExecutedEventsExecutionEventAddedValueSlewEventObservationExecutionDigestValue"
    ]


class SchedulerExecutedEventsExecutionEventAddedValueSlewEventObservationExecutionDigestValue(
    BaseModel
):
    estimate: "SchedulerExecutedEventsExecutionEventAddedValueSlewEventObservationExecutionDigestValueEstimate"


class SchedulerExecutedEventsExecutionEventAddedValueSlewEventObservationExecutionDigestValueEstimate(
    BaseModel
):
    total: "SchedulerExecutedEventsExecutionEventAddedValueSlewEventObservationExecutionDigestValueEstimateTotal"


class SchedulerExecutedEventsExecutionEventAddedValueSlewEventObservationExecutionDigestValueEstimateTotal(
    BaseModel
):
    total: "SchedulerExecutedEventsExecutionEventAddedValueSlewEventObservationExecutionDigestValueEstimateTotalTotal"


class SchedulerExecutedEventsExecutionEventAddedValueSlewEventObservationExecutionDigestValueEstimateTotalTotal(
    BaseModel
):
    seconds: Any


class SchedulerExecutedEventsExecutionEventAddedValueSlewEventVisit(BaseModel):
    site: Site


SchedulerExecutedEvents.model_rebuild()
SchedulerExecutedEventsExecutionEventAdded.model_rebuild()
SchedulerExecutedEventsExecutionEventAddedValueSequenceEvent.model_rebuild()
SchedulerExecutedEventsExecutionEventAddedValueSequenceEventObservation.model_rebuild()
SchedulerExecutedEventsExecutionEventAddedValueSequenceEventObservationExecution.model_rebuild()
SchedulerExecutedEventsExecutionEventAddedValueSequenceEventObservationExecutionDigest.model_rebuild()
SchedulerExecutedEventsExecutionEventAddedValueSequenceEventObservationExecutionDigestValue.model_rebuild()
SchedulerExecutedEventsExecutionEventAddedValueSequenceEventObservationExecutionDigestValueEstimate.model_rebuild()
SchedulerExecutedEventsExecutionEventAddedValueSequenceEventObservationExecutionDigestValueEstimateTotal.model_rebuild()
SchedulerExecutedEventsExecutionEventAddedValueSlewEvent.model_rebuild()
SchedulerExecutedEventsExecutionEventAddedValueSlewEventObservation.model_rebuild()
SchedulerExecutedEventsExecutionEventAddedValueSlewEventObservationExecution.model_rebuild()
SchedulerExecutedEventsExecutionEventAddedValueSlewEventObservationExecutionDigest.model_rebuild()
SchedulerExecutedEventsExecutionEventAddedValueSlewEventObservationExecutionDigestValue.model_rebuild()
SchedulerExecutedEventsExecutionEventAddedValueSlewEventObservationExecutionDigestValueEstimate.model_rebuild()
SchedulerExecutedEventsExecutionEventAddedValueSlewEventObservationExecutionDigestValueEstimateTotal.model_rebuild()
