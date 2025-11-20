"""
Environment variable reader for the GPP client.
"""

__all__ = ["EnvVarReader"]

import os

from gpp_client.config import GPPDefaults, GPPEnvironment


class EnvVarReader:
    """
    Reader for GPP client environment variables.
    """

    @staticmethod
    def get_env() -> GPPEnvironment | None:
        """
        Get the GPP environment from environment variables.

        Returns
        -------
        GPPEnvironment | None
            The GPP environment if set, else ``None``.
        """
        raw_env = os.getenv(GPPDefaults.env_var_env)
        if raw_env:
            try:
                return GPPEnvironment(raw_env.upper())
            except ValueError:
                return None
        return None

    @staticmethod
    def get_env_token(env: GPPEnvironment) -> str | None:
        """
        Get the token for a specific environment from environment variables.

        Parameters
        ----------
        env : GPPEnvironment | str
            The GPP environment to get the token for.

        Returns
        -------
        str | None
            The token if found, else ``None``.
        """
        key = GPPDefaults.env_var_env_tokens.get(env)
        return os.getenv(key) if key else None

    @staticmethod
    def get_token() -> str | None:
        """
        Get the generic GPP token from environment variables.

        Returns
        -------
        str | None
            The generic token if found, else ``None``.
        """
        return os.getenv(GPPDefaults.env_var_token)
