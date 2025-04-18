import asyncio
from typing import Any

import typer
from rich.console import Console
from rich.json import JSON
from rich.table import Table

from ...client import GPPClient
from ..utils import truncate_text, truncate_title, async_command

program_note = typer.Typer(help="Manage Program Notes.")
console = Console()


@program_note.command("get-all")
@async_command
async def get_all(
    limit: int = typer.Option(100, help="Max number of results."),
    include_deleted: bool = typer.Option(False, help="Include deleted entries."),
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
        note_id = str(note.get("id", "<No ID>"))
        title = truncate_title(note.get("title", "<No Title>"))
        text = truncate_text(note.get("text", "<No Text>"))
        table.add_row(note_id, title, text)

    console.print(table)


@program_note.command("get")
@async_command
async def get(
    resource_id: str = typer.Argument(..., help="ID of the program note to retrieve."),
):
    """Retrieve a program note by its unique ID."""
    client = GPPClient()
    result = await client.program_note.get_by_id(resource_id=resource_id)
    program_note = result.get("programNote")

    if not program_note:
        print_not_found()
        return

    console.print(JSON.from_data(program_note))


def print_not_found():
    console.print("[bold yellow]No program note(s) found.[/bold yellow]")
