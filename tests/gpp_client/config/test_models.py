import pytest  # type: ignore
from pydantic import ValidationError

from gpp_client.config import GPPDefaults, GPPEnvironment
from gpp_client.config.models import ConfigFile, Tokens


@pytest.mark.parametrize(
    "development, staging, production, expected_dev, expected_staging, expected_prod",
    [
        ("", " ", "token", None, None, "token"),
        (None, None, "token", None, None, "token"),
    ],
)
def test_tokens_empty_and_none_to_expected(
    development, staging, production, expected_dev, expected_staging, expected_prod
):
    """
    Test that Tokens model converts empty strings to None and keeps None as None.
    """
    tokens = Tokens(DEVELOPMENT=development, STAGING=staging, PRODUCTION=production)
    assert tokens.DEVELOPMENT == expected_dev
    assert tokens.STAGING == expected_staging
    assert tokens.PRODUCTION == expected_prod


@pytest.mark.parametrize(
    "development, staging, production, expected_dev, expected_staging, expected_prod",
    [
        (None, None, "token", "", "", "token"),
    ],
)
def test_tokens_none_to_empty_string_serialization(
    development, staging, production, expected_dev, expected_staging, expected_prod
):
    """
    Test that Tokens model serializes None values to empty strings.
    """
    tokens = Tokens(DEVELOPMENT=development, STAGING=staging, PRODUCTION=production)
    serialized = tokens.model_dump()
    assert serialized["DEVELOPMENT"] == expected_dev
    assert serialized["STAGING"] == expected_staging
    assert serialized["PRODUCTION"] == expected_prod


def test_config_default_values():
    """
    Test that ConfigFile model has correct default values.
    """
    config = ConfigFile()
    assert config.env == GPPDefaults.default_env
    assert config.disable_env_vars == GPPDefaults.disable_env_vars
    assert isinstance(config.tokens, Tokens)


def test_config_custom_values():
    """
    Test that ConfigFile model accepts custom values.
    """
    tokens = Tokens(
        DEVELOPMENT="dev_token", STAGING="staging_token", PRODUCTION="prod_token"
    )
    config = ConfigFile(
        env=GPPEnvironment.STAGING, disable_env_vars=True, tokens=tokens
    )
    assert config.env == GPPEnvironment.STAGING
    assert config.disable_env_vars is True
    assert config.tokens == tokens


@pytest.mark.parametrize(
    "invalid_development",
    [123, 45.6, {}, [], True],
)
def test_tokens_validation_error(invalid_development):
    """
    Test that Tokens model raises ValidationError for invalid DEVELOPMENT types.
    """
    with pytest.raises(ValidationError):
        Tokens(DEVELOPMENT=invalid_development)  # Invalid type, should be str or None
