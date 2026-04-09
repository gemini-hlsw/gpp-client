#!/usr/bin/env python3
"""
Download GraphQL schema for a specific GPP environment.
"""

import subprocess
from pathlib import Path
from typing import Annotated

import typer

from gpp_client.cli import output
from gpp_client.environment import GPPEnvironment
from gpp_client.exceptions import GPPAuthError
from gpp_client.settings import GPPSettings
from gpp_client.urls import get_graphql_url

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
) -> None:
    """
    Download the GraphQL schema for a specific environment.
    """
    output.info(f"Downloading schema for environment: {env.value}")

    settings = GPPSettings(environment_override=env)
    try:
        token = settings.resolved_token
    except GPPAuthError as exc:
        output.fail(str(exc))
        raise typer.Exit(code=1)

    url = get_graphql_url(settings.environment)

    output.info(f"Using URL: {url}")

    output_dir = Path(f"graphql/{env.value.lower()}/")
    output_dir.mkdir(exist_ok=True)
    output_file = output_dir / "schema.graphql"

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
