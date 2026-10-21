"""
Tests for choosing the GPP environment when a ``GPPClient`` is built.
"""

import logging
import warnings

import httpx
import pytest

from gpp_client import GPPClient
from gpp_client.constants import DEVELOPMENT_URL, PRODUCTION_URL
from gpp_client.environment import GPPEnvironment
from gpp_client.exceptions import GPPAuthError, GPPClientError
from tests.gpp_client.environment_sources import write_environment


pytestmark = pytest.mark.usefixtures("_no_user_configuration")


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
async def test_no_environment_warns_and_uses_production(
    gpp_transport, monkeypatch
) -> None:
    monkeypatch.setenv("GPP_TOKEN", "prod-token")

    with pytest.warns(FutureWarning) as warned:
        request = await _send_ping(gpp_transport)

    assert str(request.url) == f"{PRODUCTION_URL}/odb"
    assert request.headers["Authorization"] == "Bearer prod-token"
    assert [str(w.message) for w in warned] == [
        "No GPP environment set, so using production. Pass environment= or set "
        "GPP_ENVIRONMENT; a future release will raise an error instead."
    ]
    assert warned[0].filename == __file__


@pytest.mark.parametrize("source", ["argument", "variable", "dotenv"])
def test_environment_set_anywhere_does_not_warn(monkeypatch, tmp_path, source) -> None:
    monkeypatch.chdir(tmp_path)
    kwargs = {}
    if source == "argument":
        kwargs["environment"] = "production"
    elif source == "variable":
        monkeypatch.setenv("GPP_ENVIRONMENT", "production")
    else:
        (tmp_path / ".env").write_text("GPP_ENVIRONMENT=production\n")

    with warnings.catch_warnings():
        warnings.simplefilter("error")
        client = GPPClient(token="t", **kwargs)

    assert client.settings.environment is GPPEnvironment.PRODUCTION


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
async def test_config_file_chooses_the_environment(
    gpp_transport, _no_user_configuration
) -> None:
    _no_user_configuration.write_text(
        'environment = "development"\ndevelopment_token = "dev-token"\n'
    )

    with warnings.catch_warnings():
        warnings.simplefilter("error")
        request = await _send_ping(gpp_transport)

    assert str(request.url) == f"{DEVELOPMENT_URL}/odb"
    assert request.headers["Authorization"] == "Bearer dev-token"


@pytest.mark.asyncio
@pytest.mark.parametrize(
    ("environment", "key"),
    [("production", "token"), ("development", "development_token")],
)
async def test_config_file_supplies_the_environment_token(
    gpp_transport, _no_user_configuration, environment, key
) -> None:
    _no_user_configuration.write_text(f'{key} = "file-token"\n')

    request = await _send_ping(gpp_transport, environment=environment)

    assert request.headers["Authorization"] == "Bearer file-token"


@pytest.mark.asyncio
async def test_variable_beats_the_config_file_token(
    gpp_transport, monkeypatch, _no_user_configuration
) -> None:
    _no_user_configuration.write_text('token = "file-token"\n')
    monkeypatch.setenv("GPP_TOKEN", "variable-token")

    request = await _send_ping(gpp_transport, environment="production")

    assert request.headers["Authorization"] == "Bearer variable-token"


def test_config_file_sets_debug(_no_user_configuration, mocker) -> None:
    _no_user_configuration.write_text("debug = true\n")
    mocker.patch.object(GPPClient, "_enable_dev_logging")

    client = GPPClient(environment="production", token="t")

    assert client.settings.debug is True


def test_invalid_config_file_fails_naming_it(_no_user_configuration) -> None:
    _no_user_configuration.write_text("token = \n")

    with pytest.raises(GPPClientError) as error:
        GPPClient(environment="production", token="t")

    assert str(error.value).startswith(
        f"Cannot read {_no_user_configuration}: it is not valid TOML"
    )


@pytest.mark.asyncio
async def test_empty_values_fall_through(gpp_transport, monkeypatch) -> None:
    monkeypatch.setenv("GPP_ENVIRONMENT", "")

    with pytest.warns(FutureWarning, match="No GPP environment set"):
        request = await _send_ping(gpp_transport, environment="", token="prod-token")

    assert str(request.url) == f"{PRODUCTION_URL}/odb"


@pytest.mark.parametrize("source", ["argument", "variable", "dotenv"])
def test_blank_environment_counts_as_unset(monkeypatch, tmp_path, source) -> None:
    monkeypatch.chdir(tmp_path)
    kwargs = {}
    if source == "argument":
        kwargs["environment"] = "   "
    elif source == "variable":
        monkeypatch.setenv("GPP_ENVIRONMENT", "   ")
    else:
        (tmp_path / ".env").write_text("GPP_ENVIRONMENT='   '\n")

    with pytest.warns(FutureWarning, match="No GPP environment set"):
        client = GPPClient(token="t", **kwargs)

    assert client.settings.environment is GPPEnvironment.PRODUCTION
    assert "environment" not in client.settings.model_fields_set


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


