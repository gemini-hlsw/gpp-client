"""
Tests for the target domain.
"""

from types import SimpleNamespace

import pytest

from gpp_client.domains.target import TargetDomain
from tests.gpp_client.domains.helpers import _yield_events


@pytest.fixture()
def target_domain(domain_kwargs) -> TargetDomain:
    """
    Return a target domain instance.
    """
    return TargetDomain(**domain_kwargs)


@pytest.mark.asyncio
@pytest.mark.parametrize(
    ("method_name", "graphql_name", "kwargs"),
    [
        (
            "clone",
            "clone_target",
            {
                "target_id": "t-1",
                "include_deleted": True,
                "properties": None,
                "replace_in": None,
            },
        ),
        (
            "create_by_program_id",
            "create_target_by_program_id",
            {
                "program_id": "p-1",
                "properties": object(),
                "include_deleted": True,
            },
        ),
        (
            "create_by_program_reference",
            "create_target_by_program_reference",
            {
                "program_reference": "prog-ref",
                "properties": object(),
                "include_deleted": True,
            },
        ),
        (
            "create_by_proposal_reference",
            "create_target_by_proposal_reference",
            {
                "proposal_reference": "prop-ref",
                "properties": object(),
                "include_deleted": True,
            },
        ),
        (
            "update_all",
            "update_targets",
            {
                "properties": object(),
                "include_deleted": True,
                "where": None,
                "limit": None,
            },
        ),
        (
            "update_by_id",
            "update_target_by_id",
            {
                "target_id": "t-1",
                "properties": object(),
                "include_deleted": True,
            },
        ),
        (
            "restore_by_id",
            "restore_target_by_id",
            {
                "target_id": "t-1",
            },
        ),
        (
            "delete_by_id",
            "delete_target_by_id",
            {
                "target_id": "t-1",
            },
        ),
        (
            "get_by_id",
            "get_target_by_id",
            {
                "target_id": "t-1",
                "include_deleted": True,
            },
        ),
        (
            "get_all",
            "get_targets",
            {
                "include_deleted": True,
                "where": None,
                "offset": None,
                "limit": None,
            },
        ),
    ],
)
async def test_target_domain_dispatches_methods(
    target_domain,
    graphql,
    mocker,
    method_name: str,
    graphql_name: str,
    kwargs: dict[str, object],
) -> None:
    """
    Ensure target methods dispatch to GraphQL.
    """
    result_model = object()
    setattr(graphql, graphql_name, mocker.AsyncMock(return_value=result_model))

    method = getattr(target_domain, method_name)
    result = await method(**kwargs)

    assert result is result_model
    getattr(graphql, graphql_name).assert_called_once_with(**kwargs)


@pytest.mark.asyncio
async def test_subscribe_edits_yields_events(
    target_domain,
    graphql,
    mocker,
) -> None:
    """
    Ensure subscribe_edits yields GraphQL events.
    """
    events = [SimpleNamespace(id=1), SimpleNamespace(id=2)]
    graphql.target_edit = mocker.Mock(return_value=_yield_events(events))

    result = [event async for event in target_domain.subscribe_edits(target_id="t-1")]

    assert result == events
    graphql.target_edit.assert_called_once_with(target_edit="t-1")
