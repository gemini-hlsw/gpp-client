"""
Runtime settings for the installed GPP client package.
"""

import tomllib
from enum import Enum
from pathlib import Path
from typing import Any

import typer
from pydantic import Field, SecretStr, field_validator
from pydantic.fields import FieldInfo
from pydantic_settings import (
    BaseSettings,
    DotEnvSettingsSource,
    EnvSettingsSource,
    InitSettingsSource,
    PydanticBaseSettingsSource,
    SettingsConfigDict,
    TomlConfigSettingsSource,
)

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
    Each setting comes from the first of: an argument, the environment
    variable, the ``.env`` file in the current folder, the configuration
    file, the default.

    Supported environment variables:
      - ``GPP_ENVIRONMENT``
      - ``GPP_TOKEN`` (production)
      - ``GPP_DEVELOPMENT_TOKEN``
      - ``GPP_DEBUG``

    An empty value counts as unset. So does an environment made only of
    spaces, which lets the next source set it.
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
        Read the configuration file after the ``.env`` file.

        Parameters
        ----------
        settings_cls : type[BaseSettings]
            The settings class being built.
        init_settings : PydanticBaseSettingsSource
            Arguments to the settings class.
        env_settings : PydanticBaseSettingsSource
            Environment variables.
        dotenv_settings : PydanticBaseSettingsSource
            The ``.env`` file.
        file_secret_settings : PydanticBaseSettingsSource
            Secret files.

        Returns
        -------
        tuple[PydanticBaseSettingsSource, ...]
            The sources, first match wins.

        Raises
        ------
        GPPClientError
            If the configuration file is not valid TOML or holds a key that
            is not a setting.
        """
        sources = [init_settings, env_settings, dotenv_settings]
        path = get_config_path()
        if path.is_file():
            try:
                toml_source = TomlConfigSettingsSource(settings_cls, toml_file=path)
            except tomllib.TOMLDecodeError as exc:
                raise GPPClientError(
                    f"Cannot read {path}: it is not valid TOML ({exc})."
                ) from None
            valid = list(settings_cls.model_fields)
            unknown = [key for key in toml_source.toml_data if key not in valid]
            if unknown:
                raise GPPClientError(
                    f"Cannot read {path}: unknown keys {', '.join(unknown)}. "
                    f"Valid keys: {', '.join(valid)}."
                )
            sources.append(toml_source)
        return (
            *(_BlankEnvironmentIsUnset(source) for source in sources),
            file_secret_settings,
        )

    @field_validator("environment", mode="before")
    @classmethod
    def _parse_environment(cls, value: object) -> object:
        """
        Read an environment name in any case.
        """
        if isinstance(value, GPPEnvironment):
            return value
        return _environment_named(value)

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


class _BlankEnvironmentIsUnset(PydanticBaseSettingsSource):
    """
    Drop a blank environment from one source, so the next source can set it.
    """

    def __init__(self, source: PydanticBaseSettingsSource) -> None:
        super().__init__(source.settings_cls)
        self._source = source

    def get_field_value(
        self, field: FieldInfo, field_name: str
    ) -> tuple[Any, str, bool]:
        return self._source.get_field_value(field, field_name)

    def __call__(self) -> dict[str, Any]:
        data = self._source()
        value = data.get("environment")
        if isinstance(value, str) and not value.strip():
            return {k: v for k, v in data.items() if k != "environment"}
        return data


class SettingSource(Enum):
    """
    Where a setting's value came from.
    """

    ARGUMENT = "argument"
    VARIABLE = "variable"
    DOTENV = ".env file"
    CONFIG_FILE = "configuration file"
    DEFAULT = "default"


def settings_with_sources(
    **arguments: Any,
) -> tuple[GPPSettings, dict[str, SettingSource]]:
    """
    Build the settings and say where each one came from.

    The sources come from ``GPPSettings`` itself, so the attribution always
    follows the order the settings are read in.

    Parameters
    ----------
    **arguments : Any
        Arguments to ``GPPSettings``, which beat every other source.

    Returns
    -------
    tuple[GPPSettings, dict[str, SettingSource]]
        The settings, and the source of each setting by name.
    """
    built: list[PydanticBaseSettingsSource] = []

    class _Traced(GPPSettings):
        @classmethod
        def settings_customise_sources(
            cls, settings_cls: type[BaseSettings], **sources: PydanticBaseSettingsSource
        ) -> tuple[PydanticBaseSettingsSource, ...]:
            built.extend(super().settings_customise_sources(settings_cls, **sources))
            return tuple(built)

    traced = _Traced(**arguments)
    found = {key: SettingSource.DEFAULT for key in GPPSettings.model_fields}
    for source in reversed(built):
        for key in source():
            kind = _source_kind(source)
            if key in found and kind is not None:
                found[key] = kind
    # A plain GPPSettings, so the local subclass never shows in a repr.
    settings = GPPSettings.model_construct(
        _fields_set=traced.model_fields_set, **dict(traced)
    )
    return settings, found


def _source_kind(source: PydanticBaseSettingsSource) -> SettingSource | None:
    """
    Classify a settings source, or return ``None`` for one users never set.
    """
    inner = getattr(source, "_source", source)
    # Subclasses first: the TOML source is an init source, and .env an env one.
    if isinstance(inner, TomlConfigSettingsSource):
        return SettingSource.CONFIG_FILE
    if isinstance(inner, DotEnvSettingsSource):
        return SettingSource.DOTENV
    if isinstance(inner, EnvSettingsSource):
        return SettingSource.VARIABLE
    if isinstance(inner, InitSettingsSource):
        return SettingSource.ARGUMENT
    return None


def get_config_path() -> Path:
    """
    Get the path to the configuration file.

    Returns
    -------
    Path
        Path to the configuration file.
    """
    return Path(typer.get_app_dir(APP_NAME, force_posix=True)) / CONFIG_FILE_NAME


def _environment_named(value: object) -> GPPEnvironment:
    """
    Return the environment a name means, or raise naming the valid names.
    """
    try:
        return GPPEnvironment(value)
    except ValueError:
        valid = ", ".join(env.label for env in GPPEnvironment)
        # Not a ValueError, so pydantic raises it as is instead of wrapping it.
        raise GPPClientError(
            f"Unknown GPP environment {value!r}. Valid names: {valid}."
        ) from None


def _unwrap(secret: SecretStr | None) -> str | None:
    """
    Helper function to unwrap a ``SecretStr`` or return ``None`` if not provided.
    """
    return secret.get_secret_value() if secret else None
