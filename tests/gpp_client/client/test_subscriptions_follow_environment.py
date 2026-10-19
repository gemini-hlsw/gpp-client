"""
Tests that subscriptions follow the selected environment like queries do.

A local ``websockets`` server speaks the graphql-transport-ws protocol, so the
client runs its real websocket code offline. The committed schemas have no
environment-specific subscription, so the client is built from fixture schemas
with the real build.
"""

import pytest

from gpp_client.environment import GPPEnvironment
from tests.gpp_client.fixture_build import build_fixture
from tests.gpp_client.subscription_server import SubscriptionServer, ws_url

_DEVELOPMENT = """
type Query { program: Program }
type Program { id: ID! }
type Subscription {
  programEdit(includeDeleted: Boolean): Program
  draftEdit: Program
}
"""

_SCHEMAS = {
    "development": _DEVELOPMENT,
    "production": """
type Query { program: Program }
type Program { id: ID! reference: String }
type Subscription { programEdit: Program }
""",
}

_OPERATIONS = """
subscription programEdit($includeDeleted: Boolean) {
  programEdit(includeDeleted: $includeDeleted) { id reference }
}
subscription draftEdit { draftEdit { id } }
"""


@pytest.fixture(scope="module")
def fixture_build(tmp_path_factory):
    """
    Build a client whose subscriptions differ between environments.
    """
    return build_fixture(tmp_path_factory.mktemp("build"), _SCHEMAS, _OPERATIONS)


@pytest.fixture()
def client_class(fixture_build):
    generated = fixture_build.client_class

    def client(**kwargs):
        return generated(url="http://gpp.test/odb", **kwargs)

    with fixture_build.tables():
        yield client


@pytest.mark.asyncio
async def test_development_subscribes_with_its_trimmed_copy(client_class):
    gpp = SubscriptionServer({"programEdit": {"id": "p-1"}})
    async with gpp() as server:
        client = client_class(
            environment=GPPEnvironment.DEVELOPMENT, ws_url=ws_url(server)
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
