"""
Tests for the REST client.
"""

from types import SimpleNamespace

import pytest

from gpp_client.rest.client import RESTClient


@pytest.fixture()
def rest_client() -> RESTClient:
    """
    Return a reusable REST client instance.
    """
    return RESTClient(
        base_url="https://example.test",
        gpp_token="secret-token",
        timeout=10,
    )


def test_resolve_headers(rest_client: RESTClient) -> None:
    """
    Ensure headers are resolved correctly.
    """
    assert rest_client._resolve_headers() == {
        "Content-Type": "text/plain",
        "Authorization": "Bearer secret-token",
    }


@pytest.mark.asyncio
async def test_get_session_creates_session_when_missing(
    mocker,
    rest_client: RESTClient,
) -> None:
    """
    Ensure get_session creates a session when none exists.
    """
    session = SimpleNamespace(closed=False)
    create_session = mocker.patch.object(
        rest_client,
        "_create_session",
        return_value=session,
    )

    result = await rest_client.get_session()

    assert result is session
    assert rest_client._session is session
    create_session.assert_called_once_with()


@pytest.mark.asyncio
async def test_get_session_reuses_open_session(
    mocker,
    rest_client: RESTClient,
) -> None:
    """
    Ensure get_session reuses an existing open session.
    """
    session = SimpleNamespace(closed=False)
    rest_client._session = session
    create_session = mocker.patch.object(rest_client, "_create_session")

    result = await rest_client.get_session()

    assert result is session
    create_session.assert_not_called()


@pytest.mark.asyncio
async def test_get_session_recreates_closed_session(
    mocker,
    rest_client: RESTClient,
) -> None:
    """
    Ensure get_session recreates a closed session.
    """
    old_session = SimpleNamespace(closed=True)
    new_session = SimpleNamespace(closed=False)
    rest_client._session = old_session
    create_session = mocker.patch.object(
        rest_client,
        "_create_session",
        return_value=new_session,
    )

    result = await rest_client.get_session()

    assert result is new_session
    assert rest_client._session is new_session
    create_session.assert_called_once_with()


@pytest.mark.asyncio
async def test_close_closes_open_session(rest_client: RESTClient, mocker) -> None:
    """
    Ensure close closes an open session.
    """
    session = SimpleNamespace(
        closed=False,
        close=mocker.AsyncMock(),
    )
    rest_client._session = session

    await rest_client.close()

    session.close.assert_called_once_with()


@pytest.mark.asyncio
async def test_close_skips_when_session_already_closed(
    rest_client: RESTClient,
    mocker,
) -> None:
    """
    Ensure close does nothing when the session is already closed.
    """
    session = SimpleNamespace(
        closed=True,
        close=mocker.AsyncMock(),
    )
    rest_client._session = session

    await rest_client.close()

    session.close.assert_not_called()


@pytest.mark.asyncio
async def test_async_context_manager_returns_self(
    rest_client: RESTClient,
) -> None:
    """
    Ensure async context manager returns the client itself.
    """
    async with rest_client as entered_client:
        assert entered_client is rest_client


@pytest.mark.asyncio
async def test_async_context_manager_closes_on_exit(
    rest_client: RESTClient,
    mocker,
) -> None:
    """
    Ensure async context manager closes on exit.
    """
    close_mock = mocker.patch.object(rest_client, "close")

    async with rest_client:
        pass

    close_mock.assert_called_once_with()
