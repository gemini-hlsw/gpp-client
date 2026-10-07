"""
Tests that the pre-send check still raises when an operation selects fields only
some environments have.

Each environment receives its own trimmed copy, so the check must judge each
environment by its own copy, not by the selected environment's.
"""

import json

import httpx
import pytest

from gpp_client.environment import GPPEnvironment
from gpp_client.exceptions import GPPEnvironmentError
from tests.gpp_client.fixture_build import build_fixture

_SCHEMAS = {
    "development": """
type Program { id: ID! draftNote: String }
type Query { program(id: ID!, includeDeleted: Boolean): Program }
type Mutation { updateProgram(input: UpdateInput!): Program }
enum Kind { SCIENCE CALIBRATION }
input UpdateInput { name: String note: String kind: Kind }
""",
    "production": """
type Program { id: ID! legacyRef: String }
type Query { program(id: ID!): Program }
type Mutation { updateProgram(input: UpdateInput!): Program }
enum Kind { SCIENCE }
input UpdateInput { name: String legacy: String kind: Kind }
""",
}

_OPERATIONS = """
query getProgram($id: ID!, $includeDeleted: Boolean) {
  program(id: $id, includeDeleted: $includeDeleted) { id draftNote legacyRef }
}
mutation updateProgram($input: UpdateInput!) {
  updateProgram(input: $input) { id draftNote legacyRef }
}
"""


@pytest.fixture(scope="module")
def built_package(tmp_path_factory):
    return build_fixture(tmp_path_factory.mktemp("build"), _SCHEMAS, _OPERATIONS)


@pytest.fixture()
def built(built_package):
    with built_package.tables():
        yield built_package


async def _raised(built, environment, method, **kwargs) -> GPPEnvironmentError:
    sent: list[dict] = []

    def handler(request: httpx.Request) -> httpx.Response:
        sent.append(json.loads(request.content))
        return httpx.Response(200, json={"data": {}})

    async with httpx.AsyncClient(transport=httpx.MockTransport(handler)) as http:
        client = built.client_class(
            url="http://gpp.test/odb", http_client=http, environment=environment
        )
        with pytest.raises(GPPEnvironmentError) as raised:
            await getattr(client, method)(**kwargs)

    assert sent == []
    return raised.value


@pytest.mark.asyncio
async def test_production_raises_for_a_development_only_input_field(built):
    inputs = built.module("input_types")

    error = await _raised(
        built,
        GPPEnvironment.PRODUCTION,
        "update_program",
        input=inputs.UpdateInput(name="n", note="draft"),
    )

    assert error.item == "UpdateInput.note"
    assert error.kind == "input field"
    assert error.available == (GPPEnvironment.DEVELOPMENT,)


@pytest.mark.asyncio
async def test_production_raises_for_a_development_only_enum_value(built):
    inputs = built.module("input_types")
    enums = built.module("enums")

    error = await _raised(
        built,
        GPPEnvironment.PRODUCTION,
        "update_program",
        input=inputs.UpdateInput(name="n", kind=enums.Kind.CALIBRATION),
    )

    assert error.item == "Kind.CALIBRATION"
    assert error.kind == "enum value"
    assert error.available == (GPPEnvironment.DEVELOPMENT,)


@pytest.mark.asyncio
async def test_development_raises_for_a_production_only_input_field(built):
    inputs = built.module("input_types")

    error = await _raised(
        built,
        GPPEnvironment.DEVELOPMENT,
        "update_program",
        input=inputs.UpdateInput(name="n", legacy="old"),
    )

    assert error.item == "UpdateInput.legacy"
    assert error.kind == "input field"
    assert error.available == (GPPEnvironment.PRODUCTION,)


