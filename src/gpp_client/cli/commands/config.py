"""
Commands that manage the configuration file.
"""

__all__ = ["config_app"]

import os
from pathlib import Path
from typing import Annotated

import tomlkit
import tomlkit.exceptions
import typer
from pydantic import SecretStr, TypeAdapter, ValidationError
from pydantic_settings import (
    BaseSettings,
    DotEnvSettingsSource,
    EnvSettingsSource,
    InitSettingsSource,
    PydanticBaseSettingsSource,
    TomlConfigSettingsSource,
)
from rich.table import Table
from tomlkit import TOMLDocument

from gpp_client import settings
from gpp_client.cli import output
from gpp_client.cli.console import console
from gpp_client.environment import GPPEnvironment
from gpp_client.exceptions import GPPClientError
from gpp_client.settings import GPPSettings, _environment_named, _token_setting

_TOKEN_KEYS = {_token_setting(env): env for env in GPPEnvironment}

config_app = typer.Typer(
    name="config",
    help="Create, show and edit the configuration file.",
)


@config_app.command("path")
def path() -> None:
    """
    Print the path to the configuration file.
    """
    # Plain echo, not Rich, so a long path never wraps inside $(gpp config path).
    typer.echo(settings.get_config_path())


@config_app.command("show")
def show(ctx: typer.Context) -> None:
    """
    Show the settings in effect and where each one came from.
    """
    environment = getattr(ctx.obj, "environment", None)
    try:
        effective, sources = _settings_with_sources(environment)
    except GPPClientError as exc:
        output.fail(str(exc))
        raise typer.Exit(code=1) from None
    except ValidationError as exc:
        for error in exc.errors():
            output.fail(f"Invalid {error['loc'][0]}: {error['msg']}.")
        raise typer.Exit(code=1) from None
    table = Table(box=None, padding=(0, 2, 0, 0))
    for header in ("Key", "Value", "Source"):
        table.add_column(header)
    for key in GPPSettings.model_fields:
        table.add_row(key, _shown(getattr(effective, key)), sources[key])
    console.print(table)


@config_app.command("init")
def init(
    force: Annotated[
        bool,
        typer.Option(
            "--force",
            help="Move an existing file to config.toml.bak, then write a new one.",
        ),
    ] = False,
) -> None:
    """
    Create the configuration file, asking for each token.
    """
    config_path = settings.get_config_path()
    if config_path.exists() and not force:
        output.fail(
            f"{config_path} already exists. To back it up and write a new one, "
            "run 'gpp config init --force'."
        )
        raise typer.Exit(code=1)
    document = tomlkit.document()
    for env in GPPEnvironment:
        token = _prompt_token(env, note=", blank to skip")
        if token:
            document[_token_setting(env)] = token
    if config_path.exists():
        backup = config_path.with_name(f"{config_path.name}.bak")
        config_path.replace(backup)
        output.info(f"Moved the old file to {backup}.")
    _write(config_path, document)
    output.success(f"Wrote {config_path}.")


@config_app.command("set")
def set_(
    key: Annotated[str, typer.Argument(help="The setting to change.")],
    value: Annotated[
        str | None,
        typer.Argument(help="The new value. Tokens are asked for instead."),
    ] = None,
) -> None:
    """
    Set one key in the configuration file, keeping the rest of the file.
    """
    config_path = settings.get_config_path()
    try:
        document = _read(config_path)
        parsed = _parse(key, value)
    except GPPClientError as exc:
        output.fail(str(exc))
        raise typer.Exit(code=1) from None
    document[key] = parsed
    _write(config_path, document)
    output.success(f"Set {key} in {config_path}.")


@config_app.command("unset")
def unset(
    key: Annotated[str, typer.Argument(help="The setting to remove.")],
) -> None:
    """
    Remove one key from the configuration file, keeping the rest of the file.
    """
    config_path = settings.get_config_path()
    try:
        _check_key(key)
        document = _read(config_path)
    except GPPClientError as exc:
        output.fail(str(exc))
        raise typer.Exit(code=1) from None
    if key not in document:
        output.info(f"{key} is not set in {config_path}.")
        return
    del document[key]
    _write(config_path, document)
    output.success(f"Removed {key} from {config_path}.")


@config_app.command("delete")
def delete(
    yes: Annotated[
        bool, typer.Option("--yes", help="Delete without asking first.")
    ] = False,
) -> None:
    """
    Delete the configuration file.
    """
    config_path = settings.get_config_path()
    if not config_path.exists():
        output.info(f"There is no configuration file at {config_path}.")
        return
    if not yes and not typer.confirm(f"Delete {config_path}?"):
        return
    config_path.unlink()
    output.success(f"Deleted {config_path}.")


