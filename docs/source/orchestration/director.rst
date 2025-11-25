Directors
=========

Directors provide service-level workflows that combine multiple managers into a
single, unified interface. While managers operate on individual GraphQL
resources (programs, observations, targets, etc.), directors operate at the
domain level—such as ``scheduler`` or ``goats``—and expose workflows that
cannot be expressed through a single GraphQL call.

Concept
-------

The ODB and GPP APIs intentionally limit the amount of information that any one
query can return. Reconstructing a complete service-level view (e.g., a
scheduler program summary, or a GOATS observation payload) therefore requires
multiple queries coordinated together.

A **director** organizes these multi-step operations under a dedicated namespace.

Directors delegate the actual composition work to **coordinators**, which
encapsulate the service-specific logic. Each director owns one or more
coordinators.

Relationship to Managers
-------------------------

Directors do *not* replace managers. Instead:

- Managers handle **single-resource** interactions.
- Coordinators combine **multiple managers**.
- Directors group **coordinators by service**.

This forms the top tier of the client architecture.

Example structure:

.. code-block:: text

    GPPDirector
      ├── scheduler
      │     ├── ProgramCoordinator
      │     └── ObservationCoordinator
      └── goats
            ├── ProgramCoordinator
            └── ObservationCoordinator

Using a Director
-----------------

Directors are accessed through :class:`gpp_client.GPPClient` and provide
service-oriented namespaces:

.. code-block:: python

    from gpp_client import GPPClient, GPPDirector

    client = GPPClient()
    director = GPPDirector(client)

    program_data = await director.scheduler.program.get_all()

A matching CLI namespace is also available:

.. code-block:: bash

    gpp sched program list

API Reference
-------------
.. automodule:: gpp_client.director
   :members:
   :undoc-members:
   :inherited-members:
   :show-inheritance: