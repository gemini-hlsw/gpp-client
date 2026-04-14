"""
Rich-based output utilities for the GPP Client CLI.
"""

__all__ = [
    "section",
    "info",
    "success",
    "warning",
    "fail",
    "panel",
    "confirm_prompt",
    "print_exception",
    "status",
    "space",
    "TableColumn",
    "model_table",
]

from contextlib import contextmanager
from dataclasses import dataclass
from enum import Enum
from typing import Any, Optional

from rich.console import RenderableType
from rich.json import JSON
from rich.padding import Padding
from rich.panel import Panel
from rich.prompt import Confirm
from rich.table import Table

from gpp_client.cli.console import console, error_console

ICON_BULLET = "[bold white]•[/]"
ICON_SUCCESS = "[bold green]✔[/]"
ICON_WARNING = "[bold yellow]![/]"
ICON_ERROR = "[bold red]✖[/]"
ICON_PROCEDURE = "[bold blue]↴[/]"


def space() -> None:
    """
    Print a blank line to the console.
    """
    console.print("")


def section(title: str, style: str = "dim cyan", align: str = "left") -> None:
    """
    Render a horizontal rule section header.

    Parameters
    ----------
    title : str
        Text to display inside the rule.
    style : str, optional
        Rich style applied to the rule line and title.
    align : str, optional
        Alignment of the title within the rule.
    """
    space()
    console.rule(title=f"{title}", style=style, align=align)
    space()


def info(msg: str) -> None:
    """
    Print a plain informational message.

    Parameters
    ----------
    msg : str
        The message text.
    """
    console.print(f"{msg}", style="white")


def dim_info(msg: RenderableType) -> None:
    """
    Print a dimmed informational message.

    Parameters
    ----------
    msg : RenderableType
        The message text.
    """
    console.print(f"{msg}", style="dim")


def success(msg: RenderableType) -> None:
    """
    Print a success message prefixed with a green check mark.

    Parameters
    ----------
    msg : RenderableType
        Success message text.
    """
    console.print(f"{ICON_SUCCESS} {msg}")


def warning(msg: RenderableType) -> None:
    """
    Print a warning message prefixed with a yellow warning symbol.

    Parameters
    ----------
    msg : RenderableType
        Warning text.
    """
    console.print(f"{ICON_WARNING} {msg}")
    space()


def fail(msg: RenderableType) -> None:
    """
    Print an error message to stderr, prefixed with a red cross.

    Parameters
    ----------
    msg : RenderableType
        Error message text.
    """
    error_console.print(f"{ICON_ERROR} {msg}")


def procedure(msg: RenderableType) -> None:
    """
    Print a procedure message prefixed with a blue arrow.

    Parameters
    ----------
    msg : RenderableType
        Procedure message text.
    """
    console.print(f"{ICON_PROCEDURE} {msg}")


def procedure_steps(steps: list[RenderableType]) -> None:
    """
    Print a list of procedure steps, each prefixed with a dot and indented.

    Parameters
    ----------
    steps : list[RenderableType]
        List of procedure step messages.
    """
    for step in steps:
        console.print(f"  {ICON_BULLET} {step}")


def json(data: dict) -> None:
    """
    Print JSON data in a pretty-formatted way.

    Parameters
    ----------
    data : dict
        The JSON-serializable dictionary to print.
    """
    console.print(JSON.from_data(data))


def json_pydantic(model: object) -> None:
    """
    Print a Pydantic model as JSON.

    Parameters
    ----------
    model : object
        The Pydantic model to print.
    """
    console.print(JSON.from_data(model.model_dump(mode="json")))


def panel(
    msg: RenderableType,
    *,
    title: Optional[str] = None,
    subtitle: Optional[str] = None,
    style: Optional[str] = None,
    border_style: str = "cyan",
    expand: bool = False,
) -> None:
    """
    Render a styled Rich panel.

    Parameters
    ----------
    msg : RenderableType
        Contents of the panel.
    title : str, optional
        Optional panel title.
    subtitle : str, optional
        Optional panel subtitle.
    style : str, optional
        Optional panel style.
    border_style : str, default="cyan"
        Border style for the panel.
    expand : bool, default=False
        Whether the panel should expand to the full width of the console.
    """
    console.print(
        Panel(
            msg,
            title=title,
            subtitle=subtitle,
            style=style if style is not None else "none",
            border_style=border_style,
            expand=expand,
        )
    )


def info_table(items: dict[str, str]) -> None:
    """
    Render a table of informational key-value pairs.

    Parameters
    ----------
    items : dict[str, str]
        Dictionary of key-value pairs to display.
    """
    table = Table(box=None, show_header=False, padding=(0, 1))
    table.add_column("Field", style="white")
    table.add_column("Value", style="dim")

    for key, value in items.items():
        table.add_row(f"{ICON_BULLET} {key}", f"{value}")

    console.print(Padding(table, (0, 0, 1, 4)))


def confirm_prompt(msg: str) -> bool:
    """
    Display a yes/no prompt and return True if the user confirms.

    Parameters
    ----------
    msg : str
        Prompt text.

    Returns
    -------
    bool
        True if the user selects yes, False otherwise.
    """
    return Confirm.ask(
        f"[bold yellow]{msg}[/]",
    )


def print_exception(show_locals: bool = True) -> None:
    """
    Print the current exception's traceback to stderr.

    Parameters
    ----------
    show_locals : bool, default=True
        Whether to show local variables in each stack frame.
    """
    error_console.print_exception(show_locals=show_locals)


@contextmanager
def status(message: str, *, spinner: str = "dots"):
    """
    Context manager for displaying a Rich status spinner.

    Parameters
    ----------
    message : str
        Text to display next to the spinner.
    spinner : str, default="dots"
        Spinner style (see: ``python -m rich.spinner``).
    """
    with console.status(f"[cyan]{message}[/]", spinner=spinner) as status:
        yield status


@dataclass(frozen=True)
class TableColumn:
    """
    Definition for a rendered table column.

    Parameters
    ----------
    header : str
        The displayed column header.
    path : str
        Dotted attribute path to resolve from the item.
    default : str, optional
        Fallback text when the resolved value is missing.
    no_wrap : bool, optional
        Whether the column should avoid wrapping.
    style : str | None, optional
        Optional Rich style for the column.
    """

    header: str
    path: str
    default: str = "-"
    no_wrap: bool = False
    style: str | None = None


def _resolve_attr_path(obj: Any, path: str) -> Any:
    """
    Resolve a dotted attribute path from an object.

    Parameters
    ----------
    obj : Any
        Source object.
    path : str
        Dotted path such as ``program.id`` or ``workflow.value.state``.

    Returns
    -------
    Any
        The resolved value, or None if any segment is missing.
    """
    current = obj

    for part in path.split("."):
        if current is None:
            return None

        current = getattr(current, part, None)

    return current


def _format_cell(value: Any, *, default: str = "-") -> str:
    """
    Convert a Python value into a table-safe string.

    Parameters
    ----------
    value : Any
        Input value.
    default : str, optional
        Fallback when the value is None.

    Returns
    -------
    str
        Formatted cell text.
    """
    if value is None:
        return default

    if isinstance(value, Enum):
        return str(value.value)

    if isinstance(value, bool):
        return "yes" if value else "no"

    if isinstance(value, (list, tuple, set)):
        return ", ".join(_format_cell(item, default=default) for item in value)

    return str(value)


def model_table(
    items: list[Any],
    columns: list[TableColumn],
    *,
    title: str | None = None,
    empty_message: str = "No results found.",
) -> None:
    """
    Render a Rich table from model objects.

    Parameters
    ----------
    items : list[Any]
        Rows to render.
    columns : list[TableColumn]
        Column definitions.
    title : str | None, optional
        Optional table title.
    empty_message : str, optional
        Message to display when there are no rows.
    """
    if not items:
        console.print(empty_message, style="dim")
        return

    table = Table(title=title)

    for column in columns:
        table.add_column(
            column.header,
            no_wrap=column.no_wrap,
            style=column.style,
        )

    for item in items:
        row = [
            _format_cell(
                _resolve_attr_path(item, column.path),
                default=column.default,
            )
            for column in columns
        ]
        table.add_row(*row)

    console.print(table)
