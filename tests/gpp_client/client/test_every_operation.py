"""
Tests that every generated operation works on every environment.

A fake GPP answers each request with a response built from the selected
environment's committed schema for the exact document the client sent: once
with every nullable field null, once with every field filled. The tests assert
the same thing on every environment, so they pass on any committed schemas and
never depend on today's differences between them.
"""

import importlib.util
import inspect
from typing import Any, get_args, get_origin

import pytest
from pydantic import BaseModel

from gpp_client import GPPClient
from gpp_client.environment import GPPEnvironment
from gpp_client.exceptions import EnvironmentItemKind, GPPEnvironmentError
from gpp_client.generated.client import GraphQLClient
from tests.gpp_client.conftest import TEST_TOKEN
from tests.gpp_client.schema_transport import (
    SchemaTransport,
    schema_client,
    schema_subscriptions,
)


def _generated_operations(kind) -> list[str]:
    # Each generated operation has a module of its own, named after its method.
    return sorted(
        name
        for name, method in vars(GraphQLClient).items()
        if kind(method)
        and importlib.util.find_spec(f"gpp_client.generated.{name}") is not None
    )


_QUERIES_AND_MUTATIONS = _generated_operations(inspect.iscoroutinefunction)
_SUBSCRIPTIONS = _generated_operations(inspect.isasyncgenfunction)


def _argument(annotation: Any) -> Any:
    if get_origin(annotation) is list:
        return []
    if inspect.isclass(annotation) and issubclass(annotation, BaseModel):
        return annotation.model_construct()
    if annotation is bool:
        return False
    if inspect.isclass(annotation) and hasattr(annotation, "__members__"):
        return next(iter(annotation))
    for member in get_args(annotation):
        if member is not type(None):
            return _argument(member)
    return "x-1"


def _required_arguments(method) -> dict[str, Any]:
    return {
        name: _argument(parameter.annotation)
        for name, parameter in inspect.signature(method).parameters.items()
        if parameter.kind is parameter.POSITIONAL_OR_KEYWORD
        and parameter.default is parameter.empty
    }


_ENVIRONMENTS = pytest.mark.parametrize(
    "environment", list(GPPEnvironment), ids=lambda environment: environment.label
)
_NULLS = pytest.mark.parametrize("nulls", [True, False], ids=["nulls", "filled"])


@_NULLS
@_ENVIRONMENTS
@pytest.mark.parametrize("operation", _QUERIES_AND_MUTATIONS)
@pytest.mark.asyncio
async def test_query_or_mutation_parses_on_every_environment(
    operation: str, environment: GPPEnvironment, nulls: bool
) -> None:
    """
    Ensure each query and mutation sends a document the environment accepts and
    parses the environment's response, or is refused before sending.
    """
    transport = SchemaTransport(environment, nulls)
    async with schema_client(transport) as client:
        method = getattr(client.graphql, operation)
        try:
            await method(**_required_arguments(method))
        except GPPEnvironmentError as error:
            assert error.kind is EnvironmentItemKind.OPERATION
            assert transport.requests == []


@_NULLS
@_ENVIRONMENTS
@pytest.mark.parametrize("operation", _SUBSCRIPTIONS)
@pytest.mark.asyncio
async def test_subscription_parses_on_every_environment(
    operation: str, environment: GPPEnvironment, nulls: bool
) -> None:
    """
    Ensure each subscription sends a document the environment accepts and
    parses the environment's event, or is refused before connecting.
    """
    async with GPPClient(environment=environment, token=TEST_TOKEN) as client:
        async with schema_subscriptions(
            client, environment, nulls=nulls
        ) as subscription_server:
            method = getattr(client.graphql, operation)
            try:
                events = [
                    event async for event in method(**_required_arguments(method))
                ]
            except GPPEnvironmentError as error:
                assert error.kind is EnvironmentItemKind.OPERATION
                assert subscription_server.connections == 0
            else:
                assert len(events) == 1
