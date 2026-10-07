"""Typed views of the generated client per environment. Generated; do not edit."""

from .async_base_client import AsyncBaseClient
from .client import GraphQLClient


class SharedGraphQLClient(AsyncBaseClient):
    """
    The generated client methods on development and production.
    """

    get_observation_attachments_by_id = GraphQLClient.get_observation_attachments_by_id
    get_observation_attachments_by_reference = GraphQLClient.get_observation_attachments_by_reference
    get_program_attachments_by_id = GraphQLClient.get_program_attachments_by_id
    get_program_attachments_by_reference = GraphQLClient.get_program_attachments_by_reference
    get_program_attachments_by_proposal_reference = GraphQLClient.get_program_attachments_by_proposal_reference
    create_call_for_proposals = GraphQLClient.create_call_for_proposals
    update_calls_for_proposals = GraphQLClient.update_calls_for_proposals
    update_call_for_proposals_by_id = GraphQLClient.update_call_for_proposals_by_id
    restore_call_for_proposals_by_id = GraphQLClient.restore_call_for_proposals_by_id
    delete_call_for_proposals_by_id = GraphQLClient.delete_call_for_proposals_by_id
    get_call_for_proposals = GraphQLClient.get_call_for_proposals
    get_calls_for_proposals = GraphQLClient.get_calls_for_proposals
    get_goats_programs = GraphQLClient.get_goats_programs
    get_goats_observations = GraphQLClient.get_goats_observations
    get_goats_configuration_requests = GraphQLClient.get_goats_configuration_requests
    get_goats_config_options = GraphQLClient.get_goats_config_options
    create_observation = GraphQLClient.create_observation
    clone_observation = GraphQLClient.clone_observation
    update_observations = GraphQLClient.update_observations
    update_observation_by_id = GraphQLClient.update_observation_by_id
    update_observation_by_reference = GraphQLClient.update_observation_by_reference
    restore_observation_by_id = GraphQLClient.restore_observation_by_id
    restore_observation_by_reference = GraphQLClient.restore_observation_by_reference
    delete_observation_by_id = GraphQLClient.delete_observation_by_id
    delete_observation_by_reference = GraphQLClient.delete_observation_by_reference
    get_observation = GraphQLClient.get_observation
    get_observations = GraphQLClient.get_observations
    observation_edit = GraphQLClient.observation_edit
    obs_calculation_update = GraphQLClient.obs_calculation_update
    create_program = GraphQLClient.create_program
    update_programs = GraphQLClient.update_programs
    update_program_by_id = GraphQLClient.update_program_by_id
    restore_program_by_id = GraphQLClient.restore_program_by_id
    delete_program_by_id = GraphQLClient.delete_program_by_id
    get_program_by_id = GraphQLClient.get_program_by_id
    get_program_by_reference = GraphQLClient.get_program_by_reference
    get_program_by_proposal_reference = GraphQLClient.get_program_by_proposal_reference
    get_programs = GraphQLClient.get_programs
    program_edit = GraphQLClient.program_edit
    get_scheduler_programs = GraphQLClient.get_scheduler_programs
    get_scheduler_all_programs_id = GraphQLClient.get_scheduler_all_programs_id
    scheduler_observations_updates = GraphQLClient.scheduler_observations_updates
    clone_target = GraphQLClient.clone_target
    create_target_by_program_id = GraphQLClient.create_target_by_program_id
    create_target_by_proposal_reference = GraphQLClient.create_target_by_proposal_reference
    create_target_by_program_reference = GraphQLClient.create_target_by_program_reference
    update_targets = GraphQLClient.update_targets
    update_target_by_id = GraphQLClient.update_target_by_id
    restore_target_by_id = GraphQLClient.restore_target_by_id
    delete_target_by_id = GraphQLClient.delete_target_by_id
    get_target_by_id = GraphQLClient.get_target_by_id
    get_targets = GraphQLClient.get_targets
    target_edit = GraphQLClient.target_edit
    ping = GraphQLClient.ping
    set_observation_workflow_state = GraphQLClient.set_observation_workflow_state
    get_observation_workflow_state_by_id = GraphQLClient.get_observation_workflow_state_by_id
    get_observation_workflow_state_by_reference = GraphQLClient.get_observation_workflow_state_by_reference
    execute_custom_operation = GraphQLClient.execute_custom_operation
    query = GraphQLClient.query
    mutation = GraphQLClient.mutation


class DevelopmentGraphQLClient(SharedGraphQLClient):
    """
    The generated client methods on development.
    """


class ProductionGraphQLClient(SharedGraphQLClient):
    """
    The generated client methods on production.
    """


class EveryEnvironmentGraphQLClient(DevelopmentGraphQLClient, ProductionGraphQLClient):
    """
    Every environment's view, so the full client is typed as each one.
    """
