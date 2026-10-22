Config
======

The ``gpp config`` command group manages the configuration file that the client
and the ``gpp`` command read, so you don't have to edit the TOML by hand. For
what the file holds and where it lives, see :doc:`../configuration`.

Create the configuration file
-----------------------------

To create the file, run ``gpp config init``. It asks for each environment's
token at a hidden prompt, and a blank answer leaves that token out:

.. code-block:: bash

   gpp config init

The command creates the ``.gpp-client`` folder if it's missing, and on macOS
and Linux it makes the file readable only by you. If a configuration file
already exists, ``init`` stops without changing it. To start over, pass
``--force``, which moves the old file to ``config.toml.bak`` before writing the
new one.

Change one setting
------------------

To change one setting, run ``gpp config set`` with the key. The keys are
``environment``, ``token``, ``development_token`` and ``debug``. The
``environment`` and ``debug`` keys take the value as an argument:

.. code-block:: bash

   gpp config set environment development
   gpp config set debug true

A token never goes on the command line, because the shell would keep it in its
history. Instead, ``set`` asks for the token at a hidden prompt, or reads one
line from standard input when you redirect it:

.. code-block:: bash

   gpp config set development_token
   gpp config set development_token < development-token.txt

To remove a setting, run ``gpp config unset`` with the key. Both ``set`` and
``unset`` keep your comments and the other keys in the file.

See the settings in effect
--------------------------

The ``gpp config show`` command lists each setting with its value and the
source it came from: ``--env``, an environment variable, the ``.env`` file, the
configuration file, or the default. Tokens show only their last four
characters:

.. code-block:: bash

   gpp config show

It prints something like:

.. code-block:: text

   Key                Value        Source
   environment        development  configuration file
   token              ****1a2b     variable GPP_TOKEN
   development_token  ****9f8e     configuration file
   debug              false        default

Find or delete the file
-----------------------

To see where the configuration file lives on your system, run
``gpp config path``. To delete the file, run ``gpp config delete``, which asks
first unless you pass ``--yes``.

Reference
---------

.. typer:: gpp_client.cli.cli.app:config
   :prog: gpp config
   :make-sections:
   :show-nested:
   :width: 80
   :theme: dark
