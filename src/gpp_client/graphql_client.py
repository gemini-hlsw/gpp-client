"""
GraphQL client behavior shared by every environment.
"""

__all__ = ["EnvironmentGraphQLClient", "GPPGraphQLClient"]

from collections.abc import AsyncIterator
from typing import TYPE_CHECKING, Any

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
from gpp_client.trimmed_operations import find_trimmed_operation

if TYPE_CHECKING:
    from gpp_client.generated.async_base_client import AsyncBaseClient

    # The mixin always sits before a generated client in the bases; typing it
    # as one declares the attributes and methods it reaches through super().
    _GeneratedClient = AsyncBaseClient
else:
    _GeneratedClient = object


class EnvironmentGraphQLClient(_GeneratedClient):
    """
    Mixin for a generated GraphQL client that targets one GPP environment.

    It sends the environment's committed copy of every generated operation,
    raises before sending one the environment lacks, passes any other document
    through unchanged, and sends the client's headers with every HTTP request.

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

    def _document_to_send(self, query: str) -> str:
        """
        Return the query as this environment receives it.

        Raises
        ------
        NotAvailable
            If the environment lacks the generated operation.
        """
        trimmed = find_trimmed_operation(self.environment, query)
        if trimmed is None:
            return query
        if trimmed.document is None:
            raise NotAvailable(
                trimmed.name,
                "operation",
                self.environment,
                GPPEnvironment.where(lambda env: _sent(env, query) is not None),
            )
        return trimmed.document

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
            The raw HTTP response. ``get_data`` returns its ``data`` member.

        Raises
        ------
        NotAvailable
            If the environment lacks the generated operation; nothing is sent.
        GPPTransportError
            If GPP could not be reached, or answered with something that is
            not GraphQL.
        GPPHttpError
            If GPP answered with an HTTP error status.
        GPPGraphQLError
            If GPP returned errors for the request.
        """
        # The generated client applies `headers` only to an http client it builds
        # itself; sending them per request leaves a caller's client untouched.
        kwargs["headers"] = {**(self.headers or {}), **(kwargs.get("headers") or {})}
        query = self._document_to_send(query)
        try:
            response = await super().execute(query, operation_name, variables, **kwargs)
        except httpx.HTTPError as exc:
            raise GPPTransportError(
                self.environment, "could not be reached", str(exc)
            ) from exc
        self.get_data(response)
        return response

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
        query = self._document_to_send(query)
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


def _sent(environment: GPPEnvironment, query: str) -> str | None:
    trimmed = find_trimmed_operation(environment, query)
    return None if trimmed is None else trimmed.document
