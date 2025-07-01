Enums
=====

This module defines all enumerated types used in the GPP GraphQL schema.

Enums are used to constrain fields to a specific set of valid values, preventing invalid data during queries or mutations. These are required for many ``InputType`` fields (e.g., ``Existence``, ``CalibrationRole``, ``ScienceBand``) and should be referenced when constructing input objects or interpreting responses.

Usage
-----

Each enum is exposed as a Python ``Enum``, allowing you to access values safely in client code.

For example:

.. code-block:: python

    from gpp_client.api.enums import Existence

    input_data = TargetPropertiesInput(existence=Existence.PRESENT)

API Reference
-------------

.. automodule:: gpp_client.api.enums
   :members:
   :undoc-members:
