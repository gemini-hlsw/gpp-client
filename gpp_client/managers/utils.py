from typing import Union, Optional
from datetime import datetime
from astropy.time import Time


def normalize_iso_datetime(value: Union[str, datetime, Time]) -> str:
    """Normalize datetime inputs to ISO 8601 string."""
    if isinstance(value, datetime):
        return value.isoformat()
    if isinstance(value, Time):
        return value.to_datetime().isoformat()
    if isinstance(value, str):
        try:
            # Validate that it's a valid ISO string
            datetime.fromisoformat(value)
            return value
        except ValueError as e:
            raise ValueError(f"Invalid ISO 8601 datetime string: {value}") from e
    raise TypeError(f"Invalid type for datetime field: {type(value).__name__}")


def resolve_single_program_identifier(
    *,
    program_id: Optional[str] = None,
    program_reference: Optional[str] = None,
    proposal_reference: Optional[str] = None,
) -> dict[str, str]:
    """Resolve exactly one program identifier for use in GraphQL operations.

    Parameters
    ----------
    program_id : str, optional
        The unique program ID.
    program_reference : str, optional
        The program reference string.
    proposal_reference : str, optional
        The proposal reference string.

    Returns
    -------
    dict[str, str]
        A dict of the identifier.

    Raises
    ------
    ValueError
        If zero or more than one identifiers are provided.
    """
    identifiers = {
        "programId": program_id,
        "programReference": program_reference,
        "proposalReference": proposal_reference,
    }
    provided = {k: v for k, v in identifiers.items() if v is not None}

    if len(provided) != 1:
        raise ValueError(
            "Exactly one of 'program_id', 'program_reference', or 'proposal_reference' must be provided."
        )

    key, value = next(iter(provided.items()))

    return {key: value}
