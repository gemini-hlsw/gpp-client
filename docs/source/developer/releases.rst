Releases
========

The :ref:`versions-and-upgrades` page describes what a release promises users:
one stream, one install for every environment, and how often to upgrade. This
page shows how to make a release.

Version numbers
---------------

Versions follow calendar versioning: ``YY.M.PATCH``, with the month written
without a leading zero, such as ``26.5.0`` or ``26.10.1``. The version comes
from the git tag, so tag ``v26.5.0`` builds version ``26.5.0``. Never write a
version into ``pyproject.toml``.

Every release reaches every environment, so there's a single release stream.

Make the release
----------------

1. Check the release locally, on an up-to-date ``main`` with every tag:

   .. code-block:: bash

      git switch main
      git fetch --tags origin
      git merge --ff-only origin/main
      uv run --group codegen python -m scripts.validate_release v26.5.0

   The check fails on a tag that isn't ``vYY.M.PATCH``. It also fails when the
   merged schema, the generated code, or ``llms.txt`` differs from a fresh
   build, and it lists those files. In that case, rebuild and commit, as
   described in :doc:`updating-the-schema`. The ariadne-codegen deprecation
   warnings that it prints are expected.

2. In GitHub, open Actions, then Create Release, then Run workflow. Choose the
   ``main`` branch and enter the tag, such as ``v26.5.0``.

   The workflow checks the tag, runs Ruff and the tests, then builds and
   smoke-tests the package. Then it pushes the tag and creates a draft release
   with GitHub's generated notes.

3. Print what changed on development and production since the previous
   release tag, as Markdown:

   .. code-block:: bash

      uv run --group codegen python -m scripts.release_notes v26.4.0

   Paste the output at the top of the draft's notes.

4. Publish the draft. Publishing runs Upload Python Package, which builds the
   package from the tag, smoke-tests it, and publishes it to PyPI:

   https://pypi.org/project/gpp-client/
