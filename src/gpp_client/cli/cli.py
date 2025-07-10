import typer
from rich import print

from ..client import GPPClient
from .commands import (
    call_for_proposals,
    config,
    group,
    observation,
    program,
    program_note,
    site_status,
    target,
    scheduler,
    goats,
)
from .utils import async_command

app = typer.Typer(
    name="GPP Client", no_args_is_help=False, help="Client to communicate with GPP."
)
app.add_typer(config.app)
app.add_typer(program_note.app)
app.add_typer(target.app)
app.add_typer(program.app)
app.add_typer(call_for_proposals.app)
app.add_typer(observation.app)
app.add_typer(site_status.app)
app.add_typer(group.app)
app.add_typer(scheduler.app)
app.add_typer(goats.app)


@app.command("ping")
@async_command
async def ping() -> None:
    """Ping GPP. Requires valid credentials."""
    client = GPPClient()
    success, error = await client.is_reachable()
    if success:
        print("[green]GPP is reachable. Credentials are valid.[/green]")
    else:
        print("[red]Failed to reach GPP or credentials are invalid.[/red]")
        if error:
            print(f"[red]Details: {error}[/red]")
        raise typer.Exit(code=1)


def main():
    app()
