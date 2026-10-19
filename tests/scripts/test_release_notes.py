"""
Tests for the release-note availability lists, driven through ``release_notes``.
"""

import subprocess

from typer.testing import CliRunner

from scripts.release_notes import app, release_notes

_DEV = '@environments(names: ["development"])'
_PROD = '@environments(names: ["production"])'


def test_promoted_field_is_new_on_production_only():
    old = (
        f"type Query {{ a: Int }}\ntype Program {{ id: ID! reference: String {_DEV} }}"
    )
    new = "type Query { a: Int }\ntype Program { id: ID! reference: String }"

    assert release_notes(old, new) == (
        "### Availability changes\n\n**production**\n- New: `Program.reference`\n"
    )


def test_field_development_drops_is_removed_there_and_now_leaving_production():
    old = "type Query { a: Int }\ntype Program { id: ID! legacy: Int }"
    new = f"type Query {{ a: Int }}\ntype Program {{ id: ID! legacy: Int {_PROD} }}"

    assert release_notes(old, new) == (
        "### Availability changes\n"
        "\n"
        "**development**\n"
        "- Removed: `Program.legacy`\n"
        "\n"
        "**production**\n"
        "- Now leaving (removed from development): `Program.legacy`\n"
    )


def test_new_type_is_listed_once_not_with_each_part():
    old = "type Query { a: Int }"
    new = (
        f"type Query {{ a: Int clone(mode: Mode): Clone {_DEV} }}\n"
        f"type Clone {_DEV} {{ id: ID! {_DEV} }}\n"
        f"enum Mode {_DEV} {{ ALL {_DEV} NONE {_DEV} }}"
    )

    assert release_notes(old, new) == (
        "### Availability changes\n"
        "\n"
        "**development**\n"
        "- New: `Clone`, `Mode`, `Query.clone`\n"
    )


def test_argument_and_enum_value_changes_are_listed():
    old = f"type Query {{ find(limit: Int {_DEV}): Int }}\nenum Code {{ OK WARN {_PROD} }}"
    new = "type Query { find: Int }\nenum Code { OK WARN }"

    assert release_notes(old, new) == (
        "### Availability changes\n"
        "\n"
        "**development**\n"
        "- New: `Code.WARN`\n"
        "- Removed: `Query.find(limit:)`\n"
    )


def test_identical_schemas_report_no_changes():
    sdl = f"type Query {{ a: Int b: Int {_DEV} }}"

    assert "No changes" in release_notes(sdl, sdl)


def _git(repo, *args):
    subprocess.run(
        ["git", "-c", "user.name=t", "-c", "user.email=t@t", *args],
        cwd=repo,
        check=True,
        capture_output=True,
    )


def test_cli_merges_the_committed_schemas_at_a_ref_and_in_the_checkout(
    tmp_path, monkeypatch
):
    schemas = tmp_path / "src" / "gpp_client" / "schemas"
    schemas.mkdir(parents=True)
    (schemas / "development.graphql").write_text("type Query { a: Int b: Int }")
    (schemas / "production.graphql").write_text("type Query { a: Int }")
    _git(tmp_path, "init", "-q")
    _git(tmp_path, "add", ".")
    _git(tmp_path, "commit", "-q", "-m", "release")
    _git(tmp_path, "tag", "v26.9.0")
    (schemas / "production.graphql").write_text("type Query { a: Int b: Int }")
    monkeypatch.chdir(tmp_path)

    result = CliRunner().invoke(app, ["v26.9.0"])

    assert result.exit_code == 0, result.output
    assert "**production**\n- New: `Query.b`" in result.output
    assert "**development**" not in result.output


def test_cli_names_a_ref_without_committed_schemas(tmp_path, monkeypatch):
    (tmp_path / "README").write_text("old release")
    _git(tmp_path, "init", "-q")
    _git(tmp_path, "add", ".")
    _git(tmp_path, "commit", "-q", "-m", "release")
    _git(tmp_path, "tag", "v26.8.0")
    monkeypatch.chdir(tmp_path)

    result = CliRunner().invoke(app, ["v26.8.0"])

    assert result.exit_code != 0
    assert "v26.8.0 has no src/gpp_client/schemas/development.graphql" in result.output
