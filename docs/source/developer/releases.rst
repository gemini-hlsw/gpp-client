Releases
========

The :ref:`versions-and-upgrades` page describes what a release promises users:
one stream, one install for every environment, and how often to upgrade. This
page shows how to make a release. Releases are made by hand. A job that
releases on a schedule is planned, but it isn't built yet, so every step below
is yours to run.

Version numbers
---------------

Versions follow calendar versioning: ``YY.M.PATCH``, with the month written
without a leading zero, such as ``26.5.0`` or ``26.10.1``. The version comes
from the git tag, so tag ``v26.5.0`` builds version ``26.5.0``. Never write a
version into ``pyproject.toml``.

On every build, including the editable install that ``uv sync`` makes, a
hatchling build hook writes the version into ``src/gpp_client/_version.py``.
That file is ignored by git, and ``gpp_client.__version__`` reads it. The
release check compares it with the tag, so a package can't carry a version
other than the one on its tag.

Every release reaches every environment, so there's a single release stream.

Make the release
----------------

1. Bring the client up to date with GPP by running the schema update, as
   :doc:`updating-the-schema` describes, and merge its pull request. Read the
   update's output: if it held an environment, keep that environment's name
   for the release notes.

2. Check the release locally, on an up-to-date ``main`` with every tag. The
   check wants the tag on the commit, so create it locally, check, and then
   delete it again, because the workflow creates the real one:

   .. code-block:: bash

      git switch main
      git fetch --tags origin
      git merge --ff-only origin/main
      git tag v26.5.0
      uv run --group codegen python -m scripts.validate_release v26.5.0
      git tag -d v26.5.0

   The check fails on a tag that isn't ``vYY.M.PATCH``. It fails when the
   baked version differs from the tag, which happens when the tag isn't on the
   commit yet or the package wasn't reinstalled after tagging; ``uv run``
   reinstalls it. It also fails when the generated code differs from a fresh
   build of the committed schemas, and then it lists those files. In that
   case, run the schema update and commit. The ariadne-codegen deprecation
   warnings that it prints are expected.

3. Preview the release notes. The generator compares each environment's
   committed schema with its copy at the previous release tag:

   .. code-block:: bash

      uv run --group codegen python -m scripts.release_notes v26.4.0

   The notes open with one line per environment, ``Production: changed`` or
   ``Production: unchanged`` and the same for development, so production
   users can skip a release that doesn't touch them. For each changed
   environment, a "Breaking" list holds what graphql-core's
   ``find_breaking_changes`` found, and an "Added or relaxed" list holds what
   ``find_dangerous_changes`` found. An "Aliases" list names each input type
   or enum that production still calls by an old name, which the generated
   code carries as an alias of development's name. When a promotion makes the
   names equal, the alias goes, and that's listed under production's
   "Breaking".

   If the schema update held an environment, pass its name, and the notes
   name it with the commit its schema is from:

   .. code-block:: bash

      uv run --group codegen python -m scripts.release_notes v26.4.0 --held development

4. In GitHub, open Actions, then Create Release, then Run workflow. Choose the
   ``main`` branch and enter the tag, such as ``v26.5.0``. If the schema
   update held an environment, enter its name in the "held" field.

   The workflow creates the tag locally, reinstalls the package so that the
   baked version comes from the tag, and runs the release check. Then it runs
   Ruff and the tests, builds and smoke-tests the package, pushes the tag, and
   creates a draft release. The draft's notes start with the generated notes
   from step 3, run against the nearest earlier ``v*`` tag, and GitHub's
   generated list of pull requests follows. When there's no previous tag, or
   it has no committed schemas, the draft has only GitHub's list.

5. Read the draft's notes. Add a line for anything the generated notes can't
   know, such as a domain method you changed by hand, and then publish the
   draft. Publishing runs Upload Python Package, which builds the package from
   the tag, smoke-tests it, and publishes it to PyPI:

   https://pypi.org/project/gpp-client/
