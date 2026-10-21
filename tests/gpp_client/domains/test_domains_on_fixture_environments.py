"""
Tests that a domain gets only what its environment has from the fake GPP.

The committed schemas share every field the domains read, so the client is
built from fixture schemas with the real build, and the fake GPP answers each
environment from its fixture schema. A domain that depended on a field one
environment lacks would fail on that environment's fake GPP here, as it would
in ``test_every_operation.py`` once the committed schemas differ that way.
"""

import json

import httpx
import pytest

from gpp_client.domains.scheduler import SchedulerDomain
from gpp_client.environment import GPPEnvironment
from graphql import build_schema
from tests.gpp_client.fixture_build import build_fixture
from tests.gpp_client.schema_transport import SchemaTransport

_SELECT = """
type Query { programs(today: String): ProgramSelect! }
type ProgramSelect { matches: [Program!]! hasMore: Boolean! }
"""
_SCHEMAS = {
    "development": _SELECT + "type Program { id: ID! }",
    "production": _SELECT + "type Program { id: ID! reference: ProgramReference }\n"
    "type ProgramReference { label: String! }",
}
_OPERATIONS = """
query GetSchedulerAllProgramsId($today: String) {
  programs(today: $today) { matches { id reference { label } } }
}
"""


@pytest.fixture(scope="module")
def fixture_build(tmp_path_factory):
    """
    Build a client whose scheduler operation selects a production-only field.
    """
    return build_fixture(tmp_path_factory.mktemp("build"), _SCHEMAS, _OPERATIONS)


async def _reference_labels(fixture_build, environment: GPPEnvironment):
    transport = SchemaTransport(
        environment, nulls=False, schema=build_schema(_SCHEMAS[environment.label])
    )
    with fixture_build.tables():
        async with httpx.AsyncClient(transport=transport) as http_client:
            graphql = fixture_build.client_class(
                url="http://gpp.test/odb",
                http_client=http_client,
                environment=environment,
            )
            domain = SchedulerDomain(graphql=graphql, rest=None, settings=None)
            labels = await domain.get_all_reference_labels(date="2026-10-13")
    return labels, json.loads(transport.requests[0].content)["query"]


@pytest.mark.asyncio
async def test_domain_reads_the_field_where_the_environment_has_it(fixture_build):
    labels, sent = await _reference_labels(fixture_build, GPPEnvironment.PRODUCTION)

    assert labels == [("String-1", "ID-1")]
    assert "reference" in sent


@pytest.mark.asyncio
async def test_domain_gets_nothing_for_the_field_the_environment_lacks(
    fixture_build,
):
    labels, sent = await _reference_labels(fixture_build, GPPEnvironment.DEVELOPMENT)

    assert labels == []
    assert "reference" not in sent
