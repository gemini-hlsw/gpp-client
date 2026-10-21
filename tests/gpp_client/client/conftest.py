"""
Shared pytest fixtures for client tests.
"""

import pytest


@pytest.fixture()
def _no_user_configuration(monkeypatch, tmp_path):
    """
    Clear the environment variables and point the config file at an empty folder.
    """
    for name in (
        "GPP_ENVIRONMENT",
        "GPP_TOKEN",
        "GPP_DEVELOPMENT_TOKEN",
    ):
        monkeypatch.delenv(name, raising=False)
    config_path = tmp_path / "config.toml"
    monkeypatch.setattr("gpp_client.settings.get_config_path", lambda: config_path)
    return config_path
