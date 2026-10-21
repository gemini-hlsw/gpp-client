"""
GraphQL client behavior shared by every environment.
"""

__all__ = ["EnvironmentGraphQLClient", "GPPGraphQLClient"]

from collections.abc import AsyncIterator
from functools import cache
from typing import TYPE_CHECKING, Any
from urllib.parse import urljoin
from weakref import WeakKeyDictionary

import httpx
from websockets.exceptions import WebSocketException

from gpp_client.environment import GPPEnvironment
from gpp_client.exceptions import (
    GPPGraphQLError,
    GPPHttpError,
    GPPTransportError,
    NotAvailable,
)
from gpp_client.generated.client import GraphQLClient
from gpp_client.generated.exceptions import (
    GraphQLClientError,
    GraphQLClientGraphQLMultiError,
    GraphQLClientHttpError,
)
from gpp_client.generated_tables import load_generated
from gpp_client.trimmed_operations import find_trimmed_operation
from graphql import OperationDefinitionNode, parse

if TYPE_CHECKING:
    from gpp_client.generated.async_base_client import AsyncBaseClient

    # The mixin always sits before a generated client in the bases; typing it
    # as one declares the attributes and methods it reaches through super().
    _GeneratedClient = AsyncBaseClient
else:
    _GeneratedClient = object


# Each response's parsed data, kept while the response is alive. ``execute``
# must parse to raise GPP's answer for raw callers, and every generated method
# then calls ``get_data`` on the same response; the cache keeps that one parse
# without changing what either method returns.
_parsed_data: WeakKeyDictionary[Any, dict[str, Any]] = WeakKeyDictionary()


