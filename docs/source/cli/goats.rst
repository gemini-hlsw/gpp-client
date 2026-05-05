GOATS
=====

The ``gpp goats`` command group provides access to GOATS resources.

Quick Example
-------------

List GOATS programs:

.. code-block:: bash

   gpp goats list-programs

List observations for a program:

.. code-block:: bash

   gpp goats list-observations p-123

Reference
---------

.. typer:: gpp_client.cli.cli.app:goats
   :prog: gpp goats
   :make-sections:
   :show-nested:
   :width: 80
   :theme: dark

See also: :doc:`../domains/goats`