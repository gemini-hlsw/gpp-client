"""
Tests for the scheduler domain.
"""

from datetime import datetime, timezone
from types import SimpleNamespace

import pytest

from gpp_client.domains import scheduler as scheduler_module
from gpp_client.domains.scheduler import SchedulerDomain
from gpp_client.exceptions import GPPClientError
from gpp_client.generated.enums import ObservationWorkflowState
from gpp_client.generated.fragments import ObservationDetails, ProgramCore
from gpp_client.generated.get_scheduler_programs import (
    GetSchedulerPrograms,
    GetSchedulerProgramsPrograms,
    GetSchedulerProgramsProgramsMatches,
)
from gpp_client.generated.scheduler_observations_updates import (
    SchedulerObservationsUpdatesObscalcUpdateValue,
    SchedulerObservationsUpdatesObscalcUpdateValueProgram,
)
from tests.gpp_client.domains.helpers import _yield_events


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
    Build an observations page whose matches dump to their ID and empty
    scheduling constraints.
    """
    return SimpleNamespace(
        observations=SimpleNamespace(
            matches=[
                SimpleNamespace(
                    id=obs_id,
                    model_dump=lambda obs_id=obs_id: {
                        "id": obs_id,
                        "scheduling_constraints": {"timing_windows": []},
                    },
                )
                for obs_id in ids
            ],
            has_more=has_more,
        )
    )


def _mock_get_programs(mocker, programs: list[dict]):
    """
    Build a ``get_programs`` stand-in whose response dumps to ``programs``.
    """
    return mocker.AsyncMock(
        return_value=mocker.Mock(
            model_dump=mocker.Mock(return_value={"programs": {"matches": programs}})
        )
    )


@pytest.mark.asyncio
async def test_get_all_queries_every_tree_observation_by_id_in_batches(
    scheduler_domain: SchedulerDomain,
    rest,
    graphql,
    mocker,
    monkeypatch,
) -> None:
    """
    Ensure every observation in the program trees, nested groups included, is
    asked for by ID in capped batches with no OFFSET cursor, and every one the
    ODB returns lands in the tree and gets a sequence.
    """
    monkeypatch.setattr(scheduler_module, "ID_BATCH_SIZE", 2)
    programs = [
        {
            "id": "p-1",
            "all_group_elements": [
                {"parent_group_id": None, "observation": {"id": "o-1"}},
                {"parent_group_id": None, "group": {"id": "g-1"}},
                {"parent_group_id": "g-1", "observation": {"id": "o-2"}},
                # Not Ready/Ongoing, so the ODB never returns it.
                {"parent_group_id": "g-1", "observation": {"id": "o-3"}},
            ],
        },
        {
            "id": "p-2",
            "all_group_elements": [
                {"parent_group_id": None, "observation": {"id": "o-4"}},
                {"parent_group_id": None, "observation": {"id": "o-5"}},
            ],
        },
    ]
    ready = {"o-1", "o-2", "o-4", "o-5"}
    observation_calls = []

    async def get_observations(**kwargs):
        observation_calls.append(kwargs)
        asked = kwargs["where"].id.in_
        return _observations_page([i for i in asked if i in ready], has_more=False)

    mocker.patch.object(
        scheduler_domain, "get_programs", _mock_get_programs(mocker, programs)
    )
    graphql.get_observations = get_observations
    rest.get_atom_digests = mocker.AsyncMock(return_value="")

    result = await scheduler_domain.get_all(programs_list=["p-1", "p-2"])

    assert [c["where"].id.in_ for c in observation_calls] == [
        ["o-1", "o-2"],
        ["o-3", "o-4"],
        ["o-5"],
    ]
    for call in observation_calls:
        # No OFFSET or LIMIT, so there is no cursor that could stall.
        assert set(call) == {"where", "include_deleted"}
        assert call["where"].workflow.workflow_state.in_ == [
            ObservationWorkflowState.READY,
            ObservationWorkflowState.ONGOING,
        ]
    rest.get_atom_digests.assert_awaited_once_with(["o-1", "o-2", "o-4", "o-5"])

    p1_root, p2_root = (p["root"]["elements"] for p in result)
    assert p1_root[0]["observation"]["id"] == "o-1"
    assert [e["observation"]["id"] for e in p1_root[1]["group"]["elements"]] == ["o-2"]
    assert [e["observation"]["id"] for e in p2_root] == ["o-4", "o-5"]


@pytest.mark.asyncio
async def test_get_all_raises_when_an_observation_batch_is_incomplete(
    scheduler_domain: SchedulerDomain,
    rest,
    graphql,
    mocker,
) -> None:
    """
    Ensure a batch the ODB reports as cut short fails instead of dropping
    observations.
    """
    program = {
        "id": "p-1",
        "all_group_elements": [
            {"parent_group_id": None, "observation": {"id": "o-1"}},
        ],
    }
    mocker.patch.object(
        scheduler_domain, "get_programs", _mock_get_programs(mocker, [program])
    )
    graphql.get_observations = mocker.AsyncMock(
        return_value=_observations_page(["o-1"], has_more=True)
    )
    rest.get_atom_digests = mocker.AsyncMock(return_value="")

    with pytest.raises(GPPClientError, match="observations"):
        await scheduler_domain.get_all(programs_list=["p-1"])

    rest.get_atom_digests.assert_not_awaited()


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
async def test_get_all_moves_timing_windows_to_observation_root(
    scheduler_domain: SchedulerDomain,
    rest,
    graphql,
    mocker,
) -> None:
    """
    Ensure each observation carries its scheduling-constraint timing windows at
    the root, replacing the deprecated root field.
    """
    window = {"inclusion": "INCLUDE", "start_utc": "2026-10-19 00:00:00", "end": None}
    observation = SimpleNamespace(
        id="o-1",
        model_dump=lambda: {
            "id": "o-1",
            "timing_windows": [],
            "scheduling_constraints": {
                "too_activation": "NONE",
                "timing_windows": [window],
            },
        },
    )
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
        return_value=SimpleNamespace(
            observations=SimpleNamespace(matches=[observation], has_more=False)
        )
    )
    rest.get_atom_digests = mocker.AsyncMock(return_value="")

    result = await scheduler_domain.get_all(programs_list=["p-1"])

    obs = result[0]["root"]["elements"][0]["observation"]
    assert obs["timing_windows"] == [window]
    assert obs["scheduling_constraints"] == {"too_activation": "NONE"}


@pytest.mark.asyncio
async def test_get_programs_queries_listed_ids_in_batches(
    scheduler_domain: SchedulerDomain,
    graphql,
    mocker,
    monkeypatch,
) -> None:
    """
    Ensure listed program IDs are asked for in capped batches, without repeats,
    and every batch is merged into one result.
    """
    monkeypatch.setattr(scheduler_module, "ID_BATCH_SIZE", 2)
    graphql.get_scheduler_programs = mocker.AsyncMock(
        side_effect=[
            _programs_page(["p-1", "p-2"], has_more=False),
            _programs_page(["p-3"], has_more=False),
        ]
    )

    result = await scheduler_domain.get_programs(
        programs_list=["p-1", "p-2", "p-2", "p-3"]
    )

    assert [p.id for p in result.programs.matches] == ["p-1", "p-2", "p-3"]
    assert result.programs.has_more is False
    assert graphql.get_scheduler_programs.await_args_list == [
        mocker.call(programs_list=["p-1", "p-2"]),
        mocker.call(programs_list=["p-3"]),
    ]


@pytest.mark.asyncio
async def test_get_programs_without_a_list_makes_one_query(
    scheduler_domain: SchedulerDomain,
    graphql,
    mocker,
) -> None:
    """
    Ensure all active programs come from one query, returned as is.
    """
    page = _programs_page(["p-1"], has_more=False)
    graphql.get_scheduler_programs = mocker.AsyncMock(return_value=page)

    result = await scheduler_domain.get_programs()

    assert result is page
    graphql.get_scheduler_programs.assert_awaited_once_with(programs_list=None)


@pytest.mark.parametrize("programs_list", [None, ["p-1", "p-2"]])
@pytest.mark.asyncio
async def test_get_programs_raises_when_the_odb_leaves_programs_out(
    scheduler_domain: SchedulerDomain,
    graphql,
    mocker,
    programs_list,
) -> None:
    """
    Ensure a result the ODB reports as cut short fails instead of dropping
    programs.
    """
    graphql.get_scheduler_programs = mocker.AsyncMock(
        return_value=_programs_page(["p-1"], has_more=True)
    )

    with pytest.raises(GPPClientError, match="programs"):
        await scheduler_domain.get_programs(programs_list=programs_list)


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
    since = datetime(2026, 7, 15, 9, 0, tzinfo=timezone.utc)

    result = await scheduler_domain.get_visibility_changes(since)

    rest.get_visibility_changes.assert_awaited_once_with(since)
    assert result.observation_ids == frozenset({"o-123"})
    assert result.target_ids == frozenset({"t-456"})
    assert result.max_timestamp == datetime(2026, 7, 15, 11, 30, tzinfo=timezone.utc)


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
            datetime(2026, 7, 15, 9, 0, tzinfo=timezone.utc)
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
        datetime(2026, 7, 15, 9, 0, tzinfo=timezone.utc)
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
async def test_subscribe_to_calculation_updates_yields_executable_events(
    scheduler_domain: SchedulerDomain,
    graphql,
    mocker,
) -> None:
    """
    Ensure only executable observation updates are requested and every event
    is yielded.
    """
    events = [SimpleNamespace(id=1), SimpleNamespace(id=2)]
    graphql.scheduler_observations_updates = mocker.Mock(
        return_value=_yield_events(events)
    )

    result = [
        event async for event in scheduler_domain.subscribe_to_calculation_updates()
    ]

    assert result == events
    graphql.scheduler_observations_updates.assert_called_once_with(executable_only=True)


def test_calculation_update_observation_matches_get_all_observations() -> None:
    """
    Ensure an updated observation carries the same fields as the observations
    in get_all, plus the program active dates the scheduler reads.
    """
    assert issubclass(
        SchedulerObservationsUpdatesObscalcUpdateValue, ObservationDetails
    )

    # Selecting program again in the subscription replaces the fragment's
    # program, so ProgramCore must still be there.
    program = SchedulerObservationsUpdatesObscalcUpdateValueProgram
    assert issubclass(program, ProgramCore)
    assert "active" in program.model_fields
