#!/usr/bin/env python3
"""
Run Ariadne code generation for a specific GPP environment.
"""

import shutil
import subprocess
import tomllib
from dataclasses import dataclass
from pathlib import Path
from typing import Annotated, Any

import typer

from gpp_client.cli import output
from gpp_client.environment import GPPEnvironment
from graphql import DocumentNode, FragmentDefinitionNode, OperationDefinitionNode, parse

app = typer.Typer(
    help="Run the code generator for a given GPP environment.",
    add_completion=False,
)


class CodegenError(RuntimeError):
    """
    Raised when codegen preparation or execution fails.
    """


@dataclass(frozen=True)
class CodegenPaths:
    """
    Repository paths used by the codegen workflow.

    Parameters
    ----------
    root : Path
        Repository root directory.
    """

    root: Path

    @property
    def graphql_dir(self) -> Path:
        """
        Return the GraphQL root directory.

        Returns
        -------
        Path
            GraphQL root directory.
        """
        return self.root / "graphql"

    @property
    def codegen_dir(self) -> Path:
        """
        Return the codegen config directory.

        Returns
        -------
        Path
            Codegen config directory.
        """
        return self.graphql_dir / "codegen"

    @property
    def operations_dir(self) -> Path:
        """
        Return the GraphQL operations directory.

        Returns
        -------
        Path
            Operations directory.
        """
        return self.graphql_dir / "operations"

    @property
    def shared_operations_dir(self) -> Path:
        """
        Return the shared operations directory.

        Returns
        -------
        Path
            Shared operations directory.
        """
        return self.operations_dir / "shared"

    @property
    def development_only_path(self) -> Path:
        """
        Return the development-only GraphQL file path.

        Returns
        -------
        Path
            Development-only GraphQL file path.
        """
        return self.operations_dir / "development_only.graphql"

    @property
    def build_dir(self) -> Path:
        """
        Return the build directory root.

        Returns
        -------
        Path
            Build directory root.
        """
        return self.root / "build"

    def codegen_toml_path(self, env: GPPEnvironment) -> Path:
        """
        Return the codegen TOML path for an environment.

        Parameters
        ----------
        env : GPPEnvironment
            Target environment.

        Returns
        -------
        Path
            Codegen TOML path.
        """
        return self.codegen_dir / f"{env.value.lower()}.toml"

    def build_operations_dir(self, env: GPPEnvironment) -> Path:
        """
        Return the assembled operations directory for an environment.

        Parameters
        ----------
        env : GPPEnvironment
            Target environment.

        Returns
        -------
        Path
            Assembled operations directory.
        """
        return self.build_dir / "graphql" / env.value.lower()


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
    with toml_path.open("rb") as f:
        return tomllib.load(f)


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
    CodegenError
        Raised if the required settings block is missing.
    """
    try:
        return config["tool"]["ariadne-codegen"]
    except KeyError as exc:
        raise CodegenError(
            "Missing [tool.ariadne-codegen] section in codegen config."
        ) from exc


def _get_target_package_dir(
    *,
    repo_root: Path,
    codegen_settings: dict[str, Any],
) -> Path:
    """
    Resolve the generated package directory from codegen settings.

    Parameters
    ----------
    repo_root : Path
        Repository root directory.
    codegen_settings : dict[str, Any]
        Ariadne codegen settings.

    Returns
    -------
    Path
        Absolute path to the generated package directory.

    Raises
    ------
    CodegenError
        Raised if required package path settings are missing.
    """
    target_package_path = codegen_settings.get("target_package_path")
    target_package_name = codegen_settings.get("target_package_name")

    if not target_package_path:
        raise CodegenError("Missing 'target_package_path' in codegen config.")

    if not target_package_name:
        raise CodegenError("Missing 'target_package_name' in codegen config.")

    return (repo_root / target_package_path / target_package_name).resolve()


def _write_package_environment(package_dir: Path, env: GPPEnvironment) -> None:
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
    CodegenError
        Raised if the target package directory does not exist.
    """
    if not package_dir.exists():
        raise CodegenError(f"Generated package directory not found at {package_dir}")

    module_path = package_dir / "package_environment.py"
    module_contents = f'''"""
Package-level environment constant for generated client code.
"""

PACKAGE_ENVIRONMENT = "{env.value}"
'''
    module_path.write_text(module_contents, encoding="utf-8")
    output.info(f"Wrote package environment module to {module_path}")


