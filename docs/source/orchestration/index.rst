Orchestration Layer
===================

The orchestration layer sits above the manager layer and provides
service-level workflows that combine multiple GraphQL operations into a
single, unified interface.

This layer introduces two key concepts:

- **Directors** — service-level entry points (e.g., ``scheduler`` and ``goats``)
  that organize workflows by domain.
- **Coordinators** — components that combine multiple managers to assemble
  higher-level payloads that cannot be retrieved with a single GraphQL call.

Purpose
-------

The ODB and GPP APIs intentionally limit the amount of information returned
per query. Many operations—such as reconstructing a full scheduler summary or
assembling GOATS-specific observation payloads—require multiple managers to be
queried together.

The orchestration layer provides these multi-step workflows in a structured
and reusable form.

When to Use This Layer
----------------------

Use the orchestration layer when:

- A workflow spans multiple GPP resources.
- The data you need cannot be fetched with a single operation.
- A service (Scheduler, GOATS, etc.) needs a transformed or enriched payload.
- You want a stable, high-level API for downstream applications.

Relationship to Other Layers
----------------------------

.. code-block:: text

    GPPClient
      └── Managers
            └── Direct Manager for a single resource
      └── Orchestration Layer
            ├── Directors (service namespaces)
            └── Coordinators (multi-manager workflows)

Contents
--------

.. toctree::
   :maxdepth: 1

   director
   coordinator
   scheduler
   goats