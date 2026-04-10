Site Status
===========

The ``gpp site-status`` command group provides access to Gemini site status.

Quick Example
-------------

Get status for Gemini North:

.. code-block:: bash

   gpp site-status get north

Get status for Gemini South:

.. code-block:: bash

   gpp site-status get south

Reference
---------

.. typer:: gpp_client.cli.cli.app:site-status
   :prog: gpp site-status
   :make-sections:
   :show-nested:
   :width: 80
   :theme: dark

See also: :doc:`../domains/site-status`