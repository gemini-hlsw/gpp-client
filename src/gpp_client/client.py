"""
This module provides the main entry point for interacting with GPP.
"""

__all__ = ["GPPClient"]

import logging
from typing import Any, Optional

from typing_extensions import Self

from gpp_client.domains import (
    AtomDomain,
    AttachmentDomain,
    GOATSDomain,
    ObservationDomain,
    ProgramDomain,
    SchedulerDomain,
    SiteStatusDomain,
    TargetDomain,
    WorkflowStateDomain,
)
from gpp_client.environment import GPPEnvironment
from gpp_client.generated.client import GraphQLClient
from gpp_client.logging_utils import _enable_dev_console_logging
from gpp_client.rest import RESTClient
from gpp_client.settings import GPPSettings, _get_packaged_environment
from gpp_client.urls import get_graphql_url, get_ws_url

logger = logging.getLogger(__name__)


class GPPClient:
    """
    Main entry point for interacting with the GPP GraphQL API.

    Parameters
    ----------
    token : str, optional
        GPP API token to use for authentication. If not provided, the client will attempt to resolve a token from environment variables or other configuration sources.
    debug : bool, optional
        Whether to enable debug logging for the client. If not provided, defaults to ``False``.
    """

    def __init__(
        self,
        *,
        token: str | None = None,
        debug: bool | None = None,
    ) -> None:
        self._settings = self._build_settings(token=token, debug=debug)
        if self._settings.debug:
            self._enable_dev_logging()

        logger.debug("GPPClient initialized with settings: %s", self._settings)

        self._graphql = self._build_graphql_client()
        self._rest = self._build_rest_client()
        self._init_domains()

    def _build_settings(
        self,
        *,
        token: str | None = None,
        debug: bool | None = None,
    ) -> GPPSettings:
        """
        Build the effective runtime settings.

        Parameters
        ----------
        token : str | None, optional
            Explicit token override.
        debug : bool | None, optional
            Explicit debug override.

        Returns
        -------
        GPPSettings
            Resolved client settings.
        """
        settings_kwargs: dict[str, Any] = {}
        if token is not None:
            environment = _get_packaged_environment()
            if environment is GPPEnvironment.DEVELOPMENT:
                settings_kwargs["development_token"] = token
            else:
                settings_kwargs["token"] = token
        if debug is not None:
            settings_kwargs["debug"] = debug

        return GPPSettings(**settings_kwargs)

    def _build_graphql_client(self) -> GraphQLClient:
        """
        Build the GraphQL client.

        Returns
        -------
        GraphQLClient
            Configured GraphQL client instance.
        """
        headers = {
            "Authorization": f"Bearer {self._settings.resolved_token}",
        }
        ws_url = get_ws_url(self._settings.environment)
        graphql_url = get_graphql_url(self._settings.environment)

        logger.debug("Initializing GraphQL client for %s", graphql_url)

        return GraphQLClient(
            url=graphql_url,
            headers=headers,
            ws_url=ws_url,
        )

    def _build_rest_client(self) -> RESTClient:
        """
        Build the REST client.

        Returns
        -------
        RESTClient
            Configured REST client instance.
        """
        logger.debug(
            "Initializing REST client for %s",
            self._settings.environment.base_url,
        )
        return RESTClient(
            base_url=self._settings.environment.base_url,
            gpp_token=self._settings.resolved_token,
        )

    def _build_domain_kwargs(self) -> dict[str, Any]:
        """
        Build shared keyword arguments for domain initialization.

        Returns
        -------
        dict[str, Any]
            Shared domain constructor keyword arguments.
        """
        return {
            "graphql": self._graphql,
            "rest": self._rest,
            "settings": self._settings,
        }

    def _init_domains(self) -> None:
        """
        Initialize domain clients.
        """
        domain_kwargs = self._build_domain_kwargs()

        self.scheduler = SchedulerDomain(**domain_kwargs)
        self.target = TargetDomain(**domain_kwargs)
        self.workflow_state = WorkflowStateDomain(**domain_kwargs)
        self.observation = ObservationDomain(**domain_kwargs)
        self.program = ProgramDomain(**domain_kwargs)
        self.site_status = SiteStatusDomain()
        self.goats = GOATSDomain(**domain_kwargs)
        self.atom = AtomDomain(**domain_kwargs)
        self.attachment = AttachmentDomain(**domain_kwargs)

    @property
    def graphql(self) -> GraphQLClient:
        """
        Access the GraphQL client for making GraphQL requests.

        Returns
        -------
        GraphQLClient
            The GraphQL client instance.
        """
        return self._graphql

    @property
    def rest(self) -> RESTClient:
        """
        Access the REST client for making non-GraphQL requests.

        Returns
        -------
        RESTClient
            The REST client instance.
        """
        return self._rest

    @property
    def settings(self) -> GPPSettings:
        """
        Access the effective runtime settings of the client.

        Returns
        -------
        GPPSettings
            The client's runtime settings.
        """
        return self._settings

    def _enable_dev_logging(self) -> None:
        """
        Enable debug-level console logging for development purposes.
        """
        _enable_dev_console_logging()
        logger.debug("Logging enabled for GPPClient")

    async def close(self) -> None:
        """
        Close any underlying connections held by the client.
        """
        logger.debug("Closing GPPClient connections")
        await self._rest.close()

    async def __aenter__(self) -> Self:
        """
        Enter the async context manager.

        Returns
        -------
        Self
            This client instance.
        """
        return self

    async def __aexit__(self, exc_type, exc, tb) -> None:
        """
        Exit the async context manager.
        """
        await self.close()

    async def ping(self) -> tuple[bool, Optional[str]]:
        """
        Check if the GPP GraphQL endpoint is reachable and authenticated.

        Returns
        -------
        bool
            ``True`` if the connection and authentication succeed, ``False``
            otherwise.
        str, optional
            The error message if the connection failed.
        """
        logger.debug("Pinging GPP GraphQL endpoint at %s", self._graphql.url)
        try:
            await self._graphql.ping()
            return True, None
        except Exception as exc:
            logger.error("Ping to GPP GraphQL endpoint failed: %s", exc)
            return False, str(exc)
