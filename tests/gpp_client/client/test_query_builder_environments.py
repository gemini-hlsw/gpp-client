"""
Tests that a query-builder call is checked against the selected environment.

A document that is not a generated operation, such as one built with
``client.graphql.query(...)``, is validated against the selected environment's
schema before sending. Tests build a tiny client from fixture schemas with
the real build, so they do not depend on what is environment-specific in the
committed schemas; two send the fixture's query-builder calls through a real
``GPPClient``.
"""

import json
import warnings

import httpx
import pytest

from gpp_client import GPPClient
from gpp_client.environment import GPPEnvironment
from gpp_client.exceptions import (
    EnvironmentItemKind,
    GPPEnvironmentError,
    GPPFieldLeavingWarning,
)
from tests.gpp_client.fixture_build import build_fixture

_SCHEMAS = {
    "development": """
type Query {
  program(id: ID!, includeDeleted: Boolean): Program
  draft: Program
}
type Mutation { updateProgram(input: UpdateInput!): Program }
type Program { id: ID! name: String draftNote: String }
enum Kind { SCIENCE ENGINEERING CALIBRATION }
input UpdateInput { name: String note: String owner: String kind: Kind }
""",
    "production": """
type Query { program(id: ID!): Program }
type Mutation { updateProgram(input: UpdateInput!): Program }
type Program { id: ID! name: String legacy: Int }
enum Kind { SCIENCE ENGINEERING }
input UpdateInput { name: String owner: String! kind: Kind }
""",
}

_OPERATIONS = "query getProgram($id: ID!) { program(id: $id) { id } }\n"


@pytest.fixture(scope="module")
def built_package(tmp_path_factory):
    """
    Build a client whose schema differs between environments.
    """
    return build_fixture(tmp_path_factory.mktemp("build"), _SCHEMAS, _OPERATIONS)


@pytest.fixture()
def generated(built_package):
    modules = {
        name: built_package.module(name)
        for name in (
            "client",
            "custom_queries",
            "custom_mutations",
            "custom_fields",
            "input_types",
            "enums",
        )
    }
    with built_package.tables():
        yield built_package.client_class, modules


class _Recorder:
    def __init__(self, data: dict) -> None:
        self.sent: list[dict] = []
        self.data = data

    def transport(self) -> httpx.MockTransport:
        def handler(request: httpx.Request) -> httpx.Response:
            self.sent.append(json.loads(request.content))
            return httpx.Response(200, json={"data": self.data})

        return httpx.MockTransport(handler)


async def _call(generated, environment, build_fields, *, mutation=False):
    client_class, modules = generated
    recorder = _Recorder({"program": {"id": "p-1"}, "updateProgram": {"id": "p-1"}})
    async with httpx.AsyncClient(transport=recorder.transport()) as http_client:
        client = client_class(
            url="http://gpp.test/odb",
            http_client=http_client,
            environment=environment,
        )
        call = client.mutation if mutation else client.query
        try:
            await call(build_fields(modules), operation_name="custom")
        finally:
            sent = recorder.sent
    return sent


def _program(modules, *selected, **arguments):
    fields = modules["custom_fields"].ProgramFields
    return (
        modules["custom_queries"]
        .Query.program(id="p-1", **arguments)
        .fields(fields.id, *(getattr(fields, name) for name in selected))
    )


def _update(modules, **values):
    inputs = modules["input_types"]
    fields = modules["custom_fields"].ProgramFields
    return (
        modules["custom_mutations"]
        .Mutation.update_program(input=inputs.UpdateInput(**values))
        .fields(fields.id)
    )


@pytest.mark.asyncio
async def test_a_call_every_environment_has_is_sent_unchanged(generated):
    sent = await _call(
        generated, GPPEnvironment.PRODUCTION, lambda m: _program(m, "name")
    )

    assert len(sent) == 1
    assert "name" in sent[0]["query"]


@pytest.mark.asyncio
@pytest.mark.parametrize(
    ("build_fields", "mutation", "item", "kind"),
    [
        (lambda m: _program(m, "draft_note"), False, "Program.draftNote", "field"),
        (
            lambda m: (
                m["custom_queries"]
                .Query.draft()
                .fields(m["custom_fields"].ProgramFields.id)
            ),
            False,
            "Query.draft",
            "field",
        ),
        (
            lambda m: _program(m, include_deleted=True),
            False,
            "Query.program(includeDeleted:)",
            "argument",
        ),
        (
            lambda m: _update(m, owner="o", kind=m["enums"].Kind.CALIBRATION),
            True,
            "Kind.CALIBRATION",
            "enum value",
        ),
        (
            lambda m: _update(m, owner="o", note="n"),
            True,
            "UpdateInput.note",
            "input field",
        ),
    ],
    ids=["field", "root-field", "argument", "enum-value", "input-field"],
)
async def test_production_raises_before_sending_what_only_development_has(
    generated, build_fields, mutation, item, kind
):
    with pytest.raises(GPPEnvironmentError) as raised:
        await _call(
            generated, GPPEnvironment.PRODUCTION, build_fields, mutation=mutation
        )

    error = raised.value
    assert error.item == item
    assert error.kind == kind
    assert error.environment is GPPEnvironment.PRODUCTION
    assert error.available == (GPPEnvironment.DEVELOPMENT,)
    assert str(error).endswith("Nothing was sent.")


