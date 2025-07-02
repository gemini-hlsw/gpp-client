from ..client import GPPClient


__all__ = ["BaseCoordinator"]


class BaseCoordinator:
    """
    Coordinate several managers to fulfil domain-level workflows.

    Parameters
    ----------
    client : GPPClient
        Shared low-level client injected by the parent director.

    Attributes
    ----------
    client : GPPClient
        The shared client instance.
    """

    def __init__(self, client: GPPClient) -> None:
        self._client: GPPClient = client

    @property
    def client(self) -> GPPClient:
        """
        Return the shared ``GPPClient`` instance.

        Returns
        -------
        GPPClient
            The shared client instance.
        """
        return self._client
