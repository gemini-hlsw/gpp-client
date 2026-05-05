"""
Top-level package for gpp_client.
"""

import importlib.metadata
from typing import TYPE_CHECKING, Any

if TYPE_CHECKING:
    from .client import GPPClient

__all__ = ["GPPClient", "__version__"]

_FALLBACK_VERSION = "0.0.0"


try:
    __version__ = importlib.metadata.version(__name__)
except importlib.metadata.PackageNotFoundError:
    # Have fallback version for development environments.
    __version__ = _FALLBACK_VERSION


def __getattr__(name: str) -> Any:
    """
    Lazily import top-level package attributes.

    Parameters
    ----------
    name : str
        The attribute name being accessed.

    Returns
    -------
    Any
        The resolved attribute.

    Raises
    ------
    AttributeError
        If the attribute is not supported.
    """
    if name == "GPPClient":
        from .client import GPPClient

        return GPPClient

    raise AttributeError(f"module {__name__!r} has no attribute {name!r}")
