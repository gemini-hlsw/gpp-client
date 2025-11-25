Architecture
============

The GPP Client is organized into multiple layers, each with a distinct purpose.
This page provides a conceptual overview of the system's design, with an emphasis
on how responsibilities are distributed across components. It does *not* describe
how to call functions—only how the pieces fit together.

Layer Overview Diagram
----------------------

The following diagram shows the full stack:

.. code-block:: text

                          +---------------------------+
                          |       User Code           |
                          +---------------------------+
                                       |
                                       v
                          +---------------------------+
                          |        GPPClient          |
                          |  (high-level façade)      |
                          +---------------------------+
                                       |
                                       v
                          +---------------------------+
                          |   Directors & Coordinators|
                          | (service/domain workflows)|
                          +---------------------------+
                                       |
                                       v
                          +---------------------------+
                          |         Managers          |
                          | (resource-level logic)    |
                          +---------------------------+
                                       |
                                       v
                          +---------------------------+
                          |     Generated Operations  |
                          |  (GraphQL query/mutation) |
                          +---------------------------+
                                       |
                                       v
                          +---------------------------+
                          |        Transport          |
                          |   (HTTP, auth, headers)   |
                          +---------------------------+
                                       |
                                       v
                          +---------------------------+
                          |           GPP             |
                          +---------------------------+

GPP
---
At the bottom sits the GPP GraphQL API, which exposes all resources and
operations. The client communicates with GPP exclusively via this API.

Transport Layer
---------------

The transport layer is the foundation. It manages:

- HTTP connections
- Authentication headers
- Low-level request execution
- Error propagation at the protocol level

The transport implementation is intentionally minimal and generic. All other
components depend on it to communicate with the GPP GraphQL endpoint.

Generated API Layer
-------------------

Above the transport layer sits the code-generated GraphQL operations. These are
created by ``ariadne-codegen`` and provide:

- Strongly typed representations of queries and mutations
- Typed Python models for GraphQL results
- A stable interface corresponding directly to the GPP schema

It mirrors the GraphQL schema exactly
and is regenerated as the schema evolves.

Manager Layer
-------------

Managers provide the first level of abstraction **above the raw generated
operations**. Each manager corresponds to a specific domain resource such as:

- Programs
- Targets
- Observations
- Program Notes
- Groups
- Configuration Requests

Managers are responsible for:

- Selecting the correct GraphQL operation to call
- Normalizing error handling into consistent GPP exceptions
- Providing resource-level convenience methods (create, read, batch, update)
- Exposing asynchronous Pythonic interfaces

Managers do not combine multiple resources or reshape payloads into another
service's expected format. They represent “one resource at a time.”

Director and Coordinator Layer
-------------------------------

Some services (e.g., ``Scheduler``, ``GOATS``) require complex workflows that involve
multiple resources, service-specific queries, and structured payloads that do
not map directly to any single GraphQL operation. The ODB deliberately limits
how much data each endpoint returns, so reconstruction of a service-level view
requires composition.

This architectural need is addressed by **Directors** and **Coordinators**.

Purpose of Directors
~~~~~~~~~~~~~~~~~~~~

A *Director* provides access to a set of domain-specific workflows for a given
service. It organizes higher-level operations under separate namespaces, such as:

- ``scheduler``
- ``goats``

Directors:

- Do not execute queries directly
- Do not contain resource-level logic
- Provide a façade to a group of Coordinators

Purpose of Coordinators
~~~~~~~~~~~~~~~~~~~~~~~

A *Coordinator* performs the actual orchestration. It may:

- Combine multiple manager calls
- Invoke service-specific GraphQL helpers
- Reconstruct domain-specific data structures
- Validate and normalize payloads beyond the ODB's defaults

Coordinators encapsulate all logic needed to express workflows that cannot be
handled by a single manager or operation.

Directors/Coordinators vs. Managers
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Managers operate at the **resource level**:

- one GraphQL operation at a time
- one type of resource (e.g., program, target)
- one payload format

Coordinators operate at the **service or workflow level**:

- multiple GraphQL calls across managers
- service-specific transformations
- domain-oriented results (GOATS-specific payloads, Scheduler summaries, etc.)

Directors and coordinators are therefore positioned **above managers** in the
architecture.

Director Layer Diagram
~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: text

                      +---------------------------+
                      |      Directors            |
                      |  (per service namespace)  |
                      +---------------------------+
                                   |
                                   v
                      +---------------------------+
                      |      Coordinators         |
                      | (compose manager outputs) |
                      +---------------------------+


High-Level Client Layer
-----------------------

At the top sits the :class:`~gpp_client.GPPClient`, which provides:

- Entry points for resource managers
- Entry points for service-specific directors
- Credential resolution
- Environment selection
- Transport initialization
- Configuration integration

The client itself does not contain resource or orchestration logic; it delegates
to managers and directors.

Extending the Architecture
--------------------------

The layered design supports safe extension:

- Add a new **manager** when a new resource category exists in GraphQL.
- Add a new **coordinator** when reconstruction requires multiple resources.
- Add a new **director** when a domain namespace requires multiple coordinated workflows.
- Add new **generated operations** whenever the schema changes.

This ensures clear boundaries between GraphQL schema concerns, resource-level
interfaces, and service-level workflows.