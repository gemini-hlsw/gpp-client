"""
Observation CLI commands.
"""

__all__ = ["observation_app"]

from typing import Annotated

import typer

from gpp_client.cli import output
from gpp_client.cli.utils import async_command, require_exactly_one
from gpp_client.client import GPPClient

observation_app = typer.Typer(name="observation", help="Observation operations.")


@observation_app.command("get")
@async_command
async def get_observation(
    observation_id: Annotated[
        str | None,
        typer.Option(
            "--observation-id",
            help="Get an observation by ID.",
        ),
    ] = None,
    observation_reference: Annotated[
        str | None,
        typer.Option(
            "--observation-reference",
            help="Get an observation by reference.",
        ),
    ] = None,
) -> None:
    """
    Get an observation using exactly one selector.

    Parameters
    ----------
    observation_id : str | None, optional
        Observation ID.
    observation_reference : str | None, optional
        Observation reference label.
    """
    selector_name, selector_value = require_exactly_one(
        observation_id=observation_id,
        observation_reference=observation_reference,
    )

    with output.status("Fetching observation..."):
        async with GPPClient() as client:
            match selector_name:
                case "observation_id":
                    result = await client.observation.get_by_id(
                        observation_id=selector_value
                    )
                case "observation_reference":
                    result = await client.observation.get_by_reference(
                        observation_reference=selector_value
                    )
                case _:
                    raise typer.BadParameter(f"Unsupported selector: {selector_name}")

    output.json_pydantic(result)


@observation_app.command("list")
@async_command
async def list_observations(
    include_deleted: Annotated[
        bool,
        typer.Option(
            "--include-deleted",
            help="Include deleted observations.",
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
            help="Maximum number of observations to return.",
        ),
    ] = None,
) -> None:
    """
    List observations.

    Parameters
    ----------
    include_deleted : bool, optional
        Whether to include deleted observations.
    offset : str | None, optional
        Pagination offset.
    limit : int | None, optional
        Maximum number of observations to return.
    """
    with output.status("Fetching observations..."):
        async with GPPClient() as client:
            result = await client.observation.get_all(
                include_deleted=include_deleted,
                offset=offset,
                limit=limit,
            )
    output.json_pydantic(result)
