"""
Tests for the one-command schema update, with GPP mocked by an httpx transport.
"""

import shutil
from datetime import UTC, datetime
from pathlib import Path

import httpx
import pytest
from typer.testing import CliRunner

from graphql import build_schema, introspection_from_schema, print_schema
from scripts import schema_update as schema_update_script
from scripts.build_client import BuildPaths
from scripts.download_schema import SchemaDownloadError
from scripts.schema_update import schema_update

REPO_ROOT = Path(__file__).resolve().parents[2]

_SCHEMA = "type Query { program: Program }\ntype Program { id: ID! name: String }\n"
_SCHEMA_WITH_REFERENCE = (
    "type Query { program: Program }\n"
    "type Program { id: ID! name: String reference: String }\n"
)
_OPERATION = "query getProgram { program { id name } }\n"


def _printed(sdl: str) -> str:
    return print_schema(build_schema(sdl)) + "\n"


def _dated(sdl: str) -> str:
    """
    Return ``sdl`` as a download writes it today.
    """
    return f"# schema-date: {datetime.now(UTC).date().isoformat()}\n" + _printed(sdl)


def _introspection(sdl: str) -> dict:
    return {"data": introspection_from_schema(build_schema(sdl))}


def _introspection_that_does_not_build() -> dict:
    """
    Return an introspection whose ``Query.program`` names a type it lacks.
    """
    body = _introspection(_SCHEMA)
    for type_ in body["data"]["__schema"]["types"]:
        if type_["name"] == "Program":
            type_["name"] = "Missing"
    return body


class _FakeGPP:
    """
    Answers introspection per environment with the given body.
    """

    def __init__(self, *, development: dict, production: dict):
        self.bodies = {"development": development, "production": production}
        self.requests: list[httpx.Request] = []

    def __call__(self, request: httpx.Request) -> httpx.Response:
        self.requests.append(request)
        environment = "development" if "-dev." in request.url.host else "production"
        return httpx.Response(200, json=self.bodies[environment])

    def client(self) -> httpx.Client:
        return httpx.Client(transport=httpx.MockTransport(self))


def _checkout(root: Path) -> BuildPaths:
    """
    Return a checkout whose committed schemas are ``_SCHEMA`` on both environments.
    """
    paths = BuildPaths.for_repo(root)
    paths.schemas_dir.mkdir(parents=True)
    for environment in ("development", "production"):
        paths.schema_path(environment).write_text(_printed(_SCHEMA))
    paths.operations_dir.mkdir(parents=True)
    (paths.operations_dir / "operations.graphql").write_text(_OPERATION)
    shutil.copyfile(REPO_ROOT / "graphql" / "codegen.toml", paths.codegen_config)
    return paths


def test_environment_whose_schema_does_not_build_is_held_and_named(tmp_path):
    paths = _checkout(tmp_path)
    gpp = _FakeGPP(
        development=_introspection_that_does_not_build(),
        production=_introspection(_SCHEMA_WITH_REFERENCE),
    )

    result = schema_update(
        paths, http_client=gpp.client(), environ={}, run_suite=lambda: 0
    )

    assert paths.schema_path("development").read_text() == _printed(_SCHEMA)
    assert paths.schema_path("production").read_text() == _dated(_SCHEMA_WITH_REFERENCE)
    assert result.held == ("development",)
    assert "Development: held" in result.summary
    assert "unknown type: Program" in result.summary


def test_second_run_without_a_gpp_change_changes_nothing(tmp_path):
    paths = _checkout(tmp_path)
    gpp = _FakeGPP(
        development=_introspection(_SCHEMA_WITH_REFERENCE),
        production=_introspection(_SCHEMA),
    )
    first = schema_update(
        paths, http_client=gpp.client(), environ={}, run_suite=lambda: 0
    )
    before = {
        path: path.read_text()
        for path in [*paths.schemas_dir.iterdir(), *paths.package_dir.rglob("*.py")]
    }

    second = schema_update(
        paths, http_client=gpp.client(), environ={}, run_suite=lambda: 0
    )

    assert first.changed == ("development",)
    assert second.changed == ()
    assert {path: path.read_text() for path in before} == before
    assert "- Development: unchanged\n- Production: unchanged" in second.summary


def test_a_later_day_without_a_gpp_change_keeps_the_committed_schema_date(tmp_path):
    paths = _checkout(tmp_path)
    dated_earlier = "# schema-date: 2026-01-01\n" + _printed(_SCHEMA)
    paths.schema_path("production").write_text(dated_earlier)
    gpp = _FakeGPP(
        development=_introspection(_SCHEMA), production=_introspection(_SCHEMA)
    )

    result = schema_update(
        paths, http_client=gpp.client(), environ={}, run_suite=lambda: 0
    )

    assert result.changed == ()
    assert paths.schema_path("production").read_text() == dated_earlier
    assert paths.schema_path("development").read_text() == _printed(_SCHEMA)


def test_runs_the_suite_on_the_built_client_and_reports_a_failure(tmp_path):
    paths = _checkout(tmp_path)
    gpp = _FakeGPP(
        development=_introspection(_SCHEMA), production=_introspection(_SCHEMA)
    )
    built_when_run = []

    def run_suite() -> int:
        built_when_run.append((paths.package_dir / "client.py").is_file())
        return 1

    result = schema_update(
        paths, http_client=gpp.client(), environ={}, run_suite=run_suite
    )

    assert built_when_run == [True]
    assert result.suite_passed is False


def test_command_updates_the_checkout_in_the_current_directory(tmp_path, monkeypatch):
    paths = _checkout(tmp_path)
    gpp = _FakeGPP(
        development=_introspection(_SCHEMA_WITH_REFERENCE),
        production=_introspection(_SCHEMA),
    )
    client = gpp.client()
    monkeypatch.chdir(tmp_path)
    monkeypatch.setattr(schema_update_script.httpx, "Client", lambda **_: client)
    monkeypatch.setattr(schema_update_script, "_run_pytest", lambda: 1)

    result = CliRunner().invoke(schema_update_script.app, [])

    assert result.exit_code == 1, result.output
    assert paths.schema_path("development").read_text() == _dated(
        _SCHEMA_WITH_REFERENCE
    )
    assert (paths.package_dir / "client.py").is_file()
    assert "- Development: changed\n- Production: unchanged" in result.output
    assert "### Merge summary" in result.output
    assert "Tests failed" in result.output


def test_a_refused_introspection_fails_the_update_instead_of_holding(tmp_path):
    paths = _checkout(tmp_path)
    gpp = _FakeGPP(
        development=_introspection(_SCHEMA), production=_introspection(_SCHEMA)
    )
    refusing = httpx.Client(
        transport=httpx.MockTransport(
            lambda request: (
                httpx.Response(401, json={"errors": [{}]})
                if "-dev." in request.url.host
                else gpp(request)
            )
        )
    )

    with pytest.raises(SchemaDownloadError, match="GPP_DEVELOPMENT_TOKEN"):
        schema_update(paths, http_client=refusing, environ={}, run_suite=lambda: 0)

    assert paths.schema_path("development").read_text() == _printed(_SCHEMA)
