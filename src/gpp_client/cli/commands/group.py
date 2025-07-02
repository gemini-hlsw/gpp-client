from pathlib import Path
from typing import Annotated, Optional

import typer
from rich.console import Console
from rich.json import JSON

from ...api import GroupPropertiesInput
from ...cli.utils import async_command
from ...client import GPPClient


console = Console()
app = typer.Typer(name="groups", help="Manage Groups.")


@app.command("get")
@async_command
async def get(
    group_id: Annotated[Optional[str], typer.Option(help="Group ID.")] = None,
    group_name: Annotated[Optional[str], typer.Option(help="Group name.")] = None,
    include_deleted: Annotated[
        bool, typer.Option(help="Include deleted entries.")
    ] = False,
):
    """Get a group by ID or name."""
    client = GPPClient()
    result = await client.group.get_by_id(
        grouop_id=group_id,
        group_name=group_name,
        include_deleted=include_deleted,
    )
    console.print(JSON.from_data(result))


@app.command("delete")
@async_command
async def delete(
    group_id: Annotated[Optional[str], typer.Option(help="Group ID.")] = None,
    group_name: Annotated[Optional[str], typer.Option(help="Group name.")] = None,
):
    """Delete a group by ID or name."""

    client = GPPClient()
    result = await client.group.delete_by_id(
        group_id=group_id,
        group_name=group_name,
    )
    console.print(JSON.from_data(result))


@app.command("restore")
@async_command
async def restore(
    group_id: Annotated[Optional[str], typer.Option(help="Group ID.")] = None,
    group_name: Annotated[Optional[str], typer.Option(help="Group name.")] = None,
):
    """Restore a group by ID or name."""

    client = GPPClient()
    result = await client.group.restore_by_id(
        group_id=group_id,
        group_name=group_name,
    )
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
    program_id: Annotated[
        Optional[str],
        typer.Option(help="Program ID (supply exactly one identifier)."),
    ] = None,
    proposal_reference: Annotated[
        Optional[str],
        typer.Option(help="Proposal reference label (supply exactly one identifier)."),
    ] = None,
    program_reference: Annotated[
        Optional[str],
        typer.Option(help="Program label reference (supply exactly one identifier)."),
    ] = None,
):
    """Create a new group.

    Exactly one of --program-id, --proposal-reference, or --program-reference
    must be provided to identify the program. Supplying more than one (or none)
    will result in an error.
    """
    client = GPPClient()
    result = await client.group.create(
        from_json=from_json,
        program_id=program_id,
        program_reference=program_reference,
        proposal_reference=proposal_reference,
    )
    console.print(JSON.from_data(result))


@app.command("update")
@async_command
async def update_by_id(
    from_json: Annotated[
        Path,
        typer.Option(
            ...,
            "--from-json",
            exists=True,
            help="JSON file with the properties definition.",
        ),
    ],
    group_id: Annotated[
        Optional[str],
        typer.Option(help="Group ID (supply exactly one identifier)."),
    ] = None,
    group_name: Annotated[
        Optional[str],
        typer.Option(help="Group name (supply exactly one identifier)."),
    ] = None,
):
    """Update a group by ID or name.

    Exactly one of --group-id or --group-name must be provided to
    identify the group. Supplying more than one (or none) will result in an error.
    """
    client = GPPClient()
    result = await client.group.update_by_id(
        group_id=group_id,
        group_name=group_name,
        from_json=from_json,
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
    schema = GroupPropertiesInput.model_json_schema()
    console.print(JSON.from_data(schema, indent=indent, sort_keys=sort_keys))
