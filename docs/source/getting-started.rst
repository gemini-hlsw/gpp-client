Getting Started
===============

.. code-block:: bash

    pip install gpp-client

Requirements:

- ``python>=3.10``
- ``toml``
- ``typer``
- ``aiohttp``
- ``beautifulsoup4``
- ``httpx``
- ``graphql-core``
- ``websockets``


Basic Usage
-----------

The :class:`~gpp_client.GPPClient` automatically resolves:

1. The active GPP environment
2. The base URL for that environment
3. The authentication token

The available environments (``DEVELOPMENT``, ``STAGING``, ``PRODUCTION``) match
the corresponding GPP deployments. See :doc:`config` for details on configuring them.

Credential resolution follows a strict priority order:

1. Explicit arguments (``env=``, ``token=``)
2. Environment variables (for example ``GPP_PRODUCTION_TOKEN``)
3. Local TOML configuration file (``~/.config/gpp-client/config.toml``)
4. Defaults (``PRODUCTION``) environment.

Credentials are automatically loaded from environment variables or your local
configuration file. See :doc:`credentials` for a full explanation.

.. note::

   All GPPClient manager methods are ``async``. Make sure to call them inside
   an event loop (for example with ``asyncio.run``). See :doc:`client` for details.


Initializing the Client
~~~~~~~~~~~~~~~~~~~~~~~

By default, the client loads configuration from the local TOML config file and
environment variables.

.. code-block:: python

    from gpp_client import GPPClient
    # Use the active environment from config or environment variables.
    client = GPPClient()

Initialize a specific environment:

.. code-block:: python

    from gpp_client import GPPClient
    client = GPPClient(env="DEVELOPMENT")

or with the environment enum:

.. code-block:: python

    from gpp_client import GPPClient
    from gpp_client.config import GPPEnvironment
    client = GPPClient(env=GPPEnvironment.STAGING)

Initialize with an explicit token:

.. code-block:: python

    from gpp_client import GPPClient
    from gpp_client.config import GPPEnvironment
    client = GPPClient(env=GPPEnvironment.DEVELOPMENT, token="my-token")

You can create multiple clients if you need to query different environments:

.. code-block:: python

    from gpp_client import GPPClient
    from gpp_client.config import GPPEnvironment

    prod = GPPClient(env=GPPEnvironment.PRODUCTION)
    dev = GPPClient(env=GPPEnvironment.DEVELOPMENT)


Listing Program Notes
~~~~~~~~~~~~~~~~~~~~~

.. code-block:: python

    notes = await client.program_note.get_all(limit=5)
    for note in notes["matches"]:
        print(f"{note['id']}: {note['title']}")


Creating a Note from JSON
~~~~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: python

    new_note = await client.program_note.create(
        from_json="payloads/program_note.json",
        program_id="p-123",
    )
    print("Created:", new_note)


Creating a Note Using Pydantic Models
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: python

    from gpp_client.api.enums import Existence
    from gpp_client.api.input_types import ProgramNotePropertiesInput

    properties = ProgramNotePropertiesInput(
        title="Example",
        text="This is an example.",
        is_private=False,
        existence=Existence.PRESENT,
    )

    result = await client.program_note.create(
        properties=properties,
        program_id="p-123",
    )

    print("Created:", result)


Updating Credentials
--------------------

You can store and optionally activate a token for any environment.

.. code-block:: python

    from gpp_client import GPPClient
    from gpp_client.config import GPPEnvironment

    GPPClient.set_credentials(
        env=GPPEnvironment.DEVELOPMENT,
        token="my-dev-token",
        # Activate is True by default.
        activate=True,
    )


Checking Connectivity
---------------------

Use :meth:`~gpp_client.GPPClient.is_reachable` to verify the endpoint and token.

.. code-block:: python

    ok, error = await client.is_reachable()
    if ok:
        print("Connected successfully.")
    else:
        print("Failed:", error)


Command Line Usage
------------------

The package includes a rich CLI for interacting with GPP resources.

Show help:

.. code-block:: bash

    gpp --help


List observations:

.. code-block:: bash

    gpp obs list --limit 3


Get one observation:

.. code-block:: bash

    gpp obs get o-123


Create an observation from JSON:

.. code-block:: bash

    gpp obs create --from-json new_obs.json --program-id p-123


Update an observation from JSON:

.. code-block:: bash

    gpp obs update --observation-id o-123 --from-json updated_obs.json


Next Steps
----------

- See :doc:`client` for details on the client and how to use to communicate with different resources.
- See :doc:`config` for the TOML configuration file format.
- See :doc:`credentials` for environment variable conventions and resolving credentials.
- See :doc:`managers/index` for available resource managers.
- See :doc:`api/index` for available API types and enums to use with the client for requests and responses.
- See :doc:`cli/index` for full CLI documentation.