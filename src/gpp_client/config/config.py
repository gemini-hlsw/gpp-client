"""Configuration class for the GPP client."""

__all__ = ["GPPConfig"]

from pathlib import Path
from typing import Any, Optional

import toml
import typer

from ..constants import GPPEnvironment


class GPPConfig:
    """Manage loading, saving, and updating GPP client configuration."""

    _APP_NAME = "GPP Client"

    def __init__(self) -> None:
        self._path = (
            Path(typer.get_app_dir(self._APP_NAME, force_posix=True)) / "config.toml"
        )
        self._data = self._load()

    def _load(self) -> dict[str, Any]:
        """
        Load configuration data from disk.

        Returns
        -------
        dict[str, Any]
            The configuration data if found, otherwise an empty dictionary.
        """
        if self.exists():
            return toml.load(self.path)
        return {}

    def get_environment(self) -> GPPEnvironment:
        """
        Return the stored GPP environment.

        Returns
        -------
        GPPEnvironment
            The configured environment (default is PRODUCTION).
        """
        raw = self._data.get("credentials", {}).get("environment")
        if not raw:
            return GPPEnvironment.PRODUCTION

        try:
            return GPPEnvironment(raw.lower())
        except ValueError:
            return GPPEnvironment.PRODUCTION

    def save(self) -> None:
        """Save the current configuration data to disk."""
        self.path.parent.mkdir(parents=True, exist_ok=True)
        self.path.write_text(toml.dumps(self._data))

        # Reload to read the new credentials.
        self._data = self._load()

    def exists(self) -> bool:
        """
        Whether the configuration file exists.

        Returns
        -------
        bool
            ``True`` if the config file exists, ``False`` otherwise.
        """
        return self.path.exists()

    def get(self) -> dict[str, Any]:
        """
        Return the full configuration dictionary.

        Returns
        -------
        dict[str, Any]
            The configuration data.
        """
        return self._data

    def get_credentials(self) -> tuple[Optional[str], Optional[str]]:
        """
        Return the stored environment and token.

        Returns
        -------
        tuple[Optional[str], Optional[str]]
            The environment and token if set, otherwise ``None`` for missing values.
        """
        creds = self._data.get("credentials", {})
        return creds.get("environment"), creds.get("token")

    def set_credentials(self, environment: str, token: str) -> None:
        """
        Set new API credentials and save the configuration.

        Parameters
        ----------
        environment : str
            The GPP environment (production, staging, development).
        token : str
            The bearer token for authentication.
        """
        self._data.setdefault("credentials", {})
        self._data["credentials"]["environment"] = environment
        self._data["credentials"]["token"] = token
        self.save()

    def credentials_set(self) -> bool:
        """
        Check whether both environment and token are set.

        Returns
        -------
        bool
            ``True`` if both credentials are present, ``False`` otherwise.
        """
        environment, token = self.get_credentials()
        return bool(environment and token)

    @property
    def path(self) -> Path:
        """
        Path to the configuration file.

        Returns
        -------
        Path
            Full path to the configuration file.
        """
        return self._path
