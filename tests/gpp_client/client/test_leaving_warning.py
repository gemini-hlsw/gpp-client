"""
Tests that using a field development has removed warns on the environments that
still have it.

The committed schemas have no leaving field, so the tests build a tiny client
from fixture schemas with the real build.
"""

import json
import warnings

import httpx
import pytest

from gpp_client.environment import GPPEnvironment
from gpp_client.exceptions import GPPFieldLeavingWarning
from tests.gpp_client.fixture_build import build_fixture

_DEVELOPMENT = """
type Program { id: ID! name: String }
type Query { program(id: ID!): Program }
"""

_PRODUCTION = """
type Program { id: ID! name: String legacy: String oldName: String retired: String }
type Query { program(id: ID!): Program }
"""

_SCHEMAS = {
    "development": _DEVELOPMENT,
    "production": _PRODUCTION,
}

_OPERATIONS = """
query getLegacy($id: ID!) { program(id: $id) { id legacy } }
query getOldName($id: ID!) { program(id: $id) { id oldName } }
query getRetired($id: ID!) { program(id: $id) { id retired } }
query getName($id: ID!) { program(id: $id) { id name } }
"""


@pytest.fixture(scope="module")
def built_package(tmp_path_factory):
    """
    Build a client whose operations select fields development has removed.
    """
    return build_fixture(tmp_path_factory.mktemp("build"), _SCHEMAS, _OPERATIONS)


@pytest.fixture()
def fixture_build(built_package):
    with built_package.tables():
        yield built_package.client_class, built_package.package


def _transport(sent: list[dict]) -> httpx.MockTransport:
    def handler(request: httpx.Request) -> httpx.Response:
        sent.append(json.loads(request.content))
        return httpx.Response(
            200, json={"data": {"program": {"id": "p-1", "name": "N"}}}
        )

    return httpx.MockTransport(handler)


def _client(fixture_build, http_client, environment):
    client_class, _ = fixture_build
    return client_class(
        url="http://gpp.test/odb",
        http_client=http_client,
        environment=environment,
    )


@pytest.mark.asyncio
async def test_production_warns_once_for_a_field_development_removed(
    fixture_build,
):
    sent: list[dict] = []
    async with httpx.AsyncClient(transport=_transport(sent)) as http_client:
        with warnings.catch_warnings(record=True) as caught:
            warnings.simplefilter("always")
            client = _client(fixture_build, http_client, GPPEnvironment.PRODUCTION)
            await client.get_legacy(id="p-1")
            await client.get_legacy(id="p-1")
            other = _client(fixture_build, http_client, GPPEnvironment.PRODUCTION)
            await other.get_legacy(id="p-1")

    leaving = [w for w in caught if issubclass(w.category, GPPFieldLeavingWarning)]
    assert len(leaving) == 1
    assert str(leaving[0].message) == (
        "The field Program.legacy is gone from development and is expected to "
        "leave production at a coming promotion."
    )
    assert leaving[0].filename == __file__
    assert len(sent) == 3


@pytest.mark.asyncio
@pytest.mark.parametrize(
    ("environment", "call"),
    [
        (GPPEnvironment.DEVELOPMENT, "get_retired"),
        (GPPEnvironment.PRODUCTION, "get_name"),
    ],
)
async def test_no_warning_on_development_or_for_fields_everywhere(
    fixture_build, environment, call
):
    # Each leaving field warns once per process, so this case selects one no
    # other test uses.
    async with httpx.AsyncClient(transport=_transport([])) as http_client:
        client = _client(fixture_build, http_client, environment)
        with warnings.catch_warnings():
            warnings.simplefilter("error", GPPFieldLeavingWarning)
            await getattr(client, call)(id="p-1")


@pytest.mark.asyncio
async def test_warning_can_be_raised_as_an_error_with_the_warnings_module(
    fixture_build,
):
    sent: list[dict] = []
    async with httpx.AsyncClient(transport=_transport(sent)) as http_client:
        client = _client(fixture_build, http_client, GPPEnvironment.PRODUCTION)
        with warnings.catch_warnings():
            warnings.simplefilter("error", GPPFieldLeavingWarning)
            with pytest.raises(GPPFieldLeavingWarning) as raised:
                await client.get_old_name(id="p-1")

    assert raised.value.field == "Program.oldName"
    assert raised.value.environment is GPPEnvironment.PRODUCTION
    assert sent == []
