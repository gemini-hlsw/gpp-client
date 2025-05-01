import re

import pytest

from gpp_client.cli.cli import app


def extract_first_cfp_id(output: str) -> str | None:
    """Extract the first Call for Proposals ID from a rich table output."""
    for line in output.splitlines():
        match = re.match(r"│\s+(c-[a-z0-9]+)\s+│", line)
        if match:
            return match.group(1)
    return None


@pytest.fixture(scope="module")
def call_for_proposals_id(cli_runner) -> str:
    """Fixture to extract the first available call-for-proposals ID from the CLI."""
    result = cli_runner.invoke(app, ["call-for-proposals", "get-all", "--limit", "5"])
    assert result.exit_code == 0, result.stdout
    cfp_id = extract_first_cfp_id(result.stdout)
    if not cfp_id:
        pytest.skip("No Call for Proposals ID found in CLI output.")
    return cfp_id


@pytest.mark.remote_data
class TestCallForProposals:
    def test_get_all(self, cli_runner):
        """Test listing multiple calls for proposals."""
        result = cli_runner.invoke(app, ["call-for-proposals", "get-all", "--limit", "2"])
        assert result.exit_code == 0
        assert (
            "Calls for Proposals" in result.stdout or "No items found." in result.stdout
        )

    def test_get_all_open_and_closed_exclusive(self, cli_runner):
        """Test that --is-open and --is-closed cannot be used together."""
        result = cli_runner.invoke(
            app, ["call-for-proposals", "get-all", "--is-open", "--is-closed"]
        )
        assert result.exit_code != 0
        assert "Cannot use --is-open and --is-closed together." in result.stdout

    def test_get_by_id(self, call_for_proposals_id, cli_runner):
        """Test retrieving a single call for proposals by ID."""
        result = cli_runner.invoke(
            app, ["call-for-proposals", "get", call_for_proposals_id]
        )
        assert result.exit_code == 0
        assert call_for_proposals_id in result.stdout

    def test_get_by_id_not_found(self, cli_runner):
        """Test retrieving a non-existent call for proposals."""
        result = cli_runner.invoke(app, ["call-for-proposals", "get", "nonexistent"])
        assert result.exit_code != 0
        assert "Error:" in result.stdout
