import typer
from .commands import program_note

app = typer.Typer()
app.add_typer(program_note.program_note, name="program-note")


def main():
    app()
