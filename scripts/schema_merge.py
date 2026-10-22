"""
Merge the development and production schemas into one that records availability.

A coordinate names one schema element: ``Type.field``, ``Type.field(arg:)``
or ``Input.field``. Production wins a conflict because a release must stay
exact against production. Development's names win a rename because
development changes first and is where most work happens.

Three steps. First, pairing: a production type is renamed to development's
name when a shared coordinate carries, on each side, a type of the same kind
and list depth under a name the other side lacks (``pair_types``). Then the
union: every type, field, argument, input field and enum value that is not on
both environments carries ``@environments(names: [...])``. Then production
wins each remaining conflict. Type rules:

1. Output nullability differs: nullable.
2. Input field or argument nullability differs: optional.
3. Present on one environment only, or on fewer than its parent: nullable
   (output) or optional (input).
4. Type differs by named type or list nesting, or is a kind conflict:
   production's type, marked production-only, reported as a ``TypeConflict``.
5. Type kind differs: production's definition, marked production-only;
   development-only elements typed by that name are dropped and reported as a
   ``KindConflict``.

Descriptions, defaults and other directives come from development where it
has the element, from production otherwise. The merge never fails on a
difference; only an invalid schema raises ``SchemaMergeError``.
"""

from collections import Counter
from collections.abc import Iterable, Mapping
from copy import copy
from dataclasses import dataclass, field
from typing import TypeVar

from custom_plugins.environments import AVAILABILITY_DIRECTIVE
from gpp_client.environment import GPPEnvironment
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
    Visitor,
    build_ast_schema,
    parse,
    print_ast,
    visit,
)

__all__ = [
    "DEVELOPMENT",
    "PRODUCTION",
    "MergedSchema",
    "Pairing",
    "Rename",
    "KindConflict",
    "SchemaMergeError",
    "TypeConflict",
    "merge_schemas",
    "pair_types",
    "rename_named_types",
]

DEVELOPMENT = GPPEnvironment.DEVELOPMENT.label
PRODUCTION = GPPEnvironment.PRODUCTION.label

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
class Rename:
    """
    A production type paired with the development type that replaced it.

    Parameters
    ----------
    production : str
        The type's name on production.
    development : str
        The type's name on development, which the merged schema uses.
    coordinates : tuple[str, ...]
        The coordinates that carry the type on both environments.
    kind : str
        The kind of type, as ``KindConflict`` names it: ``"union"``,
        ``"interface"`` and so on.
    """

    production: str
    development: str
    coordinates: tuple[str, ...]
    kind: str


@dataclass(frozen=True)
class Pairing:
    """
    The renames found between production's and development's type names.

    Parameters
    ----------
    renames : tuple[Rename, ...]
        Each production type renamed to its development name.
    ambiguous : tuple[str, ...]
        Production types whose coordinates voted for different development
        names, so no rename was made; one line each.
    collisions : tuple[str, ...]
        Production types that voted for a development name another rename
        already took, so no rename was made; one line each.
    """

    renames: tuple[Rename, ...] = ()
    ambiguous: tuple[str, ...] = ()
    collisions: tuple[str, ...] = ()

    @property
    def by_production_name(self) -> dict[str, str]:
        """
        Return each rename as production name to development name.

        Returns
        -------
        dict[str, str]
            Development name per renamed production name.
        """
        return {rename.production: rename.development for rename in self.renames}

    @property
    def reverse(self) -> dict[str, str]:
        """
        Return each rename as development name to production name.

        Returns
        -------
        dict[str, str]
            Production name per development name the merged schema uses.
        """
        return {rename.development: rename.production for rename in self.renames}


@dataclass(frozen=True)
class KindConflict:
    """
    A type name that means a different kind of type on each environment.

    Parameters
    ----------
    name : str
        The type name.
    kinds : tuple[tuple[str, str], ...]
        Each environment with the kind the name has there.
    dropped : tuple[str, ...]
        Development-only elements typed by the name and left out, sorted:
        ``Type.field``, ``Type.field(arg:)``, ``Input.field``,
        ``Union = Member`` or ``Type implements Interface``.
    """

    name: str
    kinds: tuple[tuple[str, str], ...]
    dropped: tuple[str, ...]


