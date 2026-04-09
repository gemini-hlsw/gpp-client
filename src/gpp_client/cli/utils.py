"""
Utility helpers for the GPP Client CLI.
"""

__all__ = [
    "async_command",
    "truncate_string",
    "truncate_short",
    "truncate_long",
    "print_not_found",
    "require_exactly_one",
]

import asyncio
import functools
from collections.abc import Callable
from typing import Any

import typer
from click import get_current_context

from gpp_client.cli import output


def async_command(func: Callable[..., Any]) -> Callable[..., None]:
    """
    Decorator to run async Typer commands using ``asyncio.run()``.

    Parameters
    ----------
    func : Callable[..., Any]
        Async command function.

    Returns
    -------
    Callable[..., None]
        Wrapped synchronous callable for Typer.
    """

    @functools.wraps(func)
    def wrapper(*args, **kwargs) -> Any:
        try:
            return asyncio.run(func(*args, **kwargs))
        except typer.Exit:
            raise
        except Exception as exc:
            ctx = get_current_context(silent=True)
            debug = bool(getattr(getattr(ctx, "obj", None), "debug", False))
            if debug:
                output.print_exception()
            else:
                output.fail(str(exc))

            raise typer.Exit(code=1) from exc

    return wrapper


def truncate_string(value: str | None, max_length: int) -> str:
    """
    Truncate a string to a maximum length with ellipsis.

    Parameters
    ----------
    value : str | None
        The string to truncate.
    max_length : int
        Maximum number of characters allowed, including the ellipsis if applied.

    Returns
    -------
    str
        Truncated string, possibly with "..." appended if truncated.
    """
    if not value:
        return "<None>"
    return value if len(value) <= max_length else value[: max_length - 3] + "..."


def truncate_short(value: str | None) -> str:
    """
    Truncate a string to a short readable length.

    Parameters
    ----------
    value : str | None
        The string to truncate.

    Returns
    -------
    str
        Truncated string, possibly with "..." appended if truncated.
    """
    return truncate_string(value, max_length=20)


def truncate_long(value: str | None) -> str:
    """
    Truncate a string to a readable paragraph length.

    Parameters
    ----------
    value : str | None
        The string to truncate.

    Returns
    -------
    str
        Truncated string, intended for longer fields like descriptions or paragraphs.
    """
    return truncate_string(value, max_length=50)


def print_not_found() -> None:
    """
    Print a not found message.
    """
    output.warning("No items found.")


def require_exactly_one(**selectors: str | None) -> tuple[str, str]:
    """
    Ensure exactly one selector is provided.

    Parameters
    ----------
    **selectors : str | None
        Named selector values (e.g., observation_id, program_id).

    Returns
    -------
    tuple[str, str]
        The selected (name, value) pair.

    Raises
    ------
    typer.BadParameter
        If none or more than one selector is provided.
    """
    provided: list[tuple[str, str]] = []

    for name, value in selectors.items():
        if value is None:
            continue

        value_str = value.strip()
        if value_str == "":
            continue

        provided.append((name, value_str))

    if len(provided) == 0:
        valid = ", ".join(f"--{name.replace('_', '-')}" for name in selectors)
        raise typer.BadParameter(
            f"Exactly one selector is required. Provide one of: {valid}."
        )

    if len(provided) > 1:
        received = ", ".join(f"--{name.replace('_', '-')}" for name, _ in provided)
        raise typer.BadParameter(
            f"Selectors are mutually exclusive. Received: {received}."
        )

    return provided[0]
