import pytest

from gpp_client.cli import app


def test_cli_help(cli_runner):
    """
    Test that the CLI displays the help message.
    """
    result = cli_runner.invoke(app, ["--help"])
    assert result.exit_code == 0


def test_cli_invalid_command(cli_runner):
    """
    Test that an invalid command returns an error.
    """
    result = cli_runner.invoke(app, ["invalid_command"])
    assert result.exit_code != 0


def test_cli_version_option(cli_runner):
    """
    Test that the '--version' option displays the correct version and exits.
    """
    result = cli_runner.invoke(app, ["--version"])
    assert result.exit_code == 0


@pytest.mark.remote_data
def test_ping(cli_runner):
    result = cli_runner.invoke(app, ["ping"])
    assert result.exit_code == 0
