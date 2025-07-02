__all__ = ["BaseCoordinator"]

from dataclasses import dataclass

from ..client import GPPClient


@dataclass
class BaseCoordinator:
    """
    Coordinate several managers to fulfil domain-level workflows.

    Attributes
    ----------
    client : GPPClient
        Shared low-level client injected by the parent director.
    """

    client: GPPClient
