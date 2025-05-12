import pytest

from gpp_client.cli.cli import app

_RESOURCE_NAME = "program"
_RESOURCE_PREFIX = "p"
_TABLE_TITLE = "Programs"


@pytest.fixture
def resource_id(cli_runner, helpers) -> str:
    """Fixture to extract the first resource ID from the CLI."""
    result = cli_runner.invoke(app, [_RESOURCE_NAME, "list", "--limit", "1"])
    assert result.exit_code == 0, result.stdout
    resource_id = helpers.extract_first_resource_id(result.stdout, _RESOURCE_PREFIX)
    if not resource_id:
        pytest.skip(f"No {_RESOURCE_NAME} ID found in CLI output.")
    return resource_id


@pytest.mark.remote_data
class TestObservation:
    def test_get_all(self, cli_runner):
        """Test listing multiple items."""
        result = cli_runner.invoke(app, [_RESOURCE_NAME, "list", "--limit", "2"])
        assert result.exit_code == 0
        assert _TABLE_TITLE in result.stdout or "No items found." in result.stdout

    def test_get_by_id(self, resource_id, cli_runner):
        """Test retrieving a single item by ID."""
        result = cli_runner.invoke(app, [_RESOURCE_NAME, "get", resource_id])
        assert result.exit_code == 0
        assert resource_id in result.stdout

    def test_get_by_id_not_found(self, cli_runner):
        """Test retrieving a non-existent item."""
        result = cli_runner.invoke(app, [_RESOURCE_NAME, "get", "nonexistent"])
        assert result.exit_code != 0
        assert "Error:" in result.stdout
