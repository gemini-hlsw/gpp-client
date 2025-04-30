from typing import Optional

from gpp_client import GPPClient


_INTROSPECTION_QUERY = """
{
  __schema {
    types {
      name
    }
  }
}
"""


async def check_connectivity(
    url: Optional[str] = None,
    token: Optional[str] = None,
) -> bool:
    """Returns ``True`` if GPP GraphQL endpoint is reachable and authenticated.

    Parameters
    ----------
    url : str, optional
        The base URL of the GPP GraphQL endpoint.
    token : str, optional
        The bearer token used for authorization.

    Returns
    -------
    bool
        ``True`` if endpoint is reachable and returns valid data.
    """
    try:
        client = GPPClient(url=url, token=token)
        await client._execute(query=_INTROSPECTION_QUERY)

    except Exception:
        return False

    return True
