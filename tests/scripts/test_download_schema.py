"""
Tests for downloading environment schemas, with GPP mocked by an httpx transport.
"""

import json

import httpx
import pytest

from graphql import build_schema, introspection_from_schema
from scripts.download_schema import SchemaDownloadError, download_schemas

FIXTURE_SDL = """
scalar Email @specifiedBy(url: "https://example.com/email")

input AngleInput @oneOf {
  degrees: Float
  "Old name."
  arcsec: Float @deprecated(reason: "Use degrees.")
}

type Query {
  angle(input: AngleInput!): Float
  contact: Email
}
"""


def _introspection() -> dict:
    return {"data": introspection_from_schema(build_schema(FIXTURE_SDL))}


class _FakeGPP:
    """
    Answers introspection like GPP; ``refuse`` lists hosts that need a token.
    """

    def __init__(self, refuse: set[str] = frozenset()):
        self.refuse = refuse
        self.requests: list[httpx.Request] = []

    def __call__(self, request: httpx.Request) -> httpx.Response:
        self.requests.append(request)
        anonymous = "authorization" not in request.headers
        if request.url.host in self.refuse and anonymous:
            return httpx.Response(401, json={"errors": [{"message": "Unauthorized"}]})
        return httpx.Response(200, json=_introspection())

    def client(self) -> httpx.Client:
        return httpx.Client(transport=httpx.MockTransport(self))


def test_downloads_development_and_production_anonymously_with_full_fidelity(tmp_path):
    gpp = _FakeGPP()

    written = download_schemas(tmp_path, http_client=gpp.client(), environ={})

    assert [path.name for path in written] == [
        "development.graphql",
        "production.graphql",
    ]
    assert [r.url.path for r in gpp.requests] == ["/odb"] * 2
    assert all("authorization" not in r.headers for r in gpp.requests)
    query = json.loads(gpp.requests[0].content)["query"]
    for flag in ("specifiedByURL", "isOneOf", "includeDeprecated: true"):
        assert flag in query
    sdl = (tmp_path / "production.graphql").read_text()
    assert "@oneOf" in sdl
    assert '@specifiedBy(url: "https://example.com/email")' in sdl
    assert 'arcsec: Float @deprecated(reason: "Use degrees.")' in sdl


def test_falls_back_to_the_token_when_anonymous_introspection_is_refused(tmp_path):
    gpp = _FakeGPP(refuse={"lucuma-postgres-odb-dev.herokuapp.com"})

    download_schemas(
        tmp_path,
        http_client=gpp.client(),
        environ={"GPP_DEVELOPMENT_TOKEN": "secret"},
    )

    development = [r for r in gpp.requests if "-dev." in r.url.host]
    assert [r.headers.get("authorization") for r in development] == [
        None,
        "Bearer secret",
    ]
    assert (tmp_path / "development.graphql").is_file()


def test_refusal_without_a_token_names_the_variable_to_set(tmp_path):
    gpp = _FakeGPP(refuse={"lucuma-postgres-odb-production.herokuapp.com"})

    with pytest.raises(SchemaDownloadError, match="GPP_TOKEN"):
        download_schemas(tmp_path, http_client=gpp.client(), environ={})


def test_downloads_only_the_named_environments(tmp_path):
    gpp = _FakeGPP()

    written = download_schemas(
        tmp_path, ["production"], http_client=gpp.client(), environ={}
    )

    assert [path.name for path in written] == ["production.graphql"]
    assert len(gpp.requests) == 1
