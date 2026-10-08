GPP Client
==========

Use GPP, the Gemini Program Platform, from Python or the shell. You can read
and change programs, observations and targets, and upload or download attached
files.

``gpp-client`` is a typed, async Python client and a ``gpp`` command. One
install reaches both GPP environments, development and production, and the
client uses production unless you select development.

To install the client, run:

.. code-block:: bash

   pip install gpp-client

This script prints up to five programs your API token can see:

.. code-block:: python

   import asyncio

   from gpp_client import GPPClient


   async def main() -> None:
       async with GPPClient(token="your-token") as client:
           result = await client.program.get_all(limit=5)
           for program in result.programs.matches:
               print(program.id, program.name)


   asyncio.run(main())

.. rubric:: Where to go next

- :doc:`getting-started` - install the client, make your first call and keep
  your token out of your code.
- :doc:`guides/configuration` - every setting, and the places you can set it.
- :doc:`guides/environments` - development or production, and a token for
  each.
- :doc:`guides/domains` - get, find and change programs, observations,
  targets and more.
- :doc:`guides/errors` - what each error means and what to catch.
- :doc:`guides/cli` - the same tasks from the shell.
- :doc:`guides/custom-queries` - select the fields yourself when no domain
  method fits.
- :doc:`guides/versions` - why you should upgrade often.

Found a bug or want a change? See :doc:`developer/contributing`.

.. toctree::
   :hidden:

   getting-started

.. toctree::
   :hidden:
   :caption: Guides

   guides/configuration
   guides/environments
   guides/domains
   guides/errors
   guides/cli
   guides/attachments
   guides/subscriptions
   guides/custom-queries
   guides/versions

.. toctree::
   :hidden:
   :caption: Reference

   domains/index
   client
   environment
   exceptions
   graphql-api/index
   rest-client
   cli/index

.. toctree::
   :hidden:
   :caption: Developer guide

   developer/contributing
