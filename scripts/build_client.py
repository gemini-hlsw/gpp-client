"""
Build the client from the committed environment schemas.

The build merges the development and production schemas committed in
``src/gpp_client/schemas/``, runs ariadne-codegen once on the merged schema, and
writes a trimmed copy of every operation per environment into the generated
package. The merged schema is a build intermediate and is never committed.
"""

import ast
import contextlib
import io
import re
import shutil
import tempfile
import tomllib
from dataclasses import dataclass
from pathlib import Path

import typer
from ariadne_codegen.exceptions import CodeGenException
from ariadne_codegen.main import client as run_ariadne_codegen
from rich.markup import escape

from custom_plugins.alias_names import ALIASES_KEY, AliasReport
from custom_plugins.environment_defaults import DEFAULTS_KEY, DefaultsReport
from custom_plugins.environments import USER_ENVIRONMENTS, environments
from gpp_client.cli import output
from graphql import (
    DocumentNode,
    EnumTypeDefinitionNode,
    FieldsOnCorrectTypeRule,
    GraphQLError,
    KnownArgumentNamesRule,
    KnownTypeNamesRule,
    OperationDefinitionNode,
    ValuesOfCorrectTypeRule,
    build_ast_schema,
    parse,
    validate,
)
from scripts.schema_merge import (
    DEVELOPMENT,
    PRODUCTION,
    KindConflict,
    MergedSchema,
    Pairing,
    Rename,
    SchemaMergeError,
    TypeConflict,
    merge_schemas,
)
from scripts.trim_operations import (
    EnvironmentOperations,
    generated_operations,
    trim_operations,
)

__all__ = [
    "BuildError",
    "BuildPaths",
    "BuildResult",
    "KindConflict",
    "Pairing",
    "Rename",
    "TypeConflict",
    "build",
    "schema_file",
]

app = typer.Typer(add_completion=False)


def schema_file(schemas_dir: Path, environment: str) -> Path:
    """
    Return one environment's schema file in a schemas directory.

    Parameters
    ----------
    schemas_dir : Path
        Directory holding one schema per environment.
    environment : str
        Environment name, such as ``"production"``.

    Returns
    -------
    Path
        The environment's schema file.
    """
    return schemas_dir / f"{environment}.graphql"


class BuildError(RuntimeError):
    """
    Raised when the build cannot complete.
    """


@dataclass(frozen=True)
class BuildPaths:
    """
    Files the build reads and writes.

    Parameters
    ----------
    schemas_dir : Path
        Directory holding ``<environment>.graphql`` per environment.
    operations_dir : Path
        Directory holding the ``.graphql`` operations, searched recursively.
    package_dir : Path
        The generated package, replaced on every build.
    codegen_config : Path
        The ariadne-codegen TOML config; the build fills in the paths.
    """

    schemas_dir: Path
    operations_dir: Path
    package_dir: Path
    codegen_config: Path

    @classmethod
    def for_repo(cls, root: Path) -> "BuildPaths":
        """
        Return the paths used in a gpp-client checkout.

        Parameters
        ----------
        root : Path
            Repository root.

        Returns
        -------
        BuildPaths
            Paths under ``root``.
        """
        return cls(
            schemas_dir=root / "src" / "gpp_client" / "schemas",
            operations_dir=root / "graphql" / "operations",
            package_dir=root / "src" / "gpp_client" / "generated",
            codegen_config=root / "graphql" / "codegen.toml",
        )

    def schema_path(self, environment: str) -> Path:
        """
        Return one environment's schema file.

        Parameters
        ----------
        environment : str
            Environment name, such as ``"production"``.

        Returns
        -------
        Path
            The environment's schema file.
        """
        return schema_file(self.schemas_dir, environment)


@dataclass(frozen=True)
class BuildResult:
    """
    What a build produced.

    Parameters
    ----------
    merged_sdl : str
        The merged schema the client was generated from, as SDL.
    conflicts : tuple[TypeConflict, ...]
        Elements given production's type because theirs differs.
    pairing : Pairing
        The production types the merge renamed to their development names.
    kind_conflicts : tuple[KindConflict, ...]
        Type names whose kind differs, where production's definition won.
    merge_summary : str
        The renames, aliases, conflicts and refused votes, as Markdown for a
        PR body.
    trim_summary : str
        What each environment does not receive, as Markdown for a PR body.
    """

    merged_sdl: str
    conflicts: tuple[TypeConflict, ...]
    pairing: Pairing
    kind_conflicts: tuple[KindConflict, ...]
    merge_summary: str
    trim_summary: str


def build(paths: BuildPaths) -> BuildResult:
    """
    Run the build pipeline.

    Parameters
    ----------
    paths : BuildPaths
        Files to read and write.

    Returns
    -------
    BuildResult
        What the build produced.

    Raises
    ------
    BuildError
        Raised when a schema file is missing, an environment schema is invalid,
        an operation selects a field no environment has, codegen fails, an
        environment-specific field did not get a ``None`` default, the
        generated client embeds fewer operations than were written, or a
        trimmed operation is invalid on its environment.
    """
    merged = _merge(paths)
    operations = _check_selections_exist_somewhere(paths, merged)
    defaults, aliases = _run_codegen(paths, merged)
    _check_environment_defaults(paths.package_dir, defaults)
    operation_strs = _embedded_operations(paths, operations)
    schemas = {env: _environment_schema(paths, env) for env in USER_ENVIRONMENTS}
    trimmed = [
        trim_operations(
            env,
            schemas[env],
            operation_strs,
            excluded=frozenset(c.coordinate for c in merged.conflicts)
            if env == DEVELOPMENT
            else frozenset(),
            reverse=merged.pairing.reverse if env == PRODUCTION else None,
        )
        for env in USER_ENVIRONMENTS
    ]
    errors = [error for environment in trimmed for error in environment.errors]
    if errors:
        raise BuildError(
            "Trimmed operations are invalid:\n" + "\n".join(f"  {e}" for e in errors)
        )
    _write_trimmed(paths.package_dir, generated_operations(operation_strs), trimmed)
    _write_availability(paths.package_dir, defaults, merged)
    return BuildResult(
        merged_sdl=merged.sdl,
        conflicts=merged.conflicts,
        pairing=merged.pairing,
        kind_conflicts=merged.kind_conflicts,
        merge_summary=_merge_summary(merged, aliases),
        trim_summary=_trim_summary(trimmed),
    )


def _merge(paths: BuildPaths) -> MergedSchema:
    missing = [
        str(paths.schema_path(env))
        for env in USER_ENVIRONMENTS
        if not paths.schema_path(env).is_file()
    ]
    if missing:
        raise BuildError(f"Schema files not found: {', '.join(missing)}")
    try:
        return merge_schemas(
            development=paths.schema_path(DEVELOPMENT).read_text(encoding="utf-8"),
            production=paths.schema_path(PRODUCTION).read_text(encoding="utf-8"),
        )
    except SchemaMergeError as exc:
        raise BuildError(str(exc)) from exc


_EXISTENCE_RULES = [
    FieldsOnCorrectTypeRule,
    KnownArgumentNamesRule,
    KnownTypeNamesRule,
    ValuesOfCorrectTypeRule,
]


def _check_selections_exist_somewhere(
    paths: BuildPaths, merged: MergedSchema
) -> DocumentNode:
    """
    Fail listing every field, argument, type or value that no environment has.

    Codegen would stop at the first; a schema update that removed several
    parts is fixed in one go when the build names them all. Returns the
    operations as written.
    """
    sources = sorted(paths.operations_dir.rglob("*.graphql"))
    if not sources:
        return DocumentNode(definitions=())
    document = parse("\n\n".join(p.read_text(encoding="utf-8") for p in sources))
    errors = validate(build_ast_schema(merged.document), document, _EXISTENCE_RULES)
    if errors:
        raise BuildError(
            "Operations select what no environment has:\n"
            + "\n".join(
                f"  {_definition_name(document, error)}: {error.message}"
                for error in errors
            )
        )
    return document


def _definition_name(document: DocumentNode, error: GraphQLError) -> str:
    start = error.nodes[0].loc.start if error.nodes and error.nodes[0].loc else -1
    for definition in document.definitions:
        if definition.loc and definition.loc.start <= start < definition.loc.end:
            name = getattr(definition, "name", None)
            return name.value if name else "anonymous"
    return "anonymous"


def _environment_schema(paths: BuildPaths, environment: str):
    return build_ast_schema(
        parse(paths.schema_path(environment).read_text(encoding="utf-8"))
    )


def _run_codegen(
    paths: BuildPaths, merged: MergedSchema
) -> tuple[DefaultsReport, AliasReport]:
    """
    Generate the client from the merged schema.

    Returns where ``None`` defaults went and which production names became
    aliases.
    """
    with paths.codegen_config.open("rb") as config_file:
        config = tomllib.load(config_file)
    defaults = DefaultsReport()
    aliases = AliasReport(renames=merged.pairing.by_production_name)
    config["tool"]["gpp-client"] = {DEFAULTS_KEY: defaults, ALIASES_KEY: aliases}

    if paths.package_dir.is_dir():
        shutil.rmtree(paths.package_dir)
    paths.package_dir.parent.mkdir(parents=True, exist_ok=True)
    with tempfile.TemporaryDirectory(prefix="gpp-client-merged-") as scratch:
        merged_path = Path(scratch) / "merged.graphql"
        merged_path.write_text(merged.sdl, encoding="utf-8")
        config["tool"]["ariadne-codegen"].update(
            schema_path=str(merged_path),
            queries_path=str(paths.operations_dir),
            target_package_path=str(paths.package_dir.parent),
            target_package_name=paths.package_dir.name,
        )
        try:
            with contextlib.redirect_stdout(io.StringIO()):
                run_ariadne_codegen(config)
        except (CodeGenException, GraphQLError) as exc:
            raise BuildError(f"Codegen failed: {exc}") from exc
    return defaults, aliases


