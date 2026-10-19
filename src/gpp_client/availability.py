"""
Answer which environment has a generated model's field or an enum's value.

The build writes ``generated/availability.py`` from the merged schema: each
result-model field and each enum value that some environment lacks, with the
environments that have it. Anything not listed is on every environment. The
answers come from that table, so they need no network call.
"""

__all__ = ["enum_values", "is_available"]

from enum import Enum
from typing import TypeVar

from gpp_client.environment import GPPEnvironment
from gpp_client.generated_tables import load_generated

_EnumT = TypeVar("_EnumT", bound=Enum)


def is_available(
    model: object, field: str, environment: GPPEnvironment | str | None = None
) -> bool:
    """
    Return whether an environment has a generated model's field.

    A field the environment lacks reads ``None`` on a response from it; this
    tells that apart from a value GPP left null.

    Parameters
    ----------
    model : object
        A generated result model, as an instance or a class.
    field : str
        The field's attribute name on the model.
    environment : GPPEnvironment | str | None, optional
        The environment to answer for. If not provided, the environment a
        ``GPPClient`` built without one would use: ``GPP_ENVIRONMENT``, then
        the ``.env`` file, then production.

    Returns
    -------
    bool
        ``True`` when the environment has the field.

    Raises
    ------
    AttributeError
        If the model has no such field.
    """
    cls = model if isinstance(model, type) else type(model)
    if field not in getattr(cls, "model_fields", {}):
        raise AttributeError(f"{cls.__name__} has no field {field!r}")
    label = _environment(environment).label
    fields = load_generated("availability").FIELDS
    for base in cls.__mro__:
        environments = fields.get(base.__name__, {}).get(field)
        if environments is not None:
            return label in environments
    return True


def enum_values(
    enum: type[_EnumT], environment: GPPEnvironment | str | None = None
) -> list[_EnumT]:
    """
    Return the members of a generated enum that an environment accepts.

    A generated enum carries every environment's values; this gives the ones
    the environment's schema declares, for a dropdown or a check before
    sending.

    Parameters
    ----------
    enum : type[Enum]
        A generated enum.
    environment : GPPEnvironment | str | None, optional
        The environment to answer for. If not provided, the environment a
        ``GPPClient`` built without one would use: ``GPP_ENVIRONMENT``, then
        the ``.env`` file, then production.

    Returns
    -------
    list[Enum]
        The members the environment has, in declaration order.
    """
    label = _environment(environment).label
    values = load_generated("availability").ENUM_VALUES.get(enum.__name__, {})
    return [
        member
        for member in enum
        if member.value not in values or label in values[member.value]
    ]


def _environment(environment: GPPEnvironment | str | None) -> GPPEnvironment:
    if not environment:
        from gpp_client.settings import GPPSettings

        return GPPSettings().environment
    return GPPEnvironment(environment)
