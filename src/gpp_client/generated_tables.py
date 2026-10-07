"""
Load the tables the build writes into the generated package.

The runtime reads trimmed operations and bundled schemas from
``gpp_client.generated``. Tests build small clients from fixture schemas into
other packages, and read their tables with ``use_generated_package``.
"""

__all__ = ["generated_package", "load_generated", "use_generated_package"]

import importlib
from collections.abc import Iterator
from contextlib import contextmanager
from types import ModuleType

_package = "gpp_client.generated"


def generated_package() -> str:
    """
    Return the generated package the tables are read from.

    Returns
    -------
    str
        The package name, ``"gpp_client.generated"`` outside tests.
    """
    return _package


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
def use_generated_package(package: str) -> Iterator[None]:
    """
    Read the tables from another generated package while the block runs.

    Parameters
    ----------
    package : str
        An importable package written by the build.

    Yields
    ------
    None
    """
    global _package
    previous = _package
    _package = package
    try:
        yield
    finally:
        _package = previous
