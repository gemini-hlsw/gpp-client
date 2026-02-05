"""
Credential resolution logic for the GPP client.
"""

__all__ = ["CredentialResolver"]

import logging
import re

from gpp_client.config import GPPConfig, GPPDefaults, GPPEnvironment
from gpp_client.credentials.env_var_reader import EnvVarReader
from gpp_client.exceptions import GPPAuthError

logger = logging.getLogger(__name__)


class CredentialResolver:
    """
    Resolves the effective GPP credentials to use based on priority.

    Priority order (high to low):
    1. Explicit arguments
    2. Environment variables (if enabled)
    3. Configuration file
    """

    @staticmethod
    def resolve(
        *,
        env: GPPEnvironment | None = None,
        token: str | None = None,
        config: GPPConfig | None = None,
    ) -> tuple[str, str, GPPEnvironment, str]:
        """
        Resolve the effective GPP URL, token, and environment.

        Parameters
        ----------
        env : GPPEnvironment | None, optional
            Optional explicit environment override.
        token : str | None, optional
            Optional explicit token override.
        config : GPPConfig | None, optional
            Optional GPPConfig instance. If ``None``, a new instance will be created
            and loaded if the configuration file exists.

        Returns
        -------
        tuple[str, str, GPPEnvironment, str]
            A tuple containing (URL, token, environment, WS URL).

        Raises
        ------
        GPPAuthError
            If no valid token could be resolved.
        """
        # Load config if not provided.
        config = config or GPPConfig()

        # Resolve environment and token.
        resolved_env = CredentialResolver.resolve_env(env=env, config=config)
        resolved_token = CredentialResolver.resolve_token(
            token=token, env=resolved_env, config=config
        )

        # Resolve URL based on environment.
        resolved_url = GPPDefaults.url[resolved_env]
        ws_url = re.sub(r"^https?://([^/]+).*", r"wss://\1/ws", resolved_url)

        return resolved_url, resolved_token, resolved_env, ws_url

    @staticmethod
    def resolve_env(
        *,
        env: GPPEnvironment | None = None,
        config: GPPConfig | None = None,
    ) -> GPPEnvironment:
        """
        Resolve the effective GPP environment to use.

        Parameters
        ----------
        env : GPPEnvironment | None, optional
            Optional explicit environment override.
        config : GPPConfig | None, optional
            The GPPConfig instance, if not provided a new instance will be created.

        Returns
        -------
        GPPEnvironment
            The resolved environment.
        """
        # Load config if not provided.
        config = config or GPPConfig()

        # Check explicit argument.
        if env is not None:
            logger.debug("Resolved environment from argument: %s", env.value)
            return env
        # Check environment variables if enabled.
        if config.use_env_vars():
            # Check for environment from env var.
            if env_from_env := EnvVarReader.get_env():
                logger.debug(
                    "Resolved environment from environment variable: %s",
                    env_from_env.value,
                )
                return env_from_env

        # Fallback to config file.
        fallback_env = config.active_env
        logger.debug("Resolved environment from config file: %s", fallback_env.value)
        return fallback_env

    @staticmethod
    def resolve_token(
        *,
        env: GPPEnvironment,
        token: str | None = None,
        config: GPPConfig | None = None,
    ) -> str:
        """
        Resolve the effective GPP token to use.

        Parameters
        ----------
        env : GPPEnvironment
            The GPP environment to resolve the token for.
        token : str | None, optional
            Optional explicit token override.
        config : GPPConfig | None, optional
            The GPPConfig instance, if not provided a new instance will be created.

        Returns
        -------
        str
            The resolved token.

        Raises
        ------
        GPPAuthError
            If no valid token could be resolved.
        """
        # Load config if not provided.
        config = config or GPPConfig()

        if token:
            logger.debug("Resolved token from argument")
            return token

        # Check environment variables if enabled.
        if config.use_env_vars():
            # Check for environment-specific token.
            if token := EnvVarReader.get_env_token(env):
                logger.debug(
                    "Resolved token from environment variable for %s", env.value
                )
                return token
            # Fallback to generic token.
            if token := EnvVarReader.get_token():
                logger.debug("Resolved token from fallback environment variable")
                return token

        # Fallback to config file.
        token = config.active_token

        # Validate token from config.
        if token is not None:
            token = token.strip()
        if token:
            logger.debug("Resolved token from config file for %s", env.value)
            return token

        raise GPPAuthError(
            f"No valid token found for environment '{env.value}'. "
            "Check your config file or environment variables."
        )
