from enum import Enum
from types import SimpleNamespace

import pytest
from rich.console import Console
from rich.table import Table

from gpp_client.cli import output


@pytest.fixture()
def consoles(mocker):
    """
    Mock both console and error_console for all tests.
    """
    mock_console = mocker.patch("gpp_client.cli.output.console")
    mock_error_console = mocker.patch("gpp_client.cli.output.error_console")
    return mock_console, mock_error_console


@pytest.fixture()
def recorded_console(mocker) -> Console:
    """
    Patch the CLI output console with a recording Rich console.
    """
    test_console = Console(record=True)
    mocker.patch.object(output, "console", test_console)
    return test_console


@pytest.fixture()
def recorded_error_console(mocker) -> Console:
    """
    Patch the CLI error console with a recording Rich console.
    """
    test_console = Console(stderr=True, record=True)
    mocker.patch.object(output, "error_console", test_console)
    return test_console


@pytest.mark.parametrize(
    "func, expected",
    [
        (output.success, f"{output.ICON_SUCCESS} hello"),
        (output.warning, f"{output.ICON_WARNING} hello"),
        (output.fail, f"{output.ICON_ERROR} hello"),
        (output.info, "hello"),
        (output.procedure, f"{output.ICON_PROCEDURE} hello"),
    ],
)
def test_basic_output_functions(consoles, func, expected):
    """Ensure basic output helpers call the correct console with the expected markup."""
    mock_console, mock_error = consoles

    func("hello")

    if func is output.fail:
        mock_error.print.assert_called_once_with(expected)
        mock_console.print.assert_not_called()
    elif func is output.info:
        mock_console.print.assert_any_call("hello", style="white")
    else:
        mock_console.print.assert_any_call(expected)


def test_space(consoles):
    """Verify space() prints a blank line."""
    mock_console, _ = consoles
    output.space()
    mock_console.print.assert_called_once_with("")


def test_section(consoles):
    """Verify section() prints a rule before and after spacing."""
    mock_console, _ = consoles
    output.section("TITLE")
    assert mock_console.rule.call_count == 1
    assert mock_console.print.call_count == 2


def test_dim_info(consoles):
    """Ensure dim_info uses dim style."""
    mock_console, _ = consoles
    output.dim_info("msg")
    mock_console.print.assert_called_once()


def test_panel(consoles):
    """Verify panel() wraps content and prints exactly once."""
    mock_console, _ = consoles
    output.panel("hello", title="Test")
    assert mock_console.print.call_count == 1


def test_info_table(consoles):
    """Verify info_table() prints a padded table."""
    mock_console, _ = consoles
    output.info_table({"A": "1"})
    assert mock_console.print.call_count == 1


def test_procedure_steps(consoles):
    """Ensure procedure_steps prints all steps with bullet prefixes."""
    mock_console, _ = consoles
    output.procedure_steps(["x", "y", "z"])
    assert mock_console.print.call_count == 3
    calls = [str(call.args[0]) for call in mock_console.print.call_args_list]
    assert all(output.ICON_BULLET in c for c in calls)


def test_confirm_prompt(mocker):
    """Ensure confirm_prompt invokes Confirm.ask with markup."""
    mock_confirm = mocker.patch("gpp_client.cli.output.Confirm.ask", return_value=True)
    assert output.confirm_prompt("Proceed?") is True
    mock_confirm.assert_called_once()


def test_print_exception(consoles):
    """Verify print_exception sends output to error_console."""
    _, mock_error = consoles
    output.print_exception()
    mock_error.print_exception.assert_called_once()


def test_status_context_manager(mocker):
    """Ensure status() yields the inner Rich status object."""
    mock_console = mocker.patch("gpp_client.cli.output.console")
    fake_status = mocker.MagicMock()
    mock_console.status.return_value.__enter__.return_value = fake_status

    with output.status("Working...") as s:
        assert s is fake_status

    mock_console.status.assert_called_once()


class DummyState(Enum):
    """
    Dummy enum for testing cell formatting.
    """

    READY = "READY"
    INACTIVE = "INACTIVE"


def test_table_column_defaults() -> None:
    """
    Ensure TableColumn uses the expected default values.
    """
    column = output.TableColumn(
        header="ID",
        path="id",
    )

    assert column.header == "ID"
    assert column.path == "id"
    assert column.default == "-"
    assert column.no_wrap is False
    assert column.style is None


