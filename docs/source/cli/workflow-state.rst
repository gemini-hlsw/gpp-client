Workflow State
==============

The ``gpp workflow-state`` command group provides access to observation workflow state.

Quick Example
-------------

Get workflow state:

.. code-block:: bash

   gpp workflow-state get --observation-id o-123

Selecting Workflow State
------------------------

The ``get`` command requires exactly one selector:

- ``--observation-id``
- ``--observation-reference``

.. warning::

   Provide exactly one selector.

Reference
---------

.. typer:: gpp_client.cli.cli.app:workflow-state
   :prog: gpp workflow-state
   :make-sections:
   :show-nested:
   :width: 80
   :theme: dark

See also: :doc:`../domains/workflow-state`