"""
Utility helpers for the GPP Client CLI.
"""

__all__ = [
    "async_command",
    "open_client",
    "truncate_string",
    "truncate_short",
    "truncate_long",
    "print_not_found",
    "require_exactly_one",
]

import asyncio
import functools
import inspect
from collections.abc import Callable
from typing import Any

import typer

from gpp_client.cli import output
from gpp_client.cli.console import error_console
from gpp_client.client import GPPClient
from gpp_client.environment import GPPEnvironment
from gpp_client.settings import GPPSettings


def async_command(func: Callable[..., Any]) -> Callable[..., None]:
    """
    Decorator to run async Typer commands using ``asyncio.run()``.

    The command must take a ``typer.Context`` parameter. The decorator reads
    ``--debug`` from it to decide whether a failure prints the full traceback.

    Parameters
    ----------
    func : Callable[..., Any]
        Async command function.

    Returns
    -------
    Callable[..., None]
        Wrapped synchronous callable for Typer.

    Raises
    ------
    TypeError
        Raised if ``func`` has no ``typer.Context`` parameter.
    """
    context_name = next(
        (
            name
            for name, param in inspect.signature(func, eval_str=True).parameters.items()
            if param.annotation is typer.Context
        ),
        None,
    )
    if context_name is None:
        raise TypeError(
            f"{func.__name__} must take a typer.Context parameter for --debug."
        )

    @functools.wraps(func)
    def wrapper(*args, **kwargs) -> Any:
        try:
            return asyncio.run(func(*args, **kwargs))
        except typer.Exit:
            raise
        except Exception as exc:
            ctx = kwargs.get(context_name)
            debug = bool(getattr(getattr(ctx, "obj", None), "debug", False))
            if debug:
                output.print_exception()
            else:
                output.fail(str(exc))

            raise typer.Exit(code=1) from exc

    return wrapper


def open_client(ctx: typer.Context) -> GPPClient:
    """
    Build a client for the environment the command was given with ``--env``.

    Without ``--env`` the environment comes from ``GPP_ENVIRONMENT`` or the
    ``.env`` file as it does in Python, then from the default stored in the
    configuration file, then production with a warning. The environment is
    printed to stderr so piped output stays clean.

    Parameters
    ----------
    ctx : typer.Context
        The running command's context, which holds the ``--env`` choice.

    Returns
    -------
    GPPClient
        A client for the chosen environment.
    """
    environment = getattr(getattr(ctx, "obj", None), "environment", None)
    if environment is None and "environment" not in GPPSettings().model_fields_set:
        error_console.print(
            f"{output.ICON_WARNING} No GPP environment set, so using production. "
            "Pass --env, or set GPP_ENVIRONMENT or environment in the "
            "configuration file; a future release will fail instead.",
            soft_wrap=True,
        )
        environment = GPPEnvironment.PRODUCTION
    client = GPPClient(environment=environment)
    output.environment(client.settings.environment)
    return client


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
