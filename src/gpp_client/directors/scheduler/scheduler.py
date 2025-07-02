__all__ = ["SchedulerDirector"]

from functools import cached_property

from ..base_director import BaseDirector
from .coordinators import ProgramCoordinator


class SchedulerDirector(BaseDirector):
    """
    Facade for Scheduler-domain workflows.

    The director lazily instantiates and exposes coordinator objects that orchestrate
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

    @cached_property
    def program(self) -> ProgramCoordinator:
        """
        Coordinator for program-related operations.

        Returns
        -------
        ProgramCoordinator
            Lazily created instance that orchestrates program-level workflows.
        """
        return ProgramCoordinator(self.client)
