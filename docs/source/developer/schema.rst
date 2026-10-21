Schema Management
=================

The GPP Client depends on the GPP GraphQL schema of each environment. The
committed schemas in ``graphql/schemas/`` must stay current so the generated
models, enums, input types, and operations match what GPP serves.

Downloading the Schemas
-----------------------

To download both schemas:

.. code-block:: bash

   uv run --group schema python -m scripts.download_schema

Pass ``development`` or ``production`` to download only that environment.
Introspection is anonymous. If a server refuses it, the script retries with the
environment's token, so set ``GPP_DEVELOPMENT_TOKEN`` or ``GPP_TOKEN``.

Each downloaded file starts with a comment line that gives the GPP commit the
server reported at ``/health``. The build records that commit, so error
messages can name it. If the server's commit changes during the download, the
script stops, and you should run it again.

After downloading the schemas, rebuild the client as described in
:doc:`codegen`.
