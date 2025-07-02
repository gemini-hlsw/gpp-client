import os
from typing import Optional

from .api._client import _GPPClient
from .config import GPPConfig
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
    programs, targets, observations, and more. It handles
    authentication, configuration, and connection setup automatically.

    Parameters
    ----------
    url : str, optional
        The base URL of the GPP GraphQL API. If not provided, it will be loaded from
        the ``GPP_URL`` environment variable or the local configuration file.
    token : str, optional
        The bearer token used for authentication. If not provided, it will be loaded
        from the ``GPP_TOKEN`` environment variable or the local configuration file.

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
        url: Optional[str] = None,
        token: Optional[str] = None,
    ) -> None:
        self.config = GPPConfig()

        # Determine which url and token to use.
        resolved_url, resolved_token = self._resolve_credentials(url=url, token=token)

        headers = self._build_headers(resolved_token)
        self._client = _GPPClient(url=resolved_url, headers=headers)

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
    def set_credentials(url: str, token: str) -> None:
        """
        Set and persist GPP credentials in the local configuration file.

        This method creates or updates the stored credentials using the standard
        configuration path defined by `typer.get_app_dir()`.

        Parameters
        ----------
        url : str
            The GraphQL API base URL to store.
        token : str
            The bearer token used for authentication.
        """
        config = GPPConfig()
        config.set_credentials(url, token)

    def _build_headers(self, token: str) -> dict[str, str]:
        return {"Authorization": f"Bearer {token}"}

    def _resolve_credentials(
        self,
        url: Optional[str] = None,
        token: Optional[str] = None,
    ) -> tuple[str, str]:
        """
        Resolve the GPP GraphQL credentials using precedence rules.

        This function looks for credentials in the following order:
        1. Direct function arguments (`url`, `token`).
        2. Environment variables `GPP_URL` and `GPP_TOKEN`.
        3. Configuration file.

        Parameters
        ----------
        url : str, optional
            The GraphQL endpoint URL. Overrides env and config if provided.
        token : str, optional
            The bearer token for authentication. Overrides env and config if provided.

        Returns
        -------
        str
            The URL for the GraphQL endpoint.
        str
            The token for authentication.

        Raises
        ------
        ValueError
            If neither the `url` nor `token` could be resolved from any source.
        """
        config_url, config_token = self.config.get_credentials()
        resolved_url = url or os.getenv("GPP_URL") or config_url
        resolved_token = token or os.getenv("GPP_TOKEN") or config_token

        if not resolved_url or not resolved_token:
            raise ValueError(
                "Missing GPP URL or GPP token. Provide via args, environment, or "
                "in configuration file."
            )

        return resolved_url, resolved_token

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
