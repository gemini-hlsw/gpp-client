"""
Tests for downloading environment schemas, with GPP mocked by an httpx transport.
"""

import json

import httpx
import pytest
from typer.testing import CliRunner

from graphql import build_schema, introspection_from_schema, print_schema
from scripts import download_schema
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


_COMMITS = {
    "lucuma-postgres-odb-dev.herokuapp.com": "d" * 40,
    "lucuma-postgres-odb-production.herokuapp.com": "p" * 40,
}


class _FakeGPP:
    """
    Answers introspection and ``/health`` like GPP, recording introspection
    requests; ``refuse`` lists hosts that need a token, ``commits`` the commits
    each host reports in turn.
    """

    def __init__(
        self,
        refuse: set[str] = frozenset(),
        commits: dict[str, list[str]] | None = None,
    ):
        self.refuse = refuse
        self.commits = commits or {}
        self.requests: list[httpx.Request] = []

    def __call__(self, request: httpx.Request) -> httpx.Response:
        if request.url.path == "/health":
            host = request.url.host
            reported = self.commits.get(host)
            commit = reported.pop(0) if reported else _COMMITS[host]
            return httpx.Response(200, json={"status": "ok", "commit": commit})
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


def test_each_schema_starts_with_the_commit_it_was_downloaded_at(tmp_path):
    gpp = _FakeGPP()

    written = download_schemas(tmp_path, http_client=gpp.client(), environ={})

    for path, commit in zip(written, ["d" * 40, "p" * 40], strict=True):
        commit_line, body = path.read_text().split("\n", 1)
        assert commit_line == f"# schema-commit: {commit}"
        assert body == print_schema(build_schema(FIXTURE_SDL)) + "\n"


def test_refuses_a_schema_when_the_server_was_deployed_during_the_download(
    tmp_path,
):
    gpp = _FakeGPP(
        commits={"lucuma-postgres-odb-dev.herokuapp.com": ["a" * 40, "b" * 40]}
    )

    with pytest.raises(SchemaDownloadError) as raised:
        download_schemas(
            tmp_path, ["development"], http_client=gpp.client(), environ={}
        )

    assert str(raised.value) == (
        "development: the server changed from commit aaaaaaa to bbbbbbb during "
        "the download; run it again."
    )
    assert not (tmp_path / "development.graphql").exists()


@pytest.mark.parametrize(
    "health",
    [
        httpx.Response(503),
        httpx.Response(200, text="not json"),
        httpx.Response(200, json={"status": "ok"}),
    ],
    ids=["error status", "not json", "no commit"],
)
def test_fails_when_the_server_commit_cannot_be_read(tmp_path, health):
    def answer(request: httpx.Request) -> httpx.Response:
        if request.url.path == "/health":
            return health
        return httpx.Response(200, json=_introspection())

    client = httpx.Client(transport=httpx.MockTransport(answer))

    with pytest.raises(SchemaDownloadError, match=r"^development: cannot read"):
        download_schemas(tmp_path, ["development"], http_client=client, environ={})


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


def test_command_writes_into_the_package_schemas_folder_by_default(
    tmp_path, monkeypatch
):
    gpp = _FakeGPP()
    client = gpp.client()
    monkeypatch.chdir(tmp_path)
    monkeypatch.setattr(download_schema.httpx, "Client", lambda **_: client)

    result = CliRunner().invoke(download_schema.app, [])

    assert result.exit_code == 0, result.output
    schemas = tmp_path / "graphql" / "schemas"
    assert sorted(path.name for path in schemas.iterdir()) == [
        "development.graphql",
        "production.graphql",
    ]


def test_downloads_environments_given_as_a_generator(tmp_path):
    gpp = _FakeGPP()

    written = download_schemas(
        tmp_path,
        (env for env in ["development"]),
        http_client=gpp.client(),
        environ={},
    )

    assert [path.name for path in written] == ["development.graphql"]
