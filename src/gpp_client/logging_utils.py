"""
Utility functions for logging within the gpp_client package.
"""

__all__ = ["_enable_dev_console_logging"]

import logging

_DEFAULT_LOGGER = logging.getLogger("gpp_client")


def _enable_dev_console_logging(
    *,
    level: int | str = logging.DEBUG,
    logger: logging.Logger = _DEFAULT_LOGGER,
) -> None:
    """
    Enable console logging for ``gpp_client`` during development.

    Parameters
    ----------
    level : int | str, default=logging.DEBUG
        The logging level for the console handler.
    logger : logging.Logger, default=_DEFAULT_LOGGER
        Logger instance to configure. Defaults to the ``gpp_client`` logger.
    """
    if any(isinstance(h, logging.StreamHandler) for h in logger.handlers):
        return

    handler = logging.StreamHandler()
    handler.setLevel(level)

    formatter = logging.Formatter("{levelname} {message}", style="{")
    handler.setFormatter(formatter)

    logger.setLevel(logging.DEBUG)
    logger.addHandler(handler)
