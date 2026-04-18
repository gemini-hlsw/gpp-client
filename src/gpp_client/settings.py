"""
Runtime settings for the installed GPP client package.
"""

from pathlib import Path

import typer
from pydantic import Field, SecretStr
from pydantic_settings import (
    BaseSettings,
    PydanticBaseSettingsSource,
    SettingsConfigDict,
    TomlConfigSettingsSource,
)

from gpp_client.constants import APP_NAME, CONFIG_FILE_NAME
from gpp_client.environment import GPPEnvironment
from gpp_client.exceptions import GPPAuthError, GPPClientError


class GPPSettings(BaseSettings):
    """
    Effective runtime settings for the installed GPP client package.

    Notes
    -----
    Supported environment variables:
      - ``GPP_TOKEN``
      - ``GPP_DEVELOPMENT_TOKEN``
      - ``GPP_DEBUG``

    Token resolution behavior:
      - Production package uses ``token``.
      - Development package uses ``development_token``.
    """

    model_config = SettingsConfigDict(
        env_prefix="GPP_",
        env_file=".env",
        extra="ignore",
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
    environment_override: GPPEnvironment | None = Field(
        default=None,
        exclude=True,
        description="Explicit environment override for tooling and codegen.",
    )

    @property
    def resolved_token(self) -> str:
        """
        Return the token appropriate for the installed package environment.

        Returns
        -------
        str
            Resolved API token.

        Raises
        ------
        GPPAuthError
            If no valid token is available for the active environment.
        """
        return _resolve_token(
            environment=self.environment,
            token=self.token,
            development_token=self.development_token,
        )

    @property
    def environment(self) -> GPPEnvironment:
        """
        Determine the effective package environment.

        Returns
        -------
        GPPEnvironment
            Effective package environment, either from the override or the generated
            constant.
        """
        if self.environment_override is not None:
            return self.environment_override
        return _get_packaged_environment()

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

    # @model_validator(mode="after")
    # def validate_tokens(self) -> Self:
    #     """
    #     Ensure a valid token exists for the active environment.

    #     Returns
    #     -------
    #     Self
    #         Validated settings instance.
    #     """
    #     try:
    #         _ = self.resolved_token
    #     except GPPAuthError as exc:
    #         raise ValueError(str(exc)) from exc
    #     return self


def get_config_path() -> Path:
    """
    Get the path to the configuration file.

    Returns
    -------
    Path
        Path to the configuration file.
    """
    return Path(typer.get_app_dir(APP_NAME)) / CONFIG_FILE_NAME


def _unwrap(secret: SecretStr | None) -> str | None:
    """
    Helper function to unwrap a ``SecretStr`` or return ``None`` if not provided.
    """
    return secret.get_secret_value() if secret else None


def _get_packaged_environment() -> GPPEnvironment:
    """
    Helper function to get the package environment from the generated constant.
    """
    try:
        from gpp_client.generated.package_environment import PACKAGE_ENVIRONMENT
    except ModuleNotFoundError as exc:
        raise GPPClientError(
            "Generated package environment is unavailable. Pass 'environment_override'"
            " to GPPSettings or ensure the client is properly installed."
        ) from exc
    return GPPEnvironment(PACKAGE_ENVIRONMENT)


def _resolve_token(
    *,
    environment: GPPEnvironment,
    token: SecretStr | None,
    development_token: SecretStr | None,
) -> str:
    """
    Resolve the correct token for the given environment.
    """
    resolved_token = _unwrap(token)
    resolved_development_token = _unwrap(development_token)

    if environment is GPPEnvironment.DEVELOPMENT:
        if resolved_development_token:
            return resolved_development_token
        raise GPPAuthError(
            "A token is required for the development environment. "
            "Set 'GPP_DEVELOPMENT_TOKEN'."
        )

    if resolved_token:
        return resolved_token

    raise GPPAuthError(
        "A token is required for the production environment. Set 'GPP_TOKEN'."
    )