class EnvironmentGraphQLClient(_GeneratedClient):
    """
    Mixin for a generated GraphQL client that targets one GPP environment.

    It sends the environment's committed copy of every generated operation
    with only the variables that copy declares, raises before sending one the
    environment lacks, passes any other document through unchanged, and sends
    the client's headers with every HTTP request.

    Parameters
    ----------
    *args : Any
        Arguments for the generated client.
    environment : GPPEnvironment
        The environment the client sends to.
    **kwargs : Any
        Keyword arguments for the generated client.
    """

    def __init__(
        self,
        *args: Any,
        environment: GPPEnvironment,
        **kwargs: Any,
    ) -> None:
        super().__init__(*args, **kwargs)
        self.environment = environment

    def _to_send(
        self, query: str, variables: dict[str, Any] | None
    ) -> tuple[str, dict[str, Any] | None]:
        """
        Return the query and variables as this environment receives them.

        A generated operation goes out as the environment's committed copy,
        with only the variables that copy still declares. Any other document
        goes out unchanged.

        Raises
        ------
        NotAvailable
            If the environment lacks the generated operation.
        """
        trimmed = find_trimmed_operation(self.environment, query)
        if trimmed is None:
            return query, variables
        if trimmed.document is None:
            raise NotAvailable(
                trimmed.name,
                "operation",
                self.environment,
                GPPEnvironment.where(lambda env: _sent(env, query) is not None),
            )
        if trimmed.document != query and variables:
            declared = _declared_variables(trimmed.document)
            variables = {k: v for k, v in variables.items() if k in declared}
        return trimmed.document, variables

    async def execute(
        self,
        query: str,
        operation_name: str | None = None,
        variables: dict[str, Any] | None = None,
        **kwargs: Any,
    ) -> Any:
        """
        Send a GraphQL request as this client's environment receives it.

        Parameters
        ----------
        query : str
            The GraphQL document.
        operation_name : str | None, optional
            The operation to run.
        variables : dict[str, Any] | None, optional
            The operation variables.
        **kwargs : Any
            Extra arguments for the HTTP client's ``post``.

        Returns
        -------
        Any
            The raw HTTP response. ``get_data`` returns its ``data`` member,
            parsed once here.

        Raises
        ------
        NotAvailable
            If the environment lacks the generated operation; nothing is sent.
        GPPTransportError
            If GPP could not be reached, or answered with something that is
            not GraphQL.
        GPPHttpError
            If GPP answered with an HTTP error status. The message carries
            GPP's errors, and for a rejected request other than a refused
            token, the commit GPP runs and the commit the client's schema was
            downloaded at.
        GPPGraphQLError
            If GPP returned errors for the request.
        """
        # The generated client applies `headers` only to an http client it builds
        # itself; sending them per request leaves a caller's client untouched.
        kwargs["headers"] = {**(self.headers or {}), **(kwargs.get("headers") or {})}
        query, variables = self._to_send(query, variables)
        try:
            response = await super().execute(query, operation_name, variables, **kwargs)
        except httpx.HTTPError as exc:
            raise GPPTransportError(
                self.environment, "could not be reached", str(exc)
            ) from exc
        try:
            _parsed_data[response] = self.get_data(response)
        except GPPHttpError as exc:
            messages = _graphql_error_messages(response)
            if not messages:
                raise
            detail = "; ".join(messages)
            if exc.status_code not in _AUTH_STATUSES:
                detail += f" ({await self._commit_comparison()})"
            raise GPPHttpError(
                self.environment, exc.status_code, response, detail
            ) from exc.__cause__
        return response

    async def _commit_comparison(self) -> str:
        """
        Name the commit GPP runs and the one the client's schema came from,
        so a rejected request shows whether the client is behind the server.
        """
        try:
            health = await self.http_client.get(
                urljoin(self.url, "/health"), timeout=_HEALTH_TIMEOUT
            )
            health.raise_for_status()
            server = health.json()["commit"]
        except (httpx.HTTPError, ValueError, KeyError, TypeError):
            server = None
        if not isinstance(server, str):
            server = None
        label = self.environment.label
        built = load_generated("schema_commits").COMMITS.get(label)
        return (
            f"GPP {label} runs commit {_short(server)}; this client was built "
            f"from its schema at commit {_short(built)}"
        )

    def get_data(self, response: Any) -> dict[str, Any]:
        """
        Return the ``data`` member of a GraphQL response.

        Parameters
        ----------
        response : Any
            The HTTP response ``execute`` returned.

        Returns
        -------
        dict[str, Any]
            The response's ``data``.

        Raises
        ------
        GPPHttpError
            If the response status is not a success.
        GPPGraphQLError
            If the response holds GraphQL errors.
        GPPTransportError
            If the response is not a GraphQL response.
        """
        try:
            return _parsed_data[response]
        except KeyError:
            pass
        try:
            return super().get_data(response)
        except GraphQLClientHttpError as exc:
            raise GPPHttpError(self.environment, exc.status_code, response) from exc
        except GraphQLClientGraphQLMultiError as exc:
            raise GPPGraphQLError(self.environment, exc.errors, exc.data) from exc
        except GraphQLClientError as exc:
            raise GPPTransportError(
                self.environment, "sent a response that is not GraphQL"
            ) from exc

    async def execute_ws(
        self,
        query: str,
        operation_name: str | None = None,
        variables: dict[str, Any] | None = None,
        **kwargs: Any,
    ) -> AsyncIterator[dict[str, Any]]:
        """
        Subscribe as this client's environment receives the operation.

        Parameters
        ----------
        query : str
            The GraphQL subscription document.
        operation_name : str | None, optional
            The operation to run.
        variables : dict[str, Any] | None, optional
            The operation variables.
        **kwargs : Any
            Extra arguments for the websocket connection.

        Yields
        ------
        dict[str, Any]
            Each message's data.

        Raises
        ------
        NotAvailable
            If the environment lacks the subscription; nothing is sent.
        GPPGraphQLError
            If GPP answers the subscription with errors.
        GPPTransportError
            If the connection fails or drops, or GPP sends a message the
            client cannot read.
        """
        query, variables = self._to_send(query, variables)
        try:
            async for data in super().execute_ws(
                query, operation_name, variables, **kwargs
            ):
                yield data
        except GraphQLClientGraphQLMultiError as exc:
            raise GPPGraphQLError(self.environment, exc.errors, exc.data) from exc
        except GraphQLClientError as exc:
            raise GPPTransportError(
                self.environment, "sent a message that is not GraphQL", str(exc)
            ) from exc
        except (OSError, WebSocketException) as exc:
            raise GPPTransportError(
                self.environment, "could not be reached", str(exc)
            ) from exc


class GPPGraphQLClient(EnvironmentGraphQLClient, GraphQLClient):
    """
    The generated GraphQL client, targeting one GPP environment.
    """


_HEALTH_TIMEOUT = 5.0
# A refused token says nothing about the schema, so it skips the commits.
_AUTH_STATUSES = frozenset({401, 403})


def _graphql_error_messages(response: Any) -> list[str]:
    try:
        errors = response.json().get("errors")
    except (ValueError, AttributeError):
        return []
    if not isinstance(errors, list):
        return []
    return [
        error["message"]
        for error in errors
        if isinstance(error, dict) and isinstance(error.get("message"), str)
    ]


def _short(commit: str | None) -> str:
    return commit[:7] if commit else "unknown"


def _sent(environment: GPPEnvironment, query: str) -> str | None:
    trimmed = find_trimmed_operation(environment, query)
    return None if trimmed is None else trimmed.document


@cache
def _declared_variables(document: str) -> frozenset[str]:
    return frozenset(
        variable.variable.name.value
        for definition in parse(document).definitions
        if isinstance(definition, OperationDefinitionNode)
        for variable in definition.variable_definitions
    )
