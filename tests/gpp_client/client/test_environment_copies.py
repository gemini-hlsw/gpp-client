"""
Tests that each environment receives its own copy of an operation.

The committed schemas have little that is environment-specific, so the client
is built from fixture schemas with the real build, and sends through the
environment-aware GraphQL client that ``GPPClient.graphql`` uses.
"""

import asyncio
import json

import httpx
import pytest

from gpp_client.constants import DEVELOPMENT_URL, PRODUCTION_URL
from gpp_client.environment import GPPEnvironment
from gpp_client.exceptions import GPPError, NotAvailable
from tests.gpp_client.conftest import RecordingTransport
from tests.gpp_client.fixture_build import build_fixture
from tests.gpp_client.subscription_server import SubscriptionServer, ws_url

_SCHEMAS = {
    "development": """
type Program { id: ID! }
type Query {
  program: Program
  draft: Program
  programs(limit: Int, after: ID): [ID!]!
}
type Subscription {
  programEdit(includeDeleted: Boolean): Program
  draftEdit: Program
}
""",
    "production": """
type Program { id: ID! reference: String }
type Query { program: Program programs(limit: Int): [ID!]! }
type Subscription { programEdit: Program }
""",
}
_OPERATIONS = """
query getProgram { program { id reference } }
query getDraft { draft { id } }
query listPrograms($limit: Int, $after: ID) {
  programs(limit: $limit, after: $after)
}
subscription programEdit($includeDeleted: Boolean) {
  programEdit(includeDeleted: $includeDeleted) { id reference }
}
subscription draftEdit { draftEdit { id } }
"""


@pytest.fixture(scope="module")
def fixture_build(tmp_path_factory):
    return build_fixture(tmp_path_factory.mktemp("build"), _SCHEMAS, _OPERATIONS)


@pytest.fixture()
def client_class(fixture_build):
    with fixture_build.tables():
        yield fixture_build.client_class


async def _send(client_class, environment, response, call):
    sent: list[dict] = []

    def handler(request: httpx.Request) -> httpx.Response:
        sent.append(json.loads(request.content))
        return httpx.Response(200, json={"data": response})

    async with httpx.AsyncClient(transport=httpx.MockTransport(handler)) as http:
        client = client_class(
            url="http://gpp.test/odb", http_client=http, environment=environment
        )
        result = await call(client)
    return result, sent[0]


@pytest.mark.asyncio
async def test_development_reads_none_for_a_production_only_field(client_class):
    result, body = await _send(
        client_class,
        GPPEnvironment.DEVELOPMENT,
        {"program": {"id": "p-1"}},
        lambda client: client.get_program(),
    )

    assert result.program.id == "p-1"
    assert result.program.reference is None
    assert body["query"] == "query getProgram {\n  program {\n    id\n  }\n}"


@pytest.mark.asyncio
async def test_production_receives_and_reads_its_field(client_class):
    result, body = await _send(
        client_class,
        GPPEnvironment.PRODUCTION,
        {"program": {"id": "p-1", "reference": "G-1"}},
        lambda client: client.get_program(),
    )

    assert result.program.reference == "G-1"
    assert "reference" in body["query"]


@pytest.mark.asyncio
async def test_two_clients_on_different_environments_at_once(client_class) -> None:
    gpp = RecordingTransport()
    gpp.respond({"program": None})
    gpp.respond({"program": None})

    async with httpx.AsyncClient(transport=gpp) as http_client:
        development = client_class(
            url=f"{DEVELOPMENT_URL}/odb",
            http_client=http_client,
            environment=GPPEnvironment.DEVELOPMENT,
            headers={"Authorization": "Bearer d"},
        )
        production = client_class(
            url=f"{PRODUCTION_URL}/odb",
            http_client=http_client,
            environment=GPPEnvironment.PRODUCTION,
            headers={"Authorization": "Bearer p"},
        )
        await asyncio.gather(development.get_program(), production.get_program())

    sent = {
        str(request.url): (request.headers["Authorization"], body["query"])
        for request, body in zip(gpp.requests, gpp.bodies, strict=True)
    }
    assert sent[f"{DEVELOPMENT_URL}/odb"][0] == "Bearer d"
    assert "reference" not in sent[f"{DEVELOPMENT_URL}/odb"][1]
    assert sent[f"{PRODUCTION_URL}/odb"][0] == "Bearer p"
    assert "reference" in sent[f"{PRODUCTION_URL}/odb"][1]


