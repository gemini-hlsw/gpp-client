__all__ = ["valid_program_identifier", "print_fields", "validate_single_identifier"]

from typing import Optional

from graphql import print_ast


def valid_program_identifier(
    *,
    program_id: Optional[str] = None,
    program_reference: Optional[str] = None,
    proposal_reference: Optional[str] = None,
    raise_exception: bool = True,
) -> bool:
    """Validate that exactly one program identifier is provided.

    Parameters
    ----------
    program_id : str, optional
        The unique program ID.
    program_reference : str, optional
        A reference string for the program.
    proposal_reference : str, optional
        A reference string for the proposal.
    raise_exception : bool, default=True
        Whether to raise a ValueError if validation fails.

    Returns
    -------
    bool
        `True` if exactly one identifier is provided; `False` if validation fails and
        `raise_exception` is `False`.

    Raises
    ------
    ValueError
        If none or more than one identifiers are provided and `raise_exception` is True.
    """
    values = [
        v for v in (program_id, program_reference, proposal_reference) if v is not None
    ]

    if len(values) != 1:
        if raise_exception:
            raise ValueError(
                "Exactly one of 'program_id', 'program_reference', or "
                "'proposal_reference' must be provided."
            )
        return False
    return True


def print_fields(fields):
    """Print the fields to string."""
    return print(print_ast(fields.to_ast(0)))


def validate_single_identifier(**kwargs) -> None:
    """Validate that exactly one identifier is provided.

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
