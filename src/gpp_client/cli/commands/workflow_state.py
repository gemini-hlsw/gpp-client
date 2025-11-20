from typing import Annotated, Optional

import typer
from rich.console import Console
from rich.json import JSON

from gpp_client.api.enums import ObservationWorkflowState
from gpp_client.cli.utils import (
    async_command,
)
from gpp_client.client import GPPClient

console = Console()
app = typer.Typer(name="wfs", help="Manage observation workflow states.")


@app.command("get")
@async_command
async def get(
    observation_id: Annotated[
        Optional[str], typer.Option(help="Observation ID.")
    ] = None,
    observation_reference: Annotated[
        Optional[str], typer.Option(help="Observation reference label.")
    ] = None,
):
    """Get a workflow state for an observation by ID or reference."""
    client = GPPClient()
    result = await client.workflow_state.get_by_id(
        observation_id=observation_id,
        observation_reference=observation_reference,
    )
    console.print(JSON.from_data(result))


@app.command("update")
@async_command
async def update(
    workflow_state: Annotated[
        ObservationWorkflowState,
        typer.Option(
            help="The new workflow state to set.",
            case_sensitive=False,
        ),
    ],
    observation_id: Annotated[str, typer.Option(help="Observation ID.")],
):
    """Update the workflow state for an observation by ID."""
    client = GPPClient()
    result = await client.workflow_state.update_by_id(
        workflow_state=workflow_state,
        observation_id=observation_id,
    )
    console.print(JSON.from_data(result))
