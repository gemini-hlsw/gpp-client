import typer
from .commands import program_note, program, config, call_for_proposals

app = typer.Typer()
app.add_typer(config.config, name="config")
app.add_typer(program_note.program_note, name="program-note")
app.add_typer(program.program, name="program")
app.add_typer(call_for_proposals.call_for_proposals, name="call-for-proposals")


def main():
    app()
