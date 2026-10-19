__all__ = ["ALIASES_KEY", "AliasNamesPlugin", "AliasReport"]

import ast
from dataclasses import dataclass, field

from ariadne_codegen.plugins.base import Plugin

from graphql import GraphQLSchema

ALIASES_KEY = "type_aliases"
"""Key under ``[tool.gpp-client]`` of the ``AliasReport`` the plugin reads and fills."""

_ALIASED_MODULES = ("input_types", "enums")

# The package's lazy __init__ forwards here, so the warning must skip its frame.
_GETATTR_SOURCE = """
def __getattr__(name: str):
    target = _DEPRECATED_ALIASES.get(name)
    if target is None:
        raise AttributeError(f"module {__name__!r} has no attribute {name!r}")
    level = 2
    frame = sys._getframe(1)
    while _in_package(frame) and frame.f_back is not None:
        frame = frame.f_back
        level += 1
    warnings.warn(
        f"{name} is deprecated: production will call it {target} at its next "
        f"promotion; import {target} instead",
        DeprecationWarning,
        stacklevel=level,
    )
    return globals()[target]


def _in_package(frame) -> bool:
    name = frame.f_globals.get("__name__", "")
    return name == __package__ or name.startswith(__package__ + ".")
"""


@dataclass
class AliasReport:
    """
    The aliases the plugin should place and where it placed them.

    Parameters
    ----------
    renames : dict[str, str]
        Development name per renamed production name, from the build's pairing.
    placed : list[tuple[str, str, str]]
        Each alias placed: module name, alias, target.
    """

    renames: dict[str, str] = field(default_factory=dict)
    placed: list[tuple[str, str, str]] = field(default_factory=list)


class AliasNamesPlugin(Plugin):
    """
    Expose production's name for a renamed input type or enum as a deprecated
    alias of the class carrying development's name.

    The alias is a ``TYPE_CHECKING`` assignment, so type checkers resolve it,
    and a module ``__getattr__`` that warns and returns the class. The package
    ``__init__`` lists it in ``__all__`` and the lazy import map.
    """

    def __init__(self, schema: GraphQLSchema, config_dict: dict) -> None:
        super().__init__(schema, config_dict)
        report = config_dict.get("tool", {}).get("gpp-client", {}).get(ALIASES_KEY)
        self.report: AliasReport = report if report is not None else AliasReport()
        self.by_module: dict[str, dict[str, str]] = {}

    def generate_inputs_module(self, module: ast.Module) -> ast.Module:
        return self._add_aliases(module, "input_types")

    def generate_enums_module(self, module: ast.Module) -> ast.Module:
        return self._add_aliases(module, "enums")

    def generate_init_import(self, import_: ast.ImportFrom) -> ast.ImportFrom:
        aliases = self.by_module.get((import_.module or "").lstrip("."), {})
        imported = {name.name for name in import_.names}
        extra = sorted(alias for alias, target in aliases.items() if target in imported)
        if extra:
            import_.names = sorted(
                import_.names + [ast.alias(name=alias) for alias in extra],
                key=lambda name: name.name,
            )
        return import_

    def _add_aliases(self, module: ast.Module, module_name: str) -> ast.Module:
        classes = {node.name for node in module.body if isinstance(node, ast.ClassDef)}
        aliases = {
            alias: target
            for alias, target in sorted(self.report.renames.items())
            if target in classes
        }
        self.by_module[module_name] = aliases
        if not aliases:
            return module
        self.report.placed += [
            (module_name, alias, target) for alias, target in aliases.items()
        ]
        module.body[:0] = [
            ast.Import(names=[ast.alias(name="sys")]),
            ast.Import(names=[ast.alias(name="warnings")]),
            ast.ImportFrom(
                module="typing", names=[ast.alias(name="TYPE_CHECKING")], level=0
            ),
        ]
        module.body.append(
            ast.If(
                test=ast.Name(id="TYPE_CHECKING"),
                body=[
                    ast.Assign(targets=[ast.Name(id=alias)], value=ast.Name(id=target))
                    for alias, target in aliases.items()
                ],
                orelse=[],
            )
        )
        module.body.append(
            ast.Assign(
                targets=[ast.Name(id="_DEPRECATED_ALIASES")],
                value=ast.Dict(
                    keys=[ast.Constant(alias) for alias in aliases],
                    values=[ast.Constant(target) for target in aliases.values()],
                ),
            )
        )
        module.body.extend(ast.parse(_GETATTR_SOURCE).body)
        ast.fix_missing_locations(module)
        return module
