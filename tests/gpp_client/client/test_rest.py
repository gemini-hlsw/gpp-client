"""
Tests for the REST client.
"""

import aiohttp
import pytest

from gpp_client.rest import _GPPRESTClient


@pytest.fixture
def rest_client() -> _GPPRESTClient:
    """
    Fixture that provides a REST client instance.
    """
    return _GPPRESTClient("https://example.invalid/graphql", "TOK", timeout=12.5)


def test_get_base_url_extracts_scheme_and_netloc(rest_client: _GPPRESTClient) -> None:
    """
    Test that ``get_base_url`` extracts the base URL correctly.
    """
    assert (
        rest_client.get_base_url("https://example.invalid/graphql")
        == "https://example.invalid"
    )
    assert (
        rest_client.get_base_url("http://example.invalid:8080/foo")
        == "http://example.invalid:8080"
    )


def test_resolve_headers_includes_bearer_and_content_type(
    rest_client: _GPPRESTClient,
) -> None:
    """
    Test that ``resolve_headers`` includes the correct Content-Type and Authorization
    headers.
    """
    headers = rest_client.resolve_headers()

    assert headers["Content-Type"] == "text/plain"
    assert headers["Authorization"] == "Bearer TOK"


@pytest.mark.asyncio
async def test_get_session_creates_session_once_and_reuses(
    mocker, rest_client: _GPPRESTClient
) -> None:
    """
    Test that ``get_session`` creates the session once and reuses it on subsequent
    calls.
    """
    mocker.patch("gpp_client.rest.certifi.where", return_value="/fake/cacert.pem")
    ssl_ctx = object()
    mocker.patch("gpp_client.rest.ssl.create_default_context", return_value=ssl_ctx)

    connector = object()
    tcp_connector = mocker.patch(
        "gpp_client.rest.aiohttp.TCPConnector", return_value=connector
    )

    # Fake session instance with the minimal surface we use.
    session = mocker.MagicMock(spec=aiohttp.ClientSession)
    session.closed = False

    client_session_ctor = mocker.patch(
        "gpp_client.rest.aiohttp.ClientSession",
        return_value=session,
    )

    s1 = await rest_client.get_session()
    s2 = await rest_client.get_session()

    # Same object returned, constructor called once.
    assert s1 is session
    assert s2 is session
    assert client_session_ctor.call_count == 1

    # Assert the “wiring” into aiohttp.ClientSession is correct.
    _, kwargs = client_session_ctor.call_args
    assert kwargs["base_url"] == rest_client.base_url
    assert isinstance(kwargs["timeout"], aiohttp.ClientTimeout)
    assert kwargs["timeout"].total == 12.5
    assert kwargs["connector"] == connector
    assert kwargs["headers"]["Authorization"] == "Bearer TOK"

    # Assert we built TCPConnector with the SSL context.
    tcp_connector.assert_called_once()
    _, tcp_kwargs = tcp_connector.call_args
    assert tcp_kwargs["ssl"] is ssl_ctx


@pytest.mark.asyncio
async def test_get_session_recreates_if_closed(
    mocker, rest_client: _GPPRESTClient
) -> None:
    """
    Test that ``get_session`` recreates the session if the existing one is closed.
    """
    mocker.patch("gpp_client.rest.certifi.where", return_value="/fake/cacert.pem")
    mocker.patch("gpp_client.rest.ssl.create_default_context", return_value=object())
    mocker.patch("gpp_client.rest.aiohttp.TCPConnector", return_value=object())

    session1 = mocker.MagicMock(spec=aiohttp.ClientSession)
    session1.closed = True  # Simulate closed session.

    session2 = mocker.MagicMock(spec=aiohttp.ClientSession)
    session2.closed = False

    client_session_ctor = mocker.patch(
        "gpp_client.rest.aiohttp.ClientSession",
        side_effect=[session1, session2],
    )

    s1 = await rest_client.get_session()
    assert s1 is session1

    # Since session is closed, next call should create a new one.
    s2 = await rest_client.get_session()
    assert s2 is session2

    assert client_session_ctor.call_count == 2


@pytest.mark.asyncio
async def test_close_closes_when_open(mocker, rest_client: _GPPRESTClient) -> None:
    """
    Test that ``close`` closes the session when it is open.
    """
    session = mocker.MagicMock(spec=aiohttp.ClientSession)
    session.closed = False
    session.close = mocker.AsyncMock()

    rest_client._session = session

    await rest_client.close()

    session.close.assert_awaited_once()


@pytest.mark.asyncio
async def test_close_noop_when_missing_or_closed(
    mocker, rest_client: _GPPRESTClient
) -> None:
    """
    Test that ``close`` is a noop when there is no session or the session is already
    closed.
    """
    rest_client._session = None
    await rest_client.close()

    # Closed session -> noop.
    session = mocker.MagicMock(spec=aiohttp.ClientSession)
    session.closed = True
    session.close = mocker.AsyncMock()
    rest_client._session = session

    await rest_client.close()
    session.close.assert_not_awaited()


@pytest.mark.asyncio
async def test_async_context_manager_closes(mocker) -> None:
    """
    Test that the async context manager closes the client on exit.
    """
    client = _GPPRESTClient("https://example.invalid/graphql", "TOK")

    close_spy = mocker.spy(client, "close")

    async with client as entered:
        assert entered is client
        close_spy.assert_not_called()

    close_spy.assert_awaited_once()
