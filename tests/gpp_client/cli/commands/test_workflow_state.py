"""
Tests for workflow state CLI commands.
"""

from types import SimpleNamespace

import pytest


@pytest.mark.parametrize(
    ("args", "method_name", "expected_kwargs"),
    [
        (
            ["workflow-state", "get", "--observation-id", "o-1"],
            "get_by_id",
            {"observation_id": "o-1"},
        ),
        (
            ["workflow-state", "get", "--observation-reference", "obs-ref"],
            "get_by_reference",
            {"observation_reference": "obs-ref"},
        ),
    ],
)
def test_get_workflow_state_dispatches_correctly(
    runner,
    cli_app,
    mocker,
    dummy_async_client_factory,
    args: list[str],
    method_name: str,
    expected_kwargs: dict[str, str],
) -> None:
    """
    Ensure workflow state get dispatches correctly.
    """
    result_model = {"state": "READY"}

    workflow_state = SimpleNamespace(
        get_by_id=mocker.AsyncMock(),
        get_by_reference=mocker.AsyncMock(),
    )
    getattr(workflow_state, method_name).return_value = result_model

    mocker.patch(
        "gpp_client.cli.commands.workflow_state.GPPClient",
        return_value=dummy_async_client_factory(workflow_state=workflow_state),
    )
    json_pydantic_mock = mocker.patch(
        "gpp_client.cli.commands.workflow_state.output.json_pydantic"
    )

    result = runner.invoke(cli_app, args)

    assert result.exit_code == 0
    getattr(workflow_state, method_name).assert_called_once_with(**expected_kwargs)
    json_pydantic_mock.assert_called_once_with(result_model)


def test_get_workflow_state_fails_with_no_selector(runner, cli_app) -> None:
    """
    Ensure workflow state get fails with no selector.
    """
    result = runner.invoke(cli_app, ["workflow-state", "get"])

    assert result.exit_code != 0
    assert "Exactly one selector is required" in result.output


def test_get_workflow_state_fails_with_multiple_selectors(runner, cli_app) -> None:
    """
    Ensure workflow state get fails with multiple selectors.
    """
    result = runner.invoke(
        cli_app,
        [
            "workflow-state",
            "get",
            "--observation-id",
            "o-1",
            "--observation-reference",
            "obs-ref",
        ],
    )

    assert result.exit_code != 0
    assert "Selectors are mutually exclusive" in result.output
