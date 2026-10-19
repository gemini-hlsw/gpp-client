"""
Tests for the atom domain.
"""

import pytest
from aiohttp import web

from tests.gpp_client.domains.test_scheduler_environments import _serve


@pytest.mark.asyncio
async def test_get_digests_posts_ids_and_returns_tsv(gpp_client) -> None:
    """
    Ensure get_digests posts one observation ID per line and returns the TSV.
    """
    received: list[str] = []

    async def handler(request: web.Request) -> web.Response:
        received.append(f"{request.method} {request.path} {await request.text()}")
        return web.Response(text="o-1\tdigest\n")

    runner, url = await _serve(handler)
    try:
        gpp_client.rest.base_url = url
        result = await gpp_client.atom.get_digests(
            observation_ids=["o-1", "o-2"], accept_gzip=False
        )
    finally:
        await runner.cleanup()

    assert result == "o-1\tdigest\n"
    assert received == ["POST /scheduler/atoms o-1\no-2"]
