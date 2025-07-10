import pytest

from gpp_client.cli.cli import app

_RESOURCE_NAME = "goats"


@pytest.mark.remote_data
class TestGOATS:
    def test_observation_get_all(self, cli_runner):
        """Test listing multiple items."""
        result = cli_runner.invoke(app, [_RESOURCE_NAME, "obs", "list", "-p", "p-42"])
        assert result.exit_code == 0
