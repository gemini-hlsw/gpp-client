Coding standards
================

This page lists the rules that a reviewer checks. It doesn't repeat lint,
format, and docstring style, because the commit hooks enforce them, as
described in :doc:`setup`.

Generated code
--------------

- Change GraphQL by editing the ``.graphql`` files under
  ``graphql/operations/`` and rebuilding. Never edit
  ``src/gpp_client/generated/`` by hand.
- Commit the regenerated code in the same change as the operation or schema
  change behind it.

Tests
-----

- Tests run offline, so mock every GPP and REST call.
- Tests get environment differences from fixture schemas, built with
  ``tests/gpp_client/fixture_build.py``, never from the committed schemas.
  What's environment-specific in the committed schemas changes whenever GPP
  promotes something. The Environment Independence Check, described in
  :doc:`ci-checks`, catches a test that breaks this rule.
- A test may read the committed schemas when it asserts the same thing on every
  environment, because then it passes on any schemas. The test in
  ``tests/gpp_client/client/test_every_operation.py`` shows the pattern.
