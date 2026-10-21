"""
Helpers shared by the script tests: a checkout layout, a generated package
import and a call through a built client that records what it sent.
"""

import asyncio
import importlib
import json
import shutil
from pathlib import Path
from typing import Any

import httpx

from scripts.run_codegen import BuildPaths

REPO_ROOT = Path(__file__).resolve().parents[2]

# Valid on any schema, so merge-only tests need no operations of their own.
TYPENAME_OPERATION = "query typenameOnly { __typename }\n"


def checkout(
    root: Path,
    *,
    sdl: str = "type Query { a: Int }\n",
    operations: str = TYPENAME_OPERATION,
    schemas_dir: Path | None = None,
) -> BuildPaths:
    """
    Lay out a checkout with one schema per environment and return its paths.

    Parameters
    ----------
    root : Path
        The checkout's root folder.
    sdl : str, optional
        The schema written for both environments.
    operations : str, optional
        The operations file's text.
    schemas_dir : Path | None, optional
        Where to write the schemas; the repo layout's folder by default.

    Returns
    -------
    BuildPaths
        The checkout's build paths.
    """
    paths = BuildPaths.for_repo(root)
    schemas_dir = paths.schemas_dir if schemas_dir is None else schemas_dir
    schemas_dir.mkdir(parents=True, exist_ok=True)
    for environment in ("development", "production"):
        (schemas_dir / f"{environment}.graphql").write_text(sdl)
    paths.operations_dir.mkdir(parents=True, exist_ok=True)
    (paths.operations_dir / "operations.graphql").write_text(operations)
    paths.codegen_config.parent.mkdir(parents=True, exist_ok=True)
    shutil.copyfile(REPO_ROOT / "graphql" / "codegen.toml", paths.codegen_config)
    return paths


def import_generated(paths: BuildPaths, module: str = "client"):
    """
    Import a module of the package the build wrote at ``paths``.
    """
    return importlib.import_module(f"{paths.package_dir.name}.{module}")


def send(
    paths: BuildPaths, method: str, response_data: dict, **kwargs: Any
) -> tuple[dict, Any]:
    """
    Call a generated client method and return the request body it sent.

    Parameters
    ----------
    paths : BuildPaths
        The build whose generated client to call.
    method : str
        The client method's name.
    response_data : dict
        The ``data`` GPP answers with.
    **kwargs : Any
        The method's arguments.

    Returns
    -------
    tuple[dict, Any]
        The JSON body sent, and the method's result.
    """
    sent: list[dict] = []

    def handler(request: httpx.Request) -> httpx.Response:
        sent.append(json.loads(request.content))
        return httpx.Response(200, json={"data": response_data})

    module = import_generated(paths)

    async def call():
        async with httpx.AsyncClient(transport=httpx.MockTransport(handler)) as http:
            client = module.GraphQLClient(url="http://gpp.test/odb", http_client=http)
            return await getattr(client, method)(**kwargs)

    result = asyncio.run(call())
    return sent[0], result
