from typing import Annotated, Optional

import typer
from rich.console import Console
from rich.table import Table

from ...cli.utils import (
    async_command,
    print_not_found,
    truncate_long,
)
from ...client import GPPClient

console = Console()
app = typer.Typer(name="cr", help="Manage configuration requests.")


@app.command("list")
@async_command
async def list_configuration_requests(
    program_id: Annotated[
        str, typer.Option("--program-id", "-p", help="Filter by Program ID.")
    ],
    approved: Annotated[
        bool, typer.Option("--approved", help="Only show approved requests.")
    ] = False,
    limit: Annotated[Optional[int], typer.Option(help="Max number of results.")] = None,
    offset: Annotated[
        Optional[int],
        typer.Option(help="Start results after the given ID (as offset)."),
    ] = None,
):
    """
    List configuration requests filtered by program ID (and approval if requested).
    """
    client = GPPClient()

    if approved:
        result = await client.configuration_request.get_all_approved_by_program_id(
            program_id=program_id,
            limit=limit,
            offset=offset,
        )
    else:
        result = await client.configuration_request.get_all(
            program_id=program_id,
            limit=limit,
            offset=offset,
        )

    items = result.get("matches", [])

    if not items:
        print_not_found()
        return

    table = Table(title="Configuration Requests")
    table.add_column("ID", no_wrap=True)
    table.add_column("Status")
    table.add_column("Justification")
    table.add_column("# Applicable Obs.", justify="right")
    table.add_column("Instrument", no_wrap=True)
    table.add_column("Mode", no_wrap=True)

    for item in items:
        id_ = item.get("id", "")
        status = item.get("status", "")
        justification = truncate_long(item.get("justification"))
        applicable_obs = str(len(item.get("applicableObservations", [])))

        config = item.get("configuration", {})
        observing_mode = config.get("observingMode", {})
        instrument = observing_mode.get("instrument", "—")
        mode = observing_mode.get("mode", "—")

        table.add_row(id_, status, justification, applicable_obs, instrument, mode)

    console.print(table)
