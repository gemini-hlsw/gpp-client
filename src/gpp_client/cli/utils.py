__all__ = [
    "async_command",
    "truncate_string",
    "truncate_short",
    "truncate_long",
    "print_not_found",
]

import asyncio
import functools
from typing import Any, Callable, Optional

import typer
from gpp_client.cli import output
from click import get_current_context


def async_command(func: Callable[..., Any]) -> Callable[..., None]:
    """Decorator to run async Typer commands using asyncio.run()."""

    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        try:
            return asyncio.run(func(*args, **kwargs))
        except typer.Exit:
            raise
        except Exception as exc:
            # On exception, check if debug mode is enabled to print full traceback.
            ctx = get_current_context(silent=True)
            debug = bool(getattr(getattr(ctx, "obj", None), "debug", False))
            if debug:
                output.print_exception()
            else:
                # Print a simple error message.
                output.fail(str(exc))

            raise typer.Exit(code=1) from exc

    return wrapper


def truncate_string(value: Optional[str], max_length: int) -> str:
    """Truncate a string to a maximum length with ellipsis.

    Parameters
    ----------
    value : str, optional
        The string to truncate. If `None` or empty, returns an empty string.
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


def truncate_short(value: Optional[str]) -> str:
    """Truncate a string to a short, readable length.

    Parameters
    ----------
    value : str, optional
        The string to truncate.

    Returns
    -------
    str
        Truncated string, intended for short fields like titles or IDs.
    """
    return truncate_string(value, max_length=20)


def truncate_long(value: Optional[str]) -> str:
    """Truncate a string to a readable paragraph length.

    Parameters
    ----------
    value : str, optional
        The string to truncate.

    Returns
    -------
    str
        Truncated string, intended for longer fields like descriptions or paragraphs.
    """
    return truncate_string(value, max_length=50)


def print_not_found() -> None:
    """Print not found message in yellow."""
    output.warning("No items found.")
