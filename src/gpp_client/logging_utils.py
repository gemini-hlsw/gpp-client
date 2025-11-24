"""
Utility functions for logging within the gpp_client package.
"""

__all__ = ["_enable_dev_console_logging"]

import logging

logger = logging.getLogger("gpp_client")


def _enable_dev_console_logging(level: int | str = logging.DEBUG) -> None:
    """
    Enable console logging for gpp_client during development.

    Parameters
    ----------
    level : int | str, default=logging.DEBUG
        The logging level for the console handler. Can be an integer or string
        representation of the logging level (e.g., 'DEBUG', 'INFO').
    """
    # Check if a stream handler is already present.
    if any(isinstance(h, logging.StreamHandler) for h in logger.handlers):
        return

    handler = logging.StreamHandler()

    handler.setLevel(level)
    formatter = logging.Formatter("{levelname} {message}", style="{")
    handler.setFormatter(formatter)

    # Set logger level to DEBUG to ensure all messages are processed.
    logger.setLevel(logging.DEBUG)
    logger.addHandler(handler)
