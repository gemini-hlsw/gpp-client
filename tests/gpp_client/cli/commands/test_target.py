"""
Tests for target CLI commands.
"""

from types import SimpleNamespace


def test_get_target_dispatches_correctly(
    runner,
    cli_app,
    mocker,
    dummy_async_client_factory,
) -> None:
    """Ensure target get dispatches correctly."""
    result_model = {"id": "t-1"}

    target = SimpleNamespace(
        get_by_id=mocker.AsyncMock(return_value=result_model),
    )

    mocker.patch(
        "gpp_client.cli.commands.target.GPPClient",
        return_value=dummy_async_client_factory(target=target),
    )
    json_pydantic_mock = mocker.patch(
        "gpp_client.cli.commands.target.output.json_pydantic"
    )

    result = runner.invoke(cli_app, ["target", "get", "--target-id", "t-1"])

    assert result.exit_code == 0
    target.get_by_id.assert_called_once_with(
        target_id="t-1",
        include_deleted=False,
    )
    json_pydantic_mock.assert_called_once_with(result_model)


def test_get_target_dispatches_with_include_deleted(
    runner,
    cli_app,
    mocker,
    dummy_async_client_factory,
) -> None:
    """
    Ensure target get passes include_deleted when requested.
    """
    result_model = {"id": "t-1"}

    target = SimpleNamespace(
        get_by_id=mocker.AsyncMock(return_value=result_model),
    )

    mocker.patch(
        "gpp_client.cli.commands.target.GPPClient",
        return_value=dummy_async_client_factory(target=target),
    )
    json_pydantic_mock = mocker.patch(
        "gpp_client.cli.commands.target.output.json_pydantic"
    )

    result = runner.invoke(
        cli_app,
        ["target", "get", "--target-id", "t-1", "--include-deleted"],
    )

    assert result.exit_code == 0
    target.get_by_id.assert_called_once_with(
        target_id="t-1",
        include_deleted=True,
    )
    json_pydantic_mock.assert_called_once_with(result_model)


def test_get_target_fails_with_no_selector(runner, cli_app) -> None:
    """
    Ensure target get fails with no selector.
    """
    result = runner.invoke(cli_app, ["target", "get"])

    assert result.exit_code != 0
    assert "Exactly one selector is required" in result.output


def test_list_targets_dispatches_correctly(
    runner,
    cli_app,
    mocker,
    dummy_async_client_factory,
) -> None:
    """
    Ensure target list dispatches correctly.
    """
    result_model = {"items": []}

    target = SimpleNamespace(
        get_all=mocker.AsyncMock(return_value=result_model),
    )

    mocker.patch(
        "gpp_client.cli.commands.target.GPPClient",
        return_value=dummy_async_client_factory(target=target),
    )
    json_pydantic_mock = mocker.patch(
        "gpp_client.cli.commands.target.output.json_pydantic"
    )

    result = runner.invoke(
        cli_app,
        [
            "target",
            "list",
            "--include-deleted",
            "--offset",
            "abc",
            "--limit",
            "10",
        ],
    )

    assert result.exit_code == 0
    target.get_all.assert_called_once_with(
        include_deleted=True,
        offset="abc",
        limit=10,
    )
    json_pydantic_mock.assert_called_once_with(result_model)
