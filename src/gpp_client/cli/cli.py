import typer

from .commands import (
    call_for_proposals,
    config,
    observation,
    program,
    program_note,
    site_status,
    target,
)

app = typer.Typer(
    name="GPP Client", no_args_is_help=True, help="Client to communicate with GPP."
)
app.add_typer(config.app)
app.add_typer(program_note.app)
app.add_typer(target.app)
app.add_typer(program.app)
app.add_typer(call_for_proposals.app)
app.add_typer(observation.app)
app.add_typer(site_status.app)


def main():
    app()
