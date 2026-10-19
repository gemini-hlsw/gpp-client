__all__ = ["DEFAULTS_KEY", "DefaultsReport", "EnvironmentDefaultsPlugin"]

import ast
from dataclasses import dataclass, field
from pathlib import Path

from ariadne_codegen.plugins.base import Plugin

from custom_plugins.environments import environment_specific_selections
from graphql import (
    ExecutableDefinitionNode,
    FieldNode,
    GraphQLSchema,
    SelectionSetNode,
)

DEFAULTS_KEY = "environment_defaults"
"""Key under ``[tool.gpp-client]`` of the ``DefaultsReport`` the plugin fills."""


@dataclass
class DefaultsReport:
    """
    What the plugin expected to default to ``None`` and where it did.

    Parameters
    ----------
    expected : dict[int, str]
        Each environment-specific selection by source offset, described as
        ``Type.field in definition``.
    placed : list[tuple[int, str, str]]
        Each defaulted model field: source offset, class name, attribute name.
    """

    expected: dict[int, str] = field(default_factory=dict)
    placed: list[tuple[int, str, str]] = field(default_factory=list)


class EnvironmentDefaultsPlugin(Plugin):
    """
    Default to ``None`` the result fields that some environments lack.

    An environment that lacks a field never receives it, so the response has
    no key for it. Every other field stays required, so a key missing for any
    other reason is still an error.
    """

    def __init__(self, schema: GraphQLSchema, config_dict: dict) -> None:
        super().__init__(schema, config_dict)
        sink = config_dict.get("tool", {}).get("gpp-client", {}).get(DEFAULTS_KEY)
        self.report: DefaultsReport = sink if sink is not None else DefaultsReport()
        self._pending: dict[int, tuple[ast.AnnAssign, int]] = {}
        queries_path = config_dict["tool"]["ariadne-codegen"]["queries_path"]
        for offset, selection in environment_specific_selections(
            schema, Path(queries_path)
        ).items():
            self.report.expected[offset] = selection.description

    def generate_result_field(
        self,
        field_implementation: ast.AnnAssign,
        operation_definition: ExecutableDefinitionNode,
        field: FieldNode,
    ) -> ast.AnnAssign:
        """
        Add a ``None`` default to an environment-specific field.

        Parameters
        ----------
        field_implementation : ast.AnnAssign
            The generated model field.
        operation_definition : ExecutableDefinitionNode
            The operation or fragment the field belongs to.
        field : FieldNode
            The selected field.

        Returns
        -------
        ast.AnnAssign
            The model field, with ``None`` as its default when the field is on
            fewer environments than its parent type.
        """
        if field.loc is None or field.loc.start not in self.report.expected:
            return field_implementation
        value = field_implementation.value
        if value is None:
            field_implementation.value = ast.Constant(value=None)
        elif isinstance(value, ast.Call) and not any(
            keyword.arg == "default" for keyword in value.keywords
        ):
            value.keywords.append(
                ast.keyword(arg="default", value=ast.Constant(value=None))
            )
        self._pending[id(field_implementation)] = (
            field_implementation,
            field.loc.start,
        )
        return field_implementation

    def generate_result_class(
        self,
        class_def: ast.ClassDef,
        operation_definition: ExecutableDefinitionNode,
        selection_set: SelectionSetNode,
    ) -> ast.ClassDef:
        """
        Record which model fields received a ``None`` default.

        Parameters
        ----------
        class_def : ast.ClassDef
            The generated model class.
        operation_definition : ExecutableDefinitionNode
            The operation or fragment the class belongs to.
        selection_set : SelectionSetNode
            The selections the class models.

        Returns
        -------
        ast.ClassDef
            ``class_def``, unchanged.
        """
        for statement in class_def.body:
            pending = self._pending.get(id(statement))
            if pending is not None and isinstance(statement.target, ast.Name):
                self.report.placed.append(
                    (pending[1], class_def.name, statement.target.id)
                )
        return class_def
