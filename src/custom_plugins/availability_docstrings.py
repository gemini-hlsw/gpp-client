__all__ = ["AvailabilityDocstringsPlugin", "available_on"]

import ast
from pathlib import Path

from ariadne_codegen.plugins.base import Plugin

from custom_plugins.environments import (
    USER_ENVIRONMENTS,
    environment_specific_selections,
    environments,
)
from graphql import (
    ExecutableDefinitionNode,
    FieldNode,
    GraphQLEnumType,
    GraphQLInputField,
    GraphQLInputObjectType,
    GraphQLSchema,
    OperationDefinitionNode,
    OperationType,
    SelectionSetNode,
)


def available_on(names: tuple[str, ...] | None) -> str | None:
    """
    Return the availability line for a part, or ``None`` when it is everywhere.

    Parameters
    ----------
    names : tuple[str, ...] | None
        Environments that have the part, or ``None`` for every environment.

    Returns
    -------
    str | None
        ``"Available on: development."`` and the like; ``None`` when every
        environment has the part.
    """
    if names is None:
        return None
    offered = [env for env in USER_ENVIRONMENTS if env in names]
    if len(offered) == len(USER_ENVIRONMENTS):
        return None
    return f"Available on: {', '.join(offered)}."


class AvailabilityDocstringsPlugin(Plugin):
    """
    Add an ``Available on: ...`` docstring to environment-specific client
    methods, result fields, input types, input fields, enums and enum values.
    """

    def __init__(self, schema: GraphQLSchema, config_dict: dict) -> None:
        super().__init__(schema, config_dict)
        self._method_lines: dict[str, str] = {}
        self._field_lines: dict[int, str] = {}
        self._input_fields: dict[int, GraphQLInputField] = {}
        queries_path = config_dict["tool"]["ariadne-codegen"]["queries_path"]
        self._selections = environment_specific_selections(schema, Path(queries_path))

    def generate_client_method(
        self,
        method_def: ast.FunctionDef | ast.AsyncFunctionDef,
        operation_definition: OperationDefinitionNode,
    ) -> ast.FunctionDef | ast.AsyncFunctionDef:
        """
        Document where the method's operation works.

        Parameters
        ----------
        method_def : ast.FunctionDef | ast.AsyncFunctionDef
            The generated client method.
        operation_definition : OperationDefinitionNode
            The operation it sends.

        Returns
        -------
        ast.FunctionDef | ast.AsyncFunctionDef
            The method, with a docstring when its operation is not on every
            environment.
        """
        line = available_on(_operation_environments(self.schema, operation_definition))
        if line is not None:
            self._method_lines[method_def.name] = line
        return method_def

    def generate_client_module(self, module: ast.Module) -> ast.Module:
        """
        Put each recorded availability line first in its method.

        Runs after ``ClientForwardRefsPlugin``, which inserts an import at the
        top of every method, so the line stays the docstring.

        Parameters
        ----------
        module : ast.Module
            The generated client module.

        Returns
        -------
        ast.Module
            The module, with the availability docstrings added.
        """
        for node in ast.walk(module):
            if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef)):
                line = self._method_lines.get(node.name)
                if line is not None:
                    node.body.insert(0, _docstring_expr(line))
        return module

    def generate_result_field(
        self,
        field_implementation: ast.AnnAssign,
        operation_definition: ExecutableDefinitionNode,
        field: FieldNode,
    ) -> ast.AnnAssign:
        """
        Record the availability line of an environment-specific result field.

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
            ``field_implementation``, unchanged.
        """
        selection = self._selections.get(field.loc.start) if field.loc else None
        line = available_on(selection.environments) if selection else None
        if line is not None:
            self._field_lines[id(field_implementation)] = line
        return field_implementation

    def generate_result_class(
        self,
        class_def: ast.ClassDef,
        operation_definition: ExecutableDefinitionNode,
        selection_set: SelectionSetNode,
    ) -> ast.ClassDef:
        """
        Put each recorded availability line after its field.

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
            The class, with an attribute docstring after each
            environment-specific field.
        """
        _add_attribute_docstrings(class_def, self._field_lines)
        return class_def

    def generate_input_field(
        self,
        field_implementation: ast.AnnAssign,
        input_field: GraphQLInputField,
        field_name: str,
    ) -> ast.AnnAssign:
        """
        Remember which schema input field a model field implements.

        Parameters
        ----------
        field_implementation : ast.AnnAssign
            The generated input model field.
        input_field : GraphQLInputField
            The schema input field.
        field_name : str
            The input field's GraphQL name.

        Returns
        -------
        ast.AnnAssign
            ``field_implementation``, unchanged.
        """
        self._input_fields[id(field_implementation)] = input_field
        return field_implementation

    def generate_input_class(
        self, class_def: ast.ClassDef, input_type: GraphQLInputObjectType
    ) -> ast.ClassDef:
        """
        Document each input field on fewer environments than its input type.

        Parameters
        ----------
        class_def : ast.ClassDef
            The generated input model.
        input_type : GraphQLInputObjectType
            The schema input type.

        Returns
        -------
        ast.ClassDef
            The class, with an attribute docstring after each
            environment-specific field.
        """
        parent = environments(input_type.ast_node)
        _add_class_docstring(class_def, available_on(parent))
        lines = {}
        for statement in class_def.body:
            input_field = self._input_fields.get(id(statement))
            if input_field is None:
                continue
            names = environments(input_field.ast_node)
            line = available_on(names) if names != parent else None
            if line is not None:
                lines[id(statement)] = line
        _add_attribute_docstrings(class_def, lines)
        return class_def

    def generate_enum(
        self, class_def: ast.ClassDef, enum_type: GraphQLEnumType
    ) -> ast.ClassDef:
        """
        Document each enum value on fewer environments than its enum.

        Parameters
        ----------
        class_def : ast.ClassDef
            The generated enum.
        enum_type : GraphQLEnumType
            The schema enum.

        Returns
        -------
        ast.ClassDef
            The enum, with an attribute docstring after each
            environment-specific member.
        """
        parent = environments(enum_type.ast_node)
        _add_class_docstring(class_def, available_on(parent))
        lines = {}
        for statement in class_def.body:
            if not (
                isinstance(statement, ast.Assign)
                and isinstance(statement.targets[0], ast.Name)
            ):
                continue
            value = enum_type.values.get(statement.targets[0].id)
            names = environments(value.ast_node) if value else None
            line = available_on(names) if names != parent else None
            if line is not None:
                lines[id(statement)] = line
        _add_attribute_docstrings(class_def, lines)
        return class_def


