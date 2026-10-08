"""
Tests that a client sends each operation as its environment receives it.

The committed schemas select no environment-specific field yet, so these tests
build a tiny client from fixture schemas with the real build, and send through
the environment-aware GraphQL client that ``GPPClient.graphql`` uses.
"""

import json

import httpx
import pytest

from gpp_client.environment import GPPEnvironment
from tests.gpp_client.fixture_build import build_fixture

_QUERY = "type Query { program: Program }\n"


@pytest.fixture(scope="module")
def built_package(tmp_path_factory):
    """
    Build a client whose ``getProgram`` selects a production-only field.
    """
    programs = {
        "development": "type Program { id: ID! }",
        "production": "type Program { id: ID! reference: String }",
    }
    return build_fixture(
        tmp_path_factory.mktemp("build"),
        {env: _QUERY + program for env, program in programs.items()},
        "query getProgram { program { id reference } }",
    )


@pytest.fixture()
def fixture_client(built_package):
    with built_package.tables():
        yield built_package.client_class, built_package.package


def _recording(response: dict, sent: list[dict]) -> httpx.MockTransport:
    def handler(request: httpx.Request) -> httpx.Response:
        sent.append(json.loads(request.content))
        return httpx.Response(200, json={"data": response})

    return httpx.MockTransport(handler)


@pytest.mark.asyncio
async def test_development_reads_none_for_a_production_only_field(fixture_client):
    client_class, _ = fixture_client
    sent: list[dict] = []
    transport = _recording({"program": {"id": "p-1"}}, sent)

    async with httpx.AsyncClient(transport=transport) as http_client:
        client = client_class(
            url="http://gpp.test/odb",
            http_client=http_client,
            environment=GPPEnvironment.DEVELOPMENT,
        )
        result = await client.get_program()

    assert result.program.id == "p-1"
    assert result.program.reference is None
    assert sent[0]["query"] == "query getProgram {\n  program {\n    id\n  }\n}"


@pytest.mark.asyncio
async def test_production_receives_and_reads_its_field(fixture_client):
    client_class, _ = fixture_client
    sent: list[dict] = []
    transport = _recording({"program": {"id": "p-1", "reference": "G-1"}}, sent)

    async with httpx.AsyncClient(transport=transport) as http_client:
        client = client_class(
            url="http://gpp.test/odb",
            http_client=http_client,
            environment=GPPEnvironment.PRODUCTION,
        )
        result = await client.get_program()

    assert result.program.reference == "G-1"
    assert "reference" in sent[0]["query"]
