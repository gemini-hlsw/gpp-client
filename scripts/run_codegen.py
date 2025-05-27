#!/usr/bin/env python3

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
    logging.error(message)
    sys.exit(1)


def main() -> None:
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