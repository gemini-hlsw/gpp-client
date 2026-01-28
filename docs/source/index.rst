GPP Client Documentation
========================

Welcome to the documentation for the **GPP Python Client**, a modern,
fully asynchronous interface for interacting with GPP *without requiring any
GraphQL knowledge*.

The client provides a clean Python API for GPP resources such as programs,
observations, targets, and more. It also includes a configuration system,
credential manager, command-line interface, and a high-level orchestration
layer for complex multi-manager workflows.

This documentation serves both users of the client and developers maintaining
or extending the library.

What This Documentation Covers
------------------------------

The documentation is organized to guide you from basic usage to advanced
internals:

- :doc:`Getting Started <getting-started>`
  — Install the client, configure credentials, and connect to GPP in minutes.

- :doc:`Client Overview <client>`
  — How ``GPPClient`` resolves credentials, selects environments, and executes operations.

- :doc:`Configuration <configuration/index>`
  — Learn how settings, tokens, and environments are stored and managed.

- :doc:`Authentication and Credentials <credentials>`
  — All supported authentication methods and how resolution precedence works.

- :doc:`CLI Reference <cli/index>`
  — Command-line tools for configuring and interacting with GPP.

- :doc:`Resource Managers <managers/index>`
  — Program-level APIs for resources such as programs, observations, and calls for proposals.

- :doc:`Orchestration Layer <orchestration/index>`
  — Directors and Coordinators for service-specific, multi-manager workflows.

- :doc:`GPP GraphQL Building Blocks <api/index>`
  — Auto-generated types, inputs, and fields used internally by the client.

- :doc:`Exceptions <exceptions>`
  — All exception types raised by the client.

Getting Started
---------------

If you're new to the client:

1. Start with :doc:`Getting Started <getting-started>`.
2. Continue with the :doc:`Client Overview <client>` to understand the core
   execution model.

These two pages provide everything needed to authenticate and begin interacting
with GPP.

Contents
--------

.. toctree::
   :maxdepth: 2
   :caption: User Guide

   getting-started
   client
   configuration/index
   credentials
   cli/index
   managers/index
   exceptions

.. toctree::
   :maxdepth: 2
   :caption: Advanced

   orchestration/index
   api/index

.. toctree::
   :maxdepth: 2
   :caption: Developer Guide

   developer/setup
   developer/architecture
   developer/schema
   developer/codegen
   developer/workflow
   developer/releases
   contributing