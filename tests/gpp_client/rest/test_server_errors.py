"""
Tests that every REST failure is raised as a ``GPPError`` naming the
environment.

A local aiohttp server stands in for GPP, so the REST client runs its real
HTTP code offline.
"""

from datetime import UTC, datetime

import pytest
import pytest_asyncio
from aiohttp import web

from gpp_client import GPPClient
from gpp_client.environment import GPPEnvironment
from gpp_client.exceptions import GPPHttpError, GPPTransportError
from gpp_client.rest import RESTClient

_CALLS = pytest.mark.parametrize(
    ("call", "path"),
    [
        (
            lambda rest: rest.get_visibility_changes(datetime.now(UTC)),
            "/scheduler/visibility-changes",
        ),
        (lambda rest: rest.get_atom_digests(["o-1"]), "/scheduler/atoms"),
    ],
    ids=["visibility-changes", "atoms"],
)


@pytest_asyncio.fixture(loop_scope="function")
async def served():
    """
    Return a function that starts a server answering every request one way.
    """
    runners = []

    async def start(status: int, text: str) -> str:
        async def answer(request: web.Request) -> web.Response:
            return web.Response(status=status, text=text)

        app = web.Application()
        app.router.add_route("*", "/{tail:.*}", answer)
        runner = web.AppRunner(app)
        await runner.setup()
        site = web.TCPSite(runner, "127.0.0.1", 0)
        await site.start()
        runners.append(runner)
        host, port = runner.addresses[0][:2]
        return f"http://{host}:{port}"

    try:
        yield start
    finally:
        for runner in runners:
            await runner.cleanup()


def _rest(url: str) -> RESTClient:
    return RESTClient(
        base_url=url, gpp_token="test-token", environment=GPPEnvironment.PRODUCTION
    )


@_CALLS
@pytest.mark.asyncio
async def test_a_404_is_an_http_error_saying_the_path_may_not_be_served(
    served, call, path
):
    async with _rest(await served(404, "Not Found")) as rest:
        with pytest.raises(GPPHttpError) as raised:
            await call(rest)

    assert raised.value.status_code == 404
    assert str(raised.value) == (
        f"GPP production answered HTTP 404: Not Found; the path {path} may not "
        "be served on production"
    )


@_CALLS
@pytest.mark.asyncio
async def test_an_error_status_raises_with_the_status_and_body(served, call, path):
    async with _rest(await served(500, "boom")) as rest:
        with pytest.raises(GPPHttpError) as raised:
            await call(rest)

    assert raised.value.status_code == 500
    assert str(raised.value) == "GPP production answered HTTP 500: boom"


@_CALLS
@pytest.mark.asyncio
async def test_a_connection_failure_names_the_environment(served, call, path):
    url = await served(200, "")
    async with _rest(url.replace("http://", "http://closed.")) as rest:
        with pytest.raises(GPPTransportError) as raised:
            await call(rest)

    assert str(raised.value).startswith("GPP production could not be reached: ")


@pytest.mark.asyncio
async def test_an_attachment_call_gpp_refuses_names_the_environment(
    served,
):
    client = GPPClient(environment="development", token="test-token")
    client.rest.base_url = await served(404, "attachment a-1 not found")
    async with client:
        with pytest.raises(GPPHttpError) as raised:
            await client.attachment.get_download_url_by_id("a-1")

    assert raised.value.status_code == 404
    assert str(raised.value) == (
        "GPP development answered HTTP 404: attachment a-1 not found"
    )
