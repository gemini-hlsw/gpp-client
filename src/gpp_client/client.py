"""
This module provides the main entry point for interacting with GPP.
"""

__all__ = ["GPPClient"]

import logging
import os
import warnings
from collections.abc import Mapping
from typing import Any, Optional

import httpx
from dotenv import dotenv_values
from typing_extensions import Self

from gpp_client import availability
from gpp_client.availability import EnumT
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
from gpp_client.graphql_client import GPPGraphQLClient
from gpp_client.logging_utils import _enable_dev_console_logging
from gpp_client.rest import RESTClient
from gpp_client.settings import GPPSettings
from gpp_client.urls import get_graphql_url, get_ws_url

logger = logging.getLogger(__name__)

# httpx defaults to 5 seconds, which is too aggressive for slow GPP operations
# such as cloning observations.
_HTTP_TIMEOUT = httpx.Timeout(60.0, connect=10.0)


_DEFAULT_SOURCE = "the default"


def _environment_source(
    environment: GPPEnvironment | str | None, settings: GPPSettings
) -> str:
    """
    Name where the client's environment came from, for the log and the warning.
    """
    if environment is not None:
        return "the environment argument"
    if "environment" not in settings.model_fields_set:
        return _DEFAULT_SOURCE
    # pydantic-settings matches variable names in any case.
    if _names_environment(os.environ):
        return "GPP_ENVIRONMENT"
    if _names_environment(dotenv_values(".env")):
        return "the .env file"
    return "the configuration file"


def _names_environment(variables: Mapping[str, str | None]) -> bool:
    return any(
        name.upper() == "GPP_ENVIRONMENT" and value and value.strip()
        for name, value in variables.items()
    )


