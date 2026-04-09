"""
Tests for program CLI commands.
"""

from types import SimpleNamespace

import pytest


@pytest.mark.parametrize(
    ("args", "method_name", "expected_kwargs"),
    [
        (
            ["program", "get", "--program-id", "p-1"],
            "get_by_id",
            {"program_id": "p-1", "include_deleted": False},
        ),
        (
            ["program", "get", "--program-reference", "prog-ref"],
            "get_by_reference",
            {"program_reference": "prog-ref", "include_deleted": False},
        ),
        (
            ["program", "get", "--proposal-reference", "prop-ref"],
            "get_by_proposal_reference",
            {"proposal_reference": "prop-ref", "include_deleted": False},
        ),
        (
            ["program", "get", "--program-id", "p-1", "--include-deleted"],
            "get_by_id",
            {"program_id": "p-1", "include_deleted": True},
        ),
    ],
)
def test_get_program_dispatches_correctly(
    runner,
    cli_app,
    mocker,
    dummy_async_client_factory,
    args: list[str],
    method_name: str,
    expected_kwargs: dict[str, str | bool],
) -> None:
    """
    Ensure program get dispatches correctly.
    """
    result_model = {"id": "p-1"}

    program = SimpleNamespace(
        get_by_id=mocker.AsyncMock(),
        get_by_reference=mocker.AsyncMock(),
        get_by_proposal_reference=mocker.AsyncMock(),
    )
    getattr(program, method_name).return_value = result_model

    mocker.patch(
        "gpp_client.cli.commands.program.GPPClient",
        return_value=dummy_async_client_factory(program=program),
    )
    json_pydantic_mock = mocker.patch(
        "gpp_client.cli.commands.program.output.json_pydantic"
    )

    result = runner.invoke(cli_app, args)

    assert result.exit_code == 0
    getattr(program, method_name).assert_called_once_with(**expected_kwargs)
    json_pydantic_mock.assert_called_once_with(result_model)


def test_get_program_fails_with_no_selector(runner, cli_app) -> None:
    """
    Ensure program get fails with no selector.
    """
    result = runner.invoke(cli_app, ["program", "get"])

    assert result.exit_code != 0
    assert "Exactly one selector is required" in result.output


def test_get_program_fails_with_multiple_selectors(runner, cli_app) -> None:
    """
    Ensure program get fails with multiple selectors.
    """
    result = runner.invoke(
        cli_app,
        [
            "program",
            "get",
            "--program-id",
            "p-1",
            "--program-reference",
            "prog-ref",
        ],
    )

    assert result.exit_code != 0
    assert "Selectors are mutually exclusive" in result.output


def test_list_programs_dispatches_correctly(
    runner,
    cli_app,
    mocker,
    dummy_async_client_factory,
) -> None:
    """
    Ensure program list dispatches correctly.
    """
    result_model = {"items": []}

    program = SimpleNamespace(
        get_all=mocker.AsyncMock(return_value=result_model),
    )

    mocker.patch(
        "gpp_client.cli.commands.program.GPPClient",
        return_value=dummy_async_client_factory(program=program),
    )
    json_pydantic_mock = mocker.patch(
        "gpp_client.cli.commands.program.output.json_pydantic"
    )

    result = runner.invoke(
        cli_app,
        [
            "program",
            "list",
            "--include-deleted",
            "--offset",
            "abc",
            "--limit",
            "10",
        ],
    )

    assert result.exit_code == 0
    program.get_all.assert_called_once_with(
        include_deleted=True,
        offset="abc",
        limit=10,
    )
    json_pydantic_mock.assert_called_once_with(result_model)