def _check_environment_defaults(package_dir: Path, report: DefaultsReport) -> None:
    """
    Fail naming each environment-specific selection whose model lacks a None default.

    Read from the generated source, so a field the plugin matched wrongly, or a
    default a later plugin removed, cannot pass unnoticed.
    """
    fields: dict[tuple[str, str], list[ast.expr | None]] = {}
    for module in package_dir.glob("*.py"):
        for node in ast.walk(ast.parse(module.read_text(encoding="utf-8"))):
            if not isinstance(node, ast.ClassDef):
                continue
            for statement in node.body:
                if isinstance(statement, ast.AnnAssign) and isinstance(
                    statement.target, ast.Name
                ):
                    fields.setdefault((node.name, statement.target.id), []).append(
                        statement.value
                    )

    defaulted = {
        offset
        for offset, class_name, attribute in report.placed
        if fields.get((class_name, attribute))
        and all(_defaults_to_none(value) for value in fields[class_name, attribute])
    }
    missing = sorted(
        {
            selection.description
            for offset, selection in report.expected.items()
            if offset not in defaulted
        }
    )
    if missing:
        raise BuildError(
            "Environment-specific fields did not get a None default:\n"
            + "\n".join(f"  {description}" for description in missing)
        )


def _defaults_to_none(value: ast.expr | None) -> bool:
    if isinstance(value, ast.Constant):
        return value.value is None
    if isinstance(value, ast.Call):
        return any(
            keyword.arg == "default"
            and isinstance(keyword.value, ast.Constant)
            and keyword.value.value is None
            for keyword in value.keywords
        )
    return False


def _embedded_operations(paths: BuildPaths, written: DocumentNode) -> list[str]:
    """
    Return each operation as the generated client embeds it.

    The queries are read back from the generated client's source, so the
    trimmed copies start from the exact text the client sends, whatever a
    plugin did to it. Fails when fewer come back than operations were written.
    """
    queries = _embedded_queries(paths.package_dir / "client.py")
    expected = sum(isinstance(d, OperationDefinitionNode) for d in written.definitions)
    if len(queries) != expected:
        raise BuildError(
            "Reading gql(...) queries back from the generated client found "
            f"{len(queries)} of {expected} generated operations."
        )
    return queries


def _embedded_queries(client_path: Path) -> list[str]:
    return _embedded_queries_in(ast.parse(client_path.read_text(encoding="utf-8")))


def _embedded_queries_in(tree: ast.AST) -> list[str]:
    return [
        node.args[0].value
        for node in ast.walk(tree)
        if isinstance(node, ast.Call)
        and isinstance(node.func, ast.Name)
        and node.func.id == "gql"
        and node.args
        and isinstance(node.args[0], ast.Constant)
    ]


def _merge_summary(merged: MergedSchema, aliases: AliasReport) -> str:
    lines = [
        f"- Renamed `{rename.production}` to `{rename.development}` "
        f"({_names(rename.coordinates)})"
        for rename in merged.pairing.renames
    ]
    lines += [
        f"- Alias `{alias}` of `{target}` in `{module}`"
        for module, alias, target in aliases.placed
    ]
    # Responses carry production's __typename, which nothing maps back to the
    # merged name; a renamed union or interface is the trigger to add that map.
    lines += [
        f"- Warning: {rename.kind} `{rename.production}` was renamed; production "
        f"answers `__typename` with `{rename.production}`, so a `__typename` map "
        "is now needed"
        for rename in merged.pairing.renames
        if rename.kind in ("union", "interface")
    ]
    lines += [
        f"- Conflict `{conflict.coordinate}`: {_on_each(conflict.types)}; "
        "production's type used"
        for conflict in merged.conflicts
    ]
    for conflict in merged.kind_conflicts:
        dropped = f", dropped {_names(conflict.dropped)}" if conflict.dropped else ""
        lines.append(
            f"- Kind conflict `{conflict.name}`: {_on_each(conflict.kinds)}; "
            f"production's definition used{dropped}"
        )
    lines += [f"- Ambiguous `{vote}`; not renamed" for vote in merged.pairing.ambiguous]
    lines += [
        f"- Collision `{vote}`; not renamed" for vote in merged.pairing.collisions
    ]
    if not lines:
        return "### Merge summary\n\nNo renames, conflicts or refused votes.\n"
    return "### Merge summary\n\n" + "\n".join(lines) + "\n"


