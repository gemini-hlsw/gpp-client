"""
Tests for logging utilities.
"""

import logging

import pytest

from gpp_client.logging_utils import _enable_dev_console_logging


def test_enable_dev_console_logging_adds_handler_to_provided_logger() -> None:
    """
    Test that ``_enable_dev_console_logging`` adds a ``StreamHandler`` to the provided
    logger.
    """
    logger = logging.getLogger("test_logger")
    logger.handlers.clear()

    _enable_dev_console_logging(logger=logger)

    handlers = [h for h in logger.handlers if isinstance(h, logging.StreamHandler)]
    assert len(handlers) == 1
    assert handlers[0].level == logging.DEBUG
    assert logger.level == logging.DEBUG


def test_enable_dev_console_logging_is_idempotent() -> None:
    """
    Test that ``_enable_dev_console_logging`` does not add multiple ``StreamHandlers``
    to the same logger.
    """
    logger = logging.getLogger("test_logger_idempotent")
    logger.handlers.clear()

    _enable_dev_console_logging(logger=logger)
    _enable_dev_console_logging(logger=logger)

    handlers = [h for h in logger.handlers if isinstance(h, logging.StreamHandler)]
    assert len(handlers) == 1


@pytest.mark.parametrize(
    "level,expected",
    [
        (logging.INFO, logging.INFO),
        ("INFO", logging.INFO),
        ("WARNING", logging.WARNING),
    ],
)
def test_enable_dev_console_logging_respects_level(level, expected) -> None:
    """
    Test that ``_enable_dev_console_logging`` sets the handler level correctly.
    """
    logger = logging.getLogger(f"test_logger_{expected}")
    logger.handlers.clear()

    _enable_dev_console_logging(level=level, logger=logger)

    handler = next(h for h in logger.handlers if isinstance(h, logging.StreamHandler))
    assert handler.level == expected
