#!/usr/bin/env python3
"""
Validate a release tag.
"""

import re
import sys
from typing import Final

TAG_PATTERN: Final[re.Pattern[str]] = re.compile(r"^v\d{2}\.(?:[1-9]|1[0-2])\.\d+$")
DEV_TAG_PATTERN: Final[re.Pattern[str]] = re.compile(
    r"^v\d{2}\.(?:[1-9]|1[0-2])\.\d+\.dev\d+$"
)


class ReleaseValidationError(RuntimeError):
    """
    Raised when release validation fails.
    """


def validate_release(tag: str) -> None:
    """
    Validate a release tag.

    Parameters
    ----------
    tag : str
        Release tag, including the leading ``v``.

    Raises
    ------
    ReleaseValidationError
        Raised if the tag is a ``.devN`` pre-release tag or is not a CalVer
        release tag.
    """
    if DEV_TAG_PATTERN.fullmatch(tag):
        raise ReleaseValidationError(
            f"Pre-release tag refused: {tag}. gpp-client releases in one stream "
            "that reaches every environment, so there are no .devN releases. "
            "Use a release tag such as v26.5.0."
        )
    if TAG_PATTERN.fullmatch(tag) is None:
        raise ReleaseValidationError(
            f"Invalid release tag: {tag}. Expected format: v26.5.0."
        )


def main() -> None:
    """
    Validate a release tag from the command line.
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
