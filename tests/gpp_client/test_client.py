import os
import tempfile
from pathlib import Path

import pytest
import toml

from gpp_client.client import load_gpp_config, resolve_credentials


@pytest.fixture
def mock_config_file(mocker):
    """Create a temporary GPP config file and patch Path.home()."""
    temp_dir = tempfile.TemporaryDirectory()
    config_path = Path(temp_dir.name) / ".gpp" / "config.toml"
    config_path.parent.mkdir(parents=True, exist_ok=True)
    config_path.write_text(
        toml.dumps({"url": "mock-url-config", "token": "mock-token-config"})
    )
    mocker.patch("pathlib.Path.home", return_value=Path(temp_dir.name))
    yield config_path
    temp_dir.cleanup()


@pytest.fixture
def mock_env(mocker):
    """Patch environment variables for GPP credentials."""
    mocker.patch.dict(
        os.environ,
        {"GPP_URL": "mock-url-env", "GPP_TOKEN": "mock-token-env"},
        clear=True,
    )


def test_load_gpp_config_from_file(mock_config_file):
    """Test loading configuration from file."""
    config = load_gpp_config()
    assert config["url"] == "mock-url-config"
    assert config["token"] == "mock-token-config"


def test_resolve_credentials_from_args():
    """Test getting credentials from args."""
    url, token = resolve_credentials(url="mock-url-arg", token="mock-token-arg")
    assert url == "mock-url-arg"
    assert token == "mock-token-arg"


def test_resolve_credentials_from_env(mock_env):
    """Test getting credentials from env."""
    url, token = resolve_credentials()
    assert url == "mock-url-env"
    assert token == "mock-token-env"


def test_resolve_credentials_from_file(mock_config_file):
    """Test getting credentials from config file."""
    url, token = resolve_credentials()
    assert url == "mock-url-config"
    assert token == "mock-token-config"


def test_resolve_credentials_missing_all(mocker):
    """Test raising issue if credentials are missing."""
    mocker.patch("pathlib.Path.home", return_value=Path("/wrong"))

    with pytest.raises(ValueError, match="Missing GPP URL or GPP token"):
        resolve_credentials()


def test_resolve_credentials_args_override_env_and_config(mock_env, mock_config_file):
    """Ensure that passed-in args take precedence over env and config file."""
    url, token = resolve_credentials(url="mock-url-arg", token="mock-token-arg")

    assert url == "mock-url-arg"
    assert token == "mock-token-arg"


def test_resolve_credentials_env_override_config(mock_env, mock_config_file):
    """Ensure that env vars take precedence over the config file."""
    url, token = resolve_credentials()

    assert url == "mock-url-env"
    assert token == "mock-token-env"
