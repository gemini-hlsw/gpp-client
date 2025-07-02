__all__ = ["BaseDirector"]

from dataclasses import dataclass

from ..client import GPPClient


@dataclass
class BaseDirector:
    """Orchestrate multiple resource managers for a single GPP service.

    Attributes
    ----------
    client : GPPClient
        Authenticated low-level client reused by every manager / coordinator.
    """

    client: GPPClient
