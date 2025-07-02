import pytest

from gpp_client.cli.cli import app

_RESOURCE_NAME = "sched"


@pytest.mark.remote_data
class TestScheduler:
    def test_program_get_all(self, cli_runner):
        """Test listing multiple items."""
        result = cli_runner.invoke(app, [_RESOURCE_NAME, "program", "list"])
        print(result.stdout)
        assert result.exit_code == 0
