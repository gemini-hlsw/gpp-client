import asyncio

import pytest
from gpp_client import GPPClient

# First check if the connection works before trying GPP queries.
@pytest.fixture(scope="session", autouse=True)
def check_connection(pytestconfig):
    # "remote_data" doesn't return `None` it return "none".
    if pytestconfig.getoption("remote_data") == "none":
        return

    client = GPPClient()
    ok, error = asyncio.get_event_loop().run_until_complete(client.check_connection())

    if not ok:
        pytest.exit(f"[remote-data] Remote connection failed: {error}", returncode=1)
