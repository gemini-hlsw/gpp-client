import datetime
import re

import pytest

from gpp_client.cli.cli import app


def extract_first_note_id(output: str) -> str | None:
    """Extract the first program note ID from a rich table output."""
    for line in output.splitlines():
        match = re.match(r"│\s+(n-[a-z0-9]+)\s+│", line)
        if match:
            return match.group(1)
    return None


@pytest.fixture(scope="module")
def program_note_id(cli_runner) -> str:
    """Retrieve the first available program note ID for use in tests."""
    result = cli_runner.invoke(app, ["program-note", "get-all", "--limit", "5"])
    assert result.exit_code == 0

    note_id = extract_first_note_id(result.stdout)
    if not note_id:
        pytest.skip("No program note ID found in CLI output.")
    return note_id


@pytest.mark.remote_data
class TestProgramNote:
    def test_get_all(self, cli_runner):
        """Test getting all program notes."""
        result = cli_runner.invoke(app, ["program-note", "get-all", "--limit", "2"])
        assert result.exit_code == 0
        assert "Program Notes" in result.stdout or "No items found." in result.stdout

    def test_get_by_id_not_found(self, cli_runner):
        """Test getting a note with a wrong ID."""
        result = cli_runner.invoke(app, ["program-note", "get", "nonexistent"])
        assert result.exit_code != 0
        assert "Error:" in result.stdout

    def test_create_missing_identifier(self, cli_runner):
        """Test creating a note missing an identifier."""
        result = cli_runner.invoke(
            app,
            [
                "program-note",
                "create",
                "--title",
                "Test Note",
                "--text",
                "This is a test note",
            ],
        )
        assert result.exit_code != 0

    def test_update_no_fields(self, cli_runner):
        """Test updating a note with no fields to change."""
        result = cli_runner.invoke(app, ["program-note", "update", "n-dummy"])
        assert result.exit_code != 0
        assert (
            "At least one field must be provided to update." in result.stdout
            or "Error" in result.stdout
        )

    def test_get_by_id(self, cli_runner, program_note_id):
        """Test fetching a single program note by ID."""
        result = cli_runner.invoke(app, ["program-note", "get", program_note_id])
        assert result.exit_code == 0
        assert program_note_id in result.stdout

    def test_update_note(self, cli_runner, program_note_id):
        """Test updating an existing note's text field."""
        timestamp = datetime.datetime.utcnow().isoformat()
        result = cli_runner.invoke(
            app,
            [
                "program-note",
                "update",
                program_note_id,
                "--text",
                f"Updated at {timestamp}",
            ],
        )
        assert result.exit_code == 0
        assert "Updated at" in result.stdout
        assert timestamp in result.stdout
