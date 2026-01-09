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

- ``stable`` (latest production release)
- ``latest`` (latest development release)
- Tagged releases (production and development)
- Pull request previews

The documentation UI may display a banner indicating whether the current build
corresponds to a stable release, a development release, or a pull request preview.
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

It is normal to see warnings during documentation builds.

Some warnings are unavoidable due to the structure of the project:

- Portions of the API are generated via **ariadne-codegen**
- Generated models reflect the upstream **GPP GraphQL schema**
- The schema is external and may introduce naming collisions or ambiguous
  references (for example, repeated fields named ``type``)

As a result:

- Certain Sphinx warnings (such as ambiguous cross-references) may appear
- These warnings do **not** indicate documentation breakage
- Builds are considered successful as long as Sphinx completes without errors

.. note::

   If you identify warnings that indicate genuine documentation problems,
   please address them or raise an issue for further investigation.

Developers should focus on resolving **errors** and clear documentation issues,
but warnings originating from generated code are expected and acceptable.

