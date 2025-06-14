from collections import defaultdict
from typing import Any, List, Dict

from src.gpp_client import GPPClient
from src.gpp_client.api import WhereProgram, WhereObservation, WhereOrderObservationId


class Program:
    """ GPP Scheduler's program manager.
    The following version is a stripped and tailored version of a Program Manager
    that uses the regular client to get the program and observation information.
    """
    def __init__(self, client: GPPClient):
        self.client = client

    async def _traverse_for_observation(self, group: Dict[str, Any], obs_map: Dict[str, Any]) -> None:
        """Maps the information between the groups tree and the observations retrieved from a different query.
        Parameters
        ----------
        group: Dict[str, Any]
            Root group and subsequently groups
        obs_map: Dict[str, Any]
            Mapping of observation ids with observation raw data.

        Returns
        -------

        """
        obs = group.get("observation")
        if obs is not None:
            obs_id = obs["id"]
            obs_data = obs_map.get(obs_id)
            if obs_data is not None:
                group["observation"] = obs_data
            else:
                # No information on the ODB about the observation
                # but the structure remains in the program.
                # Put to None so observation doesn't get parse.
                group["observation"] = None

        if "elements" in group:
            for child in group["elements"]:
                await self._traverse_for_observation(child, obs_map)

    async def get_all(
            self,
            where: WhereProgram | None = None,
    ) -> List[dict[str, Any]]:
        """Fetch all programs with a complete group tree and observations."""

        response = await self.client.program.get_all(where=where)

        programs = response.get("matches", [])
        observations = []
        for program in programs:
            # Create root group
            root = {"name": "root", "elements": []}
            groups_elements_mapping = {}
            children_map = defaultdict(list)

            # Iterate for all elements
            groups_in_programs = program['allGroupElements']
            for g in groups_in_programs:
                parent_id = g.get('parentGroupId')

                if parent_id is None:
                    root['elements'].append(g)
                    obs = g.get('observation')
                    elem = obs or g.get('group')

                    groups_elements_mapping[elem['id']] = g
                    if elem == obs:
                        observations.append(elem['id'])
                else:
                    children_map[parent_id].append(g)

                for parent_id, children in children_map.items():
                    if parent_id in groups_elements_mapping:
                        groups_elements_mapping[parent_id]["elements"] = children
                    else:
                        # Ignore orphans for now, but check for this use case in the ODB
                        pass
            program["elements"] = root


        where_observation = WhereObservation(id=WhereOrderObservationId(in_=observations))
        obs_response = await self.client.observation.get_all(where=where_observation)
        obs_mapping = {o['id']: o for o in obs_response['matches'] }

        for program in programs:
            await self._traverse_for_observation(program["elements"], obs_mapping)

        return programs


