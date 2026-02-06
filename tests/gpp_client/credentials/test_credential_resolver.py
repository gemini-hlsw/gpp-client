import pytest  # type: ignore

from gpp_client.config import GPPConfig, GPPDefaults, GPPEnvironment
from gpp_client.credentials import CredentialResolver, EnvVarReader
from gpp_client.exceptions import GPPAuthError


@pytest.fixture
def mock_config(mocker):
    config = mocker.Mock(spec=GPPConfig)
    config.use_env_vars.return_value = True
    config.active_env = GPPEnvironment.DEVELOPMENT
    config.active_token = "config_token"
    return config


@pytest.mark.parametrize("explicit_env", [None, GPPEnvironment.PRODUCTION])
def test_resolve_env_priority_order(mock_config, explicit_env, mocker):
    """
    Test that resolve_env respects priority:
    1. Explicit argument
    2. Environment variable (if enabled)
    3. Configuration file
    """
    mocker.patch.object(EnvVarReader, "get_env", return_value=GPPEnvironment.STAGING)

    result = CredentialResolver.resolve_env(env=explicit_env, config=mock_config)
    expected = explicit_env or GPPEnvironment.STAGING

    assert result == expected, (
        f"Expected environment '{expected}', got '{result}'. "
        "Explicit args take priority, then env vars, then config."
    )


def test_resolve_env_fallback_to_config_if_env_vars_disabled(mock_config, mocker):
    """
    Test that resolve_env falls back to config when env vars are disabled.
    """
    mock_config.use_env_vars.return_value = False
    mocker.patch.object(EnvVarReader, "get_env", return_value=GPPEnvironment.STAGING)

    result = CredentialResolver.resolve_env(env=None, config=mock_config)

    assert result == GPPEnvironment.DEVELOPMENT, (
        "When env vars disabled, config.active_env must be used."
    )


@pytest.mark.parametrize(
    "explicit_token,env_token,env_fallback_token,config_token,expected",
    [
        ("explicit", None, None, None, "explicit"),
        (None, "env_token", None, None, "env_token"),
        (None, None, "env_fallback_token", None, "env_fallback_token"),
        (None, None, None, "config_token", "config_token"),
    ],
)
def test_resolve_token_sources(
    mock_config,
    mocker,
    explicit_token,
    env_token,
    env_fallback_token,
    config_token,
    expected,
):
    """
    Test that resolve_token respects priority:
    1. Explicit argument
    2. Environment variable (specific to env)
    3. Environment variable (generic)
    4. Configuration file
    """
    mock_config.active_token = config_token

    mocker.patch.object(EnvVarReader, "get_env_token", return_value=env_token)
    mocker.patch.object(EnvVarReader, "get_token", return_value=env_fallback_token)

    result = CredentialResolver.resolve_token(
        token=explicit_token,
        env=GPPEnvironment.PRODUCTION,
        config=mock_config,
    )

    assert result == expected, (
        f"Expected token '{expected}', got '{result}'. "
        "Token priority order did not match expected resolution."
    )


def test_resolve_token_raises_if_unresolved(mock_config, mocker):
    """
    Test that resolve_token raises GPPAuthError if no token can be resolved.
    """
    mock_config.active_token = None
    mocker.patch.object(EnvVarReader, "get_env_token", return_value=None)
    mocker.patch.object(EnvVarReader, "get_token", return_value=None)

    with pytest.raises(GPPAuthError, match="No valid token found"):
        CredentialResolver.resolve_token(
            token=None,
            env=GPPEnvironment.STAGING,
            config=mock_config,
        )


def test_resolve_returns_correct_tuple(mock_config, mocker):
    """
    Test that CredentialResolver.resolve returns the correct (url, token, env) tuple.
    """
    mocker.patch.object(
        CredentialResolver, "resolve_env", return_value=GPPEnvironment.PRODUCTION
    )
    mocker.patch.object(
        CredentialResolver, "resolve_token", return_value="resolved_token"
    )

    url, token, env = CredentialResolver.resolve(
        env=None, token=None, config=mock_config
    )

    assert url == GPPDefaults.url[GPPEnvironment.PRODUCTION]
    assert token == "resolved_token"
    assert env == GPPEnvironment.PRODUCTION


@pytest.mark.parametrize("explicit_env", [None, GPPEnvironment.STAGING])
@pytest.mark.parametrize("explicit_token", [None, "explicit_token"])
@pytest.mark.parametrize("use_env_vars", [True, False])
@pytest.mark.parametrize("env_var_env", [None, GPPEnvironment.PRODUCTION])
@pytest.mark.parametrize("env_env_token", [None, "env_specific_token"])
@pytest.mark.parametrize("env_generic_token", [None, "generic_token"])
def test_resolve_all_combinations(
    mock_config,
    mocker,
    explicit_env,
    explicit_token,
    use_env_vars,
    env_var_env,
    env_env_token,
    env_generic_token,
):
    """
    Exhaustively test resolution combinations for CredentialResolver.resolve.

    Priority:
        Environment: explicit > env var > config
        Token: explicit > env var (specific) > env var (generic) > config
    """
    # Setup config behavior.
    mock_config.use_env_vars.return_value = use_env_vars

    # Patch environment variable readers.
    mocker.patch.object(EnvVarReader, "get_env", return_value=env_var_env)
    mocker.patch.object(EnvVarReader, "get_env_token", return_value=env_env_token)
    mocker.patch.object(EnvVarReader, "get_token", return_value=env_generic_token)

    # Cannot hardcode expected values, compute them.
    # Compute expected environment resolution
    if explicit_env is not None:
        expected_env = explicit_env
    elif use_env_vars and env_var_env is not None:
        expected_env = env_var_env
    else:
        expected_env = mock_config.active_env

    # Compute expected token resolution.
    if explicit_token is not None:
        expected_token = explicit_token
    elif use_env_vars and env_env_token is not None:
        expected_token = env_env_token
    elif use_env_vars and env_generic_token is not None:
        expected_token = env_generic_token
    else:
        expected_token = mock_config.active_token

    # Execute resolve
    url, token, resolved_env = CredentialResolver.resolve(
        env=explicit_env,
        token=explicit_token,
        config=mock_config,
    )

    # Expected URL
    expected_url = GPPDefaults.url[expected_env]

    assert resolved_env == expected_env, (
        f"Env mismatch: expected {expected_env}, got {resolved_env}. "
        f"explicit_env={explicit_env}, env_var={env_var_env}, config={mock_config.active_env}"
    )

    assert token == expected_token, (
        f"Token mismatch: expected '{expected_token}', got '{token}'. "
        f"explicit_token={explicit_token}, env_specific={env_env_token}, "
        f"env_generic={env_generic_token}, config={mock_config.active_token}"
    )

    assert url == expected_url, (
        f"URL mismatch: expected {expected_url}, got {url}. "
        f"Resolved env used was {resolved_env}"
    )


def test_resolve_raises_no_token_any_path(mocker, mock_config):
    """
    Confirm raise when all sources produce no token and config token is None.
    """
    mock_config.active_token = None
    mock_config.use_env_vars.return_value = True

    mocker.patch.object(EnvVarReader, "get_env_token", return_value=None)
    mocker.patch.object(EnvVarReader, "get_token", return_value=None)
    mocker.patch.object(EnvVarReader, "get_env", return_value=GPPEnvironment.STAGING)

    with pytest.raises(GPPAuthError, match="No valid token found"):
        CredentialResolver.resolve(env=None, token=None, config=mock_config)
