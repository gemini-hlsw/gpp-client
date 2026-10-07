"""
GraphQL client behavior shared by every environment.
"""

__all__ = ["EnvironmentGraphQLClient", "GPPGraphQLClient"]

from collections.abc import AsyncIterator
from functools import lru_cache
from typing import TYPE_CHECKING, Any

from gpp_client.document_checks import check_document
from gpp_client.environment import GPPEnvironment
from gpp_client.exceptions import EnvironmentItemKind, GPPEnvironmentError
from gpp_client.generated.client import GraphQLClient
from gpp_client.generated.environment_clients import EveryEnvironmentGraphQLClient
from gpp_client.trimmed_operations import find_trimmed_operation
from graphql import OperationDefinitionNode, parse

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

    It checks every call against the environment before sending, sends the
    environment's trimmed copy of every generated operation, and sends the
    client's headers with every HTTP request.

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

    def _document_and_variables_to_send(
        self, query: str, operation_name: str | None, variables: dict[str, Any] | None
    ) -> tuple[str, dict[str, Any] | None]:
        """
        Return the query and variables to send, raising if the environment lacks
        what they use.
        """
        trimmed = find_trimmed_operation(self.environment, query)
        if trimmed is None:
            check_document(
                self.environment,
                query,
                operation_name,
                self._convert_dict_to_json_serializable(variables or {}),
            )
            return query, variables
        if trimmed.document is None:
            raise GPPEnvironmentError(
                trimmed.name,
                EnvironmentItemKind.OPERATION,
                self.environment,
                GPPEnvironment.where(lambda env: _sent(env, query) is not None),
            )
        check_document(
            self.environment,
            query,
            operation_name,
            self._convert_dict_to_json_serializable(variables or {}),
            sent=lambda environment: _sent(environment, query),
        )
        if variables and trimmed.document != query:
            # Trimming drops the variables only the removed parts used; sending
            # them anyway would rely on GPP ignoring undeclared variables.
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
            The raw HTTP response.
        """
        # The generated client applies `headers` only to an http client it builds
        # itself; sending them per request leaves a caller's client untouched.
        kwargs["headers"] = {**(self.headers or {}), **(kwargs.get("headers") or {})}
        query, variables = self._document_and_variables_to_send(
            query, operation_name, variables
        )
        return await super().execute(query, operation_name, variables, **kwargs)

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
        """
        query, variables = self._document_and_variables_to_send(
            query, operation_name, variables
        )
        async for data in super().execute_ws(
            query, operation_name, variables, **kwargs
        ):
            yield data


class GPPGraphQLClient(
    EnvironmentGraphQLClient, GraphQLClient, EveryEnvironmentGraphQLClient
):
    """
    The generated GraphQL client, targeting one GPP environment.

    It is every environment's typed view, so a client typed for one environment
    accepts the full client.
    """


def _sent(environment: GPPEnvironment, query: str) -> str | None:
    trimmed = find_trimmed_operation(environment, query)
    return None if trimmed is None else trimmed.document


@lru_cache(maxsize=256)
def _declared_variables(document: str) -> frozenset[str]:
    return frozenset(
        variable.variable.name.value
        for definition in parse(document).definitions
        if isinstance(definition, OperationDefinitionNode)
        for variable in definition.variable_definitions or ()
    )
