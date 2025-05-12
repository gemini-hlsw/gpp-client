import ast

import pytest
from ariadne_codegen.client_generators.input_types import InputTypesGenerator
from ariadne_codegen.plugins.manager import PluginManager
from graphql import build_schema

from custom_plugins.alias_str_wrapper import AliasStrWrapperPlugin


@pytest.fixture
def plugin_manager(schema_str):
    schema = build_schema(schema_str)
    return PluginManager(schema=schema, plugins_types=[AliasStrWrapperPlugin])


def test_alias_str_wrapper(plugin_manager, schema_str):
    """Test wrapping the alias with 'str()' for IDE."""
    schema = build_schema(schema_str)

    generator = InputTypesGenerator(
        schema=schema,
        convert_to_snake_case=True,
        plugin_manager=plugin_manager,
    )
    module = generator.generate()
    code = ast.unparse(module)

    # Check output, black hasn't run so its not formatted yet.
    assert "class SetProgramReferenceInput(BaseModel):" in code
    assert (
        "program_id: Optional[Any] = Field(alias=str('programId'), default=None)"
        in code
    )
