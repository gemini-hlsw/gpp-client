import pytest
from pathlib import Path
from gpp_client.config import GPPConfig


class TestGPPConfig:
    """Tests for GPPConfig class."""

    @pytest.fixture
    def mock_app_dir(self, mocker, tmp_path) -> Path:
        """Mock typer.get_app_dir to return a temporary path."""
        app_dir = tmp_path / "gpp-config-test"
        mocker.patch("typer.get_app_dir", return_value=app_dir)
        return app_dir

    @pytest.fixture
    def config(self, mock_app_dir) -> GPPConfig:
        """Provide a GPPConfig instance."""
        return GPPConfig()

    def test_path_property(self, config: GPPConfig, mock_app_dir: Path) -> None:
        """Test that path is correctly set."""
        assert config.path == mock_app_dir / "config.toml"

    def test_exists_false_when_no_file(self, config: GPPConfig) -> None:
        """Test that exists() returns False when no file."""
        assert not config.exists()

    def test_save_and_load_data(self, config: GPPConfig) -> None:
        """Test saving and loading configuration data."""
        # Set and save credentials.
        config.set_credentials(url="test-url", token="test-token")
        assert config.exists()

        assert config.get_credentials() == ("test-url", "test-token")

    def test_get_credentials_when_empty(self, config: GPPConfig) -> None:
        """Test get_credentials() returns (None, None) when empty."""
        url, token = config.get_credentials()
        assert url is None
        assert token is None

    def test_set_credentials_and_credentials_set(self, config: GPPConfig) -> None:
        """Test set_credentials() and credentials_set()."""
        assert not config.credentials_set()

        config.set_credentials(url="test-url", token="test-token")

        assert config.credentials_set()
        url, token = config.get_credentials()
        assert url == "test-url"
        assert token == "test-token"

    def test_get_returns_full_data(self, config: GPPConfig) -> None:
        """Test get() returns full dictionary."""
        config.set_credentials(url="test-url", token="test-token")
        data = config.get()
        assert "credentials" in data
        assert data["credentials"]["url"] == "test-url"
        assert data["credentials"]["token"] == "test-token"
