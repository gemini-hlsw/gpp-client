"""
Module for retrieving scheduler information.
"""

__all__ = ["SchedulerDomain"]

from datetime import datetime
from typing import Any, AsyncIterator, Iterator

from gpp_client.domains.base import BaseDomain
from gpp_client.exceptions import GPPClientError
from gpp_client.rest.models import VisibilityChanges, parse_visibility_changes
from gpp_client.generated import (
    SchedulerObservationsUpdates,
    SchedulerExecutedEvents,
    WhereOptionEqObservingModeType,
)
from gpp_client.generated.get_scheduler_all_programs_id import (
    GetSchedulerAllProgramsId,
)
from gpp_client.generated.get_scheduler_programs import (
    GetSchedulerPrograms,
    GetSchedulerProgramsPrograms,
)
from gpp_client.generated.input_types import (
    ObservationWorkflowState,
    WhereCalculatedObservationWorkflow,
    WhereObservation,
    WhereOrderObservationId,
    WhereOrderObservationWorkflowState,
)

# The ODB returns at most this many matches per select. Asking for at most this
# many IDs at a time means a batch can never be cut short.
ID_BATCH_SIZE = 1000


def _id_batches(ids: list[str]) -> Iterator[list[str]]:
    """
    Split IDs into batches no larger than the ODB select cap, dropping repeats.

    Parameters
    ----------
    ids : list[str]
        IDs to split, in the order to query them.

    Yields
    ------
    list[str]
        The next batch of at most ``ID_BATCH_SIZE`` unique IDs.
    """
    unique = list(dict.fromkeys(ids))
    for start in range(0, len(unique), ID_BATCH_SIZE):
        yield unique[start : start + ID_BATCH_SIZE]


def _require_complete(result: Any, what: str) -> None:
    """
    Fail when the ODB says it left matches out.

    Parameters
    ----------
    result : Any
        Select result with ``matches`` and ``has_more``.
    what : str
        Plural name of the selected items, for the message.

    Raises
    ------
    GPPClientError
        If ``result.has_more`` is set.
    """
    # The scheduler must see every observation. A partial answer is worse than
    # no answer, so stop instead of returning it.
    if result.has_more:
        raise GPPClientError(
            f"ODB returned {len(result.matches)} {what} and reported more that "
            "were left out; refusing to return an incomplete result."
        )


