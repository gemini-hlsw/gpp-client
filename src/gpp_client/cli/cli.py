import typer
from rich.console import Console

from gpp_client.cli.commands import (
    call_for_proposals,
    config,
    configuration_request,
    goats,
    group,
    observation,
    program,
    program_note,
    scheduler,
    site_status,
    target,
    workflow_state,
)
from gpp_client.cli.utils import async_command
from gpp_client.client import GPPClient
from gpp_client.exceptions import GPPClientError

console = Console()


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
app.add_typer(configuration_request.app)
app.add_typer(workflow_state.app)
app.add_typer(scheduler.app)
app.add_typer(goats.app)


@app.command("ping")
@async_command
async def ping() -> None:
    """Ping GPP. Requires valid credentials."""
    client = GPPClient()
    success, error = await client.is_reachable()
    if success:
        typer.secho("GPP is reachable. Credentials are valid.")
    else:
        raise GPPClientError(f"Failed to reach GPP: {error}")


def main():
    app()
