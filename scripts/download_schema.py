#!/usr/bin/env python3
"""
Download the GraphQL schema for a specific GPP environment.
"""

import os
import subprocess
from dataclasses import dataclass
from pathlib import Path
from typing import Annotated

import typer

from gpp_client.cli import output
from gpp_client.constants import DEVELOPMENT_TOKEN_ENV_VAR, TOKEN_ENV_VAR
from gpp_client.environment import GPPEnvironment

app = typer.Typer(
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

    def schema_toml_path(self, env: GPPEnvironment) -> Path:
        """
        Return the schema TOML path for an environment.

        Parameters
        ----------
        env : GPPEnvironment
            Target environment.

        Returns
        -------
        Path
            Schema TOML path.
        """
        return self.schemas_dir / f"{env.value.lower()}.toml"


def _required_token_env_var(env: GPPEnvironment) -> str:
    """
    Return the required token environment variable.

    Parameters
    ----------
    env : GPPEnvironment
        Target environment.

    Returns
    -------
    str
        Required token environment variable.
    """
    if env is GPPEnvironment.DEVELOPMENT:
        return DEVELOPMENT_TOKEN_ENV_VAR

    return TOKEN_ENV_VAR


def _validate_token_env_var(env: GPPEnvironment) -> None:
    """
    Ensure the required token environment variable is set.

    Parameters
    ----------
    env : GPPEnvironment
        Target environment.

    Raises
    ------
    SchemaDownloadError
        Raised if the required token environment variable is not set.
    """
    env_var = _required_token_env_var(env)

    if not os.getenv(env_var):
        raise SchemaDownloadError(
            f"Required environment variable '{env_var}' is not set."
        )


def _run_schema_download(toml_path: Path) -> None:
    """
    Download a GraphQL schema using Ariadne Codegen.

    Parameters
    ----------
    toml_path : Path
        Path to the schema TOML configuration.

    Raises
    ------
    SchemaDownloadError
        Raised if Ariadne Codegen fails.
    """
    with output.status("Downloading schema..."):
        try:
            process = subprocess.run(
                [
                    "ariadne-codegen",
                    "graphqlschema",
                    "--config",
                    str(toml_path),
                ],
                check=True,
                capture_output=True,
                text=True,
                cwd=Path.cwd(),
            )

            if process.stdout:
                output.dim_info(process.stdout)

        except subprocess.CalledProcessError as exc:
            if exc.stdout:
                output.dim_info(exc.stdout)

            stderr = exc.stderr.strip() if exc.stderr else "Schema download failed."
            raise SchemaDownloadError(stderr) from exc


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

    toml_path = paths.schema_toml_path(env)

    if not toml_path.exists():
        raise SchemaDownloadError(f"Schema config file not found at {toml_path}")

    _validate_token_env_var(env)

    output.info(f"Using config: {toml_path}")

    _run_schema_download(toml_path)


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

    The following environment variables must be set:
    - DEVELOPMENT: GPP_DEVELOPMENT_TOKEN
    - PRODUCTION: GPP_TOKEN
    """
    try:
        _run(env)
    except SchemaDownloadError as exc:
        output.fail(str(exc))
        raise typer.Exit(code=1) from exc

    output.success("Schema download completed successfully")


if __name__ == "__main__":
    app()
