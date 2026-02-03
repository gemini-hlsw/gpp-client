import json
from pathlib import Path

import pytest  # type: ignore[import]
from pydantic import BaseModel

from gpp_client.exceptions import GPPClientError, GPPValidationError
from gpp_client.managers.base import BaseManager


class DummyProps(BaseModel):
    """
    Dummy properties class for testing load_properties.
    """

    a: int
    b: str


@pytest.fixture
def manager(dummy_client) -> BaseManager:
    """
    Fixture that provides a BaseManager instance with a dummy client.
    """
    return BaseManager(dummy_client)


@pytest.mark.parametrize("include_traceback", [True, False])
def test_raise_error(manager: BaseManager, include_traceback: bool) -> None:
    """
    Test that raise_error includes class name context in the error message.
    """
    exc = ValueError("bad")
    with pytest.raises(GPPClientError) as e:
        manager.raise_error(GPPClientError, exc, include_traceback=include_traceback)

    # Ensure the message includes the class name context.
    assert "BaseManager" in str(e.value)


@pytest.mark.parametrize(
    "kwargs,should_raise",
    [
        ({"a": "x", "b": None}, False),
        ({"a": None, "b": "y"}, False),
        ({"a": None, "b": None}, True),
        ({"a": "x", "b": "y"}, True),
    ],
)
def test_validate_single_identifier(
    manager: BaseManager, kwargs: dict[str, str | None], should_raise: bool
) -> None:
    """
    Test validate_single_identifier with various input combinations.
    """
    if should_raise:
        with pytest.raises(GPPValidationError):
            manager.validate_single_identifier(**kwargs)
    else:
        manager.validate_single_identifier(**kwargs)


@pytest.mark.parametrize(
    "result,operation_name,expected",
    [
        ({"foo": {"x": 1}}, None, {"x": 1}),
        ({"foo": {"x": 1}}, "foo", {"x": 1}),
    ],
)
def test_get_result_success(
    manager: BaseManager,
    result: dict[str, dict[str, int]],
    operation_name: str | None,
    expected: dict[str, int],
) -> None:
    """
    Test get_result with successful cases.
    """
    assert manager.get_result(result, operation_name) == expected


@pytest.mark.parametrize(
    "result,operation_name,exc",
    [
        (None, None, GPPClientError),
        ({}, None, GPPClientError),
        ({"a": {}, "b": {}}, None, GPPClientError),
        ({"a": {}}, "x", GPPClientError),
    ],
)
def test_get_result_failure(
    manager: BaseManager,
    result: dict[str, dict[str, int]] | None,
    operation_name: str | None,
    exc: type[Exception],
) -> None:
    """
    Test get_result with failure cases.
    """
    with pytest.raises(exc):
        manager.get_result(result, operation_name)


@pytest.mark.parametrize(
    "payload,key,expected",
    [
        ({"items": [{"a": 1}]}, "items", {"a": 1}),
    ],
)
def test_get_single_result_success(
    manager: BaseManager,
    payload: dict[str, list[dict[str, int]]],
    key: str,
    expected: dict[str, int],
) -> None:
    """
    Test get_single_result with successful cases.
    """
    assert manager.get_single_result(payload, key) == expected


@pytest.mark.parametrize(
    "payload,key,exc",
    [
        ({}, "items", GPPClientError),
        ({"items": None}, "items", GPPClientError),
        ({"items": []}, "items", GPPClientError),
        ({"items": [{"a": 1}, {"b": 2}]}, "items", GPPClientError),
    ],
)
def test_get_single_result_failure(
    manager: BaseManager,
    payload: dict[str, object],
    key: str,
    exc: type[Exception],
) -> None:
    """
    Test get_single_result with failure cases.
    """
    with pytest.raises(exc):
        manager.get_single_result(payload, key)


def test_load_properties_from_dict(manager: BaseManager) -> None:
    """
    Test load_properties with a dictionary input.
    """
    result = manager.load_properties(
        properties=None,
        from_json={"a": 1, "b": "z"},
        cls=DummyProps,
    )

    assert isinstance(result, DummyProps)
    assert result.a == 1
    assert result.b == "z"


def test_load_properties_from_file(tmp_path: Path, manager: BaseManager) -> None:
    """
    Test load_properties with a file input.
    """
    path = tmp_path / "props.json"
    path.write_text(json.dumps({"a": 3, "b": "ok"}))

    result = manager.load_properties(
        properties=None,
        from_json=path,
        cls=DummyProps,
    )

    assert isinstance(result, DummyProps)
    assert result.a == 3
    assert result.b == "ok"


@pytest.mark.parametrize(
    "from_json,exc",
    [
        ("missing.json", GPPValidationError),
        ({"a": "not-int", "b": "x"}, GPPValidationError),
    ],
)
def test_load_properties_invalid(
    manager: BaseManager,
    from_json: str | dict[str, object],
    exc: type[Exception],
) -> None:
    """
    Test load_properties with invalid inputs.
    """
    with pytest.raises(exc):
        manager.load_properties(
            properties=None,
            from_json=from_json,
            cls=DummyProps,
        )


def test_load_properties_mutual_exclusion(manager: BaseManager) -> None:
    """
    Test that load_properties raises an error when both properties and from_json are
    provided.
    """
    props = DummyProps(a=1, b="x")
    with pytest.raises(GPPValidationError):
        manager.load_properties(properties=props, from_json={"a": 2}, cls=DummyProps)


def test_load_properties_passthrough(manager: BaseManager) -> None:
    """
    Test load_properties when properties are passed directly.
    """
    props = DummyProps(a=9, b="nine")
    result = manager.load_properties(
        properties=props,
        from_json=None,
        cls=DummyProps,
    )

    assert result is props
    assert result.a == 9
    assert result.b == "nine"
