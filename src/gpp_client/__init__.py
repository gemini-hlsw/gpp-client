"""
Top-level package for gpp_client.
"""

from typing import Any

__all__ = ["GPPClient"]


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
