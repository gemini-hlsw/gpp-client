"""
Site status CLI commands.
"""

__all__ = ["site_status_app"]

from typing import Annotated

import typer

from gpp_client.cli import output
from gpp_client.cli.utils import async_command
from gpp_client.client import GPPClient
from gpp_client.domains.site_status import Site

site_status_app = typer.Typer(
    name="site-status",
    help="Site status operations.",
)


@site_status_app.command("get")
@async_command
async def get_site_status(
    site_id: Annotated[
        Site,
        typer.Argument(help="Site identifier: north or south."),
    ],
) -> None:
    """
    Get site status by site ID.
    """
    with output.status("Fetching site status..."):
        async with GPPClient() as client:
            result = await client.site_status.get_by_id(site_id=site_id.value)

    output.json(result)
