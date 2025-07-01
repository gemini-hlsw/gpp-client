import pytest
import typer
from rich.console import Console

from gpp_client.cli.utils import (
    async_command,
    print_not_found,
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
