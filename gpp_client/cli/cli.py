import typer
from .commands import program_note, program, config

app = typer.Typer()
app.add_typer(config.config, name="config")
app.add_typer(program_note.program_note, name="program-note")
app.add_typer(program.program, name="program")


def main():
    app()
