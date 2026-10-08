"""
Tests for the scheduler domain.
"""

from datetime import UTC, datetime
from types import SimpleNamespace

import pytest

from gpp_client.domains.scheduler import (
    OBSERVATIONS_PAGE_SIZE,
    PROGRAMS_PAGE_SIZE,
    SchedulerDomain,
)
from gpp_client.generated.get_scheduler_programs import (
    GetSchedulerPrograms,
    GetSchedulerProgramsPrograms,
    GetSchedulerProgramsProgramsMatches,
)


@pytest.fixture()
def scheduler_domain(domain_kwargs) -> SchedulerDomain:
    """
    Return a scheduler domain instance.
    """
    return SchedulerDomain(**domain_kwargs)


def _programs_page(ids: list[str], has_more: bool) -> GetSchedulerPrograms:
    """
    Build a scheduler programs page holding only program IDs.
    """
    return GetSchedulerPrograms.model_construct(
        programs=GetSchedulerProgramsPrograms.model_construct(
            matches=[
                GetSchedulerProgramsProgramsMatches.model_construct(id=program_id)
                for program_id in ids
            ],
            has_more=has_more,
        )
    )


def _observations_page(ids: list[str], has_more: bool) -> SimpleNamespace:
    """
    Build an observations page whose matches dump to their ID only.
    """
    return SimpleNamespace(
        observations=SimpleNamespace(
            matches=[
                SimpleNamespace(
                    id=obs_id, model_dump=lambda obs_id=obs_id: {"id": obs_id}
                )
                for obs_id in ids
            ],
            has_more=has_more,
        )
    )


@pytest.mark.asyncio
async def test_get_all_pages_observations_after_programs(
    scheduler_domain: SchedulerDomain,
    rest,
    graphql,
    mocker,
) -> None:
    """
    Ensure programs, observation pages and sequences are fetched in that order,
    every observation page lands in the tree, and sequences are requested only
    for observations the query returned.
    """
    calls = []
    filters = []
    program = {
        "id": "p-1",
        "all_group_elements": [
            {"parent_group_id": None, "observation": {"id": "o-1"}},
            {"parent_group_id": None, "observation": {"id": "o-2"}},
            # Not Ready/Ongoing, so the observation query never returns it.
            {"parent_group_id": None, "observation": {"id": "o-3"}},
        ],
    }
    observation_pages = [
        _observations_page(["o-1"], has_more=True),
        _observations_page(["o-1", "o-2"], has_more=False),
    ]

    async def get_programs(**kwargs):
        calls.append("programs")
        return mocker.Mock(
            model_dump=mocker.Mock(return_value={"programs": {"matches": [program]}})
        )

    async def get_observations(**kwargs):
        calls.append(("observations", kwargs["offset"], kwargs["limit"]))
        filters.append(kwargs["where"])
        return observation_pages.pop(0)

    async def get_atom_digests(observation_ids):
        calls.append(("atoms", observation_ids))
        return ""

    mocker.patch.object(scheduler_domain, "get_programs", get_programs)
    graphql.get_observations = get_observations
    rest.get_atom_digests = get_atom_digests

    result = await scheduler_domain.get_all(programs_list=["p-1"])

    assert calls == [
        "programs",
        ("observations", None, OBSERVATIONS_PAGE_SIZE),
        ("observations", "o-1", OBSERVATIONS_PAGE_SIZE),
        # Sequences only for observations the query returned.
        ("atoms", ["o-1", "o-2"]),
    ]
    assert [e["observation"]["id"] for e in result[0]["root"]["elements"]] == [
        "o-1",
        "o-2",
    ]
    # Observations are filtered by program, not by the full observation ID list.
    for where in filters:
        assert where.program.id.in_ == ["p-1"]
        assert where.id is None


@pytest.mark.asyncio
async def test_get_all_skips_excluded_programs(
    scheduler_domain: SchedulerDomain,
    rest,
    graphql,
    mocker,
) -> None:
    """
    Ensure excluded program IDs never reach the programs query.
    """
    get_programs = mocker.AsyncMock(
        return_value=mocker.Mock(
            model_dump=mocker.Mock(return_value={"programs": {"matches": []}})
        )
    )
    mocker.patch.object(scheduler_domain, "get_programs", get_programs)
    graphql.get_observations = mocker.AsyncMock(
        return_value=_observations_page([], has_more=False)
    )

    await scheduler_domain.get_all(
        programs_list=["p-1", "p-18ca", "p-2"], exclude_programs=["p-18ca"]
    )

    get_programs.assert_awaited_once_with(programs_list=["p-1", "p-2"])


@pytest.mark.asyncio
async def test_get_programs_merges_every_page(
    scheduler_domain: SchedulerDomain,
    graphql,
    mocker,
) -> None:
    """
    Ensure pages are walked by offset and merged without the repeated program.
    """
    graphql.get_scheduler_programs = mocker.AsyncMock(
        side_effect=[
            _programs_page(["p-1", "p-2", "p-3"], has_more=True),
            _programs_page(["p-3", "p-4", "p-5"], has_more=True),
            _programs_page(["p-5", "p-6"], has_more=False),
        ]
    )

    result = await scheduler_domain.get_programs(
        programs_list=["p-1", "p-6"], page_size=3
    )

    assert [p.id for p in result.programs.matches] == [
        "p-1",
        "p-2",
        "p-3",
        "p-4",
        "p-5",
        "p-6",
    ]
    assert result.programs.has_more is False
    assert graphql.get_scheduler_programs.await_args_list == [
        mocker.call(programs_list=["p-1", "p-6"], offset=None, limit=3),
        mocker.call(programs_list=["p-1", "p-6"], offset="p-3", limit=3),
        mocker.call(programs_list=["p-1", "p-6"], offset="p-5", limit=3),
    ]


