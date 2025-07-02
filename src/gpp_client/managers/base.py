__all__ = ["BaseManager"]

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from ..client import GPPClient


class BaseManager:
    """
    Base class for all resource managers.

    Provides access to the underlying GraphQL client used to perform operations.

    Parameters
    ----------
    client : GPPClient
        The public-facing client instance. This is used to extract the internal
        GraphQL client used for executing queries and mutations.
    """

    def __init__(self, client: "GPPClient") -> None:
        self.client = client._client
