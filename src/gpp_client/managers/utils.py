__all__ = [
    "_print_fields",
    "validate_single_identifier",
    "load_properties",
]

import json
from pathlib import Path
from typing import Any, Optional, Type, TypeVar
from datetime import datetime
from zoneinfo import ZoneInfo


from graphql import print_ast
from pydantic import BaseModel

T = TypeVar("T", bound=BaseModel)


def _print_fields(fields):
    """Print the fields to string."""
    return print(print_ast(fields.to_ast(0)))


def validate_single_identifier(**kwargs) -> None:
    """
    Validate that exactly one identifier is provided.

    This helper checks that exactly one of the provided keyword arguments
    is non-None. It raises a ValueError otherwise.

    Parameters
    ----------
    **kwargs : dict[str, Optional[str]]
        A dictionary of identifier keyword arguments to validate.

    Raises
    ------
    ValueError
        If none or more than one identifiers are provided.
    """
    non_null = [k for k, v in kwargs.items() if v is not None]
    if len(non_null) != 1:
        raise ValueError(
            f"Expected exactly one of {', '.join(kwargs.keys())}, got {len(non_null)}."
        )


def load_properties(
    *,
    properties: Optional[T] = None,
    from_json: Optional[str | Path | dict[str, Any]] = None,
    cls: Type[T],
) -> T:
    """
    Return a validated properties object from exactly one data source.

    Parameters
    ----------
    properties : T, optional
        Preconstructed properties instance. Returned unchanged when provided.
    from_json : str | Path | dict[str, Any], optional
        Path to a JSON file or a dictionary containing the JSON data.
    cls : Type[T]
        Concrete PropertiesInput class for validation. Required.

    Returns
    -------
    T
        Instance of ``cls`` representing the validated properties.

    Raises
    ------
    ValueError
        Raised when both or neither of ``properties`` and ``from_json`` are provided.
    FileNotFoundError
        Raised when ``from_json`` is a path that does not exist.
    json.JSONDecodeError
        Raised when the JSON file cannot be parsed.
    TypeError
        Raised when ``from_json`` is neither path-like nor a mapping.
    """
    # Ensure exactly one data source is provided.
    if (properties is None) == (from_json is None):
        raise ValueError(
            "Provide exactly one of 'properties' or 'from_json', but not both."
        )

    if properties is not None:
        return properties

    # Load data from dictionary or JSON file.
    if isinstance(from_json, dict):
        data = from_json
    else:
        path = Path(from_json).expanduser()
        if not path.is_file():
            raise FileNotFoundError(f"JSON properties file not found: {path}")
        with path.open() as f:
            data = json.load(f)

    return cls(**data)


def normalize_to_utc(
    time_str: Optional[str],
    time_format: str,
    local_zone: str = "UTC",
) -> Optional[str]:
    """
    Normalize a time string to UTC and return ISO 8601 format.

    Parameters
    ----------
    time_str : str
        The input time string (e.g. "Thu May 15 12:01:06 2025").
    time_format : str
        Format string for `datetime.strptime`.
    local_zone : str, default="UTC"
        IANA timezone name. Only used if `time_str` is in local time.

    Returns
    -------
    str, optional
        The UTC datetime in ISO 8601 format with 'T' separator.
    """
    if not time_str:
        return None
    dt = datetime.strptime(time_str, time_format)
    if dt.tzinfo is None:
        dt = dt.replace(tzinfo=ZoneInfo(local_zone))
    return dt.astimezone(ZoneInfo("UTC")).isoformat()
