"""
Check a document against one environment before sending it.

Every document is validated, and its variables coerced, against the schema of
each environment, which the build bundles in the generated package. A generated operation is checked as each environment receives it: its
trimmed copy.
"""

__all__ = ["check_document"]

from collections.abc import Callable
from enum import Enum
from functools import lru_cache
from importlib.resources import files
from typing import Any, NamedTuple

from graphql.execution.values import get_variable_values

from gpp_client.environment import GPPEnvironment
from gpp_client.exceptions import EnvironmentItemKind, GPPEnvironmentError
from gpp_client.generated_tables import generated_package
from gpp_client.leaving_fields import warn_leaving_field
from graphql import (
    BREAK,
    ArgumentNode,
    DocumentNode,
    EnumValueNode,
    FieldNode,
    GraphQLEnumType,
    GraphQLError,
    GraphQLInputObjectType,
    GraphQLSchema,
    ObjectFieldNode,
    OperationDefinitionNode,
    TypeInfo,
    TypeInfoVisitor,
    Undefined,
    VariableNode,
    Visitor,
    build_ast_schema,
    get_named_type,
    is_list_type,
    is_non_null_type,
    parse,
    type_from_ast,
    validate,
    visit,
)


class _Lack(NamedTuple):
    """
    An item the selected environment lacks, as the parts of its schema coordinate.

    An operation has no coordinate, so its lack holds its name in ``type_name``.
    """

    kind: EnvironmentItemKind
    type_name: str
    member: str | None = None
    argument: str | None = None
    required: bool = False

    @property
    def item(self) -> str:
        """
        Return the item as the error names it.

        Returns
        -------
        str
            The coordinate, such as ``Query.program(id:)``, or the operation name.
        """
        item = self.type_name
        if self.member is not None:
            item += f".{self.member}"
        if self.argument is not None:
            item += f"({self.argument}:)"
        return item


def check_document(
    environment: GPPEnvironment,
    query: str,
    operation_name: str | None,
    variables: dict[str, Any] | None,
    sent: Callable[[GPPEnvironment], str | None] | None = None,
) -> None:
    """
    Raise if the document uses something the environment lacks; warn for each
    field it selects that is leaving.

    A call no environment accepts still raises when another environment has the
    item the selected one lacks, as when a call sets both a field and its
    replacement. An item no environment has, such as a misspelled field, is
    left for GPP to answer.

    Parameters
    ----------
    environment : GPPEnvironment
        The selected environment.
    query : str
        The document about to be sent.
    operation_name : str | None
        The operation to run, when the document has several.
    variables : dict[str, Any] | None
        The variables as sent: input models already dumped by alias.
    sent : Callable[[GPPEnvironment], str | None] | None, optional
        The document each environment receives, ``None`` where it receives
        none. Defaults to ``query`` on every environment.

    Raises
    ------
    GPPEnvironmentError
        Raised when the selected environment rejects the document and another
        environment has what it lacks: another environment accepts the
        document, or, when none does, another environment has the item.
    """
    package = generated_package()

    def received(env: GPPEnvironment) -> str | None:
        return query if sent is None else sent(env)

    selected_query = received(environment)
    document = None if selected_query is None else _parse(selected_query)
    if selected_query is None or document is None:
        return
    operation = _operation(document, operation_name)
    if operation is None:
        return
    values = variables or {}

    def works_on(env: GPPEnvironment) -> bool:
        env_query = received(env)
        return (
            env_query is not None
            and _works_on(package, env.label, env_query, operation_name, values)
            and _dropped_argument(package, env.label, query, env_query, values) is None
        )

    if works_on(environment):
        if environment is not GPPEnvironment.DEVELOPMENT:
            for field in _leaving_fields(package, environment.label, selected_query):
                warn_leaving_field(field, environment)
        return

    available = GPPEnvironment.where(
        lambda env: env is not environment and works_on(env)
    )
    works_there = bool(available)
    if works_there:
        lack = _dropped_argument(
            package, environment.label, query, selected_query, values
        ) or _what_lacks(
            _schema(package, environment.label),
            _schema(package, available[0].label),
            document,
            operation,
            values,
        )
    else:
        found = _lack_another_environment_has(
            package, environment, document, operation, values
        )
        if found is None:
            return
        lack, available = found
    raise GPPEnvironmentError(
        lack.item,
        lack.kind,
        environment,
        available,
        required=lack.required,
        works_there=works_there,
    )


