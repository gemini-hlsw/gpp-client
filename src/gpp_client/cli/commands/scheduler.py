import typer
from rich.console import Console
from rich.json import JSON

from ...client import GPPClient
from ...director import GPPDirector
from ..utils import (
    async_command,
)

console = Console()
app = typer.Typer(name="sched", help="Run scheduler-specific queries.")

program_sub_app = typer.Typer(
    name="program",
    help="Program-level coordinations.",
)
app.add_typer(program_sub_app, name="program")


@program_sub_app.command("list")
@async_command
async def get_all() -> None:
    """List all programs from the scheduler with full group and observation trees."""
    client = GPPClient()
    director = GPPDirector(client)
    result = await director.scheduler.program.get_all()
    console.print(JSON.from_data(result))
