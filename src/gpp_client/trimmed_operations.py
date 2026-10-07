"""
Find the copy of a generated operation trimmed for one environment.

``gpp_client.generated.trimmed`` lists every generated operation in
``GENERATED``. ``gpp_client.generated.trimmed.<environment>`` stores a copy only
for an operation the environment receives differently: trimmed, or unavailable.
An operation is found by a digest of the query the generated client sends, so a
query-builder call that reuses a generated operation's name is never mistaken
for it.
"""

__all__ = [
    "TrimmedOperation",
    "find_trimmed_operation",
    "lookup_trimmed_operation",
    "operation_digest",
]

import hashlib
from dataclasses import dataclass

from gpp_client.environment import GPPEnvironment
from gpp_client.generated_tables import load_generated


@dataclass(frozen=True)
class TrimmedOperation:
    """
    One operation as an environment receives it.

    Attributes
    ----------
    name : str
        The operation name.
    document : str | None
        The query to send: the trimmed copy, or the generated query unchanged
        when the environment needs no trimming. ``None`` when the environment
        lacks one of the operation's root fields.
    """

    name: str
    document: str | None


def operation_digest(query: str) -> str:
    """
    Return the digest that identifies a generated operation.

    Parameters
    ----------
    query : str
        The query text, as generated or as sent.

    Returns
    -------
    str
        A hex digest that ignores differences in whitespace.

    Notes
    -----
    The generated client re-indents each operation inside its source, so only
    the whitespace-normalized text matches what the build saw.
    """
    return hashlib.sha256(" ".join(query.split()).encode("utf-8")).hexdigest()


def find_trimmed_operation(
    environment: GPPEnvironment, query: str
) -> TrimmedOperation | None:
    """
    Return the copy of a generated operation trimmed for an environment.

    Parameters
    ----------
    environment : GPPEnvironment
        The environment the query goes to.
    query : str
        The query the generated client is about to send.

    Returns
    -------
    TrimmedOperation | None
        The operation as the environment receives it, or ``None`` when
        ``query`` is not a generated operation, such as a query-builder call.
    """
    tables = load_generated("trimmed")
    environment_tables = load_generated(f"trimmed.{environment.label}")
    return lookup_trimmed_operation(
        tables.GENERATED,
        environment_tables.OPERATIONS,
        environment_tables.FRAGMENTS,
        query,
    )


def lookup_trimmed_operation(
    generated: dict[str, str],
    operations: dict[str, tuple[str, str | None, tuple[str, ...]]],
    fragments: dict[str, str],
    query: str,
) -> TrimmedOperation | None:
    """
    Return an operation as one environment receives it, from its stored tables.

    Parameters
    ----------
    generated : dict[str, str]
        Name of every generated operation, by digest.
    operations : dict[str, tuple[str, str | None, tuple[str, ...]]]
        The environment's stored copies by digest: name, trimmed text (``None``
        when unavailable) and the fragments it uses.
    fragments : dict[str, str]
        The environment's trimmed fragments by name.
    query : str
        The query the generated client is about to send.

    Returns
    -------
    TrimmedOperation | None
        The operation as the environment receives it, or ``None`` when
        ``query`` is not a generated operation.
    """
    digest = operation_digest(query)
    entry = operations.get(digest)
    if entry is None:
        name = generated.get(digest)
        return None if name is None else TrimmedOperation(name=name, document=query)
    name, operation, fragment_names = entry
    if operation is None:
        return TrimmedOperation(name=name, document=None)
    parts = [operation, *(fragments[fragment] for fragment in fragment_names)]
    return TrimmedOperation(name=name, document="\n\n".join(parts))
