Target
======

The ``gpp target`` command group provides access to target operations.

Quick Example
-------------

Get a target:

.. code-block:: bash

   gpp target get --target-id t-123

List targets:

.. code-block:: bash

   gpp target list --limit 10

Selecting Targets
-----------------

The ``get`` command requires exactly one selector:

- ``--target-id``

.. warning::

   Provide exactly one selector.

Reference
---------

.. typer:: gpp_client.cli.cli.app:target
   :prog: gpp target
   :make-sections:
   :show-nested:
   :width: 80
   :theme: dark

See also: :doc:`../domains/target`