def _settings_with_sources(
    environment: str | None,
) -> tuple[GPPSettings, dict[str, str]]:
    """
    Build the settings and name the source of each one.

    The sources come from ``GPPSettings`` itself, so the order shown is the
    order the client uses.
    """
    built: list[PydanticBaseSettingsSource] = []

    class _Traced(GPPSettings):
        @classmethod
        def settings_customise_sources(
            cls, settings_cls: type[BaseSettings], **sources: PydanticBaseSettingsSource
        ) -> tuple[PydanticBaseSettingsSource, ...]:
            built.extend(super().settings_customise_sources(settings_cls, **sources))
            return tuple(built)

    arguments = {} if environment is None else {"environment": environment}
    effective = _Traced(**arguments)
    names = {key: "default" for key in GPPSettings.model_fields}
    for source in reversed(built):
        for key in source():
            if key in names:
                names[key] = _source_name(source, key)
    return effective, names


def _source_name(source: PydanticBaseSettingsSource, key: str) -> str:
    """
    Name a settings source the way a user would recognize it.
    """
    inner = getattr(source, "_source", source)
    # Subclasses first: the TOML source is an init source, and .env an env one.
    if isinstance(inner, TomlConfigSettingsSource):
        return "configuration file"
    if isinstance(inner, DotEnvSettingsSource):
        return ".env file"
    if isinstance(inner, EnvSettingsSource):
        return f"variable {inner.env_prefix.upper()}{key.upper()}"
    if isinstance(inner, InitSettingsSource):
        return "--env"
    return type(inner).__name__


def _shown(value: object) -> str:
    """
    Format a setting for display, masking tokens to their last four characters.
    """
    if value is None:
        return "(not set)"
    if isinstance(value, SecretStr):
        secret = value.get_secret_value()
        # A token of four characters or fewer would show in full.
        return "****" + (secret[-4:] if len(secret) > 4 else "")
    if isinstance(value, GPPEnvironment):
        return value.label
    if isinstance(value, bool):
        return str(value).lower()
    return str(value)


def _parse(key: str, value: str | None) -> str | bool:
    """
    Return the value to store for a key, or raise naming what it accepts.
    """
    _check_key(key)
    if key in _TOKEN_KEYS:
        if value is not None:
            # An argument lands in shell history and process listings.
            raise GPPClientError(
                f"Pass {key} at the hidden prompt or on stdin, never as an argument."
            )
        return _ask_token(_TOKEN_KEYS[key])
    if value is None:
        raise GPPClientError(f"'gpp config set {key}' needs a value.")
    if key == "debug":
        try:
            return TypeAdapter(bool).validate_python(value)
        except ValidationError:
            raise GPPClientError(f"debug takes true or false, not {value!r}.") from None
    return _environment_named(value).label


def _ask_token(env: GPPEnvironment) -> str:
    """
    Return a token typed at a hidden prompt, or one line piped to stdin.
    """
    stdin = typer.get_text_stream("stdin")
    token = _prompt_token(env) if stdin.isatty() else stdin.readline().strip()
    if not token:
        raise GPPClientError(f"No token given for {_token_setting(env)}.")
    return token


def _check_key(key: str) -> None:
    """
    Raise naming the valid keys if ``key`` is not a setting.
    """
    valid = list(GPPSettings.model_fields)
    if key not in valid:
        raise GPPClientError(f"Unknown key {key!r}. Valid keys: {', '.join(valid)}.")


def _read(config_path: Path) -> TOMLDocument:
    """
    Read the configuration file, or start an empty one if there is none.
    """
    if not config_path.exists():
        return tomlkit.document()
    try:
        return tomlkit.parse(config_path.read_text(encoding="utf-8"))
    except tomlkit.exceptions.ParseError as exc:
        raise GPPClientError(
            f"Cannot read {config_path}: it is not valid TOML ({exc})."
        ) from None


def _prompt_token(env: GPPEnvironment, note: str = "") -> str:
    """
    Ask for one environment's token without echoing it.
    """
    answer = typer.prompt(
        f"{env.label.capitalize()} token ({env.token_variable}{note})",
        default="",
        hide_input=True,
        show_default=False,
    )
    return answer.strip()


def _write(config_path: Path, document: TOMLDocument) -> None:
    """
    Write the configuration file, creating its folder if needed.
    """
    config_path.parent.mkdir(parents=True, exist_ok=True)
    # The mode only applies on creation, so a user's own chmod survives edits.
    fd = os.open(config_path, os.O_WRONLY | os.O_CREAT | os.O_TRUNC, 0o600)
    with open(fd, "w", encoding="utf-8") as file:
        file.write(tomlkit.dumps(document))
