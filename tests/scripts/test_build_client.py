"""
Tests for the client build pipeline, driven through ``build``.
"""

import ast
import asyncio
import dataclasses
import importlib
import json
import shutil
import uuid
from pathlib import Path

import httpx
import pytest
from pydantic import ValidationError

from gpp_client.environment import GPPEnvironment
from gpp_client.generated_tables import use_generated_package
from gpp_client.trimmed_operations import TrimmedOperation, find_trimmed_operation
from graphql import GraphQLScalarType, build_schema
from scripts.build_client import (
    BuildError,
    BuildPaths,
    KindConflict,
    Pairing,
    Rename,
    TypeConflict,
    build,
)

REPO_ROOT = Path(__file__).resolve().parents[2]

# Valid on any schema, so merge-only tests need no operations of their own.
_TYPENAME_OPERATION = "query typenameOnly { __typename }\n"


def _write_schemas(
    root: Path, operations: str = _TYPENAME_OPERATION, **sdl_by_environment: str
) -> BuildPaths:
    stem = uuid.uuid4().hex[:12]
    schemas_dir = root / "packages" / f"schemas_{stem}"
    schemas_dir.mkdir(parents=True)
    (schemas_dir / "__init__.py").write_text("")
    for environment, sdl in sdl_by_environment.items():
        (schemas_dir / f"{environment}.graphql").write_text(sdl)
    operations_dir = root / "operations"
    operations_dir.mkdir(parents=True, exist_ok=True)
    (operations_dir / "operations.graphql").write_text(operations)
    return BuildPaths(
        schemas_dir=schemas_dir,
        operations_dir=operations_dir,
        package_dir=root / "packages" / f"generated_{stem}",
        codegen_config=REPO_ROOT / "graphql" / "codegen.toml",
    )


@pytest.fixture(autouse=True)
def _generated_packages_importable(tmp_path, monkeypatch):
    monkeypatch.syspath_prepend(str(tmp_path / "packages"))


def _import_generated(paths: BuildPaths, module: str = "client"):
    return importlib.import_module(f"{paths.package_dir.name}.{module}")


def _sent_query(paths: BuildPaths, method: str, response_data: dict, **kwargs):
    """
    Call a generated client method and return the query it sent.
    """
    sent = []

    def handler(request: httpx.Request) -> httpx.Response:
        sent.append(json.loads(request.content)["query"])
        return httpx.Response(200, json={"data": response_data})

    module = _import_generated(paths)

    async def call():
        async with httpx.AsyncClient(transport=httpx.MockTransport(handler)) as http:
            client = module.GraphQLClient(url="http://gpp.test/odb", http_client=http)
            return await getattr(client, method)(**kwargs)

    result = asyncio.run(call())
    return sent[0], result


def _trimmed(paths: BuildPaths, environment: str, query: str):
    with use_generated_package(paths.package_dir.name, paths.schemas_dir.name):
        return find_trimmed_operation(GPPEnvironment(environment), query)


def _merged(result):
    return build_schema(result.merged_sdl)


def _environments(node) -> list[str] | None:
    for directive in node.directives:
        if directive.name.value == "environments":
            return [value.value for value in directive.arguments[0].value.values]
    return None


def test_field_only_on_production_is_nullable_and_marked(tmp_path):
    base = "type Query { program: Program }\n"
    paths = _write_schemas(
        tmp_path,
        development=base + "type Program { id: ID! }",
        production=base + "type Program { id: ID! reference: String! }",
    )

    result = build(paths)

    field = _merged(result).type_map["Program"].fields["reference"]
    assert str(field.type) == "String"
    assert _environments(field.ast_node) == ["production"]


def _write(path: Path, text: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text)


def _checkout(
    root: Path, schemas_dir: Path, sdl: str = "type Query { a: Int }\n"
) -> None:
    """
    Lay out a checkout with one schema per environment under ``schemas_dir``.
    """
    for environment in ("development", "production"):
        _write(schemas_dir / f"{environment}.graphql", sdl)
    _write(root / "graphql" / "operations" / "operations.graphql", _TYPENAME_OPERATION)
    shutil.copyfile(
        REPO_ROOT / "graphql" / "codegen.toml", root / "graphql" / "codegen.toml"
    )


def _files(root: Path) -> set[Path]:
    return {
        path.relative_to(root)
        for path in root.rglob("*")
        if path.is_file() and "__pycache__" not in path.parts
    }


