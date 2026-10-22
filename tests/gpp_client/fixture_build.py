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

from gpp_client.generated import exceptions as generated_exceptions
from gpp_client.generated_tables import use_generated_package
from gpp_client.graphql_client import EnvironmentGraphQLClient
from scripts.run_codegen import BuildPaths, build

REPO_ROOT = Path(__file__).resolve().parents[2]


@dataclass
class FixtureBuild:
    """
    A generated package built from fixture schemas.

    Parameters
    ----------
    package : str
        The importable package name.
    schemas : str
        The importable package holding the fixture schemas.
    packages_dir : Path
        The folder holding both packages.
    """

    package: str
    schemas: str
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
        # The mixin catches the exceptions of the one generated package the
        # runtime has; a fixture package carries its own copies of them.
        base_client = self.module("async_base_client")
        for name, value in vars(generated_exceptions).items():
            if name.startswith("GraphQLClient") and hasattr(base_client, name):
                setattr(base_client, name, value)
        generated = self.module("client").GraphQLClient
        return type("Client", (EnvironmentGraphQLClient, generated), {})

    @contextmanager
    def tables(self) -> Iterator["FixtureBuild"]:
        """
        Read the runtime's generated tables from this build while active.
        """
        sys.path.insert(0, str(self.packages_dir))
        try:
            with use_generated_package(self.package):
                yield self
        finally:
            sys.path.remove(str(self.packages_dir))


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
    stem = uuid.uuid4().hex[:12]
    schemas_dir = root / "packages" / f"schemas_{stem}"
    schemas_dir.mkdir(parents=True)
    (schemas_dir / "__init__.py").write_text("")
    for environment, sdl in schemas.items():
        (schemas_dir / f"{environment}.graphql").write_text(sdl)
    operations_dir = root / "operations"
    operations_dir.mkdir()
    (operations_dir / "operations.graphql").write_text(operations)
    package = f"generated_{stem}"
    build(
        BuildPaths(
            schemas_dir=schemas_dir,
            operations_dir=operations_dir,
            package_dir=root / "packages" / package,
            codegen_config=REPO_ROOT / "graphql" / "codegen.toml",
        )
    )
    return FixtureBuild(
        package=package, schemas=schemas_dir.name, packages_dir=root / "packages"
    )
