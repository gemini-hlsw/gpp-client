"""
CLI entry point for GPP Client.
"""

__all__ = ["app"]

from dataclasses import dataclass
from enum import Enum
from typing import Annotated

import typer

from gpp_client import __version__, settings
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
from gpp_client.cli.utils import async_command, open_client
from gpp_client.environment import GPPEnvironment
from gpp_client.exceptions import GPPClientError
from gpp_client.settings import get_config_path as _get_config_path


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
async def ping() -> None:
    """Ping GPP. Requires valid credentials."""
    async with open_client() as client:
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


@app.command("set-default-env")
def set_default_env(
    env: Annotated[
        CLIEnvironment,
        typer.Argument(
            help="Environment to use when none is given.", case_sensitive=False
        ),
    ],
) -> None:
    """Store the default GPP environment in the configuration file."""
    try:
        path = settings.set_default_environment(env.value)
    except GPPClientError as exc:
        output.fail(str(exc))
        raise typer.Exit(code=1) from exc

    output.success(f"Default environment set to {env.value} in {path}.")


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
