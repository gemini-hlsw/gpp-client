Pull requests
=============

Open pull requests against ``main``. The pull request template asks for a
summary, whether you updated the docs and the generated code, and whether the
change breaks the API or behavior. If there's a Jira ticket, name it in the
title, for example ``GPC-174: Fix Scheduler query``.

Before you push
---------------

Run the same checks that the pull request runs:

.. code-block:: bash

   uv run ruff check . && uv run ruff format --check .
   uv run ty check --error-on-warning src/gpp_client
   uv run pytest

If you changed an operation or a schema, commit the rebuilt files too. If you
changed behavior, update the page that describes it. For every check the pull
request runs, see :doc:`ci-checks`.

What to write
-------------

Write for the reviewer. Say what changes for users of the client, and point to
what needs a careful review and what they can skim, such as regenerated code.
GitHub collapses the generated code, the downloaded and merged schemas, and
``llms.txt`` in the diff, because ``.gitattributes`` marks them as generated.

For a schema update, paste the build's trim summary, as described in
:doc:`updating-the-schema`.

If the change breaks the API, tick the box in the template and say how users
should change their code.
