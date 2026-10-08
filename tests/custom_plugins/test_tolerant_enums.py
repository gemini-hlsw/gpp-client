import ast

from ariadne_codegen.client_generators.enums import EnumsGenerator
from ariadne_codegen.plugins.manager import PluginManager

from custom_plugins.tolerant_enums import TolerantEnumsPlugin
from graphql import GraphQLEnumType, build_schema


def test_every_generated_enum_accepts_unknown_values(schema_str):
    """
    Ensure each enum in the schema is generated on the tolerant base.
    """
    schema = build_schema(schema_str)
    generator = EnumsGenerator(
        schema=schema,
        plugin_manager=PluginManager(
            schema=schema, plugins_types=[TolerantEnumsPlugin]
        ),
    )
    namespace: dict = {}
    exec(ast.unparse(generator.generate()), namespace)

    enum_names = [
        name
        for name, type_ in schema.type_map.items()
        if isinstance(type_, GraphQLEnumType) and not name.startswith("__")
    ]
    assert enum_names
    for name in enum_names:
        enum_class = namespace[name]
        assert enum_class("NOT_IN_SCHEMA").value == "NOT_IN_SCHEMA", name
        assert isinstance(enum_class("NOT_IN_SCHEMA"), str), name


def test_tolerant_base_is_not_exported(schema_str):
    """
    Ensure the base stays private to the generated enums module.
    """
    schema = build_schema(schema_str)
    generator = EnumsGenerator(
        schema=schema,
        plugin_manager=PluginManager(
            schema=schema, plugins_types=[TolerantEnumsPlugin]
        ),
    )
    generator.generate()

    assert "_TolerantEnum" not in generator.get_generated_public_names()