@lru_cache(maxsize=8)
def _schema(package: str, environment: str) -> GraphQLSchema:
    sdl = files(package).joinpath("schemas", f"{environment}.graphql").read_text()
    return build_ast_schema(parse(sdl, no_location=True), assume_valid_sdl=True)


@lru_cache(maxsize=256)
def _parse(query: str) -> DocumentNode | None:
    try:
        return parse(query)
    except GraphQLError:
        return None


def _operation(
    document: DocumentNode, operation_name: str | None
) -> OperationDefinitionNode | None:
    operations = [
        definition
        for definition in document.definitions
        if isinstance(definition, OperationDefinitionNode)
    ]
    for operation in operations:
        if operation_name is None or (
            operation.name and operation.name.value == operation_name
        ):
            return operation
    return None


def _works_on(
    package: str,
    environment: str,
    query: str,
    operation_name: str | None,
    variables: dict[str, Any],
) -> bool:
    document = _parse(query)
    if document is None or not _valid(package, environment, query):
        return False
    operation = _operation(document, operation_name)
    if operation is None:
        return False
    coerced = get_variable_values(
        _schema(package, environment),
        operation.variable_definitions or (),
        variables,
        max_errors=1,
    )
    return not isinstance(coerced, list)


@lru_cache(maxsize=256)
def _valid(package: str, environment: str, query: str) -> bool:
    document = _parse(query)
    return document is not None and not validate(
        _schema(package, environment), document, max_errors=1
    )


@lru_cache(maxsize=256)
def _leaving_fields(package: str, environment: str, query: str) -> tuple[str, ...]:
    """
    Return each field the document selects that development lacks.
    """
    document = _parse(query)
    if document is None:
        return ()
    development = _schema(package, GPPEnvironment.DEVELOPMENT.label)
    type_info = TypeInfo(_schema(package, environment))
    found: list[str] = []

    class _Collector(Visitor):
        def enter_field(self, node: FieldNode, *_args) -> None:
            parent = type_info.get_parent_type()
            if parent is None or node.name.value.startswith("__"):
                return
            if not _has_field(development, parent.name, node.name.value):
                coordinate = f"{parent.name}.{node.name.value}"
                if coordinate not in found:
                    found.append(coordinate)

    visit(document, TypeInfoVisitor(type_info, _Collector()))
    return tuple(found)


def _dropped_argument(
    package: str,
    environment: str,
    query: str,
    sent: str,
    variables: dict[str, Any],
) -> _Lack | None:
    """
    Return the first argument set by a variable that ``sent`` dropped with it.

    ``query`` is the operation before trimming. Only an argument the
    environment lacks on a field it has counts: a value passed to a field it
    lacks belongs to a field that reads ``None`` there.
    """
    if sent == query:
        return None
    document = _parse(query)
    if document is None:
        return None
    finder = _DroppedArgumentFinder(TypeInfo(_schema(package, environment)), variables)
    visit(document, TypeInfoVisitor(finder.type_info, finder))
    return finder.lack