def test_repo_build_reads_the_package_schemas_and_writes_only_the_generated_package(
    tmp_path,
):
    root = tmp_path / "repo"
    _checkout(root, root / "src" / "gpp_client" / "schemas")
    paths = BuildPaths.for_repo(root)
    before = _files(root)

    build(paths)

    assert (paths.package_dir / "client.py").is_file()
    written = _files(root) - before
    assert written
    assert all(
        path.is_relative_to(paths.package_dir.relative_to(root)) for path in written
    )
    assert not (paths.package_dir / "schemas").exists()


def test_repo_build_ignores_schemas_at_the_old_location(tmp_path):
    root = tmp_path / "repo"
    _checkout(root, root / "graphql" / "schemas")

    with pytest.raises(
        BuildError, match=r"src/gpp_client/schemas/development\.graphql"
    ):
        build(BuildPaths.for_repo(root))


def _build_two(tmp_path, development: str, production: str):
    paths = _write_schemas(tmp_path, development=development, production=production)
    result = build(paths)
    return result, _merged(result)


def test_output_nullability_that_differs_becomes_nullable(tmp_path):
    _, schema = _build_two(
        tmp_path,
        development="type Query { names: [String]! }",
        production="type Query { names: [String!] }",
    )

    field = schema.query_type.fields["names"]
    assert str(field.type) == "[String]"
    assert _environments(field.ast_node) is None


def test_input_and_argument_nullability_that_differs_becomes_optional(tmp_path):
    _, schema = _build_two(
        tmp_path,
        development="type Query { find(id: ID, where: Where!): Int }\n"
        "input Where { name: String! }",
        production="type Query { find(id: ID!, where: Where!): Int }\n"
        "input Where { name: String }",
    )

    find = schema.query_type.fields["find"]
    assert str(find.args["id"].type) == "ID"
    assert str(find.args["where"].type) == "Where!"
    assert str(schema.type_map["Where"].fields["name"].type) == "String"


def test_input_parts_on_some_environments_become_optional_and_marked(tmp_path):
    _, schema = _build_two(
        tmp_path,
        development="type Query { find(id: ID!, limit: Int!): Int }\n"
        "input Where { name: String! sort: String! }",
        production="type Query { find(id: ID!): Int }\ninput Where { name: String! }",
    )

    limit = schema.query_type.fields["find"].args["limit"]
    sort = schema.type_map["Where"].fields["sort"]
    assert str(limit.type) == "Int"
    assert _environments(limit.ast_node) == ["development"]
    assert str(sort.type) == "String"
    assert _environments(sort.ast_node) == ["development"]
    assert str(schema.type_map["Where"].fields["name"].type) == "String!"


def test_availability_marks_root_operations_types_and_enum_values(tmp_path):
    common = "enum Code { OK }\n"
    _, schema = _build_two(
        tmp_path,
        development="type Query { a: Int clone: Clone }\ntype Clone { id: ID! }\n"
        "enum Code { OK WARN }",
        production="type Query { a: Int }\n" + common,
    )

    clone_type = schema.type_map["Clone"]
    assert _environments(schema.query_type.fields["clone"].ast_node) == ["development"]
    assert _environments(clone_type.ast_node) == ["development"]
    assert _environments(clone_type.fields["id"].ast_node) == ["development"]
    assert str(clone_type.fields["id"].type) == "ID!"
    assert _environments(schema.type_map["Code"].values["WARN"].ast_node) == [
        "development"
    ]
    assert _environments(schema.type_map["Code"].values["OK"].ast_node) is None
    assert _environments(schema.query_type.fields["a"].ast_node) is None


def test_type_of_a_different_kind_takes_production_and_drops_development_uses(
    tmp_path,
):
    result, schema = _build_two(
        tmp_path,
        development="type Query { a: Mode c: Mode find(mode: Mode): Int items: Item }\n"
        "enum Mode { FAST }\ntype Thing { v: Int }\ntype Other { w: Int }\n"
        "union Item = Thing | Other",
        production="type Query { a: Mode find: Int items: Item }\n"
        "scalar Mode\nscalar Thing\ntype Other { w: Int }\nunion Item = Other",
    )

    assert isinstance(schema.type_map["Mode"], GraphQLScalarType)
    assert _environments(schema.type_map["Mode"].ast_node) == ["production"]
    assert "c" not in schema.query_type.fields
    assert "mode" not in schema.query_type.fields["find"].args
    assert [t.name for t in schema.type_map["Item"].types] == ["Other"]
    assert result.kind_conflicts == (
        KindConflict(
            name="Mode",
            kinds=(("development", "enum"), ("production", "scalar")),
            dropped=("Query.c", "Query.find(mode:)"),
        ),
        KindConflict(
            name="Thing",
            kinds=(("development", "object"), ("production", "scalar")),
            dropped=("Item = Thing",),
        ),
    )


