# Generated by ariadne-codegen

from typing import Any, Dict, Optional

from .custom_fields import (
    AddAtomEventResultFields,
    AddConditionsEntryResultFields,
    AddDatasetEventResultFields,
    AddProgramUserResultFields,
    AddSequenceEventResultFields,
    AddSlewEventResultFields,
    AddStepEventResultFields,
    AddTimeChargeCorrectionResultFields,
    ChangeProgramUserRoleResultFields,
    CloneGroupResultFields,
    CloneObservationResultFields,
    CloneTargetResultFields,
    ConfigurationRequestFields,
    CreateCallForProposalsResultFields,
    CreateGroupResultFields,
    CreateObservationResultFields,
    CreateProgramNoteResultFields,
    CreateProgramResultFields,
    CreateProposalResultFields,
    CreateTargetResultFields,
    CreateUserInvitationResultFields,
    DeleteProgramUserResultFields,
    DeleteProposalResultFields,
    LinkUserResultFields,
    ObservationWorkflowFields,
    RecordAtomResultFields,
    RecordDatasetResultFields,
    RecordFlamingos2StepResultFields,
    RecordFlamingos2VisitResultFields,
    RecordGmosNorthStepResultFields,
    RecordGmosNorthVisitResultFields,
    RecordGmosSouthStepResultFields,
    RecordGmosSouthVisitResultFields,
    RedeemUserInvitationResultFields,
    ResetAcquisitionResultFields,
    RevokeUserInvitationResultFields,
    SetAllocationsResultFields,
    SetGuideTargetNameResultFields,
    SetProgramReferenceResultFields,
    SetProposalStatusResultFields,
    UnlinkUserResultFields,
    UpdateAsterismsResultFields,
    UpdateAttachmentsResultFields,
    UpdateCallsForProposalsResultFields,
    UpdateConfigurationRequestsResultFields,
    UpdateDatasetsResultFields,
    UpdateGroupsResultFields,
    UpdateObservationsResultFields,
    UpdateProgramNotesResultFields,
    UpdateProgramsResultFields,
    UpdateProgramUsersResultFields,
    UpdateProposalResultFields,
    UpdateTargetsResultFields,
)
from .input_types import (
    AddAtomEventInput,
    AddDatasetEventInput,
    AddProgramUserInput,
    AddSequenceEventInput,
    AddSlewEventInput,
    AddStepEventInput,
    AddTimeChargeCorrectionInput,
    ChangeProgramUserRoleInput,
    CloneGroupInput,
    CloneObservationInput,
    CloneTargetInput,
    ConditionsEntryInput,
    CreateCallForProposalsInput,
    CreateConfigurationRequestInput,
    CreateGroupInput,
    CreateObservationInput,
    CreateProgramInput,
    CreateProgramNoteInput,
    CreateProposalInput,
    CreateTargetInput,
    CreateUserInvitationInput,
    DeleteProgramUserInput,
    DeleteProposalInput,
    LinkUserInput,
    RecordAtomInput,
    RecordDatasetInput,
    RecordFlamingos2StepInput,
    RecordFlamingos2VisitInput,
    RecordGmosNorthStepInput,
    RecordGmosNorthVisitInput,
    RecordGmosSouthStepInput,
    RecordGmosSouthVisitInput,
    RedeemUserInvitationInput,
    ResetAcquisitionInput,
    RevokeUserInvitationInput,
    SetAllocationsInput,
    SetGuideTargetNameInput,
    SetObservationWorkflowStateInput,
    SetProgramReferenceInput,
    SetProposalStatusInput,
    UnlinkUserInput,
    UpdateAsterismsInput,
    UpdateAttachmentsInput,
    UpdateCallsForProposalsInput,
    UpdateConfigurationRequestsInput,
    UpdateDatasetsInput,
    UpdateGroupsInput,
    UpdateObservationsInput,
    UpdateObservationsTimesInput,
    UpdateProgramNotesInput,
    UpdateProgramsInput,
    UpdateProgramUsersInput,
    UpdateProposalInput,
    UpdateTargetsInput,
)


