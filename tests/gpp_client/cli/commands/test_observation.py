"""
Tests for observation CLI commands.
"""

from types import SimpleNamespace

import pytest


@pytest.mark.parametrize(
    ("args", "method_name", "expected_kwargs"),
    [
        (
            ["observation", "get", "--observation-id", "o-1"],
            "get_by_id",
            {"observation_id": "o-1"},
        ),
        (
            ["observation", "get", "--observation-reference", "obs-ref"],
            "get_by_reference",
            {"observation_reference": "obs-ref"},
        ),
    ],
)
def test_get_observation_dispatches_correctly(
    runner,
    cli_app,
    mocker,
    dummy_async_client_factory,
    args: list[str],
    method_name: str,
    expected_kwargs: dict[str, str],
) -> None:
    """
    Ensure observation get dispatches correctly.
    """
    result_model = {"id": "o-1"}

    observation = SimpleNamespace(
        get_by_id=mocker.AsyncMock(),
        get_by_reference=mocker.AsyncMock(),
    )
    getattr(observation, method_name).return_value = result_model

    mocker.patch(
        "gpp_client.cli.commands.observation.GPPClient",
        return_value=dummy_async_client_factory(observation=observation),
    )
    json_pydantic_mock = mocker.patch(
        "gpp_client.cli.commands.observation.output.json_pydantic"
    )

    result = runner.invoke(cli_app, args)

    assert result.exit_code == 0
    getattr(observation, method_name).assert_called_once_with(**expected_kwargs)
    json_pydantic_mock.assert_called_once_with(result_model)


def test_get_observation_fails_with_no_selector(runner, cli_app) -> None:
    """
    Ensure observation get fails with no selector.
    """
    result = runner.invoke(cli_app, ["observation", "get"])

    assert result.exit_code != 0
    assert "Exactly one selector is required" in result.output


def test_get_observation_fails_with_multiple_selectors(runner, cli_app) -> None:
    """
    Ensure observation get fails with multiple selectors.
    """
    result = runner.invoke(
        cli_app,
        [
            "observation",
            "get",
            "--observation-id",
            "o-1",
            "--observation-reference",
            "obs-ref",
        ],
    )

    assert result.exit_code != 0
    assert "Selectors are mutually exclusive" in result.output


def test_list_observations_dispatches_correctly(
    runner,
    cli_app,
    mocker,
    dummy_async_client_factory,
) -> None:
    """
    Ensure observation list dispatches correctly.
    """
    result_model = {"items": []}

    observation = SimpleNamespace(
        get_all=mocker.AsyncMock(return_value=result_model),
    )

    mocker.patch(
        "gpp_client.cli.commands.observation.GPPClient",
        return_value=dummy_async_client_factory(observation=observation),
    )
    json_pydantic_mock = mocker.patch(
        "gpp_client.cli.commands.observation.output.json_pydantic"
    )

    result = runner.invoke(
        cli_app,
        [
            "observation",
            "list",
            "--include-deleted",
            "--offset",
            "abc",
            "--limit",
            "10",
        ],
    )

    assert result.exit_code == 0
    observation.get_all.assert_called_once_with(
        include_deleted=True,
        offset="abc",
        limit=10,
    )
    json_pydantic_mock.assert_called_once_with(result_model)
