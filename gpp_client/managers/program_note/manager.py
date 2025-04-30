"""Program note manager for accessing and mutating program note data via GraphQL.

This manager provides CRUD operations for program notes by composing reusable mixins.
Each mixin handles one operation (get, create, update, delete, etc.), making this
class modular, testable, and extendable.

To build your own manager, inherit from:

- `BaseManager` for core GraphQL functionality.

- Operation-specific mixins from the `mixins/` package (e.g., `CreateMixin`).

Then, override or extend behavior by adding custom methods like `create()`.

Each manager must define:

- `queries`: a mapping from operation names to GraphQL templates with `{fields}` placeholder.

- `default_fields`: a string of default GraphQL fields returned from each query.

- `resource_id_field`: the name of the unique identifier field used for 'GetByIdMixin'.

Example
-------
>>> client = GPPClient(...)
>>> note = await client.program_note.get_by_id(resource_id="n-abc123")
"""

__all__ = ["ProgramNoteManager"]

from typing import Any, Optional, Union
from pathlib import Path

from ...mixins import (
    CreateMixin,
    DeleteBatchByProgramIdMixin,
    DeleteBatchMixin,
    DeleteByIdViaBatchMixin,
    GetBatchByProgramIdMixin,
    GetBatchMixin,
    GetByIdMixin,
    RestoreBatchByProgramIdMixin,
    RestoreByIdViaBatchMixin,
    UpdateBatchByProgramIdMixin,
    UpdateBatchMixin,
    UpdateByIdViaBatchMixin,
)
from ..base_manager import BaseManager
from . import queries

from ..utils import resolve_single_program_identifier


class ProgramNoteManager(
    # Mixins are ordered top-down so that `super()` resolves as expected.
    # These mixins each provide one type of query or mutation logic.
    UpdateBatchByProgramIdMixin,
    UpdateBatchMixin,
    UpdateByIdViaBatchMixin,
    CreateMixin,
    DeleteBatchByProgramIdMixin,
    DeleteBatchMixin,
    DeleteByIdViaBatchMixin,
    GetBatchMixin,
    GetBatchByProgramIdMixin,
    RestoreBatchByProgramIdMixin,
    RestoreByIdViaBatchMixin,
    GetByIdMixin,
    BaseManager,
):
    # GraphQL selection set used when a user does not pass custom `fields`.
    default_fields = queries.DEFAULT_FIELDS

    # Query templates. Each must include a `{fields}` placeholder to allow
    # customization.
    queries = {
        "get_batch": queries.GET_PROGRAM_NOTES,
        "get_batch_by_program_id": queries.GET_PROGRAM_NOTES,
        "get_by_id": queries.GET_PROGRAM_NOTE,
        "restore_by_id": queries.UPDATE_PROGRAM_NOTES,
        "restore_by_program_id": queries.UPDATE_PROGRAM_NOTES,
        "update_by_id": queries.UPDATE_PROGRAM_NOTES,
        "update_batch": queries.UPDATE_PROGRAM_NOTES,
        "update_batch_by_program_id": queries.UPDATE_PROGRAM_NOTES,
        "create": queries.CREATE_PROGRAM_NOTE,
        "delete_batch": queries.UPDATE_PROGRAM_NOTES,
        "delete_by_id": queries.UPDATE_PROGRAM_NOTES,
        "delete_batch_by_program_id": queries.UPDATE_PROGRAM_NOTES,
    }
    # Field name used to filter single resources (e.g., `id = resource_id`)
    resource_id_field = "programNoteId"

    async def create(
        self,
        *,
        title: str,
        text: str,
        is_private: bool = False,
        program_id: Optional[str] = None,
        program_reference: Optional[str] = None,
        proposal_reference: Optional[str] = None,
        from_json_file: Optional[Union[str, Path]] = None,
        fields: Optional[str] = None,
    ) -> dict[str, Any]:
        """Create a new program note.

        At least one of `program_id` or `program_reference` must be provided.
        If both are provided, they must refer to the same program.

        This override makes the CreateMixin easier to use by handling
        the construction of the `set_values` dictionary internally.

        Users can pass meaningful keyword arguments directly instead of
        needing to know or build the correct GraphQL input structure themselves.

        Parameters
        ----------
        title : str
            Title of the note.
        text : str
            Note content.
        is_private : bool, optional
            Whether the note is private. Defaults to False.
        existence : str, optional
            Note existence state. Defaults to "PRESENT".
        program_id : str, optional
            The unique program ID.
        program_reference : str, optional
            The reference string of the program.
        proposal_reference : str, optional
            The reference to the proposal.
        from_json_file : str or Path, optional
            Path to a JSON file whose keys will override values in `set_values`.
            This only affects the `SET` portion of the mutation.
        fields : str, optional
            Fields to return in the response.

        Returns
        -------
        dict[str, Any]
            A dictionary containing the newly created program note.

        Raises
        ------
        ValueError
            If zero or more than one identifiers are provided.
        """
        identifier = resolve_single_program_identifier(
            program_id=program_id,
            program_reference=program_reference,
            proposal_reference=proposal_reference,
        )
        set_values = {
            "title": title,
            "text": text,
            "isPrivate": is_private,
            "existence": "PRESENT",
        }

        # Delegate to CreateMixin with optional custom fields.
        return await super().create(
            set_values=set_values,
            identifier=identifier,
            fields=fields,
            from_json_file=from_json_file,
        )

    async def update_by_id(
        self,
        *,
        resource_id: str,
        title: Optional[str] = None,
        text: Optional[str] = None,
        is_private: Optional[bool] = None,
        existence: Optional[str] = None,
        include_deleted: Optional[bool] = False,
        from_json_file: Optional[Union[str, Path]] = None,
        fields: Optional[str] = None,
    ) -> dict[str, Any]:
        """Update a specific program note by ID.

        This override simplifies usage of the `UpdateByIdViaBatchMixin`
        by allowing users to pass intuitive keyword arguments instead
        of manually assembling the `set_values` dictionary.

        This makes it easier to update a note without needing to
        reference the GraphQL schema directly.

        Parameters
        ----------
        resource_id : str
            The unique ID of the note to update.
        title : str, optional
            New title for the note.
        text : str, optional
            New content for the note.
        is_private : bool, optional
            Whether the note is private.
        existence : str, optional
            New existence state.
        include_deleted : bool, optional
            Whether to include deleted notes.
        from_json_file : str or Path, optional
            Path to a JSON file whose keys will override values in `set_values`.
            This only affects the `SET` portion of the mutation.
        fields : str, optional
            Fields to return in the response.

        Returns
        -------
        dict[str, Any]
            A dictionary containing the updated program note.

        Raises
        ------
        ValueError
            If no fields are provided to update.
        """
        set_values: dict[str, Any] = {}

        if title is not None:
            set_values["title"] = title
        if text is not None:
            set_values["text"] = text
        if is_private is not None:
            set_values["isPrivate"] = is_private
        if existence is not None:
            set_values["existence"] = existence

        if not set_values:
            raise ValueError("At least one field must be provided to update.")

        # Delegate to UpdateByIdViaBatchMixin with the provided params.
        return await super().update_by_id(
            resource_id=resource_id,
            set_values=set_values,
            include_deleted=include_deleted,
            fields=fields,
            from_json_file=from_json_file,
        )
