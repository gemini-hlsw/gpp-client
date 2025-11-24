from gpp_client.config import GPPDefaults, GPPEnvironment


class TestDefaults:
    """
    Tests for the _Defaults dataclass.
    """

    def test_default_values(self):
        """
        Test that the default values in _Defaults are correct.
        """
        assert GPPDefaults.config_filename == "config.toml"
        assert GPPDefaults.app_name == "gpp-client"
        assert GPPDefaults.default_env == GPPEnvironment.PRODUCTION
        assert (
            GPPDefaults.url[GPPEnvironment.DEVELOPMENT]
            == "https://lucuma-postgres-odb-dev.herokuapp.com/odb"
        )
        assert (
            GPPDefaults.url[GPPEnvironment.STAGING]
            == "https://lucuma-postgres-odb-staging.herokuapp.com/odb"
        )
        assert (
            GPPDefaults.url[GPPEnvironment.PRODUCTION]
            == "https://lucuma-postgres-odb-production.herokuapp.com/odb"
        )
        assert GPPDefaults.env_var_env == "GPP_ENV"
        assert GPPDefaults.env_var_token == "GPP_TOKEN"
        assert (
            GPPDefaults.env_var_env_tokens[GPPEnvironment.DEVELOPMENT]
            == "GPP_DEVELOPMENT_TOKEN"
        )
        assert (
            GPPDefaults.env_var_env_tokens[GPPEnvironment.STAGING]
            == "GPP_STAGING_TOKEN"
        )
        assert (
            GPPDefaults.env_var_env_tokens[GPPEnvironment.PRODUCTION]
            == "GPP_PRODUCTION_TOKEN"
        )
        assert GPPDefaults.disable_env_vars is False

    def test_url_keys(self):
        """
        Test that the URL dictionary contains all GPPEnvironment keys.
        """
        assert set(GPPDefaults.url.keys()) == {
            GPPEnvironment.DEVELOPMENT,
            GPPEnvironment.STAGING,
            GPPEnvironment.PRODUCTION,
        }

    def test_env_var_env_tokens_keys(self):
        """
        Test that the env_var_env_tokens dictionary contains all GPPEnvironment keys.
        """
        assert set(GPPDefaults.env_var_env_tokens.keys()) == {
            GPPEnvironment.DEVELOPMENT,
            GPPEnvironment.STAGING,
            GPPEnvironment.PRODUCTION,
        }
