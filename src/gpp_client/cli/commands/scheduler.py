"""
Scheduler CLI commands.
"""

__all__ = ["scheduler_app"]

from typing import Annotated

import typer

from gpp_client.cli import output
from gpp_client.cli.utils import async_command
from gpp_client.client import GPPClient

scheduler_app = typer.Typer(
    name="scheduler",
    help="Scheduler operations.",
)


@scheduler_app.command("list-programs")
@async_command
async def list_programs(
    programs_list: Annotated[
        list[str] | None,
        typer.Option(
            "--program-id",
            help="Filter by program ID. Can be provided multiple times.",
        ),
    ] = None,
) -> None:
    """
    List scheduler programs.
    """
    with output.status("Fetching scheduler programs..."):
        async with GPPClient() as client:
            result = await client.scheduler.get_programs(programs_list=programs_list)

    output.json_pydantic(result)


@scheduler_app.command("list-program-ids")
@async_command
async def list_program_ids() -> None:
    """
    List all scheduler program IDs.
    """
    with output.status("Fetching scheduler program IDs..."):
        async with GPPClient() as client:
            result = await client.scheduler.get_program_ids()

    output.json_pydantic(result)
