Client
======

The main entry point for interacting with GPP.

This client manages:

- Transport and authentication
- Schema introspection
- Access to high-level, resource-specific managers for executing GraphQL queries and mutations

Each resource is exposed through a manager accessible via an attribute on the client. These managers encapsulate the logic for interacting with a specific part of the GPP API.

Available Managers
------------------

Each manager provides high-level, asynchronous methods such as ``create``, ``get_by_id``, ``get_batch``, and ``update_by_id``.

The following managers are accessible via ``GPPClient``:

- :attr:`~gpp_client.GPPClient.call_for_proposals` → :class:`~gpp_client.managers.call_for_proposals.CallForProposalsManager`
- :attr:`~gpp_client.GPPClient.program_note` → :class:`~gpp_client.managers.program_note.ProgramNoteManager`
- :attr:`~gpp_client.GPPClient.program` → :class:`~gpp_client.managers.program.ProgramManager`
- :attr:`~gpp_client.GPPClient.target` → :class:`~gpp_client.managers.target.TargetManager`
- :attr:`~gpp_client.GPPClient.observation` → :class:`~gpp_client.managers.observation.ObservationManager`
- :attr:`~gpp_client.GPPClient.site_status` → :class:`~gpp_client.managers.site_status.SiteStatusManager`
- :attr:`~gpp_client.GPPClient.configuration_request` → :class:`~gpp_client.managers.configuration_request.ConfigurationRequestManager`
- :attr:`~gpp_client.GPPClient.group` → :class:`~gpp_client.managers.group.GroupManager`
- - :attr:`~gpp_client.GPPClient.workflow_state` → :class:`~gpp_client.managers.workflow_state.WorkflowStateManager`
- *(more managers to be added as the client evolves)*

Example
-------

.. code-block:: python

    from gpp_client import GPPClient

    client = GPPClient(
        url="https://gpp.example.org/graphql",
        token="abc123"
    )

    note = await client.program_note.create(
        title="Night Log",
        text="Clear skies. Everything worked as expected.",
        program_id="p-123"
    )

    fetched = await client.program_note.get_by_id(resource_id=note["id"])

.. note::

   For more information on how credentials are resolved, see :doc:`credentials`.

API Reference
-------------

.. autoclass:: gpp_client.GPPClient
   :members:
   :undoc-members:
   :show-inheritance:
