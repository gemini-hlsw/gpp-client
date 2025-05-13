import nox

nox.options.sessions = ["tests"]


@nox.session(venv_backend="conda", python=["3.10", "3.11", "3.12", "3.13"])
def tests(session):
    """Run the test suite."""
    session.install("-e", ".[test]")
    session.run("pytest")


@nox.session(venv_backend="conda", python=["3.10", "3.11", "3.12", "3.13"])
def remote(session):
    """Run the '--remote-data' test suite."""
    session.install("-e", ".[test]")
    session.run("pytest", "--remote-data")
