"""
Shared fixtures for domain tests.
"""

from types import SimpleNamespace

import pytest


@pytest.fixture()
def graphql(mocker):
    """
    Return a reusable mocked GraphQL client.
    """
    return mocker.Mock()


@pytest.fixture()
def rest(mocker):
    """
    Return a reusable mocked REST client.
    """
    return mocker.Mock()


@pytest.fixture()
def settings() -> SimpleNamespace:
    """
    Return a reusable mocked settings object.
    """
    return SimpleNamespace(debug=False)


@pytest.fixture()
def domain_kwargs(graphql, rest, settings) -> dict[str, object]:
    """
    Return shared domain constructor keyword arguments.
    """
    return {
        "graphql": graphql,
        "rest": rest,
        "settings": settings,
    }
