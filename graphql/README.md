## GraphQL Operations Structure

GraphQL operations are now organized to support both shared and environment-specific behavior.

### Directory Layout

- `graphql/operations/shared/`
  - Contains all operations and fragments used in both development and production.
- `graphql/operations/development_only.graphql`
  - Contains operations and fragments that exist only in the development schema.

### How It Works

- **Production**
  - Uses only the contents of `shared/`.

- **Development**
  - Uses `shared/` + `development_only.graphql`.

- During code generation, these are assembled into a temporary build directory and passed to `ariadne-codegen`.

### Rules

- `development_only.graphql` must be **additive only**.
  - No operation or fragment names may collide with anything in `shared/`.
  - Violations will fail code generation.

- If `development_only.graphql` is empty or missing, it is ignored.

### Guidelines

- Put anything stable and supported in both environments into `shared/`.
- Put experimental, dev-only, or not-yet-released schema usage into `development_only.graphql`.
- Once a dev-only operation is promoted to production, move it into `shared/` and remove it from `development_only.graphql`.

### Notes

- The `build/` directory is temporary and is recreated on each codegen run.
- Generated client code reflects the environment used during codegen.