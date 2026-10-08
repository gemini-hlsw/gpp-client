"""
Tests that calling something the selected environment lacks raises before sending.

Tests build a tiny client from fixture schemas with the real build, so they do
not depend on what is environment-specific in the committed schemas. Most call
it through the environment-aware GraphQL client that ``GPPClient.graphql``
uses; the ``GPPClient`` tests call the fixture's generated methods on a real
``GPPClient``.
"""

import json

import httpx
import pytest

from gpp_client import GPPClient
from gpp_client.environment import GPPEnvironment
from gpp_client.exceptions import GPPEnvironmentError
from tests.gpp_client.fixture_build import build_fixture

_SHARED = """
type Program { id: ID! }
type Mutation { updateProgram(input: UpdateInput!): Program }
"""

_SCHEMAS = {
    "development": _SHARED
    + """
type Query {
  program(id: ID!, includeDeleted: Boolean): Program
  draft: Program
}
enum Kind { SCIENCE ENGINEERING CALIBRATION }
input ItemInput { kind: Kind }
input UpdateInput {
  name: String
  note: String
  owner: String
  kind: Kind
  items: [ItemInput!]
}
""",
    "production": _SHARED
    + """
type Query { program(id: ID!): Program }
enum Kind { SCIENCE ENGINEERING }
input ItemInput { kind: Kind }
input UpdateInput {
  name: String
  owner: String!
  kind: Kind
  items: [ItemInput!]
}
""",
}

_OPERATIONS = """
query getProgram($id: ID!, $includeDeleted: Boolean) {
  program(id: $id, includeDeleted: $includeDeleted) { id }
}
query getDraft { draft { id } }
mutation updateProgram($input: UpdateInput!) {
  updateProgram(input: $input) { id }
}
"""


@pytest.fixture(scope="module")
def built_package(tmp_path_factory):
    """
    Build a client whose operations and inputs differ between environments.
    """
    return build_fixture(tmp_path_factory.mktemp("build"), _SCHEMAS, _OPERATIONS)


@pytest.fixture()
def fixture_build(built_package):
    with built_package.tables():
        yield (
            built_package.client_class,
            built_package,
            built_package.module("input_types"),
            built_package.module("enums"),
        )


class _Recorder:
    def __init__(self) -> None:
        self.sent: list[dict] = []

    def transport(self, data: dict) -> httpx.MockTransport:
        def handler(request: httpx.Request) -> httpx.Response:
            self.sent.append(json.loads(request.content))
            return httpx.Response(200, json={"data": data})

        return httpx.MockTransport(handler)


@pytest.fixture()
def recorder() -> _Recorder:
    return _Recorder()


async def _call_on_gpp_client(fixture_build, transport, method, **kwargs):
    """
    Call a generated method of the fixture build on a real production GPPClient.
    """
    _, built, _, _ = fixture_build
    generated = getattr(built.module("client").GraphQLClient, method)
    async with httpx.AsyncClient(transport=transport) as http_client:
        async with GPPClient(
            environment="production", token="test-token", http_client=http_client
        ) as client:
            return await generated(client.graphql, **kwargs)


def _client(fixture_build, http_client, environment):
    client_class, _, _, _ = fixture_build
    return client_class(
        url="http://gpp.test/odb",
        http_client=http_client,
        environment=environment,
    )


@pytest.mark.asyncio
async def test_production_raises_for_a_development_only_operation(
    fixture_build, recorder
):
    async with httpx.AsyncClient(
        transport=recorder.transport({"draft": {"id": "p-1"}})
    ) as http_client:
        client = _client(fixture_build, http_client, GPPEnvironment.PRODUCTION)
        with pytest.raises(GPPEnvironmentError) as raised:
            await client.get_draft()

    assert recorder.sent == []
    error = raised.value
    assert error.item == "getDraft"
    assert error.environment is GPPEnvironment.PRODUCTION
    assert error.available == (GPPEnvironment.DEVELOPMENT,)


