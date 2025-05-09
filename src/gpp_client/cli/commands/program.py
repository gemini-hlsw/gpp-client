from typing import Annotated, Optional

import typer
from rich.console import Console
from rich.json import JSON
from rich.table import Table

from gpp_client import GPPClient
from gpp_client.cli.utils import (
    async_command,
    print_not_found,
    truncate_short,
)

console = Console()
app = typer.Typer(name="program", help="Manage programs.", no_args_is_help=True)


@app.command("list")
@async_command
async def get_all(
    limit: Annotated[Optional[int], typer.Option(help="Max number of results.")] = None,
    include_deleted: Annotated[
        bool, typer.Option(help="Include deleted entries.")
    ] = False,
):
    """Get all programs."""
    client = GPPClient()
    result = await client.program.get_all(
        limit=limit,
        include_deleted=include_deleted,
    )
    items = result.get("matches", [])

    if not items:
        print_not_found()
        return

    table = Table(title="Programs")
    table.add_column("ID", no_wrap=True)
    table.add_column("Name")
    table.add_column("Type")
    table.add_column("Active - Start Date")
    table.add_column("Active - End Date")
    table.add_column("Existence")

    for item in items:
        id_ = truncate_short(item.get("id"))
        name = truncate_short(item.get("name"))
        type_ = truncate_short(item.get("type"))
        active = item.get("active", {})
        start = truncate_short(active.get("start"))
        end = truncate_short(active.get("end"))
        existence = truncate_short(item.get("existence"))
        table.add_row(id_, name, type_, start, end, existence)

    console.print(table)


@app.command("get")
@async_command
async def get_by_id(
    program_id: Annotated[str, typer.Argument(help="Program ID.")],
    include_deleted: Annotated[
        bool, typer.Option(help="Include deleted entries.")
    ] = False,
):
    """Get program by ID."""
    client = GPPClient()
    result = await client.program.get_by_id(program_id, include_deleted=include_deleted)
    console.print(JSON.from_data(result))


@app.command("delete")
@async_command
async def delete_by_id(
    program_id: Annotated[str, typer.Argument(help="Program ID.")],
):
    """Delete a program by ID."""
    client = GPPClient()
    result = await client.program.delete_by_id(program_id)
    console.print(JSON.from_data(result))


@app.command("restore")
@async_command
async def restore_by_id(
    program_id: Annotated[str, typer.Argument(help="Program ID.")],
):
    """Restore a program by ID."""
    client = GPPClient()
    result = await client.program.restore_by_id(program_id)
    console.print(JSON.from_data(result))


@app.command("create")
@async_command
async def create():
    """Create a new program (not yet implemented)."""
    raise NotImplementedError(
        "CLI support for 'create' is not yet implemented. Use the API directly with "
        "'ProgramPropertiesInput'."
    )


@app.command("update")
@async_command
async def update_by_id():
    """Update a program by ID (not yet implemented)."""
    raise NotImplementedError(
        "CLI support for 'update' is not yet implemented. "
        "Use the API directly with 'ProgramPropertiesInput'."
    )
