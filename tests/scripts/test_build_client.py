"""
Tests for the client build pipeline, driven through ``build``.
"""

import asyncio
import dataclasses
import importlib
import json
import pickle
import subprocess
import sys
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
from tests.scripts.helpers import (
    REPO_ROOT,
    TYPENAME_OPERATION,
    checkout,
    import_generated,
    send,
)


def _write_schemas(
    root: Path, operations: str = TYPENAME_OPERATION, **sdl_by_environment: str
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


def _trimmed(paths: BuildPaths, environment: str, query: str):
    with use_generated_package(paths.package_dir.name):
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


def _files(root: Path) -> set[Path]:
    return {
        path.relative_to(root)
        for path in root.rglob("*")
        if path.is_file() and "__pycache__" not in path.parts
    }


def test_repo_build_writes_only_the_generated_package(tmp_path):
    root = tmp_path / "repo"
    paths = checkout(root)
    before = _files(root)

    build(paths)

    assert (paths.package_dir / "client.py").is_file()
    written = _files(root) - before
    assert written
    assert all(
        path.is_relative_to(paths.package_dir.relative_to(root)) for path in written
    )
    assert not (root / "docs").exists()
    assert not (paths.package_dir / "schemas").exists()


def test_repo_build_ignores_schemas_at_the_old_location(tmp_path):
    root = tmp_path / "repo"
    checkout(root, schemas_dir=root / "graphql" / "schemas")

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
        Rename("Old", "New", ("Query.a",), "object"),
        Rename("OldInner", "NewInner", ("New.x",), "object"),
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

    sent = send(paths, "get_program", {"program": {"id": "p-1", "reference": "G-1"}})[
        0
    ]["query"]
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
    sent = send(paths, "count", {"count": 1})[0]["query"]
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

    sent = send(paths, "list_programs", {"programs": []}, limit=1, after="p-1")[0][
        "query"
    ]
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

    sent = send(paths, "items", {"items": []})[0]["query"]
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

    sent = send(paths, "customized", {"execution": {"isCustomized": True}})[0]["query"]
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

    _, result = send(paths, "execution", {"execution": {"state": None}})
    assert result.execution.is_customized is None
    with pytest.raises(ValidationError, match="execution.state"):
        send(paths, "execution", {"execution": {}})


def test_operation_whose_root_field_is_missing_is_unavailable(tmp_path):
    clone = "type Clone { id: ID! }\n"
    paths = _write_schemas(
        tmp_path,
        operations="query cloneAndCount { clone { id } count }",
        development="type Query { clone: Clone count: Int }\n" + clone,
        production="type Query { count: Int }",
    )

    build(paths)

    sent = send(paths, "clone_and_count", {"clone": None, "count": 1})[0]["query"]
    assert _trimmed(paths, "production", sent) == TrimmedOperation(
        name="cloneAndCount", document=None
    )
    assert _trimmed(paths, "development", sent).document is not None


def test_variable_an_environment_requires_is_not_retyped_and_fails_the_build(
    tmp_path,
):
    paths = _write_schemas(
        tmp_path,
        operations="query findOne($a: Int) { find(a: $a) }",
        development="type Query { find(a: Int): Int }",
        production="type Query { find(a: Int!): Int }",
    )

    with pytest.raises(BuildError) as error:
        build(paths)

    assert str(error.value) == (
        "Trimmed operations are invalid:\n"
        "  findOne on production: Variable '$a' of type 'Int' used in position "
        "expecting type 'Int!'."
    )


def test_operation_selecting_a_field_whose_type_differs_builds(tmp_path):
    paths = _write_schemas(
        tmp_path,
        operations="query ab { a b }",
        development="type Query { a: Int b: String }",
        production="type Query { a: Int b: Int }",
    )

    build(paths)

    _, result = send(paths, "ab", {"a": 1, "b": 2})
    assert result.b == 2


def test_selections_on_no_environment_fail_the_build_listing_each(tmp_path):
    paths = _write_schemas(
        tmp_path,
        operations="query typo { a nmae }\nquery other { ...Count }\n"
        "fragment Count on Query { cuont }",
        development="type Query { a: Int name: String count: Int }",
        production="type Query { a: Int count: Int }",
    )

    with pytest.raises(BuildError) as error:
        build(paths)

    assert str(error.value) == (
        "Operations select what no environment has:\n"
        "  typo: Cannot query field 'nmae' on type 'Query'. Did you mean 'name'?\n"
        "  Count: Cannot query field 'cuont' on type 'Query'. Did you mean 'count'?"
    )


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
    queries = import_generated(paths, "custom_queries")
    fields = import_generated(paths, "custom_fields")
    sent = []

    def handler(request: httpx.Request) -> httpx.Response:
        sent.append(json.loads(request.content)["query"])
        return httpx.Response(200, json={"data": {"program": {"id": "p-1"}}})

    async def call():
        async with httpx.AsyncClient(transport=httpx.MockTransport(handler)) as http:
            client = import_generated(paths).GraphQLClient(
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

    one = send(paths, "one", {"program": None})[0]["query"]
    many = send(paths, "many", {"programs": []})[0]["query"]
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
        "- `$after` removed from `one`\n"
        "- `Program.reference` removed from `Details`\n"
        "- `Query.programs(after:)` removed from `one`\n"
    )


_RENAMED_OPERATION = (
    "query renamed($w: NewW) { a(w: $w) { v { ...F } } }\nfragment F on NewV { x }"
)


def _renamed_sdl(input_name: str, type_name: str) -> str:
    return (
        f"type Query {{ a(w: {input_name}): A }}\ntype A {{ v: {type_name} }}\n"
        f"type {type_name} {{ x: Int }}\ninput {input_name} {{ q: Int }}"
    )


def test_production_copy_carries_production_names_for_renamed_types(tmp_path):
    paths = _write_schemas(
        tmp_path,
        operations=_RENAMED_OPERATION,
        development=_renamed_sdl("NewW", "NewV"),
        production=_renamed_sdl("OldW", "OldV"),
    )

    build(paths)

    sent = send(paths, "renamed", {"a": {"v": {"x": 1}}})[0]["query"]
    assert _trimmed(paths, "production", sent).document == (
        "query renamed($w: OldW) {\n  a(w: $w) {\n    v {\n      ...F\n    }\n  }\n}"
        "\n\nfragment F on OldV {\n  x\n}"
    )
    assert _trimmed(paths, "development", sent).document == sent


def test_conflicts_are_excluded_from_the_development_copy(tmp_path):
    paths = _write_schemas(
        tmp_path,
        operations="query ab($id: Int) "
        '{ a b find(id: $id, where: {name: ["x"], page: 1}) }',
        development="type Query { a: Int b: String find(id: ID, where: Where): Int }\n"
        "input Where { name: String page: Int }",
        production="type Query { a: Int b: Int! find(id: Int, where: Where): Int }\n"
        "input Where { name: [String!] page: Int }",
    )

    build(paths)

    sent = send(paths, "ab", {"a": 1, "b": 2, "find": 3}, id=1)[0]["query"]
    assert _trimmed(paths, "development", sent).document == (
        "query ab {\n  a\n  find(where: {page: 1})\n}"
    )
    assert _trimmed(paths, "production", sent).document == sent


_LITERALS_SDL = (
    "type Query { obs(where: Where, flags: [Flag!]!): Int }\n"
    "input Where { flag: Flag nested: Inner! {extra} }\n"
)


def test_input_literals_lose_fields_and_enum_values_the_environment_lacks(tmp_path):
    paths = _write_schemas(
        tmp_path,
        operations="query literals { obs(where: {nested: {x: 1}, flag: B, "
        "flags: [A, B]}, flags: [A, B]) }",
        development=_LITERALS_SDL.replace("{extra}", "extra: Int")
        + "input Inner { y: Int }\nenum Flag { A C }",
        production=_LITERALS_SDL.replace("{extra}", "flags: [Flag!]")
        + "input Inner { x: Int }\nenum Flag { A B }",
    )

    build(paths)

    sent = send(paths, "literals", {"obs": 1})[0]["query"]
    assert _trimmed(paths, "development", sent).document == (
        "query literals {\n  obs(where: {nested: {}}, flags: [A])\n}"
    )
    assert _trimmed(paths, "production", sent).document == sent


def test_fragments_on_a_type_the_union_lacks_are_removed(tmp_path):
    paths = _write_schemas(
        tmp_path,
        operations="query items { items { ... on A { id } ... on B { id } "
        "...BFields } }\nfragment BFields on B { name }",
        development=_ITEMS_SDL + "type B { id: ID! name: String }\nunion Item = A | B",
        production=_ITEMS_SDL + "type B { id: ID! name: String }\nunion Item = A",
    )

    result = build(paths)

    sent = send(paths, "items", {"items": []})[0]["query"]
    assert _trimmed(paths, "production", sent).document == (
        "query items {\n  items {\n    __typename\n    ... on A {\n      id\n    }\n"
        "  }\n}"
    )
    assert "- `... on B` removed from `items`" in result.trim_summary
    assert "- `...BFields` removed from `items`" in result.trim_summary


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
        "- Alias `GmosImagingVariantInput` of `ImagingVariantInput` in "
        "`input_types`\n"
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


def test_renamed_union_or_interface_is_flagged_as_needing_a_typename_map(
    tmp_path,
):
    result, _ = _build_two(
        tmp_path,
        development="type A { x: Int }\ninterface Node { id: ID! }\n"
        "union Item = A\ntype Query { item: Item node: Node }",
        production="type A { x: Int }\ninterface OldNode { id: ID! }\n"
        "union OldItem = A\ntype Query { item: OldItem node: OldNode }",
    )

    assert result.merge_summary == (
        "### Merge summary\n"
        "\n"
        "- Renamed `OldItem` to `Item` (`Query.item`)\n"
        "- Renamed `OldNode` to `Node` (`Query.node`)\n"
        "- Warning: union `OldItem` was renamed; production answers "
        "`__typename` with `OldItem`, so a `__typename` map is now needed\n"
        "- Warning: interface `OldNode` was renamed; production answers "
        "`__typename` with `OldNode`, so a `__typename` map is now needed\n"
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


def test_trim_starts_from_the_text_the_generated_client_embeds(tmp_path, monkeypatch):
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
        after="EnvironmentDefaultsPlugin",
    )

    build(rewriting)

    sent = send(rewriting, "count", {"count": 1})[0]["query"]
    assert "# rewritten" in sent
    assert _trimmed(rewriting, "production", sent) == TrimmedOperation(
        name="count", document="query count {\n  count\n}"
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
        after="EnvironmentDefaultsPlugin",
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


def test_generated_code_carries_no_availability_docstrings(tmp_path):
    # ariadne-codegen warns at codegen time; the generated code says nothing.
    query = "type Query { program: Program }\n"
    paths = _write_schemas(
        tmp_path,
        operations="query getProgram { program { id reference } }",
        development=query + "type Program { id: ID! }",
        production=query + "type Program { id: ID! reference: String! }",
    )

    build(paths)

    sources = [path.read_text() for path in paths.package_dir.rglob("*.py")]
    assert not any("Available on" in source for source in sources)


_FIND_OUTER = "query find($outer: Outer!) { find(outer: $outer) }"


def _outer_sdl(input_name: str, enum_name: str) -> str:
    """
    Return a schema whose ``Outer`` input, shared by both environments, carries
    an input type and an enum under the given names.
    """
    return (
        "type Query { find(outer: Outer): Int }\n"
        f"input Outer {{ inner: {input_name} }}\n"
        f"input {input_name} {{ bin: Int! mode: {enum_name} }}\n"
        f"enum {enum_name} {{ FAST }}"
    )


def _renamed_input_paths(tmp_path) -> BuildPaths:
    """
    Pair production's ``GmosImagingVariantInput`` and ``GmosMode`` to
    development's ``ImagingVariantInput`` and ``Mode``.
    """
    return _write_schemas(
        tmp_path,
        operations=_FIND_OUTER,
        development=_outer_sdl("ImagingVariantInput", "Mode"),
        production=_outer_sdl("GmosImagingVariantInput", "GmosMode"),
    )


def test_production_name_of_a_paired_input_type_is_a_warning_alias(tmp_path):
    paths = _renamed_input_paths(tmp_path)

    build(paths)

    inputs = import_generated(paths, "input_types")
    with pytest.warns(DeprecationWarning, match="ImagingVariantInput") as warned:
        alias = inputs.GmosImagingVariantInput
    assert alias is inputs.ImagingVariantInput
    assert len(warned) == 1


def test_paired_enum_alias_is_in_the_package_all_and_lazy_imports(tmp_path):
    paths = _write_schemas(
        tmp_path,
        development="type Query { find(mode: Mode): Int }\nenum Mode { FAST }",
        production="type Query { find(mode: GmosMode): Int }\nenum GmosMode { FAST }",
    )

    build(paths)

    package = importlib.import_module(paths.package_dir.name)
    assert "GmosMode" in package.__all__
    assert package._LAZY_IMPORTS["GmosMode"] == ".enums"
    with pytest.warns(DeprecationWarning, match="import Mode instead") as warned:
        from_package = package.GmosMode
    assert from_package is import_generated(paths, "enums").Mode
    assert from_package.FAST is from_package("FAST")
    assert len(warned) == 1
    assert warned[0].filename == __file__


def test_paired_object_type_gets_no_alias(tmp_path):
    paths = _write_schemas(
        tmp_path,
        development="type Query { a: New }\ntype New { x: Int }",
        production="type Query { a: Old }\ntype Old { x: Int }",
    )

    result = build(paths)

    assert result.pairing.by_production_name == {"Old": "New"}
    package = importlib.import_module(paths.package_dir.name)
    assert "Old" not in package.__all__
    assert not any(
        "_DEPRECATED_ALIASES" in path.read_text()
        for path in paths.package_dir.glob("*.py")
    )


def test_pairing_without_renames_generates_no_alias_code(tmp_path):
    paths = _write_schemas(
        tmp_path,
        development="type Query { find(mode: Mode): Int }\nenum Mode { FAST }",
        production="type Query { find(mode: Mode): Int }\nenum Mode { FAST }",
    )

    build(paths)

    enums_source = (paths.package_dir / "enums.py").read_text()
    assert "__getattr__" not in enums_source
    assert "warnings" not in enums_source


def _ty_diagnostics(root: Path, packages_dir: Path, code: str) -> str:
    checked = root / "check.py"
    checked.write_text(code)
    result = subprocess.run(
        [
            sys.executable,
            "-m",
            "ty",
            "check",
            "--project",
            str(root),
            "--python",
            sys.prefix,
            "--extra-search-path",
            str(packages_dir),
            "--output-format",
            "concise",
            str(checked),
        ],
        capture_output=True,
        text=True,
        check=False,
    )
    return result.stdout + result.stderr


def test_ty_resolves_the_alias_to_its_class(tmp_path):
    paths = _renamed_input_paths(tmp_path)
    build(paths)
    package = paths.package_dir.name

    diagnostics = _ty_diagnostics(
        tmp_path,
        paths.package_dir.parent,
        f"from {package}.input_types import GmosImagingVariantInput\n"
        f"from {package} import GmosMode, ImagingVariantInput, Mode\n"
        "variant: ImagingVariantInput = GmosImagingVariantInput(bin=1, mode=Mode.FAST)\n"
        "mode: Mode = GmosMode.FAST\n"
        "wrong: int = GmosMode.FAST\n"
        f"from {package}.client import NoSuchName\n",
    )

    errors = [line for line in diagnostics.splitlines() if "error[" in line]
    assert [line.split(":")[1] for line in errors] == ["5", "6"], diagnostics
    assert "`Mode`" in errors[0]


def test_pickle_from_before_the_rename_loads_through_the_alias(tmp_path):
    before = _write_schemas(
        tmp_path / "before",
        operations=_FIND_OUTER,
        development=_outer_sdl("GmosImagingVariantInput", "GmosMode"),
        production=_outer_sdl("GmosImagingVariantInput", "GmosMode"),
    )
    build(before)
    after = _renamed_input_paths(tmp_path)
    after = dataclasses.replace(
        after, package_dir=after.package_dir.with_name(before.package_dir.name)
    )
    build(after)
    package = before.package_dir.name
    dumped = subprocess.run(
        [
            sys.executable,
            "-c",
            "import pickle, sys\n"
            f"from {package}.input_types import GmosImagingVariantInput\n"
            f"from {package}.enums import GmosMode\n"
            "sys.stdout.buffer.write(pickle.dumps(["
            "GmosImagingVariantInput(bin=1, mode=GmosMode.FAST), GmosMode.FAST]))",
        ],
        env={"PYTHONPATH": str(before.package_dir.parent)},
        capture_output=True,
        check=True,
    ).stdout

    importlib.invalidate_caches()
    with pytest.warns(DeprecationWarning):
        variant, mode = pickle.loads(dumped)

    inputs = import_generated(after, "input_types")
    assert type(variant) is inputs.ImagingVariantInput
    assert variant.model_dump(by_alias=True) == {"bin": 1, "mode": "FAST"}
    assert mode is import_generated(after, "enums").Mode.FAST


def test_input_built_through_the_alias_sends_the_same_document(tmp_path):
    paths = _renamed_input_paths(tmp_path)
    build(paths)
    inputs = import_generated(paths, "input_types")
    enums = import_generated(paths, "enums")
    with pytest.warns(DeprecationWarning):
        through_alias = inputs.Outer(
            inner=inputs.GmosImagingVariantInput(bin=1, mode=enums.GmosMode.FAST)
        )
    through_class = inputs.Outer(
        inner=inputs.ImagingVariantInput(bin=1, mode=enums.Mode.FAST)
    )

    sent_alias = send(paths, "find", {"find": 1}, outer=through_alias)[0]
    sent_class = send(paths, "find", {"find": 1}, outer=through_class)[0]

    assert sent_alias == sent_class
    assert sent_alias["variables"] == {"outer": {"inner": {"bin": 1, "mode": "FAST"}}}


def test_build_output_lists_every_alias_with_its_target(tmp_path):
    result = build(_renamed_input_paths(tmp_path))

    assert result.merge_summary == (
        "### Merge summary\n"
        "\n"
        "- Renamed `GmosImagingVariantInput` to `ImagingVariantInput` "
        "(`Outer.inner`)\n"
        "- Renamed `GmosMode` to `Mode` (`ImagingVariantInput.mode`)\n"
        "- Alias `GmosImagingVariantInput` of `ImagingVariantInput` in "
        "`input_types`\n"
        "- Alias `GmosMode` of `Mode` in `enums`\n"
    )


def test_the_build_records_no_schema_date(tmp_path):
    base = "type Query { program: String }\n"
    paths = _write_schemas(
        tmp_path, development="# schema-date: 2024-05-06\n" + base, production=base
    )

    build(paths)

    assert not any(
        "2024-05-06" in path.read_text() for path in paths.package_dir.rglob("*.py")
    )
