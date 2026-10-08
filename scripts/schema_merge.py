"""
Merge each environment's GraphQL schema into one schema that records availability.

Every type, field, argument, input field and enum value that is not on every
environment carries ``@environments(names: [...])``. Conflict rules:

1. Output nullability differs: nullable.
2. Input field or argument nullability differs: optional.
3. Present on only some of the environments that have its parent: nullable
   (output) or optional (input).
4. Type differs (named type or list nesting): left out and reported as a
   ``TypeConflict``; an argument that differs leaves out its field.
5. Type kind differs: ``SchemaMergeError``.

Descriptions, defaults and other directives come from the first environment in
the given order that has the element, so callers pass the newest environment
first.
"""

from collections.abc import Iterable, Mapping
from copy import copy
from dataclasses import dataclass
from typing import TypeVar

from custom_plugins.environments import AVAILABILITY_DIRECTIVE
from graphql import (
    ArgumentNode,
    DirectiveDefinitionNode,
    DirectiveNode,
    DocumentNode,
    EnumTypeDefinitionNode,
    EnumValueDefinitionNode,
    FieldDefinitionNode,
    GraphQLError,
    InputObjectTypeDefinitionNode,
    InputValueDefinitionNode,
    InterfaceTypeDefinitionNode,
    ListTypeNode,
    ListValueNode,
    NamedTypeNode,
    NameNode,
    NonNullTypeNode,
    ObjectTypeDefinitionNode,
    ScalarTypeDefinitionNode,
    SchemaDefinitionNode,
    StringValueNode,
    TypeDefinitionNode,
    TypeNode,
    UnionTypeDefinitionNode,
    build_ast_schema,
    parse,
    print_ast,
)

__all__ = [
    "MergedSchema",
    "SchemaMergeError",
    "TypeConflict",
    "merge_schemas",
]

_DIRECTIVE_DEFINITION = parse(
    f"directive @{AVAILABILITY_DIRECTIVE}(names: [String!]!) on "
    "OBJECT | INTERFACE | UNION | ENUM | INPUT_OBJECT | SCALAR | FIELD_DEFINITION "
    "| ARGUMENT_DEFINITION | INPUT_FIELD_DEFINITION | ENUM_VALUE"
).definitions[0]

_KIND_NAMES: dict[type, str] = {
    ObjectTypeDefinitionNode: "object",
    InterfaceTypeDefinitionNode: "interface",
    UnionTypeDefinitionNode: "union",
    EnumTypeDefinitionNode: "enum",
    InputObjectTypeDefinitionNode: "input object",
    ScalarTypeDefinitionNode: "scalar",
}

_Node = TypeVar("_Node")


class SchemaMergeError(RuntimeError):
    """
    Raised when the environment schemas cannot be merged.
    """


@dataclass(frozen=True)
class TypeConflict:
    """
    A schema element whose type differs between environments.

    Parameters
    ----------
    coordinate : str
        Schema coordinate, such as ``Type.field`` or ``Type.field(arg:)``.
    types : tuple[tuple[str, str], ...]
        Each environment that has the element, with its type there.
    """

    coordinate: str
    types: tuple[tuple[str, str], ...]


@dataclass(frozen=True)
class MergedSchema:
    """
    The result of merging environment schemas.

    Parameters
    ----------
    document : DocumentNode
        The merged schema, including the availability directive definition.
    conflicts : tuple[TypeConflict, ...]
        Elements left out because their type differs between environments.
    """

    document: DocumentNode
    conflicts: tuple[TypeConflict, ...]

    @property
    def sdl(self) -> str:
        """
        Return the merged schema as SDL text.

        Returns
        -------
        str
            The printed schema, ending with a newline.
        """
        return print_ast(self.document) + "\n"


def merge_schemas(sdl_by_environment: Mapping[str, str]) -> MergedSchema:
    """
    Merge environment schemas, newest environment first.

    Parameters
    ----------
    sdl_by_environment : Mapping[str, str]
        Schema SDL per environment name, in promotion order from newest to
        oldest (development, then production).

    Returns
    -------
    MergedSchema
        The merged schema and the elements left out by rule 4.

    Raises
    ------
    SchemaMergeError
        Raised when an environment schema is invalid, a type has a different
        kind on two environments, or the merged schema is invalid.
    """
    return _Merger(sdl_by_environment).merge()


