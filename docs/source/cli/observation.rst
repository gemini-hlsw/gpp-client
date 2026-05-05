Observation
===========

The ``gpp observation`` command group provides access to observation operations.

Quick Example
-------------

Get an observation:

.. code-block:: bash

   gpp observation get --observation-id o-123

List observations:

.. code-block:: bash

   gpp observation list --limit 10

Selecting Observations
----------------------

The ``get`` command requires exactly one selector:

- ``--observation-id``
- ``--observation-reference``

.. warning::

   Provide exactly one selector.

Reference
---------

.. typer:: gpp_client.cli.cli.app:observation
   :prog: gpp observation
   :make-sections:
   :show-nested:
   :width: 80
   :theme: dark

See also: :doc:`../domains/observation`