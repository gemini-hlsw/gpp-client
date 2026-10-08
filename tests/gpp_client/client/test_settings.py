"""
Tests for GPP settings.
"""

from pydantic import SecretStr
from pydantic_settings import TomlConfigSettingsSource

from gpp_client.settings import GPPSettings, _unwrap


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
