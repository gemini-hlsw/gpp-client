__all__ = ["ReferenceManager"]

from typing import Any, Optional

from .....mixins import UpdateByIdMixin
from ....base_manager import BaseManager
from ....utils import resolve_single_program_identifier
from . import queries
from .....schema import enums


class ReferenceManager(UpdateByIdMixin, BaseManager):
    default_fields = queries.DEFAULT_FIELDS

    queries = {}

    resource_id_field = ""

    async def set_type(
        self,
        *,
        reference_type: str,
        reference_data: dict[str, Any],
        program_id: Optional[str] = None,
        proposal_reference: Optional[str] = None,
        program_reference: Optional[str] = None,
        fields: Optional[str] = None,
    ) -> dict[str, Any]:
        """Set a reference type (e.g., calibration, science, engineering) for a program.

        Parameters
        ----------
        reference_type : str
            One of the allowed reference types (e.g., 'calibration', 'science').
        reference_data : dict[str, Any]
            Data associated with the reference type.
        program_id : str, optional
            The program's unique ID.
        proposal_reference : str, optional
            Proposal reference string.
        program_reference : str, optional
            Program reference string.
        fields : str, optional
            Fields to return in the response.

        Returns
        -------
        dict[str, Any]
            Result of the mutation.
        """
        if reference_type not in {
            "science",
            "calibration",
            "commissioning",
            "engineering",
            "example",
            "library",
            "monitoring",
            "system",
        }:
            raise ValueError(f"Invalid reference_type: {reference_type}")

        resource_id_field, resource_id = resolve_single_program_identifier(
            program_id=program_id,
            program_reference=program_reference,
            proposal_reference=proposal_reference,
        )

        input_values: dict[str, Any] = {
            resource_id_field: resource_id,
            "SET": {reference_type: reference_data},
        }

        return await super().update_by_id(input_values=input_values, fields=fields)

    async def set_type_to_calibration(
        self,
        *,
        semester: str,
        instrument: str,
        program_id: Optional[str] = None,
        proposal_reference: Optional[str] = None,
        program_reference: Optional[str] = None,
        fields: Optional[str] = None,
    ) -> dict[str, Any]:
        """Set the program reference to a calibration program.

        Parameters
        ----------
        semester : str
            Semester string in the format YYYY[A|B], e.g., "2024A" or "24B".
        instrument : str
            One of the allowed instrument values.
        program_id : str, optional
            The unique program ID.
        proposal_reference : str, optional
            The proposal reference.
        program_reference : str, optional
            The program reference string.
        fields : str, optional
            Optional fields to include in the mutation response.

        Returns
        -------
        dict[str, Any]
            The result of the mutation.

        Raises
        ------
        ValueError
            If semester or instrument is invalid.
        """
        enums.Instrument(instrument)

        reference_data = {"semester": semester, "instrument": instrument}

        return await self.set_type(
            reference_type="calibration",
            reference_data=reference_data,
            program_id=program_id,
            proposal_reference=proposal_reference,
            program_reference=program_reference,
            fields=fields,
        )
