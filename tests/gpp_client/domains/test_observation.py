"""Tests for the observation domain."""

from types import SimpleNamespace

import pytest

from gpp_client.domains.observation import ObservationDomain
from tests.gpp_client.domains.helpers import _yield_events


@pytest.fixture()
def observation_domain(domain_kwargs) -> ObservationDomain:
    """
    Return an observation domain instance.
    """
    return ObservationDomain(**domain_kwargs)


@pytest.mark.asyncio
@pytest.mark.parametrize(
    ("method_name", "graphql_name", "kwargs"),
    [
        (
            "create",
            "create_observation",
            {"input": object()},
        ),
        (
            "clone",
            "clone_observation",
            {"input": object()},
        ),
        (
            "update_all",
            "update_observations",
            {"input": object()},
        ),
        (
            "restore_by_id",
            "restore_observation_by_id",
            {"observation_id": "o-1"},
        ),
        (
            "restore_by_reference",
            "restore_observation_by_reference",
            {"observation_reference": "obs-ref"},
        ),
        (
            "delete_by_reference",
            "delete_observation_by_reference",
            {"observation_reference": "obs-ref"},
        ),
        (
            "delete_by_id",
            "delete_observation_by_id",
            {"observation_id": "o-1"},
        ),
        (
            "get_by_id",
            "get_observation",
            {"observation_id": "o-1"},
        ),
        (
            "get_by_reference",
            "get_observation",
            {"observation_reference": "obs-ref"},
        ),
    ],
)
async def test_observation_domain_dispatches_simple_methods(
    observation_domain,
    graphql,
    mocker,
    method_name: str,
    graphql_name: str,
    kwargs: dict[str, object],
) -> None:
    """
    Ensure simple observation methods dispatch to GraphQL.
    """
    result_model = object()
    setattr(graphql, graphql_name, mocker.AsyncMock(return_value=result_model))

    method = getattr(observation_domain, method_name)
    result = await method(**kwargs)

    assert result is result_model
    getattr(graphql, graphql_name).assert_called_once_with(**kwargs)


@pytest.mark.asyncio
async def test_update_by_id_dispatches_correctly(
    observation_domain,
    graphql,
    mocker,
) -> None:
    """
    Ensure update_by_id dispatches with set_.
    """
    result_model = object()
    properties = object()
    graphql.update_observation_by_id = mocker.AsyncMock(return_value=result_model)

    result = await observation_domain.update_by_id("o-1", properties=properties)

    assert result is result_model
    graphql.update_observation_by_id.assert_called_once_with(
        observation_id="o-1",
        set_=properties,
    )


@pytest.mark.asyncio
async def test_update_by_reference_dispatches_correctly(
    observation_domain,
    graphql,
    mocker,
) -> None:
    """
    Ensure update_by_reference dispatches with set_.
    """
    result_model = object()
    properties = object()
    graphql.update_observation_by_reference = mocker.AsyncMock(
        return_value=result_model
    )

    result = await observation_domain.update_by_reference(
        "obs-ref", properties=properties
    )

    assert result is result_model
    graphql.update_observation_by_reference.assert_called_once_with(
        observation_reference="obs-ref",
        set_=properties,
    )


@pytest.mark.asyncio
async def test_get_all_dispatches_correctly(
    observation_domain,
    graphql,
    mocker,
) -> None:
    """
    Ensure get_all dispatches with filters.
    """
    result_model = object()
    where = object()
    graphql.get_observations = mocker.AsyncMock(return_value=result_model)

    result = await observation_domain.get_all(
        include_deleted=True,
        where=where,
        offset="abc",
        limit=10,
    )

    assert result is result_model
    graphql.get_observations.assert_called_once_with(
        include_deleted=True,
        where=where,
        offset="abc",
        limit=10,
    )


@pytest.mark.asyncio
async def test_subscribe_to_edits_yields_events(
    observation_domain,
    graphql,
    mocker,
) -> None:
    """
    Ensure subscribe_to_edits yields GraphQL events.
    """
    events = [SimpleNamespace(id=1), SimpleNamespace(id=2)]

    graphql.observation_edit = mocker.Mock(return_value=_yield_events(events))

    result = [
        event async for event in observation_domain.subscribe_to_edits(program_id="p-1")
    ]

    assert result == events
    graphql.observation_edit.assert_called_once_with(program_id="p-1")


@pytest.mark.asyncio
async def test_subscribe_to_calculation_updates_yields_events(
    observation_domain,
    graphql,
    mocker,
) -> None:
    """
    Ensure subscribe_to_calculation_updates yields GraphQL events.
    """
    events = [SimpleNamespace(id=1), SimpleNamespace(id=2)]

    graphql.obs_calculation_update = mocker.Mock(return_value=_yield_events(events))

    result = [
        event
        async for event in observation_domain.subscribe_to_calculation_updates(
            program_id="p-1"
        )
    ]

    assert result == events
    graphql.obs_calculation_update.assert_called_once_with(program_id="p-1")
