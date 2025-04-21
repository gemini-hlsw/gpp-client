"""GPP GraphQL Client.

This module provides the GPPClient class for interacting with the GPP GraphQL API.
It manages authentication, transport configuration, and access to namespaced resource
managers for performing queries and mutations.

Examples
--------
>>> client = GPPClient(url="https://gpp.example.org/graphql", token="abc123")
>>> result = await client.program_note.get_by_id(resource_id="n-123")
"""

__all__ = ["GPPClient"]

import os
from pathlib import Path
from typing import Any, Optional

import aiohttp
import toml
from gql import Client, gql
from gql.transport.aiohttp import AIOHTTPTransport

from .managers.program import ProgramManager
from .managers.program_note import ProgramNoteManager


class GPPClient:
    """A client for interacting with the GPP GraphQL API.

    This client manages transport, authentication, and shared resource interfaces.

    Parameters
    ----------
    url : str, optional
        The base URL of the GPP GraphQL endpoint.
    token : str, optional
        The bearer token used for authorization.

    Attributes
    ----------
    program_note : ProgramNoteManager
        Manager for program note operations.
    program : ProgramManager
        Manager for program operations.
    """

    def __init__(
        self,
        url: Optional[str] = None,
        token: Optional[str] = None,
    ) -> None:
        resolved_url, resolved_token = resolve_credentials(url=url, token=token)
        self._transport: AIOHTTPTransport = AIOHTTPTransport(
            url=resolved_url,
            headers={"Authorization": f"Bearer {resolved_token}"},
            ssl=True,
            client_session_args={
                "timeout": aiohttp.ClientTimeout(
                    total=300,  # Total timeout in seconds (5 minutes).
                    connect=60,  # Connection timeout.
                    sock_read=60,  # Socket read timeout.
                    sock_connect=60,  # Socket connect timeout.
                )
            },
        )
        try:
            self._client: Client = Client(
                transport=self._transport, fetch_schema_from_transport=True
            )
        except Exception:
            raise

        # TODO: Initialize all resource managers.
        self.program_note = ProgramNoteManager(self)
        self.program = ProgramManager(self)

    async def _execute(
        self,
        query: str,
        variables: Optional[dict[str, Any]] = None,
    ) -> dict[str, Any]:
        """Execute a GraphQL query or mutation with unified error handling.

        Parameters
        ----------
        query : str
            The raw GraphQL query or mutation string.
        variables : dict[str, Any], optional
            A dictionary of variables to pass along with the query.

        Returns
        -------
        dict[str, Any]
            The result of the GraphQL execution.

        Raises
        ------
        RuntimeError
            If execution fails for any reason, the underlying exception
            is wrapped and re-raised with context.
        """
        try:
            async with self._client as session:
                return await session.execute(gql(query), variable_values=variables)
        except Exception as exc:
            # TODO: Log error, re-raise custom exception, or retry.
            raise RuntimeError(f"GraphQL execution failed: {exc}") from exc


def load_gpp_config() -> dict[str, str]:
    """Load the GPP client configuration for a given profile.

    This function reads from the `~/.gpp/config.toml` file and returns the
    configuration values.

    Returns
    -------
    dict[str, str]
        A dictionary of configuration values (typically `url` and `token`).
        Returns an empty dictionary if the file is missing.
    """
    config_path = Path.home() / ".gpp" / "config.toml"
    if not config_path.exists():
        return {}

    return toml.load(config_path)


def resolve_credentials(
    url: Optional[str] = None,
    token: Optional[str] = None,
) -> tuple[str, str]:
    """Resolve the GPP GraphQL credentials using precedence rules.

    This function looks for credentials in the following order:
    1. Direct function arguments (`url`, `token`).
    2. Environment variables `GPP_URL` and `GPP_TOKEN`.
    3. Configuration file '~/.gpp/config.toml'.

    Parameters
    ----------
    url : str, optional
        The GraphQL endpoint URL. Overrides env and config if provided.
    token : str, optional
        The bearer token for authentication. Overrides env and config if provided.

    Returns
    -------
    tuple[str, str]
        A tuple containing the resolved (url, token).

    Raises
    ------
    ValueError
        If neither the `url` nor `token` could be resolved from any source.
    """
    config = load_gpp_config()
    resolved_url = url or os.getenv("GPP_URL") or config.get("url")
    resolved_token = token or os.getenv("GPP_TOKEN") or config.get("token")

    if not resolved_url or not resolved_token:
        raise ValueError(
            "Missing GPP URL or GPP token. Provide via args, environment, or "
            "in configuration file '~/.gpp/config.toml.'"
        )

    return resolved_url, resolved_token
