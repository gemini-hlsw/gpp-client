"""Tests for the main GPP client."""

from types import SimpleNamespace

import httpx
import pytest

from gpp_client.client import _HTTP_TIMEOUT, GPPClient
from gpp_client.constants import DEVELOPMENT_URL, PRODUCTION_URL
from gpp_client.environment import GPPEnvironment
from gpp_client.urls import get_graphql_url


@pytest.fixture()
def mock_settings() -> SimpleNamespace:
    """
    Return a reusable fake settings object.
    """
    return SimpleNamespace(
        debug=False,
        resolved_token="resolved-token",
        token="raw-token",
        environment=GPPEnvironment.PRODUCTION,
    )


@pytest.fixture()
def bare_client() -> GPPClient:
    """
    Return an uninitialized GPPClient instance for targeted tests.
    """
    return object.__new__(GPPClient)


def test_init_builds_settings_and_core_clients(
    mocker,
    mock_settings,
) -> None:
    """
    Ensure initialization builds settings and core clients.
    """
    graphql_client = SimpleNamespace(url="https://graphql.example.test")
    rest_client = object()

    build_settings = mocker.patch.object(
        GPPClient,
        "_build_settings",
        return_value=mock_settings,
    )
    build_graphql = mocker.patch.object(
        GPPClient,
        "_build_graphql_client",
        return_value=graphql_client,
    )
    build_rest = mocker.patch.object(
        GPPClient,
        "_build_rest_client",
        return_value=rest_client,
    )
    init_domains = mocker.patch.object(GPPClient, "_init_domains")

    client = GPPClient(token="abc", debug=True)

    build_settings.assert_called_once_with(environment=None, token="abc", debug=True)
    build_graphql.assert_called_once_with(None)
    build_rest.assert_called_once_with()
    init_domains.assert_called_once_with()

    assert client.settings is mock_settings
    assert client.graphql is graphql_client
    assert client.rest is rest_client


def test_init_enables_dev_logging_when_debug_true(
    mocker,
    mock_settings,
) -> None:
    """
    Ensure debug logging is enabled when settings.debug is true.
    """
    mock_settings.debug = True

    mocker.patch.object(
        GPPClient,
        "_build_settings",
        return_value=mock_settings,
    )
    mocker.patch.object(
        GPPClient,
        "_build_graphql_client",
        return_value=SimpleNamespace(url="https://graphql.example.test"),
    )
    mocker.patch.object(
        GPPClient,
        "_build_rest_client",
        return_value=object(),
    )
    mocker.patch.object(GPPClient, "_init_domains")
    enable_logging = mocker.patch.object(GPPClient, "_enable_dev_logging")

    GPPClient()

    enable_logging.assert_called_once_with()


def test_graphql_client_targets_the_selected_environment() -> None:
    """
    Ensure the GraphQL client sends HTTP and websocket requests to the selected
    environment with the token, and waits longer than httpx's 5 second default.
    """
    client = GPPClient(environment="development", token="dev-token")
    auth = {"Authorization": "Bearer dev-token"}

    assert client.graphql.url == f"{DEVELOPMENT_URL}/odb"
    assert client.graphql.ws_url == "wss://lucuma-postgres-odb-dev.herokuapp.com/ws"
    assert client.graphql.ws_headers == auth
    assert client.graphql.ws_connection_init_payload == auth
    assert client.graphql.http_client.timeout == _HTTP_TIMEOUT


def test_build_rest_client_uses_expected_settings(
    mocker,
    bare_client,
    mock_settings,
) -> None:
    """
    Ensure the REST client is constructed from settings.
    """
    rest_cls = mocker.patch("gpp_client.client.RESTClient")

    bare_client._settings = mock_settings

    bare_client._build_rest_client()

    rest_cls.assert_called_once_with(
        base_url=PRODUCTION_URL,
        gpp_token="resolved-token",
        environment=GPPEnvironment.PRODUCTION,
    )


def test_init_domains_uses_shared_domain_kwargs(
    mocker,
    bare_client,
    mock_settings,
) -> None:
    """
    Ensure domain instances are initialized with shared dependencies.
    """
    scheduler_domain = object()
    target_domain = object()
    workflow_state_domain = object()
    observation_domain = object()
    program_domain = object()
    site_status_domain = object()
    goats_domain = object()
    atom_domain = object()
    attachment_domain = object()

    scheduler_cls = mocker.patch(
        "gpp_client.client.SchedulerDomain",
        return_value=scheduler_domain,
    )
    target_cls = mocker.patch(
        "gpp_client.client.TargetDomain",
        return_value=target_domain,
    )
    workflow_state_cls = mocker.patch(
        "gpp_client.client.WorkflowStateDomain",
        return_value=workflow_state_domain,
    )
    observation_cls = mocker.patch(
        "gpp_client.client.ObservationDomain",
        return_value=observation_domain,
    )
    program_cls = mocker.patch(
        "gpp_client.client.ProgramDomain",
        return_value=program_domain,
    )
    site_status_cls = mocker.patch(
        "gpp_client.client.SiteStatusDomain",
        return_value=site_status_domain,
    )
    goats_cls = mocker.patch(
        "gpp_client.client.GOATSDomain",
        return_value=goats_domain,
    )
    atom_cls = mocker.patch(
        "gpp_client.client.AtomDomain",
        return_value=atom_domain,
    )
    attachment_cls = mocker.patch(
        "gpp_client.client.AttachmentDomain",
        return_value=attachment_domain,
    )

    bare_client._graphql = object()
    bare_client._rest = object()
    bare_client._settings = mock_settings

    bare_client._init_domains()

    expected_domain_kwargs = {
        "graphql": bare_client._graphql,
        "rest": bare_client._rest,
        "settings": mock_settings,
    }

    scheduler_cls.assert_called_once_with(**expected_domain_kwargs)
    target_cls.assert_called_once_with(**expected_domain_kwargs)
    workflow_state_cls.assert_called_once_with(**expected_domain_kwargs)
    observation_cls.assert_called_once_with(**expected_domain_kwargs)
    program_cls.assert_called_once_with(**expected_domain_kwargs)
    goats_cls.assert_called_once_with(**expected_domain_kwargs)
    atom_cls.assert_called_once_with(**expected_domain_kwargs)
    attachment_cls.assert_called_once_with(**expected_domain_kwargs)
    site_status_cls.assert_called_once_with()

    assert bare_client.scheduler is scheduler_domain
    assert bare_client.target is target_domain
    assert bare_client.workflow_state is workflow_state_domain
    assert bare_client.observation is observation_domain
    assert bare_client.program is program_domain
    assert bare_client.site_status is site_status_domain
    assert bare_client.goats is goats_domain
    assert bare_client.atom is atom_domain
    assert bare_client.attachment is attachment_domain