def _file_has_content(path: Path) -> bool:
    """
    Return whether a file exists and contains non-whitespace content.

    Parameters
    ----------
    path : Path
        Path to the file.

    Returns
    -------
    bool
        True if the file exists and contains non-whitespace content.
    """
    return path.exists() and bool(path.read_text(encoding="utf-8").strip())


def _iter_graphql_files(root_dir: Path) -> list[Path]:
    """
    Return all GraphQL files under a directory.

    Parameters
    ----------
    root_dir : Path
        Root directory to search.

    Returns
    -------
    list[Path]
        Sorted list of GraphQL files.
    """
    if not root_dir.exists():
        return []

    return sorted(
        path
        for pattern in ("*.graphql", "*.gql")
        for path in root_dir.rglob(pattern)
        if path.is_file()
    )


def _parse_graphql_file(path: Path) -> DocumentNode:
    """
    Parse a GraphQL document file.

    Parameters
    ----------
    path : Path
        Path to the GraphQL file.

    Returns
    -------
    DocumentNode
        Parsed GraphQL document AST.

    Raises
    ------
    CodegenError
        Raised if the file cannot be parsed.
    """
    try:
        return parse(path.read_text(encoding="utf-8"))
    except Exception as exc:
        raise CodegenError(f"Failed to parse GraphQL file: {path}\n{exc}") from exc


def _collect_definition_names(file_paths: list[Path]) -> dict[str, Path]:
    """
    Collect named GraphQL operations and fragments from files.

    Parameters
    ----------
    file_paths : list[Path]
        GraphQL files to inspect.

    Returns
    -------
    dict[str, Path]
        Mapping of definition name to defining file.

    Raises
    ------
    CodegenError
        Raised if duplicate names are found within the given files.
    """
    names_to_paths: dict[str, Path] = {}

    for file_path in file_paths:
        document = _parse_graphql_file(file_path)

        for definition in document.definitions:
            definition_name: str | None = None

            if isinstance(definition, OperationDefinitionNode) and definition.name:
                definition_name = definition.name.value
            elif isinstance(definition, FragmentDefinitionNode):
                definition_name = definition.name.value

            if not definition_name:
                continue

            if definition_name in names_to_paths:
                raise CodegenError(
                    "Duplicate GraphQL definition name found:\n"
                    f"  Name: {definition_name}\n"
                    f"  First file: {names_to_paths[definition_name]}\n"
                    f"  Second file: {file_path}"
                )

            names_to_paths[definition_name] = file_path

    return names_to_paths


def _validate_development_only_is_additive(paths: CodegenPaths) -> None:
    """
    Ensure development-only GraphQL definitions do not collide with shared ones.

    Parameters
    ----------
    paths : CodegenPaths
        Repository path configuration.

    Raises
    ------
    CodegenError
        Raised if development-only definitions reuse names from shared.
    """
    # Skip validation if the development-only file is missing or empty.
    if not _file_has_content(paths.development_only_path):
        return

    shared_definitions = _collect_definition_names(
        _iter_graphql_files(paths.shared_operations_dir)
    )
    dev_definitions = _collect_definition_names([paths.development_only_path])

    collisions = {
        name: (shared_definitions[name], dev_path)
        for name, dev_path in dev_definitions.items()
        if name in shared_definitions
    }

    if not collisions:
        return

    lines = ["Development-only GraphQL must be additive. Name collisions found:"]
    for name, (shared_path, dev_path) in sorted(collisions.items()):
        lines.append(f"  {name}")
        lines.append(f"    shared: {shared_path}")
        lines.append(f"    dev:    {dev_path}")

    raise CodegenError("\n".join(lines))


