#!/usr/bin/env python3
"""
Download GraphQL schema for a specific GPP environment.
"""

import subprocess
from pathlib import Path
from typing import Annotated

import typer

from gpp_client.cli import output
from gpp_client.config import GPPDefaults, GPPEnvironment
from gpp_client.credentials import EnvVarReader

app = typer.Typer(
    help="Download the GraphQL schema for a given GPP environment.",
    add_completion=False,
)


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
    """
    output.info(f"Downloading schema for environment: {env.value}")

    token = EnvVarReader.get_env_token(env)
    if not token:
        expected_key = GPPDefaults.env_var_env_tokens.get(env)
        output.fail(
            f"No token found for environment {env.value}. "
            f"Make sure the environment variable '{expected_key}' is set."
        )
        raise typer.Exit(code=1)

    output.info("Token found in environment variables.")
    url = GPPDefaults.url.get(env)
    if not url:
        output.fail(f"No URL defined for environment {env.value}")
        raise typer.Exit(code=1)

    output.info(f"Using URL: {url}")

    output_dir.mkdir(exist_ok=True)
    output_file = output_dir / f"{env.value.lower()}.schema.graphql"

    cmd = [
        "gql-cli",
        url,
        "--transport",
        "aiohttp",
        "--print-schema",
        "--schema-download",
        "input_value_deprecation:true",
        "-H",
        f"Authorization:Bearer {token}",
    ]
    with output.status("Downloading schema..."):
        try:
            result = subprocess.run(
                cmd,
                check=True,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
            )
            output_file.write_bytes(result.stdout)

        except subprocess.CalledProcessError as exc:
            output.fail(exc.stderr)
            raise typer.Exit(code=1) from exc

    output.info(f"Schema saved to {output_file}")
    output.success("Schema download completed successfully")


if __name__ == "__main__":
    app()