@pytest.mark.parametrize(
    ("source", "named"),
    [
        ("argument", "the environment argument"),
        ("variable", "GPP_ENVIRONMENT"),
        ("dotenv", "the .env file"),
        ("config", "the configuration file"),
    ],
)
def test_one_log_line_names_the_environment_its_source_and_url(
    caplog, monkeypatch, tmp_path, _no_user_configuration, source, named
) -> None:
    monkeypatch.chdir(tmp_path)
    kwargs = {}
    if source == "argument":
        kwargs["environment"] = "development"
    elif source == "variable":
        monkeypatch.setenv("GPP_ENVIRONMENT", "development")
    elif source == "dotenv":
        (tmp_path / ".env").write_text("GPP_ENVIRONMENT=development\n")
    else:
        _no_user_configuration.write_text('environment = "development"\n')

    with caplog.at_level(logging.INFO, logger="gpp_client"):
        GPPClient(token="t", **kwargs)

    lines = [r.getMessage() for r in caplog.records if r.levelno >= logging.INFO]
    assert lines == [
        f"GPPClient using the development environment, from {named}, "
        f"at {DEVELOPMENT_URL}/odb"
    ]


def test_log_line_says_production_was_the_fallback(caplog) -> None:
    with (
        caplog.at_level(logging.INFO, logger="gpp_client"),
        pytest.warns(FutureWarning),
    ):
        GPPClient(token="t")

    lines = [r.getMessage() for r in caplog.records if r.levelno >= logging.INFO]
    assert lines == [
        "GPPClient using the production environment, from the default, "
        f"at {PRODUCTION_URL}/odb"
    ]


def test_repr_names_the_environment() -> None:
    client = GPPClient(environment="development", token="t")

    assert repr(client) == "GPPClient(environment='development')"


@pytest.mark.parametrize(
    ("blank", "below"),
    [("variable", "dotenv"), ("variable", "config"), ("dotenv", "config")],
)
def test_blank_source_falls_through_to_the_next_one(
    monkeypatch, tmp_path, _no_user_configuration, blank, below
) -> None:
    monkeypatch.chdir(tmp_path)
    if blank == "variable":
        monkeypatch.setenv("GPP_ENVIRONMENT", "   ")
    else:
        (tmp_path / ".env").write_text("GPP_ENVIRONMENT='   '\n")
    if below == "dotenv":
        (tmp_path / ".env").write_text("GPP_ENVIRONMENT=development\n")
    else:
        _no_user_configuration.write_text('environment = "development"\n')

    with warnings.catch_warnings():
        warnings.simplefilter("error")
        client = GPPClient(token="t")

    assert client.settings.environment is GPPEnvironment.DEVELOPMENT


@pytest.mark.parametrize("blank", ["", "   "])
def test_blank_config_environment_falls_through_to_production(
    _no_user_configuration, blank
) -> None:
    _no_user_configuration.write_text(f'environment = "{blank}"\n')

    with pytest.warns(FutureWarning):
        client = GPPClient(token="t")

    assert client.settings.environment is GPPEnvironment.PRODUCTION


def _set_environment(source, name, monkeypatch, tmp_path, config_path) -> dict:
    """
    Name the environment in one source; return the client arguments it needs.
    """
    if source == "argument":
        return {"environment": name}
    write_environment(source, name, monkeypatch, tmp_path, config_path)
    return {}


@pytest.mark.parametrize(
    ("higher", "lower"),
    [
        ("argument", "dotenv"),
        ("argument", "config"),
        ("variable", "dotenv"),
        ("variable", "config"),
        ("dotenv", "config"),
    ],
)
def test_each_source_beats_the_ones_after_it(
    monkeypatch, tmp_path, _no_user_configuration, higher, lower
) -> None:
    monkeypatch.chdir(tmp_path)
    kwargs = _set_environment(
        lower, "production", monkeypatch, tmp_path, _no_user_configuration
    )
    kwargs |= _set_environment(
        higher, "development", monkeypatch, tmp_path, _no_user_configuration
    )

    client = GPPClient(token="t", **kwargs)

    assert client.settings.environment is GPPEnvironment.DEVELOPMENT


@pytest.mark.parametrize("value", ["prod", "staging"])
@pytest.mark.parametrize("source", ["argument", "variable", "dotenv", "config"])
def test_bad_environment_from_any_source_fails_listing_valid_names(
    monkeypatch, tmp_path, _no_user_configuration, source, value
) -> None:
    monkeypatch.chdir(tmp_path)
    kwargs = _set_environment(
        source, value, monkeypatch, tmp_path, _no_user_configuration
    )

    with pytest.raises(GPPClientError) as error:
        GPPClient(token="t", **kwargs)

    assert str(error.value) == (
        f"Unknown GPP environment '{value}'. Valid names: development, production."
    )


def test_config_environment_that_is_not_text_fails_naming_it(
    _no_user_configuration,
) -> None:
    _no_user_configuration.write_text("environment = 1\n")

    with pytest.raises(GPPClientError) as error:
        GPPClient(token="t")

    assert str(error.value) == (
        "Unknown GPP environment 1. Valid names: development, production."
    )


@pytest.mark.parametrize("source", ["variable", "dotenv", "config"])
def test_environment_from_any_source_ignores_case(
    monkeypatch, tmp_path, _no_user_configuration, source
) -> None:
    monkeypatch.chdir(tmp_path)
    _set_environment(
        source, "Development", monkeypatch, tmp_path, _no_user_configuration
    )

    client = GPPClient(token="t")

    assert client.settings.environment is GPPEnvironment.DEVELOPMENT
