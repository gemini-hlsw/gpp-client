Mixins
======

Mixins in the `gpp_client` library encapsulate reusable logic for common GraphQL operations such as `create`, `get`, `update`, `delete`, and `restore`. They allow individual resource managers to inherit only the behaviors they need, promoting **modularity**, **consistency**, and **code reuse** across the client.

Purpose
-------

The GPP API exposes many GraphQL resources that follow a predictable pattern in terms of operations. For example, most resources support:

- Fetching a resource by ID
- Fetching in batches
- Creating or updating via a mutation
- Soft-deleting or restoring resources

Rather than duplicating that logic in every manager, the client implements these operations once as generic mixins.

Benefits of Mixins
------------------

- **Composable**: Managers include only the mixins they need
- **Override-friendly**: Managers can override specific methods while retaining the shared base logic
- **DRY and consistent**: Shared GraphQL formatting, error handling, and conventions are enforced in one place
- **Typed and extendable**: Mixins are written with type hints to support IDE autocomplete and static analysis

For example, a `ProgramNoteManager` might inherit:

- `GetByIdMixin`
- `GetBatchByProgramIdMixin`
- `CreateMixin`
- `UpdateByIdViaBatchMixin`
- `DeleteByIdViaBatchMixin`
- and more...

Each of those mixins contributes one or more methods (e.g., `get_by_id`, `create`, `delete_by_id`).

API Reference
-------------

.. toctree::
   :maxdepth: 1

   create
   delete
   get
   restore
   update