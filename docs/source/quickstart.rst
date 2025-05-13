Quickstart
==========

Get up and running with the GPP Python Client in minutes.

Installation
------------

Install the package using ``pip``:

.. code-block:: bash

    pip install gpp-client

Requirements:

- ``python>=3.10``
- ``toml``
- ``typer``
- ``ariadne-codegen``

Basic Usage
-----------

.. code-block:: python

    from gpp_client import GPPClient

    # Initialize with your GraphQL endpoint and credentials.
    client = GPPClient(url="YOUR_URL", token="YOUR_TOKEN")

    # List the first 5 program notes.
    notes = await client.program_note.get_all(limit=5)
    for note in notes["matches"]:
        print(f"{note['id']}: {note['title']}")

    # Create a new note from a JSON file.
    new_note = await client.program_note.create(
        from_json="path/to/program_note_payload.json",
        program_id="p-123"
    )
    print("Created:", new_note)

    # Or create a note from the pydantic model.
    from gpp_client.api.enums import Existence
    from gpp_client.api.input_types import ProgramNotePropertiesInput

    properties = ProgramNotePropertiesInput(
        title="Example",
        text="This is an example.",
        is_private=False,
        existence=Existence.PRESENT
    )
    another_note = await client.program_note.create(properties=properties, program_id="p-123")

    print("Created another:", another_note)

Command Line Usage
------------------

Use the CLI to interact with GPP resources directly from the terminal.

.. code-block:: bash

    # Get help.
    gpp --help

    # Get observation help.
    gpp obs --help

    # List observations.
    gpp obs list --limit 3

    # Get details for one.
    gpp obs get o-123

    # Create via JSON.
    gpp obs create --from-json new_obs.json --program-id p-123

    # Update by ID via JSON.
    gpp obs update --observation-id o-123 --from-json updated_obs.json

Next Steps
----------

- See :doc:`client` for more on the `GPPClient` and how to authenticate.
- Learn how to configure the client using TOML settings in :doc:`config`.
- Understand how to pass or store API credentials in :doc:`credentials`.
- Browse :doc:`managers/index` for full details on available managers and supported operations.
- Use :doc:`cli/index` for CLI command documentation.