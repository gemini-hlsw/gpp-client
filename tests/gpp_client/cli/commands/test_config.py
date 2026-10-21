"""
Tests for the ``gpp config`` commands.
"""

import os
import stat
import tomllib
from types import SimpleNamespace

import pytest
import typer
from typer.testing import CliRunner

from gpp_client.settings import get_config_path as real_get_config_path


@pytest.fixture(autouse=True)
def home(monkeypatch, tmp_path):
    """
    Point HOME at a temp folder and use the real configuration file path.
    """
    for name in ("GPP_ENVIRONMENT", "GPP_TOKEN", "GPP_DEVELOPMENT_TOKEN", "GPP_DEBUG"):
        monkeypatch.delenv(name, raising=False)
    monkeypatch.setenv("HOME", str(tmp_path))
    monkeypatch.chdir(tmp_path)
    monkeypatch.setattr("gpp_client.settings.get_config_path", real_get_config_path)
    return tmp_path


@pytest.fixture()
def config_file(home):
    return home / ".gpp-client" / "config.toml"


def test_path_prints_the_configuration_file_in_home(
    runner, cli_app, config_file
) -> None:
    result = runner.invoke(cli_app, ["config", "path"])

    assert result.exit_code == 0, result.output
    assert result.output.strip() == str(config_file)


def test_path_stays_on_one_line_in_a_narrow_terminal(cli_app, config_file) -> None:
    result = CliRunner(env={"COLUMNS": "20"}).invoke(cli_app, ["config", "path"])

    assert result.exit_code == 0, result.output
    assert result.output == f"{config_file}\n"


def test_get_config_path_command_is_gone(runner, cli_app) -> None:
    result = runner.invoke(cli_app, ["get-config-path"])

    assert result.exit_code == 2
    assert "No such command" in result.output


def test_init_writes_the_entered_tokens_and_skips_blank_ones(
    runner, cli_app, config_file
) -> None:
    result = runner.invoke(cli_app, ["config", "init"], input="\nprod-secret\n")

    assert result.exit_code == 0, result.output
    assert tomllib.loads(config_file.read_text()) == {"token": "prod-secret"}
    assert "prod-secret" not in result.output


@pytest.mark.skipif(os.name != "posix", reason="file modes are POSIX only")
def test_init_creates_a_file_only_the_owner_can_read(
    runner, cli_app, config_file
) -> None:
    result = runner.invoke(cli_app, ["config", "init"], input="dev-secret\n\n")

    assert result.exit_code == 0, result.output
    assert stat.S_IMODE(config_file.stat().st_mode) == 0o600


def test_init_refuses_an_existing_file_and_names_force(
    runner, cli_app, config_file
) -> None:
    config_file.parent.mkdir()
    config_file.write_text('token = "kept"\n')

    result = runner.invoke(cli_app, ["config", "init"], input="\n\n")

    assert result.exit_code == 1
    assert "--force" in result.stderr
    assert config_file.read_text() == 'token = "kept"\n'


def test_init_force_backs_up_the_existing_file_then_writes(
    runner, cli_app, config_file
) -> None:
    config_file.parent.mkdir()
    config_file.write_text('# mine\ntoken = "old"\n')

    result = runner.invoke(
        cli_app, ["config", "init", "--force"], input="dev-secret\n\n"
    )

    assert result.exit_code == 0, result.output
    backup = config_file.with_name("config.toml.bak")
    assert backup.read_text() == '# mine\ntoken = "old"\n'
    assert tomllib.loads(config_file.read_text()) == {"development_token": "dev-secret"}


def _write_config(config_file, text):
    config_file.parent.mkdir(parents=True, exist_ok=True)
    config_file.write_text(text)


def test_set_environment_keeps_comments_and_other_keys(
    runner, cli_app, config_file
) -> None:
    _write_config(config_file, '# my tokens\ntoken = "prod-secret"  # rotated\n')

    result = runner.invoke(cli_app, ["config", "set", "environment", "Development"])

    assert result.exit_code == 0, result.output
    assert config_file.read_text() == (
        '# my tokens\ntoken = "prod-secret"  # rotated\nenvironment = "development"\n'
    )


def test_set_environment_rejects_an_unknown_name(runner, cli_app, config_file) -> None:
    result = runner.invoke(cli_app, ["config", "set", "environment", "staging"])

    assert result.exit_code == 1
    assert "Valid names: development, production" in result.stderr
    assert not config_file.exists()


