import pytest

from gpp_client.cli.cli import app


@pytest.mark.remote_data
class TestProgramCommands:
    def test_get_all(self, cli_runner):
        """Test listing all programs."""
        result = cli_runner.invoke(app, ["program", "get-all", "--limit", "3"])
        assert result.exit_code == 0
