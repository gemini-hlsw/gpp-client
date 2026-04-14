"""
Tests for the program domain.
"""

from types import SimpleNamespace

import pytest

from gpp_client.domains.program import ProgramDomain
from tests.gpp_client.domains.helpers import _yield_events


@pytest.fixture()
def program_domain(domain_kwargs) -> ProgramDomain:
    """
    Return a program domain instance.
    """
    return ProgramDomain(**domain_kwargs)


@pytest.mark.asyncio
@pytest.mark.parametrize(
    ("method_name", "graphql_name", "kwargs"),
    [
        (
            "create",
            "create_program",
            {"include_deleted": False, "properties": None},
        ),
        (
            "restore_by_id",
            "restore_program_by_id",
            {"program_id": "p-1"},
        ),
        (
            "delete_by_id",
            "delete_program_by_id",
            {"program_id": "p-1"},
        ),
        (
            "get_by_id",
            "get_program_by_id",
            {"program_id": "p-1", "include_deleted": False},
        ),
        (
            "get_by_reference",
            "get_program_by_reference",
            {"program_reference": "prog-ref", "include_deleted": False},
        ),
        (
            "get_by_proposal_reference",
            "get_program_by_proposal_reference",
            {"proposal_reference": "prop-ref", "include_deleted": False},
        ),
        (
            "get_all",
            "get_programs",
            {
                "include_deleted": False,
                "where": None,
                "offset": None,
                "limit": None,
            },
        ),
    ],
)
async def test_program_domain_dispatches_simple_methods(
    program_domain,
    graphql,
    mocker,
    method_name: str,
    graphql_name: str,
    kwargs: dict[str, object],
) -> None:
    """
    Ensure simple program methods dispatch to GraphQL.
    """
    result_model = object()
    setattr(graphql, graphql_name, mocker.AsyncMock(return_value=result_model))

    method = getattr(program_domain, method_name)
    result = await method(**kwargs)

    assert result is result_model
    getattr(graphql, graphql_name).assert_called_once_with(**kwargs)


@pytest.mark.asyncio
async def test_update_all_dispatches_correctly(
    program_domain,
    graphql,
    mocker,
) -> None:
    """
    Ensure update_all dispatches with the expected arguments.
    """
    result_model = object()
    properties = object()
    where = object()
    graphql.update_programs = mocker.AsyncMock(return_value=result_model)

    result = await program_domain.update_all(
        properties=properties,
        include_deleted=True,
        where=where,
        limit=10,
    )

    assert result is result_model
    graphql.update_programs.assert_called_once_with(
        properties=properties,
        include_deleted=True,
        where=where,
        limit=10,
    )


@pytest.mark.asyncio
async def test_update_by_id_dispatches_correctly(
    program_domain,
    graphql,
    mocker,
) -> None:
    """
    Ensure update_by_id dispatches with the expected arguments.
    """
    result_model = object()
    properties = object()
    graphql.update_program_by_id = mocker.AsyncMock(return_value=result_model)

    result = await program_domain.update_by_id(
        "p-1",
        properties=properties,
        include_deleted=True,
    )

    assert result is result_model
    graphql.update_program_by_id.assert_called_once_with(
        program_id="p-1",
        properties=properties,
        include_deleted=True,
    )


@pytest.mark.asyncio
async def test_subscribe_to_edits_yields_events(
    program_domain,
    graphql,
    mocker,
) -> None:
    """
    Ensure subscribe_to_edits yields GraphQL events.
    """
    events = [SimpleNamespace(id=1), SimpleNamespace(id=2)]

    graphql.program_edit = mocker.Mock(return_value=_yield_events(events))

    result = [
        event async for event in program_domain.subscribe_to_edits(program_id="p-1")
    ]

    assert result == events
    graphql.program_edit.assert_called_once_with(program_id="p-1")
