"""
Tests for release validation, driven through ``validate_release``.
"""

import shutil
import sys
from pathlib import Path

import pytest

from scripts.build_client import BuildPaths, build
from scripts.validate_release import ReleaseValidationError, main, validate_release

REPO_ROOT = Path(__file__).resolve().parents[2]

_SCHEMA = "type Query { program: Program }\ntype Program { id: ID! name: String }\n"
_OPERATION = "query getProgram { program { id name } }\n"


def _committed_build(root: Path) -> BuildPaths:
    """
    Return a checkout whose generated code is a fresh build of its schemas.
    """
    schemas_dir = root / "graphql" / "schemas"
    schemas_dir.mkdir(parents=True)
    for environment in ("development", "production"):
        (schemas_dir / f"{environment}.graphql").write_text(_SCHEMA)
    operations_dir = root / "graphql" / "operations"
    operations_dir.mkdir(parents=True)
    (operations_dir / "operations.graphql").write_text(_OPERATION)
    shutil.copyfile(
        REPO_ROOT / "graphql" / "codegen.toml", root / "graphql" / "codegen.toml"
    )
    paths = BuildPaths.for_repo(root)
    build(paths)
    return paths


def test_accepts_a_tag_when_generated_code_matches_a_fresh_build(tmp_path):
    paths = _committed_build(tmp_path)

    validate_release("v26.5.0", paths)


def test_refuses_a_tag_when_generated_code_differs_from_a_fresh_build(tmp_path):
    paths = _committed_build(tmp_path)
    client = paths.package_dir / "client.py"
    client.write_text(client.read_text() + "\n# edited by hand\n")

    with pytest.raises(ReleaseValidationError) as exc_info:
        validate_release("v26.5.0", paths)

    assert "client.py" in str(exc_info.value)


@pytest.mark.parametrize("tag", ["v26.5.0.dev1", "v26.12.3.dev12"])
def test_refuses_a_dev_tag_explaining_the_single_stream(tmp_path, tag):
    paths = _committed_build(tmp_path)

    with pytest.raises(ReleaseValidationError, match="one stream"):
        validate_release(tag, paths)


@pytest.mark.parametrize(
    "tag",
    [
        "",
        "26.5.0",
        "v2026.5.0",
        "v26.05.0",
        "v26.13.0",
        "v26.5",
        "v26.5.0.1",
        "v26.5.0-dev.1",
        "v26.5.0.dev",
        "v26.5.0rc1",
        "release-v26.5.0",
    ],
)
def test_refuses_a_tag_that_is_not_calver(tmp_path, tag):
    paths = _committed_build(tmp_path)

    with pytest.raises(ReleaseValidationError, match="Invalid release tag"):
        validate_release(tag, paths)


def test_refuses_when_a_schema_changed_without_rebuilding(tmp_path):
    paths = _committed_build(tmp_path)
    paths.schema_path("production").write_text(_SCHEMA + "type Extra { id: ID! }\n")

    with pytest.raises(ReleaseValidationError) as exc_info:
        validate_release("v26.5.0", paths)

    assert "merged.graphql" in str(exc_info.value)


def test_refuses_when_an_operation_changed_without_rebuilding(tmp_path):
    paths = _committed_build(tmp_path)
    (paths.operations_dir / "operations.graphql").write_text(
        "query getProgram { program { id } }\n"
    )

    with pytest.raises(ReleaseValidationError, match="get_program.py"):
        validate_release("v26.5.0", paths)


def test_refuses_when_llms_txt_differs_from_a_fresh_build(tmp_path):
    paths = _committed_build(tmp_path)
    paths.llms_txt.write_text(paths.llms_txt.read_text() + "\nedited by hand\n")

    with pytest.raises(ReleaseValidationError, match="differs: .*llms.txt"):
        validate_release("v26.5.0", paths)


def test_refuses_when_llms_txt_is_missing(tmp_path):
    paths = _committed_build(tmp_path)
    paths.llms_txt.unlink()

    with pytest.raises(ReleaseValidationError, match="missing: .*llms.txt"):
        validate_release("v26.5.0", paths)


def test_refuses_a_stray_file_in_the_generated_package(tmp_path):
    paths = _committed_build(tmp_path)
    (paths.package_dir / "stale_operation.py").write_text("")

    with pytest.raises(ReleaseValidationError, match="stale_operation.py"):
        validate_release("v26.5.0", paths)


def test_refuses_a_generated_file_that_is_missing(tmp_path):
    paths = _committed_build(tmp_path)
    (paths.package_dir / "client.py").unlink()

    with pytest.raises(ReleaseValidationError, match="missing: .*client.py"):
        validate_release("v26.5.0", paths)


def test_ignores_bytecode_caches(tmp_path):
    paths = _committed_build(tmp_path)
    cache = paths.package_dir / "__pycache__"
    cache.mkdir()
    (cache / "client.cpython-311.pyc").write_bytes(b"\0")

    validate_release("v26.5.0", paths)


def test_refuses_when_the_build_fails(tmp_path):
    paths = _committed_build(tmp_path)
    paths.schema_path("production").unlink()

    with pytest.raises(ReleaseValidationError, match="production.graphql"):
        validate_release("v26.5.0", paths)


def test_leaves_the_checkout_unchanged(tmp_path):
    paths = _committed_build(tmp_path)
    client = paths.package_dir / "client.py"
    edited = client.read_text() + "\n# edited by hand\n"
    client.write_text(edited)

    with pytest.raises(ReleaseValidationError):
        validate_release("v26.5.0", paths)

    assert client.read_text() == edited


def test_command_validates_the_checkout_in_the_current_directory(
    tmp_path, monkeypatch, capsys
):
    _committed_build(tmp_path)
    monkeypatch.chdir(tmp_path)
    monkeypatch.setattr(sys, "argv", ["validate_release", "v26.5.0.dev1"])

    with pytest.raises(SystemExit) as exc_info:
        main()

    assert exc_info.value.code == 1
    assert "one stream" in capsys.readouterr().err


def test_command_accepts_a_matching_checkout(tmp_path, monkeypatch):
    _committed_build(tmp_path)
    monkeypatch.chdir(tmp_path)
    monkeypatch.setattr(sys, "argv", ["validate_release", "v26.5.0"])

    main()