@pytest.mark.asyncio
async def test_variable_the_copy_dropped_is_not_sent(client_class):
    _, body = await _send(
        client_class,
        GPPEnvironment.PRODUCTION,
        {"programs": []},
        lambda client: client.list_programs(limit=1, after="p-1"),
    )

    assert body["variables"] == {"limit": 1}
    assert "$after" not in body["query"]


@pytest.mark.asyncio
async def test_environment_with_the_argument_receives_its_variable(client_class):
    _, body = await _send(
        client_class,
        GPPEnvironment.DEVELOPMENT,
        {"programs": []},
        lambda client: client.list_programs(limit=1, after="p-1"),
    )

    assert body["variables"] == {"limit": 1, "after": "p-1"}


@pytest.mark.asyncio
async def test_raw_execute_sends_its_variables_as_given(client_class):
    _, body = await _send(
        client_class,
        GPPEnvironment.PRODUCTION,
        {"programs": []},
        lambda client: client.execute(
            "query mine($limit: Int) { programs(limit: $limit) }",
            variables={"limit": 1, "after": "p-1"},
        ),
    )

    assert body["variables"] == {"limit": 1, "after": "p-1"}


@pytest.mark.asyncio
async def test_a_missing_operation_raises_not_available_with_nothing_sent(
    client_class,
):
    requests: list[httpx.Request] = []

    def handler(request: httpx.Request) -> httpx.Response:
        requests.append(request)
        return httpx.Response(200, json={"data": {"draft": None}})

    async with httpx.AsyncClient(transport=httpx.MockTransport(handler)) as http:
        client = client_class(
            url="http://gpp.test/odb",
            http_client=http,
            environment=GPPEnvironment.PRODUCTION,
        )
        with pytest.raises(NotAvailable) as raised:
            await client.get_draft()

    assert requests == []
    assert isinstance(raised.value, GPPError)
    assert raised.value.item == "getDraft"
    assert raised.value.environment is GPPEnvironment.PRODUCTION
    assert raised.value.available == (GPPEnvironment.DEVELOPMENT,)
    assert str(raised.value) == (
        "The operation getDraft is not available on production. It is available "
        "on development. Nothing was sent."
    )


@pytest.mark.asyncio
async def test_development_subscribes_with_its_trimmed_copy(client_class):
    gpp = SubscriptionServer({"programEdit": {"id": "p-1"}})
    async with gpp() as server:
        client = client_class(
            url="http://gpp.test/odb",
            environment=GPPEnvironment.DEVELOPMENT,
            ws_url=ws_url(server),
        )
        events = [event async for event in client.program_edit()]

    assert gpp.subscribed[0]["query"] == (
        "subscription programEdit($includeDeleted: Boolean) {\n"
        "  programEdit(includeDeleted: $includeDeleted) {\n"
        "    id\n"
        "  }\n"
        "}"
    )
    assert events[0].program_edit.id == "p-1"
    assert events[0].program_edit.reference is None


@pytest.mark.asyncio
async def test_a_missing_subscription_raises_not_available_before_connecting(
    client_class,
):
    gpp = SubscriptionServer({"draftEdit": {"id": "p-1"}})
    async with gpp() as server:
        client = client_class(
            url="http://gpp.test/odb",
            environment=GPPEnvironment.PRODUCTION,
            ws_url=ws_url(server),
        )
        with pytest.raises(NotAvailable) as raised:
            [event async for event in client.draft_edit()]

    assert gpp.connections == 0
    assert raised.value.item == "draftEdit"