@pytest.mark.asyncio
async def test_nothing_is_sent_when_a_call_raises(generated):
    client_class, modules = generated
    recorder = _Recorder({})
    async with httpx.AsyncClient(transport=recorder.transport()) as http_client:
        client = client_class(
            url="http://gpp.test/odb",
            http_client=http_client,
            environment=GPPEnvironment.PRODUCTION,
        )
        with pytest.raises(GPPEnvironmentError):
            await client.query(_program(modules, "draft_note"), operation_name="x")

    assert recorder.sent == []


@pytest.mark.asyncio
async def test_production_raises_for_an_input_field_it_requires(generated):
    with pytest.raises(GPPEnvironmentError) as raised:
        await _call(
            generated,
            GPPEnvironment.PRODUCTION,
            lambda m: _update(m, name="n"),
            mutation=True,
        )

    error = raised.value
    assert error.item == "UpdateInput.owner"
    assert error.kind is EnvironmentItemKind.INPUT_FIELD
    assert error.required is True
    assert error.available == (GPPEnvironment.DEVELOPMENT,)


@pytest.mark.asyncio
async def test_development_raises_for_a_field_only_production_has(generated):
    with pytest.raises(GPPEnvironmentError) as raised:
        await _call(
            generated, GPPEnvironment.DEVELOPMENT, lambda m: _program(m, "legacy")
        )

    assert raised.value.item == "Program.legacy"
    assert raised.value.available == (GPPEnvironment.PRODUCTION,)


@pytest.mark.asyncio
async def test_production_warns_once_for_a_leaving_field_and_sends(generated):
    with warnings.catch_warnings(record=True) as caught:
        warnings.simplefilter("always")
        first = await _call(
            generated, GPPEnvironment.PRODUCTION, lambda m: _program(m, "legacy")
        )
        second = await _call(
            generated, GPPEnvironment.PRODUCTION, lambda m: _program(m, "legacy")
        )

    leaving = [w for w in caught if issubclass(w.category, GPPFieldLeavingWarning)]
    assert [str(w.message) for w in leaving] == [
        "The field Program.legacy is gone from development and is expected to "
        "leave production at a coming promotion."
    ]
    assert leaving[0].filename == __file__
    assert len(first) == len(second) == 1


@pytest.mark.asyncio
async def test_a_document_no_environment_accepts_is_left_to_gpp(generated):
    client_class, _ = generated
    recorder = _Recorder({})
    async with httpx.AsyncClient(transport=recorder.transport()) as http_client:
        client = client_class(
            url="http://gpp.test/odb",
            http_client=http_client,
            environment=GPPEnvironment.PRODUCTION,
        )
        await client.execute("query typo { programz { id } }")

    assert recorder.sent[0]["query"] == "query typo { programz { id } }"


@pytest.mark.asyncio
async def test_gpp_client_on_production_raises_for_a_development_only_field(
    generated, gpp_transport
):
    async with httpx.AsyncClient(transport=gpp_transport) as http_client:
        async with GPPClient(
            environment="production", token="t", http_client=http_client
        ) as client:
            with pytest.raises(GPPEnvironmentError) as raised:
                await client.graphql.query(
                    _program(generated[1], "draft_note"), operation_name="custom"
                )

    assert raised.value.item == "Program.draftNote"
    assert raised.value.available == (GPPEnvironment.DEVELOPMENT,)
    assert gpp_transport.requests == []


@pytest.mark.asyncio
async def test_gpp_client_on_production_sends_a_call_it_accepts(
    generated, gpp_transport
):
    gpp_transport.respond({"program": {"id": "p-1", "name": "N"}})
    async with httpx.AsyncClient(transport=gpp_transport) as http_client:
        async with GPPClient(
            environment="production", token="t", http_client=http_client
        ) as client:
            data = await client.graphql.query(
                _program(generated[1], "name"), operation_name="custom"
            )

    assert data == {"program": {"id": "p-1", "name": "N"}}
    assert len(gpp_transport.requests) == 1


def _update_selecting_legacy(modules, **values):
    inputs = modules["input_types"]
    fields = modules["custom_fields"].ProgramFields
    return (
        modules["custom_mutations"]
        .Mutation.update_program(input=inputs.UpdateInput(**values))
        .fields(fields.id, fields.legacy)
    )


@pytest.mark.asyncio
@pytest.mark.parametrize(
    ("build_fields", "mutation", "item", "kind", "required"),
    [
        (
            lambda m: _program(m, "draft_note", "legacy"),
            False,
            "Program.draftNote",
            "field",
            False,
        ),
        (
            lambda m: _program(m, "legacy", include_deleted=True),
            False,
            "Query.program(includeDeleted:)",
            "argument",
            False,
        ),
        (
            lambda m: _update_selecting_legacy(m, name="n"),
            True,
            "UpdateInput.owner",
            "input field",
            True,
        ),
    ],
    ids=["field", "argument", "required-input-field"],
)
async def test_production_raises_for_its_own_lack_when_no_environment_accepts(
    generated, build_fields, mutation, item, kind, required
):
    with pytest.raises(GPPEnvironmentError) as raised:
        await _call(
            generated, GPPEnvironment.PRODUCTION, build_fields, mutation=mutation
        )

    error = raised.value
    assert error.item == item
    assert error.kind == kind
    assert error.required is required
    assert error.available == (GPPEnvironment.DEVELOPMENT,)
