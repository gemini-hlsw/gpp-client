"""
Tests for choosing the GPP environment when a ``GPPClient`` is built.
"""

import logging

import httpx
import pytest

from gpp_client import GPPClient
from gpp_client.constants import DEVELOPMENT_URL, PRODUCTION_URL
from gpp_client.environment import GPPEnvironment
from gpp_client.exceptions import GPPAuthError, GPPClientError


@pytest.fixture(autouse=True)
def _no_user_configuration(monkeypatch, tmp_path):
    for name in (
        "GPP_ENVIRONMENT",
        "GPP_TOKEN",
        "GPP_DEVELOPMENT_TOKEN",
    ):
        monkeypatch.delenv(name, raising=False)
    config_path = tmp_path / "config.toml"
    monkeypatch.setattr("gpp_client.settings.get_config_path", lambda: config_path)
    return config_path


async def _send_ping(gpp_transport, **client_kwargs) -> httpx.Request:
    """
    Build a client, send one generated query, and return the request sent.
    """
    gpp_transport.respond({"observation": None})
    async with httpx.AsyncClient(transport=gpp_transport) as http_client:
        async with GPPClient(http_client=http_client, **client_kwargs) as client:
            await client.workflow_state.get_by_id(observation_id="o-1")
    return gpp_transport.requests[-1]


@pytest.mark.asyncio
async def test_environment_argument_chooses_the_server(gpp_transport) -> None:
    request = await _send_ping(
        gpp_transport, environment="development", token="dev-token"
    )

    assert str(request.url) == f"{DEVELOPMENT_URL}/odb"
    assert request.headers["Authorization"] == "Bearer dev-token"


@pytest.mark.asyncio
async def test_production_is_the_default(gpp_transport, monkeypatch) -> None:
    monkeypatch.setenv("GPP_TOKEN", "prod-token")

    request = await _send_ping(gpp_transport)

    assert str(request.url) == f"{PRODUCTION_URL}/odb"
    assert request.headers["Authorization"] == "Bearer prod-token"


@pytest.mark.asyncio
async def test_variable_chooses_the_environment(gpp_transport, monkeypatch) -> None:
    monkeypatch.setenv("GPP_ENVIRONMENT", "development")
    monkeypatch.setenv("GPP_DEVELOPMENT_TOKEN", "dev-token")

    request = await _send_ping(gpp_transport)

    assert str(request.url) == f"{DEVELOPMENT_URL}/odb"
    assert request.headers["Authorization"] == "Bearer dev-token"


@pytest.mark.asyncio
async def test_argument_beats_the_variable(gpp_transport, monkeypatch) -> None:
    monkeypatch.setenv("GPP_ENVIRONMENT", "development")

    request = await _send_ping(
        gpp_transport, environment="production", token="prod-token"
    )

    assert str(request.url) == f"{PRODUCTION_URL}/odb"


@pytest.mark.asyncio
async def test_config_file_default_is_for_the_command_line_only(
    gpp_transport, _no_user_configuration
) -> None:
    _no_user_configuration.write_text('environment = "development"\n')

    request = await _send_ping(gpp_transport, token="prod-token")

    assert str(request.url) == f"{PRODUCTION_URL}/odb"


@pytest.mark.asyncio
async def test_empty_values_fall_through(gpp_transport, monkeypatch) -> None:
    monkeypatch.setenv("GPP_ENVIRONMENT", "")

    request = await _send_ping(gpp_transport, environment="", token="prod-token")

    assert str(request.url) == f"{PRODUCTION_URL}/odb"


@pytest.mark.parametrize("source", ["argument", "variable"])
def test_unknown_environment_fails_listing_valid_names(monkeypatch, source) -> None:
    kwargs = {}
    if source == "argument":
        kwargs["environment"] = "prodution"
    else:
        monkeypatch.setenv("GPP_ENVIRONMENT", "prodution")

    with pytest.raises(GPPClientError) as error:
        GPPClient(token="t", **kwargs)

    assert str(error.value) == (
        "Unknown GPP environment 'prodution'. Valid names: development, production."
    )


@pytest.mark.parametrize("name", ["Development", "DEVELOPMENT", " development "])
def test_environment_names_ignore_case_and_spaces(name) -> None:
    client = GPPClient(environment=name, token="t")

    assert client.settings.environment is GPPEnvironment.DEVELOPMENT


def test_staging_is_an_unknown_environment(monkeypatch) -> None:
    monkeypatch.setenv("GPP_STAGING_TOKEN", "staging-token")

    with pytest.raises(GPPClientError) as error:
        GPPClient(environment="staging")

    assert str(error.value) == (
        "Unknown GPP environment 'staging'. Valid names: development, production."
    )


@pytest.mark.asyncio
async def test_token_argument_applies_to_the_selected_environment(
    gpp_transport, monkeypatch
) -> None:
    monkeypatch.setenv("GPP_ENVIRONMENT", "development")
    monkeypatch.setenv("GPP_DEVELOPMENT_TOKEN", "from-variable")
    monkeypatch.setenv("GPP_TOKEN", "prod-token")

    request = await _send_ping(gpp_transport, token="from-argument")

    assert request.headers["Authorization"] == "Bearer from-argument"


@pytest.mark.asyncio
async def test_production_token_never_reaches_development(monkeypatch) -> None:
    monkeypatch.setenv("GPP_TOKEN", "prod-token")

    with pytest.raises(GPPAuthError) as error:
        GPPClient(environment="development")

    assert "Set 'GPP_DEVELOPMENT_TOKEN'" in str(error.value)


@pytest.mark.parametrize(
    ("environment", "variable"),
    [
        ("production", "GPP_TOKEN"),
        ("development", "GPP_DEVELOPMENT_TOKEN"),
    ],
)
def test_missing_token_names_the_variable_to_set(environment, variable) -> None:
    with pytest.raises(GPPAuthError) as error:
        GPPClient(environment=environment)

    assert str(error.value) == (
        f"A token is required for the {environment} environment. Set '{variable}'."
    )


def test_one_log_line_names_the_environment_and_url(caplog) -> None:
    with caplog.at_level(logging.INFO, logger="gpp_client"):
        GPPClient(environment="development", token="t")

    lines = [r.getMessage() for r in caplog.records if r.levelno >= logging.INFO]
    assert lines == [
        f"GPPClient using the development environment at {DEVELOPMENT_URL}/odb"
    ]
