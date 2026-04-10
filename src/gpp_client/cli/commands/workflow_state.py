"""
Workflow state CLI commands.
"""

__all__ = ["workflow_state_app"]

from typing import Annotated

import typer

from gpp_client.cli import output
from gpp_client.cli.utils import async_command, require_exactly_one
from gpp_client.client import GPPClient

workflow_state_app = typer.Typer(
    name="workflow-state",
    help="Workflow state operations.",
)


@workflow_state_app.command("get")
@async_command
async def get_workflow_state(
    observation_id: Annotated[
        str | None,
        typer.Option(
            "--observation-id",
            help="Get workflow state by observation ID.",
        ),
    ] = None,
    observation_reference: Annotated[
        str | None,
        typer.Option(
            "--observation-reference",
            help="Get workflow state by observation reference.",
        ),
    ] = None,
) -> None:
    """
    Get workflow state using exactly one selector.
    """
    selector_name, selector_value = require_exactly_one(
        observation_id=observation_id,
        observation_reference=observation_reference,
    )

    with output.status("Fetching workflow state..."):
        async with GPPClient() as client:
            match selector_name:
                case "observation_id":
                    result = await client.workflow_state.get_by_id(
                        observation_id=selector_value
                    )
                case "observation_reference":
                    result = await client.workflow_state.get_by_reference(
                        observation_reference=selector_value
                    )
                case _:
                    raise typer.BadParameter(f"Unsupported selector: {selector_name}")

    output.json_pydantic(result)