@dataclass(frozen=True)
class MergedSchema:
    """
    The result of merging environment schemas.

    Parameters
    ----------
    document : DocumentNode
        The merged schema, including the availability directive definition.
    pairing : Pairing
        The production types renamed to their development names first.
    conflicts : tuple[TypeConflict, ...]
        Elements given production's type because theirs differs.
    kind_conflicts : tuple[KindConflict, ...]
        Type names that production's definition won, with what was dropped.
    """

    document: DocumentNode
    pairing: Pairing = field(default_factory=Pairing)
    conflicts: tuple[TypeConflict, ...] = ()
    kind_conflicts: tuple[KindConflict, ...] = ()

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


def merge_schemas(*, development: str, production: str) -> MergedSchema:
    """
    Pair renamed types, then merge the two environment schemas.

    Parameters
    ----------
    development : str
        Development's schema as SDL.
    production : str
        Production's schema as SDL.

    Returns
    -------
    MergedSchema
        The merged schema, the pairing and the conflicts.

    Raises
    ------
    SchemaMergeError
        Raised when an environment schema is invalid or the merged schema is.
    """
    development_doc = _parse_schema(DEVELOPMENT, development)
    production_doc = _parse_schema(PRODUCTION, production)
    pairing = pair_types(production_doc, development_doc)
    renamed = rename_named_types(production_doc, pairing.by_production_name)
    return _Merger(development_doc, renamed, pairing).merge()


def pair_types(production: DocumentNode, development: DocumentNode) -> Pairing:
    """
    Find production types that development renamed.

    A production type is renamed to a development type when a shared coordinate
    (same parent type and field, argument or input field name) carries the two
    names with the same kind and list depth, production's name is absent from
    development and development's name is absent from production. For example,
    production's ``Obs.window: TimeWindowProd`` and development's
    ``Obs.window: TimeWindow`` vote to rename ``TimeWindowProd`` to
    ``TimeWindow``. Each coordinate votes once; a type whose coordinates vote
    for different names, or two types voting for the same name, make no rename.
    Renames are applied one step at a time until none is found, and a renamed
    name never renames again.

    Only types are paired, never fields: a field renamed on one environment
    stays two fields in the merged schema, each on its own environment.

    Parameters
    ----------
    production : DocumentNode
        Production's schema.
    development : DocumentNode
        Development's schema.

    Returns
    -------
    Pairing
        The renames, and the votes that made none.
    """
    development_types = _type_definitions(development)
    renames: dict[str, Rename] = {}
    ambiguous: dict[str, None] = {}
    collisions: dict[str, None] = {}
    while True:
        production_types = _type_definitions(
            rename_named_types(
                production, {r.production: r.development for r in renames.values()}
            )
        )
        votes = _votes(production_types, development_types)
        taken = {rename.development for rename in renames.values()}
        wanted = Counter(
            next(iter(counter)) for counter in votes.values() if len(counter) == 1
        )
        found: list[Rename] = []
        for production_name, counter in sorted(votes.items()):
            if len(counter) > 1:
                by_votes = sorted(counter.items(), key=lambda item: -len(item[1]))
                listed = ", ".join(f"{name} ({len(c)})" for name, c in by_votes)
                ambiguous[f"{production_name}: {listed}"] = None
                continue
            ((development_name, coordinates),) = counter.items()
            if development_name in taken or wanted[development_name] > 1:
                collisions[f"{production_name} -> {development_name}"] = None
                continue
            found.append(
                Rename(
                    production_name,
                    development_name,
                    tuple(coordinates),
                    _KIND_NAMES[type(production_types[production_name])],
                )
            )
        if not found:
            break
        renames.update({rename.production: rename for rename in found})
    return Pairing(
        renames=tuple(renames.values()),
        ambiguous=tuple(ambiguous),
        collisions=tuple(collisions),
    )


def _votes(
    production_types: dict[str, TypeDefinitionNode],
    development_types: dict[str, TypeDefinitionNode],
) -> dict[str, dict[str, list[str]]]:
    """
    Collect, per production type name, the coordinates voting for each development name.
    """
    votes: dict[str, dict[str, list[str]]] = {}
    for name, production_node in production_types.items():
        development_node = development_types.get(name)
        if development_node is None or type(production_node) is not type(
            development_node
        ):
            continue
        for coordinate, production_type, development_type in _shared_type_refs(
            name, production_node, development_node
        ):
            production_name = _named(production_type)
            development_name = _named(development_type)
            if production_name == development_name or _list_depth(
                production_type
            ) != _list_depth(development_type):
                continue
            renamed = production_types.get(production_name)
            target = development_types.get(development_name)
            if renamed is None or target is None or type(renamed) is not type(target):
                continue
            if (
                production_name in development_types
                or development_name in production_types
            ):
                continue
            votes.setdefault(production_name, {}).setdefault(
                development_name, []
            ).append(coordinate)
    return votes


