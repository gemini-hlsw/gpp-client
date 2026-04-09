#!/usr/bin/env python3
"""
Runs the code generator on a specified GraphQL schema.
"""

import subprocess
from pathlib import Path
from typing import Annotated, Any

import toml
import typer

from gpp_client.cli import output
from gpp_client.environment import GPPEnvironment

app = typer.Typer(
    help="Run the code generator for a given GPP environment.",
    add_completion=False,
)


def _load_codegen_config(toml_path: Path) -> dict[str, Any]:
    """
    Load an ariadne-codegen TOML configuration file.

    Parameters
    ----------
    toml_path : Path
        Path to the TOML configuration file.

    Returns
    -------
    dict[str, Any]
        Parsed TOML configuration.
    """
    return toml.loads(toml_path.read_text(encoding="utf-8"))


def _get_codegen_settings(config: dict[str, Any]) -> dict[str, Any]:
    """
    Return the ``tool.ariadne-codegen`` settings block.

    Parameters
    ----------
    config : dict[str, Any]
        Parsed TOML configuration.

    Returns
    -------
    dict[str, Any]
        Ariadne codegen settings.

    Raises
    ------
    typer.Exit
        Raised if the required settings block is missing.
    """
    try:
        return config["tool"]["ariadne-codegen"]
    except KeyError:
        output.fail("Missing [tool.ariadne-codegen] section in codegen config.")
        raise typer.Exit(code=1) from None


def _get_target_package_dir(
    codegen_settings: dict[str, Any],
) -> Path:
    """
    Resolve the generated package directory from codegen settings.

    Parameters
    ----------
    toml_path : Path
        Path to the TOML configuration file.
    codegen_settings : dict[str, Any]
        Ariadne codegen settings.

    Returns
    -------
    Path
        Absolute path to the generated package directory.

    Raises
    ------
    typer.Exit
        Raised if required package path settings are missing.
    """
    target_package_path = codegen_settings.get("target_package_path")
    target_package_name = codegen_settings.get("target_package_name")

    if not target_package_path:
        output.fail("Missing 'target_package_path' in codegen config.")
        raise typer.Exit(code=1)

    if not target_package_name:
        output.fail("Missing 'target_package_name' in codegen config.")
        raise typer.Exit(code=1)

    project_root = Path.cwd()
    return (project_root / target_package_path / target_package_name).resolve()


def _write_package_environment(
    package_dir: Path,
    env: GPPEnvironment,
) -> None:
    """
    Write the package environment module into the generated package.

    Parameters
    ----------
    package_dir : Path
        Path to the generated package directory.
    env : GPPEnvironment
        Active package environment.

    Raises
    ------
    typer.Exit
        Raised if the target package directory does not exist.
    """
    if not package_dir.exists():
        output.fail(f"Generated package directory not found at {package_dir}")
        raise typer.Exit(code=1)

    module_path = package_dir / "package_environment.py"
    module_contents = f'''"""
Package-level environment constant for generated client code.
"""

PACKAGE_ENVIRONMENT = "{env.value}"
'''

    module_path.write_text(module_contents, encoding="utf-8")
    output.dim_info(f"Wrote package environment module to {module_path}")


@app.command()
def main(
    env: Annotated[
        GPPEnvironment,
        typer.Argument(help="Environment to run codegen for.", case_sensitive=False),
    ],
) -> None:
    """
    Run the codegen for a specific GPP environment.
    """
    output.info(f"Running codegen for environment: {env.value}")
    toml_path = Path("graphql") / env.value.lower() / "ariadne-codegen.toml"
    if not toml_path.exists():
        output.fail(f"Codegen config file not found at {toml_path}")
        raise typer.Exit(code=1)

    with output.status("Running codegen..."):
        try:
            process = subprocess.run(
                [
                    "ariadne-codegen",
                    "--config",
                    str(toml_path),
                ],
                check=True,
                capture_output=True,
                text=True,
            )
            output.dim_info(process.stdout)

        except subprocess.CalledProcessError as exc:
            output.fail(exc.stderr)
            raise typer.Exit(code=1) from exc

    config = _load_codegen_config(toml_path)
    codegen_settings = _get_codegen_settings(config)
    package_dir = _get_target_package_dir(codegen_settings)
    _write_package_environment(package_dir, env)

    output.success("Codegen completed successfully")


if __name__ == "__main__":
    app()
