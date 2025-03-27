# GPP GraphQL Client

![Docs Status](https://readthedocs.org/projects/gpp-client/badge/?version=latest)

The GPP Client is a Python library for interacting with the Gemini Program Platform (GPP) GraphQL API. It provides a high-level, async interface for querying and mutating data without writing raw GraphQL.

## Documentation
https://gpp-client.readthedocs.io/en/latest/

## Overview

This client exposes resource-specific managers that group related GraphQL operations. Each manager supports operations like `create`, `get_by_id`, `update_by_id`, and `delete_by_id`, using standard async methods. No GraphQL knowledge required.

## Example Usage

```python
from gpp_client import GPPClient

client = GPPClient(
    url="https://your-gpp-api/graphql",
    auth_token="your_token_here"
)

# Create a program note
note = await client.program_note.create(
    title="Weather Update",
    text="Thin cirrus moving in, seeing around 1.3\".",
    program_id="p-123"
)

# Fetch a note by ID
fetched = await client.program_note.get_by_id(resource_id=note["id"])
```