def test_type_that_differs_takes_production_type_and_is_listed(tmp_path):
    result, schema = _build_two(
        tmp_path,
        development="type Query { a: Int b: String find(id: ID!, where: Where): Int }\n"
        "input Where { name: String! page: Int }",
        production="type Query { a: Int b: Int! find(id: Int, where: Where): Int }\n"
        "input Where { name: [String!] page: Int }",
    )

    query = schema.query_type
    assert str(query.fields["b"].type) == "Int"
    assert _environments(query.fields["b"].ast_node) == ["production"]
    assert str(query.fields["find"].args["id"].type) == "Int"
    assert _environments(query.fields["find"].args["id"].ast_node) == ["production"]
    assert _environments(query.fields["find"].ast_node) is None
    assert str(schema.type_map["Where"].fields["name"].type) == "[String!]"
    assert _environments(schema.type_map["Where"].ast_node) is None
    assert result.conflicts == (
        TypeConflict("Query.b", (("development", "String"), ("production", "Int!"))),
        TypeConflict(
            "Query.find(id:)", (("development", "ID!"), ("production", "Int"))
        ),
        TypeConflict(
            "Where.name", (("development", "String!"), ("production", "[String!]"))
        ),
    )


def test_field_typed_by_a_kind_conflict_on_both_environments_is_production_only(
    tmp_path,
):
    _, schema = _build_two(
        tmp_path,
        development="type Query { a: Mode }\nenum Mode { FAST }",
        production="type Query { a: Mode }\nscalar Mode",
    )

    assert _environments(schema.query_type.fields["a"].ast_node) == ["production"]


def _variant_sdl(name: str) -> str:
    return f"type Query {{ find(variant: {name}): Int }}\ninput {name} {{ bin: Int! }}"


def test_renamed_input_type_is_paired_under_development_name(tmp_path):
    result, schema = _build_two(
        tmp_path,
        development=_variant_sdl("ImagingVariantInput"),
        production=_variant_sdl("GmosImagingVariantInput"),
    )

    assert "GmosImagingVariantInput" not in schema.type_map
    variant = schema.type_map["ImagingVariantInput"]
    assert _environments(variant.ast_node) is None
    assert _environments(variant.fields["bin"].ast_node) is None
    assert str(schema.query_type.fields["find"].args["variant"].type) == (
        "ImagingVariantInput"
    )
    assert result.pairing.reverse == {"ImagingVariantInput": "GmosImagingVariantInput"}


def test_pairing_follows_a_rename_into_the_renamed_type(tmp_path):
    result, schema = _build_two(
        tmp_path,
        development="type Query { a: New }\ntype New { x: NewInner }\n"
        "type NewInner { v: Int }",
        production="type Query { a: Old }\ntype Old { x: OldInner }\n"
        "type OldInner { v: Int }",
    )

    assert result.pairing.renames == (
        Rename("Old", "New", ("Query.a",)),
        Rename("OldInner", "NewInner", ("New.x",)),
    )
    assert {"Old", "OldInner"}.isdisjoint(schema.type_map)
    assert _environments(schema.type_map["NewInner"].ast_node) is None


def test_no_rename_when_either_environment_still_has_the_other_name(tmp_path):
    result, schema = _build_two(
        tmp_path,
        development="type Query { a: Kept b: Fresh }\ntype Kept { z: Int }\n"
        "type Fresh { y: Int }\ntype Gone { y: Int }",
        production="type Query { a: Old b: Gone }\ntype Old { x: Int }\n"
        "type Kept { x: Int }\ntype Gone { y: Int }",
    )

    assert result.pairing == Pairing()
    assert _environments(schema.query_type.fields["a"].ast_node) == ["production"]
    assert _environments(schema.query_type.fields["b"].ast_node) == ["production"]
    assert _environments(schema.type_map["Old"].ast_node) == ["production"]


def test_no_rename_across_list_depth_or_kind(tmp_path):
    result, _ = _build_two(
        tmp_path,
        development="type Query { a: [Deep] b: Shape }\ntype Deep { x: Int }\n"
        "interface Shape { x: Int }",
        production="type Query { a: OldDeep b: OldShape }\ntype OldDeep { x: Int }\n"
        "type OldShape { x: Int }",
    )

    assert result.pairing == Pairing()


def test_renames_never_chain(tmp_path):
    result, _ = _build_two(
        tmp_path,
        development="type Query { a: B b: C }\ntype B { x: Int }\ntype C { x: Int }",
        production="type Query { a: A b: B }\ntype A { x: Int }\ntype B { x: Int }",
    )

    assert result.pairing == Pairing()


