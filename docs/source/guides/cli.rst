Use the command line
====================

Installing the client also installs the ``gpp`` command. The command reads the
same settings and tokens as the Python client.

Check your setup
----------------

To check that GPP is reachable and your token is valid, run ``gpp ping``:

.. code-block:: bash

   gpp ping

Run a command
-------------

Commands are grouped by domain, as in the Python client, such as
``program``, ``observation`` or ``attachment``:

.. code-block:: bash

   gpp program list --limit 10
   gpp observation get --observation-id o-1a2
   gpp attachment list --program-id p-10a

Commands that fetch data print the result as JSON.

Some ``get`` and ``list`` commands can find their item in several ways, such as
by ID or by reference. Those commands take exactly one of these options, and
giving none, or more than one, is an error.

To see the options of any command or group, add ``--help``. For every command,
see :doc:`../cli/index`.

Select the environment
----------------------

To select the environment for one command, put ``--env`` before the command:

.. code-block:: bash

   gpp --env development program list

To store a default instead, see :ref:`environment-on-the-command-line`.

Each command that calls GPP prints the environment it uses, and its URL, to
stderr, so the line stays apart from the result:

.. code-block:: text

   Environment: development (https://lucuma-postgres-odb-dev.herokuapp.com)

When a command fails
--------------------

A failing command prints the error and exits with code 1. To see the full
traceback, add the global ``--debug`` option before the command:

.. code-block:: bash

   gpp --debug program get --program-id p-10a
