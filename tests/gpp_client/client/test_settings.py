"""
Tests for GPP settings.
"""

import sys
from types import SimpleNamespace

import pytest
from pydantic import SecretStr
from pydantic_settings import TomlConfigSettingsSource

from gpp_client.environment import GPPEnvironment
from gpp_client.exceptions import GPPAuthError, GPPClientError
from gpp_client.settings import (
    GPPSettings,
    _get_packaged_environment,
    _resolve_token,
    _unwrap,
)


def test_resolved_token_requires_production_token_for_production(mocker) -> None:
    """
    Ensure production resolved_token fails without token.
    """
    mocker.patch(
        "gpp_client.settings._get_packaged_environment",
        return_value=GPPEnvironment.PRODUCTION,
    )
    settings = GPPSettings(token=None, development_token=SecretStr("dev"))
    with pytest.raises(GPPAuthError, match="GPP_TOKEN"):
        _ = settings.resolved_token


def test_resolved_token_requires_development_token_for_development() -> None:
    """
    Ensure development resolved_token fails without development token.
    """
    settings = GPPSettings(
        token=SecretStr("prod"),
        development_token=None,
        environment_override=GPPEnvironment.DEVELOPMENT,
    )
    with pytest.raises(GPPAuthError, match="GPP_DEVELOPMENT_TOKEN"):
        _ = settings.resolved_token


def test_unwrap_returns_string_value() -> None:
    """
    Ensure SecretStr is unwrapped correctly.
    """
    assert _unwrap(SecretStr("abc")) == "abc"


def test_unwrap_returns_none_for_none() -> None:
    """
    Ensure unwrap returns None when no value is provided.
    """
    assert _unwrap(None) is None


@pytest.mark.parametrize(
    ("environment", "token", "dev_token", "expected"),
    [
        (GPPEnvironment.PRODUCTION, "prod", None, "prod"),
        (GPPEnvironment.PRODUCTION, "prod", "dev", "prod"),
        (GPPEnvironment.DEVELOPMENT, None, "dev", "dev"),
        (GPPEnvironment.DEVELOPMENT, "prod", "dev", "dev"),
    ],
)
def test_resolve_token_success(
    environment: GPPEnvironment,
    token: str | None,
    dev_token: str | None,
    expected: str,
) -> None:
    """
    Ensure token resolution works for valid cases.
    """
    result = _resolve_token(
        environment=environment,
        token=SecretStr(token) if token else None,
        development_token=SecretStr(dev_token) if dev_token else None,
    )
    assert result == expected


@pytest.mark.parametrize(
    ("environment", "token", "dev_token"),
    [
        (GPPEnvironment.PRODUCTION, None, None),
        (GPPEnvironment.PRODUCTION, None, "dev"),
        (GPPEnvironment.DEVELOPMENT, None, None),
        (GPPEnvironment.DEVELOPMENT, "prod", None),
    ],
)
def test_resolve_token_failures(
    environment: GPPEnvironment,
    token: str | None,
    dev_token: str | None,
) -> None:
    """
    Ensure token resolution fails when the required environment-specific token
    is missing.
    """
    with pytest.raises(GPPAuthError):
        _resolve_token(
            environment=environment,
            token=SecretStr(token) if token else None,
            development_token=SecretStr(dev_token) if dev_token else None,
        )


def test_environment_uses_override() -> None:
    """
    Ensure environment_override takes precedence.
    """
    settings = GPPSettings(
        development_token=SecretStr("abc"),
        environment_override=GPPEnvironment.DEVELOPMENT,
    )
    assert settings.environment is GPPEnvironment.DEVELOPMENT


def test_environment_uses_packaged_environment(mocker) -> None:
    """
    Ensure packaged environment is used when no override.
    """
    mocker.patch(
        "gpp_client.settings._get_packaged_environment",
        return_value=GPPEnvironment.PRODUCTION,
    )

    settings = GPPSettings(token=SecretStr("abc"))

    assert settings.environment is GPPEnvironment.PRODUCTION


def test_get_packaged_environment_success(mocker) -> None:
    """
    Ensure packaged environment resolves correctly.
    """
    module = SimpleNamespace(PACKAGE_ENVIRONMENT="DEVELOPMENT")

    mocker.patch.dict(
        sys.modules,
        {"gpp_client.generated.package_environment": module},
    )

    result = _get_packaged_environment()

    assert result is GPPEnvironment.DEVELOPMENT


def test_get_packaged_environment_missing_module(mocker) -> None:
    """
    Ensure missing package environment raises GPPClientError.
    """
    module_name = "gpp_client.generated.package_environment"

    mocker.patch.dict(sys.modules, {module_name: None})

    with pytest.raises(GPPClientError):
        _get_packaged_environment()


def test_resolved_token_property_for_production(mocker) -> None:
    """
    Ensure resolved_token delegates correctly for production.
    """
    mocker.patch(
        "gpp_client.settings._get_packaged_environment",
        return_value=GPPEnvironment.PRODUCTION,
    )

    settings = GPPSettings(token=SecretStr("abc"))

    assert settings.resolved_token == "abc"


def test_resolved_token_property_for_development() -> None:
    """
    Ensure resolved_token delegates correctly for development.
    """
    settings = GPPSettings(
        development_token=SecretStr("abc"),
        environment_override=GPPEnvironment.DEVELOPMENT,
    )

    assert settings.resolved_token == "abc"


def test_settings_source_order_without_app_toml(mocker) -> None:
    """
    Ensure settings source precedence is correct when no app TOML file exists.
    """
    mock_path = mocker.Mock()
    mock_path.is_file.return_value = False
    mocker.patch("gpp_client.settings.get_config_path", return_value=mock_path)

    sources = GPPSettings.settings_customise_sources(
        GPPSettings,
        "init",
        "env",
        "dotenv",
        "secrets",
    )

    assert sources == ("init", "env", "dotenv", "secrets")


def test_settings_source_order_with_app_toml(
    mocker,
    tmp_path,
) -> None:
    """
    Ensure app TOML is inserted before file secrets when present.
    """
    config_path = tmp_path / "settings.toml"
    config_path.write_text("debug = true\n", encoding="utf-8")

    mocker.patch("gpp_client.settings.get_config_path", return_value=config_path)

    sources = GPPSettings.settings_customise_sources(
        GPPSettings,
        "init",
        "env",
        "dotenv",
        "secrets",
    )

    assert sources[:3] == ("init", "env", "dotenv")
    assert isinstance(sources[3], TomlConfigSettingsSource)
    assert sources[4] == "secrets"
