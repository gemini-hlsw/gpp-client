import os
from typing import Optional

from .api._client import _GPPClient
from .config import GPPConfig
from .constants import GPPConstants, GPPEnvironment
from .managers import (
    CallForProposalsManager,
    GroupManager,
    ObservationManager,
    ProgramManager,
    ProgramNoteManager,
    SiteStatusManager,
    TargetManager,
)
from .patches import patch_base_operations_graphql_field_get_formatted_variables

# Apply patch to fix inner includeDelete bug.
patch_base_operations_graphql_field_get_formatted_variables()


class GPPClient:
    """
    Main entry point for interacting with the GPP GraphQL API.

    This client provides access to all supported resource managers, including
    programs, targets, observations, and more. It handles authentication,
    configuration, and connection setup automatically.

    Parameters
    ----------
    token : str, optional
        The bearer token used for authentication. If not provided, it will be loaded
        from the ``GPP_TOKEN`` environment variable or the local configuration file.
    environment : GPPEnvironment, optional
        The GPP deployment to connect to ("production", "staging", "development").
        Defaults to ``GPP_ENV`` environment variable or the config file, or falls back to "production".

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
    """

    def __init__(
        self,
        *,
        token: Optional[str] = None,
        environment: Optional[GPPEnvironment] = None,
    ) -> None:
        self.config = GPPConfig()

        # Determine which environment and token to use.
        resolved_token, resolved_environment = self._resolve_credentials(
            token=token, environment=environment
        )
        url = GPPConstants.graphql_url(resolved_environment)
        headers = self._build_headers(resolved_token)
        self._client = _GPPClient(url=url, headers=headers)

        # Initialize the managers.
        self.program_note = ProgramNoteManager(self)
        self.target = TargetManager(self)
        self.program = ProgramManager(self)
        self.call_for_proposals = CallForProposalsManager(self)
        self.observation = ObservationManager(self)
        # SiteStatusManager doesn't use the client so don't pass self.
        self.site_status = SiteStatusManager()
        self.group = GroupManager(self)

    @staticmethod
    def set_credentials(
        token: str, environment: Optional[GPPEnvironment] = None
    ) -> None:
        """
        Set and persist GPP credentials in the local configuration file.

        This method creates or updates the stored credentials using the standard
        configuration path defined by `typer.get_app_dir()`.

        Parameters
        ----------
        token : str
            The bearer token used for authentication.
        environment : GPPEnvironment, optional
            The selected environment to connect to.
        """
        config = GPPConfig()
        config.set_credentials(token=token, environment=environment)

    def _build_headers(self, token: str) -> dict[str, str]:
        return {"Authorization": f"Bearer {token}"}

    def _resolve_credentials(
        self,
        token: Optional[str] = None,
        environment: Optional[GPPEnvironment] = None,
    ) -> tuple[str, str]:
        """
        Resolve the GPP environment and authentication token.

        Environment resolution order:
        1. Function argument
        2. Environment variable: GPP_ENV
        3. Config file
        4. Default to PRODUCTION

        Token resolution order:
        1. Function argument
        2. Environment variable: GPP_TOKEN
        3. Config file

        Returns
        -------
        GPPEnvironment
            The resolved environment.
        str
            The resolved authentication token.

        Raises
        ------
        ValueError
            If the token could not be resolved.
        """
        # Resolve environment
        env_str = environment or os.getenv("GPP_ENV")
        if isinstance(env_str, str):
            try:
                resolved_env = GPPEnvironment(env_str.lower())
            except ValueError:
                resolved_env = GPPEnvironment.PRODUCTION
        elif isinstance(env_str, GPPEnvironment):
            resolved_env = env_str
        else:
            resolved_env = self.config.get_environment()

        # Resolve token.
        _, config_token = self.config.get_credentials()
        resolved_token = token or os.getenv("GPP_TOKEN") or config_token

        if not resolved_token:
            raise ValueError(
                "Missing GPP token. Provide via argument, env var, or config file."
            )

        return resolved_token, resolved_env

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
            return False, str(exc)