def test_ambiguous_votes_and_collisions_make_no_rename_and_are_listed(tmp_path):
    result, schema = _build_two(
        tmp_path,
        development="type Query { a: A1 b: A2 c: A2 d: B e: B }\n"
        "type A1 { x: Int }\ntype A2 { x: Int }\ntype B { x: Int }",
        production="type Query { a: OldA b: OldA c: OldA d: OldB e: OldC }\n"
        "type OldA { x: Int }\ntype OldB { x: Int }\ntype OldC { x: Int }",
    )

    assert result.pairing == Pairing(
        renames=(),
        ambiguous=("OldA: A2 (2), A1 (1)",),
        collisions=("OldB -> B", "OldC -> B"),
    )
    assert {"OldA", "OldB", "OldC"} <= set(schema.type_map)


def test_descriptions_come_from_development_where_it_has_the_element(tmp_path):
    _, schema = _build_two(
        tmp_path,
        development='"Dev type." type Query { "Dev field." a: Int b: String '
        'c(id: ID): Int }\n"Dev enum." enum Code { "Dev value." OK }',
        production='"Prod type." type Query { "Prod field." a: Int '
        '"Prod only." b: Int "Prod c." c("Prod arg." id: ID): Int }\n'
        '"Prod enum." enum Code { "Prod value." OK "Prod warn." WARN }',
    )

    query = schema.query_type
    assert query.description == "Dev type."
    assert query.fields["a"].description == "Dev field."
    assert query.fields["b"].description == "Prod only."
    assert query.fields["c"].description is None
    assert query.fields["c"].args["id"].description is None
    assert schema.type_map["Code"].description == "Dev enum."
    assert schema.type_map["Code"].values["OK"].description == "Dev value."
    assert schema.type_map["Code"].values["WARN"].description == "Prod warn."


def test_two_builds_write_identical_files(tmp_path):
    paths = _write_schemas(
        tmp_path,
        development="type Query { a: Int b: Int c(x: Int): Int }\nenum E { X Y }",
        production="type Query { a: Int! d: Int }\nenum E { X Z }",
    )

    first = build(paths)
    first_files = {p: p.read_bytes() for p in paths.package_dir.rglob("*.py")}
    second = build(paths)

    assert second.merged_sdl == first.merged_sdl
    assert {p: p.read_bytes() for p in paths.package_dir.rglob("*.py")} == first_files


def test_missing_environment_schema_fails(tmp_path):
    paths = _write_schemas(tmp_path, development="type Query { a: Int }")

    with pytest.raises(BuildError, match="production.graphql"):
        build(paths)


def test_union_and_interface_members_are_combined(tmp_path):
    shared = "interface Node { id: ID! }\ntype A implements Node { id: ID! }\n"
    _, schema = _build_two(
        tmp_path,
        development=shared + "type B implements Node { id: ID! }\n"
        "union Item = A | B\ntype Query { item: Item node: Node }",
        production=shared + "union Item = A\ntype Query { item: Item node: Node }",
    )

    assert [t.name for t in schema.type_map["Item"].types] == ["A", "B"]
    assert [t.name for t in schema.get_possible_types(schema.type_map["Node"])] == [
        "A",
        "B",
    ]
    assert _environments(schema.type_map["B"].ast_node) == ["development"]


def test_empty_environment_schema_fails_naming_the_environment(tmp_path):
    paths = _write_schemas(
        tmp_path,
        development="type Query { a: Int }",
        production="",
    )

    with pytest.raises(BuildError, match="production"):
        build(paths)


def test_field_only_on_production_is_trimmed_from_other_environments(tmp_path):
    query = "type Query { program: Program }\n"
    paths = _write_schemas(
        tmp_path,
        operations="query getProgram { program { id reference } }",
        development=query + "type Program { id: ID! }",
        production=query + "type Program { id: ID! reference: String! }",
    )

    build(paths)

    sent, _ = _sent_query(
        paths, "get_program", {"program": {"id": "p-1", "reference": "G-1"}}
    )
    development = _trimmed(paths, "development", sent)
    production = _trimmed(paths, "production", sent)
    assert development.document == "query getProgram {\n  program {\n    id\n  }\n}"
    assert production == TrimmedOperation(name="getProgram", document=sent)


