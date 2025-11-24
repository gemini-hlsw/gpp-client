"""
Configuration class for the GPP client.
"""

__all__ = ["GPPConfig"]

import logging
from pathlib import Path

import toml
import typer
from pydantic import ValidationError
from toml import TomlDecodeError

from gpp_client.config.defaults import GPPDefaults
from gpp_client.config.environment import GPPEnvironment
from gpp_client.config.models import ConfigFile
from gpp_client.exceptions import GPPClientError, GPPValidationError

logger = logging.getLogger(__name__)


class GPPConfig:
    """
    Manage loading, saving, and updating GPP client configuration.

    This class manages user tokens and environment settings, stored in a TOML file.
    """

    def __init__(self) -> None:
        self.path = self._get_app_dir()
        self.directory = self.path.parent
        self._data = self._load()

    @staticmethod
    def _get_app_dir() -> Path:
        """
        Get the path to the configuration file using ``typer.get_app_dir()``.

        Returns
        -------
        Path
            Full path to the configuration file.
        """
        return (
            Path(typer.get_app_dir(GPPDefaults.app_name, force_posix=True))
            / GPPDefaults.config_filename
        )

    def _load(self) -> ConfigFile:
        """
        Load configuration data from disk.

        Returns
        -------
        ConfigFile
            The validated configuration model.

        Raises
        ------
        GPPValidationError
            If the TOML content is invalid.
        """
        if self.exists():
            try:
                data = toml.load(self.path)
                return ConfigFile(**data)
            except (ValidationError, TomlDecodeError) as exc:
                logger.error("Invalid configuration file at %s: %s", self.path, exc)
                raise GPPValidationError(f"{exc}") from None
        return ConfigFile()

    def exists(self) -> bool:
        """
        Whether the configuration file exists.

        Returns
        -------
        bool
            ``True`` if the config file exists, ``False`` otherwise.
        """
        return self.path.exists()

    def save(self) -> None:
        """
        Save the current configuration data to disk.
        """
        logger.debug("Saving config to %s", self.path)
        self.path.parent.mkdir(parents=True, exist_ok=True)
        self.path.write_text(toml.dumps(self.to_dict()))
        self._data = self._load()

    @property
    def active_env(self) -> GPPEnvironment:
        """
        Return the currently active environment.

        Returns
        -------
        GPPEnvironment
            The active GPP environment.
        """
        return self._data.env

    @property
    def active_token(self) -> str | None:
        """
        Return the token for the currently active environment.

        Returns
        -------
        str | None
            The token for the active environment, or ``None`` if not set.
        """
        return self.get_token_for(self.active_env)

    @property
    def has_credentials(self) -> bool:
        """
        Checks whether credentials are set for the current environment.

        Returns
        -------
        bool
            ``True`` if a token is set for the active environment, ``False`` otherwise.
        """
        token = self.active_token
        return bool(token and token.strip())

    def get_token_for(self, env: GPPEnvironment | str) -> str | None:
        """
        Return the token for a specific environment.

        Parameters
        ----------
        env : GPPEnvironment | str
            The environment to get the token for.

        Returns
        -------
        str | None
            The token for the specified environment, or ``None`` if not set.
        """
        env = GPPEnvironment(env)
        return getattr(self._data.tokens, env.value)

    def get_all_envs_with_tokens(self) -> dict[GPPEnvironment, str]:
        """
        Return all environments with non-empty tokens.

        Returns
        -------
        dict[GPPEnvironment, str]
            A dictionary mapping environment names to their non-empty tokens.
        """
        return {
            GPPEnvironment(key): token
            for key, token in self._data.tokens.model_dump().items()
            if token and token.strip()
        }

    def set_token(
        self, env: GPPEnvironment | str, token: str, save: bool = False
    ) -> None:
        """
        Store a token for the given environment without activating it.

        Parameters
        ----------
        env : GPPEnvironment | str
            The environment to store the token for.
        token : str
            The bearer token.
        save : bool, default=False
            Whether to save the configuration to disk immediately.

        Raises
        ------
        GPPValidationError
            If the provided token is empty or whitespace.
        """
        if not token or not token.strip():
            raise GPPValidationError(
                "Token cannot be empty or whitespace. Use 'clear_token()' to remove it."
            )

        logger.debug("Setting token for %s", env)
        env = GPPEnvironment(env)
        setattr(self._data.tokens, env.value, token)
        if save:
            self.save()

    def clear_token(self, env: GPPEnvironment | str, save: bool = False) -> None:
        """
        Clear the token for the given environment.

        Parameters
        ----------
        env : GPPEnvironment | str
            The environment to clear the token for.
        save : bool, default=False
            Whether to save the configuration to disk immediately.
        """
        logger.debug("Clearing token for %s", env)
        env = GPPEnvironment(env)
        setattr(self._data.tokens, env.value, None)
        if save:
            self.save()

    def clear_tokens(self, save: bool = False) -> None:
        """
        Clear all stored tokens for all environments.

        Parameters
        ----------
        save : bool, default=False
            Whether to save the configuration to disk immediately.
        """
        logger.warning("Clearing all stored tokens")
        for env in GPPEnvironment:
            setattr(self._data.tokens, env.value, None)
        if save:
            self.save()

    def activate(self, env: GPPEnvironment | str, save: bool = False) -> None:
        """
        Activate the given environment.

        Parameters
        ----------
        env : GPPEnvironment | str
            The environment to activate.
        save : bool, default=False
            Whether to save the configuration to disk immediately.
        """
        logger.info("Activating environment %s", env)
        env = GPPEnvironment(env)
        self._data.env = env
        if save:
            self.save()

    def set_credentials(
        self,
        env: GPPEnvironment | str,
        token: str,
        activate: bool = True,
        save: bool = False,
    ) -> None:
        """
        Set the token for a given environment and optionally activate it. By default, the environment will be activated.

        Parameters
        ----------
        env : GPPEnvironment | str
            The environment to store the token for.
        token : str
            The bearer token.
        activate : bool, default=True
            Whether to activate the given environment.
        save : bool, default=False
            Whether to save the configuration to disk immediately.

        Raises
        ------
        GPPValidationError
            If the provided token is empty or whitespace.
        """
        logger.info("Setting credentials for %s", env)
        self.set_token(env, token, save=False)
        if activate:
            self.activate(env, save=save)
        elif save:
            self.save()

    def disable_env_vars(self, save: bool = False) -> None:
        """
        Disable the use of environment variables for configuration.

        Parameters
        ----------
        save : bool, default=False
            Whether to save the configuration to disk immediately.
        """
        logger.debug("Disabling environment variables for configuration")
        self._data.disable_env_vars = True
        if save:
            self.save()

    def enable_env_vars(self, save: bool = False) -> None:
        """
        Enable the use of environment variables for configuration.

        Parameters
        ----------
        save : bool, default=False
            Whether to save the configuration to disk immediately.
        """
        logger.debug("Enabling environment variables for configuration")
        self._data.disable_env_vars = False
        if save:
            self.save()

    def use_env_vars(self) -> bool:
        """
        Whether to use environment variables based on config.

        Returns
        -------
        bool
            ``True`` if environment variables should be used, ``False`` otherwise.
        """
        return not self._data.disable_env_vars

    @staticmethod
    def create_default_config_file() -> None:
        """
        Create an empty configuration file with placeholder tokens.
        """
        logger.debug("Creating default config file at %s", GPPConfig._get_app_dir())
        default = ConfigFile()
        path = GPPConfig._get_app_dir()
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(toml.dumps(default.model_dump()))
        logger.info("Default config file created at %s", path)

    def to_dict(self) -> dict:
        """
        Return the configuration as a dictionary.

        Returns
        -------
        dict
            The configuration data as a dictionary.
        """
        try:
            return self._data.model_dump()
        except Exception as exc:
            logger.error("Failed to convert config to dict: %s", exc)
            raise GPPClientError(f"Failed to convert config to dict: {exc}") from None

    def to_json(self) -> str:
        """
        Return the configuration as a JSON string.

        Returns
        -------
        str
            The configuration data as a JSON string.
        """
        try:
            return self._data.model_dump_json()
        except Exception as exc:
            logger.error("Failed to convert config to JSON: %s", exc)
            raise GPPClientError(f"Failed to convert config to JSON: {exc}") from None

    def to_toml(self) -> str:
        """
        Return the configuration as a TOML string.

        Returns
        -------
        str
            The configuration data as a TOML string.
        """
        try:
            return toml.dumps(self.to_dict())
        except Exception as exc:
            logger.error("Failed to convert config to TOML: %s", exc)
            raise GPPClientError(f"Failed to convert config to TOML: {exc}") from None