class _Merger:
    def __init__(self, sdl_by_environment: Mapping[str, str]) -> None:
        self.environments = tuple(sdl_by_environment)
        self.documents = {
            env: _parse_schema(env, sdl) for env, sdl in sdl_by_environment.items()
        }
        self.conflicts: list[TypeConflict] = []

    def merge(self) -> MergedSchema:
        definitions: list = [_DIRECTIVE_DEFINITION]
        definitions += self._merge_schema_definition()
        definitions += self._merge_directive_definitions()
        for name, by_env in _ordered_union(
            {env: self._type_definitions(env) for env in self.environments}
        ):
            self._check_kind(name, by_env)
            definitions.append(self._merge_type(by_env))

        document = DocumentNode(definitions=tuple(definitions))
        try:
            build_ast_schema(document)
        except (GraphQLError, TypeError) as exc:
            raise SchemaMergeError(f"Merged schema is invalid: {exc}") from exc
        return MergedSchema(document=document, conflicts=tuple(self.conflicts))

    def _type_definitions(self, env: str) -> list[tuple[str, TypeDefinitionNode]]:
        return [
            (definition.name.value, definition)
            for definition in self.documents[env].definitions
            if isinstance(definition, TypeDefinitionNode)
        ]

    def _merge_schema_definition(self) -> list[SchemaDefinitionNode]:
        for env in self.environments:
            for definition in self.documents[env].definitions:
                if isinstance(definition, SchemaDefinitionNode):
                    return [definition]
        return []

    def _merge_directive_definitions(self) -> list[DirectiveDefinitionNode]:
        merged = []
        for name, by_env in _ordered_union(
            {
                env: [
                    (definition.name.value, definition)
                    for definition in self.documents[env].definitions
                    if isinstance(definition, DirectiveDefinitionNode)
                ]
                for env in self.environments
            }
        ):
            if name == AVAILABILITY_DIRECTIVE:
                raise SchemaMergeError(
                    f"Schema of {', '.join(by_env)} already defines "
                    f"@{AVAILABILITY_DIRECTIVE}."
                )
            merged.append(next(iter(by_env.values())))
        return merged

    def _check_kind(self, name: str, by_env: Mapping[str, TypeDefinitionNode]) -> None:
        kinds = {env: _KIND_NAMES[type(node)] for env, node in by_env.items()}
        if len(set(kinds.values())) > 1:
            listed = ", ".join(f"{kind} on {env}" for env, kind in kinds.items())
            raise SchemaMergeError(
                f"Type '{name}' has a different kind on two environments: {listed}."
            )

    def _merge_type(
        self, by_env: Mapping[str, TypeDefinitionNode]
    ) -> TypeDefinitionNode:
        newest = next(iter(by_env.values()))
        envs = tuple(by_env)
        type_name = newest.name.value
        changes: dict = {"directives": self._directives(newest, envs)}

        if isinstance(newest, (ObjectTypeDefinitionNode, InterfaceTypeDefinitionNode)):
            changes["interfaces"] = _merge_names(n.interfaces for n in by_env.values())
            changes["fields"] = self._merge_fields(type_name, by_env, envs)
        elif isinstance(newest, InputObjectTypeDefinitionNode):
            changes["fields"] = self._merge_input_values(
                type_name, {env: n.fields for env, n in by_env.items()}, envs
            )
        elif isinstance(newest, EnumTypeDefinitionNode):
            changes["values"] = self._merge_enum_values(by_env)
        elif isinstance(newest, UnionTypeDefinitionNode):
            changes["types"] = _merge_names(n.types for n in by_env.values())

        return _copy(newest, **changes)

    def _merge_fields(
        self,
        type_name: str,
        by_env: Mapping[str, ObjectTypeDefinitionNode | InterfaceTypeDefinitionNode],
        parent_envs: tuple[str, ...],
    ) -> tuple[FieldDefinitionNode, ...]:
        merged = []
        for name, fields in _ordered_union(
            {
                env: [(f.name.value, f) for f in node.fields or ()]
                for env, node in by_env.items()
            }
        ):
            coordinate = f"{type_name}.{name}"
            envs = tuple(fields)
            field_type = self._merge_type_ref(
                coordinate, {env: f.type for env, f in fields.items()}
            )
            arguments = self._merge_input_values(
                coordinate,
                {env: f.arguments for env, f in fields.items()},
                envs,
                argument=True,
            )
            if field_type is None or arguments is None:
                continue
            if envs != parent_envs:
                field_type = _nullable(field_type)
            newest = next(iter(fields.values()))
            merged.append(
                _copy(
                    newest,
                    type=field_type,
                    arguments=arguments,
                    directives=self._directives(newest, envs),
                )
            )
        return tuple(merged)

    def _merge_input_values(
        self,
        owner: str,
        by_env: Mapping[str, Iterable[InputValueDefinitionNode] | None],
        parent_envs: tuple[str, ...],
        *,
        argument: bool = False,
    ) -> tuple[InputValueDefinitionNode, ...] | None:
        """
        Merge input fields or arguments; ``None`` means an argument conflicts.
        """
        merged = []
        for name, values in _ordered_union(
            {
                env: [(v.name.value, v) for v in nodes or ()]
                for env, nodes in by_env.items()
            }
        ):
            coordinate = f"{owner}({name}:)" if argument else f"{owner}.{name}"
            envs = tuple(values)
            value_type = self._merge_type_ref(
                coordinate, {env: v.type for env, v in values.items()}
            )
            if value_type is None:
                if argument:
                    return None
                continue
            if envs != parent_envs:
                value_type = _nullable(value_type)
            newest = next(iter(values.values()))
            merged.append(
                _copy(
                    newest,
                    type=value_type,
                    directives=self._directives(newest, envs),
                )
            )
        return tuple(merged)

    def _merge_enum_values(
        self, by_env: Mapping[str, EnumTypeDefinitionNode]
    ) -> tuple[EnumValueDefinitionNode, ...]:
        merged = []
        for _, values in _ordered_union(
            {
                env: [(v.name.value, v) for v in node.values or ()]
                for env, node in by_env.items()
            }
        ):
            newest = next(iter(values.values()))
            merged.append(
                _copy(newest, directives=self._directives(newest, tuple(values)))
            )
        return tuple(merged)

    def _merge_type_ref(
        self, coordinate: str, by_env: Mapping[str, TypeNode]
    ) -> TypeNode | None:
        """
        Merge a type reference by rules 1 and 2; ``None`` on a rule 4 conflict.
        """
        shapes = {_shape(type_node) for type_node in by_env.values()}
        if len(shapes) > 1:
            self.conflicts.append(
                TypeConflict(
                    coordinate=coordinate,
                    types=tuple(
                        (env, print_ast(type_node)) for env, type_node in by_env.items()
                    ),
                )
            )
            return None
        return _least_strict(list(by_env.values()))

    def _directives(
        self,
        node: TypeDefinitionNode
        | FieldDefinitionNode
        | InputValueDefinitionNode
        | EnumValueDefinitionNode,
        envs: tuple[str, ...],
    ) -> tuple[DirectiveNode, ...]:
        directives = tuple(node.directives or ())
        if envs == self.environments:
            return directives
        names = tuple(env for env in self.environments if env in envs)
        return directives + (_availability(names),)


