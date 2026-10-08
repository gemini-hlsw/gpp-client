"""
Tests for the client build pipeline, driven through ``build``.
"""

import ast
import asyncio
import dataclasses
import importlib
import json
import uuid
from pathlib import Path

import httpx
import pytest
from pydantic import ValidationError

from gpp_client.environment import GPPEnvironment
from gpp_client.generated_tables import use_generated_package
from gpp_client.trimmed_operations import TrimmedOperation, find_trimmed_operation
from graphql import build_schema
from scripts.build_client import BuildError, BuildPaths, TypeConflict, build

REPO_ROOT = Path(__file__).resolve().parents[2]

# Valid on any schema, so merge-only tests need no operations of their own.
_TYPENAME_OPERATION = "query typenameOnly { __typename }\n"


def _write_schemas(
    root: Path, operations: str = _TYPENAME_OPERATION, **sdl_by_environment: str
) -> BuildPaths:
    schemas_dir = root / "schemas"
    schemas_dir.mkdir(parents=True, exist_ok=True)
    for environment, sdl in sdl_by_environment.items():
        (schemas_dir / f"{environment}.graphql").write_text(sdl)
    operations_dir = root / "operations"
    operations_dir.mkdir(parents=True, exist_ok=True)
    (operations_dir / "operations.graphql").write_text(operations)
    return BuildPaths(
        schemas_dir=schemas_dir,
        operations_dir=operations_dir,
        package_dir=root / "packages" / f"generated_{uuid.uuid4().hex[:12]}",
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
    with use_generated_package(paths.package_dir.name):
        return find_trimmed_operation(GPPEnvironment(environment), query)


def _merged(paths: BuildPaths):
    return build_schema(paths.merged_schema_path.read_text())


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

    build(paths)

    field = _merged(paths).type_map["Program"].fields["reference"]
    assert str(field.type) == "String"
    assert _environments(field.ast_node) == ["production"]


def test_llms_txt_lists_leaving_fields_selected_through_fragments(tmp_path):
    development = "type Query { program: Program }\ntype Program { id: ID! draft: Int }"
    production = "type Query { program: Program }\ntype Program { id: ID! legacy: Int }"
    paths = dataclasses.replace(
        _write_schemas(
            tmp_path,
            operations=(
                "query getProgram { program { ...ProgramParts draft } }\n"
                "fragment ProgramParts on Program { id legacy }\n"
                "query getId { program { id } }\n"
            ),
            development=development,
            production=production,
        ),
        llms_txt=tmp_path / "llms.txt",
    )

    build(paths)

    assert "- Fields leaving production: `Program.legacy`\n" in (
        paths.llms_txt.read_text()
    )


def _build_two(tmp_path, development: str, production: str):
    paths = _write_schemas(tmp_path, development=development, production=production)
    result = build(paths)
    return result, _merged(paths)


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


def test_type_of_a_different_kind_fails_naming_type_and_environments(tmp_path):
    paths = _write_schemas(
        tmp_path,
        development="type Query { a: Mode }\nenum Mode { FAST }",
        production="type Query { a: Mode }\nscalar Mode",
    )

    with pytest.raises(BuildError) as error:
        build(paths)

    message = str(error.value)
    assert "'Mode'" in message
    assert "enum on development" in message
    assert "scalar on production" in message
    assert not paths.merged_schema_path.exists()


def test_field_whose_type_differs_is_left_out_and_reported(tmp_path):
    result, schema = _build_two(
        tmp_path,
        development="type Query { a: Int b: String }",
        production="type Query { a: Int b: Int }",
    )

    assert "b" not in schema.query_type.fields
    assert result.conflicts == (
        TypeConflict(
            coordinate="Query.b",
            types=(
                ("development", "String"),
                ("production", "Int"),
            ),
        ),
    )


def test_two_builds_write_identical_files(tmp_path):
    paths = _write_schemas(
        tmp_path,
        development="type Query { a: Int b: Int c(x: Int): Int }\nenum E { X Y }",
        production="type Query { a: Int! d: Int }\nenum E { X Z }",
    )

    build(paths)
    first = paths.merged_schema_path.read_bytes()
    build(paths)

    assert paths.merged_schema_path.read_bytes() == first


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


def test_selecting_a_field_whose_type_differs_fails_naming_each_type(tmp_path):
    paths = _write_schemas(
        tmp_path,
        operations="query ab { a b }",
        development="type Query { a: Int b: String }",
        production="type Query { a: Int b: Int }",
    )

    with pytest.raises(BuildError) as error:
        build(paths)

    assert str(error.value) == (
        "Operations select fields whose type differs between environments:\n"
        "  Query.b in ab: String on development, Int on production"
    )


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


def test_llms_txt_lists_what_works_where(tmp_path):
    development = (
        "type Query { clone: Int program: Program find(where: Where): Int }\n"
        "type Program { id: ID! draft: Int }\n"
        "input Where { name: String sort: String }"
    )
    production = (
        "type Query { program: Program find(where: Where): Int }\n"
        "type Program { id: ID! legacy: Int }\n"
        "input Where { name: String }"
    )
    paths = dataclasses.replace(
        _write_schemas(
            tmp_path,
            operations="query cloneOne { clone }\n"
            "query getProgram { program { id draft legacy } }\n"
            "query find($where: Where) { find(where: $where) }",
            development=development,
            production=production,
        ),
        llms_txt=tmp_path / "llms.txt",
    )

    build(paths)

    text = paths.llms_txt.read_text()
    assert text.startswith("# gpp-client\n")
    stable = "https://gpp-client.readthedocs.io/en/stable/"
    for page in (
        "getting-started.html",
        "guides/environments.html",
        "guides/errors.html#environment-errors",
        "guides/custom-queries.html",
        "guides/cli.html",
        "guides/versions.html",
        "guides/subscriptions.html",
        "guides/attachments.html",
        "client.html",
    ):
        assert f"({stable}{page})" in text
    assert "async with GPPClient() as client:\n" in text
    assert "do not edit" not in text
    assert "GPP_ENVIRONMENT" not in text
    assert "GPPFieldLeavingWarning" not in text
    assert "- Methods only on development: `client.graphql.clone_one`\n" in text
    assert (
        "- Arguments, input fields and enum values only on development: "
        "`Where.sort`\n" in text
    )
    assert "- Fields that read `None` on development: `Program.legacy`\n" in text
    assert "- Fields that read `None` on production: `Program.draft`\n" in text
    assert "- Fields leaving production: `Program.legacy`\n" in text


def test_llms_txt_without_differences_says_everything_works(tmp_path):
    paths = dataclasses.replace(
        _write_schemas(
            tmp_path,
            development="type Query { a: Int }",
            production="type Query { a: Int }",
        ),
        llms_txt=tmp_path / "llms.txt",
    )

    build(paths)

    assert paths.llms_txt.read_text().endswith(
        "- Everything the client generates works on development and production.\n"
    )


def test_bundles_user_environment_schemas_without_descriptions(tmp_path):
    sdl = '"""The root."""\ntype Query {\n  """A program."""\n  program: ID\n}\n'
    paths = _write_schemas(
        tmp_path,
        development=sdl,
        production=sdl.replace("program: ID", "program: ID\n  legacy: Int"),
    )

    build(paths)

    bundled = paths.package_dir / "schemas"
    assert sorted(p.name for p in bundled.iterdir()) == [
        "development.graphql",
        "production.graphql",
    ]
    assert (bundled / "development.graphql").read_text() == (
        "type Query {\n  program: ID\n}\n"
    )
    assert "legacy: Int" in (bundled / "production.graphql").read_text()