def test_set_debug_writes_a_boolean(runner, cli_app, config_file) -> None:
    result = runner.invoke(cli_app, ["config", "set", "debug", "yes"])

    assert result.exit_code == 0, result.output
    assert tomllib.loads(config_file.read_text()) == {"debug": True}


@pytest.mark.parametrize("key", ["environment", "debug"])
def test_set_needs_a_value_for_plain_keys(runner, cli_app, config_file, key) -> None:
    result = runner.invoke(cli_app, ["config", "set", key])

    assert result.exit_code == 1
    assert f"'gpp config set {key}' needs a value" in result.stderr
    assert not config_file.exists()


def test_set_rejects_an_unknown_key_naming_the_valid_ones(
    runner, cli_app, config_file
) -> None:
    result = runner.invoke(cli_app, ["config", "set", "envirnoment", "development"])

    assert result.exit_code == 1
    assert (
        "Unknown key 'envirnoment'. Valid keys: environment, token, "
        "development_token, debug." in result.stderr
    )
    assert not config_file.exists()


def test_set_token_reads_one_line_from_piped_stdin(
    runner, cli_app, config_file
) -> None:
    result = runner.invoke(
        cli_app, ["config", "set", "development_token"], input="dev-secret\nextra\n"
    )

    assert result.exit_code == 0, result.output
    assert tomllib.loads(config_file.read_text()) == {"development_token": "dev-secret"}
    assert "dev-secret" not in result.output


@pytest.mark.parametrize("key", ["token", "development_token"])
def test_set_token_refuses_a_value_argument(runner, cli_app, config_file, key) -> None:
    result = runner.invoke(cli_app, ["config", "set", key, "leaked"], input="x\n")

    assert result.exit_code == 1
    assert "leaked" not in result.output
    assert "leaked" not in result.stderr
    assert "never as an argument" in result.stderr
    assert not config_file.exists()


def test_set_token_asks_at_a_hidden_prompt_on_a_terminal(
    runner, cli_app, config_file, monkeypatch
) -> None:
    monkeypatch.setattr(
        typer, "get_text_stream", lambda _: SimpleNamespace(isatty=lambda: True)
    )

    result = runner.invoke(cli_app, ["config", "set", "token"], input="prod-secret\n")

    assert result.exit_code == 0, result.output
    assert "Production token (GPP_TOKEN):" in result.output
    assert "prod-secret" not in result.output
    assert tomllib.loads(config_file.read_text()) == {"token": "prod-secret"}


def test_set_leaves_a_file_that_is_not_valid_toml(runner, cli_app, config_file) -> None:
    _write_config(config_file, "token = \n")

    result = runner.invoke(cli_app, ["config", "set", "debug", "true"])

    assert result.exit_code == 1
    assert "not valid TOML" in result.stderr
    assert config_file.read_text() == "token = \n"


def test_unset_removes_the_key_and_keeps_the_rest(runner, cli_app, config_file) -> None:
    _write_config(
        config_file, '# mine\nenvironment = "development"\ntoken = "p"  # rotated\n'
    )

    result = runner.invoke(cli_app, ["config", "unset", "environment"])

    assert result.exit_code == 0, result.output
    assert config_file.read_text() == '# mine\ntoken = "p"  # rotated\n'


def test_unset_without_a_file_creates_nothing(runner, cli_app, config_file) -> None:
    result = runner.invoke(cli_app, ["config", "unset", "token"])

    assert result.exit_code == 0, result.output
    assert "token is not set" in result.output
    assert not config_file.exists()


def test_delete_removes_the_file_after_confirming(runner, cli_app, config_file) -> None:
    _write_config(config_file, 'token = "p"\n')

    result = runner.invoke(cli_app, ["config", "delete"], input="y\n")

    assert result.exit_code == 0, result.output
    assert not config_file.exists()


def test_delete_yes_skips_the_prompt(runner, cli_app, config_file) -> None:
    _write_config(config_file, 'token = "p"\n')

    result = runner.invoke(cli_app, ["config", "delete", "--yes"])

    assert result.exit_code == 0, result.output
    assert "[y/N]" not in result.output
    assert not config_file.exists()


