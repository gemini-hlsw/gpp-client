#!/usr/bin/env python3
"""
Validate release tag and package environment consistency.
"""

import re
import sys
from pathlib import Path
from typing import Final

TAG_PATTERN: Final[re.Pattern[str]] = re.compile(r"^v\d{2}\.\d{1,2}\.\d+(?:\.dev\d+)?$")
ENV_PATTERN: Final[re.Pattern[str]] = re.compile(
    r'^PACKAGE_ENVIRONMENT\s*=\s*["\']'
    r'(?P<environment>DEVELOPMENT|PRODUCTION)["\']\s*$',
    re.MULTILINE,
)
ENV_FILE: Final[Path] = Path("src/gpp_client/generated/package_environment.py")


class ReleaseValidationError(RuntimeError):
    """
    Raised when release validation fails.
    """


def _parse_environment(path: Path = ENV_FILE) -> str:
    """
    Extract the generated package environment.

    Parameters
    ----------
    path : Path, default=ENV_FILE
        Path to the generated package environment file.

    Returns
    -------
    str
        Package environment value.

    Raises
    ------
    ReleaseValidationError
        Raised if the environment file is missing or invalid.
    """
    if not path.exists():
        raise ReleaseValidationError(f"Missing environment file: {path}")

    match = ENV_PATTERN.search(path.read_text(encoding="utf-8"))
    if match is None:
        raise ReleaseValidationError(
            f"Could not find a valid PACKAGE_ENVIRONMENT in {path}."
        )

    return match.group("environment")


def _expected_environment(tag: str) -> str:
    """
    Return the expected package environment for a release tag.

    Parameters
    ----------
    tag : str
        Release tag.

    Returns
    -------
    str
        Expected package environment.
    """
    return "DEVELOPMENT" if ".dev" in tag else "PRODUCTION"


def validate_release(tag: str, env_file: Path = ENV_FILE) -> None:
    """
    Validate release tag format and package environment consistency.

    Parameters
    ----------
    tag : str
        Release tag, including the leading ``v``.
    env_file : Path, optional
        Path to the generated package environment file.

    Raises
    ------
    ReleaseValidationError
        Raised if the release tag or package environment is invalid.
    """
    if TAG_PATTERN.fullmatch(tag) is None:
        raise ReleaseValidationError(
            f"Invalid release tag: {tag}. Expected format: v26.5.0 or v26.5.0.dev1."
        )

    expected = _expected_environment(tag)
    actual = _parse_environment(env_file)

    if actual != expected:
        raise ReleaseValidationError(
            "Package environment does not match release tag.\n"
            f"Tag: {tag}\n"
            f"Expected PACKAGE_ENVIRONMENT: {expected}\n"
            f"Actual PACKAGE_ENVIRONMENT: {actual}"
        )


def main() -> None:
    """
    Validate release inputs from the command line.
    """
    if len(sys.argv) != 2:
        raise SystemExit("Usage: validate_release.py <tag>")

    try:
        validate_release(sys.argv[1])
    except ReleaseValidationError as exc:
        print(exc, file=sys.stderr)
        raise SystemExit(1) from exc


if __name__ == "__main__":
    main()