@pytest.mark.asyncio
async def test_production_raises_for_a_set_argument_its_copy_dropped(built):
    error = await _raised(
        built,
        GPPEnvironment.PRODUCTION,
        "get_program",
        id="p-1",
        include_deleted=True,
    )

    assert error.item == "Query.program(includeDeleted:)"
    assert error.kind == "argument"
    assert error.available == (GPPEnvironment.DEVELOPMENT,)


@pytest.mark.asyncio
async def test_production_raises_when_the_call_mixes_both_environments_fields(built):
    inputs = built.module("input_types")

    error = await _raised(
        built,
        GPPEnvironment.PRODUCTION,
        "update_program",
        input=inputs.UpdateInput(name="n", note="new", legacy="old"),
    )

    assert error.item == "UpdateInput.note"
    assert error.kind == "input field"
    assert error.available == (GPPEnvironment.DEVELOPMENT,)
    assert error.works_there is False
    assert str(error) == (
        "The input field UpdateInput.note is not available on production. "
        "It is available on development. Leave it unset on production. "
        "Nothing was sent."
    )


@pytest.mark.asyncio
async def test_development_raises_when_the_call_mixes_both_environments_fields(built):
    inputs = built.module("input_types")

    error = await _raised(
        built,
        GPPEnvironment.DEVELOPMENT,
        "update_program",
        input=inputs.UpdateInput(name="n", note="new", legacy="old"),
    )

    assert error.item == "UpdateInput.legacy"
    assert error.kind == "input field"
    assert error.available == (GPPEnvironment.PRODUCTION,)
    assert error.works_there is False
    assert "select production" not in str(error)


@pytest.mark.asyncio
async def test_production_raises_for_a_new_enum_value_mixed_with_an_old_field(built):
    inputs = built.module("input_types")
    enums = built.module("enums")

    error = await _raised(
        built,
        GPPEnvironment.PRODUCTION,
        "update_program",
        input=inputs.UpdateInput(legacy="old", kind=enums.Kind.CALIBRATION),
    )

    assert error.item == "Kind.CALIBRATION"
    assert error.kind == "enum value"
    assert error.available == (GPPEnvironment.DEVELOPMENT,)


_BOTH_REQUIRE = {
    "development": """
type Program { id: ID! }
type Query { program(id: ID!, site: String!): Program }
type Mutation { updateProgram(input: UpdateInput!): Program }
input UpdateInput { name: String owner: String! }
""",
    "production": """
type Program { id: ID! legacyRef: String }
type Query { program(id: ID!, site: String!): Program }
type Mutation { updateProgram(input: UpdateInput!): Program }
input UpdateInput { name: String owner: String! }
""",
}


@pytest.fixture(scope="module")
def both_require_package(tmp_path_factory):
    return build_fixture(
        tmp_path_factory.mktemp("both_require"),
        _BOTH_REQUIRE,
        "mutation updateProgram($input: UpdateInput!) "
        "{ updateProgram(input: $input) { id legacyRef } }\n",
    )


@pytest.mark.asyncio
@pytest.mark.parametrize(
    ("query", "variables"),
    [
        (
            "mutation m($input: UpdateInput!) "
            "{ updateProgram(input: $input) { id legacyRef } }",
            {"input": {"name": "n"}},
        ),
        ('query q { program(id: "p-1") { id legacyRef } }', None),
    ],
    ids=["input-field", "argument"],
)
async def test_what_every_environment_requires_is_left_to_gpp(
    both_require_package, query, variables
):
    sent: list[dict] = []

    def handler(request: httpx.Request) -> httpx.Response:
        sent.append(json.loads(request.content))
        return httpx.Response(200, json={"errors": [{"message": "owner required"}]})

    with both_require_package.tables():
        client_class = both_require_package.client_class
        async with httpx.AsyncClient(transport=httpx.MockTransport(handler)) as http:
            client = client_class(
                url="http://gpp.test/odb",
                http_client=http,
                environment=GPPEnvironment.PRODUCTION,
            )
            await client.execute(query, variables=variables)

    assert len(sent) == 1
