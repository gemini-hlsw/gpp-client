"""
Attachment CLI commands.
"""

__all__ = ["attachment_app"]

from typing import Annotated

import typer

from gpp_client.cli import output
from gpp_client.cli.utils import async_command, require_exactly_one
from gpp_client.client import GPPClient

attachment_app = typer.Typer(
    name="attachment",
    help="Attachment operations.",
)


@attachment_app.command("list")
@async_command
async def list_attachments(
    observation_id: Annotated[
        str | None,
        typer.Option(
            "--observation-id",
            help="List attachments by observation ID.",
        ),
    ] = None,
    observation_reference: Annotated[
        str | None,
        typer.Option(
            "--observation-reference",
            help="List attachments by observation reference.",
        ),
    ] = None,
    program_id: Annotated[
        str | None,
        typer.Option(
            "--program-id",
            help="List attachments by program ID.",
        ),
    ] = None,
    program_reference: Annotated[
        str | None,
        typer.Option(
            "--program-reference",
            help="List attachments by program reference.",
        ),
    ] = None,
    proposal_reference: Annotated[
        str | None,
        typer.Option(
            "--proposal-reference",
            help="List attachments by proposal reference.",
        ),
    ] = None,
) -> None:
    """
    List attachments using exactly one selector.
    """
    selector_name, selector_value = require_exactly_one(
        observation_id=observation_id,
        observation_reference=observation_reference,
        program_id=program_id,
        program_reference=program_reference,
        proposal_reference=proposal_reference,
    )

    with output.status("Fetching attachments..."):
        async with GPPClient() as client:
            match selector_name:
                case "observation_id":
                    result = await client.attachment.get_all_by_observation_id(
                        observation_id=selector_value
                    )
                case "observation_reference":
                    result = await client.attachment.get_all_by_observation_reference(
                        observation_reference=selector_value
                    )
                case "program_id":
                    result = await client.attachment.get_all_by_program_id(
                        program_id=selector_value
                    )
                case "program_reference":
                    result = await client.attachment.get_all_by_program_reference(
                        program_reference=selector_value
                    )
                case "proposal_reference":
                    result = await client.attachment.get_all_by_proposal_reference(
                        proposal_reference=selector_value
                    )
                case _:
                    raise typer.BadParameter(f"Unsupported selector: {selector_name}")

    output.json_pydantic(result)
