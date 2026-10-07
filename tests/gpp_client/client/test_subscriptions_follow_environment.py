"""
Tests that subscriptions follow the selected environment like queries do.

A local ``websockets`` server speaks the graphql-transport-ws protocol, so the
client runs its real websocket code offline. The committed schemas have no
environment-specific subscription, so the client is built from fixture schemas
with the real build.
"""

import warnings

import pytest

from gpp_client.environment import GPPEnvironment
from gpp_client.exceptions import GPPEnvironmentError, GPPFieldLeavingWarning
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
type Program { id: ID! reference: String label: String }
type Subscription { programEdit: Program }
""",
}

_OPERATIONS = """
subscription programEdit($includeDeleted: Boolean) {
  programEdit(includeDeleted: $includeDeleted) { id reference }
}
subscription draftEdit { draftEdit { id } }
subscription programLabel { programEdit { id label } }
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


@pytest.mark.asyncio
async def test_production_raises_before_connecting_for_a_development_only_subscription(
    client_class,
):
    gpp = SubscriptionServer({"draftEdit": {"id": "p-1"}})
    async with gpp() as server:
        client = client_class(
            environment=GPPEnvironment.PRODUCTION, ws_url=ws_url(server)
        )
        with pytest.raises(GPPEnvironmentError) as raised:
            [event async for event in client.draft_edit()]

    assert gpp.connections == 0
    assert raised.value.item == "draftEdit"
    assert raised.value.kind == "operation"
    assert raised.value.available == (GPPEnvironment.DEVELOPMENT,)


@pytest.mark.asyncio
async def test_production_raises_before_connecting_for_a_development_only_argument(
    client_class,
):
    gpp = SubscriptionServer({"programEdit": {"id": "p-1"}})
    async with gpp() as server:
        client = client_class(
            environment=GPPEnvironment.PRODUCTION, ws_url=ws_url(server)
        )
        with pytest.raises(GPPEnvironmentError) as raised:
            [event async for event in client.program_edit(include_deleted=True)]

    assert gpp.connections == 0
    assert raised.value.item == "Subscription.programEdit(includeDeleted:)"
    assert raised.value.kind == "argument"


@pytest.mark.asyncio
async def test_production_does_not_subscribe_with_a_variable_its_copy_dropped(
    client_class,
):
    gpp = SubscriptionServer({"programEdit": {"id": "p-1", "reference": "G-1"}})
    async with gpp() as server:
        client = client_class(
            environment=GPPEnvironment.PRODUCTION, ws_url=ws_url(server)
        )
        events = [event async for event in client.program_edit(include_deleted=None)]

    assert "variables" not in gpp.subscribed[0]
    assert "includeDeleted" not in gpp.subscribed[0]["query"]
    assert events[0].program_edit.reference == "G-1"


@pytest.mark.asyncio
async def test_production_warns_once_for_a_leaving_field_a_subscription_selects(
    client_class,
):
    # Each leaving field warns once per process, so only this test selects label.
    gpp = SubscriptionServer({"programEdit": {"id": "p-1", "label": "L"}})
    async with gpp() as server:
        client = client_class(
            environment=GPPEnvironment.PRODUCTION, ws_url=ws_url(server)
        )
        with warnings.catch_warnings(record=True) as caught:
            warnings.simplefilter("always")
            for _ in range(2):
                [event async for event in client.program_label()]

    leaving = [w.message for w in caught if w.category is GPPFieldLeavingWarning]
    assert [(w.field, w.environment) for w in leaving] == [
        ("Program.label", GPPEnvironment.PRODUCTION)
    ]
    assert [w.filename for w in caught if w.category is GPPFieldLeavingWarning] == [
        __file__
    ]
