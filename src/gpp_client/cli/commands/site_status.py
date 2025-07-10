from typing import Annotated

import typer
from rich.console import Console
from rich.json import JSON

from ...client import GPPClient
from ...managers.site_status import Site
from ..utils import async_command

console = Console()
app = typer.Typer(name="site", help="Retrieve site status.")


@app.command("get")
@async_command
async def get_by_id(
    site_id: Annotated[
        Site,
        typer.Argument(
            help="Site name: north or south (case-insensitive).", case_sensitive=False
        ),
    ],
) -> None:
    """Get site status for Gemini North or South."""
    client = GPPClient()
    result = await client.site_status.get_by_id(site_id)
    console.print(JSON.from_data(result))
