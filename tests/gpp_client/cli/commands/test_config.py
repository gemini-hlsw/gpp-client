from pathlib import Path

import pytest

from gpp_client.cli.cli import app
from gpp_client.config import GPPConfig

_RESOURCE_NAME = "config"


@pytest.fixture
def isolated_config_env(tmp_path, mocker) -> Path:
    """Patch the configuration path with a temporary file for test isolation."""
    config_path = tmp_path / "config.toml"
    mocker.patch("gpp_client.config.GPPConfig.path", config_path)
    return config_path


class TestConfig:
    """Tests for the `config` CLI subcommands."""

    def test_show_empty_config_fails(self, isolated_config_env, cli_runner):
        """Verify that 'config show' exits with error when config is empty."""
        result = cli_runner.invoke(app, [_RESOURCE_NAME, "show"])
        assert result.exit_code == 1
        assert "Configuration is empty" in result.stdout

    def test_auth_creates_config_and_hides_token(self, isolated_config_env, cli_runner):
        """Test 'config auth' writes config and hides token when shown."""
        url = "https://test.com"
        token = "abc"

        result = cli_runner.invoke(
            app, [_RESOURCE_NAME, "auth", "--url", url, "--token", token]
        )
        assert result.exit_code == 0
        assert "Credentials updated successfully" in result.stdout

        result = cli_runner.invoke(app, [_RESOURCE_NAME, "show"])
        assert result.exit_code == 0
        assert "*******" in result.stdout
        assert token not in result.stdout

    def test_show_displays_existing_config(self, isolated_config_env, cli_runner):
        """Confirm 'config show' outputs masked credentials from saved config."""
        config = GPPConfig()
        config.set_credentials(url="http://test", token="abc")

        result = cli_runner.invoke(app, [_RESOURCE_NAME, "show"])
        assert result.exit_code == 0
        assert "url" in result.stdout
        assert "*******" in result.stdout
