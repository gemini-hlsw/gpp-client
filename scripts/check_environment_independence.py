"""
Check that the tests pass when every environment has the development schema.

Tests get environment differences from fixture schemas, never from the
committed ones, because a schema update changes those whenever GPP promotes
something. This copies the checkout to a scratch directory, copies the
development schema over production there, rebuilds the client and runs
pytest. The checkout itself is never written to.

Run from the repository root: ``uv run python -m scripts.check_environment_independence``.
"""

import os
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path

import typer

from gpp_client.cli import output
from gpp_client.environment import GPPEnvironment
from scripts.build_client import BuildPaths

SOURCE_ENVIRONMENT = GPPEnvironment.DEVELOPMENT.label
REPLACED_ENVIRONMENTS = tuple(
    env.label for env in GPPEnvironment if env is not GPPEnvironment.DEVELOPMENT
)

app = typer.Typer(add_completion=False)


def _copy_checkout(root: Path, target: Path) -> None:
    # Tracked and untracked-but-not-ignored files, so local edits are checked too.
    listed = subprocess.run(
        ["git", "ls-files", "-z", "--cached", "--others", "--exclude-standard"],
        cwd=root,
        check=True,
        capture_output=True,
    ).stdout.decode()
    for name in filter(None, listed.split("\0")):
        source = root / name
        if not source.is_file():
            continue
        destination = target / name
        destination.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(source, destination)


def _run(command: list[str], cwd: Path, env: dict[str, str]) -> None:
    output.info(" ".join(command))
    result = subprocess.run(command, cwd=cwd, env=env)
    if result.returncode != 0:
        raise typer.Exit(code=result.returncode)


@app.command()
def main() -> None:
    """
    Rebuild with the development schema everywhere in a scratch copy and run pytest.
    """
    root = Path.cwd()
    # The scratch copy gets its own environment, not the caller's.
    env = {k: v for k, v in os.environ.items() if k != "VIRTUAL_ENV"}
    with tempfile.TemporaryDirectory(prefix="gpp-env-independence-") as scratch:
        copy = Path(scratch)
        _copy_checkout(root, copy)
        paths = BuildPaths.for_repo(copy)
        for environment in REPLACED_ENVIRONMENTS:
            shutil.copyfile(
                paths.schema_path(SOURCE_ENVIRONMENT), paths.schema_path(environment)
            )
        output.info(f"Scratch copy at {copy}")
        _run(
            ["uv", "run", "--locked", "python", "-m", "scripts.build_client"],
            copy,
            env,
        )
        _run(["uv", "run", "--locked", "pytest"], copy, env)
    output.success("Tests pass with the development schema in every environment.")


if __name__ == "__main__":
    sys.exit(app())
