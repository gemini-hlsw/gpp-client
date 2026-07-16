"""
Tests for the scheduler domain.
"""

from datetime import datetime, timezone

import pytest

from gpp_client.domains.scheduler import SchedulerDomain


@pytest.fixture()
def scheduler_domain(domain_kwargs) -> SchedulerDomain:
    """
    Return a scheduler domain instance.
    """
    return SchedulerDomain(**domain_kwargs)


@pytest.mark.asyncio
async def test_get_visibility_changes_parses_rest_response(
    scheduler_domain: SchedulerDomain,
    rest,
    mocker,
) -> None:
    """
    Ensure the REST body is fetched with since and parsed into sets.
    """
    rest._get_visibility_changes = mocker.AsyncMock(
        return_value=(
            "o-123\t2026-07-15T10:00:00Z\n"
            "t-456\t2026-07-15T11:30:00Z\n"
        )
    )
    since = datetime(2026, 7, 15, 9, 0, tzinfo=timezone.utc)

    result = await scheduler_domain.get_visibility_changes(since)

    rest._get_visibility_changes.assert_awaited_once_with(since)
    assert result.observation_ids == frozenset({"o-123"})
    assert result.target_ids == frozenset({"t-456"})
    assert result.max_timestamp == datetime(
        2026, 7, 15, 11, 30, tzinfo=timezone.utc
    )


@pytest.mark.asyncio
async def test_get_visibility_changes_propagates_rest_errors(
    scheduler_domain: SchedulerDomain,
    rest,
    mocker,
) -> None:
    """
    Ensure REST failures propagate to the caller.
    """
    rest._get_visibility_changes = mocker.AsyncMock(
        side_effect=RuntimeError("HTTP 500")
    )

    with pytest.raises(RuntimeError, match="HTTP 500"):
        await scheduler_domain.get_visibility_changes(
            datetime(2026, 7, 15, 9, 0, tzinfo=timezone.utc)
        )