class _DroppedArgumentFinder(Visitor):
    def __init__(self, type_info: TypeInfo, variables: dict[str, Any]) -> None:
        super().__init__()
        self.type_info = type_info
        self.variables = variables
        self.field = ""
        self.argument: _Lack | None = None
        self.lack: _Lack | None = None

    def enter_field(self, node: FieldNode, *_args) -> None:
        self.field = node.name.value

    def enter_argument(self, node: ArgumentNode, *_args) -> None:
        parent = self.type_info.get_parent_type()
        if (
            parent is not None
            and self.type_info.get_field_def() is not None
            and self.type_info.get_directive() is None
            and self.type_info.get_argument() is None
        ):
            self.argument = _Lack(
                EnvironmentItemKind.ARGUMENT,
                parent.name,
                self.field,
                node.name.value,
            )

    def leave_argument(self, *_args) -> None:
        self.argument = None

    def enter_variable(self, node: VariableNode, *_args) -> object:
        if (
            self.argument is not None
            and self.variables.get(node.name.value) is not None
        ):
            self.lack = self.argument
            return BREAK
        return None


def _lack_another_environment_has(
    package: str,
    environment: GPPEnvironment,
    document: DocumentNode,
    operation: OperationDefinitionNode,
    variables: dict[str, Any],
) -> tuple[_Lack, tuple[GPPEnvironment, ...]] | None:
    """
    Return what the selected environment lacks and the environments that have it.

    When every environment rejects the call, each can lack something different,
    such as a field and its replacement during a rename. The selected
    environment's own problem is still an environment problem when another
    environment has the item; when none has it, GPP should answer.
    """
    selected = _schema(package, environment.label)
    others = GPPEnvironment.where(lambda env: env is not environment)
    for other in others:
        lack = _what_lacks(
            selected, _schema(package, other.label), document, operation, variables
        )
        having = tuple(env for env in others if _has(_schema(package, env.label), lack))
        if having:
            return lack, having
    return None


def _has(schema: GraphQLSchema, lack: _Lack) -> bool:
    member = lack.member
    if member is None:
        return False
    if lack.kind is EnvironmentItemKind.ENUM_VALUE:
        return _has_enum_value(schema, lack.type_name, member)
    fields = getattr(schema.get_type(lack.type_name), "fields", {})
    if lack.kind is EnvironmentItemKind.FIELD:
        return member in fields
    if lack.kind is EnvironmentItemKind.ARGUMENT:
        field = fields.get(member)
        definition = field.args.get(lack.argument) if field is not None else None
    elif lack.kind is EnvironmentItemKind.INPUT_FIELD:
        definition = fields.get(member)
    else:
        return False
    if lack.required:
        return definition is None or not (
            is_non_null_type(definition.type) and definition.default_value is Undefined
        )
    return definition is not None


def _what_lacks(
    selected: GraphQLSchema,
    working: GraphQLSchema,
    document: DocumentNode,
    operation: OperationDefinitionNode,
    variables: dict[str, Any],
) -> _Lack:
    """
    Return the first part the document uses that ``selected`` lacks.

    The document is read with ``working``, a schema it is valid on, so every
    field, argument and value has a known definition to compare.
    """
    finder = _LackFinder(TypeInfo(working), selected)
    visit(document, TypeInfoVisitor(finder.type_info, finder))
    if finder.lack is not None:
        return finder.lack
    for definition in operation.variable_definitions or ():
        input_type = type_from_ast(working, definition.type)
        value = variables.get(definition.variable.name.value)
        if input_type is None:
            continue
        lack = _value_lack(input_type, value, selected)
        if lack is not None:
            return lack
    name = operation.name.value if operation.name else "anonymous"
    return _Lack(EnvironmentItemKind.OPERATION, name)


