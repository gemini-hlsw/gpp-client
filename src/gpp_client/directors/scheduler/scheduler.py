__all__ = ["SchedulerDirector"]

from dataclasses import dataclass

from ..base import BaseDirector
from .coordinators import ProgramCoordinator, ObservationCoordinator


@dataclass
class SchedulerDirector(BaseDirector):
    """
    Facade for Scheduler-domain workflows.

    The director instantiates and exposes coordinator objects that orchestrate
    multiple managers to fulfil complex Scheduler-specific tasks. Each coordinator
    receives the shared ``GPPClient`` instance injected into this director.

    Parameters
    ----------
    client : GPPClient
        The low-level API client used by all underlying managers.

    Attributes
    ----------
    program : ProgramCoordinator
        Coordinates program data tailored to the Scheduler.
    """

    def __post_init__(self) -> None:
        self.program: ProgramCoordinator = ProgramCoordinator(self.client)
        self.observation: ObservationCoordinator = ObservationCoordinator(self.client)
