from pathlib import Path
from typing import Annotated, Optional

import typer
from rich.console import Console
from rich.json import JSON
from rich.table import Table

from ...api.input_types import ObservationPropertiesInput
from ...cli.utils import (
    async_command,
    print_not_found,
    truncate_long,
    truncate_short,
)
from ...client import GPPClient
from ...managers.utils import validate_single_identifier

console = Console()
app = typer.Typer(name="obs", help="Manage observations.")


@app.command("list")
@async_command
async def get_all(
    limit: Annotated[Optional[int], typer.Option(help="Max number of results.")] = None,
    include_deleted: Annotated[
        bool, typer.Option(help="Include deleted entries.")
    ] = False,
):
    """Get all observations."""
    client = GPPClient()
    result = await client.observation.get_all(
        limit=limit,
        include_deleted=include_deleted,
    )
    items = result.get("matches", [])

    if not items:
        print_not_found()
        return

    table = Table(title="Observations")
    table.add_column("ID", no_wrap=True)
    table.add_column("Reference")
    table.add_column("Existence")
    table.add_column("Calibration Role")
    table.add_column("Instrument")
    table.add_column("Program ID")

    for item in items:
        id_ = item.get("id")
        reference = "test"
        calibration_role = truncate_long(item.get("calibrationRole"))
        program_id = truncate_short(item.get("program").get("id"))
        existence = truncate_short(item.get("existence"))
        instrument = truncate_short(item.get("instrument"))
        table.add_row(
            id_, reference, existence, calibration_role, instrument, program_id
        )

    console.print(table)


@app.command("get")
@async_command
async def get(
    observation_id: Annotated[
        Optional[str], typer.Option(help="Observation ID.")
    ] = None,
    observation_reference: Annotated[
        Optional[str], typer.Option(help="Observation reference label.")
    ] = None,
    include_deleted: Annotated[
        bool, typer.Option(help="Include deleted entries.")
    ] = False,
):
    """Get an observation by ID or reference."""
    validate_single_identifier(
        observation_id=observation_id, observation_reference=observation_reference
    )
    client = GPPClient()
    result = await client.observation.get_by_id(
        observation_id=observation_id,
        observation_reference=observation_reference,
        include_deleted=include_deleted,
    )
    console.print(JSON.from_data(result))


@app.command("delete")
@async_command
async def delete(
    observation_id: Annotated[
        Optional[str], typer.Option(help="Observation ID.")
    ] = None,
    observation_reference: Annotated[
        Optional[str], typer.Option(help="Observation reference label.")
    ] = None,
):
    """Delete an observation by ID or reference."""
    validate_single_identifier(
        observation_id=observation_id, observation_reference=observation_reference
    )
    client = GPPClient()
    result = await client.observation.delete_by_id(
        observation_id=observation_id,
        observation_reference=observation_reference,
    )
    console.print(JSON.from_data(result))


@app.command("restore")
@async_command
async def restore(
    observation_id: Annotated[
        Optional[str], typer.Option(help="Observation ID.")
    ] = None,
    observation_reference: Annotated[
        Optional[str], typer.Option(help="Observation reference label.")
    ] = None,
):
    """Restore an observation by ID or reference."""
    validate_single_identifier(
        observation_id=observation_id, observation_reference=observation_reference
    )
    client = GPPClient()
    result = await client.observation.restore_by_id(
        observation_id=observation_id,
        observation_reference=observation_reference,
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
    """Create a new observation.

    Exactly one of --program-id, --proposal-reference, or --program-reference
    must be provided to identify the program. Supplying more than one (or none)
    will result in an error.
    """
    client = GPPClient()
    result = await client.observation.create(
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
    observation_id: Annotated[
        Optional[str],
        typer.Option(help="Observation ID (supply exactly one identifier)."),
    ] = None,
    observation_reference: Annotated[
        Optional[str],
        typer.Option(
            help="OBservation reference label (supply exactly one identifier)."
        ),
    ] = None,
):
    """Update a observation by ID or reference.

    Exactly one of --observation-id or --observation-reference must be provided to
    identify the observation. Supplying more than one (or none) will result in an error.
    """
    client = GPPClient()
    result = await client.observation.update_by_id(
        observation_id=observation_id,
        observation_reference=observation_reference,
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
    schema = ObservationPropertiesInput.model_json_schema()
    console.print(JSON.from_data(schema, indent=indent, sort_keys=sort_keys))