class _LackFinder(Visitor):
    def __init__(self, type_info: TypeInfo, selected: GraphQLSchema) -> None:
        super().__init__()
        self.type_info = type_info
        self.selected = selected
        self.lack: _Lack | None = None

    def _found(self, lack: _Lack) -> object:
        self.lack = lack
        return BREAK

    def enter_field(self, node: FieldNode, *_args) -> object:
        parent = self.type_info.get_parent_type()
        name = node.name.value
        if parent is None or name.startswith("__"):
            return None
        selected_type = self.selected.get_type(parent.name)
        selected_field = getattr(selected_type, "fields", {}).get(name)
        if selected_field is None:
            return self._found(_Lack(EnvironmentItemKind.FIELD, parent.name, name))
        given = {argument.name.value for argument in node.arguments or ()}
        for argument_name, argument in selected_field.args.items():
            if argument_name in given:
                continue
            if is_non_null_type(argument.type) and argument.default_value is Undefined:
                return self._found(
                    _Lack(
                        EnvironmentItemKind.ARGUMENT,
                        parent.name,
                        name,
                        argument_name,
                        required=True,
                    )
                )
        for argument in node.arguments or ():
            if argument.name.value not in selected_field.args:
                return self._found(
                    _Lack(
                        EnvironmentItemKind.ARGUMENT,
                        parent.name,
                        name,
                        argument.name.value,
                    )
                )
        return None

    def enter_object_field(self, node: ObjectFieldNode, *_args) -> object:
        parent = self.type_info.get_parent_input_type()
        if parent is None:
            return None
        named = get_named_type(parent)
        if not _has_input_field(self.selected, named.name, node.name.value):
            return self._found(
                _Lack(EnvironmentItemKind.INPUT_FIELD, named.name, node.name.value)
            )
        return None

    def enter_enum_value(self, node: EnumValueNode, *_args) -> object:
        input_type = self.type_info.get_input_type()
        if input_type is None:
            return None
        named = get_named_type(input_type)
        if not _has_enum_value(self.selected, named.name, node.value):
            return self._found(
                _Lack(EnvironmentItemKind.ENUM_VALUE, named.name, node.value)
            )
        return None


def _value_lack(input_type: Any, value: Any, selected: GraphQLSchema) -> _Lack | None:
    """
    Return the first input field or enum value in a variable ``selected`` lacks.
    """
    if value is None:
        return None
    if is_non_null_type(input_type):
        input_type = input_type.of_type
    if is_list_type(input_type):
        items = value if isinstance(value, list) else [value]
        for item in items:
            lack = _value_lack(input_type.of_type, item, selected)
            if lack is not None:
                return lack
        return None
    if isinstance(input_type, GraphQLEnumType):
        if isinstance(value, Enum):
            value = value.value
        if isinstance(value, str) and not _has_enum_value(
            selected, input_type.name, value
        ):
            return _Lack(EnvironmentItemKind.ENUM_VALUE, input_type.name, value)
        return None
    if not isinstance(input_type, GraphQLInputObjectType) or not isinstance(
        value, dict
    ):
        return None
    selected_type = selected.get_type(input_type.name)
    selected_fields = getattr(selected_type, "fields", {})
    for name, field in selected_fields.items():
        if (
            is_non_null_type(field.type)
            and field.default_value is Undefined
            and value.get(name) is None
        ):
            return _Lack(
                EnvironmentItemKind.INPUT_FIELD, input_type.name, name, required=True
            )
    for name, item in value.items():
        if name not in selected_fields:
            return _Lack(EnvironmentItemKind.INPUT_FIELD, input_type.name, name)
        if name in input_type.fields:
            lack = _value_lack(input_type.fields[name].type, item, selected)
            if lack is not None:
                return lack
    return None


def _has_field(schema: GraphQLSchema, type_name: str, field: str) -> bool:
    return field in getattr(schema.get_type(type_name), "fields", {})


def _has_input_field(schema: GraphQLSchema, type_name: str, field: str) -> bool:
    named = schema.get_type(type_name)
    return isinstance(named, GraphQLInputObjectType) and field in named.fields


def _has_enum_value(schema: GraphQLSchema, type_name: str, value: str) -> bool:
    named = schema.get_type(type_name)
    return isinstance(named, GraphQLEnumType) and value in named.values
