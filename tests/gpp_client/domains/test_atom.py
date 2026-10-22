"""
Tests for the atom domain.
"""

import pytest

from gpp_client.domains.atom import AtomDomain
from gpp_client.rest.client import RESTClient


@pytest.mark.asyncio
async def test_get_digests_calls_rest_atom_digests(mocker, graphql, settings) -> None:
    # A spec'd mock fails on a misspelled REST method, a bare Mock does not.
    rest = mocker.create_autospec(RESTClient, instance=True)
    rest.get_atom_digests.return_value = "o-1\tdigest\n"
    domain = AtomDomain(graphql=graphql, rest=rest, settings=settings)

    result = await domain.get_digests(observation_ids=["o-1"], accept_gzip=False)

    assert result == "o-1\tdigest\n"
    rest.get_atom_digests.assert_awaited_once_with(
        observation_ids=["o-1"], accept_gzip=False
    )
