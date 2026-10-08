"""
Build a small client from fixture schemas with the real build.

Runtime tests use it so they never depend on what is environment-specific in
the committed schemas, which changes whenever GPP promotes something.
"""

import importlib
import sys
import uuid
from collections.abc import Iterator
from contextlib import contextmanager
from dataclasses import dataclass
from functools import cached_property
from pathlib import Path
from types import ModuleType

from gpp_client.generated_tables import use_generated_package
from gpp_client.graphql_client import EnvironmentGraphQLClient
from scripts.build_client import BuildPaths, build

REPO_ROOT = Path(__file__).resolve().parents[2]


@dataclass
class FixtureBuild:
    """
    A generated package built from fixture schemas.

    Parameters
    ----------
    package : str
        The importable package name.
    packages_dir : Path
        The folder holding the package.
    """

    package: str
    packages_dir: Path

    def module(self, name: str) -> ModuleType:
        """
        Import a module of the package.
        """
        sys.path.insert(0, str(self.packages_dir))
        try:
            return importlib.import_module(f"{self.package}.{name}")
        finally:
            sys.path.remove(str(self.packages_dir))

    @cached_property
    def client_class(self) -> type:
        """
        The package's generated client with the environment behavior.
        """
        generated = self.module("client").GraphQLClient
        return type("Client", (EnvironmentGraphQLClient, generated), {})

    @contextmanager
    def tables(self) -> Iterator["FixtureBuild"]:
        """
        Read the runtime's generated tables from this package while active.
        """
        with use_generated_package(self.package):
            yield self


def build_fixture(root: Path, schemas: dict[str, str], operations: str) -> FixtureBuild:
    """
    Build a package from one schema per environment and an operations file.

    Parameters
    ----------
    root : Path
        An empty folder to build in.
    schemas : dict[str, str]
        SDL by environment name; both are required.
    operations : str
        The operations, as one ``.graphql`` file.

    Returns
    -------
    FixtureBuild
        The built package.
    """
    schemas_dir = root / "schemas"
    schemas_dir.mkdir()
    for environment, sdl in schemas.items():
        (schemas_dir / f"{environment}.graphql").write_text(sdl)
    operations_dir = root / "operations"
    operations_dir.mkdir()
    (operations_dir / "operations.graphql").write_text(operations)
    package = f"generated_{uuid.uuid4().hex[:12]}"
    build(
        BuildPaths(
            schemas_dir=schemas_dir,
            operations_dir=operations_dir,
            package_dir=root / "packages" / package,
            codegen_config=REPO_ROOT / "graphql" / "codegen.toml",
        )
    )
    return FixtureBuild(package=package, packages_dir=root / "packages")
