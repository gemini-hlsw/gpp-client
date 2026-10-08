"""
A fake GPP that answers any GraphQL document from an environment's committed
schema.

Each response is built from the schema for the exact document the client sent,
either with every nullable field null or with every field filled. Tests that
use it must assert the same thing on every environment, so they pass on any
committed schemas.
"""

import json
from collections.abc import AsyncIterator
from contextlib import asynccontextmanager
from pathlib import Path
from typing import Any

import httpx
from graphql.pyutils import Undefined

from gpp_client import GPPClient
from gpp_client.environment import GPPEnvironment
from graphql import (
    DocumentNode,
    GraphQLEnumType,
    GraphQLInputObjectType,
    GraphQLList,
    GraphQLNonNull,
    GraphQLSchema,
    build_schema,
    execute,
    get_named_type,
    is_composite_type,
    parse,
    type_from_ast,
    validate,
)
from tests.gpp_client.conftest import TEST_TOKEN
from tests.gpp_client.subscription_server import SubscriptionServer, ws_url

_SCHEMA_DIR = Path(__file__).resolve().parents[2] / "graphql" / "schemas"
SCHEMAS: dict[GPPEnvironment, GraphQLSchema] = {
    environment: build_schema(
        (_SCHEMA_DIR / f"{environment.label}.graphql").read_text()
    )
    for environment in GPPEnvironment
}
_BUILT_IN_LEAVES = {"Int": 1, "Float": 1.5, "Boolean": True}


def _leaf(named_type) -> Any:
    if isinstance(named_type, GraphQLEnumType):
        return next(iter(named_type.values))
    return _BUILT_IN_LEAVES.get(named_type.name, f"{named_type.name}-1")


def _output_value(type_, nulls: bool) -> Any:
    if nulls and not isinstance(type_, GraphQLNonNull):
        return None
    if isinstance(type_, GraphQLNonNull):
        type_ = type_.of_type
    if isinstance(type_, GraphQLList):
        return [_output_value(type_.of_type, nulls=False)]
    named_type = get_named_type(type_)
    return {} if is_composite_type(named_type) else _leaf(named_type)


def _input_value(type_) -> Any:
    if isinstance(type_, GraphQLNonNull):
        type_ = type_.of_type
    if isinstance(type_, GraphQLList):
        return [_input_value(type_.of_type)]
    if isinstance(type_, GraphQLInputObjectType):
        return {
            name: _input_value(field.type)
            for name, field in type_.fields.items()
            if isinstance(field.type, GraphQLNonNull)
            and field.default_value is Undefined
        }
    return _leaf(type_)


def _required_variables(schema: GraphQLSchema, document: DocumentNode) -> dict:
    # The fake ignores the variables the client sent: they come from empty
    # input models, and only the response shape is under test.
    variables = {}
    for definition in document.definitions:
        for variable in getattr(definition, "variable_definitions", None) or ():
            type_ = type_from_ast(schema, variable.type)
            if isinstance(type_, GraphQLNonNull) and variable.default_value is None:
                variables[variable.variable.name.value] = _input_value(type_)
    return variables


def answer(schema: GraphQLSchema, payload: dict, nulls: bool) -> dict:
    """
    Build the ``data`` a GPP with ``schema`` would return for ``payload``.

    Fails the calling test if the document is not valid against the schema.

    Parameters
    ----------
    schema : GraphQLSchema
        The schema to validate and answer against.
    payload : dict
        A GraphQL request body with ``query`` and optional ``operationName``.
    nulls : bool
        Whether every nullable field is null, rather than filled.

    Returns
    -------
    dict
        The response's ``data`` member.
    """
    document = parse(payload["query"])
    assert validate(schema, document) == []
    result = execute(
        schema,
        document,
        root_value={},
        variable_values=_required_variables(schema, document),
        operation_name=payload.get("operationName"),
        field_resolver=lambda source, info, **arguments: _output_value(
            info.return_type, nulls
        ),
        type_resolver=lambda value, info, abstract_type: (
            info.schema.get_possible_types(abstract_type)[0].name
        ),
    )
    assert result.errors is None
    assert result.data is not None
    return result.data


class SchemaTransport(httpx.MockTransport):
    """
    Answer each GraphQL request from an environment's committed schema.

    Parameters
    ----------
    environment : GPPEnvironment
        The environment whose committed schema answers requests.
    nulls : bool, optional
        Whether every nullable field is null, rather than filled.
    """

    def __init__(self, environment: GPPEnvironment, nulls: bool = False) -> None:
        super().__init__(self._handle)
        self.environment = environment
        self.schema = SCHEMAS[environment]
        self.nulls = nulls
        self.requests: list[httpx.Request] = []

    def _handle(self, request: httpx.Request) -> httpx.Response:
        self.requests.append(request)
        data = answer(self.schema, json.loads(request.content), self.nulls)
        return httpx.Response(200, json={"data": data})


@asynccontextmanager
async def schema_client(transport: SchemaTransport) -> AsyncIterator[GPPClient]:
    """
    Open a real ``GPPClient`` on the transport's environment.

    Parameters
    ----------
    transport : SchemaTransport
        The fake that answers the client's GraphQL requests.

    Yields
    ------
    GPPClient
        A client whose GraphQL requests go to ``transport``.
    """
    async with httpx.AsyncClient(transport=transport) as http_client:
        async with GPPClient(
            environment=transport.environment,
            token=TEST_TOKEN,
            http_client=http_client,
        ) as client:
            yield client


@asynccontextmanager
async def schema_subscriptions(
    client: GPPClient, environment: GPPEnvironment, *, nulls: bool
) -> AsyncIterator[SubscriptionServer]:
    """
    Serve the client's subscriptions from an environment's committed schema.

    Parameters
    ----------
    client : GPPClient
        The client whose subscriptions go to the local server.
    environment : GPPEnvironment
        The environment whose schema shapes each event.
    nulls : bool
        Whether the server answers every nullable field with null.

    Yields
    ------
    SubscriptionServer
        The running server, to count its connections.
    """
    schema = SCHEMAS[environment]
    subscription_server = SubscriptionServer(
        lambda payload: answer(schema, payload, nulls)
    )
    async with subscription_server() as running:
        client.graphql.ws_url = ws_url(running)
        yield subscription_server
