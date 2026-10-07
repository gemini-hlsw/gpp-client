Domains
=======

Each domain groups the methods for one area of GPP. You reach a domain as an
attribute of the client, such as ``client.program``.

Most domain methods return a model generated for their query. If a lookup
finds nothing, the model holds ``None`` in place of the item. When no domain
method fits, write a custom query, as described in
:doc:`../guides/custom-queries`.

.. list-table::
   :header-rows: 1

   * - Domain
     - Use it to
   * - :doc:`client.program <program>`
     - Get, find and change programs.
   * - :doc:`client.observation <observation>`
     - Get, find and change observations.
   * - :doc:`client.target <target>`
     - Get, find and change targets.
   * - :doc:`client.workflow_state <workflow-state>`
     - Read and change an observation's workflow state.
   * - :doc:`client.attachment <attachment>`
     - Upload, list and download files attached to programs and observations.
   * - :doc:`client.scheduler <scheduler>`
     - Fetch the data the Gemini scheduler needs.
   * - :doc:`client.atom <atom>`
     - Fetch atom digests for the scheduler.
   * - :doc:`client.goats <goats>`
     - Run the queries built for GOATS.
   * - :doc:`client.site_status <site-status>`
     - Read the status of Gemini North or South.

.. toctree::
   :maxdepth: 1
   :hidden:

   program
   observation
   target
   workflow-state
   attachment
   scheduler
   atom
   goats
   site-status
