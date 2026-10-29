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


class SchedulerExecutedEventsExecutionEventAddedValueSequenceEventObservationReference(
    BaseModel
):
    label: Any


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


class SchedulerExecutedEventsExecutionEventAddedValueSlewEventObservationReference(
    BaseModel
):
    label: Any


class SchedulerExecutedEventsExecutionEventAddedValueSlewEventVisit(BaseModel):
    site: Site


SchedulerExecutedEvents.model_rebuild()
SchedulerExecutedEventsExecutionEventAdded.model_rebuild()
SchedulerExecutedEventsExecutionEventAddedValueSequenceEvent.model_rebuild()
SchedulerExecutedEventsExecutionEventAddedValueSequenceEventObservation.model_rebuild()
SchedulerExecutedEventsExecutionEventAddedValueSlewEvent.model_rebuild()
SchedulerExecutedEventsExecutionEventAddedValueSlewEventObservation.model_rebuild()
