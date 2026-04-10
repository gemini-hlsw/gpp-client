Attachment
==========

The ``gpp attachment`` command group provides attachment operations
for programs and observations.

Quick Example
-------------

List attachments for a program:

.. code-block:: bash

   gpp attachment list --program-id p-123

List attachments for an observation:

.. code-block:: bash

   gpp attachment list --observation-id o-123

Selecting Attachments
---------------------

The ``list`` command requires exactly one selector.

Supported selectors:

- ``--observation-id``
- ``--observation-reference``
- ``--program-id``
- ``--program-reference``
- ``--proposal-reference``

.. warning::

   Provide exactly one selector. Passing none or more than one will result
   in an error.

Examples
--------

By observation reference:

.. code-block:: bash

   gpp attachment list --observation-reference GN-2026A-Q-1-1

By program reference:

.. code-block:: bash

   gpp attachment list --program-reference GN-2026A-Q-1

By proposal reference:

.. code-block:: bash

   gpp attachment list --proposal-reference GN-2026A-Q-1

Reference
---------

.. typer:: gpp_client.cli.cli.app:attachment
   :prog: gpp attachment
   :make-sections:
   :show-nested:
   :width: 80
   :theme: dark

See also: :doc:`../domains/attachment`