def test_copy_is_stored_only_where_it_differs_from_the_generated_string(tmp_path):
    query = "type Query { program: Program count: Int }\n"
    paths = _write_schemas(
        tmp_path,
        operations="query getProgram { program { ...Details } }\n"
        "query count { count }\n"
        "fragment Details on Program { id reference }",
        development=query + "type Program { id: ID! }",
        production=query + "type Program { id: ID! reference: String! }",
    )

    build(paths)

    stored = {
        env: (paths.package_dir / "trimmed" / f"{env}.py").read_text()
        for env in ("development", "production")
    }
    assert "getProgram" in stored["development"]
    assert "Details" in stored["development"]
    assert "count" not in stored["development"]
    assert "getProgram" not in stored["production"]
    assert "Details" not in stored["production"]
    sent, _ = _sent_query(paths, "count", {"count": 1})
    assert _trimmed(paths, "development", sent) == TrimmedOperation(
        name="count", document=sent
    )


def test_argument_an_environment_lacks_is_removed_with_its_variable(tmp_path):
    paths = _write_schemas(
        tmp_path,
        operations="query listPrograms($limit: Int, $after: ID) "
        "{ programs(limit: $limit, after: $after) }",
        development="type Query { programs(limit: Int, after: ID): [ID!]! }",
        production="type Query { programs(limit: Int): [ID!]! }",
    )

    build(paths)

    sent, _ = _sent_query(
        paths, "list_programs", {"programs": []}, limit=1, after="p-1"
    )
    assert _trimmed(paths, "production", sent).document == (
        "query listPrograms($limit: Int) {\n  programs(limit: $limit)\n}"
    )
    assert "after: $after" in _trimmed(paths, "development", sent).document


_ITEMS_SDL = "type Query { items: [Item!]! }\ntype A { id: ID! }\n"


def test_inline_fragment_and_spread_on_a_missing_type_are_removed(tmp_path):
    paths = _write_schemas(
        tmp_path,
        operations="query items { items { ... on A { id } ... on B { id } "
        "...BFields } }\nfragment BFields on B { name }",
        development=_ITEMS_SDL + "type B { id: ID! name: String }\nunion Item = A | B",
        production=_ITEMS_SDL + "union Item = A",
    )

    build(paths)

    sent, _ = _sent_query(paths, "items", {"items": []})
    assert _trimmed(paths, "production", sent).document == (
        "query items {\n  items {\n    __typename\n    ... on A {\n      id\n    }\n"
        "  }\n}"
    )
    assert _trimmed(paths, "development", sent).document == sent


_EXECUTION_SDL = "type Query { execution: Execution }\n"
_DEVELOPMENT_EXECUTION = (
    _EXECUTION_SDL + "type Execution { state: String isCustomized: Boolean! }"
)
_PRODUCTION_EXECUTION = _EXECUTION_SDL + "type Execution { state: String }"


def test_selection_emptied_by_trimming_gets_typename(tmp_path):
    paths = _write_schemas(
        tmp_path,
        operations="query customized { execution { isCustomized } }",
        development=_DEVELOPMENT_EXECUTION,
        production=_PRODUCTION_EXECUTION,
    )

    build(paths)

    sent, _ = _sent_query(paths, "customized", {"execution": {"isCustomized": True}})
    assert _trimmed(paths, "production", sent).document == (
        "query customized {\n  execution {\n    __typename\n  }\n}"
    )


def test_only_environment_specific_fields_default_to_none(tmp_path):
    paths = _write_schemas(
        tmp_path,
        operations="query execution { execution { state isCustomized } }",
        development=_DEVELOPMENT_EXECUTION,
        production=_PRODUCTION_EXECUTION,
    )

    build(paths)

    _, result = _sent_query(paths, "execution", {"execution": {"state": None}})
    assert result.execution.is_customized is None
    with pytest.raises(ValidationError, match="execution.state"):
        _sent_query(paths, "execution", {"execution": {}})


def test_operation_whose_root_field_is_missing_is_unavailable(tmp_path):
    clone = "type Clone { id: ID! }\n"
    paths = _write_schemas(
        tmp_path,
        operations="query cloneAndCount { clone { id } count }",
        development="type Query { clone: Clone count: Int }\n" + clone,
        production="type Query { count: Int }",
    )

    build(paths)

    sent, _ = _sent_query(paths, "clone_and_count", {"clone": None, "count": 1})
    assert _trimmed(paths, "production", sent) == TrimmedOperation(
        name="cloneAndCount", document=None
    )
    assert _trimmed(paths, "development", sent).document is not None


def test_trimmed_copy_invalid_on_its_environment_fails_the_build(tmp_path):
    query = "type Query { find(where: Where): Int }\n"
    paths = _write_schemas(
        tmp_path,
        operations='query findSorted { find(where: {sort: "name"}) }',
        development=query + "input Where { name: String sort: String }",
        production=query + "input Where { name: String }",
    )

    with pytest.raises(BuildError) as error:
        build(paths)

    message = str(error.value)
    assert "findSorted on production" in message
    assert "'sort'" in message
    assert "on development" not in message


