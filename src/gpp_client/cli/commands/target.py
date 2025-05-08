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
app = typer.Typer(name="target", help="Manage targets.", no_args_is_help=True)


@app.command("list")
@async_command
async def get_all(
    limit: Annotated[Optional[int], typer.Option(help="Max number of results.")] = None,
    include_deleted: Annotated[
        bool, typer.Option(help="Include deleted entries.")
    ] = False,
):
    """Get all targets."""
    client = GPPClient()
    result = await client.target.get_all(
        limit=limit,
        include_deleted=include_deleted,
    )
    items = result.get("matches", [])

    if not items:
        print_not_found()
        return

    table = Table(title="Targets")
    table.add_column("ID", no_wrap=True)
    table.add_column("Name")
    table.add_column("Calibration Role")
    table.add_column("Program ID")
    table.add_column("Existence")

    for item in items:
        id_ = item.get("id")
        name = truncate_short(item.get("name"))
        description = truncate_long(item.get("calibrationRole"))
        program_id = truncate_short(item.get("program").get("id"))
        existence = truncate_short(item.get("existence"))
        table.add_row(id_, name, description, program_id, existence)

    console.print(table)


@app.command("get")
@async_command
async def get_by_id(
    target_id: Annotated[str, typer.Argument(help="Target ID.")],
    include_deleted: Annotated[
        bool, typer.Option(help="Include deleted entries.")
    ] = False,
):
    """Get target by ID."""
    client = GPPClient()
    result = await client.target.get_by_id(target_id, include_deleted=include_deleted)
    console.print(JSON.from_data(result))


@app.command("delete")
@async_command
async def delete_by_id(
    target_id: Annotated[str, typer.Argument(help="Target ID.")],
):
    """Delete a target by ID."""
    client = GPPClient()
    result = await client.target.delete_by_id(target_id)
    console.print(JSON.from_data(result))


@app.command("restore")
@async_command
async def restore_by_id(
    target_id: Annotated[str, typer.Argument(help="Target ID.")],
):
    """Restore a target by ID."""
    client = GPPClient()
    result = await client.target.restore_by_id(target_id)
    console.print(JSON.from_data(result))


@app.command("create")
@async_command
async def create():
    """Create a new target (not yet implemented)."""
    raise NotImplementedError(
        "CLI support for 'create' is not yet implemented. Use the API directly with "
        "'TargetPropertiesInput'."
    )


@app.command("update")
@async_command
async def update_by_id():
    """Update a target by ID (not yet implemented)."""
    raise NotImplementedError(
        "CLI support for 'update' is not yet implemented. "
        "Use the API directly with 'TargetPropertiesInput'."
    )
