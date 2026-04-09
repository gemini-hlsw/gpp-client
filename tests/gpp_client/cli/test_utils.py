import pytest
import typer
from rich.console import Console

from gpp_client.cli.utils import (
    async_command,
    print_not_found,
    require_exactly_one,
    truncate_long,
    truncate_short,
    truncate_string,
)

console = Console()


class TestTruncateString:
    def test_none_value(self):
        assert truncate_string(None, 10) == "<None>"

    def test_empty_string(self):
        assert truncate_string("", 10) == "<None>"

    def test_short_string(self):
        assert truncate_string("short", 10) == "short"

    def test_exact_limit(self):
        assert truncate_string("123456", 6) == "123456"

    def test_truncated_string(self):
        assert truncate_string("1234567890", 6) == "123..."

    def test_short_vs_long(self):
        short = "this is short"
        long = "this is a much longer paragraph that will be truncated"

        assert truncate_short(short) == short
        assert truncate_short(long) == "this is a much lo..."

        assert truncate_long(short) == short
        assert (
            truncate_long(long) == "this is a much longer paragraph that will be tr..."
        )


class TestPrintNotFound:
    def test_prints_yellow_message(self, capsys):
        print_not_found()
        captured = capsys.readouterr()
        assert "No items found." in captured.out


class TestAsyncCommand:
    def test_successful_execution(self):
        @async_command
        async def dummy():
            return "ok"

        result = dummy()
        assert result == "ok"

    def test_exception_triggers_exit(self, capsys):
        @async_command
        async def broken():
            raise ValueError

        with pytest.raises(typer.Exit):
            broken()

        _ = capsys.readouterr()


@pytest.mark.parametrize(
    ("selectors", "expected"),
    [
        (
            {"observation_id": "obs-123"},
            ("observation_id", "obs-123"),
        ),
        (
            {"observation_id": "  obs-123  "},
            ("observation_id", "obs-123"),
        ),
        (
            {"program_id": "prog-001", "observation_id": None},
            ("program_id", "prog-001"),
        ),
        (
            {"program_id": None, "observation_id": "obs-123"},
            ("observation_id", "obs-123"),
        ),
        (
            {"program_id": "", "observation_id": "obs-123"},
            ("observation_id", "obs-123"),
        ),
        (
            {"program_id": "   ", "observation_id": "obs-123"},
            ("observation_id", "obs-123"),
        ),
        (
            {"program_id": "\t", "observation_id": "  obs-123  "},
            ("observation_id", "obs-123"),
        ),
        (
            {
                "program_id": None,
                "observation_id": None,
                "observation_reference": " GS-2025A-Q-1-1 ",
            },
            ("observation_reference", "GS-2025A-Q-1-1"),
        ),
    ],
)
def test_require_exactly_one_returns_selected_pair(
    selectors: dict[str, str | None],
    expected: tuple[str, str],
) -> None:
    """
    Return the single provided selector after trimming whitespace.
    """
    result = require_exactly_one(**selectors)

    assert result == expected


@pytest.mark.parametrize(
    "selectors",
    [
        {"observation_id": None},
        {"observation_id": ""},
        {"observation_id": "   "},
        {"observation_id": None, "program_id": None},
        {"observation_id": "", "program_id": "   "},
        {
            "observation_id": None,
            "program_id": "",
            "observation_reference": "   ",
        },
    ],
)
def test_require_exactly_one_raises_when_none_provided(
    selectors: dict[str, str | None],
) -> None:
    """
    Raise when no selector is effectively provided.

    Parameters
    ----------
    selectors : dict[str, str | None]
        Selector inputs.
    """
    with pytest.raises(typer.BadParameter) as exc_info:
        require_exactly_one(**selectors)

    message = str(exc_info.value)
    assert "Exactly one selector is required." in message


def test_require_exactly_one_none_provided_lists_valid_options() -> None:
    """
    Error message should include normalized CLI option names.
    """
    with pytest.raises(typer.BadParameter) as exc_info:
        require_exactly_one(
            observation_id=None,
            program_id="",
            observation_reference="   ",
        )

    message = str(exc_info.value)
    assert "--observation-id" in message
    assert "--program-id" in message
    assert "--observation-reference" in message


@pytest.mark.parametrize(
    ("selectors", "expected_flags"),
    [
        (
            {
                "observation_id": "obs-123",
                "program_id": "prog-001",
            },
            ["--observation-id", "--program-id"],
        ),
        (
            {
                "observation_id": " obs-123 ",
                "program_id": "   ",
                "observation_reference": " GS-2025A-Q-1-1 ",
            },
            ["--observation-id", "--observation-reference"],
        ),
        (
            {
                "observation_id": "\tobs-123\t",
                "program_id": "\nprog-001\n",
                "target_id": None,
            },
            ["--observation-id", "--program-id"],
        ),
    ],
)
def test_require_exactly_one_raises_when_multiple_provided(
    selectors: dict[str, str | None],
    expected_flags: list[str],
) -> None:
    """
    Raise when more than one selector is effectively provided.
    """
    with pytest.raises(typer.BadParameter) as exc_info:
        require_exactly_one(**selectors)

    message = str(exc_info.value)
    assert "Selectors are mutually exclusive." in message
    for flag in expected_flags:
        assert flag in message
