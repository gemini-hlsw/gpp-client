"""
Tests for the schema download script.
"""

from pathlib import Path
from subprocess import CalledProcessError, CompletedProcess

import pytest

from gpp_client.environment import GPPEnvironment
from scripts.download_schema import (
    SchemaDownloadError,
    SchemaPaths,
    _download_schema,
    _get_token,
    _run,
    _write_schema,
)


def _write_file(path, content):
    """
    Write a file and create parents.
    """
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(content, encoding="utf-8")


@pytest.fixture()
def repo_root(tmp_path, monkeypatch):
    """
    Create and switch to a temp repo.
    """
    monkeypatch.chdir(tmp_path)
    return tmp_path


@pytest.fixture()
def paths(repo_root):
    """
    Return schema paths for temp repo.
    """
    return SchemaPaths(root=repo_root)


def test_schema_file_path(paths):
    """
    Schema path resolves correctly.
    """
    result = paths.schema_file_path(GPPEnvironment.DEVELOPMENT)

    assert result == paths.root / "graphql" / "schemas" / "development.graphql"


def test_write_schema_creates_parent_dirs_and_file(paths):
    """
    Schema text is written to disk.
    """
    output_file = paths.schema_file_path(GPPEnvironment.DEVELOPMENT)

    _write_schema("type Query { ping: String }", output_file)

    assert output_file.exists()
    assert output_file.read_text(encoding="utf-8") == "type Query { ping: String }"


def test_get_token_returns_resolved_token_and_environment(mocker):
    """
    Token resolution succeeds.
    """
    settings_mock = mocker.Mock()
    settings_mock.resolved_token = "secret-token"
    settings_mock.environment = GPPEnvironment.DEVELOPMENT

    settings_cls = mocker.patch(
        "scripts.download_schema.GPPSettings",
        return_value=settings_mock,
    )

    token, environment = _get_token(GPPEnvironment.DEVELOPMENT)

    settings_cls.assert_called_once_with(
        environment_override=GPPEnvironment.DEVELOPMENT
    )
    assert token == "secret-token"
    assert environment is GPPEnvironment.DEVELOPMENT


def test_get_token_raises_schema_download_error_for_gpp_auth_error(mocker):
    """
    GPP auth errors are wrapped.
    """
    from gpp_client.exceptions import GPPAuthError

    mocker.patch(
        "scripts.download_schema.GPPSettings",
        side_effect=GPPAuthError("missing token"),
    )

    with pytest.raises(SchemaDownloadError, match="missing token"):
        _get_token(GPPEnvironment.DEVELOPMENT)


def test_download_schema_calls_subprocess(mocker):
    """
    Schema download calls gql-cli.
    """
    run_spy = mocker.patch(
        "scripts.download_schema.subprocess.run",
        return_value=CompletedProcess(
            args=["gql-cli"],
            returncode=0,
            stdout="type Query { ping: String }",
            stderr="",
        ),
    )

    result = _download_schema("https://example.test/odb", "secret")

    assert result == "type Query { ping: String }"
    run_spy.assert_called_once_with(
        [
            "gql-cli",
            "https://example.test/odb",
            "--transport",
            "aiohttp",
            "--print-schema",
            "--schema-download",
            "input_value_deprecation:true",
            "-H",
            "Authorization: Bearer secret",
        ],
        check=True,
        capture_output=True,
        text=True,
        cwd=Path.cwd(),
    )


@pytest.mark.parametrize(
    ("stderr", "expected"),
    [
        ("permission denied", "permission denied"),
        ("", "Schema download failed."),
        (None, "Schema download failed."),
    ],
)
def test_download_schema_raises_schema_download_error_on_subprocess_failure(
    mocker,
    stderr,
    expected,
):
    """
    Subprocess failures are wrapped.
    """
    error = CalledProcessError(
        returncode=1,
        cmd=["gql-cli"],
        stderr=stderr,
        output="partial",
    )

    mocker.patch("scripts.download_schema.subprocess.run", side_effect=error)

    with pytest.raises(SchemaDownloadError, match=expected):
        _download_schema("https://example.test/odb", "secret")


def test_run_downloads_and_writes_schema(repo_root, paths, mocker):
    """
    Full workflow downloads and writes schema.
    """
    settings_mock = mocker.Mock()
    settings_mock.resolved_token = "secret-token"
    settings_mock.environment = GPPEnvironment.DEVELOPMENT

    mocker.patch("scripts.download_schema.GPPSettings", return_value=settings_mock)
    get_graphql_url = mocker.patch(
        "scripts.download_schema.get_graphql_url",
        return_value="https://example.test/odb",
    )
    download_schema = mocker.patch(
        "scripts.download_schema._download_schema",
        return_value="type Query { ping: String }",
    )

    _run(GPPEnvironment.DEVELOPMENT)

    get_graphql_url.assert_called_once_with(GPPEnvironment.DEVELOPMENT)
    download_schema.assert_called_once_with(
        "https://example.test/odb",
        "secret-token",
    )

    output_file = paths.schema_file_path(GPPEnvironment.DEVELOPMENT)
    assert output_file.exists()
    assert output_file.read_text(encoding="utf-8") == "type Query { ping: String }"


def test_run_uses_effective_environment_for_url_lookup(repo_root, paths, mocker):
    """
    Effective environment is used for URL lookup.
    """
    settings_mock = mocker.Mock()
    settings_mock.resolved_token = "secret-token"
    settings_mock.environment = GPPEnvironment.PRODUCTION

    mocker.patch("scripts.download_schema.GPPSettings", return_value=settings_mock)
    get_graphql_url = mocker.patch(
        "scripts.download_schema.get_graphql_url",
        return_value="https://example.test/prod/odb",
    )
    mocker.patch(
        "scripts.download_schema._download_schema",
        return_value="type Query { ping: String }",
    )

    _run(GPPEnvironment.DEVELOPMENT)

    get_graphql_url.assert_called_once_with(GPPEnvironment.PRODUCTION)

    output_file = paths.schema_file_path(GPPEnvironment.DEVELOPMENT)
    assert output_file.exists()


@pytest.mark.parametrize(
    "side_effect",
    [
        SchemaDownloadError("token failure"),
        SchemaDownloadError("download failure"),
    ],
)
def test_run_propagates_schema_download_error(repo_root, mocker, side_effect):
    """
    Workflow propagates download errors.
    """
    mocker.patch("scripts.download_schema._get_token", side_effect=side_effect)

    with pytest.raises(SchemaDownloadError, match=str(side_effect)):
        _run(GPPEnvironment.DEVELOPMENT)
