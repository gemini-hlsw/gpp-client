"""
Trim generated operations for one environment.

Each operation, as the generated client embeds it, loses the fields,
arguments, inline fragments and fragment spreads the environment lacks, and the
variables only those used.
"""

from collections.abc import Callable, Iterable
from copy import copy
from dataclasses import dataclass
from typing import TypeVar

from gpp_client.trimmed_operations import operation_digest
from graphql import (
    REMOVE,
    DocumentNode,
    FieldNode,
    FragmentDefinitionNode,
    FragmentSpreadNode,
    GraphQLSchema,
    InlineFragmentNode,
    NamedTypeNode,
    NameNode,
    Node,
    OperationDefinitionNode,
    SelectionSetNode,
    TypeInfo,
    TypeInfoVisitor,
    VariableNode,
    Visitor,
    parse,
    print_ast,
    validate,
    visit,
)

__all__ = ["EnvironmentOperations", "generated_operations", "trim_operations"]

_Node = TypeVar("_Node", bound=Node)


@dataclass(frozen=True)
class EnvironmentOperations:
    """
    Every generated operation as one environment receives it.

    Parameters
    ----------
    environment : str
        Environment name.
    operations : dict[str, tuple[str, str | None, tuple[str, ...]]]
        Per digest of each operation the environment receives differently from
        the generated string: the operation name, its trimmed text (``None``
        when unavailable) and the names of the fragments it uses.
    fragments : dict[str, str]
        Trimmed text of each fragment those operations use, stored once.
    errors : tuple[str, ...]
        Each way a trimmed operation is invalid on the environment.
    unavailable : tuple[str, ...]
        Operations the environment lacks a root field of, sorted.
    removed : dict[str, tuple[str, ...]]
        Per removed part (``Type.field``, ``Type.field(arg:)``, ``... on Type``
        or ``...Fragment``), the operations and fragments it was removed from.
    """

    environment: str
    operations: dict[str, tuple[str, str | None, tuple[str, ...]]]
    fragments: dict[str, str]
    errors: tuple[str, ...]
    unavailable: tuple[str, ...]
    removed: dict[str, tuple[str, ...]]


def trim_operations(
    environment: str, schema: GraphQLSchema, operation_strs: Iterable[str]
) -> EnvironmentOperations:
    """
    Trim each generated operation for one environment.

    Parameters
    ----------
    environment : str
        Environment name.
    schema : GraphQLSchema
        The environment's schema.
    operation_strs : Iterable[str]
        Each operation with its fragments, as the generated client embeds it.

    Returns
    -------
    EnvironmentOperations
        The trimmed operations.
    """
    trimmer = _EnvironmentTrimmer(schema)
    operations: dict[str, tuple[str, str | None, tuple[str, ...]]] = {}
    errors: list[str] = []
    unavailable: list[str] = []
    stored_fragments: set[str] = set()
    for operation_str in operation_strs:
        document = parse(operation_str)
        sources = {
            d.name.value: d
            for d in document.definitions
            if isinstance(d, FragmentDefinitionNode)
        }
        operation = next(
            d for d in document.definitions if isinstance(d, OperationDefinitionNode)
        )
        digest = operation_digest(operation_str)
        if _missing_root_fields(operation, schema):
            operations[digest] = (operation.name.value, None, ())
            unavailable.append(operation.name.value)
            continue
        trimmed = trimmer.trim(operation, sources)
        fragment_names = trimmer.reachable_fragments(trimmed, sources)
        used = _variables_used(
            [trimmed.selection_set]
            + [trimmer.fragments[name] for name in fragment_names]
        )
        trimmed = _copy(
            trimmed,
            variable_definitions=tuple(
                definition
                for definition in trimmed.variable_definitions or ()
                if definition.variable.name.value in used
            ),
        )
        text = print_ast(trimmed)
        assembled = "\n\n".join(
            [text, *(print_ast(trimmer.fragments[n]) for n in fragment_names)]
        )
        if operation_digest(assembled) != digest:
            operations[digest] = (operation.name.value, text, fragment_names)
            stored_fragments.update(fragment_names)
        sent = DocumentNode(
            definitions=(trimmed, *(trimmer.fragments[n] for n in fragment_names))
        )
        errors += [
            f"{operation.name.value} on {environment}: {error.message}"
            for error in validate(schema, sent)
        ]
    return EnvironmentOperations(
        environment=environment,
        operations=operations,
        fragments={
            name: print_ast(trimmer.fragments[name])
            for name in sorted(stored_fragments)
        },
        errors=tuple(errors),
        unavailable=tuple(sorted(unavailable)),
        removed={
            part: tuple(sorted(definitions))
            for part, definitions in sorted(trimmer.removed.items())
        },
    )


def generated_operations(operation_strs: Iterable[str]) -> dict[str, str]:
    """
    Return the name of every generated operation by digest.

    Parameters
    ----------
    operation_strs : Iterable[str]
        Each operation with its fragments, as the generated client embeds it.

    Returns
    -------
    dict[str, str]
        Operation names keyed by ``operation_digest``, sorted by name.
    """
    names = {
        operation_digest(operation_str): next(
            d.name.value
            for d in parse(operation_str).definitions
            if isinstance(d, OperationDefinitionNode)
        )
        for operation_str in operation_strs
    }
    return dict(sorted(names.items(), key=lambda item: (item[1], item[0])))


class _EnvironmentTrimmer:
    def __init__(self, schema: GraphQLSchema) -> None:
        self.schema = schema
        self.fragments: dict[str, FragmentDefinitionNode | None] = {}
        """Each fragment trimmed once; ``None`` when its type is missing."""
        self.removed: dict[str, set[str]] = {}

    def trim(
        self,
        node: OperationDefinitionNode | FragmentDefinitionNode,
        sources: dict[str, FragmentDefinitionNode],
    ):
        type_info = TypeInfo(self.schema)

        def record(part: str) -> None:
            self.removed.setdefault(part, set()).add(node.name.value)

        return visit(
            node,
            TypeInfoVisitor(
                type_info, _Trimmer(type_info, self.schema, sources, record)
            ),
        )

    def fragment(
        self, name: str, sources: dict[str, FragmentDefinitionNode]
    ) -> FragmentDefinitionNode | None:
        if name not in self.fragments:
            source = sources[name]
            exists = source.type_condition.name.value in self.schema.type_map
            self.fragments[name] = self.trim(source, sources) if exists else None
        return self.fragments[name]

    def reachable_fragments(
        self, node: Node, sources: dict[str, FragmentDefinitionNode]
    ) -> tuple[str, ...]:
        reached: set[str] = set()
        pending = _spread_names(node)
        while pending:
            name = pending.pop()
            if name in reached:
                continue
            reached.add(name)
            fragment = self.fragment(name, sources)
            if fragment is not None:
                pending |= _spread_names(fragment)
        return tuple(sorted(reached))


class _Trimmer(Visitor):
    def __init__(
        self,
        type_info: TypeInfo,
        schema: GraphQLSchema,
        sources: dict[str, FragmentDefinitionNode],
        record: Callable[[str], None],
    ) -> None:
        super().__init__()
        self.type_info = type_info
        self.schema = schema
        self.sources = sources
        self.record = record

    def enter_field(self, node: FieldNode, *_args):
        name = node.name.value
        if name == "__typename":
            return None
        parent = self.type_info.get_parent_type()
        coordinate = f"{parent.name}.{name}"
        if name not in parent.fields:
            self.record(coordinate)
            return REMOVE
        arguments = parent.fields[name].args
        kept = tuple(a for a in node.arguments or () if a.name.value in arguments)
        if len(kept) == len(node.arguments or ()):
            return None
        for argument in node.arguments:
            if argument.name.value not in arguments:
                self.record(f"{coordinate}({argument.name.value}:)")
        return _copy(node, arguments=kept)

    def enter_inline_fragment(self, node: InlineFragmentNode, *_args):
        if node.type_condition and not self._has_type(node.type_condition):
            self.record(f"... on {node.type_condition.name.value}")
            return REMOVE
        return None

    def enter_fragment_spread(self, node: FragmentSpreadNode, *_args):
        if not self._has_type(self.sources[node.name.value].type_condition):
            self.record(f"...{node.name.value}")
            return REMOVE
        return None

    def leave_selection_set(self, node: SelectionSetNode, *_args):
        if node.selections:
            return None
        # Keeps the parent's generated model valid when every child is gone.
        return SelectionSetNode(
            selections=(
                FieldNode(
                    name=NameNode(value="__typename"), arguments=(), directives=()
                ),
            )
        )

    def _has_type(self, named: NamedTypeNode) -> bool:
        return named.name.value in self.schema.type_map


def _missing_root_fields(
    operation: OperationDefinitionNode, schema: GraphQLSchema
) -> list[str]:
    root = schema.get_root_type(operation.operation)
    names = [
        selection.name.value
        for selection in operation.selection_set.selections
        if isinstance(selection, FieldNode) and selection.name.value != "__typename"
    ]
    return [name for name in names if root is None or name not in root.fields]


def _variables_used(nodes: Iterable[Node]) -> set[str]:
    used: set[str] = set()

    class _Collector(Visitor):
        def enter_variable(self, variable: VariableNode, *_args) -> None:
            used.add(variable.name.value)

    for node in nodes:
        visit(node, _Collector())
    return used


def _spread_names(node: Node) -> set[str]:
    names: set[str] = set()

    class _Collector(Visitor):
        def enter_fragment_spread(self, spread: FragmentSpreadNode, *_args) -> None:
            names.add(spread.name.value)

    visit(node, _Collector())
    return names


def _copy(node: _Node, **changes) -> _Node:
    copied = copy(node)
    for key, value in changes.items():
        setattr(copied, key, value)
    return copied
