"""
Runtime settings for the installed GPP client package.
"""

from pathlib import Path

import tomlkit
import typer
from pydantic import Field, SecretStr, field_validator
from pydantic_settings import (
    BaseSettings,
    PydanticBaseSettingsSource,
    SettingsConfigDict,
    TomlConfigSettingsSource,
)
from tomlkit.exceptions import TOMLKitError

from gpp_client.constants import APP_NAME, CONFIG_FILE_NAME
from gpp_client.environment import GPPEnvironment
from gpp_client.exceptions import GPPAuthError, GPPClientError

_ENV_PREFIX = "GPP_"


def _token_setting(environment: GPPEnvironment) -> str:
    """
    Return the setting holding an environment's token, read from its variable.
    """
    return environment.token_variable.removeprefix(_ENV_PREFIX).lower()


class GPPSettings(BaseSettings):
    """
    Effective runtime settings for the installed GPP client package.

    Notes
    -----
    Supported environment variables:
      - ``GPP_ENVIRONMENT``
      - ``GPP_TOKEN`` (production)
      - ``GPP_DEVELOPMENT_TOKEN``
      - ``GPP_DEBUG``

    An empty value counts as unset.
    """

    model_config = SettingsConfigDict(
        env_prefix=_ENV_PREFIX,
        env_file=".env",
        env_ignore_empty=True,
        extra="ignore",
    )
    environment: GPPEnvironment = Field(
        default=GPPEnvironment.PRODUCTION,
        description="The GPP environment to connect to.",
    )
    token: SecretStr | None = Field(
        default=None,
        description="GPP API token for the production environment.",
    )
    development_token: SecretStr | None = Field(
        default=None,
        description="GPP API token for the development environment.",
    )
    debug: bool = Field(
        default=False, description="Whether to enable debug logging for the client."
    )

    @field_validator("environment", mode="before")
    @classmethod
    def _parse_environment(cls, value: object) -> object:
        """
        Read an environment name in any case, and an empty one as production.
        """
        if isinstance(value, GPPEnvironment):
            return value
        if isinstance(value, str) and not value.strip():
            return GPPEnvironment.PRODUCTION
        try:
            return GPPEnvironment(value)
        except ValueError:
            valid = ", ".join(env.label for env in GPPEnvironment)
            # Not a ValueError, so pydantic raises it as is instead of wrapping it.
            raise GPPClientError(
                f"Unknown GPP environment {value!r}. Valid names: {valid}."
            ) from None

    @property
    def resolved_token(self) -> str:
        """
        Return the token for the selected environment.

        Returns
        -------
        str
            Resolved API token.

        Raises
        ------
        GPPAuthError
            If the selected environment has no token.
        """
        token = _unwrap(getattr(self, _token_setting(self.environment)))
        if token:
            return token
        raise GPPAuthError(
            f"A token is required for the {self.environment.label} "
            f"environment. Set '{self.environment.token_variable}'."
        )

    def with_token(self, token: str) -> "GPPSettings":
        """
        Return a copy whose selected environment uses ``token``.

        Parameters
        ----------
        token : str
            The API token.

        Returns
        -------
        GPPSettings
            The settings with the token in the selected environment's slot.
        """
        return self.model_copy(
            update={_token_setting(self.environment): SecretStr(token)}
        )

    @classmethod
    def settings_customise_sources(
        cls,
        settings_cls: type[BaseSettings],
        init_settings: PydanticBaseSettingsSource,
        env_settings: PydanticBaseSettingsSource,
        dotenv_settings: PydanticBaseSettingsSource,
        file_secret_settings: PydanticBaseSettingsSource,
    ) -> tuple[PydanticBaseSettingsSource, ...]:
        """
        Customise the settings sources to ensure the expected precedence order.

        Parameters
        ----------
        settings_cls : type[BaseSettings]
            The settings class being constructed.
        init_settings : PydanticBaseSettingsSource
            Source for initialization parameters.
        env_settings : PydanticBaseSettingsSource
            Source for environment variables.
        dotenv_settings : PydanticBaseSettingsSource
            Source for dotenv file.
        file_secret_settings : PydanticBaseSettingsSource
            Source for file secrets.

        Returns
        -------
        tuple[PydanticBaseSettingsSource, ...]
            Ordered tuple of settings sources.

        Notes
        -----
        The default precedence order is:
            1. Initialization parameters
            2. Environment variables
            3. Dotenv file
            4. App TOML file
            5. File secrets
        """
        config_path = get_config_path()

        toml_sources: tuple[PydanticBaseSettingsSource, ...] = ()
        if config_path.is_file():
            toml_sources = (
                TomlConfigSettingsSource(settings_cls, toml_file=config_path.resolve()),
            )

        return (
            init_settings,
            env_settings,
            dotenv_settings,
            *toml_sources,
            file_secret_settings,
        )


def get_config_path() -> Path:
    """
    Get the path to the configuration file.

    Returns
    -------
    Path
        Path to the configuration file.
    """
    return Path(typer.get_app_dir(APP_NAME)) / CONFIG_FILE_NAME


def set_default_environment(environment: GPPEnvironment | str) -> Path:
    """
    Store the default environment in the configuration file.

    The file and its folder are created if missing. The comments, layout and
    other settings of an existing file are kept.

    Parameters
    ----------
    environment : GPPEnvironment | str
        The environment to store.

    Returns
    -------
    Path
        The configuration file written.

    Raises
    ------
    GPPClientError
        If the existing file is not valid TOML, or its ``environment`` is not
        a single name.
    """
    environment = GPPEnvironment(environment)
    path = get_config_path()
    text = path.read_text(encoding="utf-8") if path.is_file() else ""
    try:
        document = tomlkit.parse(text)
    except TOMLKitError as exc:
        raise GPPClientError(
            f"Cannot update {path}: it is not valid TOML ({exc})."
        ) from None

    current = document.get("environment")
    if current is not None and not isinstance(current, str):
        raise GPPClientError(
            f"Cannot update {path}: environment must be a single name, "
            'such as "development".'
        )

    document["environment"] = environment.label

    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(tomlkit.dumps(document), encoding="utf-8")
    return path


def _unwrap(secret: SecretStr | None) -> str | None:
    """
    Helper function to unwrap a ``SecretStr`` or return ``None`` if not provided.
    """
    return secret.get_secret_value() if secret else None
