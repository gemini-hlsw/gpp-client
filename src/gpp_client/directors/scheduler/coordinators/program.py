__all__ = ["ProgramCoordinator"]

from typing import Any

from ....api import (
    ObservationWorkflowState,
    WhereCalculatedObservationWorkflow,
    WhereObservation,
    WhereOrderObservationId,
    WhereOrderObservationWorkflowState,
    WhereProgram,
)
from ....coordinator import BaseCoordinator


class ProgramCoordinator(BaseCoordinator):
    """
    Combines multiple managers to return views of a program and its observations.
    """

    async def _traverse_for_observation(
        self, node: dict[str, Any], obs_map: dict[str, Any]
    ) -> None:
        """
        Maps the information between the groups tree and the observations retrieved
        from a different query.

        Parameters
        ----------
        group: dict[str, Any]
            Root group and subsequently groups
        obs_map: dict[str, Any]
            Mapping of observation ids with observation raw data.
        """
        obs = node.get("observation")
        group = node.get("group")
        if obs is not None:
            obs_id = obs["id"]
            obs_data = obs_map.get(obs_id)
            if obs_data is not None:
                node["observation"] = obs_data
            else:
                # No information on the ODB about the observation but the structure
                # remains in the program.
                # Put to None so observation doesn't get parse.
                node["observation"] = None
                # print(obs)
                pass
        elif group is not None:
            if group.get("elements"):
                for child in group["elements"]:
                    await self._traverse_for_observation(child, obs_map)
            else:
                # Empty groups like Calibration might add elements later.
                group["elements"] = []

        else:
            # is the root
            for child in node["elements"]:
                await self._traverse_for_observation(child, obs_map)

    async def get_all(
        self,
        where: WhereProgram | None = None,
    ) -> list[dict[str, Any]]:
        """
        Fetch all programs with a complete group tree and observations.

        Parameters
        ----------
        where : WhereProgram, optional
            Optional filtering clause.

        Returns
        -------
        list[dict[str, Any]]
            A list of dictionaries representing the programs and their elements.
        """

        response = await self.client.program.get_all(where=where)

        programs = response.get("matches", [])
        observations = []
        for program in programs:
            # Create root group.
            root = {"name": "root", "elements": []}
            groups_elements_mapping = {}
            children_map = {}

            # Iterate for all elements.
            groups_in_programs = program["allGroupElements"]
            for g in groups_in_programs:
                parent_id = g.get("parentGroupId")

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
                        # Sub-group that can contain children of their own.
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

        obs_response = await self.client.observation.get_all(where=where_observation)
        obs_mapping = {o["id"]: o for o in obs_response["matches"]}

        for program in programs:
            await self._traverse_for_observation(program["root"], obs_mapping)

        return programs
