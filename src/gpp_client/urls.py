"""
URL endpoints for the GPP client.
"""

__all__ = ["get_graphql_url", "get_ws_url"]

from enum import Enum
from urllib.parse import urljoin, urlsplit, urlunsplit

from gpp_client.environment import GPPEnvironment


class Endpoint(str, Enum):
    """
    API endpoints for the GPP client.
    """

    GRAPHQL = "/odb"
    WEBSOCKET = "/ws"


def get_graphql_url(environment: GPPEnvironment) -> str:
    """
    Return the GraphQL URL for an environment.

    Parameters
    ----------
    environment : GPPEnvironment
        The environment for which to construct the GraphQL URL.

    Returns
    -------
    str
        The GraphQL URL for the given environment.
    """
    return urljoin(environment.base_url, Endpoint.GRAPHQL.value)


def get_ws_url(environment: GPPEnvironment) -> str:
    """
    Return the WebSocket URL for an environment.

    Parameters
    ----------
    environment : GPPEnvironment
        The environment for which to construct the WebSocket URL.

    Returns
    -------
    str
        The WebSocket URL for the given environment.
    """
    parsed = urlsplit(environment.base_url)
    ws_scheme = "wss" if parsed.scheme == "https" else "ws"
    return urlunsplit(
        (ws_scheme, parsed.netloc, Endpoint.WEBSOCKET.value, "", ""),
    )
