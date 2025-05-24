from pathlib import Path
from typing import Any, Optional

from ..api.create_program_note import CreateProgramNote
from ..api.fragments import ProgramNoteFields
from ..api.update_program_notes import UpdateProgramNotesUpdateProgramNotes
from ..api.get_all_program_notes import GetAllProgramNotes
from ..api.get_program_note import GetProgramNote

from ..api.enums import Existence
from ..api.input_types import (
    ProgramNotePropertiesInput,
    WhereOrderProgramNoteId,
    WhereProgramNote,
)
from .base_manager import BaseManager
from .utils import load_properties, validate_single_identifier


class ProgramNoteManager(BaseManager):
    async def create(
        self,
        *,
        properties: Optional[ProgramNotePropertiesInput] = None,
        from_json: Optional[str | Path | dict[str, Any]] = None,
        program_id: Optional[str] = None,
        proposal_reference: Optional[str] = None,
        program_reference: Optional[str] = None,
    ) -> ProgramNoteFields:
        """Create a new program note.

        Parameters
        ----------
        properties : ProgramNotePropertiesInput, optional
            Full program note definition to apply. This or ``from_json`` must be
            supplied.
        from_json : str | Path | dict[str, Any], optional
            JSON representation of the properties. May be a path-like object
            (``str`` or ``Path``) to a JSON file, or a ``dict`` already containing the
            JSON data.
        program_id : str, optional
            ID of the program to associate with.
        proposal_reference : str, optional
            Proposal reference, used if `program_id` is not provided.
        program_reference : str, optional
            Program label reference, used if `program_id` is not provided.

        Returns
        -------
        dict[str, Any]
            The created program note and its data.

        Raises
        ------
        ValueError
            - If none of the program identifiers are provided.
            - If zero or both of ``properties`` and ``from_json`` are provided.

        Notes
        -----
        Exactly one of ``properties`` or ``from_json`` must be supplied. Supplying
        both or neither raises ``ValueError``.
        """
        validate_single_identifier(
            program_id=program_id,
            proposal_reference=proposal_reference,
            program_reference=program_reference,
        )

        properties = load_properties(
            properties=properties, from_json=from_json, cls=ProgramNotePropertiesInput
        )

        result = await self.client.create_program_note(
            input=properties,
            program_id=program_id,
            proposal_reference=proposal_reference,
            program_reference=program_reference,
        )

        return result.create_program_note.program_note

    async def update_all(
        self,
        *,
        properties: Optional[ProgramNotePropertiesInput] = None,
        from_json: Optional[str | Path | dict[str, Any]] = None,
        where: Optional[WhereProgramNote] = None,
        limit: Optional[int] = None,
        include_deleted: bool = False,
    ) -> UpdateProgramNotesUpdateProgramNotes:
        """Update one or more program notes.

        Parameters
        ----------
        properties : ProgramNotePropertiesInput, optional
            Properties to apply to the matched program notes. This or ``from_json``
            must be supplied.
        from_json : str | Path | dict[str, Any], optional
            JSON representation of the properties. May be a path-like object
            (``str`` or ``Path``) to a JSON file, or a ``dict`` already containing the
            JSON data.
        where : WhereProgramNote, optional
            Filtering criteria to match program notes to update.
        limit : int, optional
            Maximum number of results to update.
        include_deleted : bool, default=False
            Whether to include soft-deleted entries in the match.

        Returns
        -------
        dict[str, Any]
            A dictionary of updated results and data.

        Raises
        ------
        ValueError
            If zero or both of ``properties`` and ``from_json`` are provided.

        Notes
        -----
        Exactly one of ``properties`` or ``from_json`` must be supplied. Supplying
        both or neither raises ``ValueError``.
        """

        properties = load_properties(
            properties=properties, from_json=from_json, cls=ProgramNotePropertiesInput
        )

        result = await self.client.update_program_notes(
            set=properties, where=where, limit=limit, include_deleted=include_deleted
        )
        
        return result.update_program_notes

    async def update_by_id(
        self,
        program_note_id: str,
        *,
        properties: Optional[ProgramNotePropertiesInput] = None,
        from_json: Optional[str | Path | dict[str, Any]] = None,
        include_deleted: bool = False,
    ) -> Any:
        """Update a single program note by its ID.

        Parameters
        ----------
        program_note_id : str
            Unique identifier of the program note.
        properties : ProgramNotePropertiesInput, optional
            Properties to update. This or ``from_json`` must be supplied.
        from_json : str | Path | dict[str, Any], optional
            JSON representation of the properties. May be a path-like object
            (``str`` or ``Path``) to a JSON file, or a ``dict`` already containing the
            JSON data.
        include_deleted : bool, default=False
            Whether to include soft-deleted entries.

        Returns
        -------
        dict[str, Any]
            The updated program note.

        Raises
        ------
        ValueError
            If zero or both of ``properties`` and ``from_json`` are provided.

        Notes
        -----
        Exactly one of ``properties`` or ``from_json`` must be supplied. Supplying
        both or neither raises ``ValueError``.
        """
        where = WhereProgramNote(id=WhereOrderProgramNoteId(eq=program_note_id))

        results = await self.update_all(
            where=where,
            limit=1,
            properties=properties,
            include_deleted=include_deleted,
            from_json=from_json,
        )

        # Since it returns one item, discard the 'matches' and return the item.
        return results.update_program_notes.program_notes[0]

    async def get_by_id(
        self, program_note_id: str, *, include_deleted: bool = False
    ) -> GetProgramNote:
        """Fetch a program note by its ID.

        Parameters
        ----------
        program_note_id : str
            Unique identifier of the program note.
        include_deleted : bool, default=False
            Whether to include soft-deleted notes.

        Returns
        -------
        dict[str, Any]
            The program note data.
        """
        return await self.client.get_program_note(id=program_note_id)

    async def get_all(
        self,
        *,
        include_deleted: bool = False,
        where: WhereProgramNote | None = None,
        offset: str | None = None,
        limit: int | None = None,
    ) -> GetAllProgramNotes:
        """Fetch all program notes with optional filters.

        Parameters
        ----------
        include_deleted : bool, default=False
            Whether to include soft-deleted entries.
        where : WhereProgramNote, optional
            Filters to apply to the query.
        offset : str, optional
            Cursor-based pagination offset.
        limit : int, optional
            Max number of entries to return.

        Returns
        -------
        dict[str, Any]
            A dictionary with `matches` and `hasMore` keys.
        """
        return await self.client.get_all_program_notes(
            include_deleted=include_deleted, where=where, limit=limit, offset=offset
        )

    async def restore_by_id(self, program_note_id: str) -> dict[str, Any]:
        """Restore a soft-deleted program note by ID.

        Parameters
        ----------
        program_note_id : str
            The ID of the note to restore.

        Returns
        -------
        dict[str, Any]
            The restored note.
        """
        properties = ProgramNotePropertiesInput(existence=Existence.PRESENT)
        return await self.update_by_id(
            program_note_id, properties=properties, include_deleted=True
        )

    async def delete_by_id(self, program_note_id: str) -> dict[str, Any]:
        """Soft-delete a program note by ID.

        Parameters
        ----------
        program_note_id : str
            The ID of the note to delete.

        Returns
        -------
        dict[str, Any]
            The deleted note.
        """
        properties = ProgramNotePropertiesInput(existence=Existence.DELETED)
        return await self.update_by_id(
            program_note_id,
            properties=properties,
            include_deleted=False,
        )
