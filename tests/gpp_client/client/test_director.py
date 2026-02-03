"""
Module containing tests for the director class.
"""

from gpp_client.client import GPPClient
from gpp_client.director import GPPDirector  # adjust import


def test_init_directors_wires_scheduler_and_goats(mocker) -> None:
    """
    Test that the ``_init_directors`` method correctly initializes the scheduler and
    goats directors.
    """
    client = mocker.MagicMock(spec=GPPClient)

    scheduler = mocker.patch(
        "gpp_client.director.SchedulerDirector",
        autospec=True,
    )
    goats = mocker.patch(
        "gpp_client.director.GOATSDirector",
        autospec=True,
    )

    director = GPPDirector(client)

    scheduler.assert_called_once_with(client)
    goats.assert_called_once_with(client)

    assert director.scheduler is scheduler.return_value
    assert director.goats is goats.return_value