def _shared_type_refs(
    type_name: str, production: TypeDefinitionNode, development: TypeDefinitionNode
) -> Iterable[tuple[str, TypeNode, TypeNode]]:
    """
    Yield each coordinate on both environments with its type on each.
    """
    if not isinstance(
        production,
        (
            ObjectTypeDefinitionNode,
            InterfaceTypeDefinitionNode,
            InputObjectTypeDefinitionNode,
        ),
    ):
        return
    development_fields = {f.name.value: f for f in development.fields or ()}  # type: ignore[union-attr]
    for production_field in production.fields or ():
        development_field = development_fields.get(production_field.name.value)
        if development_field is None:
            continue
        coordinate = f"{type_name}.{production_field.name.value}"
        yield coordinate, production_field.type, development_field.type
        development_args = {
            a.name.value: a for a in getattr(development_field, "arguments", None) or ()
        }
        for argument in getattr(production_field, "arguments", None) or ():
            development_arg = development_args.get(argument.name.value)
            if development_arg is not None:
                yield (
                    f"{coordinate}({argument.name.value}:)",
                    argument.type,
                    development_arg.type,
                )


def rename_named_types(
    document: DocumentNode, mapping: Mapping[str, str]
) -> DocumentNode:
    """
    Return the document with every type name in ``mapping`` replaced.

    Both a type definition's own name and each reference to it are renamed, so
    the same call serves a schema and an operation document.

    Parameters
    ----------
    document : DocumentNode
        A schema or operation document.
    mapping : Mapping[str, str]
        Each name to replace, with its replacement.

    Returns
    -------
    DocumentNode
        The renamed document, or ``document`` itself when ``mapping`` is empty.
    """
    if not mapping:
        return document

    class _Renamer(Visitor):
        def enter_named_type(self, node: NamedTypeNode, *_args):
            new_name = mapping.get(node.name.value)
            return (
                None if new_name is None else _copy(node, name=NameNode(value=new_name))
            )

        def enter(self, node, *_args):
            if isinstance(node, TypeDefinitionNode):
                new_name = mapping.get(node.name.value)
                if new_name is not None:
                    return _copy(node, name=NameNode(value=new_name))
            return None

    return visit(document, _Renamer())


def _type_definitions(document: DocumentNode) -> dict[str, TypeDefinitionNode]:
    return {
        definition.name.value: definition
        for definition in document.definitions
        if isinstance(definition, TypeDefinitionNode)
    }


def _named(type_node: TypeNode) -> str:
    while not isinstance(type_node, NamedTypeNode):
        type_node = type_node.type
    return type_node.name.value


def _list_depth(type_node: TypeNode) -> int:
    depth = 0
    while not isinstance(type_node, NamedTypeNode):
        if isinstance(type_node, ListTypeNode):
            depth += 1
        type_node = type_node.type
    return depth


