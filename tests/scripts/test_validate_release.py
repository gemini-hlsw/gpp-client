"""
Tests for the release validation script.
"""

from pathlib import Path

import pytest

from scripts import validate_release as release
from scripts.validate_release import ReleaseValidationError


@pytest.fixture()
def env_file(tmp_path: Path) -> Path:
    """
    Return a temporary package environment file path.
    """
    return tmp_path / "src" / "gpp_client" / "generated" / "package_environment.py"


def write_env_file(path: Path, environment: str) -> None:
    """
    Write a generated package environment file.
    """
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(
        '"""\n'
        "Package-level environment constant for generated client code.\n"
        '"""\n\n'
        f'PACKAGE_ENVIRONMENT = "{environment}"\n',
        encoding="utf-8",
    )


@pytest.mark.parametrize(
    ("tag", "expected"),
    [
        ("v26.5.0.dev1", "DEVELOPMENT"),
        ("v26.5.0.dev12", "DEVELOPMENT"),
        ("v26.5.0", "PRODUCTION"),
        ("v26.12.3", "PRODUCTION"),
    ],
)
def test_expected_environment(tag: str, expected: str) -> None:
    """
    Expected environment is inferred from the release tag.
    """
    assert release._expected_environment(tag) == expected


@pytest.mark.parametrize("environment", ["DEVELOPMENT", "PRODUCTION"])
def test_parse_environment_returns_environment(
    env_file: Path,
    environment: str,
) -> None:
    """
    Environment is parsed from the generated environment file.
    """
    write_env_file(env_file, environment)

    assert release._parse_environment(env_file) == environment


def test_parse_environment_raises_for_missing_file(env_file: Path) -> None:
    """
    Missing environment file raises a release validation error.
    """
    with pytest.raises(ReleaseValidationError, match="Missing environment file"):
        release._parse_environment(env_file)


@pytest.mark.parametrize(
    "content",
    [
        "",
        'PACKAGE_ENVIRONMENT = "STAGING"\n',
        "PACKAGE_ENVIRONMENT = DEVELOPMENT\n",
        'OTHER_ENVIRONMENT = "PRODUCTION"\n',
        'PACKAGE_ENVIRONMENT: str = "PRODUCTION"\n',
    ],
)
def test_parse_environment_raises_for_invalid_file_content(
    env_file: Path,
    content: str,
) -> None:
    """
    Invalid environment file content raises a release validation error.
    """
    env_file.parent.mkdir(parents=True, exist_ok=True)
    env_file.write_text(content, encoding="utf-8")

    with pytest.raises(
        ReleaseValidationError,
        match="Could not find a valid PACKAGE_ENVIRONMENT",
    ):
        release._parse_environment(env_file)


@pytest.mark.parametrize(
    ("tag", "environment"),
    [
        ("v26.5.0.dev1", "DEVELOPMENT"),
        ("v26.5.0.dev10", "DEVELOPMENT"),
        ("v26.5.0", "PRODUCTION"),
        ("v26.12.2", "PRODUCTION"),
    ],
)
def test_validate_release_accepts_valid_tag_and_matching_environment(
    env_file: Path,
    tag: str,
    environment: str,
) -> None:
    """
    Valid release tags pass when the package environment matches.
    """
    write_env_file(env_file, environment)

    release.validate_release(tag, env_file)


@pytest.mark.parametrize(
    "tag",
    [
        "26.5.0",
        "v2026.5.0",
        "v26.05.0",
        "v26.5",
        "v26.5.0.1",
        "v26.5.0-dev.1",
        "v26.5.0.dev",
        "v26.5.0.dev0.dev1",
        "v26.5.0rc1",
        "release-v26.5.0",
        "",
    ],
)
def test_validate_release_raises_for_invalid_tag(
    env_file: Path,
    tag: str,
) -> None:
    """
    Invalid release tag formats raise a release validation error.
    """
    write_env_file(env_file, "PRODUCTION")

    with pytest.raises(ReleaseValidationError, match="Invalid release tag"):
        release.validate_release(tag, env_file)


@pytest.mark.parametrize(
    ("tag", "environment", "expected"),
    [
        ("v26.5.0.dev1", "PRODUCTION", "DEVELOPMENT"),
        ("v26.5.0", "DEVELOPMENT", "PRODUCTION"),
    ],
)
def test_validate_release_raises_for_environment_mismatch(
    env_file: Path,
    tag: str,
    environment: str,
    expected: str,
) -> None:
    """
    Release validation fails when tag type and package environment mismatch.
    """
    write_env_file(env_file, environment)

    with pytest.raises(ReleaseValidationError) as exc_info:
        release.validate_release(tag, env_file)

    message = str(exc_info.value)

    assert "Package environment does not match release tag." in message
    assert f"Tag: {tag}" in message
    assert f"Expected PACKAGE_ENVIRONMENT: {expected}" in message
    assert f"Actual PACKAGE_ENVIRONMENT: {environment}" in message


def test_validate_release_uses_default_environment_file(
    env_file: Path,
    mocker,
) -> None:
    """
    Default environment file is used when no path is provided.
    """
    write_env_file(env_file, "PRODUCTION")
    mocker.patch.object(release, "ENV_FILE", env_file)

    release.validate_release("v26.5.0", env_file=release.ENV_FILE)


def test_main_exits_with_usage_when_tag_is_missing(mocker) -> None:
    """
    CLI exits with usage text when no tag is provided.
    """
    mocker.patch.object(release.sys, "argv", ["validate_release.py"])

    with pytest.raises(SystemExit, match="Usage: validate_release.py <tag>"):
        release.main()


def test_main_exits_with_error_for_invalid_release(
    env_file: Path,
    mocker,
    capsys,
) -> None:
    """
    CLI exits with code 1 and writes validation errors to stderr.
    """
    write_env_file(env_file, "PRODUCTION")

    mocker.patch.object(release, "ENV_FILE", env_file)
    mocker.patch.object(release.sys, "argv", ["validate_release.py", "v26.5.0.dev1"])
    mocker.patch.object(
        release,
        "validate_release",
        side_effect=ReleaseValidationError("validation failed"),
    )

    with pytest.raises(SystemExit) as exc_info:
        release.main()

    captured = capsys.readouterr()

    assert exc_info.value.code == 1
    assert "validation failed" in captured.err


def test_main_validates_tag_from_argv(mocker) -> None:
    """
    CLI passes the provided tag to release validation.
    """
    validate_release = mocker.patch.object(release, "validate_release")
    mocker.patch.object(release.sys, "argv", ["validate_release.py", "v26.5.0"])

    release.main()

    validate_release.assert_called_once_with("v26.5.0")
