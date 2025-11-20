from typing import Annotated

import typer
from rich.console import Console
from rich.json import JSON

from gpp_client.client import GPPClient
from gpp_client.director import GPPDirector
from gpp_client.cli.utils import (
    async_command,
)

console = Console()
app = typer.Typer(name="goats", help="Run goats-specific queries.")

program_sub_app = typer.Typer(
    name="program",
    help="Program-level coordinations.",
)
app.add_typer(program_sub_app, name="program")

observation_sub_app = typer.Typer(
    name="obs",
    help="Observation-level coordinations.",
)
app.add_typer(observation_sub_app, name="obs")


@observation_sub_app.command("list")
@async_command
async def get_all_observations(
    program_id: Annotated[
        str,
        typer.Option(
            "--program-id",
            "-p",
            help="Program ID to filter observations by.",
        ),
    ],
) -> None:
    """List observations for a specific program."""
    director = GPPDirector(GPPClient())
    result = await director.goats.observation.get_all(program_id=program_id)
    console.print(JSON.from_data(result))


@program_sub_app.command("list")
@async_command
async def get_all_programs() -> None:
    """List all programs with accepted proposal status."""
    director = GPPDirector(GPPClient())
    result = await director.goats.program.get_all()
    console.print(JSON.from_data(result))