def _assemble_operations(paths: CodegenPaths, env: GPPEnvironment) -> Path:
    """
    Assemble the effective GraphQL operations tree for an environment.

    Parameters
    ----------
    paths : CodegenPaths
        Repository path configuration.
    env : GPPEnvironment
        Environment to assemble operations for.

    Returns
    -------
    Path
        Path to the assembled operations directory.

    Raises
    ------
    CodegenError
        Raised if the shared operations directory is missing.
    """
    assembled_dir = paths.build_operations_dir(env)

    assembled_dir.mkdir(parents=True, exist_ok=True)

    if not paths.shared_operations_dir.exists():
        raise CodegenError(
            f"Shared operations directory not found at {paths.shared_operations_dir}"
        )

    # Copy the shared operations.
    for item in paths.shared_operations_dir.iterdir():
        destination_item = assembled_dir / item.name

        if item.is_dir():
            shutil.copytree(item, destination_item, dirs_exist_ok=True)
        else:
            destination_item.parent.mkdir(parents=True, exist_ok=True)
            shutil.copy2(item, destination_item)

    # Copy the development-only file.
    if env is GPPEnvironment.DEVELOPMENT and _file_has_content(
        paths.development_only_path
    ):
        shutil.copy2(
            paths.development_only_path,
            assembled_dir / paths.development_only_path.name,
        )

    output.info(f"Assembled operations into {assembled_dir}")
    return assembled_dir


def _remove_dir(path: Path, *, label: str) -> None:
    """
    Remove a directory if it exists, with output.

    Parameters
    ----------
    path : Path
        Directory path to remove.
    label : str
        Label for output messages.
    """
    if path.is_dir():
        shutil.rmtree(path)
        output.info(f"Removed {label} at {path}")


def _run_codegen(toml_path: Path) -> None:
    """
    Run Ariadne codegen with a specific TOML config.

    Parameters
    ----------
    toml_path : Path
        Path to the codegen TOML file.

    Raises
    ------
    CodegenError
        Raised if Ariadne codegen fails.
    """
    with output.status("Running codegen..."):
        try:
            process = subprocess.run(
                ["ariadne-codegen", "--config", str(toml_path)],
                check=True,
                capture_output=True,
                text=True,
            )
            if process.stdout:
                output.dim_info(process.stdout)
        except subprocess.CalledProcessError as exc:
            if exc.stdout:
                output.dim_info(exc.stdout)
            raise CodegenError(exc.stderr) from exc


def _run(env: GPPEnvironment) -> None:
    """
    Execute the full codegen workflow for an environment.

    Parameters
    ----------
    env : GPPEnvironment
        Target environment.
    """
    paths = CodegenPaths(root=Path.cwd())

    output.info(f"Running codegen for environment: {env.value}")

    toml_path = paths.codegen_toml_path(env)
    if not toml_path.exists():
        raise CodegenError(f"Codegen config file not found at {toml_path}")

    config = _load_codegen_config(toml_path)
    codegen_settings = _get_codegen_settings(config)
    package_dir = _get_target_package_dir(
        repo_root=paths.root,
        codegen_settings=codegen_settings,
    )

    if env is GPPEnvironment.DEVELOPMENT:
        _validate_development_only_is_additive(paths)

    _remove_dir(paths.build_dir, label="build directory")
    _assemble_operations(paths, env)
    _remove_dir(package_dir, label="generated package")
    _run_codegen(toml_path)
    _write_package_environment(package_dir, env)


@app.command()
def main(
    env: Annotated[
        GPPEnvironment,
        typer.Argument(help="Environment to run codegen for.", case_sensitive=False),
    ],
) -> None:
    """
    Run code generation for a specific GPP environment.
    """
    try:
        _run(env)
    except CodegenError as exc:
        output.fail(str(exc))
        raise typer.Exit(code=1) from exc

    output.success("Codegen completed successfully")


if __name__ == "__main__":
    app()
