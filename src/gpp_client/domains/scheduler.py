"""
Module for retrieving scheduler information.
"""

__all__ = ["SchedulerDomain"]

from datetime import datetime
from typing import Any

from gpp_client.domains.base import BaseDomain
from gpp_client.generated.get_scheduler_all_programs_id import (
    GetSchedulerAllProgramsId,
)
from gpp_client.generated.get_scheduler_programs import GetSchedulerPrograms
from gpp_client.generated.input_types import (
    ObservationWorkflowState,
    WhereCalculatedObservationWorkflow,
    WhereObservation,
    WhereOrderObservationId,
    WhereOrderObservationWorkflowState,
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
        Get scheduler programs.

        Parameters
        ----------
        programs_list : list[str] | None, optional
            Optional list of program IDs to restrict the result set.

        Returns
        -------
        GetSchedulerPrograms
            The generated GraphQL response model.
        """
        return await self._graphql.get_scheduler_programs(programs_list=programs_list)

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
            (
                obs_id,
                atom_idx,
                atom_id,
                observe_class,
                time_estimate,
                step_types,
                lamp_types,
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
                }
            )

        return obs_atoms_mapping

    def _traverse_for_observation(
        self,
        node: dict[str, Any],
        obs_map: dict[str, Any],
        obs_sequence: dict[str, list],
    ) -> None:
        """
        Maps the information between the groups tree and the observations retrieved
        from a different query.

        Parameters
        ----------
        node: dict[str, Any]
            Root group and subsequently groups
        obs_map: dict[str, Any]
            Mapping of observation ids with observation raw data.
        obs_sequence: dict[str, list]
            Mapping of the atoms sequence with the observation id.
        """
        obs = node.get("observation")
        group = node.get("group")
        if obs is not None:
            obs_id = obs["id"]
            obs_data = obs_map.get(obs_id)
            if obs_data is not None:
                obs_data["sequence"] = obs_sequence.get(obs_id)
                node["observation"] = obs_data
            else:
                # No information on the ODB about the observation but the structure
                # remains in the program.
                # Put to None so observation doesn't get parse.
                node["observation"] = None

        elif group is not None:
            if group.get("elements"):
                for child in group["elements"]:
                    self._traverse_for_observation(child, obs_map, obs_sequence)
            else:
                # Empty groups like Calibration might add elements later.
                group["elements"] = []

        else:
            # is the root
            for child in node["elements"]:
                self._traverse_for_observation(child, obs_map, obs_sequence)

    async def get_all(
        self,
        programs_list: list | None = None,
    ) -> list[dict[str, Any]]:
        """
        Fetch all programs with a complete group tree and observations.

        Parameters
        ----------
        programs_list : list, optional
            Optional filtering clause.

        Returns
        -------
        list[dict[str, Any]]
            A list of dictionaries representing the programs and their elements.
        """

        if not programs_list:
            programs_list = [
                p.id for p in (await self.get_program_ids()).programs.matches
            ]

        response = await self.get_programs(programs_list=programs_list)
        response = response.model_dump()
        programs = response["programs"].get("matches", [])
        observations = []
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
                    if elem == obs:
                        observations.append(elem["id"])
                else:
                    children_map.setdefault(parent_id, []).append(g)
                    group = g.get("group")
                    if group:
                        # Subgroup that can contain children of their own.
                        groups_elements_mapping[group["id"]] = g
                    else:
                        observations.append(g["observation"]["id"])

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

        # If is in the list and status is Ready or OnGoing.
        where_observation = WhereObservation(
            id=WhereOrderObservationId(in_=observations),
            workflow=WhereCalculatedObservationWorkflow(
                workflow_state=WhereOrderObservationWorkflowState(
                    in_=[
                        ObservationWorkflowState.READY,
                        ObservationWorkflowState.ONGOING,
                    ]
                )
            ),
        )

        # Get observation data
        obs_response = await self._graphql.get_observations(
            where=where_observation, include_deleted=False
        )
        obs_payload = obs_response.observations.model_dump()
        obs_mapping = {o["id"]: o for o in obs_payload["matches"]}

        # Get sequence
        async with self._rest as client:
            atom_digest_response = (await client._get_atom_digests(observations)).split(
                "\n"
            )

        obs_atoms_mapping = self._parse_atom_digest(atom_digest_response)

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