class GPPClient:
    """
    Main entry point for interacting with the GPP GraphQL API.

    Parameters
    ----------
    environment : GPPEnvironment | str, optional
        The GPP environment to connect to, ``"development"`` or ``"production"``.
        If not provided, ``GPP_ENVIRONMENT`` is used, then the ``.env`` file.
        With none of them set, the client uses production and emits a
        ``FutureWarning``: a future release will raise an error instead.
    token : str, optional
        GPP API token for the selected environment. If not provided, the token is
        read from that environment's variable (``GPP_TOKEN`` for production,
        ``GPP_DEVELOPMENT_TOKEN`` for development) or the ``.env`` file.
    debug : bool, optional
        Whether to enable debug logging for the client. If not provided, defaults to
        ``False``.
    http_client : httpx.AsyncClient, optional
        Client that sends every GraphQL HTTP request, for custom proxies, timeouts,
        or transports. The ``Authorization`` header is sent with each request and
        not stored on it. The caller owns it and closes it. If not provided, the
        client builds its own.
    """

    scheduler: SchedulerDomain
    """Domain client for scheduler-related operations."""

    program: ProgramDomain
    """Domain client for program-related operations."""

    observation: ObservationDomain
    """Domain client for observation-related operations."""

    target: TargetDomain
    """Domain client for target-related operations."""

    workflow_state: WorkflowStateDomain
    """Domain client for workflow state operations."""

    atom: AtomDomain
    """Domain client for atom digest operations."""

    attachment: AttachmentDomain
    """Domain client for attachment upload, download, and management operations."""

    goats: GOATSDomain
    """Domain client for GOATS-specific queries."""

    site_status: SiteStatusDomain
    """Domain client for Gemini site status information."""

    def __init__(
        self,
        *,
        environment: GPPEnvironment | str | None = None,
        token: str | None = None,
        debug: bool | None = None,
        http_client: httpx.AsyncClient | None = None,
    ) -> None:
        if isinstance(environment, str):
            environment = environment.strip() or None
        self._settings = self._build_settings(
            environment=environment, token=token, debug=debug
        )
        source = _environment_source(environment, self._settings)
        if source == _DEFAULT_SOURCE:
            warnings.warn(
                "No GPP environment set, so using production. Pass environment= "
                "or set GPP_ENVIRONMENT; a future release will raise an error "
                "instead.",
                FutureWarning,
                stacklevel=2,
            )
        if self._settings.debug:
            self._enable_dev_logging()

        logger.debug("GPPClient initialized with settings: %s", self._settings)

        self._owns_http_client = http_client is None
        self._graphql = self._build_graphql_client(http_client)
        self._rest = self._build_rest_client()
        self._init_domains()
        logger.info(
            "GPPClient using the %s environment, from %s, at %s",
            self._settings.environment.label,
            source,
            self._graphql.url,
        )

    def __repr__(self) -> str:
        return f"GPPClient(environment={self._settings.environment.label!r})"

    def _build_settings(
        self,
        *,
        environment: GPPEnvironment | str | None = None,
        token: str | None = None,
        debug: bool | None = None,
    ) -> GPPSettings:
        """
        Build the effective runtime settings.

        Parameters
        ----------
        environment : GPPEnvironment | str | None, optional
            Explicit environment; an empty value falls through to the next source.
        token : str | None, optional
            Explicit token for the selected environment.
        debug : bool | None, optional
            Explicit debug override.

        Returns
        -------
        GPPSettings
            Resolved client settings.
        """
        settings_kwargs: dict[str, Any] = {}
        if environment is not None:
            settings_kwargs["environment"] = environment
        if debug is not None:
            settings_kwargs["debug"] = debug

        settings = GPPSettings(**settings_kwargs)
        return settings if token is None else settings.with_token(token)

    def _build_graphql_client(
        self, http_client: httpx.AsyncClient | None = None
    ) -> GPPGraphQLClient:
        """
        Build the GraphQL client.

        Parameters
        ----------
        http_client : httpx.AsyncClient | None, optional
            Caller-supplied HTTP client. If ``None``, a new one is built.

        Returns
        -------
        GPPGraphQLClient
            Configured GraphQL client instance.
        """
        headers = {
            "Authorization": f"Bearer {self._settings.resolved_token}",
        }
        ws_url = get_ws_url(self._settings.environment)
        graphql_url = get_graphql_url(self._settings.environment)

        logger.debug("Initializing GraphQL client for %s", graphql_url)

        return GPPGraphQLClient(
            environment=self._settings.environment,
            url=graphql_url,
            headers=headers,
            http_client=http_client or httpx.AsyncClient(timeout=_HTTP_TIMEOUT),
            ws_url=ws_url,
            ws_headers=headers,
            ws_connection_init_payload=headers,
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
            environment=self._settings.environment,
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
    def graphql(self) -> GPPGraphQLClient:
        """
        Access the GraphQL client for making GraphQL requests.

        Returns
        -------
        GPPGraphQLClient
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

    def is_available(self, model: object, field: str) -> bool:
        """
        Return whether this environment has a generated model's field.

        A field the environment lacks reads ``None``; this tells that apart
        from a value GPP left null, without a network call.

        Parameters
        ----------
        model : object
            A generated result model, as an instance or a class.
        field : str
            The field's attribute name on the model.

        Returns
        -------
        bool
            ``True`` when the selected environment has the field.

        Raises
        ------
        AttributeError
            If the model has no such field.
        """
        return availability.is_available(model, field, self._settings.environment)

    def enum_values(self, enum: type[EnumT]) -> list[EnumT]:
        """
        Return the members of a generated enum that this environment accepts.

        A generated enum carries every environment's values; this gives the
        ones the selected environment's schema declares, for a dropdown or a
        check before sending.

        Parameters
        ----------
        enum : type[Enum]
            A generated enum, from ``gpp_client.generated.enums``.

        Returns
        -------
        list[Enum]
            The members the selected environment has, in declaration order.
        """
        return availability.enum_values(enum, self._settings.environment)

    def _enable_dev_logging(self) -> None:
        """
        Enable debug-level console logging for development purposes.
        """
        _enable_dev_console_logging()
        logger.debug("Logging enabled for GPPClient")

    async def close(self) -> None:
        """
        Close any underlying connections held by the client.

        A caller-supplied ``http_client`` is left open.
        """
        logger.debug("Closing GPPClient connections")
        await self._rest.close()
        if self._owns_http_client:
            await self._graphql.http_client.aclose()

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
