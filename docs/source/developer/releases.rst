Releases
========

The project uses Calendar Versioning (CalVer).

Version format:

``YY.MM.PATCH``

Examples:

- ``26.5.0``
- ``26.5.1``

Every release reaches both environments, so there are no pre-releases, and the
release workflow refuses a tag such as ``v26.5.0.dev1``.

Version Source
--------------

The project uses dynamic versioning through Git tags.

The package version is derived directly from the release tag during the build
process.

Examples:

- Git tag ``v26.5.0`` produces package version ``26.5.0``

Version values are not manually updated in ``pyproject.toml``.

Creating a Release
------------------

All releases are created through the ``Create Release`` GitHub Actions workflow.

Release tag example:

.. code-block:: text

   v26.5.0

To create a release:

1. Open the GitHub Actions tab.
2. Run the ``Create Release`` workflow.
3. Enter the desired release tag.
4. Wait for validation, tests, build, and smoke tests to complete.
5. Review the generated draft GitHub release.
6. Publish the GitHub release.

Publishing the GitHub release automatically triggers the PyPI publish workflow.

Once the publish workflow completes successfully, the release becomes available on
PyPI:

- https://pypi.org/project/gpp-client/

The published package version is derived directly from the Git tag used during
the release workflow.