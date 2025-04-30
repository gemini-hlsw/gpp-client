import typer
from rich.console import Console
from rich.json import JSON
from rich.table import Table
from typing import Optional

from ...client import GPPClient
from ...schema import enums
from ..utils import async_command, print_not_found, truncate_long, truncate_short

program_note = typer.Typer(help="Manage Program Notes.")
console = Console()


@program_note.command("get-all")
@async_command
async def get_all(
    limit: Optional[int] = typer.Option(None, help="Max number of results."),
    include_deleted: Optional[bool] = typer.Option(
        None, help="Include deleted notes in search.", is_flag=True
    ),
):
    """List all program notes the user has access to."""
    client = GPPClient()
    result = await client.program_note.get_batch(
        limit=limit,
        include_deleted=include_deleted,
    )
    notes = result.get("programNotes", {}).get("matches", [])

    if not notes:
        print_not_found()
        return

    table = Table(title="Program Notes")
    table.add_column("ID", no_wrap=True)
    table.add_column("Title")
    table.add_column("Text")

    for note in notes:
        note_id = str(note.get("id"))
        title = truncate_long(note.get("title"))
        text = truncate_short(note.get("text"))
        table.add_row(note_id, title, text)

    console.print(table)


@program_note.command("get")
@async_command
async def get(
    id: str = typer.Argument(..., help="ID of the program note to retrieve."),
):
    """Retrieve a program note by its unique ID."""
    client = GPPClient()
    result = await client.program_note.get_by_id(resource_id=id)
    program_note = result.get("programNote")

    if not program_note:
        print_not_found()
        return

    console.print(JSON.from_data(program_note))


@program_note.command("create")
@async_command
async def create(
    title: str = typer.Option(..., help="Title of the note."),
    text: str = typer.Option(..., help="Content of the note."),
    program_id: str = typer.Option(None, help="Program ID (e.g., p-2025A-001)."),
    program_reference: str = typer.Option(
        None, help="Program reference (e.g., GN-2025A-Q-123)."
    ),
    proposal_reference: str = typer.Option(None, help="Proposal reference."),
    is_private: bool = typer.Option(False, help="Mark note as private."),
):
    """Create a new program note. Must provide one identifier (e.g. program ID,
    proposal reference, or program reference).
    """
    client = GPPClient()
    note = await client.program_note.create(
        title=title,
        text=text,
        program_id=program_id,
        program_reference=program_reference,
        proposal_reference=proposal_reference,
        is_private=is_private,
    )
    console.print(JSON.from_data(note))


@program_note.command("update")
@async_command
async def update(
    id: str = typer.Argument(..., help="Program note ID (e.g., n-abc123)."),
    title: str = typer.Option(None, help="New title."),
    text: str = typer.Option(None, help="New text."),
    is_private: bool = typer.Option(None, help="Change privacy status."),
    existence: enums.Existence = typer.Option(None, help="Set existence."),
    include_deleted: Optional[bool] = typer.Option(
        None, help="Include deleted notes in search.", is_flag=True
    ),
):
    """Update an existing program note."""
    client = GPPClient()
    note = await client.program_note.update_by_id(
        resource_id=id,
        title=title,
        text=text,
        is_private=is_private,
        existence=existence,
        include_deleted=include_deleted,
    )
    console.print(JSON.from_data(note["updateProgramNotes"]["programNotes"][0]))
