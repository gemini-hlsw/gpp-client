"""
Tests for GPPClient.
"""

import pytest

from gpp_client.client import GPPClient
from gpp_client.config import GPPEnvironment


@pytest.fixture
def patched_dependencies(mocker) -> dict[str, object]:
    """
    Patch GPPClient for easy testing.
    """
    resolved_url = "https://example.com/graphql"
    resolved_token = "TEST_TOKEN"
    resolved_env = GPPEnvironment.DEVELOPMENT

    base_url = GPPClient._get_base_url(resolved_url)
    ws_url = GPPClient._get_ws_url(base_url)

    fake_graphql = mocker.MagicMock()
    fake_graphql.execute = mocker.AsyncMock()

    fake_rest = mocker.MagicMock()
    fake_rest.close = mocker.AsyncMock()

    resolve_credentials = mocker.patch(
        "gpp_client.client.CredentialResolver.resolve",
        autospec=True,
        return_value=(resolved_url, resolved_token, resolved_env),
    )
    graphql_client = mocker.patch(
        "gpp_client.client._GPPClient",
        autospec=True,
        return_value=fake_graphql,
    )
    rest_client = mocker.patch(
        "gpp_client.client._GPPRESTClient",
        autospec=True,
        return_value=fake_rest,
    )
    enable_dev_logging = mocker.patch(
        "gpp_client.client._enable_dev_console_logging",
        autospec=True,
    )

    return {
        "resolved_url": resolved_url,
        "resolved_token": resolved_token,
        "resolved_env": resolved_env,
        "base_url": base_url,
        "ws_url": ws_url,
        "resolve_credentials": resolve_credentials,
        "graphql_client": graphql_client,
        "rest_client": rest_client,
        "enable_dev_logging": enable_dev_logging,
        "fake_graphql": fake_graphql,
        "fake_rest": fake_rest,
    }


@pytest.mark.parametrize(
    "env_input,expected_env",
    [
        ("development", GPPEnvironment.DEVELOPMENT),
        (GPPEnvironment.DEVELOPMENT, GPPEnvironment.DEVELOPMENT),
        (None, None),
    ],
)
def test_init_normalizes_env_before_resolving_credentials(
    patched_dependencies: dict[str, object],
    env_input: GPPEnvironment | str | None,
    expected_env: GPPEnvironment | None,
) -> None:
    """
    Test that the env parameter is normalized before being passed to
    ``CredentialResolver``.
    """
    resolve_credentials = patched_dependencies["resolve_credentials"]

    GPPClient(env=env_input, token="abc", _debug=False)

    _, kwargs = resolve_credentials.call_args
    assert kwargs["env"] == expected_env
    assert kwargs["token"] == "abc"
    assert kwargs["config"] is not None


def test_init_invalid_env_string_raises_value_error() -> None:
    """
    Test that an invalid env string raises ``ValueError``.
    """
    with pytest.raises(ValueError):
        GPPClient(env="NOT_A_REAL_ENV", _debug=False)


def test_init_debug_true_enables_console_logging(
    patched_dependencies: dict[str, object],
) -> None:
    """
    Test that ``debug=True`` enables console logging.
    """
    enable_dev_logging = patched_dependencies["enable_dev_logging"]

    GPPClient(env="development", token="abc", _debug=True)

    enable_dev_logging.assert_called_once()


def test_init_debug_false_does_not_enable_console_logging(
    patched_dependencies: dict[str, object],
) -> None:
    """
    Test that ``debug=False`` does not enable console logging.
    """
    enable_dev_logging = patched_dependencies["enable_dev_logging"]

    GPPClient(env="development", token="abc", _debug=False)

    enable_dev_logging.assert_not_called()


def test_init_constructs_clients_from_resolved_credentials(
    patched_dependencies: dict[str, object],
) -> None:
    """
    Test that the GraphQL and REST clients are constructed with the
    resolved credentials.
    """
    graphql_client = patched_dependencies["graphql_client"]
    rest_client = patched_dependencies["rest_client"]

    client = GPPClient(_debug=False)

    assert client._client is patched_dependencies["fake_graphql"]
    assert client._rest_client is patched_dependencies["fake_rest"]

    _, gql_kwargs = graphql_client.call_args
    assert gql_kwargs["url"] == patched_dependencies["resolved_url"]
    assert gql_kwargs["headers"] == {
        "Authorization": f"Bearer {patched_dependencies['resolved_token']}"
    }
    assert gql_kwargs["ws_url"] == patched_dependencies["ws_url"]
    assert gql_kwargs["ws_connection_init_payload"] == {
        "Authorization": f"Bearer {patched_dependencies['resolved_token']}"
    }

    rest_client.assert_called_once_with(
        patched_dependencies["base_url"],
        patched_dependencies["resolved_token"],
    )


