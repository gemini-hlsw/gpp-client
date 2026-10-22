"""
Name the GPP environment in one of the sources the settings read.
"""

from pathlib import Path

import pytest


def write_environment(
    source: str,
    name: str,
    monkeypatch: pytest.MonkeyPatch,
    folder: Path,
    config_path: Path,
) -> None:
    """
    Set the environment name in one settings source.

    Parameters
    ----------
    source : str
        ``"variable"``, ``"dotenv"`` or ``"config"``.
    name : str
        The environment name to write.
    monkeypatch : pytest.MonkeyPatch
        Sets the environment variable.
    folder : Path
        The folder holding the ``.env`` file.
    config_path : Path
        The configuration file.
    """
    if source == "variable":
        monkeypatch.setenv("GPP_ENVIRONMENT", name)
    elif source == "dotenv":
        (folder / ".env").write_text(f"GPP_ENVIRONMENT={name}\n")
    else:
        config_path.parent.mkdir(parents=True, exist_ok=True)
        config_path.write_text(f'environment = "{name}"\n')