class _Merger:
    """
    Build the merged schema from development's and production's documents.

    ``dropped`` maps each type name whose kind differs between the
    environments, such as an enum on one and an object on the other, to the
    development-only elements left out because of it. Production's definition
    wins such a name, so the keys also serve as the set of kind conflicts.
    """

    def __init__(
        self, development: DocumentNode, production: DocumentNode, pairing: Pairing
    ) -> None:
        self.documents = {DEVELOPMENT: development, PRODUCTION: production}
        self.development = _type_definitions(development)
        self.production = _type_definitions(production)
        self.pairing = pairing
        self.conflicts: list[TypeConflict] = []
        self.dropped: dict[str, set[str]] = {
            name: set()
            for name in self.development
            if name in self.production
            and type(self.development[name]) is not type(self.production[name])
        }

    def merge(self) -> MergedSchema:
        definitions: list = [_DIRECTIVE_DEFINITION]
        definitions += self._merge_schema_definition()
        definitions += self._merge_directive_definitions()
        names = list(self.development) + [
            n for n in self.production if n not in self.development
        ]
        for name in names:
            development = self.development.get(name)
            if name in self.dropped:
                development = None
            definitions.append(
                self._merge_type(name, development, self.production.get(name))
            )

        document = DocumentNode(definitions=tuple(definitions))
        try:
            build_ast_schema(document)
        except (GraphQLError, TypeError) as exc:
            raise SchemaMergeError(f"Merged schema is invalid: {exc}") from exc
        return MergedSchema(
            document=document,
            pairing=self.pairing,
            conflicts=tuple(self.conflicts),
            kind_conflicts=tuple(
                KindConflict(
                    name=name,
                    kinds=(
                        (DEVELOPMENT, _KIND_NAMES[type(self.development[name])]),
                        (PRODUCTION, _KIND_NAMES[type(self.production[name])]),
                    ),
                    dropped=tuple(sorted(dropped)),
                )
                for name, dropped in self.dropped.items()
            ),
        )

    def _merge_schema_definition(self) -> list[SchemaDefinitionNode]:
        for document in self.documents.values():
            for definition in document.definitions:
                if isinstance(definition, SchemaDefinitionNode):
                    return [definition]
        return []

    def _merge_directive_definitions(self) -> list[DirectiveDefinitionNode]:
        merged: dict[str, DirectiveDefinitionNode] = {}
        for env, document in self.documents.items():
            for definition in document.definitions:
                if not isinstance(definition, DirectiveDefinitionNode):
                    continue
                if definition.name.value == AVAILABILITY_DIRECTIVE:
                    raise SchemaMergeError(
                        f"Schema of {env} already defines @{AVAILABILITY_DIRECTIVE}."
                    )
                merged.setdefault(definition.name.value, definition)
        return list(merged.values())

    def _merge_type(
        self,
        name: str,
        development: TypeDefinitionNode | None,
        production: TypeDefinitionNode | None,
    ) -> TypeDefinitionNode:
        envs = _envs(development, production)
        base = development if development is not None else production
        changes: dict = {"directives": self._directives(base, envs)}

        if isinstance(base, (ObjectTypeDefinitionNode, InterfaceTypeDefinitionNode)):
            changes["interfaces"] = self._merge_names(
                f"{name} implements", development, production, "interfaces"
            )
            changes["fields"] = self._merge_fields(name, development, production, envs)
        elif isinstance(base, InputObjectTypeDefinitionNode):
            changes["fields"] = self._merge_input_values(
                name,
                development.fields if development else None,  # type: ignore[union-attr]
                production.fields if production else None,  # type: ignore[union-attr]
                envs,
            )
        elif isinstance(base, EnumTypeDefinitionNode):
            changes["values"] = self._merge_enum_values(development, production)
        elif isinstance(base, UnionTypeDefinitionNode):
            changes["types"] = self._merge_names(
                f"{name} =", development, production, "types"
            )

        return _copy(base, **changes)

    def _merge_names(
        self,
        owner: str,
        development: TypeDefinitionNode | None,
        production: TypeDefinitionNode | None,
        attribute: str,
    ) -> tuple[NamedTypeNode, ...]:
        """
        Union of the named types two definitions list, development's first.

        A development-only member whose name is a kind conflict is dropped.
        """
        production_names = {
            n.name.value for n in getattr(production, attribute, None) or ()
        }
        seen: dict[str, NamedTypeNode] = {}
        for node in (development, production):
            for named in getattr(node, attribute, None) or ():
                member = named.name.value
                if member in self.dropped and member not in production_names:
                    self.dropped[member].add(f"{owner} {member}")
                    continue
                seen.setdefault(member, named)
        return tuple(seen.values())

    def _merge_fields(
        self,
        type_name: str,
        development: TypeDefinitionNode | None,
        production: TypeDefinitionNode | None,
        parent_envs: tuple[str, ...],
    ) -> tuple[FieldDefinitionNode, ...]:
        merged = []
        for name, dev_field, prod_field in _paired(
            getattr(development, "fields", None), getattr(production, "fields", None)
        ):
            coordinate = f"{type_name}.{name}"
            if self._drops(coordinate, dev_field, prod_field):
                continue
            resolved = self._resolve(coordinate, dev_field, prod_field)
            # After a type conflict the field is production's alone, so
            # development's arguments go with the rest of its definition.
            arguments = self._merge_input_values(
                coordinate,
                dev_field.arguments if DEVELOPMENT in resolved.envs else None,
                prod_field.arguments if prod_field else None,
                resolved.envs,
                argument=True,
            )
            field_type = resolved.type
            # An environment that has the type but not the field returns no
            # value for it, so the merged field must accept null.
            if resolved.envs != parent_envs:
                field_type = _nullable(field_type)
            merged.append(
                _copy(
                    resolved.base,
                    type=field_type,
                    arguments=arguments,
                    directives=self._directives(resolved.base, resolved.envs),
                )
            )
        return tuple(merged)

    def _merge_input_values(
        self,
        owner: str,
        development: Iterable[InputValueDefinitionNode] | None,
        production: Iterable[InputValueDefinitionNode] | None,
        parent_envs: tuple[str, ...],
        *,
        argument: bool = False,
    ) -> tuple[InputValueDefinitionNode, ...]:
        merged = []
        for name, dev_value, prod_value in _paired(development, production):
            coordinate = f"{owner}({name}:)" if argument else f"{owner}.{name}"
            if self._drops(coordinate, dev_value, prod_value):
                continue
            resolved = self._resolve(coordinate, dev_value, prod_value)
            value_type = resolved.type
            if resolved.envs != parent_envs:
                value_type = _nullable(value_type)
            merged.append(
                _copy(
                    resolved.base,
                    type=value_type,
                    directives=self._directives(resolved.base, resolved.envs),
                )
            )
        return tuple(merged)

    def _merge_enum_values(
        self,
        development: TypeDefinitionNode | None,
        production: TypeDefinitionNode | None,
    ) -> tuple[EnumValueDefinitionNode, ...]:
        merged = []
        for _, dev_value, prod_value in _paired(
            getattr(development, "values", None), getattr(production, "values", None)
        ):
            base = dev_value if dev_value is not None else prod_value
            merged.append(
                _copy(
                    base,
                    directives=self._directives(base, _envs(dev_value, prod_value)),
                )
            )
        return tuple(merged)

    def _drops(self, coordinate: str, development, production) -> bool:
        """
        Record and drop a development-only element typed by a kind conflict.
        """
        if production is None and _named(development.type) in self.dropped:
            self.dropped[_named(development.type)].add(coordinate)
            return True
        return False

    def _resolve(self, coordinate: str, development, production) -> "_Resolved":
        """
        Give an element its merged type, environments and the node to copy.

        A type that differs by more than nullability, or whose named type is a
        kind conflict, is a conflict: production's type, on production only,
        with development's description.
        """
        if development is None:
            return _Resolved(production.type, (PRODUCTION,), production)
        if production is None:
            return _Resolved(development.type, (DEVELOPMENT,), development)
        if (
            _shape(development.type) != _shape(production.type)
            or _named(production.type) in self.dropped
        ):
            self.conflicts.append(
                TypeConflict(
                    coordinate=coordinate,
                    types=(
                        (DEVELOPMENT, print_ast(development.type)),
                        (PRODUCTION, print_ast(production.type)),
                    ),
                )
            )
            base = _copy(
                production,
                description=development.description or production.description,
            )
            return _Resolved(production.type, (PRODUCTION,), base)
        return _Resolved(
            _least_strict([development.type, production.type]),
            (DEVELOPMENT, PRODUCTION),
            development,
        )

    def _directives(
        self,
        node: TypeDefinitionNode
        | FieldDefinitionNode
        | InputValueDefinitionNode
        | EnumValueDefinitionNode,
        envs: tuple[str, ...],
    ) -> tuple[DirectiveNode, ...]:
        directives = tuple(node.directives or ())
        if envs == (DEVELOPMENT, PRODUCTION):
            return directives
        return directives + (_availability(envs),)


@dataclass(frozen=True)
class _Resolved:
    type: TypeNode
    envs: tuple[str, ...]
    base: FieldDefinitionNode | InputValueDefinitionNode


def _envs(development, production) -> tuple[str, ...]:
    return tuple(
        env
        for env, node in ((DEVELOPMENT, development), (PRODUCTION, production))
        if node is not None
    )


def _paired(
    development: Iterable[_Node] | None, production: Iterable[_Node] | None
) -> list[tuple[str, _Node | None, _Node | None]]:
    """
    Pair named nodes by name, development's order first, then production-only.
    """
    dev_by_name = {n.name.value: n for n in development or ()}  # type: ignore[attr-defined]
    prod_by_name = {n.name.value: n for n in production or ()}  # type: ignore[attr-defined]
    names = list(dev_by_name) + [n for n in prod_by_name if n not in dev_by_name]
    return [(name, dev_by_name.get(name), prod_by_name.get(name)) for name in names]


def _parse_schema(env: str, sdl: str) -> DocumentNode:
    try:
        document = parse(sdl)
        build_ast_schema(document)
    except (GraphQLError, TypeError) as exc:
        raise SchemaMergeError(f"Schema of {env} is invalid: {exc}") from exc
    return document


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
