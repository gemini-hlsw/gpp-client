import asyncio
import inspect
import re
from functools import wraps
from typing import Callable, Optional

import typer

from ..client import GPPClient
from ..managers.base_manager import BaseManager


def clean_docstring(doc: Optional[str]) -> str:
    """Extract the first paragraph from a NumPy-style docstring.

    Parameters
    ----------
    doc : str, optional
        The full docstring.

    Returns
    -------
    str
        The summary paragraph only.
    """
    if not doc:
        return ""

    # Normalize indentation
    lines = doc.strip().splitlines()
    dedented = [line.strip() for line in lines]

    # Join and split again to normalize spacing
    full_text = " ".join(dedented)

    # Cut at first section header (e.g., "Parameters", "Returns", etc.)
    match = re.split(
        r"\b(?:Parameters|Returns|Raises|Examples|Notes|See Also)\b", full_text
    )
    return match[0].strip()

def format_name(name: str) -> str:
    return name.replace("_", "-")


def async_cli_method(
    app: typer.Typer,
    manager_class: BaseManager,
    manager_attr: str,
    method_name: str,
    handle_result: Optional[Callable[[dict], None]] = None,
):
    """Dynamically register an async manager method as a Typer CLI command.

    Parameters
    ----------
    app : typer.Typer
        The CLI app instance to register the command on.
    manager_class : BaseManager
        The class that defines the method, used to extract the signature.
    manager_attr : str
        Attribute on GPPClient to access the manager (e.g., 'call_for_proposals').
    method_name : str
        Name of the method to call on the manager.
    handle_result : Callable, optional
        Callback that receives the result for display/output.
    """
    method = getattr(manager_class, method_name)
    sig = inspect.signature(method)

    @wraps(method)
    def wrapper(**kwargs):
        client = GPPClient()
        bound_method = getattr(getattr(client, manager_attr), method_name)
        result = asyncio.run(bound_method(**kwargs))
        if handle_result:
            handle_result(result)
    
    wrapper.__signature__ = sig.replace(
        parameters=list(sig.parameters.values())[1:]
    )  # drop `self`
    wrapper.__doc__ = clean_docstring(method.__doc__)
    app.command(name=format_name(method_name))(wrapper)
