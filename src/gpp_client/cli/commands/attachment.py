"""
CLI commands for managing attachments.
"""

__all__ = ["app"]

from pathlib import Path
from typing import Annotated

import typer

from gpp_client.api.enums import AttachmentType
from gpp_client.cli import output
from gpp_client.cli.utils import async_command
from gpp_client.client import GPPClient

app = typer.Typer(name="att", help="Manage attachments.")


@app.command("download")
@async_command
async def download_by_id(
    attachment_id: Annotated[
        str,
        typer.Argument(help="Attachment ID.", case_sensitive=False),
    ],
    save_to: Annotated[
        Path | None,
        typer.Option(
            "--save-to",
            help="Destination directory for the download (default: ~/).",
            file_okay=False,
            dir_okay=True,
            writable=True,
            resolve_path=True,
        ),
    ] = None,
    overwrite: Annotated[
        bool,
        typer.Option(
            "--overwrite",
            help="Overwrite the file if it already exists.",
        ),
    ] = False,
) -> None:
    """Download an attachment by ID."""
    async with GPPClient() as client:
        path = await client.attachment.download_by_id(
            attachment_id,
            save_to=save_to,
            overwrite=overwrite,
        )

    if path is not None:
        output.info(f"Attachment downloaded to: {path}")


@app.command("update")
@async_command
async def update_by_id(
    attachment_id: Annotated[
        str,
        typer.Argument(help="Attachment ID.", case_sensitive=False),
    ],
    file_name: Annotated[
        str,
        typer.Option("--file-name", help="File name for the attachment."),
    ],
    file_path: Annotated[
        Path,
        typer.Option(
            "--file-path",
            help="Path to the new file content for the attachment.",
            exists=True,
            file_okay=True,
            dir_okay=False,
            readable=True,
            resolve_path=True,
        ),
    ],
    description: Annotated[
        str | None,
        typer.Option("--description", help="New description for the attachment."),
    ] = None,
) -> None:
    """Update an attachment by ID."""
    async with GPPClient() as client:
        await client.attachment.update_by_id(
            attachment_id,
            file_name=file_name,
            description=description,
            file_path=file_path,
        )
    output.info(f"Attachment with ID {attachment_id} has been updated.")


@app.command("delete")
@async_command
async def delete_by_id(
    attachment_id: Annotated[
        str,
        typer.Argument(help="Attachment ID.", case_sensitive=False),
    ],
) -> None:
    """Delete an attachment by ID."""
    async with GPPClient() as client:
        await client.attachment.delete_by_id(attachment_id)
    output.info(f"Attachment with ID {attachment_id} has been deleted.")


@app.command("upload")
@async_command
async def upload(
    file_path: Annotated[
        Path,
        typer.Option(
            "--file-path",
            help="Path to the file content for the attachment.",
            exists=True,
            file_okay=True,
            dir_okay=False,
            readable=True,
            resolve_path=True,
        ),
    ],
    program_id: Annotated[
        str,
        typer.Option("--program-id", help="Program ID.", case_sensitive=False),
    ],
    attachment_type: Annotated[
        AttachmentType,
        typer.Option("--attachment-type", help="Attachment type."),
    ],
    file_name: Annotated[
        str,
        typer.Option("--file-name", help="File name for the attachment."),
    ],
    description: Annotated[
        str | None,
        typer.Option("--description", help="Description for the attachment."),
    ] = None,
) -> None:
    """Upload an attachment to a program."""
    async with GPPClient() as client:
        attachment_id = await client.attachment.upload(
            program_id=program_id,
            attachment_type=attachment_type,
            file_name=file_name,
            description=description,
            file_path=file_path,
        )

    output.info(f"Attachment uploaded with ID: {attachment_id}")


@app.command("list")
@async_command
async def list_attachments(
    observation_id: Annotated[
        str | None,
        typer.Option("--observation-id", help="Observation ID.", case_sensitive=False),
    ] = None,
    observation_reference: Annotated[
        str | None,
        typer.Option(
            "--observation-reference",
            help="Observation reference.",
            case_sensitive=False,
        ),
    ] = None,
    program_id: Annotated[
        str | None,
        typer.Option("--program-id", help="Program ID.", case_sensitive=False),
    ] = None,
    program_reference: Annotated[
        str | None,
        typer.Option(
            "--program-reference", help="Program reference.", case_sensitive=False
        ),
    ] = None,
    proposal_reference: Annotated[
        str | None,
        typer.Option(
            "--proposal-reference", help="Proposal reference.", case_sensitive=False
        ),
    ] = None,
) -> None:
    """List attachments by observation or program (exactly one identifier required)."""
    observation_keys = [observation_id, observation_reference]
    program_keys = [program_id, program_reference, proposal_reference]

    has_observation = any(v is not None for v in observation_keys)
    has_program = any(v is not None for v in program_keys)

    if has_observation and has_program:
        raise typer.BadParameter(
            "Provide observation identifiers OR program identifiers, not both."
        )

    if not has_observation and not has_program:
        raise typer.BadParameter(
            "Provide exactly one of: --observation-id/--observation-reference "
            "OR --program-id/--program-reference/--proposal-reference."
        )

    if has_observation:
        if sum(v is not None for v in observation_keys) != 1:
            raise typer.BadParameter(
                "Provide exactly one of --observation-id or --observation-reference."
            )
    else:
        if sum(v is not None for v in program_keys) != 1:
            raise typer.BadParameter(
                "Provide exactly one of --program-id, --program-reference, or --proposal-reference."
            )

    async with GPPClient() as client:
        if has_observation:
            result = await client.attachment.get_all_by_observation(
                observation_id=observation_id,
                observation_reference=observation_reference,
            )
        else:
            result = await client.attachment.get_all_by_program(
                program_id=program_id,
                program_reference=program_reference,
                proposal_reference=proposal_reference,
            )

    output.json(result)
