"""
Program CLI commands.
"""

__all__ = ["program_app"]

from typing import Annotated

import typer

from gpp_client.cli import output
from gpp_client.cli.utils import async_command, require_exactly_one
from gpp_client.client import GPPClient

program_app = typer.Typer(name="program", help="Program operations.")


@program_app.command("get")
@async_command
async def get_program(
    program_id: Annotated[
        str | None,
        typer.Option("--program-id", help="Get a program by ID."),
    ] = None,
    program_reference: Annotated[
        str | None,
        typer.Option(
            "--program-reference",
            help="Get a program by reference.",
        ),
    ] = None,
    proposal_reference: Annotated[
        str | None,
        typer.Option(
            "--proposal-reference",
            help="Get a program by proposal reference.",
        ),
    ] = None,
    include_deleted: Annotated[
        bool,
        typer.Option(
            "--include-deleted",
            help="Include deleted related records.",
        ),
    ] = False,
) -> None:
    """
    Get a program using exactly one selector.

    Parameters
    ----------
    program_id : str | None, optional
        Program ID.
    program_reference : str | None, optional
        Program reference label.
    proposal_reference : str | None, optional
        Proposal reference label.
    include_deleted : bool, optional
        Whether deleted related records should be included.
    """
    selector_name, selector_value = require_exactly_one(
        program_id=program_id,
        program_reference=program_reference,
        proposal_reference=proposal_reference,
    )

    with output.status("Fetching program..."):
        async with GPPClient() as client:
            match selector_name:
                case "program_id":
                    result = await client.program.get_by_id(
                        program_id=selector_value,
                        include_deleted=include_deleted,
                    )
                case "program_reference":
                    result = await client.program.get_by_reference(
                        program_reference=selector_value,
                        include_deleted=include_deleted,
                    )
                case "proposal_reference":
                    result = await client.program.get_by_proposal_reference(
                        proposal_reference=selector_value,
                        include_deleted=include_deleted,
                    )
                case _:
                    raise typer.BadParameter(f"Unsupported selector: {selector_name}")

    output.json_pydantic(result)


@program_app.command("list")
@async_command
async def list_programs(
    include_deleted: Annotated[
        bool,
        typer.Option(
            "--include-deleted",
            help="Include deleted programs.",
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
            help="Maximum number of programs to return.",
        ),
    ] = None,
) -> None:
    """
    List programs.

    Parameters
    ----------
    include_deleted : bool, optional
        Whether deleted programs should be included.
    offset : str | None, optional
        Pagination offset.
    limit : int | None, optional
        Maximum number of programs to return.
    """
    with output.status("Fetching programs..."):
        async with GPPClient() as client:
            result = await client.program.get_all(
                include_deleted=include_deleted,
                offset=offset,
                limit=limit,
            )

    output.json_pydantic(result)
