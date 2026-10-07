Use the domains
===============

Most of what you'll do with the client goes through a *domain*, which groups
the methods for one area of GPP. You reach each domain as an attribute of the
client, such as ``client.program``, ``client.observation`` or
``client.target``. For every domain and what it covers, see
:doc:`../domains/index`.

Get one item
------------

To get one item, pass its ID to ``get_by_id``. Some domains also let you look
an item up by reference, with ``get_by_reference``:

.. code-block:: python

   result = await client.program.get_by_id("p-10a")
   if result.program is not None:
       print(result.program.name)
   # Galaxy survey

Each method returns a model that the client generates from GPP's schema. The
item sits in a field of that model named after it, such as
``result.program``. If no item has that ID, or your token can't see it, the
field is ``None``, so check it before you use it.

Your editor knows each model's fields, so it can complete them and flag a
field that doesn't exist.

Find items with a filter
------------------------

To find several items, call ``get_all``. The ``where`` argument takes a filter
input, and ``limit`` caps how many items come back:

.. code-block:: python

   from gpp_client.generated.input_types import (
       WhereString,
       WhereTarget,
   )

   result = await client.target.get_all(
       where=WhereTarget(name=WhereString(like="NGC%")),
       limit=10,
   )
   for target in result.targets.matches:
       print(target.id, target.name)
   print(result.targets.has_more)

The items are in ``matches``, and ``has_more`` tells you whether more items
match than ``limit`` returned. To get every match, page through the results
with ``offset``, as :doc:`../domains/program` shows.

Filters and other inputs live in ``gpp_client.generated.input_types``. Each
filter is named ``Where`` followed by the item, such as ``WhereProgram`` or
``WhereObservation``.

Change an item
--------------

The methods that change data are named for what they do, such as
``create``, ``update_by_id``, ``delete_by_id`` and ``restore_by_id``. To change
an item, pass an input with only the fields you want to set:

.. warning::

   This call changes data in GPP. Try it on development first, as described
   in :ref:`try-on-development`.

.. code-block:: python

   from gpp_client.generated.input_types import (
       ObservationPropertiesInput,
   )

   result = await client.observation.update_by_id(
       "o-1a2",
       properties=ObservationPropertiesInput(subtitle="Second visit"),
   )

The client sends only the fields you set, so the rest of the item stays as it
was. Deleting an item marks it deleted rather than removing it, so
``restore_by_id`` can bring it back. To include deleted items in a lookup, pass
``include_deleted=True``.

When no method fits
-------------------

The domains cover the common tasks, but not everything GPP offers. When you
need a field that a domain method doesn't return, or a query no domain has,
write a custom query, as described in :doc:`custom-queries`.
