# Consumers

Who builds on gpp-client, which environment each runs on, what each imports, and how each picks up a release. Read this before changing public API: a change that touches anything listed here goes in the release notes under "Breaking", naming the consumer. Refresh it from the consumers' default branches each release cycle. Facts below come from the consumer repositories as read on 2026-10-07 (GOATS `f4e445c`, scheduler `c75a19c`, AEONlib `9af2874`).

## GOATS (gemini-hlsw/goats)

- Environment: development. Its local settings template sets `GPP_ENV = "DEVELOPMENT"`, and its releases have shipped development builds of the client. It passes `environment=` from that Django setting and each user's own token as `token=`.
- Domains: attachment, goats, observation, program, target, workflow_state (19 methods). `client.graphql.ping()` directly, because `GPPClient.ping` loses the HTTP status. The attachment REST paths (upload, update, delete, download URL).
- Operations: `get_goats_observations`, `get_goats_programs`, `get_goats_configuration_requests`, `get_goats_config_options`, `create_observation`, `get_observation`, `get_observation_attachments_by_id`, `get_program_attachments_by_id`, `get_observation_workflow_state_by_id`, `get_observation_workflow_state_by_reference`, `get_program_by_id`, `set_observation_workflow_state`, `update_observation_by_id`, `update_target_by_id`, and two more of the shared operations, `get_observations` and `get_targets` being the candidates (UNCONFIRMED which).
- Imported names: 22 input types and 23 enums from `gpp_client.generated`, 17 of the enums iterated for form dropdowns, so a new or removed member reaches its UI. `gpp_client.settings.GPPSettings` (environment and token hint on its status page), `gpp_client.urls`, `gpp_client.environment`, `gpp_client.generated.exceptions.GraphQLClientHttpError`. Result models go through `model_dump(by_alias=True)` to its JavaScript, so a removed result field breaks its UI.
- Upgrade cadence: an exact pin in `pyproject.toml`, moved by hand; 11 pin changes in its history, six of them to `.devN` builds. Its conda users get releases only, from conda-forge.

## Scheduler (gemini-hlsw/scheduler)

- Environment: production for the deployed scheduler; its development apps run on development. Token from `GPP_TOKEN` or `GPP_DEVELOPMENT_TOKEN`.
- Domains: scheduler, observation, target (6 methods): `scheduler.get_all(programs_list, exclude_programs)`, `get_programs`, `get_program_ids`, `get_visibility_changes`, and the obscalc subscription. REST: atom digests (inside `scheduler.get_all`) and visibility changes, with `gpp_client.rest.models.VisibilityChanges`.
- Operations: `get_observations`, `get_scheduler_all_programs_id`, `get_scheduler_programs`, `get_targets`, `scheduler_observations_updates`. Raw documents through `client._graphql.execute` (`recordVisit`, `add*Event`, `setObservationWorkflowState`); the subscription through `client._graphql.scheduler_observations_updates(open_timeout=...)` because the domain method takes no connection options. Both are the public `client.graphql` now.
- Imported names: 9 `Where*` input types and 3 enums; `gpp_client.cli.output` for printing; `client.graphql.ws_url` in a probe script; four `generated.custom_fields` classes as an unused import and a mock return value.
- Upgrade cadence: a uv lock with two conflicting dependency groups, `gpp-prod` (`>=26.9.0`) and `gpp-dev` (`.devN` range), chosen per Docker build; the pin was edited six times between May and October. CI installs `gpp-dev` only. One release stream lets it keep one `gpp-client>=` dependency.

## AEONlib (AEONplus/AEONlib)

- Environment: either, from its `gemini_environment` setting, production by default. Today it subclasses `GPPClient` and overrides the private `_build_settings` to apply the setting; that override fails with `TypeError` on this branch, and `GPPSettings(environment_override=...)` is silently ignored. The replacement is `GPPClient(environment=...)`.
- Domains: `target.create_by_program_id`, `create_by_program_reference`, `create_by_proposal_reference`; `delete_by_id` in its online tests.
- Operations: `create_target_by_program_id`, `create_target_by_program_reference`, `create_target_by_proposal_reference`, and their result types.
- Imported names: 12 input types; the enums `TimingWindowInclusion` and `Existence`; `gpp_client.generated.exceptions.GraphQLClientHttpError`.
- Upgrade cadence: `aeonlib[gemini]` depends on `gpp-client>=26.7.3` with no upper bound, so every release reaches a fresh install untested. Its own tests mock the client. It doesn't contribute here.

## Not consumers

`gemini-hlsw/gpp-client2` (an unreleased rewrite), `conda-forge/gpp-client-feedstock` (repackages releases), and `gemini-hlsw/lucupy` (doesn't import the client). Private repositories, notebooks and personal scripts can't be seen.
