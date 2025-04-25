__all__ = ["ProgramManager"]

from typing import Any, Optional

from ...mixins import CreateMixin, GetBatchMixin, GetByIdMixin
from ..base_manager import BaseManager
from ..utils import normalize_iso_datetime, resolve_single_program_identifier
from . import queries


class ProgramManager(CreateMixin, GetByIdMixin, GetBatchMixin, BaseManager):
    default_fields = queries.DEFAULT_FIELDS

    queries = {
        "create": queries.CREATE_PROGRAM,
        "get_by_id": queries.GET_PROGRAM,
        "get_batch": queries.GET_PROGRAMS,
    }

    resource_id_field = "programId"

    def register_submanagers(self) -> None:
        pass

    async def get_by_id(
        self,
        *,
        program_id: Optional[str] = None,
        proposal_reference: Optional[str] = None,
        program_reference: Optional[str] = None,
        fields: Optional[str] = None,
    ) -> dict[str, Any]:
        """Retrieve a program using a single identifier.

        Exactly one of ``program_id``, ``program_reference``, or ``proposal_reference``
        must be provided.

        Parameters
        ----------
        program_id : str, optional
            The unique identifier of the program.
        proposal_reference : str, optional
            The proposal reference string.
        program_reference : str, optional
            The program reference string.
        fields : str, optional
            Fields to return in the response.

        Returns
        -------
        dict[str, Any]
            The retrieved program resource, or an empty dict if not found.

        Raises
        ------
        ValueError
            If none of the identifiers are provided.
        """
        identifier = resolve_single_program_identifier(
            program_id=program_id,
            program_reference=program_reference,
            proposal_reference=proposal_reference,
        )

        return await super().get_by_id(
            fields=fields,
            _identifier=identifier,
        )

    async def create(
        self,
        *,
        name: str,
        description: str,
        active_start: Optional[str] = None,
        active_end: Optional[str] = None,
        proprietary_months: Optional[int] = None,
        should_notify: Optional[bool] = None,
        private_header: Optional[bool] = None,
        fields: Optional[str] = None,
    ) -> dict[str, Any]:
        """Create a new program.

        Parameters
        ----------
        name : str
            The name of the program (non-empty).
        description : str
            A short description of the program (non-empty).
        active_start : str, optional
            The start date (ISO 8601 format). **Staff use only.**
        active_end : str, optional
            The end date (ISO 8601 format). **Staff use only.**
        proprietary_months : int, optional
            Number of months for proprietary access (GOA setting).
        should_notify : bool, optional
            Whether the user should receive notifications (GOA setting).
        private_header : bool, optional
            Whether the program's FITS headers should be private (GOA setting).
        fields : str, optional
            Fields to return in the response.

        Returns
        -------
        dict[str, Any]
            The created program resource.

        Raises
        ------
        ValueError
            If zero or more than one identifiers are provided, or if date inputs are
            not valid ISO 8601 strings.
        TypeError
            If date fields are not of type `str`, `datetime`, or `astropy.time.Time`.

        Notes
        -----
        The ``active_start`` and ``active_end`` fields are intended for staff workflows
        only. Most users should omit them when creating programs.
        """
        if not name.strip():
            raise ValueError("'name' must be a non-empty string.")
        if not description.strip():
            raise ValueError("'description' must be a non-empty string.")

        set_values: dict[str, Any] = {
            "name": name,
            "description": description,
            "existence": "PRESENT",
        }

        if active_start is not None:
            set_values["activeStart"] = normalize_iso_datetime(active_start)
        if active_end is not None:
            set_values["activeEnd"] = normalize_iso_datetime(active_end)

        # Bundle GOA settings if any are provided.
        goa: dict[str, Any] = {}
        if proprietary_months is not None:
            goa["proprietaryMonths"] = proprietary_months
        if should_notify is not None:
            goa["shouldNotify"] = should_notify
        if private_header is not None:
            goa["privateHeader"] = private_header
        if goa:
            set_values["goa"] = goa

        return await super().create(set_values=set_values, fields=fields)
