#!/usr/bin/env python3
"""
Download the GraphQL schema for a specific GPP environment.
"""

import subprocess
from dataclasses import dataclass
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


class SchemaDownloadError(RuntimeError):
    """
    Raised when schema download fails.
    """


@dataclass(frozen=True)
class SchemaPaths:
    """
    Repository paths used by the schema download workflow.

    Parameters
    ----------
    root : Path
        Repository root directory.
    """

    root: Path

    @property
    def schemas_dir(self) -> Path:
        """
        Return the schema directory.

        Returns
        -------
        Path
            Schema directory.
        """
        return self.root / "graphql" / "schemas"

    def schema_file_path(self, env: GPPEnvironment) -> Path:
        """
        Return the schema file path for an environment.

        Parameters
        ----------
        env : GPPEnvironment
            Target environment.

        Returns
        -------
        Path
            Schema file path.
        """
        return self.schemas_dir / f"{env.value.lower()}.graphql"


def _get_token(env: GPPEnvironment) -> tuple[str, GPPEnvironment]:
    """
    Resolve the auth token and effective environment.

    Parameters
    ----------
    env : GPPEnvironment
        Target environment for the schema download.

    Returns
    -------
    str
        Resolved auth token.
    GPPEnvironment
        Effective environment used for the download.

    Raises
    ------
    SchemaDownloadError
        Raised if no valid token is available for the active environment.
    """
    try:
        settings = GPPSettings(environment_override=env)
        return settings.resolved_token, settings.environment
    except GPPAuthError as exc:
        raise SchemaDownloadError(str(exc)) from exc


def _download_schema(url: str, token: str) -> str:
    """
    Download a GraphQL schema from a URL.

    Parameters
    ----------
    url : str
        GraphQL endpoint URL.
    token : str
        Bearer token.

    Returns
    -------
    str
        Downloaded schema text.

    Raises
    ------
    SchemaDownloadError
        Raised if the download command fails.
    """
    cmd = [
        "gql-cli",
        url,
        "--transport",
        "aiohttp",
        "--print-schema",
        "--schema-download",
        "input_value_deprecation:true",
        "-H",
        f"Authorization: Bearer {token}",
    ]

    with output.status("Downloading schema..."):
        try:
            result = subprocess.run(
                cmd,
                check=True,
                capture_output=True,
                text=True,
                cwd=Path.cwd(),
            )
        except subprocess.CalledProcessError as exc:
            stderr = exc.stderr.strip() if exc.stderr else "Schema download failed."
            raise SchemaDownloadError(stderr) from exc

    return result.stdout


def _write_schema(schema_text: str, output_file: Path) -> None:
    """
    Write schema text to disk.

    Parameters
    ----------
    schema_text : str
        Schema text to write.
    output_file : Path
        Output file path.
    """
    output_file.parent.mkdir(parents=True, exist_ok=True)
    output_file.write_text(schema_text, encoding="utf-8")


def _run(env: GPPEnvironment) -> None:
    """
    Execute the schema download workflow.

    Parameters
    ----------
    env : GPPEnvironment
        Target environment.

    Raises
    ------
    SchemaDownloadError
        Raised if the workflow fails.
    """
    paths = SchemaPaths(root=Path.cwd())

    output.info(f"Downloading schema for environment: {env.value}")

    token, effective_env = _get_token(env)
    url = get_graphql_url(effective_env)
    output.info(f"Using URL: {url}")

    schema_text = _download_schema(url, token)
    output_file = paths.schema_file_path(env)
    _write_schema(schema_text, output_file)

    output.info(f"Schema saved to {output_file}")


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
    try:
        _run(env)
    except SchemaDownloadError as exc:
        output.fail(str(exc))
        raise typer.Exit(code=1) from exc

    output.success("Schema download completed successfully")


if __name__ == "__main__":
    app()
