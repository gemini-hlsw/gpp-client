# Generated coverage first, curated conveniences on top

Every part of the GPP API we support reaches users through the generated client, and gaps in that coverage are bugs. Hand-written curated conveniences (such as `client.scheduler.get_all`, which combines GraphQL and REST) are allowed on top of that coverage, never instead of it, and each one needs a test that fails when the schema under it changes.

We chose this over "users first, pay the maintenance" and "maintenance first, hand-written only where generation cannot reach": GPP changes almost daily, so hand-written code is where breakage hides, but users still need task-shaped methods. The rule keeps both, and makes the cost of each hand-written layer visible in CI.
