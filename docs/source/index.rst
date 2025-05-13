GPP Client Documentation
=========================

Welcome to the documentation for the **GPP Python Client**, a modern, asynchronous client built to interact with GPP, without the GraphQL.

The GPP Client provides a clean, extensible way to manage GPP resources like programs, observations, targets, and more through a Pythonic interface.

What This Documentation Covers
-------------------------------

- :doc:`Quickstart <quickstart>`: Set up the GPP Client and connect to the GPP in minutes.
- :doc:`Client Overview <client>`: Learn how to authenticate and initialize the ``GPPClient``, the main entry point for interacting with GPP.
- :doc:`Configuration <config>`: Understand where settings and credentials are stored and how to manage them.
- :doc:`Authentication and Credentials <credentials>`: See the different ways to provide your API credentials.
- :doc:`CLI Reference <cli/index>`: If you're using the CLI, explore available commands for managing configurations and interacting with resources.
- :doc:`Resource Managers <managers/index>`: Learn how the ``ProgramManager`` and other managers work and the available API to create, delete, restore, update, and get resources from GPP.
- :doc:`GPP GraphQL Client Building Blocks <api/index>`: Explore the GraphQL API types, fields, and inputs that are essential when constructing payloads for inputs and outputs.


Getting Started
---------------

If you're new, start with the :doc:`Quickstart <quickstart>` guide to install the package and connect to GPP.
Then move on to the :doc:`Client Overview <client>` to see how the client is organized and how to perform basic operations.

.. toctree::
   :maxdepth: 2
   :caption: Contents:

   quickstart
   client
   config
   credentials
   cli/index
   managers/index
   api/index
   contributing
