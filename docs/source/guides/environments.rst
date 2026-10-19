Select an environment
=====================

GPP has two environments: ``production``, where real programs live, and
``development``, where GPP tries changes first. One install of the client
works with both: you pick the environment when you build a client, and every
call goes to that environment, as it receives it.

Development gets GPP's changes days or weeks before production does, so the
two schemas differ most days. The client is built from both. Its names and
shapes are development's, so code written against development keeps working
after GPP promotes a change to production. The reference pages show that
view; ``client.is_available`` and ``client.enum_values``, below, say what the
selected environment has.

.. _choosing-the-environment:

Set it for one client or for all
--------------------------------

The client uses ``production`` unless you select another environment. To
select one for a single client, pass ``environment=``:

.. code-block:: python

   from gpp_client import GPPClient

   async with GPPClient(
       environment="development",
   ) as client:
       result = await client.program.get_all(limit=5)
       for program in result.programs.matches:
           print(program.id, program.name)
   # p-10a Galaxy survey
   # p-10b Hot Jupiter transits

To select one for every client, set ``GPP_ENVIRONMENT`` in the shell instead:

.. code-block:: bash

   export GPP_ENVIRONMENT=development

Environment names aren't case sensitive. If you pass a name the client doesn't
recognize, it raises ``GPPClientError``, and the message lists the valid names.

To check which environment a client uses, read ``client.settings.environment``.
The client also logs the environment and its URL at INFO level when it starts.
To see that log line, pass ``debug=True`` or set up Python ``logging``.

.. _environment-on-the-command-line:

Set it on the command line
--------------------------

To select the environment for one command only, put ``--env`` before the
command:

.. code-block:: bash

   gpp --env development program list

To store a default for every command on this machine, run
``gpp set-default-env``, which writes the default to the configuration file:

.. code-block:: bash

   gpp set-default-env development

If the configuration file doesn't exist yet, ``set-default-env`` creates it. If
the file exists, the command keeps your comments and other settings, but it
won't change a file that isn't valid TOML, or one whose ``environment`` is
anything other than a single name such as ``"development"``. Only the ``gpp``
command reads the stored default. In Python, pass ``environment=`` or set
``GPP_ENVIRONMENT``.

Use both environments at once
-----------------------------

Two clients on different environments can run side by side:

.. code-block:: python

   from gpp_client import GPPClient

   async with (
       GPPClient(environment="production") as prod,
       GPPClient(environment="development") as dev,
   ):
       prod_result = await prod.program.get_all(limit=5)
       dev_result = await dev.program.get_all(limit=5)
       print(len(prod_result.programs.matches))
       print(len(dev_result.programs.matches))
   # 5
   # 5

Set a token for each environment
--------------------------------

Each environment has its own token, which you get from Explore, GPP's web
app, in that environment: https://explore.gemini.edu/ for production and
https://explore-dev.lucuma.xyz/ for development. The client reads the production token from
``GPP_TOKEN`` and the development token from ``GPP_DEVELOPMENT_TOKEN``, so a
development client never reads ``GPP_TOKEN``:

.. code-block:: bash

   export GPP_TOKEN=...
   export GPP_DEVELOPMENT_TOKEN=...

If the selected environment has no token, the client raises ``GPPAuthError``,
and the message names the variable to set. To pass a token in code, or to keep
both tokens in a ``.env`` file, see :doc:`configuration`.

.. _fields-the-environment-lacks:

Fields the environment lacks read ``None``
------------------------------------------

A result model has a field for everything either environment returns. When
the selected environment lacks a field, the client doesn't ask for it, and the
field is ``None`` in the result. That's the same ``None`` as a value GPP left
empty, so when it matters which, ask ``client.is_available``. It answers for
the client's environment, from a table the client was built with, without a
network call:

.. code-block:: python

   result = await client.program.get_by_id("p-10a")
   program = result.program
   if program is not None and program.name is None:
       if client.is_available(program, "name"):
           print("The program has no name.")
       else:
           print("This environment has no Program.name field.")

Pass a model instance or its class, and the field's attribute name. For a
field the model doesn't have at all, ``is_available`` raises
``AttributeError``. Outside a client, ``gpp_client.is_available`` takes the
environment as a third argument.

A field whose type differs between the environments has production's type in
the client, and reads ``None`` on development until the promotion;
``is_available`` says so for that field.

Enum values the environment lacks
---------------------------------

A generated enum carries every value either environment knows. To list the
values the selected environment accepts, for a dropdown or a check before
sending, call ``client.enum_values``:

.. code-block:: python

   from gpp_client.generated.enums import (
       ObservationWorkflowState,
   )

   for state in client.enum_values(ObservationWorkflowState):
       print(state.value)
   # INACTIVE
   # UNDEFINED
   # UNAPPROVED
   # DEFINED
   # READY
   # ONGOING
   # COMPLETED

A result can also hold a value that GPP added after your release was built;
it still parses, as :ref:`unknown-enum-values` describes.

Renamed types keep both names for a while
-----------------------------------------

When development renames an input type or an enum, the class carries
development's name, and production's current name works as an alias of the
same class until the promotion makes the names equal. The alias imports from
the same module and type-checks, and the first use on each line warns:

.. code-block:: text

   DeprecationWarning: GmosImagingVariantInput is deprecated: production will
   call it ImagingVariantInput at its next promotion; import
   ImagingVariantInput instead

Switch to the new name when you see the warning. The alias is dropped in the
first release after the promotion, and the release notes list it under
"Breaking".

Send a document as written
--------------------------

The client sends a domain method's or generated method's operation as the
selected environment receives it, without the fields and arguments the
environment lacks. A document you write yourself goes to GPP exactly as
written, whether through a custom query or through ``client.graphql.execute``,
as :doc:`custom-queries` shows. So a document that uses something the
environment lacks is refused by GPP, not by the client.

Errors that name the environment
--------------------------------

Two errors tell you that the selected environment can't take a call:

- ``NotAvailable`` is raised before anything is sent, when the environment
  lacks the whole operation. The message names the operation and the
  environments that have it.
- ``GPPGraphQLError`` is GPP's own answer, when a call sets an input field,
  argument or enum value the environment lacks, or your install is behind the
  server. The message names the environment.

For the full list, and how to read the messages, see :ref:`environment-errors`
and :ref:`server-errors`.
