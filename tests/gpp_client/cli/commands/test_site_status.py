"""
Tests for site status CLI commands.
"""

from types import SimpleNamespace


def test_get_site_status_dispatches_correctly(
    runner,
    cli_app,
    mocker,
    dummy_async_client_factory,
) -> None:
    """
    Ensure site status get dispatches correctly.
    """
    result_model = {"site": "north", "status": "open"}

    site_status = SimpleNamespace(
        get_by_id=mocker.AsyncMock(return_value=result_model),
    )

    mocker.patch(
        "gpp_client.cli.commands.site_status.GPPClient",
        return_value=dummy_async_client_factory(site_status=site_status),
    )
    json_mock = mocker.patch("gpp_client.cli.commands.site_status.output.json")

    result = runner.invoke(cli_app, ["site-status", "get", "north"])

    assert result.exit_code == 0
    site_status.get_by_id.assert_called_once_with(site_id="north")
    json_mock.assert_called_once_with(result_model)


def test_get_site_status_accepts_south(
    runner,
    cli_app,
    mocker,
    dummy_async_client_factory,
) -> None:
    """
    Ensure site status get accepts south.
    """
    result_model = {"site": "south", "status": "closed"}

    site_status = SimpleNamespace(
        get_by_id=mocker.AsyncMock(return_value=result_model),
    )

    mocker.patch(
        "gpp_client.cli.commands.site_status.GPPClient",
        return_value=dummy_async_client_factory(site_status=site_status),
    )
    json_mock = mocker.patch("gpp_client.cli.commands.site_status.output.json")

    result = runner.invoke(cli_app, ["site-status", "get", "south"])

    assert result.exit_code == 0
    site_status.get_by_id.assert_called_once_with(site_id="south")
    json_mock.assert_called_once_with(result_model)


def test_get_site_status_rejects_invalid_site(runner, cli_app) -> None:
    """
    Ensure site status get rejects invalid site values.
    """
    result = runner.invoke(cli_app, ["site-status", "get", "weast"])  # Hehe

    assert result.exit_code != 0
    assert "Invalid value" in result.output
