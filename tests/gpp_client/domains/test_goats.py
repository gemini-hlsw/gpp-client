"""
Tests for the GOATS domain.
"""

import pytest

from gpp_client.domains.goats import GOATSDomain


@pytest.fixture()
def goats_domain(domain_kwargs) -> GOATSDomain:
    """
    Return a GOATS domain instance.
    """
    return GOATSDomain(**domain_kwargs)


@pytest.mark.asyncio
async def test_get_observations_by_program_id_dispatches_correctly(
    goats_domain,
    graphql,
    mocker,
) -> None:
    """
    Ensure get_observations_by_program_id dispatches to GraphQL.
    """
    result_model = object()
    graphql.get_goats_observations = mocker.AsyncMock(return_value=result_model)

    result = await goats_domain.get_observations_by_program_id(program_id="p-1")

    assert result is result_model
    graphql.get_goats_observations.assert_called_once_with(program_id="p-1")


@pytest.mark.asyncio
async def test_get_programs_dispatches_correctly(
    goats_domain,
    graphql,
    mocker,
) -> None:
    """
    Ensure get_programs dispatches to GraphQL.
    """
    result_model = object()
    graphql.get_goats_programs = mocker.AsyncMock(return_value=result_model)

    result = await goats_domain.get_programs()

    assert result is result_model
    graphql.get_goats_programs.assert_called_once_with()
