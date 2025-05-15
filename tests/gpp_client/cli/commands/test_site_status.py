import pytest

from gpp_client.cli.cli import app

_RESOURCE_NAME = "site"


@pytest.mark.remote_data
class TestSiteStatus:
    def test_get_by_id_south(self, cli_runner):
        """Test getting Gemini South status."""
        result = cli_runner.invoke(app, [_RESOURCE_NAME, "get", "souTh"])
        assert result.exit_code == 0

    def test_get_by_id_north(self, cli_runner):
        """Test getting Gemini North status."""
        result = cli_runner.invoke(app, [_RESOURCE_NAME, "get", "nOrth"])
        assert result.exit_code == 0

    def test_get_by_id_not_found(self, cli_runner):
        """Test retrieving a non-existent site."""
        result = cli_runner.invoke(app, [_RESOURCE_NAME, "get", "nonexistent"])
        assert result.exit_code != 0
        assert "Usage:" in result.stdout
