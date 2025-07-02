__all__ = ["BaseDirector"]

from ..client import GPPClient


class BaseDirector:
    """Orchestrate multiple resource managers for a single GPP service.

    Parameters
    ----------
    client : GPPClient
        Authenticated low-level client reused by every manager / coordinator.

    Attributes
    ----------
    client : GPPClient
        The shared client instance.
    """

    def __init__(self, client: GPPClient) -> None:
        self._client: GPPClient = client

    @property
    def client(self) -> GPPClient:
        """Return the shared GPP client instance."""
        return self._client
