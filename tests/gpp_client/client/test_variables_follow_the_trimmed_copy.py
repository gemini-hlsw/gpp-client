"""
Tests that a generated operation sends only the variables its environment's
copy declares.

The committed schemas drop no argument yet, so the client is built from
fixture schemas with the real build, and sends through the environment-aware
GraphQL client that ``GPPClient.graphql`` uses.
"""

import json

import httpx
import pytest

from gpp_client.environment import GPPEnvironment
from tests.gpp_client.fixture_build import build_fixture

_SCHEMAS = {
    "development": "type Query { programs(limit: Int, after: ID): [ID!]! }",
    "production": "type Query { programs(limit: Int): [ID!]! }",
}
_OPERATION = (
    "query listPrograms($limit: Int, $after: ID) "
    "{ programs(limit: $limit, after: $after) }"
)


@pytest.fixture(scope="module")
def fixture_build(tmp_path_factory):
    """
    Build a client whose ``listPrograms`` takes an argument production lacks.
    """
    return build_fixture(tmp_path_factory.mktemp("build"), _SCHEMAS, _OPERATION)


@pytest.fixture()
def client_class(fixture_build):
    with fixture_build.tables():
        yield fixture_build.client_class


def _recording(sent: list[dict]) -> httpx.MockTransport:
    def handler(request: httpx.Request) -> httpx.Response:
        sent.append(json.loads(request.content))
        return httpx.Response(200, json={"data": {"programs": []}})

    return httpx.MockTransport(handler)


async def _send(client_class, environment, call):
    sent: list[dict] = []
    async with httpx.AsyncClient(transport=_recording(sent)) as http_client:
        client = client_class(
            url="http://gpp.test/odb", http_client=http_client, environment=environment
        )
        await call(client)
    return sent[0]


@pytest.mark.asyncio
async def test_variable_the_copy_dropped_is_not_sent(client_class):
    body = await _send(
        client_class,
        GPPEnvironment.PRODUCTION,
        lambda client: client.list_programs(limit=1, after="p-1"),
    )

    assert body["variables"] == {"limit": 1}
    assert "$after" not in body["query"]


@pytest.mark.asyncio
async def test_environment_with_the_argument_receives_its_variable(client_class):
    body = await _send(
        client_class,
        GPPEnvironment.DEVELOPMENT,
        lambda client: client.list_programs(limit=1, after="p-1"),
    )

    assert body["variables"] == {"limit": 1, "after": "p-1"}


@pytest.mark.asyncio
async def test_raw_execute_sends_its_variables_as_given(client_class):
    body = await _send(
        client_class,
        GPPEnvironment.PRODUCTION,
        lambda client: client.execute(
            "query mine($limit: Int) { programs(limit: $limit) }",
            variables={"limit": 1, "after": "p-1"},
        ),
    )

    assert body["variables"] == {"limit": 1, "after": "p-1"}
