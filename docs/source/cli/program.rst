Program
=======

The ``gpp program`` command group provides access to program operations.

Quick Example
-------------

Get a program:

.. code-block:: bash

   gpp program get --program-id p-123

List programs:

.. code-block:: bash

   gpp program list --limit 10

Selecting Programs
------------------

The ``get`` command requires exactly one selector:

- ``--program-id``
- ``--program-reference``
- ``--proposal-reference``

.. warning::

   Provide exactly one selector.

Reference
---------

.. typer:: gpp_client.cli.cli.app:program
   :prog: gpp program
   :make-sections:
   :show-nested:
   :width: 80
   :theme: dark

See also: :doc:`../domains/program`