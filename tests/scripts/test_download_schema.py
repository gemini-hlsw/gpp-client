"""
Tests for the schema download script.
"""

from contextlib import nullcontext
from pathlib import Path
from subprocess import CalledProcessError, CompletedProcess

import pytest
from typer.testing import CliRunner

from gpp_client.constants import DEVELOPMENT_TOKEN_ENV_VAR, TOKEN_ENV_VAR
from gpp_client.environment import GPPEnvironment
from scripts.download_schema import (
    SchemaDownloadError,
    SchemaPaths,
    _required_token_env_var,
    _run,
    _run_schema_download,
    _validate_token_env_var,
    app,
)


def _touch_file(path):
    """
    Create a file and parent directories.
    """
    path.parent.mkdir(parents=True, exist_ok=True)
    path.touch()


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


@pytest.fixture()
def runner():
    """
    Return a Typer CLI runner.
    """
    return CliRunner()


@pytest.fixture(autouse=True)
def mock_output(mocker):
    """
    Mock CLI output helpers.
    """
    mocker.patch("scripts.download_schema.output.status", return_value=nullcontext())
    mocker.patch("scripts.download_schema.output.info")
    mocker.patch("scripts.download_schema.output.dim_info")
    mocker.patch("scripts.download_schema.output.success")
    mocker.patch("scripts.download_schema.output.fail")


@pytest.mark.parametrize(
    ("env", "expected_filename"),
    [
        (GPPEnvironment.DEVELOPMENT, "development.toml"),
        (GPPEnvironment.PRODUCTION, "production.toml"),
    ],
)
def test_schema_toml_path(paths, env, expected_filename):
    """
    Schema TOML path resolves correctly.
    """
    result = paths.schema_toml_path(env)

    assert result == paths.root / "graphql" / "schemas" / expected_filename


@pytest.mark.parametrize(
    ("env", "expected_env_var"),
    [
        (GPPEnvironment.DEVELOPMENT, DEVELOPMENT_TOKEN_ENV_VAR),
        (GPPEnvironment.PRODUCTION, TOKEN_ENV_VAR),
    ],
)
def test_required_token_env_var(env, expected_env_var):
    """
    Required token environment variable resolves correctly.
    """
    result = _required_token_env_var(env)

    assert result == expected_env_var


@pytest.mark.parametrize(
    ("env", "env_var"),
    [
        (GPPEnvironment.DEVELOPMENT, DEVELOPMENT_TOKEN_ENV_VAR),
        (GPPEnvironment.PRODUCTION, TOKEN_ENV_VAR),
    ],
)
def test_validate_token_env_var_succeeds(monkeypatch, env, env_var):
    """
    Existing token environment variable succeeds.
    """
    monkeypatch.setenv(env_var, "secret-token")

    _validate_token_env_var(env)


@pytest.mark.parametrize(
    ("env", "env_var"),
    [
        (GPPEnvironment.DEVELOPMENT, DEVELOPMENT_TOKEN_ENV_VAR),
        (GPPEnvironment.PRODUCTION, TOKEN_ENV_VAR),
    ],
)
def test_validate_token_env_var_raises_for_missing_token(monkeypatch, env, env_var):
    """
    Missing token environment variable raises an error.
    """
    monkeypatch.delenv(env_var, raising=False)

    with pytest.raises(SchemaDownloadError, match=env_var):
        _validate_token_env_var(env)


def test_run_schema_download_calls_ariadne_codegen(repo_root, mocker):
    """
    Schema download calls Ariadne Codegen.
    """
    toml_path = Path("/fake/development.toml")

    run_spy = mocker.patch(
        "scripts.download_schema.subprocess.run",
        return_value=CompletedProcess(
            args=["ariadne-codegen"],
            returncode=0,
            stdout="schema downloaded",
            stderr="",
        ),
    )

    _run_schema_download(toml_path)

    run_spy.assert_called_once_with(
        [
            "ariadne-codegen",
            "graphqlschema",
            "--config",
            str(toml_path),
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
def test_run_schema_download_raises_schema_download_error_on_subprocess_failure(
    repo_root,
    mocker,
    stderr,
    expected,
):
    """
    Subprocess failures are wrapped.
    """
    toml_path = Path("/fake/development.toml")

    error = CalledProcessError(
        returncode=1,
        cmd=["ariadne-codegen"],
        stderr=stderr,
        output="partial output",
    )

    mocker.patch("scripts.download_schema.subprocess.run", side_effect=error)

    with pytest.raises(SchemaDownloadError, match=expected):
        _run_schema_download(toml_path)


def test_run_raises_when_config_file_missing(repo_root):
    """
    Workflow fails when the environment config file is missing.
    """
    with pytest.raises(
        SchemaDownloadError,
        match="Schema config file not found",
    ):
        _run(GPPEnvironment.DEVELOPMENT)


def test_run_raises_when_token_is_missing(repo_root, monkeypatch):
    """
    Workflow fails when the required token is missing.
    """
    toml_path = repo_root / "graphql" / "schemas" / "development.toml"
    _touch_file(toml_path)
    monkeypatch.delenv(DEVELOPMENT_TOKEN_ENV_VAR, raising=False)

    with pytest.raises(
        SchemaDownloadError,
        match=DEVELOPMENT_TOKEN_ENV_VAR,
    ):
        _run(GPPEnvironment.DEVELOPMENT)


def test_run_downloads_schema_when_config_and_token_exist(
    repo_root,
    mocker,
    monkeypatch,
):
    """
    Full workflow invokes schema download.
    """
    toml_path = repo_root / "graphql" / "schemas" / "development.toml"
    _touch_file(toml_path)
    monkeypatch.setenv(DEVELOPMENT_TOKEN_ENV_VAR, "secret-token")

    download_spy = mocker.patch("scripts.download_schema._run_schema_download")

    _run(GPPEnvironment.DEVELOPMENT)

    download_spy.assert_called_once_with(toml_path)


@pytest.mark.parametrize(
    "side_effect",
    [
        SchemaDownloadError("download failure"),
        SchemaDownloadError("invalid config"),
    ],
)
def test_run_propagates_schema_download_error(
    repo_root,
    mocker,
    monkeypatch,
    side_effect,
):
    """
    Workflow propagates schema download errors.
    """
    toml_path = repo_root / "graphql" / "schemas" / "development.toml"
    _touch_file(toml_path)
    monkeypatch.setenv(DEVELOPMENT_TOKEN_ENV_VAR, "secret-token")

    mocker.patch(
        "scripts.download_schema._run_schema_download",
        side_effect=side_effect,
    )

    with pytest.raises(SchemaDownloadError, match=str(side_effect)):
        _run(GPPEnvironment.DEVELOPMENT)


def test_cli_success(repo_root, runner, mocker, monkeypatch):
    """
    CLI exits successfully when schema download succeeds.
    """
    toml_path = repo_root / "graphql" / "schemas" / "development.toml"
    _touch_file(toml_path)
    monkeypatch.setenv(DEVELOPMENT_TOKEN_ENV_VAR, "secret-token")

    mocker.patch("scripts.download_schema._run_schema_download")

    result = runner.invoke(app, [GPPEnvironment.DEVELOPMENT.value.lower()])

    assert result.exit_code == 0


def test_cli_failure(runner, mocker):
    """
    CLI exits with error when schema download fails.
    """
    mocker.patch(
        "scripts.download_schema._run",
        side_effect=SchemaDownloadError("Bad schema config"),
    )

    result = runner.invoke(app, [GPPEnvironment.DEVELOPMENT.value.lower()])

    assert result.exit_code == 1
