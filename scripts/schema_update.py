"""
Bring the client up to date with GPP in one command.

The update introspects both environments, holds an environment whose schema
does not build (its committed copy stays, and the output names it), writes the
schemas that changed, builds the client and runs the test suite. Run twice
without a GPP change, it changes nothing.
"""

import os
import subprocess
import sys
import tempfile
from collections.abc import Callable, Mapping
from dataclasses import dataclass
from pathlib import Path

import httpx
import typer
from rich.markup import escape

from custom_plugins.environments import USER_ENVIRONMENTS
from gpp_client.cli import output
from scripts.build_client import (
    BuildError,
    BuildPaths,
    BuildResult,
    build,
    schema_file,
)
from scripts.download_schema import (
    TIMEOUT_SECONDS,
    SchemaDownloadError,
    SchemaInvalidError,
    download_schemas,
)

__all__ = ["UpdateResult", "schema_update"]

app = typer.Typer(add_completion=False)


@dataclass(frozen=True)
class UpdateResult:
    """
    What a schema update did.

    Parameters
    ----------
    held : tuple[str, ...]
        Environments whose committed schema was kept because the introspected
        one does not build.
    reasons : dict[str, str]
        Why each held environment was held.
    changed : tuple[str, ...]
        Environments whose schema differs from the committed one, so the
        download is now the committed copy.
    build : BuildResult
        What the build produced.
    suite_passed : bool
        Whether the test suite passed on the built client.
    """

    held: tuple[str, ...]
    reasons: dict[str, str]
    changed: tuple[str, ...]
    build: BuildResult
    suite_passed: bool

    @property
    def summary(self) -> str:
        """
        Return what the update did, as Markdown for a PR body.

        Returns
        -------
        str
            One line per environment, then the build's merge and trim
            summaries.
        """
        lines = []
        for environment in USER_ENVIRONMENTS:
            label = environment.capitalize()
            if environment in self.held:
                lines.append(
                    f"- {label}: held at its committed schema; "
                    f"{self.reasons[environment]}"
                )
            elif environment in self.changed:
                lines.append(f"- {label}: changed")
            else:
                lines.append(f"- {label}: unchanged")
        return (
            "### Schema update\n\n"
            + "\n".join(lines)
            + "\n\n"
            + self.build.merge_summary
            + "\n"
            + self.build.trim_summary
        )


def schema_update(
    paths: BuildPaths,
    *,
    run_suite: Callable[[], int],
    http_client: httpx.Client | None = None,
    environ: Mapping[str, str] = os.environ,
) -> UpdateResult:
    """
    Introspect both environments, update the committed schemas and rebuild.

    Parameters
    ----------
    paths : BuildPaths
        The checkout's schemas, operations, codegen config and generated
        package.
    run_suite : Callable[[], int]
        Runs the test suite and returns its exit code.
    http_client : httpx.Client | None, optional
        Client to introspect with; a new one by default.
    environ : Mapping[str, str], optional
        Where to read token fallbacks from; the process environment by default.

    Returns
    -------
    UpdateResult
        What the update did.

    Raises
    ------
    SchemaDownloadError
        Raised when an environment cannot be introspected.
    BuildError
        Raised when the client does not build from the updated schemas.
    """
    held: dict[str, str] = {}
    changed: list[str] = []
    with tempfile.TemporaryDirectory(prefix="gpp-client-schemas-") as scratch:
        downloaded = Path(scratch)
        for environment in USER_ENVIRONMENTS:
            try:
                download_schemas(
                    downloaded,
                    [environment],
                    http_client=http_client,
                    environ=environ,
                )
            except SchemaInvalidError as exc:
                held[environment] = str(exc)
                continue
            sdl = schema_file(downloaded, environment).read_text(encoding="utf-8")
            committed = paths.schema_path(environment)
            if not committed.is_file() or committed.read_text(encoding="utf-8") != sdl:
                committed.write_text(sdl, encoding="utf-8")
                changed.append(environment)
    result = build(paths)
    return UpdateResult(
        held=tuple(held),
        reasons=held,
        changed=tuple(changed),
        build=result,
        suite_passed=run_suite() == 0,
    )


def _run_pytest() -> int:
    return subprocess.run([sys.executable, "-m", "pytest"], check=False).returncode


@app.command()
def main() -> None:
    """
    Update the committed schemas from GPP, rebuild the client and run the tests.

    Run from the repository root. An environment whose schema does not build
    keeps its committed copy and is named in the output.
    """
    paths = BuildPaths.for_repo(Path.cwd())
    output.info("Introspecting GPP, building the client and running the tests...")
    try:
        with httpx.Client(timeout=TIMEOUT_SECONDS) as client:
            result = schema_update(paths, http_client=client, run_suite=_run_pytest)
    except (SchemaDownloadError, BuildError) as exc:
        output.fail(escape(str(exc)))
        raise typer.Exit(code=1) from exc

    # Plain text, so it pastes into a PR body unchanged.
    typer.echo("\n" + result.summary)
    if not result.suite_passed:
        output.fail("Tests failed on the updated client.")
        raise typer.Exit(code=1)
    output.success("Tests passed on the updated client.")


if __name__ == "__main__":
    app()
