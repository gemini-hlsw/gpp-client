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
    "development": f"# schema-commit: {'d' * 40}\n"
    + _QUERY
    + "type Program { id: ID! draft: String }\n"
    + _SUBSCRIPTION,
    "production": _QUERY + "type Program { id: ID! }\n" + _SUBSCRIPTION,
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
    Answer every GraphQL request with one canned JSON body, and ``/health``
    with ``health``, recording what was sent and how often health was asked.
    """

    def __init__(
        self, status: int = 200, health: httpx.Response | None = None, **body
    ) -> None:
        super().__init__(self._handle)
        self.status = status
        self.body = body
        self.health = health or httpx.Response(
            200, json={"status": "ok", "commit": "c" * 40}
        )
        self.sent: list[dict] = []
        self.health_requests: list[httpx.Request] = []

    def _handle(self, request: httpx.Request) -> httpx.Response:
        if request.url.path == "/health":
            self.health_requests.append(request)
            return self.health
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
    assert gpp.health_requests == []


@pytest.mark.asyncio
async def test_a_rejected_request_names_gpp_messages_and_both_commits(client_class):
    gpp = _GPP(
        status=422,
        errors=[
            {"message": "No field 'nope' for type Program"},
            {"message": "Unknown argument 'x'"},
        ],
    )

    async with httpx.AsyncClient(transport=gpp) as http_client:
        client = client_class(
            url="http://gpp.test/odb",
            http_client=http_client,
            environment=GPPEnvironment.DEVELOPMENT,
        )
        with pytest.raises(GPPHttpError) as raised:
            await client.execute("query { program { id nope } }")

    assert raised.value.status_code == 422
    assert str(raised.value) == (
        "GPP development answered HTTP 422: No field 'nope' for type Program; "
        "Unknown argument 'x' (GPP development runs commit ccccccc; this "
        "client was built from its schema at commit ddddddd)"
    )
    assert [str(r.url) for r in gpp.health_requests] == ["http://gpp.test/health"]


@pytest.mark.asyncio
@pytest.mark.parametrize(
    "health",
    [
        httpx.Response(503),
        httpx.Response(200, text="<html>"),
        httpx.Response(200, json={"status": "ok", "commit": 12345678}),
        httpx.Response(200, json=["ok"]),
    ],
    ids=["error status", "not json", "commit not a string", "not an object"],
)
async def test_a_rejected_request_still_raises_when_commits_are_unknown(
    client_class, health
):
    gpp = _GPP(status=422, health=health, errors=[{"message": "No field 'nope'"}])

    async with httpx.AsyncClient(transport=gpp) as http_client:
        client = client_class(
            url="http://gpp.test/odb",
            http_client=http_client,
            environment=GPPEnvironment.PRODUCTION,
        )
        with pytest.raises(GPPHttpError) as raised:
            await client.get_program()

    assert str(raised.value) == (
        "GPP production answered HTTP 422: No field 'nope' (GPP production runs "
        "commit unknown; this client was built from its schema at commit unknown)"
    )


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


@pytest.mark.asyncio
@pytest.mark.parametrize("status", [401, 403])
async def test_a_refused_token_names_gpp_message_without_commits(client_class, status):
    gpp = _GPP(status=status, errors=[{"message": "Access denied"}])

    async with httpx.AsyncClient(transport=gpp) as http_client:
        client = client_class(
            url="http://gpp.test/odb",
            http_client=http_client,
            environment=GPPEnvironment.DEVELOPMENT,
        )
        with pytest.raises(GPPHttpError) as raised:
            await client.get_program()

    assert str(raised.value) == (
        f"GPP development answered HTTP {status}: Access denied"
    )
    assert gpp.health_requests == []