def _on_each(by_environment: tuple[tuple[str, str], ...]) -> str:
    return ", ".join(f"{what} on {env}" for env, what in by_environment)


def _trim_summary(trimmed: list[EnvironmentOperations]) -> str:
    sections = []
    for environment in trimmed:
        lines = []
        if environment.unavailable:
            lines.append(f"- Unavailable: {_names(environment.unavailable)}")
        lines += [
            f"- `{part}` removed from {_names(definitions)}"
            for part, definitions in environment.removed.items()
        ]
        if lines:
            sections.append(f"**{environment.environment}**\n" + "\n".join(lines))
        else:
            sections.append(f"**{environment.environment}**: nothing trimmed.")
    return "### Trim summary\n\n" + "\n\n".join(sections) + "\n"


def _names(names: tuple[str, ...]) -> str:
    return ", ".join(f"`{name}`" for name in names)


def _write_trimmed(
    package_dir: Path,
    generated: dict[str, str],
    trimmed: list[EnvironmentOperations],
) -> None:
    trimmed_dir = package_dir / "trimmed"
    trimmed_dir.mkdir()
    (trimmed_dir / "__init__.py").write_text(
        '"""Operations trimmed per environment. Generated; do not edit."""\n\n'
        f"GENERATED = {_dict_lines(generated.items())}\n",
        encoding="utf-8",
    )
    for environment in trimmed:
        operations = sorted(
            environment.operations.items(), key=lambda item: (item[1][0], item[0])
        )
        (trimmed_dir / f"{environment.environment}.py").write_text(
            f'"""Operations as {environment.environment} receives them. '
            'Generated; do not edit."""\n\n'
            f"FRAGMENTS = {_dict_lines(environment.fragments.items())}\n\n"
            f"OPERATIONS = {_dict_lines(operations)}\n",
            encoding="utf-8",
        )


def _write_availability(
    package_dir: Path, defaults: DefaultsReport, merged: MergedSchema
) -> None:
    """
    Write the fields and enum values some environment lacks, with the
    environments that have them.

    ``is_available`` and ``enum_values`` read the table at runtime; anything
    not listed is on every environment.
    """
    fields: dict[str, dict[str, tuple[str, ...]]] = {}
    for offset, class_name, attribute in defaults.placed:
        fields.setdefault(class_name, {})[attribute] = defaults.expected[
            offset
        ].environments
    enum_values: dict[str, dict[str, tuple[str, ...]]] = {}
    for definition in merged.document.definitions:
        if not isinstance(definition, EnumTypeDefinitionNode):
            continue
        for value in definition.values or ():
            envs = environments(value)
            if envs is None:
                envs = environments(definition)
            if envs is not None:
                enum_values.setdefault(definition.name.value, {})[value.name.value] = (
                    envs
                )
    (package_dir / "availability.py").write_text(
        '"""Fields and enum values some environment lacks. '
        'Generated; do not edit."""\n\n'
        f"FIELDS = {_dict_lines(sorted(fields.items()))}\n\n"
        f"ENUM_VALUES = {_dict_lines(sorted(enum_values.items()))}\n",
        encoding="utf-8",
    )


_SCHEMA_DATE = re.compile(r"\A# schema-date: (\d{4}-\d{2}-\d{2})$", re.MULTILINE)


def schema_body(text: str) -> str:
    """
    Return a schema file's text without its ``# schema-date`` line.

    Parameters
    ----------
    text : str
        The schema file's text.

    Returns
    -------
    str
        The schema itself, so two downloads of the same schema compare equal
        whatever day they were made.
    """
    return _SCHEMA_DATE.sub("", text, count=1).lstrip("\n")


def _dict_lines(items) -> str:
    """
    Return a dict literal with one entry per line, so schema PRs diff per entry.
    """
    lines = "".join(f"    {key!r}: {value!r},\n" for key, value in items)
    return "{\n" + lines + "}"


@app.command()
def main() -> None:
    """
    Build the generated client and the trimmed operations from the schemas.
    """
    paths = BuildPaths.for_repo(Path.cwd())
    try:
        with output.status("Building..."):
            result = build(paths)
    except BuildError as exc:
        output.fail(escape(str(exc)))
        raise typer.Exit(code=1) from exc

    output.success(f"Wrote {paths.package_dir}")
    # Plain text, so it pastes into a PR body unchanged.
    typer.echo("\n" + result.merge_summary + "\n" + result.trim_summary)


if __name__ == "__main__":
    app()
