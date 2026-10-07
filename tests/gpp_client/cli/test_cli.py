"""
Tests for the CLI entry point and core commands.
"""

from types import SimpleNamespace

import pytest

from gpp_client.cli.cli import CLIState, main_callback
from tests.gpp_client.cli.conftest import DummyAsyncClient


def test_cli_help(runner, cli_app):
    """
    Test that the CLI displays the help message.
    """
    result = runner.invoke(cli_app, ["--help"])
    assert result.exit_code == 0


def test_cli_invalid_command(runner, cli_app):
    """
    Test that an invalid command returns an error.
    """
    result = runner.invoke(cli_app, ["invalid_command"])
    assert result.exit_code != 0


def test_version_option_prints_and_exits(runner, cli_app) -> None:
    """
    Ensure --version prints version and exits.
    """
    result = runner.invoke(cli_app, ["--version"])

    assert result.exit_code == 0


def test_main_callback_sets_debug_flag() -> None:
    """
    Ensure debug flag is stored in context.
    """
    ctx = SimpleNamespace(obj=None)

    main_callback(ctx=ctx, version=False, debug=True)

    assert isinstance(ctx.obj, CLIState)
    assert ctx.obj.debug is True


def test_ping_success(runner, cli_app, mocker) -> None:
    """
    Ping should succeed and print success message.
    """

    async def mock_ping():
        return True, None

    mock_client = DummyAsyncClient(ping=mock_ping)

    mocker.patch("gpp_client.cli.utils.GPPClient", return_value=mock_client)

    result = runner.invoke(cli_app, ["ping"])

    assert result.exit_code == 0
    assert "GPP is reachable" in result.output


def test_ping_failure(runner, cli_app, mocker) -> None:
    """
    Ping should fail and exit with code 1.
    """

    async def mock_ping():
        return False, "bad token"

    mock_client = DummyAsyncClient(ping=mock_ping)

    mocker.patch("gpp_client.cli.utils.GPPClient", return_value=mock_client)

    result = runner.invoke(cli_app, ["ping"])

    assert result.exit_code == 1
    assert "Failed to reach GPP: bad token" in result.output


def test_ping_calls_client_once(runner, cli_app, mocker) -> None:
    """
    Ensure ping invokes client.ping exactly once.
    """

    async def mock_ping():
        return True, None

    mock_client = DummyAsyncClient(ping=mocker.AsyncMock(side_effect=mock_ping))

    mocker.patch("gpp_client.cli.utils.GPPClient", return_value=mock_client)

    runner.invoke(cli_app, ["ping"])

    mock_client.ping.assert_called_once()


@pytest.mark.parametrize("reachable", [True, False])
def test_ping_closes_its_client(runner, cli_app, mocker, reachable) -> None:
    closed = []

    class Client(DummyAsyncClient):
        async def ping(self):
            return reachable, None if reachable else "bad token"

        async def __aexit__(self, exc_type, exc, tb) -> None:
            closed.append(True)

    mocker.patch("gpp_client.cli.utils.GPPClient", return_value=Client())

    runner.invoke(cli_app, ["ping"])

    assert closed == [True]


def test_registered_commands_exist(runner, cli_app) -> None:
    """
    Ensure core commands and groups are exposed in CLI help.
    """
    result = runner.invoke(cli_app, ["--help"])

    assert result.exit_code == 0
    assert "ping" in result.output
    assert "observation" in result.output
    assert "program" in result.output
    assert "attachment" in result.output
    assert "target" in result.output
    assert "workflow-state" in result.output
    assert "site-status" in result.output
    assert "goats" in result.output
    assert "scheduler" in result.output


def test_no_args_does_error(runner, cli_app) -> None:
    """
    CLI should error when run without args.
    """
    result = runner.invoke(cli_app, [])

    assert result.exit_code != 0
