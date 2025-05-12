__all__ = ["FixCustomFieldsLiteralPlugin"]

import ast
from typing import Any, Dict, List, Optional, cast

from ariadne_codegen.client_generators import custom_fields as _cf
from ariadne_codegen.plugins.base import Plugin


class FixCustomFieldsLiteralPlugin(Plugin):
    """Patch CustomFieldsGenerator so GraphQL literals keep camelCase.

    References
    ----------
    .. [1] *ariadne-codegen* source file:
           https://github.com/mirumee/ariadne-codegen/blob/main/ariadne_codegen/client_generators/custom_fields.py
    .. [2] Pull request that introduces the fix:
           https://github.com/mirumee/ariadne-codegen/pull/326
    """

    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)

        self._patch__generate_class_field()
        self._patch_generate_product_type_method()

    @staticmethod
    def _patch__generate_class_field() -> None:
        original = _cf.CustomFieldsGenerator._generate_class_field

        def patched(
            self,
            name: str,
            field_name: str,
            org_name: str,
            field: ast.ClassDef,
            method_required: bool,
            lineno: int,
        ):
            """Handles the generation of field types."""
            if getattr(field, "args") or method_required:
                return self.generate_product_type_method(
                    name, org_name, field_name, getattr(field, "args")
                )
            # Fallback to original behaviour (scalar fields, no args).
            return original(
                self,
                name,
                field_name,
                org_name,
                field,
                method_required,
                lineno,
            )

        _cf.CustomFieldsGenerator._generate_class_field = patched  # type: ignore[attr-defined]

    @staticmethod
    def _patch_generate_product_type_method() -> None:
        def patched(
            self: _cf.CustomFieldsGenerator,
            name: str,
            org_name: str,
            class_name: str,
            arguments: Optional[Dict[str, Any]] = None,
        ):
            """Generates a method for a product type."""
            arguments = arguments or {}
            field_class_name = _cf.generate_name(class_name)
            (
                method_arguments,
                return_arguments_keys,
                return_arguments_values,
            ) = self.argument_generator.generate_arguments(arguments)
            self._imports.extend(self.argument_generator.imports)
            arguments_body: List[ast.stmt] = []
            arguments_keyword: List[ast.keyword] = []

            if arguments:
                (
                    arguments_body,
                    arguments_keyword,
                ) = self.argument_generator.generate_clear_arguments_section(
                    return_arguments_keys, return_arguments_values
                )

            return _cf.generate_method_definition(
                name,
                arguments=method_arguments,
                body=cast(
                    List[ast.stmt],
                    [
                        *arguments_body,
                        _cf.generate_return(
                            value=_cf.generate_call(
                                func=field_class_name,
                                args=[_cf.generate_constant(org_name)],
                                keywords=arguments_keyword,
                            )
                        ),
                    ],
                ),
                return_type=_cf.generate_name(f'"{class_name}"'),
                decorator_list=[_cf.generate_name("classmethod")],
            )

        _cf.CustomFieldsGenerator.generate_product_type_method = patched  # type: ignore[attr-defined]