def _add_attribute_docstrings(class_def: ast.ClassDef, lines: dict[int, str]) -> None:
    body: list[ast.stmt] = []
    pending: str | None = None
    for statement in class_def.body:
        if pending is not None and _docstring(statement) is not None:
            body.append(_joined(pending, statement))
            pending = None
            continue
        if pending is not None:
            body.append(_docstring_expr(pending))
        body.append(statement)
        pending = lines.get(id(statement))
    if pending is not None:
        body.append(_docstring_expr(pending))
    class_def.body = body


def _add_class_docstring(class_def: ast.ClassDef, line: str | None) -> None:
    if line is None:
        return
    first = class_def.body[0] if class_def.body else None
    if first is not None and _docstring(first) is not None:
        class_def.body[0] = _joined(line, first)
    else:
        class_def.body.insert(0, _docstring_expr(line))


def _docstring(statement: ast.stmt) -> str | None:
    if (
        isinstance(statement, ast.Expr)
        and isinstance(statement.value, ast.Constant)
        and isinstance(statement.value.value, str)
    ):
        return statement.value.value
    return None


def _joined(line: str, description: ast.stmt) -> ast.Expr:
    return _docstring_expr(f"{line}\n\n{_docstring(description)}")


def _docstring_expr(text: str) -> ast.Expr:
    return ast.Expr(value=ast.Constant(value=text))


def _operation_environments(
    schema: GraphQLSchema, operation: OperationDefinitionNode
) -> tuple[str, ...] | None:
    """
    Return the environments that have every root field the operation selects.
    """
    root = {
        OperationType.QUERY: schema.query_type,
        OperationType.MUTATION: schema.mutation_type,
        OperationType.SUBSCRIPTION: schema.subscription_type,
    }[operation.operation]
    found: tuple[str, ...] | None = None
    for selection in operation.selection_set.selections:
        if not isinstance(selection, FieldNode) or root is None:
            continue
        field = root.fields.get(selection.name.value)
        names = environments(field.ast_node) if field else None
        if names is None:
            continue
        found = names if found is None else tuple(n for n in found if n in names)
    return found