def test_operation_selecting_a_field_whose_type_differs_builds(tmp_path):
    paths = _write_schemas(
        tmp_path,
        operations="query ab { a b }",
        development="type Query { a: Int b: String }",
        production="type Query { a: Int b: Int }",
    )

    build(paths)

    _, result = _sent_query(paths, "ab", {"a": 1, "b": 2})
    assert result.b == 2


def test_field_on_no_environment_fails_the_build(tmp_path):
    paths = _write_schemas(
        tmp_path,
        operations="query typo { a nmae }",
        development="type Query { a: Int name: String }",
        production="type Query { a: Int }",
    )

    with pytest.raises(BuildError, match="Cannot query field 'nmae' on type 'Query'"):
        build(paths)


def test_query_builder_call_reusing_an_operation_name_is_not_that_operation(
    tmp_path,
):
    query = "type Query { program: Program }\n"
    paths = _write_schemas(
        tmp_path,
        operations="query getProgram { program { id reference } }",
        development=query + "type Program { id: ID! reference: String }",
        production=query + "type Program { id: ID! }",
    )
    build(paths)
    queries = _import_generated(paths, "custom_queries")
    fields = _import_generated(paths, "custom_fields")
    sent = []

    def handler(request: httpx.Request) -> httpx.Response:
        sent.append(json.loads(request.content)["query"])
        return httpx.Response(200, json={"data": {"program": {"id": "p-1"}}})

    async def call():
        async with httpx.AsyncClient(transport=httpx.MockTransport(handler)) as http:
            client = _import_generated(paths).GraphQLClient(
                url="http://gpp.test/odb", http_client=http
            )
            await client.query(
                queries.Query.program().fields(fields.ProgramFields.id),
                operation_name="getProgram",
            )

    asyncio.run(call())

    assert "getProgram" in sent[0]
    assert _trimmed(paths, "production", sent[0]) is None


def test_trimmed_fragment_is_stored_once_per_environment(tmp_path):
    query = "type Query { program: Program programs: [Program!]! }\n"
    paths = _write_schemas(
        tmp_path,
        operations="query one { program { ...Details } }\n"
        "query many { programs { ...Details } }\n"
        "fragment Details on Program { id reference }",
        development=query + "type Program { id: ID! reference: String }",
        production=query + "type Program { id: ID! }",
    )

    build(paths)

    one, _ = _sent_query(paths, "one", {"program": None})
    many, _ = _sent_query(paths, "many", {"programs": []})
    fragment = "fragment Details on Program {\n  id\n}"
    assert _trimmed(paths, "production", one).document.endswith(fragment)
    assert _trimmed(paths, "production", many).document.endswith(fragment)
    stored = (paths.package_dir / "trimmed" / "production.py").read_text()
    assert stored.count("fragment Details") == 1


def test_trim_summary_lists_what_each_environment_does_not_receive(tmp_path):
    query = "type Program { id: ID! reference: String }\n"
    paths = _write_schemas(
        tmp_path,
        operations="query one($after: ID) { programs(after: $after) { ...Details } }\n"
        "query two { clone }\n"
        "fragment Details on Program { id reference }",
        development=query
        + "type Query { programs(after: ID): [Program!]! clone: Int }",
        production="type Program { id: ID! }\ntype Query { programs: [Program!]! }",
    )

    result = build(paths)

    assert result.trim_summary == (
        "### Trim summary\n"
        "\n"
        "**development**: nothing trimmed.\n"
        "\n"
        "**production**\n"
        "- Unavailable: `two`\n"
        "- `Program.reference` removed from `Details`\n"
        "- `Query.programs(after:)` removed from `one`\n"
    )


