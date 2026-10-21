Documentation Process
=====================

The **gpp-client** documentation is built using:

- **Sphinx** for documentation generation
- **Read the Docs** for hosting and versioned builds
- **autodoc / autosummary** for API reference generation
- **ariadne-codegen** output for GraphQL models and input types

Documentation is automatically generated from both handwritten code and
generated sources.

Read the Docs
-------------

Documentation is built and published automatically by **Read the Docs**.

Builds are triggered when:

- Version tags are created
- Pull requests are opened (preview builds)

Read the Docs provides separate builds for:

- ``stable`` (the newest release)
- ``latest`` (the main branch)
- Tagged releases
- Pull request previews

The ``latest`` build shows a banner saying that it follows the main branch,
which may be ahead of the newest release.
These banners are configured dynamically in ``conf.py`` using environment
variables provided by Read the Docs.

Building Documentation Locally
------------------------------

Developers should build the documentation locally when making changes to public
APIs or documentation content.

To build the documentation locally with live reload enabled:

.. code-block:: console

   uv run --group docs sphinx-autobuild docs/source docs/build

This command will:

- Install documentation dependencies using the ``docs`` dependency group
- Build the documentation
- Start a local web server
- Automatically rebuild documentation when files change

Once running, open the following URL in a browser:

.. code-block:: text

   http://127.0.0.1:8000

Warnings During Builds
~~~~~~~~~~~~~~~~~~~~~~

The documentation builds without warnings, and it should stay that way, because
a warning usually means a broken reference. Before you open a pull request
that changes the docs or a public API, build once with warnings treated as
errors:

.. code-block:: console

   uv run --group docs sphinx-build -W -b html docs/source docs/build

If the build fails, fix the reference or markup that the warning names.

