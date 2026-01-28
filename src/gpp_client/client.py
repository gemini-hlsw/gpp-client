import logging
from typing import Optional

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
            _enable_dev_console_logging()
            logger.debug("Logging enabled for GPPClient")

        logger.debug("Initializing GPPClient")
        self.config = config or GPPConfig()

        # Normalize env to GPPEnvironment if provided as str.
        if isinstance(env, str):
            env = GPPEnvironment(env.upper())

        # Resolve credentials.
        resolved_url, resolved_token, resolved_env = CredentialResolver.resolve(
            env=env, token=token, config=self.config
        )
        logger.info("Using environment: %s", resolved_env.value)

        headers = self._build_headers(resolved_token)
        self._client = _GPPClient(url=resolved_url, headers=headers)
        self._restapi = _GPPRESTClient(resolved_url, resolved_token)

        # Initialize the managers.
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

    def _build_headers(self, token: str) -> dict[str, str]:
        return {"Authorization": f"Bearer {token}"}

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
        await self._restapi.close()

    async def __aenter__(self) -> "GPPClient":
        return self

    async def __aexit__(self, exc_type, exc, tb) -> None:
        await self.close()
