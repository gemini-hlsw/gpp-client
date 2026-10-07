"""
Download each GPP environment's GraphQL schema by introspection.

Introspection is anonymous. When a server refuses it, the download retries with
that environment's token from the environment variables.
"""

import os
from collections.abc import Iterable, Mapping
from pathlib import Path
from typing import Annotated

import httpx
import typer

from custom_plugins.environments import USER_ENVIRONMENTS
from gpp_client.cli import output
from gpp_client.environment import GPPEnvironment
from gpp_client.urls import get_graphql_url
from graphql import build_client_schema, get_introspection_query, print_schema
from scripts.build_client import BuildPaths, schema_file

__all__ = ["SchemaDownloadError", "download_schemas"]


INTROSPECTION_QUERY = get_introspection_query(
    descriptions=True,
    specified_by_url=True,
    directive_is_repeatable=True,
    schema_description=False,
    input_value_deprecation=True,
    input_object_one_of=True,
)

TIMEOUT_SECONDS = 30

app = typer.Typer(add_completion=False)


class SchemaDownloadError(RuntimeError):
    """
    Raised when schema download fails.
    """


class _Refused(Exception):
    pass


def download_schemas(
    schemas_dir: Path,
    environments: Iterable[str] = USER_ENVIRONMENTS,
    *,
    http_client: httpx.Client | None = None,
    environ: Mapping[str, str] = os.environ,
) -> list[Path]:
    """
    Download environment schemas into ``<schemas_dir>/<environment>.graphql``.

    Parameters
    ----------
    schemas_dir : Path
        Directory to write the schema files into.
    environments : Iterable[str], optional
        Environments to download; development and production by default.
    http_client : httpx.Client | None, optional
        Client to send requests with; a new one by default.
    environ : Mapping[str, str], optional
        Where to read token fallbacks from; the process environment by default.

    Returns
    -------
    list[Path]
        The schema files written, in the order given.

    Raises
    ------
    SchemaDownloadError
        Raised for an unknown environment, a failed request, or a refusal when
        the environment's token variable is unset.
    """
    unknown = [env for env in environments if env not in USER_ENVIRONMENTS]
    if unknown:
        raise SchemaDownloadError(
            f"Unknown environment {', '.join(unknown)}; "
            f"choose from {', '.join(USER_ENVIRONMENTS)}."
        )

    client = http_client or httpx.Client(timeout=TIMEOUT_SECONDS)
    schemas_dir.mkdir(parents=True, exist_ok=True)
    written = []
    try:
        for env in environments:
            path = schema_file(schemas_dir, env)
            path.write_text(_download(client, env, environ), encoding="utf-8")
            written.append(path)
    finally:
        if http_client is None:
            client.close()
    return written


def _download(client: httpx.Client, env: str, environ: Mapping[str, str]) -> str:
    try:
        data = _introspect(client, env, headers={})
    except _Refused:
        token_var = GPPEnvironment(env).token_variable
        token = environ.get(token_var)
        if not token:
            raise SchemaDownloadError(
                f"{env} refused anonymous introspection; set {token_var} and retry."
            ) from None
        try:
            data = _introspect(
                client, env, headers={"Authorization": f"Bearer {token}"}
            )
        except _Refused:
            raise SchemaDownloadError(
                f"{env} refused introspection with the token in {token_var}."
            ) from None
    return print_schema(build_client_schema(data)) + "\n"


def _introspect(client: httpx.Client, env: str, headers: dict[str, str]) -> dict:
    try:
        response = client.post(
            get_graphql_url(GPPEnvironment(env)),
            json={"query": INTROSPECTION_QUERY},
            headers=headers,
        )
    except httpx.HTTPError as exc:
        raise SchemaDownloadError(f"{env}: request failed: {exc}") from exc

    if response.status_code in (401, 403):
        raise _Refused
    if response.is_error:
        raise SchemaDownloadError(f"{env}: HTTP {response.status_code}.")

    try:
        body = response.json()
    except ValueError as exc:
        raise SchemaDownloadError(f"{env}: response is not JSON.") from exc

    data = body.get("data") if isinstance(body, dict) else None
    if not isinstance(data, dict) or "__schema" not in data:
        if isinstance(body, dict) and body.get("errors"):
            raise _Refused
        raise SchemaDownloadError(f"{env}: response has no schema.")
    return data


@app.command()
def main(
    environments: Annotated[
        list[str] | None,
        typer.Argument(
            help="Environments to download; both when omitted.",
            show_default=False,
        ),
    ] = None,
    output_dir: Annotated[
        Path | None,
        typer.Option(help="Directory to write into; graphql/schemas by default."),
    ] = None,
) -> None:
    """
    Download environment schemas by introspection.

    Introspection is anonymous. If a server refuses it, set that environment's
    token: GPP_DEVELOPMENT_TOKEN or GPP_TOKEN (production).
    """
    schemas_dir = output_dir or BuildPaths.for_repo(Path.cwd()).schemas_dir
    selected = (
        [env.lower() for env in environments] if environments else USER_ENVIRONMENTS
    )
    try:
        with output.status("Downloading schemas..."):
            written = download_schemas(schemas_dir, selected)
    except SchemaDownloadError as exc:
        output.fail(str(exc))
        raise typer.Exit(code=1) from exc

    for path in written:
        output.success(f"Wrote {path}")


if __name__ == "__main__":
    app()
