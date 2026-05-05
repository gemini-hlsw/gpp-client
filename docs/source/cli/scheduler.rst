Scheduler
=========

The ``gpp scheduler`` command group provides access to scheduler data.

Quick Example
-------------

List scheduler programs:

.. code-block:: bash

   gpp scheduler list-programs

Filter by program ID:

.. code-block:: bash

   gpp scheduler list-programs --program-id p-123

Reference
---------

.. typer:: gpp_client.cli.cli.app:scheduler
   :prog: gpp scheduler
   :make-sections:
   :show-nested:
   :width: 80
   :theme: dark

See also: :doc:`../domains/scheduler`