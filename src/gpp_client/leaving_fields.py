"""
Warn when a call selects a field development has already removed.
"""

__all__ = ["warn_leaving_field"]

import sys
import threading
import warnings

from gpp_client.environment import GPPEnvironment
from gpp_client.exceptions import GPPFieldLeavingWarning
from gpp_client.generated_tables import generated_package

_warned: set[tuple[str, str]] = set()
_lock = threading.Lock()


def warn_leaving_field(field: str, environment: GPPEnvironment) -> None:
    """
    Warn that a field is leaving, once per field per process.

    Parameters
    ----------
    field : str
        The field's schema coordinate (``Type.field``).
    environment : GPPEnvironment
        The selected environment, which still has the field.
    """
    key = (generated_package(), field)
    with _lock:
        if key in _warned:
            return
        _warned.add(key)
    warnings.warn(
        GPPFieldLeavingWarning(field, environment),
        stacklevel=_first_caller_outside(("gpp_client.", f"{generated_package()}.")),
    )


def _first_caller_outside(prefixes: tuple[str, ...]) -> int:
    # Python 3.11 lacks warnings' skip_file_prefixes, and the call depth varies
    # by path (HTTP, websocket, query builder), so walk to the user's frame.
    frame = sys._getframe(1)
    level = 1
    while frame is not None and frame.f_globals.get("__name__", "").startswith(
        prefixes
    ):
        frame = frame.f_back
        level += 1
    return level
