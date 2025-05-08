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
app = typer.Typer(name="cfp", no_args_is_help=True, help="Manage call for proposals.")


@app.command("list")
@async_command
async def get_all(
    limit: Annotated[Optional[int], typer.Option(help="Max number of results.")] = None,
    include_deleted: Annotated[
        bool, typer.Option(help="Include deleted entries.")
    ] = False,
):
    """Get all calls for proposals."""
    client = GPPClient()
    result = await client.call_for_proposals.get_all(
        limit=limit, include_deleted=include_deleted
    )
    items = result.get("matches", [])

    if not items:
        print_not_found()
        return

    table = Table(title="Calls for Proposals")
    table.add_column("ID", no_wrap=True)
    table.add_column("Title")
    table.add_column("Type")
    table.add_column("Semester")
    table.add_column("Active - Start Date")
    table.add_column("Active - End Date")
    table.add_column("Submission Deadline")
    table.add_column("Existence")

    for item in items:
        id_ = truncate_short(item.get("id"))
        title = truncate_long(item.get("title"))
        type_ = truncate_short(item.get("type"))
        semester = truncate_short(item.get("semester"))
        active = item.get("active", {})
        start = truncate_short(active.get("start"))
        end = truncate_short(active.get("end"))
        submission_deadline = truncate_long(item.get("submissionDeadlineDefault"))
        existence = truncate_short(item.get("existence"))
        table.add_row(
            id_,
            title,
            type_,
            semester,
            start,
            end,
            submission_deadline,
            existence,
        )

    console.print(table)


@app.command("get")
@async_command
async def get_by_id(
    call_for_proposal_id: Annotated[str, typer.Argument(help="Call for proposal ID.")],
    include_deleted: Annotated[
        bool, typer.Option(help="Include deleted entries.")
    ] = False,
):
    """Get call for proposal by ID."""
    client = GPPClient()
    result = await client.call_for_proposals.get_by_id(
        call_for_proposal_id, include_deleted=include_deleted
    )
    console.print(JSON.from_data(result))


@app.command("delete")
@async_command
async def delete_by_id(
    call_for_proposal_id: Annotated[str, typer.Argument(help="Call for proposal ID.")],
):
    """Delete a call for proposal by ID."""
    client = GPPClient()
    result = await client.call_for_proposals.delete_by_id(call_for_proposal_id)
    console.print(JSON.from_data(result))


@app.command("restore")
@async_command
async def restore_by_id(
    call_for_proposal_id: Annotated[str, typer.Argument(help="Call for proposal ID.")],
):
    """Restore a call for proposal by ID."""
    client = GPPClient()
    result = await client.call_for_proposals.restore_by_id(call_for_proposal_id)
    console.print(JSON.from_data(result))


@app.command("create")
@async_command
async def create():
    """Create a new call for proposal (not yet implemented)."""
    raise NotImplementedError(
        "CLI support for 'create' is not yet implemented. Use the API directly with 'CallForProposalPropertiesInput'."
    )


@app.command("update")
@async_command
async def update_by_id():
    """Update a proposal by ID (not yet implemented)."""
    raise NotImplementedError(
        "CLI support for 'update' is not yet implemented. Use the API directly with 'CallForProposalPropertiesInput'."
    )
