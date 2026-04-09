"""
GOATS CLI commands.
"""

__all__ = ["goats_app"]

from typing import Annotated

import typer

from gpp_client.cli import output
from gpp_client.cli.utils import async_command
from gpp_client.client import GPPClient

goats_app = typer.Typer(
    name="goats",
    help="GOATS operations.",
)


@goats_app.command("list-programs")
@async_command
async def list_programs() -> None:
    """
    List GOATS programs.
    """
    with output.status("Fetching GOATS programs..."):
        async with GPPClient() as client:
            result = await client.goats.get_programs()

    output.json_pydantic(result)


@goats_app.command("list-observations")
@async_command
async def list_observations(
    program_id: Annotated[
        str,
        typer.Argument(help="Program ID."),
    ],
) -> None:
    """
    List GOATS observations for a program.

    Parameters
    ----------
    program_id : str
        Program ID.
    """
    with output.status("Fetching GOATS observations..."):
        async with GPPClient() as client:
            result = await client.goats.get_observations_by_program_id(
                program_id=program_id
            )

    output.json_pydantic(result)
