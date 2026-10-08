Configure the client
====================

The client has four settings: the environment, the production token, the
development token, and debug logging. You can set each one in four places: as an argument to
``GPPClient``, as an environment variable, in a ``.env`` file, or in the
configuration file. So you can keep tokens out of your code, and switch
environments without editing your scripts.

The settings
------------

This table lists each setting and its name in each place:

.. list-table::
   :header-rows: 1

   * - Setting
     - ``GPPClient`` argument
     - Environment variable and ``.env`` key
     - Configuration file key
     - Default
   * - Environment
     - ``environment``
     - ``GPP_ENVIRONMENT``
     - ``environment``
     - ``production``
   * - Production token
     - ``token``, when production is selected
     - ``GPP_TOKEN``
     - ``token``
     - None
   * - Development token
     - ``token``, when development is selected
     - ``GPP_DEVELOPMENT_TOKEN``
     - ``development_token``
     - None
   * - Debug logging
     - ``debug``
     - ``GPP_DEBUG``
     - ``debug``
     - ``false``

The client needs a token only for the environment you select. You get each
token from Explore, GPP's web app, in the matching environment:

- Production: https://explore.gemini.edu/
- Development: https://explore-dev.lucuma.xyz/

For what each environment is for, see :doc:`environments`.

Debug logging prints the client's own log messages to the console, including
each GraphQL and REST client it builds and the URL it connects to. Turn it on
when you want to see what the client is doing.

.. _settings-precedence:

Where the client looks
----------------------

The client takes each setting from the first of these places that sets it:

1. Arguments to ``GPPClient``.
2. Environment variables.
3. A ``.env`` file in the current folder.
4. The configuration file.

If none of them sets a value, the client uses the default from the table.

The client looks up each setting on its own, so the environment can come from
one place and a token from another. For example, you can keep both tokens in
the configuration file and select development for one shell with
``GPP_ENVIRONMENT``. The client then reads the development token from the
file.

An empty value counts as unset. So ``GPP_TOKEN=""`` doesn't hide a token in
your ``.env`` file or the configuration file.

Pass settings to GPPClient
--------------------------

Arguments to ``GPPClient`` apply to that one client and override every other
place:

.. code-block:: python

   from gpp_client import GPPClient

   async with GPPClient(
       environment="development",
       token="your-development-token",
       debug=True,
   ) as client:
       result = await client.program.get_all(limit=5)

The ``token`` argument is the token for the selected environment, and there's
no argument per environment. If you don't pass ``environment=``, the token goes
to whichever environment the client selects from the other places. To use both
environments at once, build two clients, as :doc:`environments` shows.

The ``token`` argument is also how you hand the client a token you keep
somewhere else, such as a secret store or a file only you can read:

.. code-block:: python

   from pathlib import Path

   from gpp_client import GPPClient

   token = Path("~/.gpp-token").expanduser().read_text().strip()

   async with GPPClient(token=token) as client:
       result = await client.program.get_all(limit=5)

Set environment variables
-------------------------

Environment variables apply to every client and every ``gpp`` command you run
from that shell:

.. code-block:: bash

   export GPP_TOKEN="your-production-token"
   export GPP_DEVELOPMENT_TOKEN="your-development-token"
   export GPP_ENVIRONMENT=development

To keep the variables across shells, add these lines to your shell's startup
file.

Use a .env file
---------------

A ``.env`` file holds the same variables, one per line, without ``export``:

.. code-block:: text

   GPP_TOKEN=your-production-token
   GPP_DEVELOPMENT_TOKEN=your-development-token
   GPP_ENVIRONMENT=development

The client reads ``.env`` from the current folder, which is the folder you run
Python or ``gpp`` from, not the folder that holds your script. A ``.env`` file
suits one project, so keep it out of version control.

Use the configuration file
--------------------------

The configuration file sets defaults for every project on your machine. It's
``config.toml``, in a ``gpp-client`` folder where your platform keeps app
settings. To print its path, run:

.. code-block:: bash

   gpp get-config-path

The client reads the file only if it exists, so create it yourself, or let
``gpp set-default-env`` create it. Here's an example configuration file:

.. code-block:: toml

   environment = "development"
   token = "your-production-token"
   development_token = "your-development-token"
   debug = true

The client ignores keys it doesn't know, so a misspelled key has no effect and
raises no error. If a setting doesn't take, check its spelling against the
table above.

To store the default environment from the command line, run
``gpp set-default-env``. For details, see
:ref:`environment-on-the-command-line`.

Use your own HTTP client
------------------------

To send requests through a proxy, or with your own timeouts, pass an
``httpx.AsyncClient`` as ``http_client=``. The client sends every GraphQL
request through it:

.. code-block:: python

   import httpx

   from gpp_client import GPPClient

   async with (
       httpx.AsyncClient(proxy="http://proxy.example.org:8080") as http,
       GPPClient(http_client=http) as client,
   ):
       result = await client.program.get_all(limit=5)

You own that HTTP client, so ``GPPClient`` leaves it open when it closes. The
``async with`` block above closes it. There's no variable or file key for
``http_client``.

Check what a client uses
------------------------

To see the settings a client resolved, read ``client.settings``:

.. code-block:: python

   print(client.settings.environment.label)
   # development
   print(client.settings.token)
   # **********

Tokens print as asterisks, so you can log the settings without leaking a
token. The client also logs the environment and its URL at INFO level when it
starts.

On the command line
-------------------

The ``gpp`` command reads the same environment variables, ``.env`` file and
configuration file as the Python client. It has no option for the token, so
set the token in one of those places. To select the environment for one
command, put ``--env`` before the command. For details, see :doc:`cli`.
