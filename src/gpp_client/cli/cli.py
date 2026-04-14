"""
CLI entry point for GPP Client.
"""

__all__ = ["app"]

from dataclasses import dataclass
from importlib.metadata import version as get_version
from typing import Annotated

import typer

from gpp_client.cli import output
from gpp_client.cli.commands import (
    attachment_app,
    goats_app,
    observation_app,
    program_app,
    scheduler_app,
    site_status_app,
    target_app,
    workflow_state_app,
)
from gpp_client.cli.utils import async_command
from gpp_client.client import GPPClient
from gpp_client.settings import get_config_path as _get_config_path

__version__ = get_version("gpp-client").strip()


@dataclass(slots=True)
class CLIState:
    """
    Shared CLI state.
    """

    debug: bool = False


app = typer.Typer(
    name="GPP Client", no_args_is_help=False, help="Client to communicate with GPP."
)


def version_callback(value: bool) -> None:
    """
    Callback to print version and exit.

    Parameters
    ----------
    value : bool
        Whether to print the version and exit.
    """
    if value:
        output.info(f"{__version__}")
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


@app.command("ping")
@async_command
async def ping() -> None:
    """Ping GPP. Requires valid credentials."""
    client = GPPClient()
    success, error = await client.ping()
    if not success:
        output.fail(f"Failed to reach GPP: {error}")
        raise typer.Exit(code=1)

    output.success("GPP is reachable. Credentials are valid.")


@app.command("get-config-path")
def get_config_path() -> None:
    """Get the path to the GPP Client configuration file."""

    config_path = _get_config_path()
    output.info(f"{config_path.resolve()}")


app.add_typer(observation_app)
app.add_typer(program_app)
app.add_typer(attachment_app)
app.add_typer(target_app)
app.add_typer(workflow_state_app)
app.add_typer(site_status_app)
app.add_typer(goats_app)
app.add_typer(scheduler_app)


def main() -> None:
    """Main entry point for GPP Client CLI."""
    app()


if __name__ == "__main__":
    main()
