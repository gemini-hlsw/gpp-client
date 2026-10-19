"""
Locate the generated package and the committed schemas.

The runtime reads trimmed operations from ``gpp_client.generated`` and each
environment's schema from ``gpp_client.schemas``. Tests build small clients
from fixture schemas into other packages, and point the runtime at them with
``use_generated_package``.
"""

__all__ = [
    "generated_package",
    "load_generated",
    "schemas_package",
    "use_generated_package",
]

import importlib
from collections.abc import Iterator
from contextlib import contextmanager
from types import ModuleType

_package = "gpp_client.generated"
_schemas = "gpp_client.schemas"


def generated_package() -> str:
    """
    Return the generated package the tables are read from.

    Returns
    -------
    str
        The package name, ``"gpp_client.generated"`` outside tests.
    """
    return _package


def schemas_package() -> str:
    """
    Return the package holding one ``<environment>.graphql`` per environment.

    Returns
    -------
    str
        The package name, ``"gpp_client.schemas"`` outside tests.
    """
    return _schemas


def load_generated(module: str) -> ModuleType:
    """
    Import a module of the generated package.

    Parameters
    ----------
    module : str
        The module path inside the package, such as ``"trimmed"``.

    Returns
    -------
    ModuleType
        The imported module.
    """
    return importlib.import_module(f"{_package}.{module}")


@contextmanager
def use_generated_package(package: str, schemas: str) -> Iterator[None]:
    """
    Read the tables and schemas from other packages while the block runs.

    Parameters
    ----------
    package : str
        An importable package written by the build.
    schemas : str
        An importable package holding the schemas that build read.

    Yields
    ------
    None
    """
    global _package, _schemas
    previous = _package, _schemas
    _package, _schemas = package, schemas
    try:
        yield
    finally:
        _package, _schemas = previous
