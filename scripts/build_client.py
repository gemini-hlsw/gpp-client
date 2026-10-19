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
import shutil
import tempfile
import tomllib
from dataclasses import dataclass
from pathlib import Path

import typer
from ariadne_codegen.exceptions import CodeGenException
from ariadne_codegen.main import client as run_ariadne_codegen
from ariadne_codegen.schema import load_graphql_files_from_path
from rich.markup import escape

from custom_plugins.capture_operations import CAPTURE_KEY
from custom_plugins.environment_defaults import DEFAULTS_KEY, DefaultsReport
from custom_plugins.environments import USER_ENVIRONMENTS
from gpp_client.cli import output
from gpp_client.trimmed_operations import lookup_trimmed_operation
from graphql import (
    FieldNode,
    GraphQLError,
    OperationDefinitionNode,
    TypeInfo,
    TypeInfoVisitor,
    Visitor,
    build_ast_schema,
    parse,
    visit,
)
from scripts.schema_merge import (
    MergedSchema,
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
        Elements left out of the merged schema because their type differs
        between environments.
    trim_summary : str
        What each environment does not receive, as Markdown for a PR body.
    """

    merged_sdl: str
    conflicts: tuple[TypeConflict, ...]
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
        Raised when a schema file is missing, the schemas cannot be merged, an
        operation selects a field whose type differs between environments or
        that no environment has, codegen fails, an environment-specific field
        did not get a ``None`` default, a trimmed operation is invalid on its
        environment, or the trimmed lookup misses a query the generated client
        sends.
    """
    merged = _merge(paths)
    _check_conflicting_selections(paths, merged)
    operation_strs, defaults = _run_codegen(paths, merged.sdl)
    _check_environment_defaults(paths.package_dir, defaults)
    schemas = {env: _environment_schema(paths, env) for env in USER_ENVIRONMENTS}
    trimmed = [
        trim_operations(env, schemas[env], operation_strs) for env in USER_ENVIRONMENTS
    ]
    errors = [error for environment in trimmed for error in environment.errors]
    if errors:
        raise BuildError(
            "Trimmed operations are invalid:\n" + "\n".join(f"  {e}" for e in errors)
        )
    generated = generated_operations(operation_strs)
    _check_lookup_finds_sent_operations(paths, generated, trimmed)
    _write_trimmed(paths.package_dir, generated, trimmed)
    return BuildResult(
        merged_sdl=merged.sdl,
        conflicts=merged.conflicts,
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
            {
                env: paths.schema_path(env).read_text(encoding="utf-8")
                for env in USER_ENVIRONMENTS
            }
        )
    except SchemaMergeError as exc:
        raise BuildError(str(exc)) from exc


def _environment_schema(paths: BuildPaths, environment: str):
    return build_ast_schema(
        parse(paths.schema_path(environment).read_text(encoding="utf-8"))
    )


def _check_conflicting_selections(paths: BuildPaths, merged: MergedSchema) -> None:
    """
    Fail naming each selected field that rule 4 left out of the merged schema.
    """
    conflicts_by_field: dict[str, TypeConflict] = {}
    for conflict in merged.conflicts:
        conflicts_by_field.setdefault(conflict.coordinate.split("(")[0], conflict)
    if not conflicts_by_field:
        return
    try:
        document = parse(load_graphql_files_from_path(paths.operations_dir))
    except (CodeGenException, GraphQLError) as exc:
        raise BuildError(f"Operations could not be read: {exc}") from exc

    found: list[str] = []
    type_info = TypeInfo(build_ast_schema(merged.document))

    class _Finder(Visitor):
        definition = ""

        def enter_operation_definition(self, node, *_args) -> None:
            self.definition = node.name.value if node.name else "anonymous"

        def enter_fragment_definition(self, node, *_args) -> None:
            self.definition = node.name.value

        def enter_field(self, node: FieldNode, *_args) -> None:
            parent = type_info.get_parent_type()
            if parent is None:
                return
            conflict = conflicts_by_field.get(f"{parent.name}.{node.name.value}")
            if conflict is not None:
                listed = ", ".join(f"{t} on {env}" for env, t in conflict.types)
                found.append(f"  {conflict.coordinate} in {self.definition}: {listed}")

    visit(document, TypeInfoVisitor(type_info, _Finder()))
    if found:
        raise BuildError(
            "Operations select fields whose type differs between environments:\n"
            + "\n".join(found)
        )


def _run_codegen(
    paths: BuildPaths, merged_sdl: str
) -> tuple[list[str], DefaultsReport]:
    """
    Generate the client from the merged schema.

    Returns each embedded operation, and where ``None`` defaults went.
    """
    with paths.codegen_config.open("rb") as config_file:
        config = tomllib.load(config_file)
    captured: list[str] = []
    defaults = DefaultsReport()
    config["tool"]["gpp-client"] = {
        CAPTURE_KEY: captured,
        DEFAULTS_KEY: defaults,
    }

    if paths.package_dir.is_dir():
        shutil.rmtree(paths.package_dir)
    paths.package_dir.parent.mkdir(parents=True, exist_ok=True)
    with tempfile.TemporaryDirectory(prefix="gpp-client-merged-") as scratch:
        merged_path = Path(scratch) / "merged.graphql"
        merged_path.write_text(merged_sdl, encoding="utf-8")
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
    return captured, defaults


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
            description
            for offset, description in report.expected.items()
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


def _check_lookup_finds_sent_operations(
    paths: BuildPaths,
    generated: dict[str, str],
    trimmed: list[EnvironmentOperations],
) -> None:
    """
    Fail naming each query in the generated client that the lookup misses.

    The queries are read back from the generated client's source, so a change
    in how ariadne-codegen embeds them can never send an untrimmed query.
    """
    queries = _embedded_queries(paths.package_dir / "client.py")
    if len(queries) != len(generated):
        raise BuildError(
            "Reading gql(...) queries back from the generated client found "
            f"{len(queries)} of {len(generated)} generated operations."
        )
    missing: dict[str, list[str]] = {}
    for query in queries:
        for environment in trimmed:
            found = lookup_trimmed_operation(
                generated, environment.operations, environment.fragments, query
            )
            if found is None:
                missing.setdefault(_operation_name(query), []).append(
                    environment.environment
                )
    if missing:
        lines = [f"  {name} on {', '.join(envs)}" for name, envs in missing.items()]
        raise BuildError(
            "The generated client sends operations the trimmed lookup cannot find:\n"
            + "\n".join(lines)
        )


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


def _operation_name(query: str) -> str:
    for definition in parse(query).definitions:
        if isinstance(definition, OperationDefinitionNode) and definition.name:
            return definition.name.value
    return "anonymous"


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

    for conflict in result.conflicts:
        types = ", ".join(f"{t} on {env}" for env, t in conflict.types)
        output.warning(f"Left out {conflict.coordinate}: type differs ({types}).")
    output.success(f"Wrote {paths.package_dir}")
    # Plain text, so it pastes into a PR body unchanged.
    typer.echo("\n" + result.trim_summary)


if __name__ == "__main__":
    app()
