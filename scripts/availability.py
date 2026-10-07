"""
Collect what differs between environments, from the merged schema, for llms.txt.

The tables hold each argument, input field and enum value with its
availability, each input field that only some environments require, and per
operation the fields it selects that development lacks but a later environment
has.
"""

from collections.abc import Iterable, Mapping
from dataclasses import dataclass

from graphql.language import Node

from custom_plugins.environments import environments
from graphql import (
    DocumentNode,
    GraphQLSchema,
    OperationDefinitionNode,
    TypeInfo,
    TypeInfoVisitor,
    Undefined,
    Visitor,
    build_ast_schema,
    is_enum_type,
    is_input_object_type,
    is_interface_type,
    is_non_null_type,
    is_object_type,
    parse,
    visit,
)

__all__ = ["AvailabilityTables", "availability_tables"]


@dataclass(frozen=True)
class AvailabilityTables:
    """
    What differs between environments, for llms.txt.

    Parameters
    ----------
    available : dict[str, tuple[str, ...]]
        Environments that have each argument (``Type.field(arg:)``), input field
        (``Input.field``) and enum value (``Enum.VALUE``) not on every
        environment.
    required : dict[str, tuple[str, ...]]
        Environments that require each input field (``Input.field``) the
        merged schema makes optional.
    leaving : dict[str, dict[str, tuple[str, ...]]]
        Per operation, each field it selects (``Type.field``) that the first
        environment in promotion order lacks, with the environments that still
        have it. Promotion is linear, so these leave those environments next.
    """

    available: dict[str, tuple[str, ...]]
    required: dict[str, tuple[str, ...]]
    leaving: dict[str, dict[str, tuple[str, ...]]]


def availability_tables(
    merged: DocumentNode,
    environment_schemas: Mapping[str, GraphQLSchema],
    operation_strs: Iterable[str],
) -> AvailabilityTables:
    """
    Return what differs between environments.

    Parameters
    ----------
    merged : DocumentNode
        The merged schema, with its availability directives.
    environment_schemas : Mapping[str, GraphQLSchema]
        Each environment's schema, in promotion order.
    operation_strs : Iterable[str]
        Each operation with its fragments, as the generated client embeds it.

    Returns
    -------
    AvailabilityTables
        The tables, sorted so they diff stably.
    """
    schema = build_ast_schema(merged)
    leaving: dict[str, dict[str, tuple[str, ...]]] = {}
    first = next(iter(environment_schemas))
    for operation_str in operation_strs:
        name, fields = _leaving_fields(schema, operation_str, first)
        if fields:
            leaving[name] = fields
    return AvailabilityTables(
        available=dict(sorted(_available(schema).items())),
        required=dict(sorted(_required(schema, environment_schemas).items())),
        leaving=dict(sorted(leaving.items())),
    )


def _available(schema: GraphQLSchema) -> dict[str, tuple[str, ...]]:
    found: dict[str, tuple[str, ...]] = {}

    def record(coordinate: str, node: Node | None) -> None:
        names = environments(node)
        if names is not None:
            found[coordinate] = names

    for type_ in schema.type_map.values():
        if is_input_object_type(type_):
            for name, field in type_.fields.items():
                record(f"{type_.name}.{name}", field.ast_node)
        elif is_enum_type(type_):
            for name, value in type_.values.items():
                record(f"{type_.name}.{name}", value.ast_node)
        elif is_object_type(type_) or is_interface_type(type_):
            for field_name, field in type_.fields.items():
                for name, argument in field.args.items():
                    record(f"{type_.name}.{field_name}({name}:)", argument.ast_node)
    return found


def _required(
    merged: GraphQLSchema, environment_schemas: Mapping[str, GraphQLSchema]
) -> dict[str, tuple[str, ...]]:
    """
    Return each input field optional in the merged schema but required somewhere.

    Arguments are left out: an operation passing a nullable variable where an
    environment requires a value fails that environment's validation at build.
    """
    found: dict[str, tuple[str, ...]] = {}
    for type_ in merged.type_map.values():
        if not is_input_object_type(type_):
            continue
        for name, field in type_.fields.items():
            if _is_required(field):
                continue
            requiring = tuple(
                env
                for env, env_schema in environment_schemas.items()
                if is_input_object_type(env_type := env_schema.type_map.get(type_.name))
                and name in env_type.fields
                and _is_required(env_type.fields[name])
            )
            if requiring:
                found[f"{type_.name}.{name}"] = requiring
    return found


def _is_required(field) -> bool:
    return is_non_null_type(field.type) and field.default_value is Undefined


def _leaving_fields(
    schema: GraphQLSchema, operation_str: str, first: str
) -> tuple[str, dict[str, tuple[str, ...]]]:
    """
    Return the operation's name, and each field it selects that ``first`` lacks.
    """
    document = parse(operation_str)
    operation = next(
        d for d in document.definitions if isinstance(d, OperationDefinitionNode)
    )
    found: dict[str, tuple[str, ...]] = {}
    type_info = TypeInfo(schema)

    class _Fields(Visitor):
        def enter_field(self, node, *_args) -> None:
            field = type_info.get_field_def()
            parent = type_info.get_parent_type()
            names = environments(field.ast_node) if field else None
            if names and first not in names:
                found[f"{parent.name}.{node.name.value}"] = names

    visit(document, TypeInfoVisitor(type_info, _Fields()))
    return operation.name.value, dict(sorted(found.items()))
