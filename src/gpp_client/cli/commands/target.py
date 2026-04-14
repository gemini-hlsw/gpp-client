"""
Target CLI commands.
"""

__all__ = ["target_app"]

from typing import Annotated

import typer

from gpp_client.cli import output
from gpp_client.cli.utils import async_command, require_exactly_one
from gpp_client.client import GPPClient

target_app = typer.Typer(name="target", help="Target operations.")


@target_app.command("get")
@async_command
async def get_target(
    target_id: Annotated[
        str | None,
        typer.Option(
            "--target-id",
            help="Get a target by ID.",
        ),
    ] = None,
    include_deleted: Annotated[
        bool,
        typer.Option(
            "--include-deleted",
            help="Include deleted program data in the result.",
        ),
    ] = False,
) -> None:
    """
    Get a target using exactly one selector.
    """
    selector_name, selector_value = require_exactly_one(
        target_id=target_id,
    )

    with output.status("Fetching target..."):
        async with GPPClient() as client:
            match selector_name:
                case "target_id":
                    result = await client.target.get_by_id(
                        target_id=selector_value,
                        include_deleted=include_deleted,
                    )
                case _:
                    raise typer.BadParameter(f"Unsupported selector: {selector_name}")

    output.json_pydantic(result)


@target_app.command("list")
@async_command
async def list_targets(
    include_deleted: Annotated[
        bool,
        typer.Option(
            "--include-deleted",
            help="Include deleted targets.",
        ),
    ] = False,
    offset: Annotated[
        str | None,
        typer.Option(
            "--offset",
            help="Pagination offset.",
        ),
    ] = None,
    limit: Annotated[
        int | None,
        typer.Option(
            "--limit",
            min=1,
            help="Maximum number of targets to return.",
        ),
    ] = None,
) -> None:
    """
    List targets.
    """
    with output.status("Fetching targets..."):
        async with GPPClient() as client:
            result = await client.target.get_all(
                include_deleted=include_deleted,
                offset=offset,
                limit=limit,
            )

    output.json_pydantic(result)