@pytest.mark.asyncio
async def test_production_raises_for_a_set_development_only_input_field(
    fixture_build, recorder
):
    _, _, inputs, _ = fixture_build
    async with httpx.AsyncClient(
        transport=recorder.transport({"updateProgram": {"id": "p-1"}})
    ) as http_client:
        client = _client(fixture_build, http_client, GPPEnvironment.PRODUCTION)
        with pytest.raises(GPPEnvironmentError) as raised:
            await client.update_program(
                input=inputs.UpdateInput(owner="me", note="draft")
            )

    assert recorder.sent == []
    assert raised.value.item == "UpdateInput.note"
    assert raised.value.kind == "input field"
    assert raised.value.available == (GPPEnvironment.DEVELOPMENT,)


@pytest.mark.asyncio
async def test_development_sends_its_input_field(fixture_build, recorder):
    _, _, inputs, _ = fixture_build
    async with httpx.AsyncClient(
        transport=recorder.transport({"updateProgram": {"id": "p-1"}})
    ) as http_client:
        client = _client(fixture_build, http_client, GPPEnvironment.DEVELOPMENT)
        await client.update_program(input=inputs.UpdateInput(note="draft"))

    assert recorder.sent[0]["variables"] == {"input": {"note": "draft"}}


@pytest.mark.asyncio
async def test_gpp_client_on_production_raises_for_a_development_only_input_field(
    fixture_build, gpp_transport
):
    _, _, inputs, _ = fixture_build
    with pytest.raises(GPPEnvironmentError) as raised:
        await _call_on_gpp_client(
            fixture_build,
            gpp_transport,
            "update_program",
            input=inputs.UpdateInput(owner="me", note="draft"),
        )

    assert gpp_transport.requests == []
    assert raised.value.item == "UpdateInput.note"
    assert raised.value.environment is GPPEnvironment.PRODUCTION
    assert raised.value.available == (GPPEnvironment.DEVELOPMENT,)


@pytest.mark.asyncio
async def test_production_raises_for_a_development_only_enum_value_in_a_list(
    fixture_build, recorder
):
    _, _, inputs, enums = fixture_build
    async with httpx.AsyncClient(
        transport=recorder.transport({"updateProgram": {"id": "p-1"}})
    ) as http_client:
        client = _client(fixture_build, http_client, GPPEnvironment.PRODUCTION)
        with pytest.raises(GPPEnvironmentError) as raised:
            await client.update_program(
                input=inputs.UpdateInput(
                    owner="me",
                    items=[
                        inputs.ItemInput(kind=enums.Kind.SCIENCE),
                        inputs.ItemInput(kind=enums.Kind.CALIBRATION),
                    ],
                )
            )

    assert recorder.sent == []
    assert raised.value.item == "Kind.CALIBRATION"
    assert raised.value.kind == "enum value"
    assert raised.value.available == (GPPEnvironment.DEVELOPMENT,)


@pytest.mark.asyncio
async def test_production_raises_for_a_set_development_only_argument(
    fixture_build, recorder
):
    async with httpx.AsyncClient(
        transport=recorder.transport({"program": {"id": "p-1"}})
    ) as http_client:
        client = _client(fixture_build, http_client, GPPEnvironment.PRODUCTION)
        with pytest.raises(GPPEnvironmentError) as raised:
            await client.get_program(id="p-1", include_deleted=True)

    assert recorder.sent == []
    assert raised.value.item == "Query.program(includeDeleted:)"
    assert raised.value.kind == "argument"
    assert raised.value.available == (GPPEnvironment.DEVELOPMENT,)


@pytest.mark.asyncio
async def test_production_sends_when_a_development_only_argument_is_unset(
    fixture_build, recorder
):
    async with httpx.AsyncClient(
        transport=recorder.transport({"program": {"id": "p-1"}})
    ) as http_client:
        client = _client(fixture_build, http_client, GPPEnvironment.PRODUCTION)
        result = await client.get_program(id="p-1")

    assert result.program.id == "p-1"
    assert "includeDeleted" not in recorder.sent[0]["query"]


@pytest.mark.asyncio
async def test_production_does_not_send_a_variable_its_trimmed_query_dropped(
    fixture_build, recorder
):
    async with httpx.AsyncClient(
        transport=recorder.transport({"program": {"id": "p-1"}})
    ) as http_client:
        client = _client(fixture_build, http_client, GPPEnvironment.PRODUCTION)
        await client.get_program(id="p-1", include_deleted=None)

    assert recorder.sent[0]["variables"] == {"id": "p-1"}


