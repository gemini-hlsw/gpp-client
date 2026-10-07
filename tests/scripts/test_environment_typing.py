"""
Tests that ty flags operations an environment lacks on ``GPPClient.graphql``.

Each test builds a client from fixture schemas into a copy of ``gpp_client``,
then runs ty on a small file that uses it, and compares the lines ty reports
with the lines marked ``# error``.
"""

import re
import shutil
import subprocess
import sys
from pathlib import Path

from scripts.build_client import BuildPaths, build

REPO_ROOT = Path(__file__).resolve().parents[2]

_CLONE_ON_DEVELOPMENT_ONLY = {
    "operations": "query cloneItem { clone { id } }\nquery countItems { count }\n",
    "development": "type Query { clone: Clone count: Int }\ntype Clone { id: ID! }",
    "production": "type Query { count: Int }",
}


def _build_package(root: Path, schemas: dict[str, str]) -> Path:
    """
    Copy ``gpp_client`` under ``root`` with a client generated from ``schemas``.
    """
    source = root / "src"
    shutil.copytree(
        REPO_ROOT / "src" / "gpp_client",
        source / "gpp_client",
        ignore=shutil.ignore_patterns("generated", "__pycache__"),
    )
    schemas_dir = root / "schemas"
    schemas_dir.mkdir()
    for environment in ("development", "production"):
        (schemas_dir / f"{environment}.graphql").write_text(schemas[environment])
    operations_dir = root / "operations"
    operations_dir.mkdir()
    (operations_dir / "operations.graphql").write_text(schemas["operations"])
    build(
        BuildPaths(
            schemas_dir=schemas_dir,
            operations_dir=operations_dir,
            package_dir=source / "gpp_client" / "generated",
            codegen_config=REPO_ROOT / "graphql" / "codegen.toml",
        )
    )
    return source


def _ty_error_lines(root: Path, source: Path, code: str) -> set[int]:
    checked = root / "check.py"
    checked.write_text(code)
    result = subprocess.run(
        [
            sys.executable,
            "-m",
            "ty",
            "check",
            "--project",
            str(root),
            "--python",
            sys.prefix,
            "--extra-search-path",
            str(source),
            "--output-format",
            "concise",
            str(checked),
        ],
        capture_output=True,
        text=True,
        check=False,
    )
    pattern = re.compile(rf"^{re.escape(str(checked))}:(\d+):\d+: error")
    lines = {
        int(match.group(1))
        for line in result.stdout.splitlines()
        if (match := pattern.match(line))
    }
    assert result.returncode == (1 if lines else 0), result.stdout + result.stderr
    return lines


def _marked_lines(code: str) -> set[int]:
    return {
        number
        for number, line in enumerate(code.splitlines(), start=1)
        if line.endswith("# error")
    }


def test_operation_production_lacks_is_an_error_only_on_a_production_client(
    tmp_path,
):
    source = _build_package(tmp_path, _CLONE_ON_DEVELOPMENT_ONLY)
    code = (
        "from gpp_client import GPPClient\n"
        "\n"
        "\n"
        "async def main() -> None:\n"
        '    production = GPPClient(environment="production")\n'
        '    development = GPPClient(environment="development")\n'
        "    await production.graphql.clone_item()  # error\n"
        "    await production.graphql.count_items()\n"
        "    await development.graphql.clone_item()\n"
        "    await development.graphql.count_items()\n"
        '    async with GPPClient(environment="production") as client:\n'
        "        await client.graphql.clone_item()  # error\n"
    )

    assert _ty_error_lines(tmp_path, source, code) == _marked_lines(code)


def test_client_whose_environment_comes_from_config_has_every_operation(tmp_path):
    source = _build_package(tmp_path, _CLONE_ON_DEVELOPMENT_ONLY)
    code = (
        "from gpp_client import GPPClient\n"
        "\n"
        "\n"
        "async def main(environment: str) -> None:\n"
        "    await GPPClient().graphql.clone_item()\n"
        "    await GPPClient(environment=environment).graphql.clone_item()\n"
        '    await GPPClient(environment="Development").graphql.clone_item()\n'
        "    await GPPClient().graphql.missing()  # error\n"
    )

    assert _ty_error_lines(tmp_path, source, code) == _marked_lines(code)


def test_production_chosen_by_enum_member_lacks_the_operation(tmp_path):
    source = _build_package(tmp_path, _CLONE_ON_DEVELOPMENT_ONLY)
    code = (
        "from gpp_client import GPPClient\n"
        "from gpp_client.environment import GPPEnvironment\n"
        "\n"
        "\n"
        "async def main() -> None:\n"
        "    production = GPPClient(environment=GPPEnvironment.PRODUCTION)\n"
        "    development = GPPClient(environment=GPPEnvironment.DEVELOPMENT)\n"
        "    await production.graphql.clone_item()  # error\n"
        "    await development.graphql.clone_item()\n"
    )

    assert _ty_error_lines(tmp_path, source, code) == _marked_lines(code)


def test_client_typed_for_one_environment_passes_where_gppclient_is_expected(
    tmp_path,
):
    source = _build_package(tmp_path, _CLONE_ON_DEVELOPMENT_ONLY)
    code = (
        "from gpp_client import GPPClient\n"
        "\n"
        "\n"
        "async def count(client: GPPClient) -> None:\n"
        "    await client.graphql.count_items()\n"
        "    await client.graphql.missing()  # error\n"
        "\n"
        "\n"
        "async def main() -> None:\n"
        '    await count(GPPClient(environment="production"))\n'
        '    await count(GPPClient(environment="development"))\n'
        "    await count(GPPClient())\n"
    )

    assert _ty_error_lines(tmp_path, source, code) == _marked_lines(code)
