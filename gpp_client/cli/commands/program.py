import typer
from rich.console import Console
from rich.table import Table

from ...client import GPPClient
from ..utils import async_command, print_not_found, truncate_long, truncate_short

program = typer.Typer(help="Manage Programs.")
console = Console()


@program.command("get-all")
@async_command
async def get_all(
    limit: int = typer.Option(None, help="Max number of results."),
    include_deleted: bool = typer.Option(False, help="Include deleted entries."),
):
    """List all programs the user has access to."""
    client = GPPClient()
    result = await client.program.get_batch(
        limit=limit,
        include_deleted=include_deleted,
    )
    items = result.get("programs", {}).get("matches", [])

    if not items:
        print_not_found()
        return

    table = Table(title="Program")
    table.add_column("ID", no_wrap=True)
    table.add_column("Name")
    table.add_column("Description")

    for item in items:
        item_id = str(item.get("id"))
        name = truncate_short(item.get("name"))
        description = truncate_long(item.get("description"))
        table.add_row(item_id, name, description)

    console.print(table)
