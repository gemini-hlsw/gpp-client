from dataclasses import asdict
from typing import Annotated

import typer
from rich.console import Console
from rich.json import JSON
from rich.syntax import Syntax

from gpp_client.config import GPPConfig, GPPDefaults, GPPEnvironment

console = Console()

app = typer.Typer(
    name="config",
    help="Manage GPP client configuration settings.",
)


@app.command("path")
def path() -> None:
    """Display the absolute path to the configuration file."""
    config = GPPConfig()
    typer.echo(config.path)


@app.command("show")
def show_config() -> None:
    """
    Display the current configuration in TOML format.
    """
    config = GPPConfig()

    if not config.exists():
        typer.secho("No configuration file found", fg="red")
        raise typer.Exit(code=1)

    toml_text = config.to_toml()
    syntax = Syntax(toml_text, "toml")
    console.print(syntax)


@app.command("set-token")
def set_token(
    env: Annotated[
        GPPEnvironment,
        typer.Argument(
            help="Environment to store the token for.", case_sensitive=False
        ),
    ],
    token: Annotated[str, typer.Argument(help="Bearer token to store.")],
    save: Annotated[
        bool,
        typer.Option(
            "--no-save",
            help="Apply the change without writing to disk.",
        ),
    ] = True,
):
    """
    Store a token for an environment.
    """
    config = GPPConfig()
    config.set_token(env, token, save=save)
    typer.echo(f"Token stored for environment: {env.value}")


@app.command("set-credentials")
def set_credentials(
    env: Annotated[
        GPPEnvironment,
        typer.Argument(
            help="Environment to store the token for.", case_sensitive=False
        ),
    ],
    token: Annotated[str, typer.Argument(help="Bearer token to store.")],
    no_activate: Annotated[
        bool,
        typer.Option(
            "--no-activate",
            help="Do not activate the environment after storing the token.",
        ),
    ] = False,
    save: Annotated[
        bool,
        typer.Option(
            "--no-save",
            help="Apply the change without writing to disk.",
        ),
    ] = True,
):
    """
    Store a token and activate the environment.
    """
    config = GPPConfig()
    config.set_credentials(env, token, activate=not no_activate, save=save)
    action = "stored" if no_activate else "stored and activated"
    typer.echo(f"Credentials {action} for: {env.value}")


@app.command("clear-token")
def clear_token(
    env: Annotated[
        GPPEnvironment,
        typer.Argument(help="Environment to clear token for", case_sensitive=False),
    ],
    save: Annotated[
        bool,
        typer.Option("--no-save", help="Apply change without writing to disk."),
    ] = True,
):
    """
    Remove stored token for a specific environment.
    """
    config = GPPConfig()
    config.clear_token(env, save=save)
    typer.echo(f"Cleared token for environment: {env.value}")


@app.command("clear-tokens")
def clear_tokens(
    save: Annotated[
        bool,
        typer.Option("--no-save", help="Apply change without writing to disk."),
    ] = True,
):
    """
    Remove all stored tokens.
    """
    config = GPPConfig()
    config.clear_tokens(save=save)
    typer.echo("Cleared all stored tokens.")


@app.command("activate")
def activate_env(
    env: Annotated[
        GPPEnvironment,
        typer.Argument(help="Environment to activate.", case_sensitive=False),
    ],
    save: Annotated[
        bool,
        typer.Option("--no-save", help="Apply change without writing to disk."),
    ] = True,
):
    """
    Set the active environment.
    """
    config = GPPConfig()
    config.activate(env, save=save)
    typer.echo(f"Activated environment: {env.value}")


@app.command("enable-env-vars")
def enable_env_vars(
    save: Annotated[
        bool,
        typer.Option("--no-save", help="Apply change without writing to disk."),
    ] = True,
):
    """
    Enable reading credentials from environment variables.
    """
    config = GPPConfig()
    config.enable_env_vars(save=save)
    typer.echo("Environment variable usage enabled.")


@app.command("disable-env-vars")
def disable_env_vars(
    save: Annotated[
        bool,
        typer.Option("--no-save", help="Apply change without writing to disk."),
    ] = True,
):
    """
    Disable reading credentials from environment variables.
    """
    config = GPPConfig()
    config.disable_env_vars(save=save)
    typer.echo("Environment variable usage disabled.")


@app.command("list-tokens")
def list_tokens() -> None:
    """
    List all stored tokens and the environments they belong to.
    """
    config = GPPConfig()
    tokens = config.get_all_envs_with_tokens()

    if not tokens:
        typer.echo("No stored tokens found.")
        return

    for env, token in tokens.items():
        typer.echo(f"{env.value}: {token}")


@app.command("init")
def init_config(
    force: Annotated[
        bool,
        typer.Option("--force", help="Overwrite existing config if present."),
    ] = False,
):
    """
    Create an empty configuration file.
    """
    path = GPPConfig._get_app_dir()

    if path.exists() and not force:
        typer.secho(
            f"Config already exists at {path}. Use --force to overwrite.",
            fg=typer.colors.YELLOW,
        )
        raise typer.Exit(code=1)

    GPPConfig.create_default_config_file()
    typer.echo(f"Created new config at {path}")


@app.command("defaults")
def show_defaults() -> None:
    """
    Show default values and environment variable names.
    """
    console.print(JSON.from_data(asdict(GPPDefaults)))
