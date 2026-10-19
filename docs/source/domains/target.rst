Target
======

The ``client.target`` domain reads and changes targets. To create a target in
a program, you can name the program by its ID, its program reference or its
proposal reference.

Get a target by ID
------------------

A sidereal target carries its coordinates in ``sidereal``. On any other kind
of target, ``sidereal`` is ``None``, so the example checks it first:

.. code-block:: python

   result = await client.target.get_by_id("t-3b4")
   target = result.target
   if target is not None:
       sidereal = target.sidereal
       if sidereal is not None:
           print(target.name)
           print(sidereal.ra.hms, sidereal.dec.dms)

The example prints the target's name. Then it prints the right ascension in
hours, minutes and seconds, and the declination in degrees, minutes and
seconds.

Clone a target
--------------

To copy a target, call ``clone``. The ``properties`` argument changes the
copy, and ``replace_in`` swaps the copy in for the original in the
observations you name.

.. warning::

   This call changes data in GPP. Try it on development first, as described
   in :ref:`try-on-development`.

This example clones a target under a new name and uses the copy in two
observations:

.. code-block:: python

   from gpp_client.generated.input_types import (
       TargetPropertiesInput,
   )

   copy = TargetPropertiesInput(name="NGC 1068 copy")
   result = await client.target.clone(
       "t-3b4",
       properties=copy,
       replace_in=["o-1a2", "o-1a3"],
   )
   print(result.clone_target.new_target.id)
   # t-3b5

API reference
-------------

.. autoclass:: gpp_client.domains.target.TargetDomain
   :members:
   :undoc-members:
