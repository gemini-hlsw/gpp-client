from typing import Annotated, Optional

import typer
from rich.console import Console
from rich.json import JSON
from rich.table import Table

from gpp_client import GPPClient
from gpp_client.cli.utils import (
    async_command,
    print_not_found,
    truncate_long,
    truncate_short,
)

console = Console()
app = typer.Typer(
    name="pnote", help="Manage program notes.", no_args_is_help=True
)


@app.command("list")
@async_command
async def get_all(
    limit: Annotated[Optional[int], typer.Option(help="Max number of results.")] = None,
    include_deleted: Annotated[
        bool, typer.Option(help="Include deleted entries.")
    ] = False,
):
    """Get all program notes."""
    client = GPPClient()
    result = await client.program_note.get_all(
        limit=limit,
        include_deleted=include_deleted,
    )
    items = result.get("matches", [])
    if not items:
        print_not_found()
        return

    table = Table(title="Program Notes")
    table.add_column("ID", no_wrap=True)
    table.add_column("Program ID")
    table.add_column("Title")
    table.add_column("Text")
    table.add_column("Existence")
    table.add_column("Is Private")

    for item in items:
        id_ = item.get("id")
        title = truncate_short(item.get("title"))
        text = truncate_long(item.get("text"))
        program_id = truncate_short(item.get("program").get("id"))
        existence = truncate_short(item.get("existence"))
        is_private = truncate_short(str(item.get("isPrivate")))
        table.add_row(id_, program_id, title, text, existence, is_private)

    console.print(table)


@app.command("get")
@async_command
async def get_by_id(
    program_note_id: Annotated[str, typer.Argument(help="Program note ID.")],
    include_deleted: Annotated[
        bool, typer.Option(help="Include deleted entries.")
    ] = False,
):
    """Get program note by ID."""
    client = GPPClient()
    result = await client.program_note.get_by_id(
        program_note_id, include_deleted=include_deleted
    )
    console.print(JSON.from_data(result))


@app.command("delete")
@async_command
async def delete_by_id(
    program_note_id: Annotated[str, typer.Argument(help="Program note ID.")],
):
    """Delete a program note by ID."""
    client = GPPClient()
    result = await client.program_note.delete_by_id(program_note_id)
    console.print(JSON.from_data(result))


@app.command("restore")
@async_command
async def restore_by_id(
    program_note_id: Annotated[str, typer.Argument(help="Program note ID.")],
):
    """Restore a program note by ID."""
    client = GPPClient()
    result = await client.program_note.restore_by_id(program_note_id)
    console.print(JSON.from_data(result))


@app.command("create")
@async_command
async def create():
    """Create a new program note (not yet implemented)."""
    raise NotImplementedError(
        "CLI support for 'create' is not yet implemented. Use the API directly with "
        "'ProgramNotePropertiesInput'."
    )


@app.command("update")
@async_command
async def update_by_id():
    """Update a program note by ID (not yet implemented)."""
    raise NotImplementedError(
        "CLI support for 'update' is not yet implemented. "
        "Use the API directly with 'ProgramNotePropertiesInput'."
    )
