"""
Tests for scheduler CLI commands.
"""

from types import SimpleNamespace


def test_list_scheduler_programs_without_filters(
    runner,
    cli_app,
    mocker,
    dummy_async_client_factory,
) -> None:
    """
    Ensure scheduler program listing works without filters.
    """
    result_model = {"items": ["program"]}

    scheduler = SimpleNamespace(
        get_programs=mocker.AsyncMock(return_value=result_model),
    )

    mocker.patch(
        "gpp_client.cli.commands.scheduler.GPPClient",
        return_value=dummy_async_client_factory(scheduler=scheduler),
    )
    json_pydantic_mock = mocker.patch(
        "gpp_client.cli.commands.scheduler.output.json_pydantic"
    )

    result = runner.invoke(cli_app, ["scheduler", "list-programs"])

    assert result.exit_code == 0
    scheduler.get_programs.assert_called_once_with(programs_list=None)
    json_pydantic_mock.assert_called_once_with(result_model)


def test_list_scheduler_programs_with_filters(
    runner,
    cli_app,
    mocker,
    dummy_async_client_factory,
) -> None:
    """
    Ensure scheduler program listing passes repeated program IDs.
    """
    result_model = {"items": ["program"]}

    scheduler = SimpleNamespace(
        get_programs=mocker.AsyncMock(return_value=result_model),
    )

    mocker.patch(
        "gpp_client.cli.commands.scheduler.GPPClient",
        return_value=dummy_async_client_factory(scheduler=scheduler),
    )
    json_pydantic_mock = mocker.patch(
        "gpp_client.cli.commands.scheduler.output.json_pydantic"
    )

    result = runner.invoke(
        cli_app,
        [
            "scheduler",
            "list-programs",
            "--program-id",
            "p-1",
            "--program-id",
            "p-2",
        ],
    )

    assert result.exit_code == 0
    scheduler.get_programs.assert_called_once_with(programs_list=["p-1", "p-2"])
    json_pydantic_mock.assert_called_once_with(result_model)


def test_list_scheduler_program_ids(
    runner,
    cli_app,
    mocker,
    dummy_async_client_factory,
) -> None:
    """
    Ensure scheduler program ID listing dispatches correctly.
    """
    result_model = {"items": ["p-1", "p-2"]}

    scheduler = SimpleNamespace(
        get_program_ids=mocker.AsyncMock(return_value=result_model),
    )

    mocker.patch(
        "gpp_client.cli.commands.scheduler.GPPClient",
        return_value=dummy_async_client_factory(scheduler=scheduler),
    )
    json_pydantic_mock = mocker.patch(
        "gpp_client.cli.commands.scheduler.output.json_pydantic"
    )

    result = runner.invoke(cli_app, ["scheduler", "list-program-ids"])

    assert result.exit_code == 0
    scheduler.get_program_ids.assert_called_once_with()
    json_pydantic_mock.assert_called_once_with(result_model)
