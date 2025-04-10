import typer
from .commands.call_for_proposals import call_for_proposals

app = typer.Typer(help="GPP CLI to manage programs, proposals, and more.")

# Add call_for_proposals subcommands
app.add_typer(call_for_proposals, name="cfp")

def main():
    app()

if __name__ == "__main__":
    main()