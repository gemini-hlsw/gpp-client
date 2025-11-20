import os

import pytest  # type: ignore

from gpp_client.config import GPPDefaults, GPPEnvironment
from gpp_client.credentials.env_var_reader import EnvVarReader


@pytest.mark.parametrize(
    "value, expected",
    [
        (None, None),
        ("PRODUCTION", GPPEnvironment.PRODUCTION),
        ("invalid", None),
    ],
)
def test_get_env(mocker, value: str | None, expected: GPPEnvironment | None):
    """
    Test EnvVarReader.get_env with various environment values.
    """
    mocker.patch.dict(
        os.environ, {GPPDefaults.env_var_env: value} if value else {}, clear=True
    )
    assert EnvVarReader.get_env() == expected


@pytest.mark.parametrize(
    ("env_key", "token_var", "token_value", "expected"),
    [
        (
            "PRODUCTION",
            GPPDefaults.env_var_env_tokens[GPPEnvironment.PRODUCTION],
            "abc123",
            "abc123",
        ),
        (
            "STAGING",
            GPPDefaults.env_var_env_tokens[GPPEnvironment.STAGING],
            "def456",
            "def456",
        ),
        (
            "DEVELOPMENT",
            GPPDefaults.env_var_env_tokens[GPPEnvironment.DEVELOPMENT],
            None,
            None,
        ),  # not set in env
        ("MISSING", None, None, None),  # env not defined in token map
    ],
)
def test_get_env_token(mocker, env_key, token_var, token_value, expected):
    """
    Test EnvVarReader.get_env_token returns correct tokens or None.
    """
    # Patch token variable in environment.
    mocker.patch.dict(
        os.environ, {token_var: token_value} if token_value else {}, clear=True
    )
    result = EnvVarReader.get_env_token(env_key)
    assert result == expected


@pytest.mark.parametrize(
    "env_value",
    ["abc-token", None],
)
def test_get_token(mocker, env_value):
    """
    Test EnvVarReader.get_token reads the general token.
    """
    env = {GPPDefaults.env_var_token: env_value} if env_value else {}
    mocker.patch.dict(os.environ, env, clear=True)
    assert EnvVarReader.get_token() == env_value
