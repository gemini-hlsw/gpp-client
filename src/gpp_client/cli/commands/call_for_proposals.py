from pathlib import Path
from typing import Annotated, Optional

import typer
from rich.console import Console
from rich.json import JSON
from rich.table import Table

from ...api.input_types import CallForProposalsPropertiesInput
from ...cli.utils import (
    async_command,
    print_not_found,
    truncate_long,
    truncate_short,
)
from ...client import GPPClient

console = Console()
app = typer.Typer(name="cfp", help="Manage call for proposals.")


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
    call_for_proposal_id: Annotated[str, typer.Argument(help="Call for proposals ID.")],
    include_deleted: Annotated[
        bool, typer.Option(help="Include deleted entries.")
    ] = False,
):
    """Get call for proposals by ID."""
    client = GPPClient()
    result = await client.call_for_proposals.get_by_id(
        call_for_proposal_id, include_deleted=include_deleted
    )
    console.print(JSON.from_data(result))


@app.command("delete")
@async_command
async def delete_by_id(
    call_for_proposal_id: Annotated[str, typer.Argument(help="Call for proposals ID.")],
):
    """Delete a call for proposals by ID."""
    client = GPPClient()
    result = await client.call_for_proposals.delete_by_id(call_for_proposal_id)
    console.print(JSON.from_data(result))


@app.command("restore")
@async_command
async def restore_by_id(
    call_for_proposal_id: Annotated[str, typer.Argument(help="Call for proposals ID.")],
):
    """Restore a call for proposals by ID."""
    client = GPPClient()
    result = await client.call_for_proposals.restore_by_id(call_for_proposal_id)
    console.print(JSON.from_data(result))


@app.command("create")
@async_command
async def create(
    from_json: Annotated[
        Path,
        typer.Option(
            ...,
            exists=True,
            help="JSON file with the properties definition.",
        ),
    ],
):
    """Create a call for proposals."""
    client = GPPClient()
    result = await client.call_for_proposals.create(from_json=from_json)
    console.print(JSON.from_data(result))


@app.command("update")
@async_command
async def update_by_id(
    call_for_proposals_id: Annotated[
        str, typer.Argument(..., help="Call for proposals ID to update.")
    ],
    from_json: Annotated[
        Path,
        typer.Option(
            ...,
            exists=True,
            help="JSON file with the properties definition.",
        ),
    ],
):
    """Update a call for proposals by ID."""
    client = GPPClient()
    result = await client.call_for_proposals.update_by_id(
        call_for_proposals_id=call_for_proposals_id, from_json=from_json
    )
    console.print(JSON.from_data(result))


@app.command("schema")
def schema(
    indent: Annotated[
        int,
        typer.Option(
            show_default=True,
            help="Indentation level for pretty printing.",
        ),
    ] = 2,
    sort_keys: Annotated[
        bool,
        typer.Option(
            help="Sort object keys alphabetically.",
        ),
    ] = False,
):
    """Display the JSON Schema for the input properties.

    Use this when crafting or validating the JSON files passed with
    --from-json to the `create` or `update` commands.
    """
    schema = CallForProposalsPropertiesInput.model_json_schema()
    console.print(JSON.from_data(schema, indent=indent, sort_keys=sort_keys))
