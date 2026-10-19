Contributing
============

Report a bug or ask for a feature
---------------------------------

To report a bug or ask for a feature, file a ticket on the GPC board in Jira:

https://noirlab.atlassian.net/jira/software/projects/GPC/boards/162

You can also ask in ``#gpp-client`` on NOIRLab Slack. Please don't file GitHub
issues, because we track the work in Jira.

Contribute code
---------------

A change goes from a fresh checkout to a pull request in these steps:

1. Set up a checkout, as described in :doc:`setup`.
2. Make a branch. The commit hooks refuse a commit on ``main``:

   .. code-block:: bash

      git switch -c <branch-name>

3. Make your change, following the :doc:`coding-standards`. To add or change a
   call, follow :doc:`adding-a-call`. To bring in GPP's latest schema, follow
   :doc:`updating-the-schema`. To understand the generated code, read
   :doc:`how-the-client-is-built`.
4. Run the checks described in :doc:`ci-checks`.
5. Update the docs, following :doc:`documentation`.
6. Open a pull request against ``main``, as described in :doc:`pull-requests`.

To publish a new version, follow :doc:`releases`.

.. toctree::
   :hidden:

   setup
   coding-standards
   adding-a-call
   how-the-client-is-built
   updating-the-schema
   ci-checks
   documentation
   pull-requests
   releases
