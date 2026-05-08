Pull Requests
=============

Pull requests should provide enough context for reviewers to understand:

- what changed
- why the change was needed
- any important testing, schema, or API considerations

Most validation is enforced automatically through GitHub Actions and repository
rulesets, including:

- formatting
- linting
- tests
- release validation

GraphQL and Code Generation
---------------------------

If a pull request changes:

- GraphQL operations
- schema files
- generated models
- generated enums
- generated input types

then the generated code must also be committed.

Generated code is treated as part of the repository source and is validated in CI.