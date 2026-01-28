Client
======

The main entry point for interacting with the GPP GraphQL API.

The :class:`~gpp_client.GPPClient` class manages:

- Transport and authentication
- Environment and credential resolution
- Schema introspection
- Access to high-level, resource-specific managers for executing GraphQL queries and mutations

Each resource is exposed through a manager accessible as an attribute on the client.  
These managers encapsulate the GraphQL operations for their domain and provide
asynchronous methods such as ``create``, ``get_by_id``, ``get_batch``, and ``update_by_id``.

.. note::

   All manager methods are asynchronous. Ensure calls run inside an event loop
   (for example using ``asyncio.run``).


Environment and Credential Resolution
-------------------------------------

The client resolves connection details automatically using a strict priority order:

1. Explicit parameters (``env=``, ``token=``)
2. Environment variables (e.g., ``GPP_PRODUCTION_TOKEN``, ``GPP_DEVELOPMENT_TOKEN``)
3. Local configuration file (``~/.config/gpp-client/config.toml``)
4. The default environment (``PRODUCTION``)

This ensures you can write:

.. code-block:: python

    client = GPPClient()

and the client will automatically select the active environment and token.

.. note::

   For advanced credential setup—including disabling environment variable resolution,
   configuring per-environment tokens, and managing the active environment—see
   :doc:`configuration/index`.


Available Managers
~~~~~~~~~~~~~~~~~~

The following managers are available as attributes on the client:

- :attr:`~gpp_client.GPPClient.call_for_proposals` → :class:`~gpp_client.managers.call_for_proposals.CallForProposalsManager`
- :attr:`~gpp_client.GPPClient.program_note` → :class:`~gpp_client.managers.program_note.ProgramNoteManager`
- :attr:`~gpp_client.GPPClient.program` → :class:`~gpp_client.managers.program.ProgramManager`
- :attr:`~gpp_client.GPPClient.target` → :class:`~gpp_client.managers.target.TargetManager`
- :attr:`~gpp_client.GPPClient.observation` → :class:`~gpp_client.managers.observation.ObservationManager`
- :attr:`~gpp_client.GPPClient.site_status` → :class:`~gpp_client.managers.site_status.SiteStatusManager`
- :attr:`~gpp_client.GPPClient.configuration_request` → :class:`~gpp_client.managers.configuration_request.ConfigurationRequestManager`
- :attr:`~gpp_client.GPPClient.group` → :class:`~gpp_client.managers.group.GroupManager`
- :attr:`~gpp_client.GPPClient.workflow_state` → :class:`~gpp_client.managers.workflow_state.WorkflowStateManager`

.. note::

   ``SiteStatusManager`` does not use the GraphQL client and is initialized
   without a network connection.


Creating a Client
-----------------

By default, credentials and the active environment come from environment variables
or the local configuration file:

.. code-block:: python

    from gpp_client import GPPClient

    client = GPPClient()


Specify an environment explicitly:

.. code-block:: python

    client = GPPClient(env="DEVELOPMENT")

or with the enum:

.. code-block:: python

    from gpp_client.config import GPPEnvironment
    client = GPPClient(env=GPPEnvironment.STAGING)


Pass an explicit token:

.. code-block:: python

    client = GPPClient(
        env="DEVELOPMENT",
        token="my-token"
    )


Storing Credentials
-------------------

Use :meth:`~gpp_client.GPPClient.set_credentials` to store tokens locally:

.. code-block:: python

    from gpp_client import GPPClient
    from gpp_client.config import GPPEnvironment

    GPPClient.set_credentials(
        env=GPPEnvironment.DEVELOPMENT,
        token="my-dev-token",
        activate=True,
    )

or by passing in the :class:`~gpp_client.config.GPPConfig` instance when creating the client:

.. code-block:: python

    from gpp_client import GPPClient
    from gpp_client.config import GPPConfig, GPPEnvironment

    config = GPPConfig()
    config.set_credentials(
        env=GPPEnvironment.DEVELOPMENT,
        token="my-dev-token",
        activate=True,
    )
    config.save_to_file()

    client = GPPClient(config=config)

.. note::

   For advanced credential setup—including disabling environment variable resolution,
   configuring per-environment tokens, and managing the active environment—see
   :doc:`configuration/index`.


Checking Connectivity
---------------------

Use :meth:`~gpp_client.GPPClient.is_reachable` to verify the endpoint and token:

.. code-block:: python

    ok, error = await client.is_reachable()
    if ok:
        print("Connected.")
    else:
        print("Failed:", error)


API Reference
-------------

.. autoclass:: gpp_client.GPPClient
   :members:
   :undoc-members:
   :show-inheritance: