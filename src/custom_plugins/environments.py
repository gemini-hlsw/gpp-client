__all__ = [
    "AVAILABILITY_DIRECTIVE",
    "USER_ENVIRONMENTS",
    "Selection",
    "environment_specific_selections",
    "environments",
]

from dataclasses import dataclass
from pathlib import Path

from ariadne_codegen.schema import load_graphql_files_from_path

from gpp_client.environment import GPPEnvironment
from graphql import (
    FieldNode,
    FragmentDefinitionNode,
    GraphQLSchema,
    ListValueNode,
    OperationDefinitionNode,
    StringValueNode,
    TypeInfo,
    TypeInfoVisitor,
    Visitor,
    parse,
    visit,
)

AVAILABILITY_DIRECTIVE = "environments"
"""Name of the merged-schema directive that lists a part's environments."""

USER_ENVIRONMENTS = tuple(env.label for env in GPPEnvironment)
"""Environments, in promotion order."""


def environments(ast_node) -> tuple[str, ...] | None:
    """
    Return the environments a merged-schema part's directive names.

    Parameters
    ----------
    ast_node : Node | None
        The part's definition in the merged schema.

    Returns
    -------
    tuple[str, ...] | None
        The environments that have the part, or ``None`` when it carries no
        directive, meaning every environment has it.
    """
    for directive in getattr(ast_node, "directives", None) or ():
        if directive.name.value != AVAILABILITY_DIRECTIVE:
            continue
        for argument in directive.arguments:
            if isinstance(argument.value, ListValueNode):
                return tuple(
                    value.value
                    for value in argument.value.values
                    if isinstance(value, StringValueNode)
                )
    return None


@dataclass(frozen=True)
class Selection:
    """
    A selected field that is on fewer environments than its parent type.

    Parameters
    ----------
    description : str
        ``Type.field in definition``.
    environments : tuple[str, ...]
        The environments that have the field.
    """

    description: str
    environments: tuple[str, ...]


def environment_specific_selections(
    schema: GraphQLSchema, queries_path: Path
) -> dict[int, Selection]:
    """
    Return each environment-specific field the operations select, by offset.

    Result-field plugin hooks get the field node but not its parent type; the
    queries ariadne-codegen loads parse to the same offsets, so a hook finds its
    field here by ``field.loc.start``.

    Parameters
    ----------
    schema : GraphQLSchema
        The merged schema.
    queries_path : Path
        The operations folder ariadne-codegen reads.

    Returns
    -------
    dict[int, Selection]
        Each selection whose field is on fewer environments than its parent
        type, keyed by the field node's source offset.
    """
    document = parse(load_graphql_files_from_path(queries_path))
    type_info = TypeInfo(schema)
    found: dict[int, Selection] = {}
    visit(document, TypeInfoVisitor(type_info, _Collector(type_info, found)))
    return found


class _Collector(Visitor):
    def __init__(self, type_info: TypeInfo, found: dict[int, Selection]) -> None:
        super().__init__()
        self.type_info = type_info
        self.found = found
        self.definition = ""

    def enter_operation_definition(self, node: OperationDefinitionNode, *_args):
        self.definition = node.name.value if node.name else "anonymous"

    def enter_fragment_definition(self, node: FragmentDefinitionNode, *_args):
        self.definition = node.name.value

    def enter_field(self, node: FieldNode, *_args) -> None:
        field = self.type_info.get_field_def()
        parent = self.type_info.get_parent_type()
        if field is None or parent is None or node.loc is None:
            return
        field_envs = environments(field.ast_node)
        if field_envs is not None and field_envs != environments(parent.ast_node):
            self.found[node.loc.start] = Selection(
                description=f"{parent.name}.{node.name.value} in {self.definition}",
                environments=field_envs,
            )
