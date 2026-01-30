#!/usr/bin/env python3
"""
Compare GraphQL schemas.
"""

import subprocess
from pathlib import Path
from typing import Annotated

import typer
from gpp_client.cli import output


app = typer.Typer(
    help="Compare GraphQL schemas.",
    add_completion=False,
)


@app.command()
def main(
    schema1: Annotated[
        Path,
        typer.Argument(
            help="Path to the first schema file.",
            exists=True,
            file_okay=True,
            dir_okay=False,
            readable=True,
        ),
    ],
    schema2: Annotated[
        Path,
        typer.Argument(
            help="Path to the second schema file.",
            exists=True,
            file_okay=True,
            dir_okay=False,
            readable=True,
        ),
    ],
) -> None:
    """
    Compare two GraphQL schema files.
    """
    # Check if graphql-inspector is installed.
    output.info("Checking for graphql-inspector installation.")
    try:
        subprocess.run(
            ["graphql-inspector", "--help"],
            check=True,
            capture_output=True,
        )
    except Exception as exc:
        output.fail(
            "graphql-inspector is not installed. Please install it with 'npm i --global @graphql-inspector/cli graphql'."
        )
        raise typer.Exit(code=1) from exc
    output.success("graphql-inspector is installed.")
    output.space()

    output.procedure("Comparing schemas:")
    output.procedure_steps([f"{schema1}", f"{schema2}"])
    output.space()

    cmd = [
        "graphql-inspector",
        "diff",
        str(schema1),
        str(schema2),
        "--rule suppressRemovalOfDeprecatedField",
    ]

    try:
        result = subprocess.run(
            cmd,
            check=False,
            capture_output=True,
            text=True,
        )
        if result.returncode == 0:
            output.success("Schemas are identical.")
        else:
            output.warning("Schemas differ:")
            output.info(result.stdout)
    except Exception as exc:
        output.fail(f"An error occurred while comparing schemas: {exc}")
        raise typer.Exit(code=1) from exc


if __name__ == "__main__":
    app()
