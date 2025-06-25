from gpp_client.cli.cli import app


class TestCLI:
    def test_help(self, cli_runner):
        """Verify the help screen is shown for adding help flag."""
        result = cli_runner.invoke(app, ["--help"])
        assert result.exit_code == 0
        assert "pnote" in result.stdout
        assert "cfp" in result.stdout
        assert "program" in result.stdout
        assert "config" in result.stdout
        assert "target" in result.stdout
        assert "site" in result.stdout
