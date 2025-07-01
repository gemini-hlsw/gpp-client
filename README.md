# GPP Client

[![Run Tests](https://github.com/gemini-hlsw/gpp-client/actions/workflows/run_tests.yaml/badge.svg?branch=main)](https://github.com/gemini-hlsw/gpp-client/actions/workflows/run_tests.yaml)
![Docs Status](https://readthedocs.org/projects/gpp-client/badge/?version=latest)

---

_Pain-free python/CLI communication with the Gemini Program Platform (GPP)._

**Documentation**: <a href="https://gpp-client.readthedocs.io/en/latest/" target="_blank">https://gpp-client.readthedocs.io/en/latest/</a>

**Source Code**: <a href="https://github.com/gemini-hlsw/gpp-client" target="_blank">https://github.com/gemini-hlsw/gpp-client</a>

---

Python client and CLI for the GPP. Key features:

- **Type‑safe GraphQL**
  - Pydantic models from the GPP GraphQL schema, so every query, mutation, and input type is validated.
- **Resource Managers**
  - High‑level `Manager` classes (e.g. `GPPClient.program`, `GPPClient.observation`) with convenient `get_by_id`, `get_all`, `create`, `update_by_id`, `delete_by_id`, `restore_by_id` and more methods, no need to write raw GraphQL.
- **Flexible payloads**
  - Create or update via in‑memory Pydantic inputs **or** `from_json` files.
- **`gpp` CLI**
  - Full CRUD surface on the command line: `gpp <resource> list|get|create|update|delete`, with rich table output and JSON export options.

### Requirements

- `python>=3.10`
- `toml`
- `typer`
- `ariadne-codegen`

## Development Status

🚧 Alpha: the library is under heavy development. The public API and CLI flags may change between releases.

## Installation

```bash
pip install gpp-client
```

## Quickstart

```python
from gpp_client import GPPClient

# Initialize with your GraphQL endpoint and credentials.
client = GPPClient(url="YOUR_URL", token="YOUR_TOKEN")

# List the first 5 program notes.
notes = await client.program_note.get_all(limit=5)
for note in notes["matches"]:
    print(f"{note['id']}: {note['title']}")

# Create a new note from a JSON file.
new_note = await client.program_note.create(
    from_json="path/to/program_note_payload.json",
    program_id="p-123"
)
print("Created:", new_note)

# Or create a note from the pydantic model.
from gpp_client.api.enums import Existence
from gpp_client.api.input_types import ProgramNotePropertiesInput

properties = ProgramNotePropertiesInput(
    title="Example",
    text="This is an example.",
    is_private=False,
    existence=Existence.PRESENT
)
another_note = await client.program_note.create(properties=properties, program_id="p-123")

print("Created another:", another_note)
```

## As a CLI

```bash
# Get help.
gpp --help

# Get observation help.
gpp obs --help

# List observations.
gpp obs list --limit 3

# Get details for one.
gpp obs get o-123

# Create via JSON.
gpp obs create --from-json new_obs.json --program-id p-123

# Update by ID via JSON.
gpp obs update --observation-id o-123 --from-json updated_obs.json
```

## Reporting Bugs and Feature Requests

**Jira**: https://noirlab.atlassian.net/jira/software/projects/GPC/boards/162

**NOIRLab Slack channel**: `#gpp-client`

While in heavy development, please file requests or report bugs via our Jira board or Slack channel.

# Developer Notes

To update the GPP GraphQL schema and generate client code, run the scripts from the project’s top-level directory located in `scripts/`.

This project uses [uv](https://github.com/astral-sh/uv) to manage dependencies and execute scripts.

When using `uv run`, a temporary virtual environment is created with only the dependencies required to run the script, based on the groups defined in `pyproject.toml`.

There’s no need to manually create or activate a virtual environment, `uv` handles everything.

## Set Up `pre-commit`

To install `pre-commit` using `uv`, run:

```bash
uv tool install pre-commit --with pre-commit-uv
```

You may be prompted to add `.local/bin` to your `PATH`, `uv` installs tools there by default.

Next, install the hooks defined in `.pre-commit-config.yaml`:

```bash
pre-commit install
```

Once installed, `pre-commit` will automatically run the configured hooks each time you make a commit. This helps catch formatting issues, docstring violations, and other problems before code is committed.

To manually run all `pre-commit` hooks on the entire codebase:

```bash
pre-commit run --all-files
```

## Download the Schema

This script downloads the latest GPP GraphQL schema to `schema.graphql`. You must have `GPP_URL` and `GPP_TOKEN` env variables set for downloading to work.

```bash
uv run --group schema python scripts/download_schema.py
```

## Run Codegen

This script regenerates the client code based on the updated schema.

```bash
uv run --group codegen python scripts/run_codegen.py
```

## Creating and Deploying a Release

Releases are managed using GitHub Actions. When you’re ready to publish a new version of the package, use the **Create Release** workflow.

1. Go to the **Actions** tab on GitHub.
2. Select the **Create Release** workflow from the sidebar.
3. Click **Run workflow**.
4. Enter the release version (e.g., `25.6.0`).
   **Note:** Do **not** include a leading `v` or unnecessary zero padding.
5. Click **Run workflow** to trigger the release.

This workflow performs the following steps:

- Updates the `version` field in `pyproject.toml`.
- Updates the `uv.lock` file to reflect the new version.
- Commits and pushes the changes to the repository.
- Creates a Git tag.
- Drafts a GitHub release.

### Finalizing the Release

After the workflow completes:

1. Go to the **Releases** section on GitHub.
2. Locate the newly created **draft release**.
3. Click **Publish release**.

Once published, the package will be automatically uploaded to [PyPI](https://pypi.org/project/gpp-client/). It may take a few minutes for the release to appear.
