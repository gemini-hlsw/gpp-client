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
        """
        Wrap the input field's alias in ``str()`` so Pyright and VS Code type it.

        Parameters
        ----------
        field_implementation : ast.AnnAssign
            The generated input field.
        input_field : GraphQLInputField
            The schema input field.
        field_name : str
            The field's Python name.

        Returns
        -------
        ast.AnnAssign
            The field, with ``alias="fooBar"`` written as
            ``alias=str("fooBar")``.
        """
        if isinstance(field_implementation.value, ast.Call):
            for keyword in field_implementation.value.keywords:
                if keyword.arg == "alias" and isinstance(keyword.value, ast.Constant):
                    keyword.value = ast.Call(
                        func=ast.Name(id="str", ctx=ast.Load()),
                        args=[keyword.value],
                        keywords=[],
                    )
        return field_implementation
