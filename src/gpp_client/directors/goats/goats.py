__all__ = ["GOATSDirector"]

from dataclasses import dataclass

from ..base import BaseDirector
from .coordinators import ObservationCoordinator


@dataclass
class GOATSDirector(BaseDirector):
    """
    Facade for GOATS-domain workflows.

    The director instantiates and exposes coordinator objects that orchestrate
    multiple managers to fulfil complex GOATS-specific tasks. Each coordinator
    receives the shared ``GPPClient`` instance injected into this director.

    Parameters
    ----------
    client : GPPClient
        The low-level API client used by all underlying managers.

    Attributes
    ----------
    observation : ObservationCoordinator
        Coordinates observation data tailored for GOATS.
    """

    def __post_init__(self) -> None:
        self.observation: ObservationCoordinator = ObservationCoordinator(self.client)
