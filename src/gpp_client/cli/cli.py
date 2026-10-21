"""
CLI entry point for GPP Client.
"""

__all__ = ["app"]

from dataclasses import dataclass
from enum import Enum
from typing import Annotated

import typer

from gpp_client import __version__
from gpp_client.cli import output
from gpp_client.cli.commands import (
    attachment_app,
    config_app,
    goats_app,
    observation_app,
    program_app,
    scheduler_app,
    site_status_app,
    target_app,
    workflow_state_app,
)
from gpp_client.cli.utils import async_command, open_client
from gpp_client.environment import GPPEnvironment


@dataclass(slots=True)
class CLIState:
    """
    Shared CLI state.
    """

    debug: bool = False
    environment: str | None = None


CLIEnvironment = Enum(
    "CLIEnvironment",
    {env.name: env.label for env in GPPEnvironment},
    type=str,
)
"""The environments offered to CLI users."""


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
    env: Annotated[
        CLIEnvironment | None,
        typer.Option(
            "--env",
            help=(
                "GPP environment for this command. Overrides GPP_ENVIRONMENT "
                "and config.toml."
            ),
            case_sensitive=False,
        ),
    ] = None,
):
    """Main entry point callback for GPP Client CLI."""
    ctx.obj = CLIState(debug=debug, environment=env.value if env else None)


@app.command("ping")
@async_command
async def ping(ctx: typer.Context) -> None:
    """Ping GPP. Requires valid credentials."""
    async with open_client(ctx) as client:
        success, error = await client.ping()
    if not success:
        output.fail(f"Failed to reach GPP: {error}")
        raise typer.Exit(code=1)

    output.success("GPP is reachable. Credentials are valid.")


app.add_typer(observation_app)
app.add_typer(program_app)
app.add_typer(attachment_app)
app.add_typer(target_app)
app.add_typer(workflow_state_app)
app.add_typer(site_status_app)
app.add_typer(goats_app)
app.add_typer(scheduler_app)
app.add_typer(config_app)


def main() -> None:
    """Main entry point for GPP Client CLI."""
    app()


if __name__ == "__main__":
    main()