def test_merge_summary_lists_renames_conflicts_and_refused_votes(tmp_path):
    result, _ = _build_two(
        tmp_path,
        development="type Query { find(variant: ImagingVariantInput): Int b: String "
        "a: Mode c: Mode p: A1 q: A2 r: A2 s: B t: B }\n"
        "input ImagingVariantInput { bin: Int! }\nenum Mode { FAST }\n"
        "type A1 { x: Int }\ntype A2 { x: Int }\ntype B { x: Int }",
        production="type Query { find(variant: GmosImagingVariantInput): Int b: Int "
        "a: Mode p: OldA q: OldA r: OldA s: OldB t: OldC }\n"
        "input GmosImagingVariantInput { bin: Int! }\nscalar Mode\n"
        "type OldA { x: Int }\ntype OldB { x: Int }\ntype OldC { x: Int }",
    )

    assert result.merge_summary == (
        "### Merge summary\n"
        "\n"
        "- Renamed `GmosImagingVariantInput` to `ImagingVariantInput` "
        "(`Query.find(variant:)`)\n"
        "- Conflict `Query.b`: String on development, Int on production; "
        "production's type used\n"
        "- Conflict `Query.a`: Mode on development, Mode on production; "
        "production's type used\n"
        "- Conflict `Query.p`: A1 on development, OldA on production; "
        "production's type used\n"
        "- Conflict `Query.q`: A2 on development, OldA on production; "
        "production's type used\n"
        "- Conflict `Query.r`: A2 on development, OldA on production; "
        "production's type used\n"
        "- Conflict `Query.s`: B on development, OldB on production; "
        "production's type used\n"
        "- Conflict `Query.t`: B on development, OldC on production; "
        "production's type used\n"
        "- Kind conflict `Mode`: enum on development, scalar on production; "
        "production's definition used, dropped `Query.c`\n"
        "- Ambiguous `OldA: A2 (2), A1 (1)`; not renamed\n"
        "- Collision `OldB -> B`; not renamed\n"
        "- Collision `OldC -> B`; not renamed\n"
    )


def test_merge_summary_without_differences_says_so(tmp_path):
    result, _ = _build_two(
        tmp_path,
        development="type Query { a: Int }",
        production="type Query { a: Int }",
    )

    assert result.merge_summary == (
        "### Merge summary\n\nNo renames, conflicts or refused votes.\n"
    )


def test_build_writes_no_packaged_environment_marker(tmp_path):
    paths = _write_schemas(
        tmp_path,
        development="type Query { a: Int }",
        production="type Query { a: Int }",
    )

    build(paths)

    assert not (paths.package_dir / "package_environment.py").exists()


def test_operations_folder_without_operations_fails_the_build(tmp_path):
    paths = _write_schemas(
        tmp_path,
        development="type Query { a: Int }",
        production="type Query { a: Int }",
    )
    (paths.operations_dir / "operations.graphql").unlink()

    with pytest.raises(BuildError, match="Codegen failed"):
        build(paths)


def _with_extra_plugin(
    paths: BuildPaths, monkeypatch, source: str, after: str
) -> BuildPaths:
    """
    Return paths whose codegen config adds a plugin right after ``after``.
    """
    plugins_dir = paths.package_dir.parent.parent / "test_plugins"
    plugins_dir.mkdir()
    module = f"extra_plugin_{uuid.uuid4().hex[:12]}"
    (plugins_dir / f"{module}.py").write_text(source)
    monkeypatch.syspath_prepend(str(plugins_dir))
    config = paths.codegen_config.read_text().replace(
        f'"custom_plugins.{after}",',
        f'"custom_plugins.{after}",\n    "{module}.ExtraPlugin",',
    )
    config_path = plugins_dir / "codegen.toml"
    config_path.write_text(config)
    return dataclasses.replace(paths, codegen_config=config_path)


def test_generated_operation_the_lookup_cannot_find_fails_the_build(
    tmp_path, monkeypatch
):
    paths = _write_schemas(
        tmp_path,
        operations="query count { count }",
        development="type Query { count: Int }",
        production="type Query { count: Int }",
    )
    rewriting = _with_extra_plugin(
        paths,
        monkeypatch,
        "from ariadne_codegen.plugins.base import Plugin\n\n\n"
        "class ExtraPlugin(Plugin):\n"
        "    def generate_operation_str(self, operation_str, operation_definition):\n"
        "        return operation_str + '\\n# rewritten'\n",
        after="CaptureOperationsPlugin",
    )

    with pytest.raises(BuildError) as error:
        build(rewriting)

    assert str(error.value) == (
        "The generated client sends operations the trimmed lookup cannot find:\n"
        "  count on development, production"
    )


def test_generated_client_without_readable_queries_fails_the_build(
    tmp_path, monkeypatch
):
    paths = _write_schemas(
        tmp_path,
        operations="query count { count }",
        development="type Query { count: Int }",
        production="type Query { count: Int }",
    )
    unwrapping = _with_extra_plugin(
        paths,
        monkeypatch,
        "from ariadne_codegen.plugins.base import Plugin\n\n\n"
        "class ExtraPlugin(Plugin):\n"
        "    def generate_client_code(self, generated_code):\n"
        "        return generated_code.replace('gql(', 'str(')\n",
        after="CaptureOperationsPlugin",
    )

    with pytest.raises(BuildError, match="found 0 of 1 generated operations"):
        build(unwrapping)


