"""
Tests for the environment-independence check, driven through ``main``.
"""

import subprocess

from scripts import check_environment_independence as check


def _checkout(root):
    schemas_dir = root / "graphql" / "schemas"
    schemas_dir.mkdir(parents=True)
    for name, sdl in {
        "development": "type Query { a: Int b: Int }",
        "production": "type Query { a: Int }",
        "merged": "type Query { a: Int b: Int }",
    }.items():
        (schemas_dir / f"{name}.graphql").write_text(sdl)
    subprocess.run(["git", "init", "-q"], cwd=root, check=True)
    return schemas_dir


def test_scratch_copy_builds_with_the_development_schema_as_production(
    tmp_path, monkeypatch
):
    _checkout(tmp_path)
    schemas_at_build = {}

    def run(command, cwd, env):
        if "scripts.build_client" in command:
            schemas_dir = cwd / "graphql" / "schemas"
            schemas_at_build.update(
                {path.name: path.read_text() for path in schemas_dir.iterdir()}
            )

    monkeypatch.chdir(tmp_path)
    monkeypatch.setattr(check, "_run", run)

    check.main()

    assert schemas_at_build == {
        "development.graphql": "type Query { a: Int b: Int }",
        "production.graphql": "type Query { a: Int b: Int }",
        "merged.graphql": "type Query { a: Int b: Int }",
    }
