__all__ = ["ProgramCoordinator"]

from typing import Any, TypeAlias


from ....api import (
    ObservationWorkflowState,
    WhereCalculatedObservationWorkflow,
    WhereObservation,
    WhereOrderObservationId,
    WhereOrderObservationWorkflowState,
    WhereProgram,
    GetSequenceObservationsMatchesExecutionAtomRecordsMatchesStepsMatches,
    GetSequenceObservationsMatchesExecutionConfig,
    GraphQLClientGraphQLMultiError,
)
from ....coordinator import BaseCoordinator


Step: TypeAlias = GetSequenceObservationsMatchesExecutionAtomRecordsMatchesStepsMatches
Config: TypeAlias = GetSequenceObservationsMatchesExecutionConfig


class ProgramCoordinator(BaseCoordinator):
    """
    Combines multiple managers to return views of a program and its observations.
    """

    @staticmethod
    def _check_instrument(instrument: str, element: Step | Config):
        match instrument:
            case "flamingos2":
                return element.flamingos2
            case "gmos_south":
                return element.gmos_south
            case "gmos_north":
                return element.gmos_north
            case _:
                raise RuntimeError(f"Unrecognized instrument: {instrument}")

    def _parse_atom_digest(self, atom_digest_response: list) -> dict:
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
            ) = atom_digest.split()
            obs_atoms_mapping[obs_id].setdefault(obs_id, [])
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

    async def _traverse_for_observation(
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
                obs_data["sequence"] = obs_sequence.get(obs_id)
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
                    await self._traverse_for_observation(child, obs_map, obs_sequence)
            else:
                # Empty groups like Calibration might add elements later.
                group["elements"] = []

        else:
            # is the root
            for child in node["elements"]:
                await self._traverse_for_observation(child, obs_map, obs_sequence)

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

        obs_response = await self.client.observation.get_all(where=where_observation)
        atom_digest_response = (
            await self.client.restapi.get_atom_digests(observations)
        ).split("\n")

        if len(atom_digest_response) != len(obs_response["matches"]):
            print("Missmatch in observation response and atom digest response")
        obs_atoms_mapping = self._parse_atom_digest(atom_digest_response)
        print(obs_atoms_mapping)

        obs_mapping = {o["id"]: o for o in obs_response["matches"]}
        obs_sequence_mapping = {}
        # Get sequence
        for obs in obs_mapping.keys():
            try:
                number_executed_atoms = 0
                response = await self.client._client.get_sequence(obs)
                # print(response)
                matches = response.observations.matches[
                    0
                ].execution.atom_records.matches
                rows = []
                for count, atom in enumerate(matches):
                    number_executed_atoms = count
                    instrument_name = atom.instrument.lower()
                    for step in atom.steps.matches:
                        ic = self._check_instrument(instrument_name, step)
                        gc = ic.grating_config
                        sc = step.step_config
                        tc = step.telescope_config
                        gcal = None
                        if (
                            sc.step_type == "GCAL"
                        ):  # combine the GCAL lamps into a single field
                            gcal = sc.continuum if sc.continuum is not None else ""
                            gcal += ",".join(sc.arcs) if len(sc.arcs) > 0 else ""
                        rows.append(
                            {
                                "atom": count,
                                "breakpoint": None,
                                "observe_class": step.observe_class,
                                "type": sc.step_type,
                                "gcal": gcal,
                                "qa": step.qa_state,
                                "exposure": ic.exposure.seconds,
                                "p": tc.offset.p.arcseconds
                                if hasattr(tc, "offset")
                                else None,
                                "q": tc.offset.q.arcseconds
                                if hasattr(tc, "offset")
                                else None,
                                "wavelength": ic.central_wavelength.nanometers,
                                "fpu": getattr(
                                    ic.fpu, "builtin", None
                                ),  # TODO: support MOS & IFU
                                "grating": getattr(gc, "grating", None),
                                "filter": ic.filter,
                                "x_bin": ic.readout.x_bin,
                                "y_bin": ic.readout.y_bin,
                                "roi": ic.roi,
                                "execution_state": step.execution_state,
                                "duration": step.interval.duration.seconds,
                            }
                        )
                config = response.observations.matches[0].execution.config
                config_by_instrument = self._check_instrument(
                    config.instrument.lower(), config
                )
                atoms = []

                if hasattr(config_by_instrument.acquisition, "next_atom"):
                    atoms.append(config_by_instrument.acquisition.next_atom)
                if hasattr(config_by_instrument.acquisition, "possible_future"):
                    atoms += config_by_instrument.acquisition.possible_future
                if hasattr(config_by_instrument.science, "next_atom"):
                    atoms.append(config_by_instrument.science.next_atom)
                if hasattr(config_by_instrument.science, "possible_future"):
                    atoms += config_by_instrument.science.possible_future

                for count, atom in enumerate(atoms):
                    for step in atom.steps:
                        tc = step.telescope_config
                        sc = step.step_config
                        ic = step.instrument_config
                        gc = ic.grating_config
                        gcal = None
                        if (
                            sc.step_type == "GCAL"
                        ):  # combine the GCAL lamps into a single field
                            gcal = sc.continuum if sc.continuum is not None else ""
                            gcal += ",".join(sc.arcs) if len(sc.arcs) > 0 else ""

                        rows.append(
                            {
                                "atom": count + 1 + number_executed_atoms,
                                "breakpoint": step.breakpoint,
                                "observe_class": step.observe_class,
                                "type": sc.step_type,
                                "gcal": gcal,
                                "qa": None,
                                "exposure": ic.exposure.seconds,
                                "p": tc.offset.p.arcseconds
                                if hasattr(tc, "offset")
                                else None,
                                "q": tc.offset.q.arcseconds
                                if hasattr(tc, "offset")
                                else None,
                                "wavelength": ic.central_wavelength.nanometers,
                                "fpu": getattr(
                                    ic.fpu, "builtin", None
                                ),  # TODO: support MOS & IFU
                                "grating": getattr(gc, "grating", None),
                                "filter": ic.filter,
                                "x_bin": ic.readout.x_bin,
                                "y_bin": ic.readout.y_bin,
                                "roi": ic.roi,
                                "execution_state": "NOT_STARTED",
                                "duration": step.estimate.total.seconds,
                            }
                        )
                obs_sequence_mapping[obs] = rows

            except GraphQLClientGraphQLMultiError as e:
                print(e)

        for program in programs:
            await self._traverse_for_observation(
                program["root"], obs_mapping, obs_sequence_mapping
            )

        return programs
