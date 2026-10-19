__all__ = ["TolerantEnumsPlugin"]

import ast

from ariadne_codegen.plugins.base import Plugin

BASE_NAME = "_TolerantEnum"

# GPP promotes new enum values often; an installed client must still parse them.
_BASE_SOURCE = f'''
class {BASE_NAME}(str, Enum):
    """Keep a value this build does not know as a member carrying the raw value."""

    @classmethod
    def _missing_(cls, value: object) -> "{BASE_NAME} | None":
        if not isinstance(value, str):
            return None
        member = str.__new__(cls, value)
        member._name_ = value
        member._value_ = value
        known = cls._value2member_map_.setdefault(value, member)
        return known if isinstance(known, cls) else None
'''


def _is_str_enum_base(bases: list[ast.expr]) -> bool:
    names = [base.id for base in bases if isinstance(base, ast.Name)]
    return names == ["str", "Enum"]


class TolerantEnumsPlugin(Plugin):
    def generate_enums_module(self, module: ast.Module) -> ast.Module:
        """
        Base every generated enum on one that accepts unknown values.

        Parameters
        ----------
        module : ast.Module
            The generated enums module.

        Returns
        -------
        ast.Module
            The module with the tolerant base inserted after its imports.
        """
        insert_at = 0
        for index, node in enumerate(module.body):
            if isinstance(node, ast.ClassDef) and _is_str_enum_base(node.bases):
                node.bases = [ast.Name(id=BASE_NAME, ctx=ast.Load())]
            if isinstance(node, (ast.Import, ast.ImportFrom)):
                insert_at = index + 1
        module.body[insert_at:insert_at] = ast.parse(_BASE_SOURCE).body
        return module
