"""
Tests that the scheduler domain works on development and production.

Each test builds a real ``GPPClient`` for one environment. GraphQL goes to an
httpx mock transport; REST and subscriptions go to local servers, so the
REST and websocket clients run their real protocol code offline.
"""

from datetime import UTC, datetime

import httpx
import pytest
import pytest_asyncio
from aiohttp import web

from gpp_client import GPPClient
from gpp_client.environment import GPPEnvironment
from gpp_client.exceptions import GPPEnvironmentError
from tests.gpp_client.conftest import TEST_TOKEN, RecordingTransport
from tests.gpp_client.subscription_server import SubscriptionServer, ws_url

ENVIRONMENTS = [GPPEnvironment.DEVELOPMENT, GPPEnvironment.PRODUCTION]


async def _serve(handler) -> tuple[web.AppRunner, str]:
    app = web.Application()
    app.router.add_route("*", "/{tail:.*}", handler)
    runner = web.AppRunner(app)
    await runner.setup()
    site = web.TCPSite(runner, "127.0.0.1", 0)
    await site.start()
    host, port = runner.addresses[0][:2]
    return runner, f"http://{host}:{port}"


@pytest_asyncio.fixture(loop_scope="function")
async def rest_url():
    """
    Return the URL of a server that serves only the visibility changes path.
    """

    async def handler(request: web.Request) -> web.Response:
        if request.path == "/scheduler/visibility-changes":
            return web.Response(text="o-1\t2026-10-01T00:00:00Z\n")
        return web.Response(status=404, text="Not Found")

    runner, url = await _serve(handler)
    try:
        yield url
    finally:
        await runner.cleanup()


@pytest_asyncio.fixture(loop_scope="function")
async def http_client():
    transport = RecordingTransport()
    async with httpx.AsyncClient(transport=transport) as client:
        client.gpp_transport = transport
        yield client


def _client(environment, http_client, *, rest_url="", ws=""):
    client = GPPClient(
        environment=environment, token=TEST_TOKEN, http_client=http_client
    )
    client.rest.base_url = rest_url or client.rest.base_url
    client.graphql.ws_url = ws or client.graphql.ws_url
    return client


@pytest.mark.parametrize("environment", ENVIRONMENTS)
@pytest.mark.asyncio
async def test_scheduler_gets_program_ids(environment, http_client):
    http_client.gpp_transport.respond(
        {"programs": {"matches": [{"id": "p-1", "reference": None}]}}
    )
    async with _client(environment, http_client) as client:
        result = await client.scheduler.get_program_ids(today="2026-10-01")

    assert result.programs.matches[0].id == "p-1"
    assert http_client.gpp_transport.bodies[0]["variables"] == {"today": "2026-10-01"}


@pytest.mark.parametrize("environment", ENVIRONMENTS)
@pytest.mark.asyncio
async def test_scheduler_gets_visibility_changes(environment, http_client, rest_url):
    async with _client(environment, http_client, rest_url=rest_url) as client:
        changes = await client.scheduler.get_visibility_changes(
            datetime(2026, 10, 1, tzinfo=UTC)
        )

    assert changes.observation_ids == {"o-1"}


@pytest.mark.parametrize("environment", ENVIRONMENTS)
@pytest.mark.asyncio
async def test_a_rest_path_the_environment_lacks_raises_naming_it(
    environment, http_client, rest_url
):
    async with _client(environment, http_client, rest_url=rest_url) as client:
        with pytest.raises(GPPEnvironmentError) as raised:
            await client.rest.get_atom_digests(["o-1"])

    assert raised.value.environment is environment
    assert raised.value.item == "/scheduler/atoms"


@pytest.mark.parametrize("environment", ENVIRONMENTS)
@pytest.mark.asyncio
async def test_scheduler_subscribes_to_calculation_updates(environment, http_client):
    gpp = SubscriptionServer(
        {
            "obscalcUpdate": {
                "oldCalculationState": "PENDING",
                "newCalculationState": "READY",
                "editType": "UPDATED",
                "value": None,
            }
        }
    )
    async with gpp() as server:
        async with _client(environment, http_client, ws=ws_url(server)) as client:
            events = [
                event
                async for event in client.scheduler.subscribe_to_calculation_updates()
            ]

    assert events[0].obscalc_update.new_calculation_state.value == "READY"
    assert gpp.subscribed[0]["operationName"] == "SchedulerObservationsUpdates"
    assert gpp.subscribed[0]["variables"] == {"executableOnly": True}
