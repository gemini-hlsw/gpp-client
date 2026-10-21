"""
Tests for choosing the GPP environment from the CLI.
"""

import warnings
from functools import partial

import httpx
import pytest

from gpp_client.constants import DEVELOPMENT_URL, PRODUCTION_URL


@pytest.fixture(autouse=True)
def config_path(monkeypatch, tmp_path):
    for name in (
        "GPP_ENVIRONMENT",
        "GPP_TOKEN",
        "GPP_DEVELOPMENT_TOKEN",
    ):
        monkeypatch.delenv(name, raising=False)
    monkeypatch.setenv("GPP_TOKEN", "prod-token")
    monkeypatch.setenv("GPP_DEVELOPMENT_TOKEN", "dev-token")
    path = tmp_path / "gpp-client" / "config.toml"
    monkeypatch.setattr("gpp_client.settings.get_config_path", lambda: path)
    return path


@pytest.fixture()
def gpp_network(monkeypatch, gpp_transport):
    """
    Send every HTTP request the CLI makes to ``gpp_transport``.
    """
    monkeypatch.setattr(
        httpx,
        "AsyncClient",
        partial(httpx.AsyncClient, transport=gpp_transport),
    )
    return gpp_transport


def _read_workflow_state(runner, cli_app, *global_options):
    return runner.invoke(
        cli_app,
        [*global_options, "workflow-state", "get", "--observation-id", "o-1"],
    )


def test_env_option_sends_to_that_environment(runner, cli_app, gpp_network) -> None:
    gpp_network.respond({"observation": None})

    result = _read_workflow_state(runner, cli_app, "--env", "development")

    assert result.exit_code == 0, result.output
    assert str(gpp_network.requests[-1].url) == f"{DEVELOPMENT_URL}/odb"
    assert gpp_network.requests[-1].headers["Authorization"] == "Bearer dev-token"


def test_env_option_beats_variable_and_config(
    runner, cli_app, gpp_network, config_path, monkeypatch
) -> None:
    monkeypatch.setenv("GPP_ENVIRONMENT", "development")
    config_path.parent.mkdir(parents=True)
    config_path.write_text('environment = "development"\n')
    gpp_network.respond({"observation": None})

    result = _read_workflow_state(runner, cli_app, "--env", "production")

    assert result.exit_code == 0, result.output
    assert str(gpp_network.requests[-1].url) == f"{PRODUCTION_URL}/odb"


def test_command_shows_its_environment_on_stderr(runner, cli_app, gpp_network) -> None:
    gpp_network.respond({"observation": None})

    result = _read_workflow_state(runner, cli_app, "--env", "development")

    assert result.exit_code == 0, result.output
    assert f"Environment: development ({DEVELOPMENT_URL})" in result.stderr
    assert "Environment:" not in result.stdout


def test_command_shows_default_environment(runner, cli_app, gpp_network) -> None:
    gpp_network.respond({"observation": None})

    result = _read_workflow_state(runner, cli_app)

    assert result.exit_code == 0, result.output
    assert f"Environment: production ({PRODUCTION_URL})" in result.stderr


def test_command_without_environment_warns_in_command_line_terms(
    runner, cli_app, gpp_network
) -> None:
    gpp_network.respond({"observation": None})

    with warnings.catch_warnings():
        warnings.simplefilter("error")
        result = _read_workflow_state(runner, cli_app)

    assert result.exit_code == 0, result.output
    assert (
        "No GPP environment set, so using production. Pass --env, or set "
        "GPP_ENVIRONMENT or environment in the configuration file; a future "
        "release will fail instead."
    ) in result.stderr


def test_command_with_environment_does_not_warn(runner, cli_app, gpp_network) -> None:
    gpp_network.respond({"observation": None})

    result = _read_workflow_state(runner, cli_app, "--env", "production")

    assert result.exit_code == 0, result.output
    assert "No GPP environment set" not in result.stderr


def test_ping_uses_env_option(runner, cli_app, gpp_network) -> None:
    gpp_network.respond({"programs": {"matches": []}})

    result = runner.invoke(cli_app, ["--env", "development", "ping"])

    assert result.exit_code == 0, result.output
    assert str(gpp_network.requests[-1].url) == f"{DEVELOPMENT_URL}/odb"


def test_env_help_offers_development_and_production_only(runner, cli_app) -> None:
    result = runner.invoke(cli_app, ["--help"], env={"COLUMNS": "200"})

    assert result.exit_code == 0
    assert "development" in result.output
    assert "production" in result.output
    assert "staging" not in result.output.lower()


def test_env_option_rejects_staging(runner, cli_app, gpp_network) -> None:
    result = _read_workflow_state(runner, cli_app, "--env", "staging")

    assert result.exit_code == 2
    assert "staging" in result.output
    assert gpp_network.requests == []


def test_config_file_environment_is_used_by_commands(
    runner, cli_app, gpp_network, config_path
) -> None:
    config_path.parent.mkdir(parents=True)
    config_path.write_text('environment = "development"\n')
    gpp_network.respond({"observation": None})

    result = _read_workflow_state(runner, cli_app)

    assert result.exit_code == 0, result.output
    assert str(gpp_network.requests[-1].url) == f"{DEVELOPMENT_URL}/odb"


def test_variable_beats_the_config_file(
    runner, cli_app, gpp_network, config_path, monkeypatch
) -> None:
    config_path.parent.mkdir(parents=True)
    config_path.write_text('environment = "development"\n')
    monkeypatch.setenv("GPP_ENVIRONMENT", "production")
    gpp_network.respond({"observation": None})

    result = _read_workflow_state(runner, cli_app)

    assert result.exit_code == 0, result.output
    assert str(gpp_network.requests[-1].url) == f"{PRODUCTION_URL}/odb"


def test_empty_config_value_means_production(
    runner, cli_app, gpp_network, config_path
) -> None:
    config_path.parent.mkdir(parents=True)
    config_path.write_text('environment = ""\n')
    gpp_network.respond({"observation": None})

    result = _read_workflow_state(runner, cli_app)

    assert result.exit_code == 0, result.output
    assert str(gpp_network.requests[-1].url) == f"{PRODUCTION_URL}/odb"


def test_unknown_environment_in_config_fails_listing_valid_names(
    runner, cli_app, gpp_network, config_path
) -> None:
    config_path.parent.mkdir(parents=True)
    config_path.write_text('environment = "prodution"\n')

    result = _read_workflow_state(runner, cli_app)

    assert result.exit_code == 1
    assert (
        "Unknown GPP environment 'prodution'. Valid names: development, production."
        in result.output
    )
    assert gpp_network.requests == []


def test_env_option_ignores_case(runner, cli_app, gpp_network) -> None:
    gpp_network.respond({"observation": None})

    result = _read_workflow_state(runner, cli_app, "--env", "Development")

    assert result.exit_code == 0, result.output
    assert str(gpp_network.requests[-1].url) == f"{DEVELOPMENT_URL}/odb"
