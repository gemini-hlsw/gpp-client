"""
CLI entry point for GPP Client.
"""

__all__ = ["app"]

from importlib.metadata import version as get_version
from typing import Annotated
from dataclasses import dataclass
import typer

from gpp_client.cli import output
from gpp_client.cli.commands import (
    attachment,
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

__version__ = get_version("gpp-client").strip()


@dataclass(slots=True)
class CLIState:
    debug: bool = False


app = typer.Typer(
    name="GPP Client", no_args_is_help=False, help="Client to communicate with GPP."
)


def version_callback(value: bool):
    if value:
        print(f"{__version__}")
        raise typer.Exit()


@app.callback()
def main_callback(
    ctx: typer.Context,
    version: Annotated[
        bool,
        typer.Option(
            "--version",
            help="Show the version and exit.",
            callback=version_callback,
            is_eager=True,
        ),
    ] = False,
    debug: Annotated[
        bool,
        typer.Option(
            "--debug",
            help="Show full exception tracebacks.",
        ),
    ] = False,
):
    """Main entry point callback for GPP Client CLI."""
    ctx.obj = CLIState(debug=debug)
    pass


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
app.add_typer(attachment.app)


@app.command("ping")
@async_command
async def ping() -> None:
    """Ping GPP. Requires valid credentials."""
    client = GPPClient()
    success, error = await client.is_reachable()
    if not success:
        output.fail(f"Failed to reach GPP: {error}")
        raise typer.Exit(code=1)

    output.success("GPP is reachable. Credentials are valid.")


def main() -> None:
    """Main entry point for GPP Client CLI."""
    app()


if __name__ == "__main__":
    main()
