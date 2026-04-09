"""
Tests for attachment CLI commands.
"""

from types import SimpleNamespace

import pytest


@pytest.mark.parametrize(
    ("args", "method_name", "expected_kwargs"),
    [
        (
            ["attachment", "list", "--observation-id", "o-1"],
            "get_all_by_observation_id",
            {"observation_id": "o-1"},
        ),
        (
            ["attachment", "list", "--observation-reference", "obs-ref"],
            "get_all_by_observation_reference",
            {"observation_reference": "obs-ref"},
        ),
        (
            ["attachment", "list", "--program-id", "p-1"],
            "get_all_by_program_id",
            {"program_id": "p-1"},
        ),
        (
            ["attachment", "list", "--program-reference", "prog-ref"],
            "get_all_by_program_reference",
            {"program_reference": "prog-ref"},
        ),
        (
            ["attachment", "list", "--proposal-reference", "prop-ref"],
            "get_all_by_proposal_reference",
            {"proposal_reference": "prop-ref"},
        ),
    ],
)
def test_list_attachments_dispatches_to_correct_method(
    runner,
    cli_app,
    mocker,
    dummy_async_client_factory,
    args: list[str],
    method_name: str,
    expected_kwargs: dict[str, str],
) -> None:
    """
    Ensure each selector dispatches to the correct client method and outputs
    the returned result.
    """
    result_model = {"items": ["fake"]}

    attachment = SimpleNamespace(
        get_all_by_observation_id=mocker.AsyncMock(),
        get_all_by_observation_reference=mocker.AsyncMock(),
        get_all_by_program_id=mocker.AsyncMock(),
        get_all_by_program_reference=mocker.AsyncMock(),
        get_all_by_proposal_reference=mocker.AsyncMock(),
    )
    getattr(attachment, method_name).return_value = result_model

    mocker.patch(
        "gpp_client.cli.commands.attachment.GPPClient",
        return_value=dummy_async_client_factory(attachment=attachment),
    )
    json_pydantic_mock = mocker.patch(
        "gpp_client.cli.commands.attachment.output.json_pydantic"
    )

    result = runner.invoke(cli_app, args)

    assert result.exit_code == 0
    getattr(attachment, method_name).assert_called_once_with(**expected_kwargs)
    json_pydantic_mock.assert_called_once_with(result_model)


def test_list_attachments_fails_with_no_selector(runner, cli_app) -> None:
    """
    Ensure the command fails when no selector is provided.
    """
    result = runner.invoke(cli_app, ["attachment", "list"])

    assert result.exit_code != 0
    assert "Exactly one selector is required" in result.output


def test_list_attachments_fails_with_multiple_selectors(runner, cli_app) -> None:
    """
    Ensure the command fails when multiple selectors are provided.
    """
    result = runner.invoke(
        cli_app,
        [
            "attachment",
            "list",
            "--observation-id",
            "o-1",
            "--program-id",
            "p-1",
        ],
    )

    assert result.exit_code != 0
    assert "Selectors are mutually exclusive" in result.output