def test_delete_keeps_the_file_when_declined(runner, cli_app, config_file) -> None:
    _write_config(config_file, 'token = "p"\n')

    result = runner.invoke(cli_app, ["config", "delete"], input="n\n")

    assert result.exit_code == 0, result.output
    assert config_file.exists()


def test_delete_without_a_file_says_there_is_none(runner, cli_app) -> None:
    result = runner.invoke(cli_app, ["config", "delete", "--yes"])

    assert result.exit_code == 0, result.output
    assert "There is no configuration file at" in result.output


def _show_row(output: str, key: str) -> str:
    """
    Return the ``show`` line for one key, with runs of spaces collapsed.
    """
    for line in output.splitlines():
        words = line.split()
        if words and words[0] == key:
            return " ".join(words)
    raise AssertionError(f"no {key} row in:\n{output}")


def test_show_names_a_variable_as_the_source(runner, cli_app, monkeypatch) -> None:
    monkeypatch.setenv("GPP_ENVIRONMENT", "development")

    result = runner.invoke(cli_app, ["config", "show"])

    assert result.exit_code == 0, result.output
    assert _show_row(result.output, "environment") == (
        "environment development variable GPP_ENVIRONMENT"
    )


@pytest.mark.parametrize(
    ("setup", "options", "expected"),
    [
        (lambda home, config_file: None, [], "environment production default"),
        (
            lambda home, config_file: _write_config(
                config_file, 'environment = "development"\n'
            ),
            [],
            "environment development configuration file",
        ),
        (
            lambda home, config_file: (home / ".env").write_text(
                "GPP_ENVIRONMENT=development\n"
            ),
            [],
            "environment development .env file",
        ),
        (
            lambda home, config_file: _write_config(
                config_file, 'environment = "production"\n'
            ),
            ["--env", "development"],
            "environment development --env",
        ),
        (
            lambda home, config_file: _write_config(config_file, 'environment = " "\n'),
            [],
            "environment production default",
        ),
    ],
    ids=["default", "file", "dotenv", "env-option", "blank-in-file"],
)
def test_show_names_each_source(
    runner, cli_app, home, config_file, setup, options, expected
) -> None:
    setup(home, config_file)

    result = runner.invoke(cli_app, [*options, "config", "show"])

    assert result.exit_code == 0, result.output
    assert _show_row(result.output, "environment") == expected


def test_show_masks_tokens_to_their_last_four_characters(
    runner, cli_app, config_file, monkeypatch
) -> None:
    monkeypatch.setenv("GPP_TOKEN", "prod-secret-1234")
    _write_config(config_file, 'development_token = "dev-secret-5678"\n')

    result = runner.invoke(cli_app, ["config", "show"])

    assert result.exit_code == 0, result.output
    assert _show_row(result.output, "token") == "token ****1234 variable GPP_TOKEN"
    assert _show_row(result.output, "development_token") == (
        "development_token ****5678 configuration file"
    )
    assert "secret" not in result.output


def test_show_reports_an_invalid_value(runner, cli_app, monkeypatch) -> None:
    monkeypatch.setenv("GPP_DEBUG", "maybe")

    result = runner.invoke(cli_app, ["config", "show"])

    assert result.exit_code == 1
    assert "debug" in result.stderr


def test_show_reports_an_unknown_key_in_the_file(runner, cli_app, config_file) -> None:
    _write_config(config_file, 'tokn = "x"\n')

    result = runner.invoke(cli_app, ["config", "show"])

    assert result.exit_code == 1
    assert "unknown keys tokn" in result.stderr


@pytest.mark.parametrize(
    "args",
    [
        ["config", "set", "environment", "development"],
        ["config", "unset", "debug"],
        ["config", "delete", "--yes"],
        ["config", "init"],
    ],
)
def test_messages_keep_a_long_path_on_one_line(
    monkeypatch, tmp_path, cli_app, args
) -> None:
    home = tmp_path / ("a-long-folder-name-" * 6)
    monkeypatch.setenv("HOME", str(home))
    config_file = home / ".gpp-client" / "config.toml"
    _write_config(config_file, 'environment = "production"\n')

    result = CliRunner(env={"COLUMNS": "20"}).invoke(cli_app, args, input="\n\n")

    output = result.stdout + result.stderr
    assert any(str(config_file) in line for line in output.splitlines()), output