class Mutation:
    @classmethod
    def add_conditions_entry(
        cls, *, input: Optional[ConditionsEntryInput] = None
    ) -> AddConditionsEntryResultFields:
        arguments: Dict[str, Dict[str, Any]] = {
            "input": {"type": "ConditionsEntryInput", "value": input}
        }
        cleared_arguments = {
            key: value for key, value in arguments.items() if value["value"] is not None
        }
        return AddConditionsEntryResultFields(
            field_name="addConditionsEntry", arguments=cleared_arguments
        )

    @classmethod
    def add_atom_event(cls, input: AddAtomEventInput) -> AddAtomEventResultFields:
        arguments: Dict[str, Dict[str, Any]] = {
            "input": {"type": "AddAtomEventInput!", "value": input}
        }
        cleared_arguments = {
            key: value for key, value in arguments.items() if value["value"] is not None
        }
        return AddAtomEventResultFields(
            field_name="addAtomEvent", arguments=cleared_arguments
        )

    @classmethod
    def add_dataset_event(
        cls, input: AddDatasetEventInput
    ) -> AddDatasetEventResultFields:
        arguments: Dict[str, Dict[str, Any]] = {
            "input": {"type": "AddDatasetEventInput!", "value": input}
        }
        cleared_arguments = {
            key: value for key, value in arguments.items() if value["value"] is not None
        }
        return AddDatasetEventResultFields(
            field_name="addDatasetEvent", arguments=cleared_arguments
        )

    @classmethod
    def add_program_user(cls, input: AddProgramUserInput) -> AddProgramUserResultFields:
        arguments: Dict[str, Dict[str, Any]] = {
            "input": {"type": "AddProgramUserInput!", "value": input}
        }
        cleared_arguments = {
            key: value for key, value in arguments.items() if value["value"] is not None
        }
        return AddProgramUserResultFields(
            field_name="addProgramUser", arguments=cleared_arguments
        )

    @classmethod
    def add_sequence_event(
        cls, input: AddSequenceEventInput
    ) -> AddSequenceEventResultFields:
        arguments: Dict[str, Dict[str, Any]] = {
            "input": {"type": "AddSequenceEventInput!", "value": input}
        }
        cleared_arguments = {
            key: value for key, value in arguments.items() if value["value"] is not None
        }
        return AddSequenceEventResultFields(
            field_name="addSequenceEvent", arguments=cleared_arguments
        )

    @classmethod
    def add_slew_event(cls, input: AddSlewEventInput) -> AddSlewEventResultFields:
        arguments: Dict[str, Dict[str, Any]] = {
            "input": {"type": "AddSlewEventInput!", "value": input}
        }
        cleared_arguments = {
            key: value for key, value in arguments.items() if value["value"] is not None
        }
        return AddSlewEventResultFields(
            field_name="addSlewEvent", arguments=cleared_arguments
        )

    @classmethod
    def add_step_event(cls, input: AddStepEventInput) -> AddStepEventResultFields:
        arguments: Dict[str, Dict[str, Any]] = {
            "input": {"type": "AddStepEventInput!", "value": input}
        }
        cleared_arguments = {
            key: value for key, value in arguments.items() if value["value"] is not None
        }
        return AddStepEventResultFields(
            field_name="addStepEvent", arguments=cleared_arguments
        )

    @classmethod
    def add_time_charge_correction(
        cls, input: AddTimeChargeCorrectionInput
    ) -> AddTimeChargeCorrectionResultFields:
        arguments: Dict[str, Dict[str, Any]] = {
            "input": {"type": "AddTimeChargeCorrectionInput!", "value": input}
        }
        cleared_arguments = {
            key: value for key, value in arguments.items() if value["value"] is not None
        }
        return AddTimeChargeCorrectionResultFields(
            field_name="addTimeChargeCorrection", arguments=cleared_arguments
        )

    @classmethod
    def change_program_user_role(
        cls, input: ChangeProgramUserRoleInput
    ) -> ChangeProgramUserRoleResultFields:
        arguments: Dict[str, Dict[str, Any]] = {
            "input": {"type": "ChangeProgramUserRoleInput!", "value": input}
        }
        cleared_arguments = {
            key: value for key, value in arguments.items() if value["value"] is not None
        }
        return ChangeProgramUserRoleResultFields(
            field_name="changeProgramUserRole", arguments=cleared_arguments
        )

    @classmethod
    def clone_observation(
        cls, input: CloneObservationInput
    ) -> CloneObservationResultFields:
        arguments: Dict[str, Dict[str, Any]] = {
            "input": {"type": "CloneObservationInput!", "value": input}
        }
        cleared_arguments = {
            key: value for key, value in arguments.items() if value["value"] is not None
        }
        return CloneObservationResultFields(
            field_name="cloneObservation", arguments=cleared_arguments
        )

    @classmethod
    def clone_group(cls, input: CloneGroupInput) -> CloneGroupResultFields:
        arguments: Dict[str, Dict[str, Any]] = {
            "input": {"type": "CloneGroupInput!", "value": input}
        }
        cleared_arguments = {
            key: value for key, value in arguments.items() if value["value"] is not None
        }
        return CloneGroupResultFields(
            field_name="cloneGroup", arguments=cleared_arguments
        )

    @classmethod
    def clone_target(cls, input: CloneTargetInput) -> CloneTargetResultFields:
        arguments: Dict[str, Dict[str, Any]] = {
            "input": {"type": "CloneTargetInput!", "value": input}
        }
        cleared_arguments = {
            key: value for key, value in arguments.items() if value["value"] is not None
        }
        return CloneTargetResultFields(
            field_name="cloneTarget", arguments=cleared_arguments
        )

    @classmethod
    def create_call_for_proposals(
        cls, input: CreateCallForProposalsInput
    ) -> CreateCallForProposalsResultFields:
        arguments: Dict[str, Dict[str, Any]] = {
            "input": {"type": "CreateCallForProposalsInput!", "value": input}
        }
        cleared_arguments = {
            key: value for key, value in arguments.items() if value["value"] is not None
        }
        return CreateCallForProposalsResultFields(
            field_name="createCallForProposals", arguments=cleared_arguments
        )

    @classmethod
    def create_group(cls, input: CreateGroupInput) -> CreateGroupResultFields:
        arguments: Dict[str, Dict[str, Any]] = {
            "input": {"type": "CreateGroupInput!", "value": input}
        }
        cleared_arguments = {
            key: value for key, value in arguments.items() if value["value"] is not None
        }
        return CreateGroupResultFields(
            field_name="createGroup", arguments=cleared_arguments
        )

    @classmethod
    def create_observation(
        cls, input: CreateObservationInput
    ) -> CreateObservationResultFields:
        arguments: Dict[str, Dict[str, Any]] = {
            "input": {"type": "CreateObservationInput!", "value": input}
        }
        cleared_arguments = {
            key: value for key, value in arguments.items() if value["value"] is not None
        }
        return CreateObservationResultFields(
            field_name="createObservation", arguments=cleared_arguments
        )

    @classmethod
    def create_program(cls, input: CreateProgramInput) -> CreateProgramResultFields:
        arguments: Dict[str, Dict[str, Any]] = {
            "input": {"type": "CreateProgramInput!", "value": input}
        }
        cleared_arguments = {
            key: value for key, value in arguments.items() if value["value"] is not None
        }
        return CreateProgramResultFields(
            field_name="createProgram", arguments=cleared_arguments
        )

    @classmethod
    def create_program_note(
        cls, input: CreateProgramNoteInput
    ) -> CreateProgramNoteResultFields:
        arguments: Dict[str, Dict[str, Any]] = {
            "input": {"type": "CreateProgramNoteInput!", "value": input}
        }
        cleared_arguments = {
            key: value for key, value in arguments.items() if value["value"] is not None
        }
        return CreateProgramNoteResultFields(
            field_name="createProgramNote", arguments=cleared_arguments
        )

    @classmethod
    def create_proposal(cls, input: CreateProposalInput) -> CreateProposalResultFields:
        arguments: Dict[str, Dict[str, Any]] = {
            "input": {"type": "CreateProposalInput!", "value": input}
        }
        cleared_arguments = {
            key: value for key, value in arguments.items() if value["value"] is not None
        }
        return CreateProposalResultFields(
            field_name="createProposal", arguments=cleared_arguments
        )

    @classmethod
    def create_target(cls, input: CreateTargetInput) -> CreateTargetResultFields:
        arguments: Dict[str, Dict[str, Any]] = {
            "input": {"type": "CreateTargetInput!", "value": input}
        }
        cleared_arguments = {
            key: value for key, value in arguments.items() if value["value"] is not None
        }
        return CreateTargetResultFields(
            field_name="createTarget", arguments=cleared_arguments
        )

    @classmethod
    def delete_program_user(
        cls, input: DeleteProgramUserInput
    ) -> DeleteProgramUserResultFields:
        arguments: Dict[str, Dict[str, Any]] = {
            "input": {"type": "DeleteProgramUserInput!", "value": input}
        }
        cleared_arguments = {
            key: value for key, value in arguments.items() if value["value"] is not None
        }
        return DeleteProgramUserResultFields(
            field_name="deleteProgramUser", arguments=cleared_arguments
        )

    @classmethod
    def delete_proposal(cls, input: DeleteProposalInput) -> DeleteProposalResultFields:
        arguments: Dict[str, Dict[str, Any]] = {
            "input": {"type": "DeleteProposalInput!", "value": input}
        }
        cleared_arguments = {
            key: value for key, value in arguments.items() if value["value"] is not None
        }
        return DeleteProposalResultFields(
            field_name="deleteProposal", arguments=cleared_arguments
        )

    @classmethod
    def link_user(cls, input: LinkUserInput) -> LinkUserResultFields:
        arguments: Dict[str, Dict[str, Any]] = {
            "input": {"type": "LinkUserInput!", "value": input}
        }
        cleared_arguments = {
            key: value for key, value in arguments.items() if value["value"] is not None
        }
        return LinkUserResultFields(field_name="linkUser", arguments=cleared_arguments)

    @classmethod
    def record_atom(cls, input: RecordAtomInput) -> RecordAtomResultFields:
        arguments: Dict[str, Dict[str, Any]] = {
            "input": {"type": "RecordAtomInput!", "value": input}
        }
        cleared_arguments = {
            key: value for key, value in arguments.items() if value["value"] is not None
        }
        return RecordAtomResultFields(
            field_name="recordAtom", arguments=cleared_arguments
        )

    @classmethod
    def record_dataset(cls, input: RecordDatasetInput) -> RecordDatasetResultFields:
        arguments: Dict[str, Dict[str, Any]] = {
            "input": {"type": "RecordDatasetInput!", "value": input}
        }
        cleared_arguments = {
            key: value for key, value in arguments.items() if value["value"] is not None
        }
        return RecordDatasetResultFields(
            field_name="recordDataset", arguments=cleared_arguments
        )

    @classmethod
    def record_flamingos_2_step(
        cls, input: RecordFlamingos2StepInput
    ) -> RecordFlamingos2StepResultFields:
        arguments: Dict[str, Dict[str, Any]] = {
            "input": {"type": "RecordFlamingos2StepInput!", "value": input}
        }
        cleared_arguments = {
            key: value for key, value in arguments.items() if value["value"] is not None
        }
        return RecordFlamingos2StepResultFields(
            field_name="recordFlamingos2Step", arguments=cleared_arguments
        )

    @classmethod
    def record_flamingos_2_visit(
        cls, input: RecordFlamingos2VisitInput
    ) -> RecordFlamingos2VisitResultFields:
        arguments: Dict[str, Dict[str, Any]] = {
            "input": {"type": "RecordFlamingos2VisitInput!", "value": input}
        }
        cleared_arguments = {
            key: value for key, value in arguments.items() if value["value"] is not None
        }
        return RecordFlamingos2VisitResultFields(
            field_name="recordFlamingos2Visit", arguments=cleared_arguments
        )

    @classmethod
    def record_gmos_north_step(
        cls, input: RecordGmosNorthStepInput
    ) -> RecordGmosNorthStepResultFields:
        arguments: Dict[str, Dict[str, Any]] = {
            "input": {"type": "RecordGmosNorthStepInput!", "value": input}
        }
        cleared_arguments = {
            key: value for key, value in arguments.items() if value["value"] is not None
        }
        return RecordGmosNorthStepResultFields(
            field_name="recordGmosNorthStep", arguments=cleared_arguments
        )

    @classmethod
    def record_gmos_north_visit(
        cls, input: RecordGmosNorthVisitInput
    ) -> RecordGmosNorthVisitResultFields:
        arguments: Dict[str, Dict[str, Any]] = {
            "input": {"type": "RecordGmosNorthVisitInput!", "value": input}
        }
        cleared_arguments = {
            key: value for key, value in arguments.items() if value["value"] is not None
        }
        return RecordGmosNorthVisitResultFields(
            field_name="recordGmosNorthVisit", arguments=cleared_arguments
        )

    @classmethod
    def record_gmos_south_step(
        cls, input: RecordGmosSouthStepInput
    ) -> RecordGmosSouthStepResultFields:
        arguments: Dict[str, Dict[str, Any]] = {
            "input": {"type": "RecordGmosSouthStepInput!", "value": input}
        }
        cleared_arguments = {
            key: value for key, value in arguments.items() if value["value"] is not None
        }
        return RecordGmosSouthStepResultFields(
            field_name="recordGmosSouthStep", arguments=cleared_arguments
        )

    @classmethod
    def record_gmos_south_visit(
        cls, input: RecordGmosSouthVisitInput
    ) -> RecordGmosSouthVisitResultFields:
        arguments: Dict[str, Dict[str, Any]] = {
            "input": {"type": "RecordGmosSouthVisitInput!", "value": input}
        }
        cleared_arguments = {
            key: value for key, value in arguments.items() if value["value"] is not None
        }
        return RecordGmosSouthVisitResultFields(
            field_name="recordGmosSouthVisit", arguments=cleared_arguments
        )

    @classmethod
    def reset_acquisition(
        cls, input: ResetAcquisitionInput
    ) -> ResetAcquisitionResultFields:
        arguments: Dict[str, Dict[str, Any]] = {
            "input": {"type": "ResetAcquisitionInput!", "value": input}
        }
        cleared_arguments = {
            key: value for key, value in arguments.items() if value["value"] is not None
        }
        return ResetAcquisitionResultFields(
            field_name="resetAcquisition", arguments=cleared_arguments
        )

    @classmethod
    def set_allocations(cls, input: SetAllocationsInput) -> SetAllocationsResultFields:
        arguments: Dict[str, Dict[str, Any]] = {
            "input": {"type": "SetAllocationsInput!", "value": input}
        }
        cleared_arguments = {
            key: value for key, value in arguments.items() if value["value"] is not None
        }
        return SetAllocationsResultFields(
            field_name="setAllocations", arguments=cleared_arguments
        )

    @classmethod
    def set_guide_target_name(
        cls, input: SetGuideTargetNameInput
    ) -> SetGuideTargetNameResultFields:
        arguments: Dict[str, Dict[str, Any]] = {
            "input": {"type": "SetGuideTargetNameInput!", "value": input}
        }
        cleared_arguments = {
            key: value for key, value in arguments.items() if value["value"] is not None
        }
        return SetGuideTargetNameResultFields(
            field_name="setGuideTargetName", arguments=cleared_arguments
        )

    @classmethod
    def set_program_reference(
        cls, input: SetProgramReferenceInput
    ) -> SetProgramReferenceResultFields:
        arguments: Dict[str, Dict[str, Any]] = {
            "input": {"type": "SetProgramReferenceInput!", "value": input}
        }
        cleared_arguments = {
            key: value for key, value in arguments.items() if value["value"] is not None
        }
        return SetProgramReferenceResultFields(
            field_name="setProgramReference", arguments=cleared_arguments
        )

    @classmethod
    def set_proposal_status(
        cls, input: SetProposalStatusInput
    ) -> SetProposalStatusResultFields:
        arguments: Dict[str, Dict[str, Any]] = {
            "input": {"type": "SetProposalStatusInput!", "value": input}
        }
        cleared_arguments = {
            key: value for key, value in arguments.items() if value["value"] is not None
        }
        return SetProposalStatusResultFields(
            field_name="setProposalStatus", arguments=cleared_arguments
        )

    @classmethod
    def unlink_user(cls, input: UnlinkUserInput) -> UnlinkUserResultFields:
        arguments: Dict[str, Dict[str, Any]] = {
            "input": {"type": "UnlinkUserInput!", "value": input}
        }
        cleared_arguments = {
            key: value for key, value in arguments.items() if value["value"] is not None
        }
        return UnlinkUserResultFields(
            field_name="unlinkUser", arguments=cleared_arguments
        )

    @classmethod
    def update_asterisms(
        cls, input: UpdateAsterismsInput
    ) -> UpdateAsterismsResultFields:
        arguments: Dict[str, Dict[str, Any]] = {
            "input": {"type": "UpdateAsterismsInput!", "value": input}
        }
        cleared_arguments = {
            key: value for key, value in arguments.items() if value["value"] is not None
        }
        return UpdateAsterismsResultFields(
            field_name="updateAsterisms", arguments=cleared_arguments
        )

    @classmethod
    def update_attachments(
        cls, input: UpdateAttachmentsInput
    ) -> UpdateAttachmentsResultFields:
        arguments: Dict[str, Dict[str, Any]] = {
            "input": {"type": "UpdateAttachmentsInput!", "value": input}
        }
        cleared_arguments = {
            key: value for key, value in arguments.items() if value["value"] is not None
        }
        return UpdateAttachmentsResultFields(
            field_name="updateAttachments", arguments=cleared_arguments
        )

    @classmethod
    def update_calls_for_proposals(
        cls, input: UpdateCallsForProposalsInput
    ) -> UpdateCallsForProposalsResultFields:
        arguments: Dict[str, Dict[str, Any]] = {
            "input": {"type": "UpdateCallsForProposalsInput!", "value": input}
        }
        cleared_arguments = {
            key: value for key, value in arguments.items() if value["value"] is not None
        }
        return UpdateCallsForProposalsResultFields(
            field_name="updateCallsForProposals", arguments=cleared_arguments
        )

    @classmethod
    def update_datasets(cls, input: UpdateDatasetsInput) -> UpdateDatasetsResultFields:
        arguments: Dict[str, Dict[str, Any]] = {
            "input": {"type": "UpdateDatasetsInput!", "value": input}
        }
        cleared_arguments = {
            key: value for key, value in arguments.items() if value["value"] is not None
        }
        return UpdateDatasetsResultFields(
            field_name="updateDatasets", arguments=cleared_arguments
        )

    @classmethod
    def update_groups(cls, input: UpdateGroupsInput) -> UpdateGroupsResultFields:
        arguments: Dict[str, Dict[str, Any]] = {
            "input": {"type": "UpdateGroupsInput!", "value": input}
        }
        cleared_arguments = {
            key: value for key, value in arguments.items() if value["value"] is not None
        }
        return UpdateGroupsResultFields(
            field_name="updateGroups", arguments=cleared_arguments
        )

    @classmethod
    def update_observations(
        cls, input: UpdateObservationsInput
    ) -> UpdateObservationsResultFields:
        arguments: Dict[str, Dict[str, Any]] = {
            "input": {"type": "UpdateObservationsInput!", "value": input}
        }
        cleared_arguments = {
            key: value for key, value in arguments.items() if value["value"] is not None
        }
        return UpdateObservationsResultFields(
            field_name="updateObservations", arguments=cleared_arguments
        )

    @classmethod
    def update_configuration_requests(
        cls, input: UpdateConfigurationRequestsInput
    ) -> UpdateConfigurationRequestsResultFields:
        arguments: Dict[str, Dict[str, Any]] = {
            "input": {"type": "UpdateConfigurationRequestsInput!", "value": input}
        }
        cleared_arguments = {
            key: value for key, value in arguments.items() if value["value"] is not None
        }
        return UpdateConfigurationRequestsResultFields(
            field_name="updateConfigurationRequests", arguments=cleared_arguments
        )

    @classmethod
    def update_observations_times(
        cls, input: UpdateObservationsTimesInput
    ) -> UpdateObservationsResultFields:
        arguments: Dict[str, Dict[str, Any]] = {
            "input": {"type": "UpdateObservationsTimesInput!", "value": input}
        }
        cleared_arguments = {
            key: value for key, value in arguments.items() if value["value"] is not None
        }
        return UpdateObservationsResultFields(
            field_name="updateObservationsTimes", arguments=cleared_arguments
        )

    @classmethod
    def update_programs(cls, input: UpdateProgramsInput) -> UpdateProgramsResultFields:
        arguments: Dict[str, Dict[str, Any]] = {
            "input": {"type": "UpdateProgramsInput!", "value": input}
        }
        cleared_arguments = {
            key: value for key, value in arguments.items() if value["value"] is not None
        }
        return UpdateProgramsResultFields(
            field_name="updatePrograms", arguments=cleared_arguments
        )

    @classmethod
    def update_program_notes(
        cls, input: UpdateProgramNotesInput
    ) -> UpdateProgramNotesResultFields:
        arguments: Dict[str, Dict[str, Any]] = {
            "input": {"type": "UpdateProgramNotesInput!", "value": input}
        }
        cleared_arguments = {
            key: value for key, value in arguments.items() if value["value"] is not None
        }
        return UpdateProgramNotesResultFields(
            field_name="updateProgramNotes", arguments=cleared_arguments
        )

    @classmethod
    def update_program_users(
        cls, input: UpdateProgramUsersInput
    ) -> UpdateProgramUsersResultFields:
        arguments: Dict[str, Dict[str, Any]] = {
            "input": {"type": "UpdateProgramUsersInput!", "value": input}
        }
        cleared_arguments = {
            key: value for key, value in arguments.items() if value["value"] is not None
        }
        return UpdateProgramUsersResultFields(
            field_name="updateProgramUsers", arguments=cleared_arguments
        )

    @classmethod
    def update_proposal(cls, input: UpdateProposalInput) -> UpdateProposalResultFields:
        arguments: Dict[str, Dict[str, Any]] = {
            "input": {"type": "UpdateProposalInput!", "value": input}
        }
        cleared_arguments = {
            key: value for key, value in arguments.items() if value["value"] is not None
        }
        return UpdateProposalResultFields(
            field_name="updateProposal", arguments=cleared_arguments
        )

    @classmethod
    def update_targets(cls, input: UpdateTargetsInput) -> UpdateTargetsResultFields:
        arguments: Dict[str, Dict[str, Any]] = {
            "input": {"type": "UpdateTargetsInput!", "value": input}
        }
        cleared_arguments = {
            key: value for key, value in arguments.items() if value["value"] is not None
        }
        return UpdateTargetsResultFields(
            field_name="updateTargets", arguments=cleared_arguments
        )

    @classmethod
    def create_user_invitation(
        cls, input: CreateUserInvitationInput
    ) -> CreateUserInvitationResultFields:
        arguments: Dict[str, Dict[str, Any]] = {
            "input": {"type": "CreateUserInvitationInput!", "value": input}
        }
        cleared_arguments = {
            key: value for key, value in arguments.items() if value["value"] is not None
        }
        return CreateUserInvitationResultFields(
            field_name="createUserInvitation", arguments=cleared_arguments
        )

    @classmethod
    def redeem_user_invitation(
        cls, input: RedeemUserInvitationInput
    ) -> RedeemUserInvitationResultFields:
        arguments: Dict[str, Dict[str, Any]] = {
            "input": {"type": "RedeemUserInvitationInput!", "value": input}
        }
        cleared_arguments = {
            key: value for key, value in arguments.items() if value["value"] is not None
        }
        return RedeemUserInvitationResultFields(
            field_name="redeemUserInvitation", arguments=cleared_arguments
        )

    @classmethod
    def revoke_user_invitation(
        cls, input: RevokeUserInvitationInput
    ) -> RevokeUserInvitationResultFields:
        arguments: Dict[str, Dict[str, Any]] = {
            "input": {"type": "RevokeUserInvitationInput!", "value": input}
        }
        cleared_arguments = {
            key: value for key, value in arguments.items() if value["value"] is not None
        }
        return RevokeUserInvitationResultFields(
            field_name="revokeUserInvitation", arguments=cleared_arguments
        )

    @classmethod
    def create_configuration_request(
        cls, input: CreateConfigurationRequestInput
    ) -> ConfigurationRequestFields:
        arguments: Dict[str, Dict[str, Any]] = {
            "input": {"type": "CreateConfigurationRequestInput!", "value": input}
        }
        cleared_arguments = {
            key: value for key, value in arguments.items() if value["value"] is not None
        }
        return ConfigurationRequestFields(
            field_name="createConfigurationRequest", arguments=cleared_arguments
        )

    @classmethod
    def set_observation_workflow_state(
        cls, input: SetObservationWorkflowStateInput
    ) -> ObservationWorkflowFields:
        arguments: Dict[str, Dict[str, Any]] = {
            "input": {"type": "SetObservationWorkflowStateInput!", "value": input}
        }
        cleared_arguments = {
            key: value for key, value in arguments.items() if value["value"] is not None
        }
        return ObservationWorkflowFields(
            field_name="setObservationWorkflowState", arguments=cleared_arguments
        )
