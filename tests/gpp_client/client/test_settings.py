"""
Tests for GPP settings.
"""

from pydantic import SecretStr

from gpp_client.settings import _unwrap, get_config_path


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


def test_config_file_lives_in_a_dot_folder_in_home(monkeypatch, tmp_path) -> None:
    """
    Ensure the configuration file is ``~/.gpp-client/config.toml`` on every
    POSIX system, macOS included.
    """
    monkeypatch.setenv("HOME", str(tmp_path))

    assert get_config_path() == tmp_path / ".gpp-client" / "config.toml"
