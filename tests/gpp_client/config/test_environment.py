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
