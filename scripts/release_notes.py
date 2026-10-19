"""
List what a release changes per environment, for its release notes.

Diffs each environment's committed schema between the previous release tag
and the checkout with graphql-core's breaking and dangerous change finders.
"""

import subprocess
from collections.abc import Mapping
from pathlib import Path
from typing import Annotated

import typer

from custom_plugins.environments import USER_ENVIRONMENTS
from graphql import (
    build_schema,
    find_breaking_changes,
    find_dangerous_changes,
    parse,
)
from scripts.build_client import BuildPaths
from scripts.schema_merge import DEVELOPMENT, PRODUCTION, pair_types

__all__ = ["release_notes"]

app = typer.Typer(add_completion=False)

_HEADLINE_ORDER = (PRODUCTION, DEVELOPMENT)


def release_notes(
    previous: Mapping[str, str],
    current: Mapping[str, str],
    *,
    held: Mapping[str, str] | None = None,
) -> str:
    """
    Return what changed per environment between two schema sets, as Markdown.

    Parameters
    ----------
    previous : Mapping[str, str]
        The previous release's schema per environment, as SDL.
    current : Mapping[str, str]
        This release's schema per environment, as SDL.
    held : Mapping[str, str] | None, optional
        Per environment held at its committed schema, the commit that schema
        is from.

    Returns
    -------
    str
        A "changed" or "unchanged" headline per environment, then for each
        changed environment its "Breaking" and "Added or relaxed" lists, then
        the aliases this release adds.
    """
    previous_renames = _renames(previous)
    current_renames = _renames(current)
    headlines = []
    sections = []
    for environment in _HEADLINE_ORDER:
        changed = previous[environment] != current[environment]
        if held and environment in held:
            headline = (
                f"held at `{held[environment]}`; its introspected schema did not build"
            )
        else:
            headline = "changed" if changed else "unchanged"
        headlines.append(f"{environment.capitalize()}: {headline}")
        # A dropped alias breaks imports on every environment; it is listed
        # under production because its promotion made the names equal.
        dropped = (
            _dropped_alias_lines(previous_renames, current_renames)
            if environment == PRODUCTION
            else []
        )
        if changed or dropped:
            sections.append(
                f"**{environment.capitalize()}**\n\n"
                + _changes(previous[environment], current[environment], dropped)
            )
    aliases = _alias_lines(previous_renames, current_renames)
    if aliases:
        sections.append("**Aliases**\n\n" + "\n".join(aliases))
    return (
        "\n\n".join(["### Schema changes\n\n" + "\n".join(headlines), *sections]) + "\n"
    )


def _renames(schemas: Mapping[str, str]) -> dict[str, str]:
    return pair_types(
        parse(schemas[PRODUCTION]), parse(schemas[DEVELOPMENT])
    ).by_production_name


def _alias_lines(previous: Mapping[str, str], current: Mapping[str, str]) -> list[str]:
    return [
        f"- `{alias}` is now an alias of `{target}`; production adopts `{target}` "
        "at its next promotion, and the alias goes with it."
        for alias, target in current.items()
        if previous.get(alias) != target
    ]


def _dropped_alias_lines(
    previous: Mapping[str, str], current: Mapping[str, str]
) -> list[str]:
    return [
        f"Alias `{alias}` of `{target}` was dropped; import `{target}`."
        for alias, target in previous.items()
        if current.get(alias) != target
    ]


def _changes(previous_sdl: str, current_sdl: str, dropped_aliases: list[str]) -> str:
    previous_schema = build_schema(previous_sdl)
    current_schema = build_schema(current_sdl)
    breaking = [
        change.description
        for change in find_breaking_changes(previous_schema, current_schema)
    ] + dropped_aliases
    relaxed = [
        change.description
        for change in find_dangerous_changes(previous_schema, current_schema)
    ]
    parts = []
    if breaking:
        parts.append("Breaking:\n" + "\n".join(f"- {line}" for line in breaking))
    if relaxed:
        parts.append("Added or relaxed:\n" + "\n".join(f"- {line}" for line in relaxed))
    return "\n\n".join(parts)


def _git(root: Path, *args: str) -> str:
    return subprocess.run(
        ["git", *args], cwd=root, check=True, capture_output=True, text=True
    ).stdout


def _schemas_at(ref: str, paths: BuildPaths, root: Path) -> dict[str, str]:
    schemas = {}
    for environment in USER_ENVIRONMENTS:
        schema = paths.schema_path(environment).relative_to(root).as_posix()
        try:
            schemas[environment] = _git(root, "show", f"{ref}:{schema}")
        except subprocess.CalledProcessError as exc:
            raise typer.BadParameter(
                f"{ref} has no {schema}: {exc.stderr.strip()}"
            ) from exc
    return schemas


def _schemas_in_checkout(paths: BuildPaths) -> dict[str, str]:
    return {
        environment: paths.schema_path(environment).read_text(encoding="utf-8")
        for environment in USER_ENVIRONMENTS
    }


def _last_commit_of(path: Path, root: Path) -> str:
    return _git(root, "log", "-1", "--format=%h", "--", str(path)).strip()


@app.command()
def main(
    since: Annotated[
        str, typer.Argument(help="Git ref of the previous release, such as v26.10.0.")
    ],
    held: Annotated[
        list[str] | None,
        typer.Option(
            help="An environment the schema update held at its committed schema.",
            show_default=False,
        ),
    ] = None,
) -> None:
    """
    Print what changed per environment since a git ref, as Markdown.

    Run from the repository root; the committed schemas in the checkout are
    this release's.
    """
    root = Path.cwd()
    paths = BuildPaths.for_repo(root)
    unknown = [env for env in held or () if env not in USER_ENVIRONMENTS]
    if unknown:
        raise typer.BadParameter(
            f"Unknown environment {', '.join(unknown)}; "
            f"choose from {', '.join(USER_ENVIRONMENTS)}."
        )
    typer.echo(
        release_notes(
            _schemas_at(since, paths, root),
            _schemas_in_checkout(paths),
            held={
                env: _last_commit_of(paths.schema_path(env), root) for env in held or ()
            },
        )
    )


if __name__ == "__main__":
    app()