@pytest.mark.asyncio
async def test_development_sends_a_variable_its_query_declares(fixture_build, recorder):
    async with httpx.AsyncClient(
        transport=recorder.transport({"program": {"id": "p-1"}})
    ) as http_client:
        client = _client(fixture_build, http_client, GPPEnvironment.DEVELOPMENT)
        await client.get_program(id="p-1", include_deleted=None)

    assert recorder.sent[0]["variables"] == {"id": "p-1", "includeDeleted": None}


@pytest.mark.parametrize("owner", [{}, {"owner": None}], ids=["unset", "none"])
@pytest.mark.asyncio
async def test_production_raises_for_an_input_field_it_requires_left_unset(
    fixture_build, recorder, owner
):
    _, _, inputs, _ = fixture_build
    async with httpx.AsyncClient(
        transport=recorder.transport({"updateProgram": {"id": "p-1"}})
    ) as http_client:
        client = _client(fixture_build, http_client, GPPEnvironment.PRODUCTION)
        with pytest.raises(GPPEnvironmentError) as raised:
            await client.update_program(input=inputs.UpdateInput(name="n", **owner))

    assert recorder.sent == []
    assert raised.value.item == "UpdateInput.owner"
    assert raised.value.kind == "input field"
    assert raised.value.required is True
    assert raised.value.environment is GPPEnvironment.PRODUCTION
    assert raised.value.available == (GPPEnvironment.DEVELOPMENT,)
    assert "required on production" in str(raised.value)


@pytest.mark.asyncio
async def test_development_sends_without_an_input_field_only_production_requires(
    fixture_build, recorder
):
    _, _, inputs, _ = fixture_build
    async with httpx.AsyncClient(
        transport=recorder.transport({"updateProgram": {"id": "p-1"}})
    ) as http_client:
        client = _client(fixture_build, http_client, GPPEnvironment.DEVELOPMENT)
        await client.update_program(input=inputs.UpdateInput(name="n"))

    assert recorder.sent[0]["variables"] == {"input": {"name": "n"}}


@pytest.mark.asyncio
async def test_gpp_client_on_production_raises_for_a_development_only_enum_value(
    fixture_build, gpp_transport
):
    _, _, inputs, enums = fixture_build
    with pytest.raises(GPPEnvironmentError) as raised:
        await _call_on_gpp_client(
            fixture_build,
            gpp_transport,
            "update_program",
            input=inputs.UpdateInput(owner="me", kind=enums.Kind.CALIBRATION),
        )

    assert gpp_transport.requests == []
    assert raised.value.item == "Kind.CALIBRATION"


@pytest.mark.asyncio
async def test_gpp_client_on_production_sends_what_production_has(
    fixture_build, gpp_transport
):
    _, _, inputs, _ = fixture_build
    gpp_transport.respond({"updateProgram": {"id": "p-1"}})

    result = await _call_on_gpp_client(
        fixture_build,
        gpp_transport,
        "update_program",
        input=inputs.UpdateInput(owner="me"),
    )

    assert result.update_program.id == "p-1"
    assert gpp_transport.bodies[0]["variables"] == {"input": {"owner": "me"}}


def test_generated_base_client_converts_variables_as_the_checks_expect(
    fixture_build,
):
    # The checks call this private ariadne-codegen method to see the variables
    # as sent; an upgrade that renames or changes it must fail here.
    from gpp_client.generated.async_base_client import AsyncBaseClient
    from gpp_client.generated.base_model import UNSET

    _, _, inputs, enums = fixture_build

    converted = AsyncBaseClient(
        url="http://gpp.test/odb"
    )._convert_dict_to_json_serializable(
        {
            "input": inputs.UpdateInput(owner="o-1"),
            "items": [inputs.ItemInput(kind=enums.Kind.SCIENCE)],
            "unset": UNSET,
            "none": None,
        }
    )

    assert converted == {
        "input": {"owner": "o-1"},
        "items": [{"kind": "SCIENCE"}],
        "none": None,
    }
