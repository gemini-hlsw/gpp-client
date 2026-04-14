"""Shared pytest fixtures for CLI tests."""

from typing import Any, Callable

import pytest
from typer.testing import CliRunner

from gpp_client.cli.cli import app


class DummyAsyncClient:
    """
    Minimal async context manager client for CLI tests.
    """

    def __init__(self, **services: Any) -> None:
        """
        Initialize the dummy client.

        Parameters
        ----------
        **services : Any
            Attributes to attach to the client.
        """
        for name, value in services.items():
            setattr(self, name, value)

    async def __aenter__(self) -> "DummyAsyncClient":
        """
        Enter the async context.

        Returns
        -------
        DummyAsyncClient
            This client instance.
        """
        return self

    async def __aexit__(self, exc_type, exc, tb) -> None:
        """
        Exit the async context.
        """
        return None


@pytest.fixture()
def runner() -> CliRunner:
    """
    Return a Typer CLI runner.

    Returns
    -------
    CliRunner
        CLI test runner.
    """
    return CliRunner()


@pytest.fixture()
def cli_app():
    """
    Import the CLI app lazily.

    Returns
    -------
    typer.Typer
        CLI application.
    """

    return app


@pytest.fixture()
def dummy_async_client_factory() -> Callable[..., DummyAsyncClient]:
    """
    Return a factory for dummy async clients.
    """

    def factory(**services: Any) -> DummyAsyncClient:
        """
        Build a dummy async client.
        """
        return DummyAsyncClient(**services)

    return factory
