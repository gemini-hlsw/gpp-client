"""
Write ``llms.txt``: a summary of gpp-client for AI agents.

The rules live on the hosted docs, so the file links to them instead of
restating them. The build generates the availability section from the merged
schema and the trimmed operations, so it changes with every schema update.
``scripts/build_client.py`` writes the file, so change the text here, never in
``llms.txt``.
"""

from collections.abc import Mapping
from dataclasses import dataclass

from custom_plugins.environments import USER_ENVIRONMENTS

__all__ = ["AvailabilityNotes", "render_llms_txt"]


@dataclass(frozen=True)
class AvailabilityNotes:
    """
    What differs between the environments.

    Parameters
    ----------
    methods : Mapping[str, tuple[str, ...]]
        Each generated client method with the environments that have it.
    inputs : Mapping[str, tuple[str, ...]]
        Each environment-specific argument, input field and enum value with the
        environments that have it.
    required : Mapping[str, tuple[str, ...]]
        Each input field only some environments require, with those
        environments.
    missing_fields : Mapping[str, tuple[str, ...]]
        Per environment, the selected result fields it lacks.
    leaving : tuple[str, ...]
        Selected fields development lacks but production still has.
    """

    methods: Mapping[str, tuple[str, ...]]
    inputs: Mapping[str, tuple[str, ...]]
    required: Mapping[str, tuple[str, ...]]
    missing_fields: Mapping[str, tuple[str, ...]]
    leaving: tuple[str, ...]


_HEADER = """\
# gpp-client

> Async Python client and `gpp` command line tool for GPP, the Gemini Program Platform. One install reaches development and production, and the client uses production unless you select development. Each environment has its own token: `GPP_TOKEN` for production and `GPP_DEVELOPMENT_TOKEN` for development. Get each token from Explore, GPP's web app: https://explore.gemini.edu/ for production and https://explore-dev.lucuma.xyz/ for development.

```python
import asyncio

from gpp_client import GPPClient


async def main() -> None:
    async with GPPClient() as client:
        result = await client.program.get_all(limit=5)
        for program in result.programs.matches:
            print(program.id, program.name)


asyncio.run(main())
```

Domains such as `client.program` cover common tasks, and `client.graphql` has a generated method for every operation. The client follows GPP's schema closely, so upgrade often.

## Docs

- [Getting started](https://gpp-client.readthedocs.io/en/stable/getting-started.html): install, token and first call.
- [Configure the client](https://gpp-client.readthedocs.io/en/stable/guides/configuration.html): every setting, and the arguments, variables, .env file and configuration file that set it.
- [Select an environment](https://gpp-client.readthedocs.io/en/stable/guides/environments.html): development or production, and a token for each.
- [Use the domains](https://gpp-client.readthedocs.io/en/stable/guides/domains.html): get, find and change items through `client.program` and the other domains.
- [Handle errors](https://gpp-client.readthedocs.io/en/stable/guides/errors.html#environment-errors): what each error and warning means, including calls that use something the selected environment lacks.
- [Write a custom query](https://gpp-client.readthedocs.io/en/stable/guides/custom-queries.html): select the fields yourself when no domain method fits.
- [Use the command line](https://gpp-client.readthedocs.io/en/stable/guides/cli.html): the `gpp` command.
- [Upgrade the client](https://gpp-client.readthedocs.io/en/stable/guides/versions.html): one release works with both environments, and why to upgrade often.
- [Reference](https://gpp-client.readthedocs.io/en/stable/client.html): generated API reference, starting at `GPPClient`; the site's Reference section also covers the domains, GraphQL API, REST client, settings, exceptions and CLI.

## Optional

- [Follow changes as they happen](https://gpp-client.readthedocs.io/en/stable/guides/subscriptions.html): subscribe to edits.
- [Upload and download attachments](https://gpp-client.readthedocs.io/en/stable/guides/attachments.html): also list, replace and delete files.

## Availability
"""


def render_llms_txt(notes: AvailabilityNotes) -> str:
    """
    Return the ``llms.txt`` text.

    Parameters
    ----------
    notes : AvailabilityNotes
        What differs between the environments.

    Returns
    -------
    str
        The file's text. The availability section names development and
        production only, and lists nothing that works on both.
    """
    lines = []
    for environment in USER_ENVIRONMENTS:
        methods = _only_on(notes.methods, environment)
        if methods:
            lines.append(
                f"- Methods only on {environment}: "
                + ", ".join(f"`client.graphql.{m}`" for m in methods)
            )
    for environment in USER_ENVIRONMENTS:
        inputs = _only_on(notes.inputs, environment)
        if inputs:
            lines.append(
                f"- Arguments, input fields and enum values only on {environment}: "
                + _names(inputs)
            )
    for environment in USER_ENVIRONMENTS:
        required = _only_on(notes.required, environment)
        if required:
            lines.append(
                f"- Input fields required on {environment} only: " + _names(required)
            )
    for environment in USER_ENVIRONMENTS:
        fields = notes.missing_fields.get(environment, ())
        if fields:
            lines.append(
                f"- Fields that read `None` on {environment}: " + _names(fields)
            )
    if notes.leaving:
        lines.append("- Fields leaving production: " + _names(notes.leaving))
    if not lines:
        lines.append(
            "- Everything the client generates works on development and production."
        )
    return (
        _HEADER + "\nThis list comes from the schemas this release was built from. "
        "Anything not listed works on "
        "development and production.\n\n" + "\n".join(lines) + "\n"
    )


def _only_on(
    availability: Mapping[str, tuple[str, ...]], environment: str
) -> list[str]:
    return sorted(
        name
        for name, environments in availability.items()
        if [env for env in USER_ENVIRONMENTS if env in environments] == [environment]
    )


def _names(names) -> str:
    return ", ".join(f"`{name}`" for name in names)
