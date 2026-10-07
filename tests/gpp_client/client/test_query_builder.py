"""
Tests for the generated query builder behind ``client.graphql.query``.
"""

import json

import httpx
import pytest

from gpp_client.generated.client import GraphQLClient
from gpp_client.generated.custom_fields import ProgramFields
from gpp_client.generated.custom_queries import Query
from graphql import parse, print_ast


@pytest.mark.asyncio
async def test_query_sends_camel_case_document_and_returns_data():
    """
    Snake-case builder names go out as the schema's camelCase names.
    """
    sent: list[dict] = []

    def handler(request: httpx.Request) -> httpx.Response:
        sent.append(json.loads(request.content))
        return httpx.Response(
            200,
            json={"data": {"program": {"id": "p-1", "proposalStatus": "ACCEPTED"}}},
        )

    client = GraphQLClient(
        url="https://gpp.test/odb",
        http_client=httpx.AsyncClient(transport=httpx.MockTransport(handler)),
    )

    data = await client.query(
        Query.program(program_id="p-1").fields(
            ProgramFields.id, ProgramFields.proposal_status
        ),
        operation_name="smoke",
    )

    assert data == {"program": {"id": "p-1", "proposalStatus": "ACCEPTED"}}
    assert len(sent) == 1
    assert sent[0]["operationName"] == "smoke"
    assert sent[0]["variables"] == {"programId_0": "p-1"}
    assert print_ast(parse(sent[0]["query"])) == print_ast(
        parse(
            "query smoke($programId_0: ProgramId) "
            "{ program(programId: $programId_0) { id proposalStatus } }"
        )
    )
