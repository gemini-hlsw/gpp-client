GraphQL Input Models
====================

The ``gpp_client.generated.input_types`` module contains all of the **GraphQL input models** used when sending data to the Gemini Program Platform (GPP) API.

These models define the structure of inputs required when creating or updating GPP resources such as `Programs`, `Observations`, `Targets`, and more. They are auto-generated from the GPP GraphQL schema using ``ariadne-codegen``, ensuring compatibility with the latest backend API types.

Each input type corresponds directly to an ``InputObjectType`` in the GraphQL schema. These are passed into manager methods such as ``create()``, ``update_by_id()``, or ``update_all()`` via arguments like ``properties``.

How to Use
----------

To use these input types, import the relevant class and populate it with the necessary fields:

.. code-block:: python

   from gpp_client.generated.input_types import ObservationPropertiesInput

   input_data = ObservationPropertiesInput(
       title="Nightly science observation",
       observerNotes="Target acquired under clear conditions.",
   )

   await client.observation.update_by_id(observation_id="o-123", properties=input_data)

For optional nested structures, you may also need to import other input types like ``SiderealInput``, ``BandNormalizedIntegratedInput``, or others defined in this module.

.. note::

   All fields are type-checked via Pydantic and support auto-completion in most modern editors.

API Reference
-------------

.. automodule:: gpp_client.generated.input_types
   :members:
   :undoc-members:
   :exclude-members: model_config