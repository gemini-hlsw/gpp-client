"""
List what a release changes per environment, for its release notes.

Compares two merged schemas, normally the one at the previous release tag and
the committed one. Per environment it lists the parts new to it and the parts
removed from it, and for production the parts newly leaving: absent
from development but still on production, so expected to go at a coming
promotion.
"""

import subprocess
from pathlib import Path

import typer

from custom_plugins.environments import USER_ENVIRONMENTS, environments
from graphql import (
    DocumentNode,
    EnumTypeDefinitionNode,
    InputObjectTypeDefinitionNode,
    InterfaceTypeDefinitionNode,
    ObjectTypeDefinitionNode,
    TypeDefinitionNode,
    parse,
)

__all__ = ["release_notes"]

MERGED_SCHEMA = Path("graphql") / "schemas" / "merged.graphql"

app = typer.Typer(add_completion=False)

Availability = dict[str, tuple[tuple[str, ...], str | None]]
"""Per coordinate: the environments that have it, and its parent coordinate."""


def release_notes(old_sdl: str, new_sdl: str) -> str:
    """
    Return the availability changes between two merged schemas as Markdown.

    Parameters
    ----------
    old_sdl : str
        The merged schema of the previous release.
    new_sdl : str
        The merged schema of this release.

    Returns
    -------
    str
        Per environment, the parts new to it and the parts removed from it, and
        the parts newly leaving production. A part whose parent
        changed the same way is left out, so a new type is listed once rather
        than with each of its fields.
    """
    old = _availability(parse(old_sdl))
    new = _availability(parse(new_sdl))
    sections = []
    for environment in USER_ENVIRONMENTS:
        added = _changed(new, old, environment)
        removed = _changed(old, new, environment)
        lines = []
        if added:
            lines.append(f"- New: {_names(added)}")
        if removed:
            lines.append(f"- Removed: {_names(removed)}")
        if environment == "production":
            leaving = _top_level(
                {c for c in new if _is_leaving(new, c) and not _is_leaving(old, c)},
                new,
            )
            if leaving:
                lines.append(
                    f"- Now leaving (removed from development): {_names(leaving)}"
                )
        if lines:
            sections.append(f"**{environment}**\n" + "\n".join(lines))
    if not sections:
        return "### Availability changes\n\nNo changes for development or production.\n"
    return "### Availability changes\n\n" + "\n\n".join(sections) + "\n"


def _availability(document: DocumentNode) -> Availability:
    found: Availability = {}

    def record(coordinate: str, node, parent: str | None) -> None:
        own = environments(node) or USER_ENVIRONMENTS
        within = found[parent][0] if parent is not None else USER_ENVIRONMENTS
        found[coordinate] = (tuple(e for e in own if e in within), parent)

    for definition in document.definitions:
        if not isinstance(definition, TypeDefinitionNode):
            continue
        type_name = definition.name.value
        record(type_name, definition, None)
        if isinstance(
            definition,
            (
                ObjectTypeDefinitionNode,
                InterfaceTypeDefinitionNode,
                InputObjectTypeDefinitionNode,
            ),
        ):
            for field in definition.fields or ():
                field_coordinate = f"{type_name}.{field.name.value}"
                record(field_coordinate, field, type_name)
                for argument in getattr(field, "arguments", None) or ():
                    record(
                        f"{field_coordinate}({argument.name.value}:)",
                        argument,
                        field_coordinate,
                    )
        elif isinstance(definition, EnumTypeDefinitionNode):
            for value in definition.values or ():
                record(f"{type_name}.{value.name.value}", value, type_name)
    return found


def _has(availability: Availability, coordinate: str, environment: str) -> bool:
    entry = availability.get(coordinate)
    return entry is not None and environment in entry[0]


def _changed(
    gaining: Availability, losing: Availability, environment: str
) -> list[str]:
    """
    Return the parts ``gaining`` has on the environment and ``losing`` lacks.
    """
    changed = {
        coordinate
        for coordinate in gaining
        if _has(gaining, coordinate, environment)
        and not _has(losing, coordinate, environment)
    }
    return _top_level(changed, gaining)


def _is_leaving(availability: Availability, coordinate: str) -> bool:
    return _has(availability, coordinate, "production") and not _has(
        availability, coordinate, "development"
    )


def _top_level(coordinates: set[str], availability: Availability) -> list[str]:
    return sorted(c for c in coordinates if availability[c][1] not in coordinates)


def _names(names: list[str]) -> str:
    return ", ".join(f"`{name}`" for name in names)


def _schema_at(ref: str) -> str:
    try:
        return subprocess.run(
            ["git", "show", f"{ref}:{MERGED_SCHEMA.as_posix()}"],
            check=True,
            capture_output=True,
            text=True,
        ).stdout
    except subprocess.CalledProcessError as exc:
        raise typer.BadParameter(
            f"{ref} has no {MERGED_SCHEMA.as_posix()}: {exc.stderr.strip()}"
        ) from exc


@app.command()
def main(
    since: str = typer.Argument(
        ..., help="Git ref of the previous release, such as v26.10.0."
    ),
    schema: Path = typer.Option(MERGED_SCHEMA, help="Merged schema of this release."),
) -> None:
    """
    Print the availability changes since a git ref, as Markdown.
    """
    typer.echo(release_notes(_schema_at(since), schema.read_text(encoding="utf-8")))


if __name__ == "__main__":
    app()
