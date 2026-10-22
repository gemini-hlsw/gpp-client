.. _configuration:

Configuration
=============

Overview
--------

The client uses ``pydantic-settings`` to resolve configuration at runtime.

Configuration is strictly validated and resolved from several sources.


Choosing an Environment
-----------------------

One install reaches both GPP environments, development and production, and you
select one each time you create a client. The client takes the first of these
that is set:

1. The ``environment`` argument, such as
   ``GPPClient(environment="development")``.
2. The ``GPP_ENVIRONMENT`` environment variable.
3. ``GPP_ENVIRONMENT`` in the ``.env`` file of the current folder.
4. ``environment`` in the configuration file described below.

Environment names ignore case. An empty value, or one made only of spaces,
counts as unset, so the next source in the list decides. An unknown name raises
:class:`~gpp_client.exceptions.GPPClientError`, which lists the valid names.

If none of them is set, the client uses production and emits a
``FutureWarning``, because a future release will raise an error instead. Set
the environment explicitly so that your code keeps working.

When the client starts, it logs at INFO level which environment it uses, where
that choice came from, and the URL it sends to. ``repr(client)`` shows the
environment as well.

The ``gpp`` command follows the same order, but its ``--env`` option comes
before everything else. Without any of them, the command uses production and
prints a warning to stderr.


When the Environments Differ
----------------------------

Changes reach development first and production later, so at any moment one
environment can have a field, an enum value, or an operation that the other
lacks. The client is generated from both schemas at once, and the request it
sends is trimmed to what the selected environment has:

- A result field that the selected environment lacks is ``None``. Call
  ``client.is_available(Model, "field")`` to tell that apart from a value that
  GPP left empty.
- ``client.enum_values(Enum)`` lists the members that the selected environment
  accepts.
- Calling an operation that the selected environment lacks raises
  :class:`~gpp_client.exceptions.NotAvailable` before anything is sent.


Authentication
--------------

Each environment has its own token:

- Development reads ``GPP_DEVELOPMENT_TOKEN``.
- Production reads ``GPP_TOKEN``.

.. code-block:: bash

   export GPP_DEVELOPMENT_TOKEN=...
   export GPP_TOKEN=...

You can also pass a token when you create the client, and it applies to the
selected environment:

.. code-block:: python

   client = GPPClient(environment="development", token="my-token")

.. warning::

   Tokens are not interchangeable. A development client never reads
   ``GPP_TOKEN``, and it raises :class:`~gpp_client.exceptions.GPPAuthError`,
   naming the variable to set, when it has no development token.


Configuration Sources
---------------------

Each setting is resolved independently, from the first of these that sets it:

1. Arguments to ``GPPClient``
2. Environment variables
3. The ``.env`` file
4. The configuration file
5. Model defaults


Configuration File
------------------

An optional TOML configuration file can hold your environment, your tokens,
and the debug setting. Both the Python client and the ``gpp`` command read it.

The file lives in a ``.gpp-client`` folder in your home directory:

- macOS and Linux:
  ``~/.gpp-client/config.toml``
- Windows:
  ``C:\Users\<user>\AppData\Roaming\gpp-client\config.toml``

The file is only used if it exists:

.. code-block:: toml

   environment = "development"
   token = "prod-token"
   development_token = "dev-token"
   debug = true

These four keys are the only ones the file can hold. Any other key, such as a
misspelled one, stops the client and the ``gpp`` command with an error that
names it, so a setting is never silently ignored.

To manage the configuration file from the command line, use the ``gpp config``
commands described in :doc:`cli/config`.

.. tip::

   To see the exact path used on your system, run ``gpp config path`` or:

   .. code-block:: python

      from gpp_client.settings import get_config_path
      print(get_config_path())


API Reference
-------------

.. autoclass:: gpp_client.settings.GPPSettings
   :members:
   :show-inheritance:
   :exclude-members: model_config