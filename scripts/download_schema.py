#!/usr/bin/env python3
"""
Download GraphQL schema for a specific GPP environment.
"""

import subprocess
from pathlib import Path
from typing import Annotated, NoReturn

import typer
from rich.console import Console

from gpp_client.config import GPPDefaults, GPPEnvironment
from gpp_client.credentials import EnvVarReader

console = Console()

app = typer.Typer(
    help="Download the GraphQL schema for a given GPP environment.",
    add_completion=False,
)


def fail(message: str) -> NoReturn:
    console.print(f"[bold]Error:[/bold] {message}", style="red")
    raise typer.Exit(code=1)


@app.command()
def main(
    env: Annotated[
        GPPEnvironment,
        typer.Argument(
            help="Environment to download schema for.",
            case_sensitive=False,
        ),
    ],
    output_dir: Annotated[
        Path,
        typer.Option(
            "--output-dir",
            "-o",
            help="Directory where the schema file will be saved.",
            exists=False,
            file_okay=False,
            dir_okay=True,
        ),
    ] = Path("schemas"),
) -> None:
    """
    Download the GraphQL schema for a specific environment.

    Parameters
    ----------
    env : GPPEnvironment
        The GPP environment to download the schema for.
    output_dir : Path, optional
        The directory where the schema file will be saved.
    """
    typer.echo(f"Downloading schema for environment: {env.value}")

    token = EnvVarReader.get_env_token(env)
    if not token:
        expected_key = GPPDefaults.env_var_env_tokens.get(env)
        fail(
            f"No token found for environment {env.value}. "
            f"Make sure the environment variable '{expected_key}' is set."
        )
    typer.echo("Token found in environment variables.")

    url = GPPDefaults.url.get(env)
    if not url:
        fail(f"No URL defined for environment {env.value}")
    typer.echo(f"Using URL: {url}")

    output_dir.mkdir(exist_ok=True)
    output_file = output_dir / f"{env.value.lower()}.schema.graphql"

    cmd = [
        "gql-cli",
        url,
        "--transport",
        "aiohttp",
        "--print-schema",
        "--schema-download",
        "-H",
        f"Authorization:Bearer {token}",
    ]
    with console.status("Downloading schema..."):
        try:
            result = subprocess.run(
                cmd,
                check=True,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
            )
            output_file.write_bytes(result.stdout)

        except subprocess.CalledProcessError as exc:
            fail(exc.stderr)

    typer.echo("Schema download completed successfully")
    typer.echo(f"Schema saved to {output_file}")


if __name__ == "__main__":
    app()
