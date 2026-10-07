.. _versions-and-upgrades:

Upgrade the client
==================

GPP changes almost daily, and each client release matches GPP on its release
day. So upgrade often, and read the release notes first:

https://github.com/gemini-hlsw/gpp-client/releases

To upgrade, and then check which version you have, run:

.. code-block:: bash

   pip install --upgrade gpp-client
   gpp --version

One release works with both development and production.

Version numbers take the form ``YY.M.PATCH``. For example, ``26.5.0`` is the
first release of May 2026, and ``26.5.1`` is the next one.

How an old release falls behind
-------------------------------

Each release is built from GPP's schemas of the day it was made. As GPP moves
on, an older release falls behind:

- New GPP operations, fields and arguments are missing from it.
- Anything that GPP removes still appears in it, and calls that use it fail.
- Enum values that GPP adds still parse. For details, see
  :ref:`unknown-enum-values`.

Expect breaking changes
-----------------------

Methods, arguments and models come from GPP's schema. When GPP renames or
removes something, the next release does too, so code that worked with one
release can break with the next. The client keeps no old names.

- Run your own tests after each upgrade.
- Watch for ``GPPFieldLeavingWarning``, which names fields that are about to
  leave production. For details, see :doc:`errors`.

Replace a pre-release
---------------------

If ``gpp --version`` shows a version that ends in ``.devN``, upgrade to the
latest release with ``pip install --upgrade gpp-client``.