@pytest.mark.asyncio
async def test_get_programs_defaults_to_module_page_size(
    scheduler_domain: SchedulerDomain,
    graphql,
    mocker,
) -> None:
    """
    Ensure a single page is requested with the default page size.
    """
    graphql.get_scheduler_programs = mocker.AsyncMock(
        return_value=_programs_page(["p-1"], has_more=False)
    )

    result = await scheduler_domain.get_programs()

    assert [p.id for p in result.programs.matches] == ["p-1"]
    graphql.get_scheduler_programs.assert_awaited_once_with(
        programs_list=None, offset=None, limit=PROGRAMS_PAGE_SIZE
    )


@pytest.mark.asyncio
async def test_get_programs_stops_when_page_has_only_the_offset(
    scheduler_domain: SchedulerDomain,
    graphql,
    mocker,
) -> None:
    """
    Ensure a page that only repeats the offset program ends the loop.
    """
    graphql.get_scheduler_programs = mocker.AsyncMock(
        side_effect=[
            _programs_page(["p-1", "p-2"], has_more=True),
            _programs_page(["p-2"], has_more=True),
        ]
    )

    result = await scheduler_domain.get_programs(page_size=2)

    assert [p.id for p in result.programs.matches] == ["p-1", "p-2"]
    assert graphql.get_scheduler_programs.await_count == 2


@pytest.mark.asyncio
async def test_get_programs_rejects_page_size_below_two(
    scheduler_domain: SchedulerDomain,
) -> None:
    """
    Ensure a page size that could never advance the offset is refused.
    """
    with pytest.raises(ValueError, match="page_size"):
        await scheduler_domain.get_programs(page_size=1)


@pytest.mark.asyncio
async def test_get_visibility_changes_parses_rest_response(
    scheduler_domain: SchedulerDomain,
    rest,
    mocker,
) -> None:
    """
    Ensure the REST body is fetched with since and parsed into sets.
    """
    rest.get_visibility_changes = mocker.AsyncMock(
        return_value=("o-123\t2026-07-15T10:00:00Z\nt-456\t2026-07-15T11:30:00Z\n")
    )
    since = datetime(2026, 7, 15, 9, 0, tzinfo=UTC)

    result = await scheduler_domain.get_visibility_changes(since)

    rest.get_visibility_changes.assert_awaited_once_with(since)
    assert result.observation_ids == frozenset({"o-123"})
    assert result.target_ids == frozenset({"t-456"})
    assert result.max_timestamp == datetime(2026, 7, 15, 11, 30, tzinfo=UTC)


@pytest.mark.asyncio
async def test_get_visibility_changes_propagates_rest_errors(
    scheduler_domain: SchedulerDomain,
    rest,
    mocker,
) -> None:
    """
    Ensure REST failures propagate to the caller.
    """
    rest.get_visibility_changes = mocker.AsyncMock(side_effect=RuntimeError("HTTP 500"))

    with pytest.raises(RuntimeError, match="HTTP 500"):
        await scheduler_domain.get_visibility_changes(
            datetime(2026, 7, 15, 9, 0, tzinfo=UTC)
        )


@pytest.mark.asyncio
async def test_get_visibility_changes_leaves_shared_rest_client_open(
    scheduler_domain: SchedulerDomain,
    rest,
    mocker,
) -> None:
    """
    Ensure the domain does not close the REST client it was handed.

    The client (and its aiohttp session) is shared with every other caller, so
    closing it here aborts their in-flight requests with
    ``ClientConnectionError("Connector is closed.")``.
    """
    rest.get_visibility_changes = mocker.AsyncMock(return_value="")

    await scheduler_domain.get_visibility_changes(
        datetime(2026, 7, 15, 9, 0, tzinfo=UTC)
    )

    rest.close.assert_not_called()


@pytest.mark.asyncio
async def test_get_all_leaves_shared_rest_client_open(
    scheduler_domain: SchedulerDomain,
    rest,
    graphql,
    mocker,
) -> None:
    """
    Ensure the atom-digest fetch in get_all does not close the shared REST client.
    """
    program = {
        "id": "p-1",
        "all_group_elements": [
            {"parent_group_id": None, "observation": {"id": "o-1"}},
        ],
    }
    mocker.patch.object(
        scheduler_domain,
        "get_programs",
        mocker.AsyncMock(
            return_value=mocker.Mock(
                model_dump=mocker.Mock(
                    return_value={"programs": {"matches": [program]}}
                )
            )
        ),
    )
    graphql.get_observations = mocker.AsyncMock(
        return_value=_observations_page(["o-1"], has_more=False)
    )
    rest.get_atom_digests = mocker.AsyncMock(return_value="")

    await scheduler_domain.get_all(programs_list=["p-1"])

    rest.get_atom_digests.assert_awaited_once_with(["o-1"])
    rest.close.assert_not_called()


@pytest.mark.asyncio
async def test_get_all_reference_labels_skips_programs_without_reference(
    gpp_client,
    gpp_transport,
) -> None:
    """
    Ensure get_all_reference_labels lists only programs that have a reference.
    """
    gpp_transport.respond(
        {
            "programs": {
                "matches": [
                    {
                        "id": "p-1",
                        "reference": {
                            "__typename": "ScienceProgramReference",
                            "label": "G-2026A-0001-Q",
                        },
                    },
                    {"id": "p-2", "reference": None},
                ]
            }
        }
    )

    result = await gpp_client.scheduler.get_all_reference_labels(date="2026-10-01")

    assert result == [("G-2026A-0001-Q", "p-1")]
