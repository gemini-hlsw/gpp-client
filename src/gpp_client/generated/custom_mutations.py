from typing import Any, Optional

from .custom_fields import (
    AddConditionsEntryResultFields,
    AddDatasetEventResultFields,
    AddEventBatchResultFields,
    AddProgramUserResultFields,
    AddSequenceEventResultFields,
    AddSlewEventResultFields,
    AddStepEventResultFields,
    AddTimeChargeCorrectionResultFields,
    ChangePrincipalInvestigatorResultFields,
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
    DeclineTooTriggerResultFields,
    DeleteProgramUserResultFields,
    DeleteProposalResultFields,
    DeleteSequenceResultFields,
    LinkUserResultFields,
    ObservationWorkflowFields,
    RecordDatasetResultFields,
    RecordFlamingos2VisitResultFields,
    RecordGmosNorthVisitResultFields,
    RecordGmosSouthVisitResultFields,
    RecordIgrins2VisitResultFields,
    RecordVisitResultFields,
    RedeemUserInvitationResultFields,
    RefreshArchiveDuplicationResultFields,
    ReplaceFlamingos2SequenceResultFields,
    ReplaceGhostSequenceResultFields,
    ReplaceGmosNorthSequenceResultFields,
    ReplaceGmosSouthSequenceResultFields,
    ReplaceGnirsSequenceResultFields,
    ReplaceIgrins2SequenceResultFields,
    ResetAcquisitionResultFields,
    RevokeUserInvitationResultFields,
    SetAllocationsResultFields,
    SetGuideTargetNameResultFields,
    SetProgramReferenceResultFields,
    SetProgramResourceLimitResultFields,
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
    AddDatasetEventInput,
    AddEventBatchInput,
    AddProgramUserInput,
    AddSequenceEventInput,
    AddSlewEventInput,
    AddStepEventInput,
    AddTimeChargeCorrectionInput,
    ChangePrincipalInvestigatorInput,
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
    DeclineTooTriggerInput,
    DeleteProgramUserInput,
    DeleteProposalInput,
    DeleteSequenceInput,
    LinkUserInput,
    RecordDatasetInput,
    RecordFlamingos2VisitInput,
    RecordGmosNorthVisitInput,
    RecordGmosSouthVisitInput,
    RecordIgrins2VisitInput,
    RecordVisitInput,
    RedeemUserInvitationInput,
    RefreshArchiveDuplicationInput,
    ReplaceFlamingos2SequenceInput,
    ReplaceGhostSequenceInput,
    ReplaceGmosNorthSequenceInput,
    ReplaceGmosSouthSequenceInput,
    ReplaceGnirsSequenceInput,
    ReplaceIgrins2SequenceInput,
    ResetAcquisitionInput,
    RevokeUserInvitationInput,
    SetAllocationsInput,
    SetGuideTargetNameInput,
    SetObservationWorkflowStateInput,
    SetProgramReferenceInput,
    SetProgramResourceLimitInput,
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
        arguments: dict[str, dict[str, Any]] = {
            "input": {"type": "ConditionsEntryInput", "value": input}
        }
        cleared_arguments = {
            key: value for key, value in arguments.items() if value["value"] is not None
        }
        return AddConditionsEntryResultFields(
            field_name="addConditionsEntry", arguments=cleared_arguments
        )

    @classmethod
    def add_dataset_event(
        cls, input: AddDatasetEventInput
    ) -> AddDatasetEventResultFields:
        arguments: dict[str, dict[str, Any]] = {
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
        arguments: dict[str, dict[str, Any]] = {
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
        arguments: dict[str, dict[str, Any]] = {
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
        arguments: dict[str, dict[str, Any]] = {
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
        arguments: dict[str, dict[str, Any]] = {
            "input": {"type": "AddStepEventInput!", "value": input}
        }
        cleared_arguments = {
            key: value for key, value in arguments.items() if value["value"] is not None
        }
        return AddStepEventResultFields(
            field_name="addStepEvent", arguments=cleared_arguments
        )

    @classmethod
    def add_event_batch(cls, input: AddEventBatchInput) -> AddEventBatchResultFields:
        arguments: dict[str, dict[str, Any]] = {
            "input": {"type": "AddEventBatchInput!", "value": input}
        }
        cleared_arguments = {
            key: value for key, value in arguments.items() if value["value"] is not None
        }
        return AddEventBatchResultFields(
            field_name="addEventBatch", arguments=cleared_arguments
        )

    @classmethod
    def add_time_charge_correction(
        cls, input: AddTimeChargeCorrectionInput
    ) -> AddTimeChargeCorrectionResultFields:
        arguments: dict[str, dict[str, Any]] = {
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
        arguments: dict[str, dict[str, Any]] = {
            "input": {"type": "ChangeProgramUserRoleInput!", "value": input}
        }
        cleared_arguments = {
            key: value for key, value in arguments.items() if value["value"] is not None
        }
        return ChangeProgramUserRoleResultFields(
            field_name="changeProgramUserRole", arguments=cleared_arguments
        )

    @classmethod
    def change_principal_investigator(
        cls, input: ChangePrincipalInvestigatorInput
    ) -> ChangePrincipalInvestigatorResultFields:
        arguments: dict[str, dict[str, Any]] = {
            "input": {"type": "ChangePrincipalInvestigatorInput!", "value": input}
        }
        cleared_arguments = {
            key: value for key, value in arguments.items() if value["value"] is not None
        }
        return ChangePrincipalInvestigatorResultFields(
            field_name="changePrincipalInvestigator", arguments=cleared_arguments
        )

    @classmethod
    def clone_observation(
        cls, input: CloneObservationInput
    ) -> CloneObservationResultFields:
        arguments: dict[str, dict[str, Any]] = {
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
        arguments: dict[str, dict[str, Any]] = {
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
        arguments: dict[str, dict[str, Any]] = {
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
        arguments: dict[str, dict[str, Any]] = {
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
        arguments: dict[str, dict[str, Any]] = {
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
        arguments: dict[str, dict[str, Any]] = {
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
        arguments: dict[str, dict[str, Any]] = {
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
        arguments: dict[str, dict[str, Any]] = {
            "input": {"type": "CreateProgramNoteInput!", "value": input}
        }
        cleared_arguments = {
            key: value for key, value in arguments.items() if value["value"] is not None
        }
        return CreateProgramNoteResultFields(
            field_name="createProgramNote", arguments=cleared_arguments
        )

    @classmethod
    def decline_too_trigger(
        cls, input: DeclineTooTriggerInput
    ) -> DeclineTooTriggerResultFields:
        arguments: dict[str, dict[str, Any]] = {
            "input": {"type": "DeclineTooTriggerInput!", "value": input}
        }
        cleared_arguments = {
            key: value for key, value in arguments.items() if value["value"] is not None
        }
        return DeclineTooTriggerResultFields(
            field_name="declineTooTrigger", arguments=cleared_arguments
        )

    @classmethod
    def create_proposal(cls, input: CreateProposalInput) -> CreateProposalResultFields:
        arguments: dict[str, dict[str, Any]] = {
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
        arguments: dict[str, dict[str, Any]] = {
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
        arguments: dict[str, dict[str, Any]] = {
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
        arguments: dict[str, dict[str, Any]] = {
            "input": {"type": "DeleteProposalInput!", "value": input}
        }
        cleared_arguments = {
            key: value for key, value in arguments.items() if value["value"] is not None
        }
        return DeleteProposalResultFields(
            field_name="deleteProposal", arguments=cleared_arguments
        )

    @classmethod
    def delete_sequence(cls, input: DeleteSequenceInput) -> DeleteSequenceResultFields:
        arguments: dict[str, dict[str, Any]] = {
            "input": {"type": "DeleteSequenceInput!", "value": input}
        }
        cleared_arguments = {
            key: value for key, value in arguments.items() if value["value"] is not None
        }
        return DeleteSequenceResultFields(
            field_name="deleteSequence", arguments=cleared_arguments
        )

    @classmethod
    def link_user(cls, input: LinkUserInput) -> LinkUserResultFields:
        arguments: dict[str, dict[str, Any]] = {
            "input": {"type": "LinkUserInput!", "value": input}
        }
        cleared_arguments = {
            key: value for key, value in arguments.items() if value["value"] is not None
        }
        return LinkUserResultFields(field_name="linkUser", arguments=cleared_arguments)

    @classmethod
    def record_dataset(cls, input: RecordDatasetInput) -> RecordDatasetResultFields:
        arguments: dict[str, dict[str, Any]] = {
            "input": {"type": "RecordDatasetInput!", "value": input}
        }
        cleared_arguments = {
            key: value for key, value in arguments.items() if value["value"] is not None
        }
        return RecordDatasetResultFields(
            field_name="recordDataset", arguments=cleared_arguments
        )

    @classmethod
    def record_flamingos_2_visit(
        cls, input: RecordFlamingos2VisitInput
    ) -> RecordFlamingos2VisitResultFields:
        arguments: dict[str, dict[str, Any]] = {
            "input": {"type": "RecordFlamingos2VisitInput!", "value": input}
        }
        cleared_arguments = {
            key: value for key, value in arguments.items() if value["value"] is not None
        }
        return RecordFlamingos2VisitResultFields(
            field_name="recordFlamingos2Visit", arguments=cleared_arguments
        )

    @classmethod
    def replace_flamingos_2_sequence(
        cls, input: ReplaceFlamingos2SequenceInput
    ) -> ReplaceFlamingos2SequenceResultFields:
        arguments: dict[str, dict[str, Any]] = {
            "input": {"type": "ReplaceFlamingos2SequenceInput!", "value": input}
        }
        cleared_arguments = {
            key: value for key, value in arguments.items() if value["value"] is not None
        }
        return ReplaceFlamingos2SequenceResultFields(
            field_name="replaceFlamingos2Sequence", arguments=cleared_arguments
        )

    @classmethod
    def record_gmos_north_visit(
        cls, input: RecordGmosNorthVisitInput
    ) -> RecordGmosNorthVisitResultFields:
        arguments: dict[str, dict[str, Any]] = {
            "input": {"type": "RecordGmosNorthVisitInput!", "value": input}
        }
        cleared_arguments = {
            key: value for key, value in arguments.items() if value["value"] is not None
        }
        return RecordGmosNorthVisitResultFields(
            field_name="recordGmosNorthVisit", arguments=cleared_arguments
        )

    @classmethod
    def replace_gmos_north_sequence(
        cls, input: ReplaceGmosNorthSequenceInput
    ) -> ReplaceGmosNorthSequenceResultFields:
        arguments: dict[str, dict[str, Any]] = {
            "input": {"type": "ReplaceGmosNorthSequenceInput!", "value": input}
        }
        cleared_arguments = {
            key: value for key, value in arguments.items() if value["value"] is not None
        }
        return ReplaceGmosNorthSequenceResultFields(
            field_name="replaceGmosNorthSequence", arguments=cleared_arguments
        )

    @classmethod
    def record_gmos_south_visit(
        cls, input: RecordGmosSouthVisitInput
    ) -> RecordGmosSouthVisitResultFields:
        arguments: dict[str, dict[str, Any]] = {
            "input": {"type": "RecordGmosSouthVisitInput!", "value": input}
        }
        cleared_arguments = {
            key: value for key, value in arguments.items() if value["value"] is not None
        }
        return RecordGmosSouthVisitResultFields(
            field_name="recordGmosSouthVisit", arguments=cleared_arguments
        )

    @classmethod
    def record_igrins_2_visit(
        cls, input: RecordIgrins2VisitInput
    ) -> RecordIgrins2VisitResultFields:
        arguments: dict[str, dict[str, Any]] = {
            "input": {"type": "RecordIgrins2VisitInput!", "value": input}
        }
        cleared_arguments = {
            key: value for key, value in arguments.items() if value["value"] is not None
        }
        return RecordIgrins2VisitResultFields(
            field_name="recordIgrins2Visit", arguments=cleared_arguments
        )

    @classmethod
    def record_visit(cls, input: RecordVisitInput) -> RecordVisitResultFields:
        arguments: dict[str, dict[str, Any]] = {
            "input": {"type": "RecordVisitInput!", "value": input}
        }
        cleared_arguments = {
            key: value for key, value in arguments.items() if value["value"] is not None
        }
        return RecordVisitResultFields(
            field_name="recordVisit", arguments=cleared_arguments
        )

    @classmethod
    def replace_gmos_south_sequence(
        cls, input: ReplaceGmosSouthSequenceInput
    ) -> ReplaceGmosSouthSequenceResultFields:
        arguments: dict[str, dict[str, Any]] = {
            "input": {"type": "ReplaceGmosSouthSequenceInput!", "value": input}
        }
        cleared_arguments = {
            key: value for key, value in arguments.items() if value["value"] is not None
        }
        return ReplaceGmosSouthSequenceResultFields(
            field_name="replaceGmosSouthSequence", arguments=cleared_arguments
        )

    @classmethod
    def replace_igrins_2_sequence(
        cls, input: ReplaceIgrins2SequenceInput
    ) -> ReplaceIgrins2SequenceResultFields:
        arguments: dict[str, dict[str, Any]] = {
            "input": {"type": "ReplaceIgrins2SequenceInput!", "value": input}
        }
        cleared_arguments = {
            key: value for key, value in arguments.items() if value["value"] is not None
        }
        return ReplaceIgrins2SequenceResultFields(
            field_name="replaceIgrins2Sequence", arguments=cleared_arguments
        )

    @classmethod
    def replace_gnirs_sequence(
        cls, input: ReplaceGnirsSequenceInput
    ) -> ReplaceGnirsSequenceResultFields:
        arguments: dict[str, dict[str, Any]] = {
            "input": {"type": "ReplaceGnirsSequenceInput!", "value": input}
        }
        cleared_arguments = {
            key: value for key, value in arguments.items() if value["value"] is not None
        }
        return ReplaceGnirsSequenceResultFields(
            field_name="replaceGnirsSequence", arguments=cleared_arguments
        )

    @classmethod
    def replace_ghost_sequence(
        cls, input: ReplaceGhostSequenceInput
    ) -> ReplaceGhostSequenceResultFields:
        arguments: dict[str, dict[str, Any]] = {
            "input": {"type": "ReplaceGhostSequenceInput!", "value": input}
        }
        cleared_arguments = {
            key: value for key, value in arguments.items() if value["value"] is not None
        }
        return ReplaceGhostSequenceResultFields(
            field_name="replaceGhostSequence", arguments=cleared_arguments
        )

    @classmethod
    def refresh_archive_duplication(
        cls, input: RefreshArchiveDuplicationInput
    ) -> RefreshArchiveDuplicationResultFields:
        arguments: dict[str, dict[str, Any]] = {
            "input": {"type": "RefreshArchiveDuplicationInput!", "value": input}
        }
        cleared_arguments = {
            key: value for key, value in arguments.items() if value["value"] is not None
        }
        return RefreshArchiveDuplicationResultFields(
            field_name="refreshArchiveDuplication", arguments=cleared_arguments
        )

    @classmethod
    def reset_acquisition(
        cls, input: ResetAcquisitionInput
    ) -> ResetAcquisitionResultFields:
        arguments: dict[str, dict[str, Any]] = {
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
        arguments: dict[str, dict[str, Any]] = {
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
        arguments: dict[str, dict[str, Any]] = {
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
        arguments: dict[str, dict[str, Any]] = {
            "input": {"type": "SetProgramReferenceInput!", "value": input}
        }
        cleared_arguments = {
            key: value for key, value in arguments.items() if value["value"] is not None
        }
        return SetProgramReferenceResultFields(
            field_name="setProgramReference", arguments=cleared_arguments
        )

    @classmethod
    def set_program_resource_limit(
        cls, input: SetProgramResourceLimitInput
    ) -> SetProgramResourceLimitResultFields:
        arguments: dict[str, dict[str, Any]] = {
            "input": {"type": "SetProgramResourceLimitInput!", "value": input}
        }
        cleared_arguments = {
            key: value for key, value in arguments.items() if value["value"] is not None
        }
        return SetProgramResourceLimitResultFields(
            field_name="setProgramResourceLimit", arguments=cleared_arguments
        )

    @classmethod
    def set_proposal_status(
        cls, input: SetProposalStatusInput
    ) -> SetProposalStatusResultFields:
        arguments: dict[str, dict[str, Any]] = {
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
        arguments: dict[str, dict[str, Any]] = {
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
        arguments: dict[str, dict[str, Any]] = {
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
        arguments: dict[str, dict[str, Any]] = {
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
        arguments: dict[str, dict[str, Any]] = {
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
        arguments: dict[str, dict[str, Any]] = {
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
        arguments: dict[str, dict[str, Any]] = {
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
        arguments: dict[str, dict[str, Any]] = {
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
        arguments: dict[str, dict[str, Any]] = {
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
        arguments: dict[str, dict[str, Any]] = {
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
        arguments: dict[str, dict[str, Any]] = {
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
        arguments: dict[str, dict[str, Any]] = {
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
        arguments: dict[str, dict[str, Any]] = {
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
        arguments: dict[str, dict[str, Any]] = {
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
        arguments: dict[str, dict[str, Any]] = {
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
        arguments: dict[str, dict[str, Any]] = {
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
        arguments: dict[str, dict[str, Any]] = {
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
        arguments: dict[str, dict[str, Any]] = {
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
        arguments: dict[str, dict[str, Any]] = {
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
        arguments: dict[str, dict[str, Any]] = {
            "input": {"type": "SetObservationWorkflowStateInput!", "value": input}
        }
        cleared_arguments = {
            key: value for key, value in arguments.items() if value["value"] is not None
        }
        return ObservationWorkflowFields(
            field_name="setObservationWorkflowState", arguments=cleared_arguments
        )
