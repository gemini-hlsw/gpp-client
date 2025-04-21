GPP Client Documentation
========================

Welcome to the official documentation for the **GPP Python Client**, a modern, asynchronous GraphQL client designed to interact with the Gemini Program Platform (GPP) APIs.

This library provides a clean, extensible interface for working with GPP resources such as programs, observations, targets, and more.

What You'll Find Here
---------------------
- :doc:`Quickstart <quickstart>`: Get going quickly communicating with GPP.
- :doc:`Client Overview <client>`: Learn how to authenticate and initialize the `GPPClient`, which serves as the main entry point to all functionality.
- :doc:`Manager Modules <managers/index>`: Understand how resource-specific managers (e.g., `ProgramNoteManager`) encapsulate logic for GraphQL operations like `get_by_id`, `create`, and `update_batch`.
- :doc:`Mixins <mixins/index>`: Dive into the reusable building blocks behind each manager — powerful abstractions that promote DRY and consistent logic for GraphQL patterns.

If you're just getting started, begin with the :doc:`Client <client>` section to see how to instantiate and use the `GPPClient`. Then, explore the available managers and mixins to understand how the system is structured and how to extend it.

.. toctree::
   :maxdepth: 2
   :caption: Contents:

   quickstart
   client
   credentials
   managers/index
   mixins/index