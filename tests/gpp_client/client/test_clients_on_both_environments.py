"""
Tests that clients on different environments work side by side in one
process, each sending its own environment's copy of an operation.

The client is built from fixture schemas with the real build, so the copies
differ whatever the committed schemas say.
"""

import asyncio

import httpx
import pytest

from gpp_client.constants import DEVELOPMENT_URL, PRODUCTION_URL
from gpp_client.environment import GPPEnvironment
from tests.gpp_client.conftest import RecordingTransport
from tests.gpp_client.fixture_build import build_fixture

_SCHEMAS = {
    "development": "type Query { program: Program }\ntype Program { id: ID! draft: String }",
    "production": "type Query { program: Program }\ntype Program { id: ID! }",
}
_OPERATION = "query getProgram { program { id draft } }"


@pytest.fixture(scope="module")
def fixture_build(tmp_path_factory):
    """
    Build a client whose ``getProgram`` selects a field production lacks.
    """
    return build_fixture(tmp_path_factory.mktemp("build"), _SCHEMAS, _OPERATION)


@pytest.fixture()
def client_class(fixture_build):
    with fixture_build.tables():
        yield fixture_build.client_class


@pytest.mark.asyncio
async def test_two_clients_on_different_environments_at_once(client_class) -> None:
    gpp = RecordingTransport()
    gpp.respond({"program": None})
    gpp.respond({"program": None})

    async with httpx.AsyncClient(transport=gpp) as http_client:
        development = client_class(
            url=f"{DEVELOPMENT_URL}/odb",
            http_client=http_client,
            environment=GPPEnvironment.DEVELOPMENT,
            headers={"Authorization": "Bearer d"},
        )
        production = client_class(
            url=f"{PRODUCTION_URL}/odb",
            http_client=http_client,
            environment=GPPEnvironment.PRODUCTION,
            headers={"Authorization": "Bearer p"},
        )
        await asyncio.gather(development.get_program(), production.get_program())

    sent = {
        str(request.url): (request.headers["Authorization"], body["query"])
        for request, body in zip(gpp.requests, gpp.bodies, strict=True)
    }
    assert sent[f"{DEVELOPMENT_URL}/odb"][0] == "Bearer d"
    assert "draft" in sent[f"{DEVELOPMENT_URL}/odb"][1]
    assert sent[f"{PRODUCTION_URL}/odb"][0] == "Bearer p"
    assert "draft" not in sent[f"{PRODUCTION_URL}/odb"][1]