@pytest.mark.parametrize(
    ("item", "path", "expected"),
    [
        (
            SimpleNamespace(
                program=SimpleNamespace(
                    id="p-123",
                )
            ),
            "program.id",
            "p-123",
        ),
        (
            SimpleNamespace(
                program=SimpleNamespace(
                    id="p-123",
                )
            ),
            "program.reference",
            None,
        ),
        (
            SimpleNamespace(
                program=None,
            ),
            "program.id",
            None,
        ),
    ],
)
def test_resolve_attr_path(
    item: SimpleNamespace,
    path: str,
    expected: object,
) -> None:
    """
    Ensure _resolve_attr_path correctly resolves nested paths.
    """
    result = output._resolve_attr_path(item, path)

    assert result == expected


@pytest.mark.parametrize(
    ("value", "expected"),
    [
        (None, "-"),
        ("abc", "abc"),
        (123, "123"),
        (True, "yes"),
        (False, "no"),
        (DummyState.READY, "READY"),
        (["a", "b"], "a, b"),
        ((1, 2), "1, 2"),
        ({"x", "y"}, "x, y"),
    ],
)
def test_format_cell_returns_expected_string(
    value: object,
    expected: str,
) -> None:
    """
    Ensure _format_cell converts supported values into display strings.
    """
    result = output._format_cell(value)

    if isinstance(value, set):
        assert set(result.split(", ")) == set(expected.split(", "))
    else:
        assert result == expected


def test_format_cell_uses_custom_default_for_none() -> None:
    """
    Ensure _format_cell uses the provided default for None values.
    """
    result = output._format_cell(None, default="N/A")

    assert result == "N/A"


def test_model_table_prints_empty_message_when_no_items(
    recorded_console: Console,
) -> None:
    """
    Ensure model_table prints the empty message when there are no items.
    """
    output.model_table(
        items=[],
        columns=[
            output.TableColumn(header="ID", path="id"),
        ],
        empty_message="Nothing here.",
    )

    rendered = recorded_console.export_text()
    assert "Nothing here." in rendered


def test_model_table_renders_table(mocker) -> None:
    """
    Ensure model_table builds and prints a Rich Table for populated items.
    """
    print_mock = mocker.patch("gpp_client.cli.output.console.print")

    items = [
        SimpleNamespace(
            id="o-1",
            title="Observation 1",
            reference=None,
            program=SimpleNamespace(id="p-1"),
            workflow=SimpleNamespace(
                value=SimpleNamespace(state=DummyState.INACTIVE),
            ),
        )
    ]
    columns = [
        output.TableColumn(header="ID", path="id", no_wrap=True, style="cyan"),
        output.TableColumn(header="Title", path="title"),
        output.TableColumn(header="Reference", path="reference"),
        output.TableColumn(header="Program ID", path="program.id"),
        output.TableColumn(header="Workflow", path="workflow.value.state"),
    ]

    output.model_table(
        items=items,
        columns=columns,
        title="Observations",
    )

    print_mock.assert_called_once()
    table = print_mock.call_args.args[0]

    assert isinstance(table, Table)
    assert table.title == "Observations"
    assert len(table.columns) == 5
    assert [column.header for column in table.columns] == [
        "ID",
        "Title",
        "Reference",
        "Program ID",
        "Workflow",
    ]


def test_model_table_formats_nested_values_and_defaults(
    recorded_console: Console,
) -> None:
    """
    Ensure model_table resolves nested values and applies defaults.
    """
    items = [
        SimpleNamespace(
            id="o-1",
            title="Observation 1",
            reference=None,
            program=SimpleNamespace(id="p-1"),
            workflow=SimpleNamespace(
                value=SimpleNamespace(state=DummyState.READY),
            ),
        )
    ]
    columns = [
        output.TableColumn(header="ID", path="id"),
        output.TableColumn(header="Reference", path="reference", default="N/A"),
        output.TableColumn(header="Program ID", path="program.id"),
        output.TableColumn(header="Workflow", path="workflow.value.state"),
    ]

    output.model_table(items=items, columns=columns)

    rendered = recorded_console.export_text()

    assert "o-1" in rendered
    assert "N/A" in rendered
    assert "p-1" in rendered
    assert "READY" in rendered


def test_model_table_formats_list_values(
    recorded_console: Console,
) -> None:
    """
    Ensure model_table formats list values into a comma-separated string.
    """
    items = [
        SimpleNamespace(
            tags=["one", "two", "three"],
        )
    ]
    columns = [
        output.TableColumn(
            header="Tags",
            path="tags",
        ),
    ]

    output.model_table(items=items, columns=columns)

    rendered = recorded_console.export_text()
    assert "one, two, three" in rendered
