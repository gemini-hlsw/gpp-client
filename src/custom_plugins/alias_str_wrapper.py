__all__ = ["AliasStrWrapperPlugin"]

import ast

from ariadne_codegen.plugins.base import Plugin
from graphql import (
    GraphQLInputField,
)


class AliasStrWrapperPlugin(Plugin):
    def generate_input_field(
        self,
        field_implementation: ast.AnnAssign,
        input_field: GraphQLInputField,
        field_name: str,
    ) -> ast.AnnAssign:
        """Wraps alias value in str() for VSCode/Pyright compatibility.
        Changes: alias="fooBar" to alias=str("fooBar")
        """
        # Check if the field has a keyword with alias=
        if isinstance(field_implementation.value, ast.Call):
            for keyword in field_implementation.value.keywords:
                if keyword.arg == "alias" and isinstance(keyword.value, ast.Constant):
                    # Wrap alias value in str()
                    keyword.value = ast.Call(
                        func=ast.Name(id="str", ctx=ast.Load()),
                        args=[keyword.value],
                        keywords=[],
                    )
        return field_implementation
