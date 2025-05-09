from typing import Annotated, Optional

import typer
from rich.console import Console
from rich.json import JSON
from rich.table import Table

from ...cli.utils import (
    async_command,
    print_not_found,
    truncate_long,
    truncate_short,
)
from ...client import GPPClient
from ...managers.utils import validate_single_identifier

console = Console()
app = typer.Typer(name="obs", help="Manage observations.", no_args_is_help=True)


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
async def create():
    """Create a new observation (not yet implemented)."""
    raise NotImplementedError(
        "CLI support for 'create' is not yet implemented. Use the API directly with "
        "'ObservationPropertiesInput'."
    )


@app.command("update")
@async_command
async def update_by_id():
    """Update a observation by ID or reference (not yet implemented)."""
    raise NotImplementedError(
        "CLI support for 'update' is not yet implemented. "
        "Use the API directly with 'ObservationPropertiesInput'."
    )
