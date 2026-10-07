# GPP Client

[![Run Tests](https://github.com/gemini-hlsw/gpp-client/actions/workflows/run_tests.yaml/badge.svg?branch=main)](https://github.com/gemini-hlsw/gpp-client/actions/workflows/run_tests.yaml)
![Docs Status](https://readthedocs.org/projects/gpp-client/badge/?version=latest)
[![codecov](https://codecov.io/gh/gemini-hlsw/gpp-client/branch/main/graph/badge.svg?token=9V5TA510MF)](https://codecov.io/gh/gemini-hlsw/gpp-client)
![PyPI - Python Version](https://img.shields.io/pypi/pyversions/gpp-client?color=green)
![PyPI - Version](https://img.shields.io/pypi/v/gpp-client?color=green)

---

_A Python client and command line tool for the Gemini Program Platform (GPP)._

**Documentation**: https://gpp-client.readthedocs.io/en/stable/

**Source code**: https://github.com/gemini-hlsw/gpp-client

---

Use GPP from Python or the shell. You can read and change programs, observations and targets, and upload or download attached files. gpp-client is a typed, async Python client and a `gpp` command line tool. Most of it is generated from GPP's GraphQL schema, so it changes when GPP does, and you should upgrade often.

One install reaches both GPP environments, development and production. The client uses production unless you select development.

## Install

You need Python 3.11 or newer. Install the client with pip:

```bash
pip install gpp-client
```

## Quickstart

You get an API token from Explore, GPP's web app. Get a production token here:
https://explore.gemini.edu/

Save this script as `first_call.py`, with your API token in place of `your-token`:

```python
import asyncio

from gpp_client import GPPClient


async def main() -> None:
    async with GPPClient(token="your-token") as client:
        result = await client.program.get_all(limit=5)
        for program in result.programs.matches:
            print(program.id, program.name)


asyncio.run(main())
```

Run it with `python first_call.py`. It prints up to five programs your token can see, something like:

```text
p-10a Galaxy survey
p-10b Hot Jupiter transits
```

To keep the token out of your code, set it in the `GPP_TOKEN` environment variable, a `.env` file or the configuration file, and build the client with `GPPClient()`. "Configure the client" shows every setting and where you can set it:
https://gpp-client.readthedocs.io/en/stable/guides/configuration.html

Production holds real programs, so try calls that change data on development first. Development needs its own token, from development Explore at https://explore-dev.lucuma.xyz/. "Select an environment" shows how:
https://gpp-client.readthedocs.io/en/stable/guides/environments.html

## Links

- Getting started: https://gpp-client.readthedocs.io/en/stable/getting-started.html
- Configure the client: https://gpp-client.readthedocs.io/en/stable/guides/configuration.html
- Select an environment: https://gpp-client.readthedocs.io/en/stable/guides/environments.html
- Use the domains: https://gpp-client.readthedocs.io/en/stable/guides/domains.html
- Handle errors: https://gpp-client.readthedocs.io/en/stable/guides/errors.html
- Write a custom query: https://gpp-client.readthedocs.io/en/stable/guides/custom-queries.html
- Use the command line: https://gpp-client.readthedocs.io/en/stable/guides/cli.html
- Upgrade the client: https://gpp-client.readthedocs.io/en/stable/guides/versions.html
- Reference: https://gpp-client.readthedocs.io/en/stable/client.html
- Contributing: https://gpp-client.readthedocs.io/en/stable/developer/contributing.html
