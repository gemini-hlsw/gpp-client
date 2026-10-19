"""
Module for retrieving scheduler information.
"""

from __future__ import annotations

__all__ = ["SchedulerDomain"]

from collections.abc import AsyncIterator, Awaitable, Callable
from datetime import datetime
from typing import TYPE_CHECKING, Any

from gpp_client.domains.base import BaseDomain
from gpp_client.rest.models import VisibilityChanges, parse_visibility_changes

if TYPE_CHECKING:
    from gpp_client.generated import SchedulerObservationsUpdates
    from gpp_client.generated.get_scheduler_all_programs_id import (
        GetSchedulerAllProgramsId,
    )
    from gpp_client.generated.get_scheduler_programs import GetSchedulerPrograms


# Each program carries its full group tree, so large pages are heavy for the ODB.
PROGRAMS_PAGE_SIZE = 1000
OBSERVATIONS_PAGE_SIZE = 1000


class SchedulerDomain(BaseDomain):
    """
    Domain for retrieving scheduler information.
    """

    @staticmethod
    async def _fetch_all_pages(
        fetch_page: Callable[[str | None, int], Awaitable[Any]],
        page_size: int,
    ) -> list[Any]:
        """
        Walk an ``OFFSET``/``LIMIT`` selection one page at a time and return
        every match.

        Parameters
        ----------
        fetch_page : Callable[[str | None, int], Awaitable[Any]]
            Coroutine taking ``offset`` and ``limit`` and returning a select
            result with ``matches`` and ``has_more``.
        page_size : int
            Number of matches requested per page. Must be at least 2.

        Returns
        -------
        list[Any]
            Every match across all pages, without repeats.

        Raises
        ------
        ValueError
            If ``page_size`` is lower than 2.
        """
        # OFFSET is inclusive, so every page after the first repeats the previous
        # page's last match. A page of 1 would never advance.
        if page_size < 2:
            raise ValueError(f"page_size must be at least 2, got {page_size}.")

        matches = []
        offset = None
        while True:
            result = await fetch_page(offset, page_size)
            page_matches = result.matches
            if offset is not None and page_matches and page_matches[0].id == offset:
                page_matches = page_matches[1:]
            matches.extend(page_matches)

            if not result.has_more or not page_matches:
                return matches
            offset = page_matches[-1].id

    async def get_programs(
        self,
        *,
        programs_list: list[str] | None = None,
        page_size: int = PROGRAMS_PAGE_SIZE,
    ) -> GetSchedulerPrograms:
        """
        Get scheduler programs, fetching every page so the result reads as a
        single query.

        Parameters
        ----------
        programs_list : list[str] | None, optional
            Optional list of program IDs to restrict the result set.
        page_size : int, optional
            Number of programs requested per page. Must be at least 2.

        Returns
        -------
        GetSchedulerPrograms
            The generated GraphQL response model holding every matching program.

        Raises
        ------
        ValueError
            If ``page_size`` is lower than 2.
        """

        async def fetch_page(offset: str | None, limit: int) -> Any:
            page = await self._graphql.get_scheduler_programs(
                programs_list=programs_list, offset=offset, limit=limit
            )
            return page.programs

        from gpp_client.generated.get_scheduler_programs import (
            GetSchedulerPrograms,
            GetSchedulerProgramsPrograms,
        )

        matches = await self._fetch_all_pages(fetch_page, page_size)
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

        from gpp_client.generated.input_types import (
            ObservationWorkflowState,
            WhereCalculatedObservationWorkflow,
            WhereObservation,
            WhereOptionEqObservingModeType,
            WhereOrderObservationWorkflowState,
            WhereOrderProgramId,
            WhereProgram,
        )

        where_observation = WhereObservation(
            program=WhereProgram(
                id=WhereOrderProgramId(in_=[p["id"] for p in programs])
            ),
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
        )

        # Get observation data, only once every program page is in.
        async def fetch_observations_page(offset: str | None, limit: int) -> Any:
            page = await self._graphql.get_observations(
                where=where_observation,
                offset=offset,
                limit=limit,
                include_deleted=False,
            )
            return page.observations

        obs_matches = await self._fetch_all_pages(
            fetch_observations_page, OBSERVATIONS_PAGE_SIZE
        )
        obs_mapping = {o.id: o.model_dump() for o in obs_matches}

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
            Programs without a reference are left out.
        """
        today = datetime.today().date().isoformat() if date is None else date
        response = await self.get_program_ids(today=today)
        return [
            (p.reference.label, p.id)
            for p in response.programs.matches
            if p.reference is not None
        ]

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
        GPPEnvironmentError
            If the selected environment does not serve the endpoint (404).
        aiohttp.ClientError
            For other HTTP errors, connection failures, or timeouts.
        """
        body = await self._rest.get_visibility_changes(since)
        return parse_visibility_changes(body)

    async def subscribe_to_calculation_updates(
        self,
    ) -> AsyncIterator[SchedulerObservationsUpdates]:
        """
        Subscribe to observation calculation update events with the
        execution flag set to true so only executed events are sent.

        Yields
        ------
        SchedulerObservationsUpdates
            Observation calculation update events.
        """
        async for event in self._graphql.scheduler_observations_updates(
            executable_only=True
        ):
            yield event
