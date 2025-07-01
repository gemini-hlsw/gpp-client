Command Line Interface Reference
================================

The ``gpp`` command-line interface provides access to the Gemini Program Platform (GPP), enabling interaction with programs, observations, targets, proposals, and related resources.

.. typer:: gpp_client.cli.cli:app
    :prog: gpp
    :make-sections:
    :width: 80
    :theme: dark

Each command supports ``--help`` for usage details.

Commands
--------

Individual commands are documented below:

.. toctree::
    :maxdepth: 1

    config
    call_for_proposals
    program_note
    observation
    target
    program
    site_status

.. note::

   The ``config`` group is used to manage local settings and authentication for the CLI.
   You must either configure credentials using ``gpp config`` or set the ``GPP_TOKEN``
   and ``GPP_URL`` environment variables. See the :doc:`credentials </credentials>` section for details.
