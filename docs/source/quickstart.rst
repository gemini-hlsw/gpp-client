Quickstart
==========

This guide shows how to quickly use the ``GPPClient`` to interact with the Gemini Program Platform (GPP) GraphQL API for working with program notes.

A valid program is required to create or update notes, what we will be working with.

Getting Started
---------------

1. Initialize the Client
^^^^^^^^^^^^^^^^^^^^^^^^

.. code-block:: python

   from gpp_client import GPPClient

   client = GPPClient(
       url="https://gpp.example.org/graphql",
       token="your_api_token_here"
   )

.. note::

   You can also omit ``url`` and ``token`` if you’ve configured them via
   environment variables or a configuration file. See :doc:`credentials` for more information.

2. Fetch a Program Note by ID
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

.. code-block:: python

   note = await client.program_note.get_by_id(resource_id="id_here")
   print(note)

3. Create a New Program Note
^^^^^^^^^^^^^^^^^^^^^^^^^^^^

.. code-block:: python

   new_note = await client.program_note.create(
       title="Seeing conditions update",
       text="Observing under patchy clouds, seeing ~1.2\".",
       is_private=True,
       program_id="id_here"
   )

4. Update an Existing Note
^^^^^^^^^^^^^^^^^^^^^^^^^^

.. code-block:: python

   updated = await client.program_note.update_by_id(
       resource_id="id_here",
       title="Updated title",
       text="New note content."
   )

5. List All Notes in a Program
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

.. code-block:: python

   notes = await client.program_note.get_batch_by_program_id(program_id="id_here")
   for note in notes["programNotes"]["matches"]:
       print(note["title"])

6. Soft-Delete a Program Note
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

.. code-block:: python

   await client.program_note.delete_by_id(resource_id="id_here")

7. Restore a Deleted Note
^^^^^^^^^^^^^^^^^^^^^^^^^

.. code-block:: python

   await client.program_note.restore_by_id(resource_id="id_here")