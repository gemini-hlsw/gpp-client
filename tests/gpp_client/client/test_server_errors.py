"""
Tests that a raw document reaches GPP unchanged and that GPP's answer, when it
is an error, is raised as a ``GPPError`` naming the environment.

The client is built from fixture schemas with the real build.
"""

import json

import httpx
import pytest

from gpp_client.environment import GPPEnvironment
from gpp_client.exceptions import (
    GPPError,
    GPPGraphQLError,
    GPPHttpError,
    GPPTransportError,
)
from gpp_client.generated.exceptions import (
    GraphQLClientError,
    GraphQLClientGraphQLMultiError,
    GraphQLClientHttpError,
)
from tests.gpp_client.fixture_build import build_fixture
from tests.gpp_client.subscription_server import SubscriptionServer, ws_url

_QUERY = "type Query { program: Program }\n"
_SUBSCRIPTION = "type Subscription { programEdit: Program }\n"
_SCHEMAS = {
    "development": "# schema-date: 2024-05-06\n"
    + _QUERY
    + "type Program { id: ID! draft: String }\n"
    + _SUBSCRIPTION,
    "production": "# schema-date: 2024-01-02\n"
    + _QUERY
    + "type Program { id: ID! }\n"
    + _SUBSCRIPTION,
}


@pytest.fixture(scope="module")
def built(tmp_path_factory):
    return build_fixture(
        tmp_path_factory.mktemp("build"),
        _SCHEMAS,
        "query getProgram { program { id } }\n"
        "subscription programEdit { programEdit { id } }",
    )


@pytest.fixture()
def client_class(built):
    with built.tables():
        yield built.client_class


class _GPP(httpx.MockTransport):
    """
    Answer every request with one canned JSON body and record what was sent.
    """

    def __init__(self, status: int = 200, **body) -> None:
        super().__init__(self._handle)
        self.status = status
        self.body = body
        self.sent: list[dict] = []

    def _handle(self, request: httpx.Request) -> httpx.Response:
        self.sent.append(json.loads(request.content))
        return httpx.Response(self.status, json=self.body)


@pytest.mark.asyncio
async def test_raw_document_is_sent_unchanged_and_a_validation_error_names_the_environment(
    client_class,
):
    document = "query   anything {\n  program { id   nope }\n}"
    gpp = _GPP(
        data=None,
        errors=[{"message": "Cannot query field 'nope' on type 'Program'."}],
    )

    async with httpx.AsyncClient(transport=gpp) as http_client:
        client = client_class(
            url="http://gpp.test/odb",
            http_client=http_client,
            environment=GPPEnvironment.DEVELOPMENT,
        )
        with pytest.raises(GPPError) as raised:
            await client.execute(document, variables={"x": 1})

    assert gpp.sent[0]["query"] == document
    assert gpp.sent[0]["variables"] == {"x": 1}
    assert str(raised.value) == (
        "GPP development returned errors: Cannot query field 'nope' on type 'Program'."
    )


@pytest.mark.asyncio
async def test_raw_document_selecting_what_the_environment_lacks_is_still_sent(
    client_class,
):
    document = "query { program { id draft } }"
    gpp = _GPP(data={"program": {"id": "p-1", "draft": None}})

    async with httpx.AsyncClient(transport=gpp) as http_client:
        client = client_class(
            url="http://gpp.test/odb",
            http_client=http_client,
            environment=GPPEnvironment.PRODUCTION,
        )
        response = await client.execute(document)

    assert gpp.sent[0]["query"] == document
    assert client.get_data(response) == {"program": {"id": "p-1", "draft": None}}


@pytest.mark.asyncio
async def test_a_partial_response_raises_with_its_data_attached(client_class):
    gpp = _GPP(
        data={"program": {"id": "p-1"}},
        errors=[{"message": "draft: not authorised", "path": ["program", "draft"]}],
    )

    async with httpx.AsyncClient(transport=gpp) as http_client:
        client = client_class(
            url="http://gpp.test/odb",
            http_client=http_client,
            environment=GPPEnvironment.DEVELOPMENT,
        )
        with pytest.raises(GPPGraphQLError) as raised:
            await client.get_program()

    assert raised.value.data == {"program": {"id": "p-1"}}
    assert [error.path for error in raised.value.errors] == [["program", "draft"]]
    assert isinstance(raised.value, GraphQLClientGraphQLMultiError)


@pytest.mark.asyncio
async def test_an_http_error_names_the_environment_and_keeps_the_status(client_class):
    gpp = _GPP(status=503, error="unavailable")

    async with httpx.AsyncClient(transport=gpp) as http_client:
        client = client_class(
            url="http://gpp.test/odb",
            http_client=http_client,
            environment=GPPEnvironment.PRODUCTION,
        )
        with pytest.raises(GPPHttpError) as raised:
            await client.get_program()

    assert raised.value.status_code == 503
    assert raised.value.response.status_code == 503
    assert isinstance(raised.value, GraphQLClientHttpError)
    assert str(raised.value) == "GPP production answered HTTP 503"


@pytest.mark.asyncio
async def test_a_connection_failure_names_the_environment(client_class):
    def refuse(request: httpx.Request) -> httpx.Response:
        raise httpx.ConnectError("Connection refused", request=request)

    async with httpx.AsyncClient(transport=httpx.MockTransport(refuse)) as http:
        client = client_class(
            url="http://gpp.test/odb",
            http_client=http,
            environment=GPPEnvironment.DEVELOPMENT,
        )
        with pytest.raises(GPPTransportError) as raised:
            await client.get_program()

    assert isinstance(raised.value, GraphQLClientError)
    assert isinstance(raised.value.__cause__, httpx.ConnectError)
    assert str(raised.value) == (
        "GPP development could not be reached: Connection refused"
    )


@pytest.mark.asyncio
async def test_a_response_that_is_not_graphql_names_the_environment(client_class):
    def html(request: httpx.Request) -> httpx.Response:
        return httpx.Response(200, text="<html>maintenance</html>")

    async with httpx.AsyncClient(transport=httpx.MockTransport(html)) as http:
        client = client_class(
            url="http://gpp.test/odb",
            http_client=http,
            environment=GPPEnvironment.DEVELOPMENT,
        )
        with pytest.raises(GPPTransportError) as raised:
            await client.get_program()

    assert str(raised.value) == "GPP development sent a response that is not GraphQL"


@pytest.mark.asyncio
async def test_a_subscription_error_names_the_environment(client_class):
    gpp = SubscriptionServer({}, errors=[{"message": "draft: not authorised"}])
    async with gpp() as server:
        client = client_class(
            url="http://gpp.test/odb",
            environment=GPPEnvironment.DEVELOPMENT,
            ws_url=ws_url(server),
        )
        with pytest.raises(GPPGraphQLError) as raised:
            [event async for event in client.program_edit()]

    assert [error.message for error in raised.value.errors] == ["draft: not authorised"]
    assert str(raised.value) == (
        "GPP development returned errors: draft: not authorised"
    )


@pytest.mark.asyncio
async def test_a_subscription_that_cannot_connect_names_the_environment(
    client_class,
):
    gpp = SubscriptionServer({})
    async with gpp() as server:
        closed_url = ws_url(server)
    client = client_class(
        url="http://gpp.test/odb",
        environment=GPPEnvironment.DEVELOPMENT,
        ws_url=closed_url,
    )

    with pytest.raises(GPPTransportError) as raised:
        [event async for event in client.program_edit()]

    assert isinstance(raised.value.__cause__, OSError)
    assert str(raised.value).startswith("GPP development could not be reached: ")
