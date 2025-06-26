#!/usr/bin/env python3

import os
import subprocess
import sys
import logging

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - [%(levelname)s] %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
)


def fail(message: str) -> None:
    logging.error(message)
    sys.exit(1)


def main() -> None:
    logging.info("Downloading GPP Graphql schema.")

    # Check for required Python modules.
    try:
        import aiohttp  # noqa: F401
        import gql  # noqa: F401
    except ImportError:
        fail('Missing required modules "gql" and "aiohttp"')

    # Read environment variables.
    GPP_URL = os.getenv("GPP_URL")
    GPP_TOKEN = os.getenv("GPP_TOKEN")

    if not GPP_URL or not GPP_TOKEN:
        fail("GPP_URL and GPP_TOKEN environment variables must be set.")

    # Compose command.
    cmd = [
        "gql-cli",
        GPP_URL,
        "--transport",
        "aiohttp",
        "--print-schema",
        "--schema-download",
        # "input_value_deprecation:true",
        "-H",
        f"Authorization:Bearer {GPP_TOKEN}",
    ]

    try:
        result = subprocess.run(
            cmd,
            check=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
        )
        with open("schema.graphql", "wb") as f:
            f.write(result.stdout)

        logging.info("Schema downloaded successfully.")
    except subprocess.CalledProcessError as e:
        fail(e.stderr.decode())


if __name__ == "__main__":
    main()
