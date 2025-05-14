import nox

nox.options.sessions = ["tests"]

PYTHON_VERSIONS = ["3.10", "3.11", "3.12", "3.13"]


def run_pytest(session, *, remote: bool = False, coverage: bool = False) -> None:
    """Helper to install and run pytest with optional flags."""
    session.install("-e", ".[test]")

    args = ["-r", "A", "-v", "-n", "auto"]

    if remote:
        args.append("--remote-data")

    if coverage and session.python == "3.10":
        args += [
            "--cov=gpp_client",
            "--cov=tests",
            "--cov-report=xml",
            "--cov-branch",
        ]

    session.run("pytest", *args)


@nox.session(venv_backend="conda", python=PYTHON_VERSIONS)
def tests(session):
    """Run the test suite."""
    run_pytest(session)


@nox.session(venv_backend="conda", python=PYTHON_VERSIONS)
def remote(session):
    """Run the '--remote-data' test suite."""
    run_pytest(session, remote=True)


@nox.session(python=PYTHON_VERSIONS)
def github_tests(session):
    """Run GitHub CI test suite with coverage (only in 3.10)."""
    run_pytest(session, coverage=True)


@nox.session(python=["3.10"])
def github_lint(session):
    """Run GitHub CI linting."""
    session.install("ruff")
    session.run("ruff", "check")
