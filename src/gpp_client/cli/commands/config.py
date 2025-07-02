import toml
import typer
from rich.console import Console
from rich.syntax import Syntax
from typing import Annotated

from ...config import GPPConfig

console = Console()

app = typer.Typer(
    name="config",
    help="Manage GPP client configuration settings.",
)


@app.command("show")
def show() -> None:
    """Print the full configuration in TOML format."""
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


@app.command("auth")
def auth(
    url: Annotated[str, typer.Option(help="GraphQL API URL.")],
    token: Annotated[str, typer.Option(help="Access token.")],
) -> None:
    """Set both the API URL and access token."""
    gpp_config = GPPConfig()

    if not gpp_config.exists:
        console.print(
            "[yellow]No configuration file found. Creating a new one.[/yellow]"
        )

    gpp_config.set_credentials(url=url, token=token)
    console.print("Credentials updated successfully.")


@app.command("path")
def path() -> None:
    """Display the absolute path to the configuration file."""
    config = GPPConfig()
    console.print(config.path)
