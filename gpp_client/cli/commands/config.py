import toml
import typer
from rich.console import Console
from rich.syntax import Syntax

from ...config import GPPConfig

console = Console()

config = typer.Typer(name="config", help="Manage GPP client configuration settings.")


@config.command("show")
def show() -> None:
    """Display all configuration values."""
    config = GPPConfig()

    if not config.exists:
        console.print("[red]No configuration file found.[/red]")
        raise typer.Exit(code=1)

    if not config._data:
        console.print("[red]Configuration is empty.[/red]")
        raise typer.Exit(code=1)

    data = config.get()

    credentials = data.get("credentials", {})
    if credentials.get("token"):
        credentials["token"] = "*******"

    toml_text = toml.dumps(config.get())

    syntax = Syntax(toml_text, "toml")
    console.print(syntax)


@config.command("set-credentials")
def set_credentials(
    url: str = typer.Option(..., help="GraphQL API URL."),
    token: str = typer.Option(..., help="Access token."),
) -> None:
    """Set both the API URL and access token."""
    gpp_config = GPPConfig()

    if not gpp_config.exists:
        console.print(
            "[yellow]No configuration file found. Creating a new one.[/yellow]"
        )

    gpp_config.set_credentials(url=url, token=token)
    console.print("Credentials updated successfully.")


@config.command("path")
def path() -> None:
    """Display the path to the configuration file."""
    config = GPPConfig()
    console.print(config.path)
