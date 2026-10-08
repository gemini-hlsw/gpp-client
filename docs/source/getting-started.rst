Getting started
===============

This page takes you from installing the client to your first call. You'll give
the client your API token, print the programs your token can see, and then
move the token out of your code.

1. Install
----------

You need Python 3.11 or newer. Install the client with pip:

.. code-block:: bash

   pip install gpp-client

2. Make your first call
-----------------------

You get an API token from Explore, GPP's web app. This page uses production,
so get your token from production Explore:

https://explore.gemini.edu/

Save this script as ``first_call.py``, with your API token in place of
``your-token``:

.. code-block:: python

   import asyncio

   from gpp_client import GPPClient


   async def main() -> None:
       async with GPPClient(token="your-token") as client:
           result = await client.program.get_all(limit=5)
           for program in result.programs.matches:
               print(program.id, program.name)


   asyncio.run(main())

Then run the script:

.. code-block:: bash

   python first_call.py

It prints up to five programs, one per line, something like:

.. code-block:: text

   p-10a Galaxy survey
   p-10b Hot Jupiter transits

Every call is ``async``, so it runs inside ``async def main``, and
``asyncio.run`` starts it. The ``async with`` block closes the client's
connections when it ends.

3. Get one program
------------------

To fetch one program, take an ID from that list and pass it to ``get_by_id``.
Put this code in ``main`` in place of the loop:

.. code-block:: python

   result = await client.program.get_by_id("p-10a")
   program = result.program
   if program is None:
       print("Not found, or your token can't see it.")
   else:
       print(program.name, program.proposal_status)
   # Galaxy survey ProposalStatus.ACCEPTED

``client.program`` is a *domain*, which groups the methods for one area of GPP.
To learn how every domain works, see :doc:`guides/domains`.

4. Keep the token out of your code
----------------------------------

Passing ``token=`` is the quickest way to try the client, but a token written
in a script ends up in your history and in anything you share. So once your
first call works, give the client the token in one of these ways instead, and
build it with no arguments:

.. code-block:: python

   async with GPPClient() as client:
       result = await client.program.get_all(limit=5)

The simplest way is the ``GPP_TOKEN`` environment variable:

.. code-block:: bash

   export GPP_TOKEN="your-token"

If you'd rather not set the variable in every shell, put the same line,
without ``export``, in a ``.env`` file in the folder you run your code from:

.. code-block:: text

   GPP_TOKEN=your-token

To set the token once for every project on your machine, put it in the
configuration file instead:

.. code-block:: toml

   token = "your-token"

If the token is set in more than one place, ``token=`` wins, then the
variable, then the ``.env`` file, then the configuration file. For where the
configuration file lives and every other setting, see
:doc:`guides/configuration`.

In a notebook
-------------

Jupyter and IPython run ``await`` at the top level, so you can skip
``asyncio.run``. Close the client yourself when you're done:

.. code-block:: python

   from gpp_client import GPPClient

   client = GPPClient()
   result = await client.program.get_all(limit=5)
   for program in result.programs.matches:
       print(program.id, program.name)
   await client.close()

In a terminal, ``python -m asyncio`` gives you the same top-level ``await``.

If it fails
-----------

These are the two most common failures:

- ``GPPAuthError: A token is required for the production environment. Set
  'GPP_TOKEN'.`` - the client found no token. Pass ``token=``, or set the
  token as step 4 shows.
- The call fails with an error from GPP - the token is wrong or has expired,
  or GPP can't be reached.

For the other errors a call can raise, see :doc:`guides/errors`.

.. _try-on-development:

Try changes on development
--------------------------

The client uses production unless you select another environment. Production
holds real programs, so try calls that change data on development first.
Development has its own token, which you get from development Explore:

https://explore-dev.lucuma.xyz/

To select development, pass the environment and its token:

.. code-block:: python

   from gpp_client import GPPClient

   async with GPPClient(
       environment="development",
       token="your-development-token",
   ) as client:
       result = await client.program.get_all(limit=5)
       for program in result.programs.matches:
           print(program.id, program.name)

Outside your code, the client reads the development token from
``GPP_DEVELOPMENT_TOKEN``. For the other ways to select an environment, see
:doc:`guides/environments`.

Next steps
----------

- :doc:`guides/configuration` - every setting and every place you can set it.
- :doc:`guides/domains` - get, find and change items through the domains.
- :doc:`guides/errors` - what to catch.
- :doc:`guides/cli` - the same calls from the ``gpp`` command.
- :doc:`guides/custom-queries` - select exactly the fields you want.
- :doc:`guides/versions` - why you should upgrade often.
