import typer
from rich.console import Console
from rich.json import JSON
from rich.table import Table
from typing import Optional
from pathlib import Path

from ...client import GPPClient
from ..utils import async_command, print_not_found, truncate_long

call_for_proposals = typer.Typer(help="Manage Calls for Proposals.")
console = Console()


@call_for_proposals.command("get")
@async_command
async def get(
    id: str = typer.Argument(..., help="ID of the call for proposals to retrieve."),
):
    """Retrieve a call for proposals by its unique ID."""
    client = GPPClient()
    result = await client.call_for_proposals.get_by_id(resource_id=id)
    call_for_proposals = result.get("callForProposals")

    if not call_for_proposals:
        print_not_found()
        return

    console.print(JSON.from_data(call_for_proposals))


@call_for_proposals.command("get-all")
@async_command
async def get_all(
    is_open: bool = typer.Option(
        False, "--is-open", help="Filter to only open calls.", is_flag=True
    ),
    is_closed: bool = typer.Option(
        False, "--is-closed", help="Filter to only closed calls.", is_flag=True
    ),
    limit: int = typer.Option(None, help="Max number of results."),
    include_deleted: Optional[bool] = typer.Option(
        None, help="Include deleted entries.", is_flag=True
    ),
):
    """List all calls for proposals the user has access to."""
    if is_open and is_closed:
        raise typer.BadParameter("Cannot use --is-open and --is-closed together.")

    client = GPPClient()

    if is_open:
        result = await client.call_for_proposals.get_all_open(
            limit=limit, include_deleted=include_deleted
        )
    elif is_closed:
        result = await client.call_for_proposals.get_all_closed(
            limit=limit, include_deleted=include_deleted
        )
    else:
        result = await client.call_for_proposals.get_batch(
            limit=limit, include_deleted=include_deleted
        )
    items = result.get("callsForProposals", {}).get("matches", [])
    if not items:
        print_not_found()
        return

    table = Table(title="Calls for Proposals")
    table.add_column("ID", no_wrap=True)
    table.add_column("Title")
    table.add_column("Type")
    table.add_column("Semester")
    table.add_column("Active Date")
    table.add_column("Active End")

    for item in items:
        active = item.get("active", {})
        call_for_proposals_id = str(item.get("id"))
        title = truncate_long(item.get("title"))
        call_for_proposals_type = item.get("type")
        semester = item.get("semester")
        active_start = active.get("start")
        active_end = active.get("end")
        table.add_row(
            call_for_proposals_id,
            title,
            call_for_proposals_type,
            semester,
            active_start,
            active_end,
        )
    console.print(table)


@call_for_proposals.command("update")
@async_command
async def update(
    id: str = typer.Argument(..., help="Call for Proposals ID."),
    json_file: Path = typer.Argument(..., exists=True, help="Update from JSON file."),
    include_deleted: Optional[bool] = typer.Option(
        None, help="Include deleted notes when updating."
    ),
):
    """Update an existing call for proposals."""
    client = GPPClient()
    result = await client.call_for_proposals.update_by_id(
        call_for_proposals_id=id,
        from_json_file=json_file,
        include_deleted=include_deleted,
    )
    console.print(
        JSON.from_data(result["updateCallsForProposals"]["callsForProposals"][0])
    )


@call_for_proposals.command("delete")
@async_command
async def delete(
    id: str = typer.Argument(..., help="Call for Proposals ID."),
):
    """Delete an existing call for proposals."""
    client = GPPClient()
    result = await client.call_for_proposals.delete_by_id(
        resource_id=id,
    )
    console.print(
        JSON.from_data(result["updateCallsForProposals"]["callsForProposals"][0])
    )


@call_for_proposals.command("restore")
@async_command
async def restore(
    id: str = typer.Argument(..., help="Call for Proposals ID."),
):
    """Restore a deleted call for proposals."""
    client = GPPClient()
    result = await client.call_for_proposals.restore_by_id(
        resource_id=id,
    )
    console.print(
        JSON.from_data(result["updateCallsForProposals"]["callsForProposals"][0])
    )


@call_for_proposals.command("create")
@async_command
async def create(
    json_file: Path = typer.Argument(..., exists=True, help="Create from JSON file."),
):
    """Create a call for proposals."""
    client = GPPClient()
    result = await client.call_for_proposals.create(
        from_json_file=json_file,
    )
    console.print(
        JSON.from_data(result["updateCallsForProposals"]["callsForProposals"][0])
    )
