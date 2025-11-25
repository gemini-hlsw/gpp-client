Coordinators
============

Coordinators perform domain-level workflows that cannot be satisfied by a
single manager. They combine multiple queries, apply service-specific logic,
and return structured payloads tailored to a service's needs.

Purpose
-------

A coordinator exists whenever:

- Several managers must be queried together.
- Results must be merged or transformed into a domain-specific payload.
- Additional validation or reshaping is required beyond what GraphQL returns.
- Data from custom GPP operations must be combined with standard results.

Coordinators are always constructed and owned by a director, and they all share
the same configured :class:`gpp_client.GPPClient` instance.

Examples of Responsibilities
----------------------------

- Constructing GOATS-specific observation payloads.
- Reassembling scheduler summaries that require cross-resource lookups.
- Fetching derived fields not directly returned by a single GraphQL operation.
- Normalizing complex ODB structures for downstream applications.

Coordinators vs. Managers
-------------------------

Managers:

- Wrap a single GraphQL operation.
- Provide typed resource-level CRUD interfaces.

Coordinators:

- Combine managers.
- Run multi-step workflows.
- Produce service-specific outputs.

API Reference
-------------

.. automodule:: gpp_client.coordinator
   :members:
   :undoc-members:
   :inherited-members:
   :show-inheritance: