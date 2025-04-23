__all__ = ["async_command", "truncate_string", "truncate_title", "truncate_text"]

import asyncio
import functools
from typing import Any, Callable, Optional

import typer
from rich.console import Console

console = Console()


def async_command(func: Callable[..., Any]) -> Callable[..., None]:
    """Decorator to run async Typer commands using asyncio.run()."""

    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        try:
            return asyncio.run(func(*args, **kwargs))
        except Exception as exc:
            console.print(f"[bold red]Error:[/bold red] {exc}", style="red")
            raise typer.Exit(code=1)

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
        return ""
    return value if len(value) <= max_length else value[: max_length - 3] + "..."


def truncate_title(value: Optional[str]) -> str:
    """Truncate a title string to a a short readable length.

    Parameters
    ----------
    value : str, optional
        The title to truncate.

    Returns
    -------
    str
        Truncated title string.
    """
    return truncate_string(value, max_length=20)


def truncate_text(value: Optional[str]) -> str:
    """Truncate a paragraph string to a short readable length.

    Parameters
    ----------
    value : str, optional
        The paragraph text to truncate.

    Returns
    -------
    str
        Truncated paragraph text.
    """
    return truncate_string(value, max_length=40)
