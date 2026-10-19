"""
Tests for the per-environment release notes, driven through ``release_notes``.
"""

import subprocess

from typer.testing import CliRunner

from scripts.release_notes import app, release_notes

_SCHEMA = "type Query { program: Program }\ntype Program { id: ID! name: String }\n"
_SCHEMA_WITH_REFERENCE = (
    "type Query { program: Program }\n"
    "type Program { id: ID! name: String reference: String }\n"
)


def _both(sdl: str) -> dict[str, str]:
    return {"development": sdl, "production": sdl}


def test_headlines_say_which_environment_changed():
    notes = release_notes(
        _both(_SCHEMA),
        {"development": _SCHEMA_WITH_REFERENCE, "production": _SCHEMA},
    )

    assert notes.startswith(
        "### Schema changes\n\nProduction: unchanged\nDevelopment: changed\n"
    )


def test_each_changed_environment_lists_breaking_and_added_or_relaxed_changes():
    previous = (
        "type Query { program(limit: Int): Program }\n"
        "type Program { id: ID! legacy: Int }\n"
        "enum Mode { A }\n"
    )
    current = (
        "type Query { program(limit: Int): Program }\n"
        "type Program { id: ID! name: String }\n"
        "enum Mode { A B }\n"
    )

    notes = release_notes(
        _both(previous), {"development": current, "production": previous}
    )

    assert notes == (
        "### Schema changes\n"
        "\n"
        "Production: unchanged\n"
        "Development: changed\n"
        "\n"
        "**Development**\n"
        "\n"
        "Breaking:\n"
        "- Program.legacy was removed.\n"
        "\n"
        "Added or relaxed:\n"
        "- B was added to enum type Mode.\n"
    )


_PRODUCTION_WITH_OLD_NAME = (
    "type Query { find(input: OldInput): Int }\ninput OldInput { a: Int }\n"
)
_DEVELOPMENT_WITH_NEW_NAME = (
    "type Query { find(input: NewInput): Int }\ninput NewInput { a: Int }\n"
)


def test_a_rename_the_pairing_finds_yields_the_alias_line():
    notes = release_notes(
        _both(_PRODUCTION_WITH_OLD_NAME),
        {
            "development": _DEVELOPMENT_WITH_NEW_NAME,
            "production": _PRODUCTION_WITH_OLD_NAME,
        },
    )

    assert notes.endswith(
        "**Aliases**\n"
        "\n"
        "- `OldInput` is now an alias of `NewInput`; production adopts `NewInput` "
        "at its next promotion, and the alias goes with it.\n"
    )


def test_a_promotion_that_makes_the_names_equal_drops_the_alias_under_breaking():
    notes = release_notes(
        {
            "development": _DEVELOPMENT_WITH_NEW_NAME,
            "production": _PRODUCTION_WITH_OLD_NAME,
        },
        _both(_DEVELOPMENT_WITH_NEW_NAME),
    )

    assert (
        "**Production**\n"
        "\n"
        "Breaking:\n"
        "- OldInput was removed.\n"
        "- Query.find arg input has changed type from OldInput to NewInput.\n"
        "- Alias `OldInput` of `NewInput` was dropped; import `NewInput`.\n"
    ) in notes
    assert "**Aliases**" not in notes


def test_a_held_environment_is_named_with_the_commit_its_schema_is_from():
    notes = release_notes(
        _both(_SCHEMA),
        {"development": _SCHEMA, "production": _SCHEMA_WITH_REFERENCE},
        held={"development": "abc1234"},
    )

    assert notes.startswith(
        "### Schema changes\n"
        "\n"
        "Production: changed\n"
        "Development: held at `abc1234`; its introspected schema did not build\n"
    )


def _git(repo, *args) -> str:
    return subprocess.run(
        ["git", "-c", "user.name=t", "-c", "user.email=t@t", *args],
        cwd=repo,
        check=True,
        capture_output=True,
        text=True,
    ).stdout.strip()


def _release_checkout(root, development: str, production: str) -> None:
    schemas = root / "src" / "gpp_client" / "schemas"
    schemas.mkdir(parents=True)
    (schemas / "development.graphql").write_text(development)
    (schemas / "production.graphql").write_text(production)
    _git(root, "init", "-q")
    _git(root, "add", ".")
    _git(root, "commit", "-q", "-m", "release")
    _git(root, "tag", "v26.9.0")


def test_command_diffs_each_committed_schema_at_a_ref_against_the_checkout(
    tmp_path, monkeypatch
):
    _release_checkout(tmp_path, development=_SCHEMA, production=_SCHEMA)
    (tmp_path / "src" / "gpp_client" / "schemas" / "development.graphql").write_text(
        "type Query { program: Program }\ntype Program { id: ID! }\n"
    )
    monkeypatch.chdir(tmp_path)

    result = CliRunner().invoke(app, ["v26.9.0"])

    assert result.exit_code == 0, result.output
    assert "Production: unchanged\nDevelopment: changed\n" in result.output
    assert "- Program.name was removed." in result.output


def test_command_names_a_held_environment_at_the_commit_its_schema_is_from(
    tmp_path, monkeypatch
):
    _release_checkout(tmp_path, development=_SCHEMA, production=_SCHEMA)
    commit = _git(tmp_path, "rev-parse", "--short", "HEAD")
    monkeypatch.chdir(tmp_path)

    result = CliRunner().invoke(app, ["v26.9.0", "--held", "development"])

    assert result.exit_code == 0, result.output
    assert f"Development: held at `{commit}`" in result.output


def test_command_names_a_ref_without_committed_schemas(tmp_path, monkeypatch):
    (tmp_path / "README").write_text("old release")
    _git(tmp_path, "init", "-q")
    _git(tmp_path, "add", ".")
    _git(tmp_path, "commit", "-q", "-m", "release")
    _git(tmp_path, "tag", "v26.8.0")
    monkeypatch.chdir(tmp_path)

    result = CliRunner().invoke(app, ["v26.8.0"])

    assert result.exit_code != 0
    assert "v26.8.0 has no src/gpp_client/schemas/development.graphql" in result.output
