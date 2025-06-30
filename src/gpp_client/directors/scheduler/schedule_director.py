from .program import Program
from ..base_director import BaseDirector

__all__ = ["SchedulerDirector"]

class SchedulerDirector(BaseDirector):
    """Director used to for GPP Scheduler that allows doing multy manager queries."""

    @property
    def program(self):
        return Program(self.client)