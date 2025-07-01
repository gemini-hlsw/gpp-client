#!/usr/bin/env python3
"""Runs the code generator."""

import subprocess
import sys
import logging
import shutil

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - [%(levelname)s] %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
)


def fail(message: str) -> None:
    """
    Log message and exit when failure.

    Parameters
    ----------
    message : str
        The message to log.
    """
    logging.error(message)
    sys.exit(1)


def main() -> None:
    """Run the codegen."""
    logging.info("Running ariadne-codegen.")

    # Check if ariadne-codegen is installed.
    if shutil.which("ariadne-codegen") is None:
        fail(
            "ariadne-codegen is not installed. Install with `pip install "
            '"ariadne-codegen[subscriptions]"`.'
        )

    # Run codegen.
    try:
        subprocess.run(
            ["ariadne-codegen"],
            check=True,
        )
        logging.info("ariadne-codegen completed successfully.")
    except subprocess.CalledProcessError as e:
        fail(e.stderr.decode())


if __name__ == "__main__":
    main()
