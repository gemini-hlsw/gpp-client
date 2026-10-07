Select an environment
=====================

GPP has two environments: ``production``, where real programs live, and
``development``, where GPP tries changes first. One install of the client
works with both.

.. _choosing-the-environment:

Set it for one client or for all
--------------------------------

The client uses ``production`` unless you select another environment. To
select one for a single client, pass ``environment=``:

.. code-block:: python

   from gpp_client import GPPClient

   async with GPPClient(
       environment="development",
   ) as client:
       result = await client.program.get_all(limit=5)
       for program in result.programs.matches:
           print(program.id, program.name)
   # p-10a Galaxy survey
   # p-10b Hot Jupiter transits

To select one for every client, set ``GPP_ENVIRONMENT`` in the shell instead:

.. code-block:: bash

   export GPP_ENVIRONMENT=development

Environment names aren't case sensitive. If you pass a name the client doesn't
recognize, it raises ``GPPClientError``, and the message lists the valid names.

To check which environment a client uses, read ``client.settings.environment``.
The client also logs the environment and its URL at INFO level when it starts.
To see that log line, pass ``debug=True`` or set up Python ``logging``.

.. _environment-on-the-command-line:

Set it on the command line
--------------------------

To select the environment for one command only, put ``--env`` before the
command:

.. code-block:: bash

   gpp --env development program list

To store a default for every command and script on this machine, run
``gpp set-default-env``, which writes the default to the configuration file:

.. code-block:: bash

   gpp set-default-env development

If the configuration file doesn't exist yet, ``set-default-env`` creates it. If
the file exists, the command keeps your other settings, but it won't change a
file that isn't valid TOML.

Use both environments at once
-----------------------------

Two clients on different environments can run side by side:

.. code-block:: python

   from gpp_client import GPPClient

   async with (
       GPPClient(environment="production") as prod,
       GPPClient(environment="development") as dev,
   ):
       prod_result = await prod.program.get_all(limit=5)
       dev_result = await dev.program.get_all(limit=5)
       print(len(prod_result.programs.matches))
       print(len(dev_result.programs.matches))
   # 5
   # 5

Set a token for each environment
--------------------------------

Each environment has its own token, which you get from Explore, GPP's web
app, in that environment: https://explore.gemini.edu/ for production and
https://explore-dev.lucuma.xyz/ for development. The client reads the production token from
``GPP_TOKEN`` and the development token from ``GPP_DEVELOPMENT_TOKEN``, so a
development client never reads ``GPP_TOKEN``:

.. code-block:: bash

   export GPP_TOKEN=...
   export GPP_DEVELOPMENT_TOKEN=...

If the selected environment has no token, the client raises ``GPPAuthError``,
and the message names the variable to set. To pass a token in code, or to keep
both tokens in a ``.env`` file or the configuration file, see
:doc:`configuration`.

When a call doesn't fit the selected environment, the client raises
``GPPEnvironmentError``. For details, see :ref:`environment-errors`.

What your editor checks
-----------------------

Your editor can tell which operations ``client.graphql`` offers, depending on
how you set the environment:

``GPPClient(environment="development")``
   When you write the environment out, as here or with ``"production"``, the
   editor offers only that environment's operations, and it flags a call that
   the environment lacks before you run the code.

``GPPClient()``
   The environment comes from ``GPP_ENVIRONMENT``, the ``.env`` file, the
   configuration file, or the default, so the editor offers every operation.

A parameter typed plain ``GPPClient``
   The editor offers only the operations that both environments have.