def test_environment_specific_field_without_none_default_fails_the_build(
    tmp_path, monkeypatch
):
    paths = _write_schemas(
        tmp_path,
        operations="query execution { execution { state isCustomized } }",
        development=_DEVELOPMENT_EXECUTION,
        production=_PRODUCTION_EXECUTION,
    )
    stripping = _with_extra_plugin(
        paths,
        monkeypatch,
        "from ariadne_codegen.plugins.base import Plugin\n\n\n"
        "class ExtraPlugin(Plugin):\n"
        "    def generate_result_field(self, field_implementation, *_args, **_kw):\n"
        "        field_implementation.value = None\n"
        "        return field_implementation\n",
        after="EnvironmentDefaultsPlugin",
    )

    with pytest.raises(BuildError) as error:
        build(stripping)

    assert str(error.value) == (
        "Environment-specific fields did not get a None default:\n"
        "  Execution.isCustomized in execution"
    )


def test_development_only_method_docstring_names_its_environments(tmp_path):
    clone = "type Clone { id: ID! }\n"
    paths = _write_schemas(
        tmp_path,
        operations="query cloneOne { clone { id } }\nquery count { count }",
        development="type Query { clone: Clone count: Int }\n" + clone,
        production="type Query { count: Int }",
    )

    build(paths)

    client = _import_generated(paths).GraphQLClient
    assert "Available on: development" in (client.clone_one.__doc__ or "")
    assert "Available on" not in (client.count.__doc__ or "")


def _attribute_docs(paths: BuildPaths) -> dict[tuple[str, str], str]:
    """
    Return each generated class attribute's docstring, as editors and Sphinx read it.
    """
    docs = {}
    for module in paths.package_dir.glob("*.py"):
        for node in ast.walk(ast.parse(module.read_text())):
            if not isinstance(node, ast.ClassDef):
                continue
            for statement, following in zip(node.body, node.body[1:]):
                target = getattr(statement, "target", None) or (
                    statement.targets[0] if isinstance(statement, ast.Assign) else None
                )
                if (
                    isinstance(target, ast.Name)
                    and isinstance(following, ast.Expr)
                    and isinstance(following.value, ast.Constant)
                ):
                    docs[node.name, target.id] = following.value.value
    return docs


def test_production_only_result_field_docstring_names_production(tmp_path):
    query = "type Query { program: Program }\n"
    paths = _write_schemas(
        tmp_path,
        operations="query getProgram { program { id reference } }",
        development=query + "type Program { id: ID! }",
        production=query + "type Program { id: ID! reference: String! }",
    )

    build(paths)

    docs = _attribute_docs(paths)
    assert docs["GetProgramProgram", "reference"] == "Available on: production."
    assert ("GetProgramProgram", "id") not in docs


def test_input_field_and_enum_value_docstrings_name_their_environments(tmp_path):
    query = "type Query { find(where: Where, code: Code): Int }\n"
    paths = _write_schemas(
        tmp_path,
        operations="query find($where: Where, $code: Code) "
        "{ find(where: $where, code: $code) }",
        development=query + "input Where { name: String sort: String }\n"
        "enum Code { OK WARN }",
        production=query + "input Where { name: String }\nenum Code { OK }",
    )

    build(paths)

    docs = _attribute_docs(paths)
    assert docs["Where", "sort"] == "Available on: development."
    assert docs["Code", "WARN"] == "Available on: development."
    assert ("Where", "name") not in docs
    assert ("Code", "OK") not in docs


def test_availability_joins_the_schema_description_in_one_docstring(tmp_path):
    query = "type Query { find(where: Where): Int }\n"
    described = query + 'input Where { name: String\n "Sort key." sort: String }'
    paths = _write_schemas(
        tmp_path,
        operations="query find($where: Where) { find(where: $where) }",
        development=described,
        production=query + "input Where { name: String }",
    )

    build(paths)

    assert _attribute_docs(paths)["Where", "sort"] == (
        "Available on: development.\n\nSort key."
    )


def test_environment_specific_enum_and_input_type_docstrings(tmp_path):
    query = "type Query { find(where: Where): Int }\n"
    development = (
        "type Query { find(where: Where, mode: Mode): Int }\n"
        "input Where { name: String }\nenum Mode { ALL NONE }"
    )
    paths = _write_schemas(
        tmp_path,
        operations="query find($where: Where) { find(where: $where) }",
        development=development,
        production=query + "input Where { name: String }",
    )

    build(paths)

    enums = _import_generated(paths, "enums")
    inputs = _import_generated(paths, "input_types")
    assert enums.Mode.__doc__ == "Available on: development."
    assert "Available on" not in (inputs.Where.__doc__ or "")
