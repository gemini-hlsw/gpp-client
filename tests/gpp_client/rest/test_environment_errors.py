"""
Tests that a REST path the environment does not serve raises the environment error.

A local aiohttp server stands in for GPP, so the REST client runs its real
HTTP code offline.
"""

from datetime import UTC, datetime

import pytest
import pytest_asyncio
from aiohttp import web

from gpp_client.environment import GPPEnvironment
from gpp_client.exceptions import GPPEnvironmentError
from gpp_client.rest import RESTClient


@pytest_asyncio.fixture(loop_scope="function")
async def not_found_url():
    """
    Return the URL of a server that answers every request with 404.
    """

    async def not_found(request: web.Request) -> web.Response:
        return web.Response(status=404, text="Not Found")

    app = web.Application()
    app.router.add_route("*", "/{tail:.*}", not_found)
    runner = web.AppRunner(app)
    await runner.setup()
    site = web.TCPSite(runner, "127.0.0.1", 0)
    await site.start()
    host, port = runner.addresses[0][:2]
    try:
        yield f"http://{host}:{port}"
    finally:
        await runner.cleanup()


@pytest.mark.parametrize(
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
@pytest.mark.asyncio
async def test_a_404_raises_naming_the_environment_and_path(not_found_url, call, path):
    async with RESTClient(
        base_url=not_found_url,
        gpp_token="test-token",
        environment=GPPEnvironment.DEVELOPMENT,
    ) as rest:
        with pytest.raises(GPPEnvironmentError) as raised:
            await call(rest)

    error = raised.value
    assert error.item == path
    assert error.kind == "REST path"
    assert error.environment is GPPEnvironment.DEVELOPMENT
    assert error.available == ()
    assert str(error) == (
        f"The REST path {path} is not served on development: GPP answered 404. "
        "Check the path, or wait until development serves it."
    )
    assert "production" not in str(error)
