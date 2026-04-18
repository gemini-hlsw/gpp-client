"""
Tests for the codegen runner script.
"""

import subprocess
from subprocess import CompletedProcess

import pytest

from gpp_client.environment import GPPEnvironment
from scripts.run_codegen import (
    CodegenError,
    CodegenPaths,
    _assemble_operations,
    _collect_definition_names,
    _file_has_content,
    _get_codegen_settings,
    _get_target_package_dir,
    _iter_graphql_files,
    _load_codegen_config,
    _parse_graphql_file,
    _remove_dir,
    _run,
    _run_codegen,
    _validate_development_only_is_additive,
    _write_package_environment,
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
    Return repo codegen paths.
    """
    return CodegenPaths(root=repo_root)


@pytest.fixture()
def development_config_text():
    """
    Return a minimal development config.
    """
    return """
[tool.ariadne-codegen]
schema_path = "graphql/schemas/development.graphql"
queries_path = "build/graphql/development"
target_package_path = "src/gpp_client"
target_package_name = "generated"
client_name = "GraphQLClient"
client_file_name = "client"
""".strip()


@pytest.fixture()
def production_config_text():
    """
    Return a minimal production config.
    """
    return """
[tool.ariadne-codegen]
schema_path = "graphql/schemas/production.graphql"
queries_path = "build/graphql/production"
target_package_path = "src/gpp_client"
target_package_name = "generated"
client_name = "GraphQLClient"
client_file_name = "client"
""".strip()


@pytest.fixture()
def shared_query_text():
    """
    Return a shared query.
    """
    return "query GetObservation { observation { id } }"


@pytest.fixture()
def shared_fragment_text():
    """
    Return a shared fragment.
    """
    return "fragment ObservationFields on Observation { id }"


@pytest.fixture()
def dev_query_text():
    """
    Return a dev-only query.
    """
    return "query DevGetObservation { observation { id } }"


@pytest.fixture()
def invalid_graphql_text():
    """
    Return invalid graphql.
    """
    return "query Broken {"


@pytest.mark.parametrize(
    ("content", "expected"),
    [
        ("", False),
        ("   \n\t", False),
        ("query Ping { ping }", True),
    ],
)
def test_file_has_content(repo_root, content, expected):
    """
    File content detection works.
    """
    file_path = repo_root / "graphql/operations/development_only.graphql"
    _write_file(file_path, content)

    assert _file_has_content(file_path) is expected


def test_load_codegen_config(repo_root, development_config_text):
    """
    TOML config loads.
    """
    toml_path = repo_root / "graphql/codegen/development.toml"
    _write_file(toml_path, development_config_text)

    result = _load_codegen_config(toml_path)

    assert result["tool"]["ariadne-codegen"]["target_package_name"] == "generated"


def test_get_codegen_settings_returns_block():
    """
    Codegen settings block is returned.
    """
    config = {
        "tool": {
            "ariadne-codegen": {
                "target_package_path": "src/gpp_client",
                "target_package_name": "generated",
            }
        }
    }

    result = _get_codegen_settings(config)

    assert result["target_package_path"] == "src/gpp_client"


def test_get_codegen_settings_raises_when_missing():
    """
    Missing settings block raises.
    """
    with pytest.raises(CodegenError, match="Missing \\[tool\\.ariadne-codegen\\]"):
        _get_codegen_settings({})


def test_get_target_package_dir(repo_root):
    """
    Target package dir resolves.
    """
    result = _get_target_package_dir(
        repo_root=repo_root,
        codegen_settings={
            "target_package_path": "src/gpp_client",
            "target_package_name": "generated",
        },
    )

    assert result == (repo_root / "src/gpp_client/generated").resolve()


@pytest.mark.parametrize(
    "settings",
    [
        {"target_package_name": "generated"},
        {"target_package_path": "src/gpp_client"},
    ],
)
def test_get_target_package_dir_raises_for_missing_settings(repo_root, settings):
    """
    Missing target package settings raise.
    """
    with pytest.raises(CodegenError):
        _get_target_package_dir(
            repo_root=repo_root,
            codegen_settings=settings,
        )


def test_iter_graphql_files_returns_sorted_graphql_only(repo_root):
    """
    Graphql file discovery works.
    """
    root_dir = repo_root / "graphql/operations/shared"
    _write_file(root_dir / "b.graphql", "query B { b }")
    _write_file(root_dir / "nested/a.gql", "query A { a }")
    _write_file(root_dir / "ignore.txt", "ignore")

    result = _iter_graphql_files(root_dir)

    assert result == sorted(result)
    assert len(result) == 2
    assert all(path.suffix in {".graphql", ".gql"} for path in result)


def test_parse_graphql_file_parses_valid_document(repo_root, shared_query_text):
    """
    Valid graphql parses.
    """
    file_path = repo_root / "doc.graphql"
    _write_file(file_path, shared_query_text)

    result = _parse_graphql_file(file_path)

    assert result.definitions


def test_parse_graphql_file_raises_for_invalid_document(
    repo_root, invalid_graphql_text
):
    """
    Invalid graphql raises.
    """
    file_path = repo_root / "broken.graphql"
    _write_file(file_path, invalid_graphql_text)

    with pytest.raises(CodegenError, match="Failed to parse GraphQL file"):
        _parse_graphql_file(file_path)


def test_collect_definition_names_collects_operations_and_fragments(
    repo_root,
    shared_query_text,
    shared_fragment_text,
):
    """
    Definition names are collected.
    """
    query_path = repo_root / "one.graphql"
    fragment_path = repo_root / "two.graphql"
    _write_file(query_path, shared_query_text)
    _write_file(fragment_path, shared_fragment_text)

    result = _collect_definition_names([query_path, fragment_path])

    assert result["GetObservation"] == query_path
    assert result["ObservationFields"] == fragment_path


def test_collect_definition_names_raises_for_duplicate_operation_name(repo_root):
    """
    Duplicate operation names raise.
    """
    first = repo_root / "one.graphql"
    second = repo_root / "two.graphql"
    _write_file(first, "query GetObservation { observation { id } }")
    _write_file(second, "query GetObservation { observation { title } }")

    with pytest.raises(CodegenError, match="Duplicate GraphQL definition name found"):
        _collect_definition_names([first, second])


def test_collect_definition_names_raises_for_duplicate_fragment_name(repo_root):
    """
    Duplicate fragment names raise.
    """
    first = repo_root / "one.graphql"
    second = repo_root / "two.graphql"
    _write_file(first, "fragment ObservationFields on Observation { id }")
    _write_file(second, "fragment ObservationFields on Observation { title }")

    with pytest.raises(CodegenError, match="Duplicate GraphQL definition name found"):
        _collect_definition_names([first, second])


def test_validate_development_only_is_additive_skips_missing_file(
    paths, shared_query_text
):
    """
    Missing dev-only file is skipped.
    """
    _write_file(
        paths.shared_operations_dir / "domains/observation/queries.graphql",
        shared_query_text,
    )

    _validate_development_only_is_additive(paths)


def test_validate_development_only_is_additive_skips_empty_file(
    paths, shared_query_text
):
    """
    Empty dev-only file is skipped.
    """
    _write_file(
        paths.shared_operations_dir / "domains/observation/queries.graphql",
        shared_query_text,
    )
    _write_file(paths.development_only_path, "  \n\t")

    _validate_development_only_is_additive(paths)


def test_validate_development_only_is_additive_passes_for_unique_names(
    paths,
    shared_query_text,
    dev_query_text,
):
    """
    Unique shared and dev-only names pass.
    """
    _write_file(
        paths.shared_operations_dir / "domains/observation/queries.graphql",
        shared_query_text,
    )
    _write_file(paths.development_only_path, dev_query_text)

    _validate_development_only_is_additive(paths)


@pytest.mark.parametrize(
    ("shared_content", "dev_content", "name"),
    [
        (
            "query GetObservation { observation { id } }",
            "query GetObservation { observation { title } }",
            "GetObservation",
        ),
        (
            "fragment ObservationFields on Observation { id }",
            "fragment ObservationFields on Observation { title }",
            "ObservationFields",
        ),
    ],
)
def test_validate_development_only_is_additive_raises_for_collisions(
    paths,
    shared_content,
    dev_content,
    name,
):
    """
    Collisions between shared and dev-only raise.
    """
    _write_file(
        paths.shared_operations_dir / "domains/observation/queries.graphql",
        shared_content,
    )
    _write_file(paths.development_only_path, dev_content)

    with pytest.raises(CodegenError, match=name):
        _validate_development_only_is_additive(paths)


def test_assemble_operations_raises_when_shared_dir_missing(paths):
    """
    Missing shared operations dir raises.
    """
    with pytest.raises(CodegenError, match="Shared operations directory not found"):
        _assemble_operations(paths, GPPEnvironment.PRODUCTION)


@pytest.mark.parametrize(
    ("env", "expect_dev_only"),
    [
        (GPPEnvironment.PRODUCTION, False),
        (GPPEnvironment.DEVELOPMENT, True),
    ],
)
def test_assemble_operations_copies_expected_files(
    paths,
    shared_query_text,
    dev_query_text,
    env,
    expect_dev_only,
):
    """
    Operations are assembled for each environment.
    """
    _write_file(
        paths.shared_operations_dir / "domains/observation/queries.graphql",
        shared_query_text,
    )
    _write_file(
        paths.shared_operations_dir / "fragments.graphql",
        "fragment SharedRootFields on Query { __typename }",
    )
    _write_file(paths.development_only_path, dev_query_text)

    assembled_dir = _assemble_operations(paths, env)

    assert (assembled_dir / "domains/observation/queries.graphql").exists()
    assert (assembled_dir / "fragments.graphql").exists()
    assert (assembled_dir / "development_only.graphql").exists() is expect_dev_only


def test_remove_dir_removes_existing_directory(repo_root):
    """
    Directory removal works.
    """
    path = repo_root / "build/graphql/development"
    _write_file(path / "queries.graphql", "query Ping { ping }")

    assert path.is_dir()

    _remove_dir(path, label="test directory")

    assert not path.exists()


def test_remove_dir_ignores_missing_directory(repo_root):
    """
    Missing directory removal is ignored.
    """
    path = repo_root / "does/not/exist"

    _remove_dir(path, label="missing directory")

    assert not path.exists()


def test_write_package_environment_creates_file(paths):
    """
    Package environment file is written.
    """
    package_dir = paths.root / "src/gpp_client/generated"
    package_dir.mkdir(parents=True)

    _write_package_environment(package_dir, GPPEnvironment.DEVELOPMENT)

    content = (package_dir / "package_environment.py").read_text(encoding="utf-8")

    assert 'PACKAGE_ENVIRONMENT = "DEVELOPMENT"' in content


def test_write_package_environment_raises_for_missing_dir(paths):
    """
    Missing package dir raises.
    """
    package_dir = paths.root / "src/gpp_client/generated"

    with pytest.raises(CodegenError, match="Generated package directory not found"):
        _write_package_environment(package_dir, GPPEnvironment.DEVELOPMENT)


def test_run_codegen_calls_subprocess(repo_root, development_config_text, mocker):
    """
    Codegen subprocess is called.
    """
    toml_path = repo_root / "graphql/codegen/development.toml"
    _write_file(toml_path, development_config_text)

    run_spy = mocker.patch(
        "scripts.run_codegen.subprocess.run",
        return_value=CompletedProcess(
            args=["ariadne-codegen", "--config", str(toml_path)],
            returncode=0,
            stdout="generated",
            stderr="",
        ),
    )

    _run_codegen(toml_path)

    run_spy.assert_called_once_with(
        ["ariadne-codegen", "--config", str(toml_path)],
        check=True,
        capture_output=True,
        text=True,
    )


def test_run_codegen_raises_on_subprocess_failure(
    repo_root, development_config_text, mocker
):
    """
    Codegen subprocess failure raises.
    """
    toml_path = repo_root / "graphql/codegen/development.toml"
    _write_file(toml_path, development_config_text)

    error = subprocess.CalledProcessError(
        returncode=1,
        cmd=["ariadne-codegen", "--config", str(toml_path)],
        stderr="boom",
        output="partial output",
    )

    mocker.patch("scripts.run_codegen.subprocess.run", side_effect=error)

    with pytest.raises(CodegenError, match="boom"):
        _run_codegen(toml_path)


@pytest.mark.parametrize(
    ("env", "toml_name", "schema_name"),
    [
        (GPPEnvironment.DEVELOPMENT, "development.toml", "development.graphql"),
        (GPPEnvironment.PRODUCTION, "production.toml", "production.graphql"),
    ],
)
def test_run_executes_full_workflow(
    paths,
    mocker,
    shared_query_text,
    dev_query_text,
    env,
    toml_name,
    schema_name,
):
    """
    Full workflow runs successfully.
    """
    config_text = f"""
[tool.ariadne-codegen]
schema_path = "graphql/schemas/{schema_name}"
queries_path = "build/graphql/{env.value.lower()}"
target_package_path = "src/gpp_client"
target_package_name = "generated"
client_name = "GraphQLClient"
client_file_name = "client"
""".strip()

    _write_file(paths.codegen_dir / toml_name, config_text)
    _write_file(
        paths.graphql_dir / "schemas" / schema_name, "type Query { ping: String }"
    )
    _write_file(
        paths.shared_operations_dir / "domains/utils/queries.graphql",
        shared_query_text,
    )
    _write_file(paths.root / "build/old.txt", "stale build")
    _write_file(paths.root / "src/gpp_client/generated/stale.py", "stale generated")

    if env is GPPEnvironment.DEVELOPMENT:
        _write_file(paths.development_only_path, dev_query_text)

    def mock_run(*args, **kwargs):
        generated_dir = paths.root / "src/gpp_client/generated"
        generated_dir.mkdir(parents=True, exist_ok=True)
        (generated_dir / "client.py").write_text(
            "class GraphQLClient: ...",
            encoding="utf-8",
        )
        return CompletedProcess(
            args=args[0],
            returncode=0,
            stdout="generated",
            stderr="",
        )

    run_spy = mocker.patch(
        "scripts.run_codegen.subprocess.run",
        side_effect=mock_run,
    )

    _run(env)

    run_spy.assert_called_once_with(
        ["ariadne-codegen", "--config", str(paths.codegen_toml_path(env))],
        check=True,
        capture_output=True,
        text=True,
    )
    assert (paths.build_operations_dir(env) / "domains/utils/queries.graphql").exists()
    assert not (paths.root / "build/old.txt").exists()
    assert not (paths.root / "src/gpp_client/generated/stale.py").exists()
    assert (paths.root / "src/gpp_client/generated/package_environment.py").exists()

    if env is GPPEnvironment.DEVELOPMENT:
        assert (paths.build_operations_dir(env) / "development_only.graphql").exists()
    else:
        assert not (
            paths.build_operations_dir(env) / "development_only.graphql"
        ).exists()


def test_run_raises_when_codegen_config_is_missing(paths):
    """
    Missing codegen config raises.
    """
    with pytest.raises(CodegenError, match="Codegen config file not found"):
        _run(GPPEnvironment.DEVELOPMENT)


def test_run_raises_when_dev_only_collides(paths, development_config_text):
    """
    Dev-only collisions fail the workflow.
    """
    _write_file(paths.codegen_dir / "development.toml", development_config_text)
    _write_file(
        paths.shared_operations_dir / "domains/observation/queries.graphql",
        "query GetObservation { observation { id } }",
    )
    _write_file(
        paths.development_only_path,
        "query GetObservation { observation { title } }",
    )

    with pytest.raises(CodegenError, match="Development-only GraphQL must be additive"):
        _run(GPPEnvironment.DEVELOPMENT)
