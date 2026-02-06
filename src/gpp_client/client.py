"""
This module provides the main entry point for interacting with GPP.
"""

__all__ = ["GPPClient"]

import logging
from typing import Optional
from urllib.parse import urlsplit, urlunsplit

from gpp_client.api._client import _GPPClient
from gpp_client.config import GPPConfig, GPPEnvironment
from gpp_client.credentials import CredentialResolver
from gpp_client.logging_utils import _enable_dev_console_logging
from gpp_client.managers import (
    AttachmentManager,
    CallForProposalsManager,
    ConfigurationRequestManager,
    GroupManager,
    ObservationManager,
    ProgramManager,
    ProgramNoteManager,
    SiteStatusManager,
    TargetManager,
    WorkflowStateManager,
)
from gpp_client.rest import _GPPRESTClient

logger = logging.getLogger(__name__)


class GPPClient:
    """
    Main entry point for interacting with the GPP GraphQL API.

    This client provides access to all supported resource managers, including
    programs, targets, observations, and more. It handles
    authentication, configuration, and connection setup automatically.

    Parameters
    ----------
    env : GPPEnvironment | str, optional
        The GPP environment to connect to (e.g., ``DEVELOPMENT``, ``STAGING``,
        ``PRODUCTION``). If not provided, it will be loaded from the
        local configuration file or defaults to ``PRODUCTION``.
    token : str, optional
        The bearer token used for authentication. If not provided, it will be loaded
        from the ``GPP_TOKEN`` environment variable or the local configuration file.
    config : GPPConfig, optional
        An optional GPPConfig instance to use for configuration management. If not
        provided, a new instance will be created and loaded from the default path.
    _debug : bool, default=True
        If ``True``, enables debug-level console logging for development purposes.

    Attributes
    ----------
    config : GPPConfig
        Interface to read and write local GPP configuration settings.
    program_note : ProgramNoteManager
        Manager for program notes (e.g., create, update, list).
    target : TargetManager
        Manager for targets in proposals or observations.
    program : ProgramManager
        Manager for proposals and observing programs.
    call_for_proposals : CallForProposalsManager
        Manager for open Calls for Proposals (CFPs).
    observation : ObservationManager
        Manager for observations submitted under proposals.
    site_status : SiteStatusManager
        Manager for current status of Gemini North and South.
    group : GroupManager
        Manager for groups.
    configuration_request : ConfigurationRequestManager
        Manager for configuration requests.
    workflow_state : WorkflowStateManager
        Manager for observation workflow states.
    attachment : AttachmentManager
        Manager for attachments associated with proposals and observations.
    """

    def __init__(
        self,
        *,
        env: GPPEnvironment | str | None = None,
        token: str | None = None,
        config: GPPConfig | None = None,
        _debug: bool = True,
    ) -> None:
        if _debug:
            self._enable_dev_logging()

        logger.debug("Initializing GPPClient")
        self.config = config or self._create_config()

        # Normalize env to GPPEnvironment if provided as str.
        if isinstance(env, str):
            env = GPPEnvironment(env)

        # Resolve credentials and URLs based on the provided environment.
        resolved_url, resolved_token, resolved_env = self._resolve_credentials(
            env=env, token=token, config=self.config
        )
        resolved_base_url = self._get_base_url(resolved_url)
        resolved_ws_url = self._get_ws_url(resolved_base_url)
        logger.info("Using environment: %s", resolved_env.value)

        self._client = self._create_graphql_client(
            url=resolved_url, token=resolved_token, ws_url=resolved_ws_url
        )
        self._rest_client = self._create_rest_client(
            url=resolved_base_url, token=resolved_token
        )

        # Initialize the managers.
        self._init_managers()

    def _create_config(self) -> GPPConfig:
        """
        Create a new GPPConfig instance.
        """
        return GPPConfig()

    def _create_graphql_client(
        self, *, url: str, token: str, ws_url: str
    ) -> _GPPClient:
        """
        Create a new _GPPClient instance for GraphQL requests.
        """
        headers = self._build_headers(token)
        return _GPPClient(
            url=url, headers=headers, ws_url=ws_url, ws_connection_init_payload=headers
        )

    def _create_rest_client(self, *, url: str, token: str) -> _GPPRESTClient:
        """
        Create a new _GPPRESTClient instance for REST requests.
        """
        return _GPPRESTClient(url, token)

    def _enable_dev_logging(self) -> None:
        """
        Enable debug-level console logging for development purposes.
        """
        _enable_dev_console_logging()
        logger.debug("Logging enabled for GPPClient")

    def _init_managers(self) -> None:
        """
        Initialize all manager instances for the client.
        """
        self.program_note = ProgramNoteManager(self)
        self.target = TargetManager(self)
        self.program = ProgramManager(self)
        self.call_for_proposals = CallForProposalsManager(self)
        self.observation = ObservationManager(self)
        # SiteStatusManager doesn't use the client so don't pass self.
        self.site_status = SiteStatusManager()
        self.group = GroupManager(self)
        self.configuration_request = ConfigurationRequestManager(self)
        self.workflow_state = WorkflowStateManager(self)
        self.attachment = AttachmentManager(self)

    @staticmethod
    def set_credentials(
        env: GPPEnvironment | str, token: str, activate: bool = False, save: bool = True
    ) -> None:
        """
        Helper to set the token for a given environment and optionally activate it.
        This gets around having to create a ``GPPConfig`` instance manually.

        Parameters
        ----------
        env : GPPEnvironment | str
            The environment to store the token for.
        token : str
            The bearer token.
        activate : bool, optional
            Whether to set the given environment as active. Default is ``False``.
        save : bool, optional
            Whether to save the configuration to disk immediately. Default is ``True``.
        """
        config = GPPConfig()
        config.set_credentials(env, token, activate=activate, save=save)

    @staticmethod
    def _get_base_url(url: str) -> str:
        """
        Get the base URL for the GraphQL endpoint by stripping any path components from
        the given URL.
        """
        parsed = urlsplit(url)
        # Remove any path components, keep scheme and netloc.
        return urlunsplit((parsed.scheme, parsed.netloc, "", "", ""))

    @staticmethod
    def _get_ws_url(base_url: str) -> str:
        """
        Get the WebSocket URL corresponding to the given base URL.
        """
        parsed = urlsplit(base_url)
        # Use wss for https and ws for http.
        ws_scheme = "wss" if parsed.scheme == "https" else "ws"
        return urlunsplit((ws_scheme, parsed.netloc, "/ws", "", ""))

    @staticmethod
    def _build_headers(token: str) -> dict[str, str]:
        """
        Build the headers for the GraphQL endpoint request.
        """
        return {"Authorization": f"Bearer {token}"}

    def _resolve_credentials(
        self,
        *,
        env: GPPEnvironment | None,
        token: str | None,
        config: GPPConfig,
    ) -> tuple[str, str, GPPEnvironment]:
        """
        Resolve the credentials for the given environment and token.
        """
        return CredentialResolver.resolve(env=env, token=token, config=config)

    async def is_reachable(self) -> tuple[bool, Optional[str]]:
        """
        Check if the GPP GraphQL endpoint is reachable and authenticated.

        Returns
        -------
        bool
            ``True`` if the connection and authentication succeed, ``False`` otherwise.
        str, optional
            The error message if the connection failed.
        """
        logger.debug("Checking if GPP GraphQL endpoint is reachable")
        query = """
            {
                __schema {
                    queryType {
                    name
                    }
                }
            }
        """
        try:
            response = await self._client.execute(query)
            # Raise for any responses which are not a 2xx success code.
            response.raise_for_status()
            return True, None
        except Exception as exc:
            logger.debug("GPP GraphQL endpoint is not reachable: %s", exc)
            return False, str(exc)

    async def close(self) -> None:
        """
        Close any underlying connections held by the client.
        """
        logger.debug("Closing GPPClient connections")
        await self._rest_client.close()

    async def __aenter__(self) -> "GPPClient":
        return self

    async def __aexit__(self, exc_type, exc, tb) -> None:
        await self.close()
