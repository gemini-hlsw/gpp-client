#!/usr/bin/env python3
"""
Validate a release tag and that the committed client matches its schemas.

A release is refused when its tag is not a CalVer release tag, or when the
committed merged schema, generated package or ``llms.txt`` differs from a fresh
build of the committed environment schemas and operations.
"""

import filecmp
import re
import shutil
import sys
import tempfile
from pathlib import Path
from typing import Final

from custom_plugins.environments import USER_ENVIRONMENTS
from scripts.build_client import BuildError, BuildPaths, build

TAG_PATTERN: Final[re.Pattern[str]] = re.compile(r"^v\d{2}\.(?:[1-9]|1[0-2])\.\d+$")
DEV_TAG_PATTERN: Final[re.Pattern[str]] = re.compile(
    r"^v\d{2}\.(?:[1-9]|1[0-2])\.\d+\.dev\d+$"
)


class ReleaseValidationError(RuntimeError):
    """
    Raised when release validation fails.
    """


def validate_release(tag: str, paths: BuildPaths) -> None:
    """
    Validate a release tag and the committed client it would release.

    Parameters
    ----------
    tag : str
        Release tag, including the leading ``v``.
    paths : BuildPaths
        The checkout's schemas, operations, codegen config, generated package
        and ``llms.txt``.

    Raises
    ------
    ReleaseValidationError
        Raised if the tag is invalid, the build fails, or the committed merged
        schema, generated package or ``llms.txt`` differs from a fresh build.
    """
    _check_tag(tag)
    differences = _differences_from_fresh_build(paths)
    if differences:
        raise ReleaseValidationError(
            "Committed generated code differs from a fresh build of the "
            "committed schemas. Run `uv run python -m scripts.build_client` "
            "and commit the result.\n" + "\n".join(f"  {d}" for d in differences)
        )


def _check_tag(tag: str) -> None:
    if DEV_TAG_PATTERN.fullmatch(tag):
        raise ReleaseValidationError(
            f"Pre-release tag refused: {tag}. gpp-client releases in one stream "
            "that reaches every environment, so there are no .devN releases. "
            "Use a release tag such as v26.5.0."
        )
    if TAG_PATTERN.fullmatch(tag) is None:
        raise ReleaseValidationError(
            f"Invalid release tag: {tag}. Expected format: v26.5.0."
        )


def _differences_from_fresh_build(paths: BuildPaths) -> list[str]:
    with tempfile.TemporaryDirectory() as scratch:
        root = Path(scratch)
        fresh = BuildPaths(
            schemas_dir=root / "schemas",
            operations_dir=root / "operations",
            package_dir=root / "package" / paths.package_dir.name,
            codegen_config=paths.codegen_config,
            llms_txt=root / "llms.txt" if paths.llms_txt is not None else None,
        )
        fresh.schemas_dir.mkdir()
        for environment in USER_ENVIRONMENTS:
            source = paths.schema_path(environment)
            if source.is_file():
                shutil.copyfile(source, fresh.schema_path(environment))
        if paths.operations_dir.is_dir():
            shutil.copytree(paths.operations_dir, fresh.operations_dir)
        else:
            fresh.operations_dir.mkdir()
        try:
            build(fresh)
        except BuildError as exc:
            raise ReleaseValidationError(f"Fresh build failed: {exc}") from exc

        differences = _file_differences(
            paths.merged_schema_path, fresh.merged_schema_path
        )
        differences += _tree_differences(paths.package_dir, fresh.package_dir)
        if paths.llms_txt is not None and fresh.llms_txt is not None:
            differences += _file_differences(paths.llms_txt, fresh.llms_txt)
        return differences


def _file_differences(committed: Path, fresh: Path) -> list[str]:
    if not committed.is_file():
        return [f"missing: {committed}"]
    if not filecmp.cmp(committed, fresh, shallow=False):
        return [f"differs: {committed}"]
    return []


def _tree_differences(committed: Path, fresh: Path) -> list[str]:
    committed_files = _files(committed)
    fresh_files = _files(fresh)
    differences = [
        f"missing: {committed / name}" for name in sorted(fresh_files - committed_files)
    ]
    differences += [
        f"unexpected: {committed / name}"
        for name in sorted(committed_files - fresh_files)
    ]
    differences += [
        f"differs: {committed / name}"
        for name in sorted(committed_files & fresh_files)
        if not filecmp.cmp(committed / name, fresh / name, shallow=False)
    ]
    return differences


def _files(root: Path) -> set[Path]:
    if not root.is_dir():
        return set()
    return {
        path.relative_to(root)
        for path in root.rglob("*")
        if path.is_file() and "__pycache__" not in path.parts
    }


def main() -> None:
    """
    Validate a release tag against the checkout in the current directory.
    """
    if len(sys.argv) != 2:
        raise SystemExit("Usage: python -m scripts.validate_release <tag>")

    try:
        validate_release(sys.argv[1], BuildPaths.for_repo(Path.cwd()))
    except ReleaseValidationError as exc:
        print(exc, file=sys.stderr)
        raise SystemExit(1) from exc


if __name__ == "__main__":
    main()
