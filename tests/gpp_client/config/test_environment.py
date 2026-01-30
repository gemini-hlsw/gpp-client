import pytest

from gpp_client.config import GPPEnvironment


class TestGPPEnvironment:
    """
    Tests for the GPPEnvironment Enum.
    """

    def test_environment_values(self):
        """
        Test that GPPEnvironment has the correct values.
        """
        assert GPPEnvironment.DEVELOPMENT == "DEVELOPMENT"
        assert GPPEnvironment.STAGING == "STAGING"
        assert GPPEnvironment.PRODUCTION == "PRODUCTION"

    def test_environment_membership(self):
        """
        Test that the enum contains the expected members.
        """
        assert "DEVELOPMENT" in GPPEnvironment.__members__
        assert "STAGING" in GPPEnvironment.__members__
        assert "PRODUCTION" in GPPEnvironment.__members__

    def test_environment_iteration(self):
        """
        Test that all enum members can be iterated over.
        """
        environments = list(GPPEnvironment)
        assert environments == [
            GPPEnvironment.DEVELOPMENT,
            GPPEnvironment.STAGING,
            GPPEnvironment.PRODUCTION,
        ]

    def test_missing_case_insensitive_match(self):
        """
        Test that _missing_ handles case-insensitive matches correctly.
        """
        assert GPPEnvironment("development") == GPPEnvironment.DEVELOPMENT
        assert GPPEnvironment("staging") == GPPEnvironment.STAGING
        assert GPPEnvironment("production") == GPPEnvironment.PRODUCTION
        assert GPPEnvironment("DeVeLoPmEnT") == GPPEnvironment.DEVELOPMENT

    def test_missing_invalid_value(self):
        """
        Test that _missing_ returns None for invalid values.
        """
        assert GPPEnvironment._missing_("invalid") is None
        assert GPPEnvironment._missing_(123) is None
        assert GPPEnvironment._missing_(None) is None

    def test_invalid_enum_value_raises_value_error(self):
        """
        Test that invalid enum construction raises ValueError.
        """
        with pytest.raises(ValueError):
            GPPEnvironment("invalid")

    def test_missing_does_not_strip_whitespace(self):
        """
        Test that leading/trailing whitespace is not accepted.
        """
        with pytest.raises(ValueError):
            GPPEnvironment(" development ")

    def test_non_string_enum_construction(self):
        """
        Test non-string inputs raise ValueError.
        """
        with pytest.raises(ValueError):
            GPPEnvironment(123)
