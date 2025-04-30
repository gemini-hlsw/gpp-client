from gpp_client.cli.cli import app


class TestCLI:
    def test_help(self, cli_runner):
        result = cli_runner.invoke(app, ["--help"])
        assert result.exit_code == 0
        assert "program-note" in result.stdout
        assert "call-for-proposals" in result.stdout
        assert "program" in result.stdout
        assert "config" in result.stdout
