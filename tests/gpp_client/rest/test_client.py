"""
Tests for the REST client.
"""

from datetime import datetime, timezone
from types import SimpleNamespace

import pytest

from gpp_client.rest.client import RESTClient


class _FakeResponse:
    """
    Async-context-manager response stub for session.get/post.
    """

    def __init__(self, text: str = "", status: int = 200) -> None:
        self._text = text
        self.status = status
        self.raise_for_status_called = False

    def raise_for_status(self) -> None:
        self.raise_for_status_called = True
        if self.status >= 400:
            raise RuntimeError(f"HTTP {self.status}")

    async def text(self) -> str:
        return self._text

    async def __aenter__(self) -> "_FakeResponse":
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb) -> None:
        return None


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


@pytest.mark.asyncio
async def test_get_visibility_changes_requests_endpoint(
    rest_client: RESTClient,
    mocker,
) -> None:
    """
    Ensure the visibility-changes endpoint is queried with the since param.
    """
    response = _FakeResponse(text="o-123\t2026-07-15T10:00:00Z\n")
    session = SimpleNamespace(get=mocker.Mock(return_value=response))
    mocker.patch.object(rest_client, "get_session", return_value=session)

    since = datetime(2026, 7, 15, 9, 0, tzinfo=timezone.utc)
    result = await rest_client._get_visibility_changes(since)

    assert result == "o-123\t2026-07-15T10:00:00Z\n"
    assert response.raise_for_status_called
    session.get.assert_called_once_with(
        "/scheduler/visibility-changes",
        params={"since": "2026-07-15T09:00:00+00:00"},
    )


@pytest.mark.asyncio
async def test_get_visibility_changes_assumes_utc_for_naive_since(
    rest_client: RESTClient,
    mocker,
) -> None:
    """
    Ensure a naive since datetime is treated as UTC.
    """
    response = _FakeResponse(text="")
    session = SimpleNamespace(get=mocker.Mock(return_value=response))
    mocker.patch.object(rest_client, "get_session", return_value=session)

    await rest_client._get_visibility_changes(datetime(2026, 7, 15, 9, 0))

    session.get.assert_called_once_with(
        "/scheduler/visibility-changes",
        params={"since": "2026-07-15T09:00:00+00:00"},
    )


@pytest.mark.asyncio
async def test_get_visibility_changes_raises_on_http_error(
    rest_client: RESTClient,
    mocker,
) -> None:
    """
    Ensure HTTP errors propagate to the caller.
    """
    response = _FakeResponse(text="boom", status=500)
    session = SimpleNamespace(get=mocker.Mock(return_value=response))
    mocker.patch.object(rest_client, "get_session", return_value=session)

    with pytest.raises(RuntimeError, match="HTTP 500"):
        await rest_client._get_visibility_changes(
            datetime(2026, 7, 15, 9, 0, tzinfo=timezone.utc)
        )
