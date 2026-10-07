Upload and download attachments
===============================

An attachment is a file stored with a program in GPP, such as a finder chart
or a science justification. The ``client.attachment`` domain uploads, lists
and downloads attachments.

Upload a file
-------------

To upload a file, give the program, the attachment type and the name that GPP
stores the file under. Then send the contents, either from a file with
``file_path=`` or as bytes with ``content=``. If you pass both, or neither, the
client raises ``GPPValidationError``. The ``attachment_type`` argument takes an
``AttachmentType``, listed in :doc:`../graphql-api/enums`.

.. warning::

   This call changes data in GPP. Try it on development first, as described
   in :ref:`try-on-development`.

This example uploads a finder chart and then downloads it again:

.. code-block:: python

   from gpp_client.generated.enums import (
       AttachmentType,
   )

   attachment_id = await client.attachment.upload(
       "p-10a",
       attachment_type=AttachmentType.FINDER,
       file_name="finder.png",
       file_path="charts/finder.png",
       description="Finder chart",
   )
   path = await client.attachment.download_by_id(
       attachment_id,
       save_to="downloads",
   )
   print(path)
   # for example: downloads/finder.png

The ``upload`` method returns the new attachment's ID, which the example uses
to download the file.

Download a file
---------------

The ``download_by_id`` method saves the file in the ``save_to=`` folder, under
the file name in GPP's download URL, and returns the file's path. It creates
the folder if it's missing. Without ``save_to=``, the file goes to your home
folder.

If the file already exists, ``download_by_id`` raises ``GPPClientError``. To
replace an existing file, pass ``overwrite=True``. To fetch the file yourself,
call ``get_download_url_by_id``, which returns a presigned download URL.

List attachments
----------------

You can list a program's attachments by program ID, as in this example, or by
program or proposal reference:

.. code-block:: python

   result = await (
       client.attachment.get_all_by_program_id("p-10a")
   )
   if result.program is not None:
       for item in result.program.attachments:
           print(
               item.id,
               item.file_name,
               item.attachment_type,
           )
   # a-2b finder.png AttachmentType.FINDER

Observations have the same methods, ``get_all_by_observation_id`` and
``get_all_by_observation_reference``.

Replace or delete a file
------------------------

To replace a file, call ``update_by_id``, which needs ``file_name=``. To
remove a file, call ``delete_by_id``:

.. code-block:: python

   await client.attachment.update_by_id(
       "a-2b",
       file_name="finder-v2.png",
       file_path="charts/finder-v2.png",
   )
   await client.attachment.delete_by_id("a-2b")

When GPP refuses an upload, download, update or delete, the client raises
``GPPResponseError``. Its ``status_code`` and ``message`` say why. For the
other errors, see :doc:`errors`.

From the command line, ``gpp attachment`` lists attachments. For its options,
see :doc:`../cli/attachment`.
