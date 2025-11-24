from pathlib import Path

import pytest  # type: ignore

from gpp_client.config import GPPConfig, GPPEnvironment
from gpp_client.exceptions import GPPClientError, GPPValidationError


class TestGPPConfig:
    """
    Tests for the GPPConfig class.
    """

    @pytest.fixture
    def mock_app_dir(self, mocker, tmp_path) -> Path:
        """
        Mock the application directory to use a temporary path.
        """
        app_dir = tmp_path / "gpp-config-test"
        mocker.patch("typer.get_app_dir", return_value=app_dir)
        return app_dir

    @pytest.fixture
    def config(self, mock_app_dir) -> GPPConfig:
        """
        Fixture to provide a GPPConfig instance for testing.
        """
        return GPPConfig()

    def test_exists_false_initially(self, config: GPPConfig):
        """
        Test that the config file does not exist initially.
        """
        assert not config.exists(), "Expected config file to not exist yet."

    def test_save_and_exists(self, config: GPPConfig):
        """
        Test saving the config file and checking existence.
        """
        config.save()
        assert config.exists(), "Expected config file to exist after save."

    def test_active_env_default(self, config: GPPConfig):
        """
        Test that the active environment is set to default initially.
        """
        assert isinstance(config.active_env, GPPEnvironment), (
            "Expected active_env to be of type GPPEnvironment."
        )

    def test_active_token_none_initially(self, config: GPPConfig):
        """
        Test that the active token is None initially.
        """
        assert config.active_token is None, "Expected no token to be set initially."

    def test_has_credentials_false_by_default(self, config: GPPConfig):
        """
        Test that has_credentials is False when no tokens are set.
        """
        assert not config.has_credentials, (
            "Expected has_credentials to be False initially."
        )

    @pytest.mark.parametrize("env", list(GPPEnvironment))
    def test_set_and_get_token(self, config: GPPConfig, env: GPPEnvironment):
        """
        Test setting and getting a token for each environment.
        """
        token = f"token-for-{env.value}"
        config.set_token(env, token)
        assert config.get_token_for(env) == token, (
            f"Token mismatch for environment {env}."
        )

    @pytest.mark.parametrize("env", list(GPPEnvironment))
    def test_clear_token(self, config: GPPConfig, env: GPPEnvironment):
        """
        Test clearing a token for each environment.
        """
        config.set_token(env, "dummy-token")
        config.clear_token(env)
        assert config.get_token_for(env) is None, f"Token was not cleared for {env}."

    def test_clear_tokens(self, config: GPPConfig):
        """
        Test clearing all tokens.
        """
        for env in GPPEnvironment:
            config.set_token(env, f"token-{env.value}")
        config.clear_tokens()
        assert all(config.get_token_for(env) is None for env in GPPEnvironment), (
            "Expected all tokens to be cleared."
        )

    def test_get_all_envs_with_tokens(self, config: GPPConfig):
        """
        Test retrieving all environments with non-empty tokens.
        """
        # Clear all tokens first.
        config.clear_tokens()
        # Set tokens for some environments.
        config.set_token("DEVELOPMENT", "dev-token")
        tokens = config.get_all_envs_with_tokens()
        assert GPPEnvironment.DEVELOPMENT in tokens, (
            "Expected development token to be included."
        )
        assert GPPEnvironment.STAGING not in tokens, (
            "Expected staging token to be excluded due to whitespace."
        )

    def test_activate_environment(self, config: GPPConfig):
        """
        Test activating a specific environment.
        """
        config.activate("STAGING")
        assert config.active_env == GPPEnvironment.STAGING, (
            "Expected active environment to be staging."
        )

    def test_set_credentials_activates_and_saves(self, config: GPPConfig, mocker):
        """
        Test setting credentials activates the environment and saves the config.
        """
        spy = mocker.spy(config, "save")
        config.set_credentials("PRODUCTION", "prod-token", activate=True, save=True)
        assert config.active_env == GPPEnvironment.PRODUCTION, (
            "Expected production to be active environment."
        )
        assert config.get_token_for("PRODUCTION") == "prod-token", (
            "Expected token to be set for production."
        )
        assert spy.call_count == 1, "Expected save() to be called once."

    def test_disable_and_enable_env_vars(self, config: GPPConfig):
        """
        Test disabling and enabling environment variable usage.
        """
        config.disable_env_vars()
        assert not config.use_env_vars(), "Expected env vars to be disabled."

        config.enable_env_vars()
        assert config.use_env_vars(), "Expected env vars to be enabled."

    def test_create_default_config_file(self, mock_app_dir: Path):
        """
        Test creating the default config file.
        """
        path = GPPConfig._get_app_dir()
        if path.exists():
            path.unlink()
        GPPConfig.create_default_config_file()
        assert path.exists(), "Expected default config file to be created."

    def test_load_with_invalid_toml(self, mock_app_dir: Path):
        """
        Test loading configuration with invalid TOML content raises an error.
        """
        path = GPPConfig._get_app_dir()
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text("invalid = TOML:::")
        with pytest.raises(GPPValidationError):
            GPPConfig()

    def test_set_token_validation_error(self, config: GPPConfig):
        """
        Test that setting a token with only whitespace raises a validation error.
        """
        with pytest.raises(GPPValidationError):
            config.set_token("DEVELOPMENT", "  ")

    def test_to_dict(self, config: GPPConfig):
        """
        Test converting the config to a dictionary.
        """
        config_dict = config.to_dict()
        assert isinstance(config_dict, dict), "Expected to_dict to return a dictionary."
        assert "env" in config_dict, "Expected 'env' key in the dictionary."
        assert "tokens" in config_dict, "Expected 'tokens' key in the dictionary."

    def test_to_json(self, config: GPPConfig):
        """
        Test converting the config to a JSON string.
        """
        config_json = config.to_json()
        assert isinstance(config_json, str), "Expected to_json to return a JSON string."
        assert "env" in config_json, "Expected 'env' key in the JSON string."
        assert "tokens" in config_json, "Expected 'tokens' key in the JSON string."

    def test_to_dict_with_invalid_data(self, config: GPPConfig, mocker):
        """
        Test that to_dict raises GPPClientError when model_dump fails.
        """
        mocker.patch.object(
            type(config._data), "model_dump", side_effect=Exception("Mocked exception")
        )
        with pytest.raises(GPPClientError, match="Failed to convert config to dict"):
            config.to_dict()

    def test_to_json_with_invalid_data(self, config: GPPConfig, mocker):
        """
        Test that to_json raises GPPClientError when model_dump_json fails.
        """
        mocker.patch.object(
            type(config._data),
            "model_dump_json",
            side_effect=Exception("Mocked exception"),
        )
        with pytest.raises(GPPClientError, match="Failed to convert config to JSON"):
            config.to_json()

    def test_to_toml(self, config: GPPConfig):
        """
        Test converting the config to a TOML string.
        """
        config_toml = config.to_toml()
        assert isinstance(config_toml, str), "Expected to_toml to return a TOML string."
        assert "[env]" in config_toml or "[tokens]" in config_toml, (
            "Expected TOML string to contain configuration sections."
        )

    def test_to_toml_with_invalid_data(self, config: GPPConfig, mocker):
        """
        Test that to_toml raises GPPClientError when to_dict fails.
        """
        mocker.patch.object(
            config, "to_dict", side_effect=Exception("Mocked exception")
        )
        with pytest.raises(GPPClientError, match="Failed to convert config to TOML"):
            config.to_toml()