class SchedulerDomain(BaseDomain):
    """
    Domain for retrieving scheduler information.
    """

    async def get_programs(
        self,
        *,
        programs_list: list[str] | None = None,
    ) -> GetSchedulerPrograms:
        """
        Get active scheduler programs.

        Given a list, the IDs are queried in batches that the ODB can always
        answer in full, so every active program in the list comes back. Without
        a list, all active programs come from a single query.

        Parameters
        ----------
        programs_list : list[str] | None, optional
            Optional list of program IDs to restrict the result set. Inactive
            programs in the list are left out.

        Returns
        -------
        GetSchedulerPrograms
            The generated GraphQL response model holding every matching program.

        Raises
        ------
        GPPClientError
            If the ODB reports matches it did not return.
        """
        if programs_list is None:
            response = await self._graphql.get_scheduler_programs(programs_list=None)
            _require_complete(response.programs, "programs")
            return response

        matches = []
        for batch in _id_batches(programs_list):
            response = await self._graphql.get_scheduler_programs(programs_list=batch)
            _require_complete(response.programs, "programs")
            matches.extend(response.programs.matches)
        return GetSchedulerPrograms(
            programs=GetSchedulerProgramsPrograms(matches=matches, has_more=False)
        )

    async def get_program_ids(
        self,
        *,
        today: str | None = None,
    ) -> GetSchedulerAllProgramsId:
        """
        Get all scheduler program IDs.

        Parameters
        ----------
        today : str | None, optional
            Optional date string to filter programs by today's date.

        Returns
        -------
        GetSchedulerAllProgramsId
            The generated GraphQL response model.
        """
        return await self._graphql.get_scheduler_all_programs_id(today=today)

    @staticmethod
    def _parse_atom_digest(atom_digest_response: list) -> dict:
        """
        Parses the plain text response from the REST API endpoint.

        Parameters
        ----------
        atom_digest_response : list
            a string stream of atom information from different set of observations.

        Returns
        -------
        dict
            observation id and a sequence of atoms.
        """
        obs_atoms_mapping = {}
        for atom_digest in atom_digest_response:
            if not atom_digest.strip():
                continue
            (
                obs_id,
                atom_idx,
                atom_id,
                observe_class,
                time_estimate,
                step_types,
                lamp_types,
                step_index,
                step_count,
            ) = atom_digest.split("\t")
            obs_atoms_mapping.setdefault(obs_id, [])
            obs_atoms_mapping[obs_id].append(
                {
                    "atom_idx": atom_idx,
                    "atom_id": atom_id,
                    "observe_class": observe_class,
                    "time_estimate": time_estimate,
                    "step_types": step_types,
                    "lamp_types": lamp_types,
                    "step_index": step_index,
                    "step_count": step_count,
                }
            )

        return obs_atoms_mapping

    @staticmethod
    def _move_timing_windows_to_root(obs: dict[str, Any]) -> dict[str, Any]:
        """
        Move the timing windows out of the scheduling constraints to the root of
        the observation, where the scheduler reads them.

        Parameters
        ----------
        obs : dict[str, Any]
            Dumped observation holding ``scheduling_constraints``.

        Returns
        -------
        dict[str, Any]
            The same observation, with ``timing_windows`` at its root.
        """
        obs["timing_windows"] = obs["scheduling_constraints"].pop("timing_windows")
        return obs

    def _traverse_for_observation(
        self,
        node: dict[str, Any],
        obs_map: dict[str, Any],
        obs_sequence: dict[str, list],
    ) -> bool:
        """
        Maps the information between the groups tree and the observations retrieved
        from a different query, dropping the elements that carry no observation.

        Parameters
        ----------
        node: dict[str, Any]
            Root group and subsequently groups
        obs_map: dict[str, Any]
            Mapping of observation ids with observation raw data.
        obs_sequence: dict[str, list]
            Mapping of the atoms sequence with the observation id.

        Returns
        -------
        bool
            ``True`` if the node was filled with observation data, ``False`` if it
            is an observation missing from the ODB response or a group left empty
            once its children were trimmed.
        """
        obs = node.get("observation")
        group = node.get("group")
        if obs is not None:
            obs_id = obs["id"]
            obs_data = obs_map.get(obs_id)
            if obs_data is None:
                # No information on the ODB about the observation but the structure
                # remains in the program.
                # Put to None so observation doesn't get parse.
                node["observation"] = None
                return False

            obs_data["sequence"] = obs_sequence.get(obs_id)
            node["observation"] = obs_data
            return True

        if group is not None:
            group["elements"] = [
                child
                for child in group.get("elements") or []
                if self._traverse_for_observation(child, obs_map, obs_sequence)
            ]
            return bool(group["elements"])

        # is the root
        node["elements"] = [
            child
            for child in node["elements"]
            if self._traverse_for_observation(child, obs_map, obs_sequence)
        ]
        return bool(node["elements"])

    async def get_all(
        self,
        programs_list: list | None = None,
        exclude_programs: list[str] | None = None,
    ) -> list[dict[str, Any]]:
        """
        Fetch all programs with a complete group tree and observations.

        Parameters
        ----------
        programs_list : list, optional
            Optional filtering clause.
        exclude_programs : list[str], optional
            Program IDs to skip, e.g. one whose observations the ODB cannot
            generate a sequence for, which otherwise fails the whole query.

        Returns
        -------
        list[dict[str, Any]]
            A list of dictionaries representing the programs and their elements.

        Raises
        ------
        GPPClientError
            If the ODB reports programs or observations it did not return.
        """

        if not programs_list:
            programs_list = [
                p.id for p in (await self.get_program_ids()).programs.matches
            ]
        if exclude_programs:
            excluded = set(exclude_programs)
            programs_list = [p for p in programs_list if p not in excluded]

        response = await self.get_programs(programs_list=programs_list)
        response = response.model_dump()
        programs = response["programs"].get("matches", [])
        for program in programs:
            # Create root group.
            root = {"name": "root", "elements": []}
            groups_elements_mapping = {}
            children_map = {}

            # Iterate for all elements.
            groups_in_programs = program["all_group_elements"]
            for g in groups_in_programs:
                parent_id = g.get("parent_group_id")

                if parent_id is None:
                    # Parent group or root observation.
                    root["elements"].append(g)
                    obs = g.get("observation")
                    elem = obs or g.get("group")

                    groups_elements_mapping[elem["id"]] = g
                else:
                    children_map.setdefault(parent_id, []).append(g)
                    group = g.get("group")
                    if group:
                        # Subgroup that can contain children of their own.
                        groups_elements_mapping[group["id"]] = g

            for parent_id, children in children_map.items():
                if parent_id in groups_elements_mapping:
                    groups_elements_mapping[parent_id]["group"].setdefault(
                        "elements", []
                    )
                    groups_elements_mapping[parent_id]["group"]["elements"] = children

                else:
                    print(f"Parent {parent_id} not found in mapping")
                    # Ignore orphans for now, but check for this use case in the ODB.
                    pass
            program["root"] = root

        tree_obs_ids = [
            g["observation"]["id"]
            for program in programs
            for g in program["all_group_elements"]
            if g.get("observation")
        ]
        obs_mapping = {}
        # Query on 1000 observation ids (max pagination limit)
        for batch in _id_batches(tree_obs_ids):
            obs_response = await self._graphql.get_observations(
                where=WhereObservation(
                    id=WhereOrderObservationId(in_=batch),
                    workflow=WhereCalculatedObservationWorkflow(
                        workflow_state=WhereOrderObservationWorkflowState(
                            in_=[
                                ObservationWorkflowState.READY,
                                ObservationWorkflowState.ONGOING,
                            ]
                        )
                    ),
                    observing_mode_type=WhereOptionEqObservingModeType(
                        is_null=False,
                    ),
                ),
                include_deleted=False,
            )
            _require_complete(obs_response.observations, "observations")
            for o in obs_response.observations.matches:
                obs_mapping[o.id] = self._move_timing_windows_to_root(o.model_dump())

        # Get sequence for filtered observations (READY/ONGOING)
        if obs_mapping:
            atom_digest_response = (
                await self._rest.get_atom_digests(list(obs_mapping))
            ).split("\n")
            obs_atoms_mapping = self._parse_atom_digest(atom_digest_response)
        else:
            obs_atoms_mapping = {}

        # Fill groups with the data above.
        for program in programs:
            self._traverse_for_observation(
                program["root"], obs_mapping, obs_atoms_mapping
            )
            del program["all_group_elements"]  # remove flatten tree

        return programs

    async def get_all_reference_labels(
        self,
        date: str | None = None,
    ) -> list[tuple[str, str]]:
        """
        Get all scheduler program reference labels and IDs.

        Parameters
        ----------
        date : str | None, optional
            Date to use for the active-end filter. Defaults to today's date.

        Returns
        -------
        list[tuple[str, str]]
            List of tuples containing the program reference label and ID.
        """
        today = datetime.today().date().isoformat() if date is None else date
        response = await self.get_program_ids(today=today)
        return [(p.reference.label, p.id) for p in response.programs.matches]

    async def get_visibility_changes(self, since: datetime) -> VisibilityChanges:
        """
        Get observations and targets with visibility changes since a time.

        Queries the ODB ``/scheduler/visibility-changes`` REST endpoint, which
        reports entities whose visibility-relevant inputs changed at or after
        ``since``.

        Parameters
        ----------
        since : datetime
            Return entities changed at or after this time. Naive datetimes are
            assumed to be UTC.

        Returns
        -------
        VisibilityChanges
            Changed observation and target GIDs plus the latest change
            timestamp reported by the endpoint.

        Raises
        ------
        aiohttp.ClientError
            For HTTP errors, connection failures, or timeouts.
        """
        body = await self._rest.get_visibility_changes(since)
        return parse_visibility_changes(body)

    async def subscribe_to_calculation_updates(
        self,
    ) -> AsyncIterator[SchedulerObservationsUpdates]:
        """
        Subscribe to observation calculation update events with the
        execution flag set to true so only executed events are sent.

        Each event's observation carries the same fields as the observations in
        ``get_all``, plus its program's active dates and its observation time.
        Unlike ``get_all``, the timing windows stay under
        ``scheduling_constraints`` and no atom sequence is attached.

        Yields
        ------
        SchedulerObservationsUpdates
            Observation calculation update events.
        """
        async for event in self._graphql.scheduler_observations_updates(
            executable_only=True
        ):
            yield event

    async def subscribe_to_executed_events(
        self,
    ) -> AsyncIterator[SchedulerExecutedEvents]:
        """
        Subscribe to executed events ``(SLEW, SEQUENCE)`` to help the Scheduler
        guide executions.

        Yields
        ------
        SchedulerExecutedEvents
            Events added by Observe, either ``SEQUENCE`` or ``SLEW``.
        """
        async for event in self._graphql.scheduler_executed_events():
            yield event