def _parse_schema(env: str, sdl: str) -> DocumentNode:
    try:
        document = parse(sdl)
        build_ast_schema(document)
    except (GraphQLError, TypeError) as exc:
        raise SchemaMergeError(f"Schema of {env} is invalid: {exc}") from exc
    return document


def _ordered_union(
    items_by_env: Mapping[str, Iterable[tuple[str, _Node]]],
) -> list[tuple[str, dict[str, _Node]]]:
    """
    Group named items across environments, in first-seen order.
    """
    grouped: dict[str, dict[str, _Node]] = {}
    for env, items in items_by_env.items():
        for name, item in items:
            grouped.setdefault(name, {})[env] = item
    return list(grouped.items())


def _merge_names(
    names_per_env: Iterable[Iterable[NamedTypeNode] | None],
) -> tuple[NamedTypeNode, ...]:
    seen: dict[str, NamedTypeNode] = {}
    for names in names_per_env:
        for named in names or ():
            seen.setdefault(named.name.value, named)
    return tuple(seen.values())


def _shape(type_node: TypeNode) -> str:
    if isinstance(type_node, NonNullTypeNode):
        return _shape(type_node.type)
    if isinstance(type_node, ListTypeNode):
        return f"[{_shape(type_node.type)}]"
    return type_node.name.value


def _least_strict(type_nodes: list[TypeNode]) -> TypeNode:
    """
    Return the shared type, non-null at a level only if every input is.
    """
    all_non_null = all(isinstance(t, NonNullTypeNode) for t in type_nodes)
    inner = [t.type if isinstance(t, NonNullTypeNode) else t for t in type_nodes]
    if isinstance(inner[0], ListTypeNode):
        merged: TypeNode = ListTypeNode(
            type=_least_strict([t.type for t in inner])  # type: ignore[attr-defined]
        )
    else:
        merged = NamedTypeNode(name=NameNode(value=inner[0].name.value))  # type: ignore[attr-defined]
    return NonNullTypeNode(type=merged) if all_non_null else merged


def _nullable(type_node: TypeNode) -> TypeNode:
    return type_node.type if isinstance(type_node, NonNullTypeNode) else type_node


def _availability(names: tuple[str, ...]) -> DirectiveNode:
    return DirectiveNode(
        name=NameNode(value=AVAILABILITY_DIRECTIVE),
        arguments=(
            ArgumentNode(
                name=NameNode(value="names"),
                value=ListValueNode(
                    values=tuple(StringValueNode(value=name) for name in names)
                ),
            ),
        ),
    )


def _copy(node: _Node, **changes) -> _Node:
    copied = copy(node)
    for key, value in changes.items():
        setattr(copied, key, value)
    return copied
