"""Configuration class for the GPP client."""

__all__ = ["GPPConfig"]

from pathlib import Path
from typing import Any, Optional

import toml
import typer


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
        Return the stored API URL and token.

        Returns
        -------
        tuple[Optional[str], Optional[str]]
            The URL and token if set, otherwise ``None`` for missing values.
        """
        creds = self._data.get("credentials", {})
        return creds.get("url"), creds.get("token")

    def set_credentials(self, url: str, token: str) -> None:
        """
        Set new API credentials and save the configuration.

        Parameters
        ----------
        url : str
            The GraphQL API URL.
        token : str
            The bearer token for authentication.
        """
        self._data.setdefault("credentials", {})
        self._data["credentials"]["url"] = url
        self._data["credentials"]["token"] = token
        self.save()

    def credentials_set(self) -> bool:
        """
        Check whether both URL and token are set.

        Returns
        -------
        bool
            ``True`` if both credentials are present, ``False`` otherwise.
        """
        url, token = self.get_credentials()
        return bool(url and token)

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
