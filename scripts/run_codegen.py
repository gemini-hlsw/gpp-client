#!/usr/bin/env python3
"""
Runs the code generator on a specified GraphQL schema.
"""

import shutil
import subprocess
import tempfile
from dataclasses import dataclass
from pathlib import Path
from typing import Annotated

import toml
import typer

from gpp_client.cli import output
from gpp_client.config import GPPEnvironment

app = typer.Typer(
    help="Run the code generator for a given GPP environment.",
    add_completion=False,
)


@dataclass
class _Defaults:
    """
    Configuration defaults for the code generator for a specific GPP environment.
    """

    # Settings for which environment to run codegen for.
    env: GPPEnvironment
    schema_dir: str = "schemas"

    # Codegen settings.
    target_package_path: str = "src/gpp_client"
    target_package_name: str = "api"
    client_name: str = "_GPPClient"
    client_file_name: str = "_client"
    queries_path: str = "src/queries"
    plugins: tuple[str] = ("custom_plugins.AliasStrWrapperPlugin",)
    enable_custom_operations: bool = True
    convert_to_snake_case: bool = True
    include_comments: str = "none"

    @property
    def schema(self) -> Path:
        return Path(self.schema_dir) / f"{self.env.value.lower()}.schema.graphql"

    @property
    def output_dir(self) -> Path:
        return Path(self.target_package_path) / self.target_package_name

    def to_toml(self) -> str:
        """
        Construct a TOML config for ariadne-codegen.

        Returns
        -------
        str
            The TOML configuration as a string.

        Notes
        -----
        There is a bug in ariadne-codegen that does not import custom scalars properly in files other than 'input_types.py'. Filing an issue there and hopefully this can be added in the future.

        # "scalars": {
        #     "Date": {"type": "datetime.date"},
        #     "NonNegInt": {"type": "pydantic.types.NonNegativeInt"},
        # },
        """
        return toml.dumps(
            {
                "tool": {
                    "ariadne-codegen": {
                        "schema_path": str(self.schema),
                        "queries_path": str(self.queries_path),
                        "target_package_path": str(self.target_package_path),
                        "target_package_name": self.target_package_name,
                        "client_name": self.client_name,
                        "client_file_name": self.client_file_name,
                        "plugins": list(self.plugins),
                        "enable_custom_operations": self.enable_custom_operations,
                        "convert_to_snake_case": self.convert_to_snake_case,
                        "include_comments": self.include_comments,
                    }
                }
            }
        )


@app.command()
def main(
    env: Annotated[
        GPPEnvironment,
        typer.Argument(help="Environment to run codegen for.", case_sensitive=False),
    ],
) -> None:
    """
    Run the codegen for a specific GPP environment.

    Parameters
    ----------
    env : GPPEnvironment
        The GPP environment to run codegen for.
    """
    output.info(f"Running codegen for environment: {env.value}")

    # Prepare the defaults.
    defaults = _Defaults(env=env)
    if defaults.schema and not defaults.schema.exists():
        output.fail(
            f"Schema file for environment {env.value} does not exist: {defaults.schema}"
        )
        raise typer.Exit(code=1)

    with tempfile.TemporaryDirectory() as tmp:
        # Write the temporary TOML config file.
        config_path = Path(tmp) / "codegen.toml"
        config_path.write_text(defaults.to_toml())
        output.info(f"Using temporary config file: {config_path}")

        # Create backup of existing generated files.
        api_dir = defaults.output_dir
        backup_dir = api_dir.with_name(f"{api_dir.name}_backup")

        # Remove stale backup first.
        if backup_dir.exists():
            shutil.rmtree(backup_dir)

        if api_dir.exists():
            output.info(f"Creating backup of existing generated client: {backup_dir}")
            api_dir.rename(backup_dir)

        with output.status("Running codegen..."):
            try:
                process = subprocess.run(
                    [
                        "ariadne-codegen",
                        "--config",
                        str(config_path),
                    ],
                    check=True,
                    capture_output=True,
                    text=True,
                )
                output.dim_info(process.stdout)
                # Codegen succeeded, remove backup.
                if backup_dir.exists():
                    shutil.rmtree(backup_dir)

            except subprocess.CalledProcessError as exc:
                # Remove partial generated files.
                output.warning("Codegen failed, restoring backup of existing client")
                if api_dir.exists():
                    shutil.rmtree(api_dir)

                # Restore backup.
                if backup_dir.exists():
                    backup_dir.rename(api_dir)

                output.fail(exc.stderr)
                raise typer.Exit(code=1) from exc

        output.success("Codegen completed successfully")


if __name__ == "__main__":
    app()
