"""
Tests that a field the selected environment lacks reads ``None``, and that
``is_available`` and ``enum_values`` answer for that environment without a
network call.

The committed schemas change with every promotion, so these tests build a tiny
client from fixture schemas with the real build and answer it from a fake GPP
built from the same fixture schemas.
"""

import json

import httpx
import pytest

from gpp_client import GPPClient, is_available
from gpp_client.environment import GPPEnvironment
from graphql import build_schema
from tests.gpp_client.fixture_build import build_fixture
from tests.gpp_client.schema_transport import answer

_QUERY = "type Query { program: Program }\n"
_PROGRAMS = {
    "development": "type Program { id: ID! note: String }",
    "production": "type Program { id: ID! }",
}


@pytest.fixture(scope="module")
def built_package(tmp_path_factory):
    """
    Build a client whose ``getProgram`` selects a development-only field.
    """
    return build_fixture(
        tmp_path_factory.mktemp("build"),
        {env: _QUERY + program for env, program in _PROGRAMS.items()},
        "query getProgram { program { id note } }",
    )


@pytest.fixture()
def fixture_client(built_package):
    with built_package.tables():
        yield built_package.client_class


def _fake_gpp(environment: GPPEnvironment) -> httpx.MockTransport:
    schema = build_schema(_QUERY + _PROGRAMS[environment.label])

    def handler(request: httpx.Request) -> httpx.Response:
        data = answer(schema, json.loads(request.content), nulls=False)
        return httpx.Response(200, json={"data": data})

    return httpx.MockTransport(handler)


async def _get_program(client_class, environment: GPPEnvironment):
    async with httpx.AsyncClient(transport=_fake_gpp(environment)) as http_client:
        client = client_class(
            url="http://gpp.test/odb", http_client=http_client, environment=environment
        )
        return await client.get_program()


@pytest.mark.asyncio
async def test_production_reads_none_for_a_development_only_field(fixture_client):
    result = await _get_program(fixture_client, GPPEnvironment.PRODUCTION)

    assert result.program.id == "ID-1"
    assert result.program.note is None
    assert (
        is_available(result.program, "note", environment=GPPEnvironment.PRODUCTION)
        is False
    )


@pytest.mark.asyncio
async def test_development_reads_its_field_and_has_it_available(fixture_client):
    result = await _get_program(fixture_client, GPPEnvironment.DEVELOPMENT)

    assert result.program.note == "String-1"
    assert (
        is_available(result.program, "note", environment=GPPEnvironment.DEVELOPMENT)
        is True
    )


@pytest.mark.asyncio
async def test_unknown_field_raises_naming_the_model(fixture_client):
    result = await _get_program(fixture_client, GPPEnvironment.DEVELOPMENT)

    with pytest.raises(AttributeError, match="GetProgramProgram has no field 'nope'"):
        is_available(result.program, "nope", environment=GPPEnvironment.DEVELOPMENT)


@pytest.fixture(scope="module")
def fragment_package(tmp_path_factory):
    """
    Build a client whose ``getProgram`` reads the field through a fragment.
    """
    return build_fixture(
        tmp_path_factory.mktemp("build"),
        {env: _QUERY + program for env, program in _PROGRAMS.items()},
        "fragment programFields on Program { id note }\n"
        "query getProgram { program { ...programFields } }",
    )


@pytest.mark.asyncio
async def test_field_selected_through_a_fragment_answers_on_the_nested_model(
    fragment_package,
):
    with fragment_package.tables():
        result = await _get_program(
            fragment_package.client_class, GPPEnvironment.PRODUCTION
        )
        available = is_available(
            result.program, "note", environment=GPPEnvironment.PRODUCTION
        )

    assert result.program.note is None
    assert available is False


_SHAPE_CHANGE = {
    "development": "type Program { id: ID! pi: [String] }",
    "production": "type Program { id: ID! pi: String }",
}


@pytest.fixture(scope="module")
def shape_change_package(tmp_path_factory):
    """
    Build a client for a field whose type development changed.
    """
    return build_fixture(
        tmp_path_factory.mktemp("build"),
        {env: _QUERY + program for env, program in _SHAPE_CHANGE.items()},
        "query getProgram { program { id pi } }",
    )


def test_field_whose_shape_changed_is_production_only(shape_change_package):
    # The development round trip needs the trim to leave the field out there;
    # until then the build's own answer is what is checked.
    model = shape_change_package.module("get_program").GetProgramProgram

    with shape_change_package.tables():
        assert model.model_validate({"id": "p-1"}).pi is None
        assert is_available(model, "pi", environment="production")
        assert not is_available(model, "pi", environment="development")


_FLAVORS = {
    "development": "type Query { flavor: Flavor secret: Secret }\n"
    "enum Flavor { VANILLA CHOCOLATE }\nenum Secret { HIDDEN }",
    "production": "type Query { flavor: Flavor }\nenum Flavor { VANILLA }",
}


@pytest.fixture(scope="module")
def enum_package(tmp_path_factory):
    """
    Build a client with an enum value and an enum type only development has.
    """
    return build_fixture(
        tmp_path_factory.mktemp("build"), _FLAVORS, "query flavor { flavor }"
    )


def _client(environment: str) -> GPPClient:
    return GPPClient(environment=environment, token="t")


def test_enum_values_are_the_selected_environments_values(enum_package):
    enums = enum_package.module("enums")

    with enum_package.tables():
        on_development = _client("development").enum_values(enums.Flavor)
        on_production = _client("production").enum_values(enums.Flavor)

    assert on_development == [enums.Flavor.VANILLA, enums.Flavor.CHOCOLATE]
    assert on_production == [enums.Flavor.VANILLA]


def test_enum_parses_either_environments_values(enum_package):
    enums = enum_package.module("enums")

    assert enums.Flavor("CHOCOLATE") is enums.Flavor.CHOCOLATE


def test_enum_values_of_an_enum_the_environment_lacks_are_empty(enum_package):
    enums = enum_package.module("enums")

    with enum_package.tables():
        on_development = _client("development").enum_values(enums.Secret)
        on_production = _client("production").enum_values(enums.Secret)

    assert on_development == [enums.Secret.HIDDEN]
    assert on_production == []


@pytest.mark.asyncio
async def test_client_answers_is_available_for_its_own_environment(fixture_client):
    result = await _get_program(fixture_client, GPPEnvironment.PRODUCTION)

    assert _client("development").is_available(result.program, "note") is True
    assert _client("production").is_available(result.program, "note") is False


@pytest.mark.asyncio
async def test_bare_is_available_reads_the_environment_variable(
    fixture_client, monkeypatch
):
    result = await _get_program(fixture_client, GPPEnvironment.PRODUCTION)

    monkeypatch.setenv("GPP_ENVIRONMENT", "development")
    assert is_available(result.program, "note") is True
    monkeypatch.delenv("GPP_ENVIRONMENT")
    assert is_available(result.program, "note") is False
    assert is_available(result.program, "note", environment="") is False
