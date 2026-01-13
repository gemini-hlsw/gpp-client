from pathlib import Path
from typing import Annotated

import typer
from rich.console import Console
from rich.json import JSON

from gpp_client.cli.utils import async_command
from gpp_client.client import GPPClient

console = Console()
app = typer.Typer(name="att", help="Manage attachments.")


@app.command("dl")
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
    client = GPPClient()
    try:
        await client.attachment.download_by_id(
            attachment_id,
            save_to=save_to,
            overwrite=overwrite,
        )
    finally:
        await client.close()


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

    console.print(JSON.from_data(result))
