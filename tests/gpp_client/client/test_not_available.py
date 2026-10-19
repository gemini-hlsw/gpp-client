"""
Tests that a generated operation the selected environment lacks raises
``NotAvailable`` before anything is sent.

The client is built from fixture schemas with the real build, so the tests do
not depend on what is environment-specific in the committed schemas.
"""

import httpx
import pytest

from gpp_client.environment import GPPEnvironment
from gpp_client.exceptions import GPPError, NotAvailable
from tests.gpp_client.fixture_build import build_fixture
from tests.gpp_client.subscription_server import SubscriptionServer, ws_url

_PROGRAM = "type Program { id: ID! }\n"
_SCHEMAS = {
    "development": _PROGRAM
    + "type Query { program: Program draft: Program }\n"
    + "type Subscription { draftEdit: Program }\n",
    "production": _PROGRAM + "type Query { program: Program }\n",
}
_OPERATIONS = """
query getProgram { program { id } }
query getDraft { draft { id } }
subscription draftEdit { draftEdit { id } }
"""


@pytest.fixture(scope="module")
def built(tmp_path_factory):
    return build_fixture(tmp_path_factory.mktemp("build"), _SCHEMAS, _OPERATIONS)


@pytest.fixture()
def client_class(built):
    with built.tables():
        yield built.client_class


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