def test_init_initializes_all_managers(patched_dependencies: dict[str, object]) -> None:
    """
    Test that all manager attributes are initialized.
    """
    client = GPPClient(_debug=False)

    assert client.program_note is not None
    assert client.target is not None
    assert client.program is not None
    assert client.call_for_proposals is not None
    assert client.observation is not None
    assert client.site_status is not None
    assert client.group is not None
    assert client.configuration_request is not None
    assert client.workflow_state is not None
    assert client.attachment is not None


@pytest.mark.asyncio
@pytest.mark.parametrize(
    "execute_raises,status_raises,expected_ok",
    [
        (None, None, True),
        (RuntimeError("boom"), None, False),
        (None, RuntimeError("bad status"), False),
    ],
)
async def test_is_reachable_returns_expected_tuple(
    mocker,
    patched_dependencies: dict[str, object],
    execute_raises: Exception | None,
    status_raises: Exception | None,
    expected_ok: bool,
) -> None:
    """
    Test that ``is_reachable`` returns the expected tuple based on different
    failure scenarios.
    """
    fake_graphql = patched_dependencies["fake_graphql"]

    if execute_raises is not None:
        fake_graphql.execute = mocker.AsyncMock(side_effect=execute_raises)
    else:
        response = mocker.MagicMock()
        response.raise_for_status.side_effect = status_raises
        fake_graphql.execute = mocker.AsyncMock(return_value=response)

    client = GPPClient(_debug=False)

    ok, error = await client.is_reachable()

    assert ok is expected_ok
    if expected_ok:
        assert error is None
    else:
        assert isinstance(error, str)
        assert error

    assert fake_graphql.execute.await_count == 1
    (query_arg,) = fake_graphql.execute.await_args.args
    assert "__schema" in query_arg


@pytest.mark.asyncio
async def test_close_closes_rest_client(
    patched_dependencies: dict[str, object],
) -> None:
    """
    Test that ``close`` calls ``close`` on the REST client.
    """
    client = GPPClient(_debug=False)

    await client.close()

    patched_dependencies["fake_rest"].close.assert_awaited_once()


@pytest.mark.asyncio
async def test_async_context_manager_closes(
    patched_dependencies: dict[str, object],
) -> None:
    """
    Test that the async context manager calls ``close`` on the REST client.
    """
    fake_rest = patched_dependencies["fake_rest"]

    async with GPPClient(_debug=False) as entered:
        assert isinstance(entered, GPPClient)
        fake_rest.close.assert_not_awaited()

    fake_rest.close.assert_awaited_once()


def test_set_credentials_delegates_to_config(mocker) -> None:
    """
    Test that ``set_credentials`` delegates to ``GPPConfig.set_credentials``.
    """
    mocked_config = mocker.patch("gpp_client.client.GPPConfig", autospec=True)
    instance = mocked_config.return_value

    GPPClient.set_credentials("development", "TOK", activate=True, save=False)

    instance.set_credentials.assert_called_once_with(
        "development",
        "TOK",
        activate=True,
        save=False,
    )


@pytest.mark.parametrize(
    "url,expected_base_url",
    [
        ("https://example.com/graphql", "https://example.com"),
        ("https://example.com/graphql?x=1", "https://example.com"),
        ("https://example.com/graphql#frag", "https://example.com"),
        ("http://localhost:8000/graphql", "http://localhost:8000"),
        ("http://localhost:8000/api/graphql", "http://localhost:8000"),
    ],
)
def test__get_base_url(url: str, expected_base_url: str) -> None:
    """
    Test that ``_get_base_url`` correctly extracts the base URL from various GraphQL
    URLs.
    """
    assert GPPClient._get_base_url(url) == expected_base_url


@pytest.mark.parametrize(
    "base_url,expected_ws_url",
    [
        ("https://example.com", "wss://example.com/ws"),
        ("https://example.com:8443", "wss://example.com:8443/ws"),
        ("http://localhost:8000", "ws://localhost:8000/ws"),
        ("http://127.0.0.1:8000", "ws://127.0.0.1:8000/ws"),
    ],
)
def test__get_ws_url(base_url: str, expected_ws_url: str) -> None:
    """
    Test that ``_get_ws_url`` correctly constructs the WebSocket URL from the base URL.
    """
    assert GPPClient._get_ws_url(base_url) == expected_ws_url
