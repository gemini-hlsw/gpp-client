"""
Tests for GOATS CLI commands.
"""

from types import SimpleNamespace


def test_list_goats_programs(
    runner, cli_app, mocker, dummy_async_client_factory
) -> None:
    """
    Ensure GOATS program listing dispatches correctly.
    """
    result_model = {"items": ["program"]}

    goats = SimpleNamespace(
        get_programs=mocker.AsyncMock(return_value=result_model),
    )

    mocker.patch(
        "gpp_client.cli.commands.goats.GPPClient",
        return_value=dummy_async_client_factory(goats=goats),
    )
    json_pydantic_mock = mocker.patch(
        "gpp_client.cli.commands.goats.output.json_pydantic"
    )

    result = runner.invoke(cli_app, ["goats", "list-programs"])

    assert result.exit_code == 0
    goats.get_programs.assert_called_once_with()
    json_pydantic_mock.assert_called_once_with(result_model)


def test_list_goats_observations(
    runner, cli_app, mocker, dummy_async_client_factory
) -> None:
    """
    Ensure GOATS observation listing dispatches correctly.
    """
    result_model = {"items": ["observation"]}

    goats = SimpleNamespace(
        get_observations_by_program_id=mocker.AsyncMock(return_value=result_model),
    )

    mocker.patch(
        "gpp_client.cli.commands.goats.GPPClient",
        return_value=dummy_async_client_factory(goats=goats),
    )
    json_pydantic_mock = mocker.patch(
        "gpp_client.cli.commands.goats.output.json_pydantic"
    )

    result = runner.invoke(cli_app, ["goats", "list-observations", "p-1"])

    assert result.exit_code == 0
    goats.get_observations_by_program_id.assert_called_once_with(program_id="p-1")
    json_pydantic_mock.assert_called_once_with(result_model)
