CLI
===

The ``gpp`` command-line interface provides access to the Gemini Program
Platform (GPP) from the command line.

The CLI uses the same configuration and authentication rules as the Python
client. See :doc:`../configuration` for details.

Quick Example
-------------

Check connectivity:

.. code-block:: bash

   gpp ping

List attachments for a program:

.. code-block:: bash

   gpp attachment list --program-id p-123

Command Reference
-----------------

.. typer:: gpp_client.cli.cli:app
   :prog: gpp
   :make-sections:
   :width: 80
   :theme: dark

.. tip::

   Use ``--help`` with any command or subcommand for usage details.

.. typer:: gpp_client.cli.cli:app:ping
   :prog: gpp ping
   :make-sections:
   :width: 80
   :theme: dark

.. typer:: gpp_client.cli.cli:app:get-config-path
   :prog: gpp get-config-path
   :make-sections:
   :width: 80
   :theme: dark

Commands
--------

.. toctree::
   :maxdepth: 1

   attachment
   observation
   target
   program
   site-status
   workflow-state
   scheduler
   goats