@pytest.mark.asyncio
async def test_close_delegates_to_rest_client(
    mocker,
    bare_client,
) -> None:
    """
    Ensure close delegates to the REST client.
    """
    rest_client = SimpleNamespace(close=mocker.AsyncMock())
    bare_client._rest = rest_client
    bare_client._owns_http_client = False

    await bare_client.close()

    rest_client.close.assert_called_once_with()


@pytest.mark.asyncio
async def test_async_context_manager_closes_client(
    mocker,
    bare_client,
) -> None:
    """
    Ensure async context manager closes the client on exit.
    """
    bare_client.close = mocker.AsyncMock()

    async with bare_client as entered_client:
        assert entered_client is bare_client

    bare_client.close.assert_called_once_with()


@pytest.mark.asyncio
async def test_ping_returns_success_on_success(
    mocker,
    bare_client,
) -> None:
    """
    Ensure ping returns success when GraphQL ping succeeds.
    """
    graphql = SimpleNamespace(
        url="https://graphql.example.test",
        ping=mocker.AsyncMock(return_value=None),
    )
    bare_client._graphql = graphql

    success, error = await bare_client.ping()

    assert success is True
    assert error is None
    graphql.ping.assert_called_once_with()


@pytest.mark.asyncio
async def test_ping_returns_failure_on_exception(
    mocker,
    bare_client,
) -> None:
    """
    Ensure ping returns failure and message when GraphQL ping fails.
    """
    graphql = SimpleNamespace(
        url="https://graphql.example.test",
        ping=mocker.AsyncMock(side_effect=RuntimeError("boom")),
    )
    bare_client._graphql = graphql

    success, error = await bare_client.ping()

    assert success is False
    assert error == "boom"
    graphql.ping.assert_called_once_with()


@pytest.mark.asyncio
async def test_supplied_http_client_sends_auth_header(
    gpp_client,
    gpp_transport,
) -> None:
    """
    Ensure requests through a caller-supplied http client carry the token.
    """
    gpp_transport.respond({"observation": None})

    await gpp_client.workflow_state.get_by_id(observation_id="o-1")

    [request] = gpp_transport.requests
    assert request.headers["Authorization"] == "Bearer test-token"
    assert str(request.url) == get_graphql_url(gpp_client.settings.environment)


@pytest.mark.asyncio
async def test_clients_sharing_http_client_send_own_token(gpp_transport) -> None:
    """
    Ensure two clients sharing one http client each send their own token and
    leave the shared client's headers unchanged.
    """
    gpp_transport.respond({"observation": None})
    gpp_transport.respond({"observation": None})

    async with httpx.AsyncClient(
        transport=gpp_transport, headers={"X-Caller": "kept"}
    ) as http_client:
        headers_before = dict(http_client.headers)
        first = GPPClient(token="token-a", http_client=http_client)
        second = GPPClient(token="token-b", http_client=http_client)

        await first.workflow_state.get_by_id(observation_id="o-1")
        await second.workflow_state.get_by_id(observation_id="o-1")

        assert dict(http_client.headers) == headers_before

    sent = [request.headers["Authorization"] for request in gpp_transport.requests]
    assert sent == ["Bearer token-a", "Bearer token-b"]
    assert all(r.headers["X-Caller"] == "kept" for r in gpp_transport.requests)


@pytest.mark.asyncio
async def test_exit_closes_built_http_client() -> None:
    """
    Ensure leaving the context closes the http client the client built.
    """
    async with GPPClient(token="test-token") as client:
        http_client = client.graphql.http_client

    assert http_client.is_closed


@pytest.mark.asyncio
async def test_exit_leaves_supplied_http_client_open(gpp_transport) -> None:
    """
    Ensure leaving the context leaves a caller-supplied http client open.
    """
    async with httpx.AsyncClient(transport=gpp_transport) as http_client:
        async with GPPClient(token="test-token", http_client=http_client):
            pass

        assert not http_client.is_closed
