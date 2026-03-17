#!/usr/bin/env python3
"""
Download GraphQL schema for a specific GPP environment.
"""

import subprocess
import tempfile
from dataclasses import dataclass
from pathlib import Path
from typing import Annotated

import toml
import typer

from gpp_client.cli import output
from gpp_client.config import GPPDefaults, GPPEnvironment
from gpp_client.credentials import EnvVarReader

app = typer.Typer(
    help="Download the GraphQL schema for a given GPP environment.",
    add_completion=False,
)


@dataclass
class _Defaults:
    remote_schema_url: str
    remote_schema_headers: dict[str, str]
    output_dir: str = "schemas"
    introspection_descriptions: bool = True
    introspection_input_value_deprecation: bool = True
    introspection_specified_by_url: bool = True
    introspection_schema_description: bool = False
    introspection_directive_is_repeatable: bool = True
    introspection_input_object_one_of: bool = False

    # Codegen properties.
    remote_schema_verify_ssl: bool = True
    remote_schema_timeout: int = 10

    def get_target_file_path(self, env: GPPEnvironment) -> Path:
        """
        Get the target file path for the downloaded schema based on the environment.

        Parameters
        ----------
        env : GPPEnvironment
            The GPP environment for which the schema file path is being generated.

        Returns
        -------
        Path
            The path to the schema file for the given environment.
        """
        return Path(self.output_dir) / f"{env.value.lower()}.schema.graphql"

    def to_toml(self, env: GPPEnvironment) -> str:
        """
        Convert the configuration to a TOML string for use with ariadne-codegen.

        Parameters
        ----------
        env : GPPEnvironment
            The GPP environment for which the schema is being downloaded.

        Returns
        -------
        str
            The TOML configuration as a string.
        """
        return toml.dumps(
            {
                "tool": {
                    "ariadne-codegen": {
                        "target_file_path": str(self.get_target_file_path(env)),
                        "remote_schema_headers": self.remote_schema_headers,
                        "remote_schema_url": self.remote_schema_url,
                        "remote_schema_verify_ssl": self.remote_schema_verify_ssl,
                        "remote_schema_timeout": self.remote_schema_timeout,
                        "introspection_descriptions": self.introspection_descriptions,
                        "introspection_input_value_deprecation": self.introspection_input_value_deprecation,
                        "introspection_specified_by_url": self.introspection_specified_by_url,
                        "introspection_schema_description": self.introspection_schema_description,
                        "introspection_directive_is_repeatable": self.introspection_directive_is_repeatable,
                        "introspection_input_object_one_of": self.introspection_input_object_one_of,
                    }
                }
            }
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

    # Build the remote headers and other config values.
    remote_schema_headers = {"Authorization": f"Bearer {token}"}

    defaults = _Defaults(
        remote_schema_url=url,
        remote_schema_headers=remote_schema_headers,
        output_dir=str(output_dir),
    )

    with tempfile.TemporaryDirectory() as tmp:
        # Write the temporary TOML config file.
        config_path = Path(tmp) / "download_schema.toml"
        config_path.write_text(defaults.to_toml(env))
        output.info(f"Using temporary config file: {config_path}")

        try:
            process = subprocess.run(
                [
                    "ariadne-codegen",
                    "graphqlschema",
                    "--config",
                    str(config_path),
                ],
                check=True,
                capture_output=True,
                text=True,
            )
            output.info(process.stdout)
        except subprocess.CalledProcessError as exc:
            output.fail(exc.stderr)
            raise typer.Exit(code=1) from exc

        output.success(
            "Schema for environment development downloaded successfully "
            f"to {defaults.get_target_file_path(env)}"
        )


if __name__ == "__main__":
    app()
