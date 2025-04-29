import os
from pathlib import Path
from typing import Generator

import pytest
import toml

from gpp_client.client import GPPClient


@pytest.fixture
def mock_config_file(tmp_path: Path, mocker) -> Generator[Path, None, None]:
    """Create a temporary GPP config file and patch typer.get_app_dir()."""
    config_dir = tmp_path / ".gpp-client"
    config_dir.mkdir(parents=True, exist_ok=True)
    config_path = config_dir / "config.toml"
    config_path.write_text(
        toml.dumps(
            {"credentials": {"url": "mock-url-config", "token": "mock-token-config"}}
        )
    )
    mocker.patch("typer.get_app_dir", return_value=config_dir)
    yield config_path


@pytest.fixture
def mock_env(mocker):
    """Patch environment variables for GPP credentials."""
    mocker.patch.dict(
        os.environ,
        {"GPP_URL": "mock-url-env", "GPP_TOKEN": "mock-token-env"},
        clear=True,
    )


class TestGPPClient:
    """Tests for GPPClient."""

    def test_credentials_from_args(self):
        """Test GPPClient resolves credentials from direct arguments."""
        client = GPPClient(url="mock-url-arg", token="mock-token-arg")
        assert client._transport.url == "mock-url-arg"
        assert client._transport.headers["Authorization"].startswith(
            "Bearer mock-token-arg"
        )

    def test_credentials_from_env(self, mock_env):
        """Test GPPClient resolves credentials from environment variables."""
        client = GPPClient()
        assert client._transport.url == "mock-url-env"
        assert client._transport.headers["Authorization"].startswith(
            "Bearer mock-token-env"
        )

    def test_credentials_from_file(self, mock_config_file):
        """Test GPPClient resolves credentials from config file."""
        client = GPPClient()
        assert client._transport.url == "mock-url-config"
        assert client._transport.headers["Authorization"].startswith(
            "Bearer mock-token-config"
        )

    def test_credentials_missing_all(self, mocker):
        """Test GPPClient raises ValueError if credentials cannot be resolved."""
        mocker.patch("typer.get_app_dir", return_value="/nonexistent")
        mocker.patch.dict(os.environ, {}, clear=True)  # clear all env

        with pytest.raises(ValueError, match="Missing GPP URL or GPP token"):
            GPPClient()

    def test_args_override_env_and_config(self, mock_env, mock_config_file):
        """Test that passed-in args take precedence over env and config file."""
        client = GPPClient(url="mock-url-arg", token="mock-token-arg")
        assert client._transport.url == "mock-url-arg"
        assert client._transport.headers["Authorization"].startswith(
            "Bearer mock-token-arg"
        )

    def test_env_overrides_config(self, mock_env, mock_config_file):
        """Test that env vars take precedence over the config file."""
        client = GPPClient()
        assert client._transport.url == "mock-url-env"
        assert client._transport.headers["Authorization"].startswith(
            "Bearer mock-token-env"
        )
