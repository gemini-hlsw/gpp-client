"""
Tests for the release validation script.
"""

import pytest

from scripts.validate_release import ReleaseValidationError, main, validate_release


@pytest.mark.parametrize("tag", ["v26.5.0", "v26.12.3", "v27.1.10"])
def test_accepts_a_calver_release_tag(tag: str) -> None:
    validate_release(tag)


@pytest.mark.parametrize("tag", ["v26.5.0.dev1", "v26.10.4.dev3"])
def test_refuses_a_pre_release_tag(tag: str) -> None:
    with pytest.raises(ReleaseValidationError) as raised:
        validate_release(tag)

    assert str(raised.value) == (
        f"Pre-release tag refused: {tag}. gpp-client releases in one stream "
        "that reaches every environment, so there are no .devN releases. "
        "Use a release tag such as v26.5.0."
    )


@pytest.mark.parametrize(
    "tag", ["26.5.0", "v26.13.0", "v26.0.1", "v26.5", "v26.5.0.1", "v26.5.0rc1"]
)
def test_refuses_a_tag_that_is_not_calver(tag: str) -> None:
    with pytest.raises(ReleaseValidationError, match="Invalid release tag"):
        validate_release(tag)


def test_main_exits_with_usage_when_tag_is_missing(mocker) -> None:
    mocker.patch("sys.argv", ["validate_release.py"])

    with pytest.raises(SystemExit, match="Usage"):
        main()


def test_main_exits_with_error_for_a_refused_tag(mocker, capsys) -> None:
    mocker.patch("sys.argv", ["validate_release.py", "v26.5.0.dev1"])

    with pytest.raises(SystemExit) as exit_info:
        main()

    assert exit_info.value.code == 1
    assert "Pre-release tag refused" in capsys.readouterr().err
