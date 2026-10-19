"""
Shared fixtures that build a real ``GPPClient`` over a mocked HTTP transport.
"""

import json
from collections.abc import AsyncIterator
from typing import Any

import httpx
import pytest
import pytest_asyncio

from gpp_client import GPPClient

TEST_TOKEN = "test-token"


class RecordingTransport(httpx.MockTransport):
    """
    Answer GraphQL requests with canned responses and record every request.
    """

    def __init__(self) -> None:
        super().__init__(self._handle)
        self.requests: list[httpx.Request] = []
        self._responses: list[dict[str, Any]] = []

    def respond(self, data: dict[str, Any] | None = None, **body: Any) -> None:
        """
        Queue the JSON body for the next request.

        Parameters
        ----------
        data : dict[str, Any] | None, optional
            The GraphQL ``data`` member.
        **body : Any
            Other top-level members, such as ``errors``.
        """
        self._responses.append({"data": data, **body})

    @property
    def bodies(self) -> list[dict[str, Any]]:
        """
        Return the decoded JSON body of every recorded request.

        Returns
        -------
        list[dict[str, Any]]
            Request bodies in the order they were sent.
        """
        return [json.loads(request.content) for request in self.requests]

    def _handle(self, request: httpx.Request) -> httpx.Response:
        self.requests.append(request)
        if not self._responses:
            raise AssertionError(f"Unexpected request: {request.content!r}")
        return httpx.Response(200, json=self._responses.pop(0))


@pytest.fixture()
def gpp_transport() -> RecordingTransport:
    """
    Return a recording transport with no canned responses yet.
    """
    return RecordingTransport()


@pytest_asyncio.fixture(loop_scope="function")
async def gpp_client(gpp_transport) -> AsyncIterator[GPPClient]:
    """
    Return a real ``GPPClient`` whose GraphQL requests go to ``gpp_transport``.
    """
    async with httpx.AsyncClient(transport=gpp_transport) as http_client:
        async with GPPClient(token=TEST_TOKEN, http_client=http_client) as client:
            yield client
