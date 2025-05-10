import ast

from ariadne_codegen.client_generators.custom_fields import CustomFieldsGenerator
from graphql import build_schema

from custom_plugins.fix_custom_fields_literal import FixCustomFieldsLiteralPlugin


def test_camel_case_literal_preserved(schema_str):
    """Test the monkeypatch for camelCase inputs."""
    # This applies the patch since it is in init.
    FixCustomFieldsLiteralPlugin(schema=None, config_dict={})

    schema = build_schema(schema_str)

    generator = CustomFieldsGenerator(
        schema=schema,
        convert_to_snake_case=True,
        plugin_manager=None,
    )
    module = generator.generate()
    code = ast.unparse(module)

    # Check output, black hasn't run so its not formatted yet.
    assert "def non_charged(cls)" in code
    assert "return TimeSpanFields('nonCharged')" in code
