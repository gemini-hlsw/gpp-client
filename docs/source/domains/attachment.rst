Attachment
==========

The attachment domain provides access to program and observation attachments.

Use :attr:`~gpp_client.GPPClient.attachment` to:

- Upload attachments to a program
- Update or delete attachments
- Download attachment content
- List attachments for programs and observations

Quick Example
-------------

.. code-block:: python

   from pathlib import Path
   from gpp_client import GPPClient
   from gpp_client.generated import AttachmentType

   async with GPPClient() as client:
      attachment_id = await client.attachment.upload(
         program_id="p-123",
         attachment_type=AttachmentType.FINDER,
         file_name="finder.png",
         file_path=Path("finder.png"),
      )

      saved_path = await client.attachment.download_by_id(
         attachment_id,
         save_to="~/Downloads",
      )

Upload
------

Upload a new attachment for a program:

.. code-block:: python

   attachment_id = await client.attachment.upload(
      program_id="p-123",
      attachment_type=AttachmentType.FINDER,
      file_name="finder.png",
      file_path="finder.png",
   )

Provide exactly one of:

- ``file_path``
- ``content``

.. warning::

   Exactly one of ``file_path`` or ``content`` must be provided.


Update and Delete
-----------------

Update an existing attachment:

.. code-block:: python

   await client.attachment.update_by_id(
      attachment_id="a-123",
      file_name="updated-finder.png",
      file_path="updated-finder.png",
   )

Delete an attachment:

.. code-block:: python

   await client.attachment.delete_by_id("a-123")


Download
--------

Download an attachment by ID:

.. code-block:: python

   path = await client.attachment.download_by_id(
      attachment_id="a-123",
      save_to="~/Downloads",
      overwrite=False,
   )

If ``save_to`` is omitted, the file is downloaded to the user's home directory.

.. tip::

   Use ``overwrite=True`` to replace an existing local file.


Listing Attachments
-------------------

List attachments by observation ID:

.. code-block:: python

   result = await client.attachment.get_all_by_observation_id("o-123")

List attachments by observation reference:

.. code-block:: python

   result = await client.attachment.get_all_by_observation_reference("GN-2026A-Q-1-1")

List attachments by program ID:

.. code-block:: python

   result = await client.attachment.get_all_by_program_id("p-123")

List attachments by program reference:

.. code-block:: python

   result = await client.attachment.get_all_by_program_reference("GN-2026A-Q-1")

List attachments by proposal reference:

.. code-block:: python

   result = await client.attachment.get_all_by_proposal_reference("GN-2026A-Q-1")


Notes
-----

Attachment operations use both REST and GraphQL:

- Upload, update, delete, and download use REST endpoints
- Listing attachments uses GraphQL queries

Download uses a presigned URL returned by the service.

API Reference
-------------

.. autoclass:: gpp_client.domains.attachment.AttachmentDomain
   :members:
   :undoc-members: