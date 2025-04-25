__all__ = [
    "create_program_id_filter",
    "merge_set_values",
    "build_input_values",
    "build_selector_values",
]

from typing import Any, Optional, Union
from pathlib import Path
import json


def create_program_id_filter(program_id: str) -> dict[str, Any]:
    """Create a GraphQL filter for matching a specific program ID.

    Parameters
    ----------
    program_id : str
        The program ID to filter on.

    Returns
    -------
    dict[str, Any]
        A GraphQL filter dict.
    """
    return {"program": {"id": {"EQ": program_id}}}


def merge_set_values(
    set_values: dict[str, Any], from_json_file: Optional[Union[str, Path]]
) -> dict[str, Any]:
    """Merge values from a JSON file into an existing `set_values` dictionary.

    If `from_json_file` is provided and valid, its contents will override or
    extend the original `set_values`.

    Parameters
    ----------
    set_values : dict[str, Any]
        The base values to be used in the GraphQL `SET` block.
    from_json_file : str or Path, optional
        Path to a JSON file. Must contain a flat object (dictionary).
        If the file is invalid, unreadable, or does not contain a valid JSON object,
        a `ValueError` is raised.

    Returns
    -------
    dict[str, Any]
        The merged dictionary with any values from the file applied on top.

    Raises
    ------
    ValueError
        If the JSON file does not exist, is not a valid object, or fails to parse.
    """
    if not from_json_file:
        return set_values

    path = Path(from_json_file)
    if not path.exists():
        raise ValueError(f"JSON file does not exist: {from_json_file}")
    try:
        json_data = json.loads(path.read_text())
        if not isinstance(json_data, dict):
            raise ValueError("JSON must be an object.")
        set_values.update(json_data)
    except Exception as exc:
        raise ValueError(f"Invalid JSON in '{from_json_file}': {exc}")

    return set_values


def build_input_values(
    *,
    set_values: Optional[dict[str, Any]] = None,
    identifier: Optional[dict[str, Any]] = None,
    where: Optional[dict[str, Any]] = None,
    limit: Optional[int] = None,
    include_deleted: bool = False,
) -> dict[str, Any]:
    """Build a GraphQL input dictionary for a mutation/query.

    Parameters
    ----------
    set_values : dict[str, Any]
        Dictionary of values to set in the mutation.
    identifier : dict[str, Any], optional
        Dictionary of GraphQL identifiers, e.g., {"programId": "p-2025A-001"}.
    where : dict[str, Any], optional
        Optional WHERE clause to filter affected items.
    limit : int, optional
        Maximum number of records to update.
    include_deleted : bool, default=False
        Whether to include soft-deleted records in the update.

    Returns
    -------
    dict[str, Any]
        A dictionary formatted for use as GraphQL mutation input.
    """
    input_values: dict[str, Any] = {}
    input_values["WHERE"] = where
    input_values["LIMIT"] = limit
    input_values["includeDeleted"] = include_deleted
    input_values["SET"] = set_values

    if identifier is not None:
        input_values.update(identifier)

    return input_values


def build_selector_values(
    *,
    identifier: Optional[dict[str, Any]] = None,
    where: Optional[dict[str, Any]] = None,
    limit: Optional[int] = None,
    offset: Optional[str] = None,
    include_deleted: bool = False,
) -> dict[str, Any]:
    """Build a GraphQL variable dictionary for selector-style queries.

    Parameters
    ----------
    identifier : dict[str, Any], optional
        Named selector values (e.g., {"targetId": "t-001"} or {"programId": "..."}).
    where : dict[str, Any], optional
        WHERE clause for filtering.
    limit : int, optional
        Limit the number of results.
    offset : str, optional
        Optional offset cursor (e.g., TargetId).
    include_deleted : bool, default=False
        Include soft-deleted records.

    Returns
    -------
    dict[str, Any]
        A dictionary of GraphQL query variables.
    """
    selector_values: dict[str, Any] = {}
    selector_values["WHERE"] = where
    selector_values["OFFSET"] = offset
    selector_values["includeDeleted"] = include_deleted
    selector_values["LIMIT"] = limit

    if identifier is not None:
        selector_values.update(identifier)

    return selector_values
