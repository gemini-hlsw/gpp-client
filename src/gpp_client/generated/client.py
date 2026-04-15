from collections.abc import AsyncIterator
from typing import Any, Optional, Union

from graphql import (
    DocumentNode,
    NamedTypeNode,
    NameNode,
    OperationDefinitionNode,
    OperationType,
    SelectionNode,
    SelectionSetNode,
    VariableDefinitionNode,
    VariableNode,
    print_ast,
)

from .async_base_client import AsyncBaseClient
from .base_model import UNSET, UnsetType
from .base_operation import GraphQLField
from .clone_observation import CloneObservation
from .clone_target import CloneTarget
from .create_call_for_proposals import CreateCallForProposals
from .create_observation import CreateObservation
from .create_program import CreateProgram
from .create_target_by_program_id import CreateTargetByProgramId
from .create_target_by_program_reference import CreateTargetByProgramReference
from .create_target_by_proposal_reference import CreateTargetByProposalReference
from .delete_call_for_proposals_by_id import DeleteCallForProposalsById
from .delete_observation_by_id import DeleteObservationById
from .delete_observation_by_reference import DeleteObservationByReference
from .delete_program_by_id import DeleteProgramById
from .delete_target_by_id import DeleteTargetById
from .enums import ObservationWorkflowState
from .get_call_for_proposals import GetCallForProposals
from .get_calls_for_proposals import GetCallsForProposals
from .get_goats_observations import GetGOATSObservations
from .get_goats_programs import GetGOATSPrograms
from .get_observation import GetObservation
from .get_observation_attachments_by_id import GetObservationAttachmentsById
from .get_observation_attachments_by_reference import (
    GetObservationAttachmentsByReference,
)
from .get_observation_workflow_state_by_id import GetObservationWorkflowStateById
from .get_observation_workflow_state_by_reference import (
    GetObservationWorkflowStateByReference,
)
from .get_observations import GetObservations
from .get_program_attachments_by_id import GetProgramAttachmentsById
from .get_program_attachments_by_proposal_reference import (
    GetProgramAttachmentsByProposalReference,
)
from .get_program_attachments_by_reference import GetProgramAttachmentsByReference
from .get_program_by_id import GetProgramById
from .get_program_by_proposal_reference import GetProgramByProposalReference
from .get_program_by_reference import GetProgramByReference
from .get_programs import GetPrograms
from .get_scheduler_all_programs_id import GetSchedulerAllProgramsId
from .get_scheduler_programs import GetSchedulerPrograms
from .get_target_by_id import GetTargetById
from .get_targets import GetTargets
from .input_types import (
    CallForProposalsPropertiesInput,
    CloneObservationInput,
    CreateObservationInput,
    ObservationPropertiesInput,
    ProgramPropertiesInput,
    TargetPropertiesInput,
    UpdateObservationsInput,
    WhereCallForProposals,
    WhereObservation,
    WhereProgram,
    WhereTarget,
)
from .obs_calculation_update import ObsCalculationUpdate
from .observation_edit import ObservationEdit
from .ping import Ping
from .program_edit import ProgramEdit
from .restore_call_for_proposals_by_id import RestoreCallForProposalsById
from .restore_observation_by_id import RestoreObservationById
from .restore_observation_by_reference import RestoreObservationByReference
from .restore_program_by_id import RestoreProgramById
from .restore_target_by_id import RestoreTargetById
from .set_observation_workflow_state import SetObservationWorkflowState
from .target_edit import TargetEdit
from .update_call_for_proposals_by_id import UpdateCallForProposalsById
from .update_calls_for_proposals import UpdateCallsForProposals
from .update_observation_by_id import UpdateObservationById
from .update_observation_by_reference import UpdateObservationByReference
from .update_observations import UpdateObservations
from .update_program_by_id import UpdateProgramById
from .update_programs import UpdatePrograms
from .update_target_by_id import UpdateTargetById
from .update_targets import UpdateTargets


def gql(q: str) -> str:
    return q


class GraphQLClient(AsyncBaseClient):
    async def get_observation_attachments_by_id(
        self, observation_id: Any, **kwargs: Any
    ) -> GetObservationAttachmentsById:
        query = gql("""
            query GetObservationAttachmentsById($observationId: ObservationId!) {
              observation(observationId: $observationId) {
                attachments {
                  ...AttachmentDetails
                }
              }
            }

            fragment AttachmentDetails on Attachment {
              id
              fileName
              attachmentType
              fileSize
              checked
              description
              updatedAt
            }
            """)
        variables: dict[str, object] = {"observationId": observation_id}
        response = await self.execute(
            query=query,
            operation_name="GetObservationAttachmentsById",
            variables=variables,
            **kwargs,
        )
        data = self.get_data(response)
        return GetObservationAttachmentsById.model_validate(data)

    async def get_observation_attachments_by_reference(
        self, observation_reference: Any, **kwargs: Any
    ) -> GetObservationAttachmentsByReference:
        query = gql("""
            query GetObservationAttachmentsByReference($observationReference: ObservationReferenceLabel!) {
              observation(observationReference: $observationReference) {
                attachments {
                  ...AttachmentDetails
                }
              }
            }

            fragment AttachmentDetails on Attachment {
              id
              fileName
              attachmentType
              fileSize
              checked
              description
              updatedAt
            }
            """)
        variables: dict[str, object] = {"observationReference": observation_reference}
        response = await self.execute(
            query=query,
            operation_name="GetObservationAttachmentsByReference",
            variables=variables,
            **kwargs,
        )
        data = self.get_data(response)
        return GetObservationAttachmentsByReference.model_validate(data)

    async def get_program_attachments_by_id(
        self, program_id: Any, **kwargs: Any
    ) -> GetProgramAttachmentsById:
        query = gql("""
            query GetProgramAttachmentsById($programId: ProgramId!) {
              program(programId: $programId) {
                attachments {
                  ...AttachmentDetails
                }
              }
            }

            fragment AttachmentDetails on Attachment {
              id
              fileName
              attachmentType
              fileSize
              checked
              description
              updatedAt
            }
            """)
        variables: dict[str, object] = {"programId": program_id}
        response = await self.execute(
            query=query,
            operation_name="GetProgramAttachmentsById",
            variables=variables,
            **kwargs,
        )
        data = self.get_data(response)
        return GetProgramAttachmentsById.model_validate(data)

    async def get_program_attachments_by_reference(
        self, program_reference: Any, **kwargs: Any
    ) -> GetProgramAttachmentsByReference:
        query = gql("""
            query GetProgramAttachmentsByReference($programReference: ProgramReferenceLabel!) {
              program(programReference: $programReference) {
                attachments {
                  ...AttachmentDetails
                }
              }
            }

            fragment AttachmentDetails on Attachment {
              id
              fileName
              attachmentType
              fileSize
              checked
              description
              updatedAt
            }
            """)
        variables: dict[str, object] = {"programReference": program_reference}
        response = await self.execute(
            query=query,
            operation_name="GetProgramAttachmentsByReference",
            variables=variables,
            **kwargs,
        )
        data = self.get_data(response)
        return GetProgramAttachmentsByReference.model_validate(data)

    async def get_program_attachments_by_proposal_reference(
        self, proposal_reference: Any, **kwargs: Any
    ) -> GetProgramAttachmentsByProposalReference:
        query = gql("""
            query GetProgramAttachmentsByProposalReference($proposalReference: ProposalReferenceLabel!) {
              program(proposalReference: $proposalReference) {
                attachments {
                  ...AttachmentDetails
                }
              }
            }

            fragment AttachmentDetails on Attachment {
              id
              fileName
              attachmentType
              fileSize
              checked
              description
              updatedAt
            }
            """)
        variables: dict[str, object] = {"proposalReference": proposal_reference}
        response = await self.execute(
            query=query,
            operation_name="GetProgramAttachmentsByProposalReference",
            variables=variables,
            **kwargs,
        )
        data = self.get_data(response)
        return GetProgramAttachmentsByProposalReference.model_validate(data)

    async def create_call_for_proposals(
        self,
        properties: Union[Optional[CallForProposalsPropertiesInput], UnsetType] = UNSET,
        **kwargs: Any,
    ) -> CreateCallForProposals:
        query = gql("""
            mutation createCallForProposals($properties: CallForProposalsPropertiesInput) {
              createCallForProposals(input: {SET: $properties}) {
                callForProposals {
                  ...CallForProposalsDetails
                }
              }
            }

            fragment CallForProposalsCore on CallForProposals {
              id
              title
            }

            fragment CallForProposalsDetails on CallForProposals {
              ...CallForProposalsCore
              type
              semester
              active {
                start
                end
              }
              submissionDeadlineDefault
              instruments
              existence
            }
            """)
        variables: dict[str, object] = {"properties": properties}
        response = await self.execute(
            query=query,
            operation_name="createCallForProposals",
            variables=variables,
            **kwargs,
        )
        data = self.get_data(response)
        return CreateCallForProposals.model_validate(data)

    async def update_calls_for_proposals(
        self,
        properties: CallForProposalsPropertiesInput,
        include_deleted: bool,
        where: Union[Optional[WhereCallForProposals], UnsetType] = UNSET,
        limit: Union[Optional[Any], UnsetType] = UNSET,
        **kwargs: Any,
    ) -> UpdateCallsForProposals:
        query = gql("""
            mutation updateCallsForProposals($properties: CallForProposalsPropertiesInput!, $where: WhereCallForProposals, $limit: NonNegInt, $includeDeleted: Boolean! = false) {
              updateCallsForProposals(
                input: {SET: $properties, WHERE: $where, LIMIT: $limit, includeDeleted: $includeDeleted}
              ) {
                hasMore
                callsForProposals {
                  ...CallForProposalsDetails
                }
              }
            }

            fragment CallForProposalsCore on CallForProposals {
              id
              title
            }

            fragment CallForProposalsDetails on CallForProposals {
              ...CallForProposalsCore
              type
              semester
              active {
                start
                end
              }
              submissionDeadlineDefault
              instruments
              existence
            }
            """)
        variables: dict[str, object] = {
            "properties": properties,
            "where": where,
            "limit": limit,
            "includeDeleted": include_deleted,
        }
        response = await self.execute(
            query=query,
            operation_name="updateCallsForProposals",
            variables=variables,
            **kwargs,
        )
        data = self.get_data(response)
        return UpdateCallsForProposals.model_validate(data)

    async def update_call_for_proposals_by_id(
        self,
        call_for_proposals_id: Any,
        properties: CallForProposalsPropertiesInput,
        include_deleted: bool,
        **kwargs: Any,
    ) -> UpdateCallForProposalsById:
        query = gql("""
            mutation updateCallForProposalsById($callForProposalsId: CallForProposalsId!, $properties: CallForProposalsPropertiesInput!, $includeDeleted: Boolean! = false) {
              updateCallsForProposals(
                input: {SET: $properties, WHERE: {id: {EQ: $callForProposalsId}}, LIMIT: 1, includeDeleted: $includeDeleted}
              ) {
                hasMore
                callsForProposals {
                  ...CallForProposalsDetails
                }
              }
            }

            fragment CallForProposalsCore on CallForProposals {
              id
              title
            }

            fragment CallForProposalsDetails on CallForProposals {
              ...CallForProposalsCore
              type
              semester
              active {
                start
                end
              }
              submissionDeadlineDefault
              instruments
              existence
            }
            """)
        variables: dict[str, object] = {
            "callForProposalsId": call_for_proposals_id,
            "properties": properties,
            "includeDeleted": include_deleted,
        }
        response = await self.execute(
            query=query,
            operation_name="updateCallForProposalsById",
            variables=variables,
            **kwargs,
        )
        data = self.get_data(response)
        return UpdateCallForProposalsById.model_validate(data)

    async def restore_call_for_proposals_by_id(
        self, call_for_proposals_id: Any, **kwargs: Any
    ) -> RestoreCallForProposalsById:
        query = gql("""
            mutation restoreCallForProposalsById($callForProposalsId: CallForProposalsId!) {
              updateCallsForProposals(
                input: {SET: {existence: PRESENT}, WHERE: {id: {EQ: $callForProposalsId}}, LIMIT: 1, includeDeleted: true}
              ) {
                hasMore
                callsForProposals {
                  ...CallForProposalsDetails
                }
              }
            }

            fragment CallForProposalsCore on CallForProposals {
              id
              title
            }

            fragment CallForProposalsDetails on CallForProposals {
              ...CallForProposalsCore
              type
              semester
              active {
                start
                end
              }
              submissionDeadlineDefault
              instruments
              existence
            }
            """)
        variables: dict[str, object] = {"callForProposalsId": call_for_proposals_id}
        response = await self.execute(
            query=query,
            operation_name="restoreCallForProposalsById",
            variables=variables,
            **kwargs,
        )
        data = self.get_data(response)
        return RestoreCallForProposalsById.model_validate(data)

    async def delete_call_for_proposals_by_id(
        self, call_for_proposals_id: Any, **kwargs: Any
    ) -> DeleteCallForProposalsById:
        query = gql("""
            mutation deleteCallForProposalsById($callForProposalsId: CallForProposalsId!) {
              updateCallsForProposals(
                input: {SET: {existence: DELETED}, WHERE: {id: {EQ: $callForProposalsId}}, LIMIT: 1, includeDeleted: false}
              ) {
                hasMore
                callsForProposals {
                  ...CallForProposalsDetails
                }
              }
            }

            fragment CallForProposalsCore on CallForProposals {
              id
              title
            }

            fragment CallForProposalsDetails on CallForProposals {
              ...CallForProposalsCore
              type
              semester
              active {
                start
                end
              }
              submissionDeadlineDefault
              instruments
              existence
            }
            """)
        variables: dict[str, object] = {"callForProposalsId": call_for_proposals_id}
        response = await self.execute(
            query=query,
            operation_name="deleteCallForProposalsById",
            variables=variables,
            **kwargs,
        )
        data = self.get_data(response)
        return DeleteCallForProposalsById.model_validate(data)

    async def get_call_for_proposals(
        self, call_for_proposals_id: Any, **kwargs: Any
    ) -> GetCallForProposals:
        query = gql("""
            query getCallForProposals($callForProposalsId: CallForProposalsId!) {
              callForProposals(callForProposalsId: $callForProposalsId) {
                ...CallForProposalsDetails
              }
            }

            fragment CallForProposalsCore on CallForProposals {
              id
              title
            }

            fragment CallForProposalsDetails on CallForProposals {
              ...CallForProposalsCore
              type
              semester
              active {
                start
                end
              }
              submissionDeadlineDefault
              instruments
              existence
            }
            """)
        variables: dict[str, object] = {"callForProposalsId": call_for_proposals_id}
        response = await self.execute(
            query=query,
            operation_name="getCallForProposals",
            variables=variables,
            **kwargs,
        )
        data = self.get_data(response)
        return GetCallForProposals.model_validate(data)

    async def get_calls_for_proposals(
        self,
        include_deleted: bool,
        where: Union[Optional[WhereCallForProposals], UnsetType] = UNSET,
        offset: Union[Optional[Any], UnsetType] = UNSET,
        limit: Union[Optional[Any], UnsetType] = UNSET,
        **kwargs: Any,
    ) -> GetCallsForProposals:
        query = gql("""
            query getCallsForProposals($where: WhereCallForProposals, $offset: CallForProposalsId, $limit: NonNegInt, $includeDeleted: Boolean! = false) {
              callsForProposals(
                WHERE: $where
                OFFSET: $offset
                LIMIT: $limit
                includeDeleted: $includeDeleted
              ) {
                hasMore
                matches {
                  ...CallForProposalsDetails
                }
              }
            }

            fragment CallForProposalsCore on CallForProposals {
              id
              title
            }

            fragment CallForProposalsDetails on CallForProposals {
              ...CallForProposalsCore
              type
              semester
              active {
                start
                end
              }
              submissionDeadlineDefault
              instruments
              existence
            }
            """)
        variables: dict[str, object] = {
            "where": where,
            "offset": offset,
            "limit": limit,
            "includeDeleted": include_deleted,
        }
        response = await self.execute(
            query=query,
            operation_name="getCallsForProposals",
            variables=variables,
            **kwargs,
        )
        data = self.get_data(response)
        return GetCallsForProposals.model_validate(data)

    async def get_goats_programs(self, **kwargs: Any) -> GetGOATSPrograms:
        query = gql("""
            query GetGOATSPrograms {
              programs(includeDeleted: false, WHERE: {proposalStatus: {EQ: ACCEPTED}}) {
                matches {
                  id
                  name
                  description
                  reference {
                    __typename
                    label
                  }
                  proposalStatus
                  type
                }
                hasMore
              }
            }
            """)
        variables: dict[str, object] = {}
        response = await self.execute(
            query=query,
            operation_name="GetGOATSPrograms",
            variables=variables,
            **kwargs,
        )
        data = self.get_data(response)
        return GetGOATSPrograms.model_validate(data)

    async def get_goats_observations(
        self, program_id: Any, **kwargs: Any
    ) -> GetGOATSObservations:
        query = gql("""
            query GetGOATSObservations($programId: ProgramId!) {
              observations(
                includeDeleted: false
                WHERE: {program: {id: {EQ: $programId}, proposalStatus: {EQ: ACCEPTED}}}
              ) {
                matches {
                  id
                  reference {
                    label
                  }
                  instrument
                  title
                  constraintSet {
                    imageQuality
                    cloudExtinction
                    skyBackground
                    waterVapor
                    elevationRange {
                      airMass {
                        min
                        max
                      }
                      hourAngle {
                        minHours
                        maxHours
                      }
                    }
                  }
                  workflow {
                    state
                    value {
                      state
                      validTransitions
                      validationErrors {
                        code
                      }
                    }
                  }
                  attachments {
                    id
                    attachmentType
                    fileName
                    description
                    updatedAt
                  }
                  timingWindows {
                    inclusion
                    startUtc
                    end {
                      __typename
                      ... on TimingWindowEndAt {
                        atUtc
                      }
                      ... on TimingWindowEndAfter {
                        after {
                          seconds
                        }
                        repeat {
                          period {
                            seconds
                          }
                          times
                        }
                      }
                    }
                  }
                  targetEnvironment {
                    asterism {
                      id
                      name
                      opportunity {
                        __typename
                      }
                    }
                    firstScienceTarget {
                      id
                      name
                      opportunity {
                        __typename
                      }
                      sidereal {
                        ra {
                          hms
                          hours
                          degrees
                        }
                        dec {
                          dms
                          degrees
                        }
                        properMotion {
                          ra {
                            milliarcsecondsPerYear
                          }
                          dec {
                            milliarcsecondsPerYear
                          }
                        }
                        parallax {
                          milliarcseconds
                        }
                        radialVelocity {
                          kilometersPerSecond
                        }
                      }
                      sourceProfile {
                        point {
                          bandNormalized {
                            brightnesses {
                              band
                              value
                              units
                            }
                            sed {
                              blackBodyTempK
                              coolStar
                              fluxDensities {
                                wavelength {
                                  nanometers
                                }
                                density
                              }
                              fluxDensitiesAttachment
                              galaxy
                              hiiRegion
                              planet
                              planetaryNebula
                              powerLaw
                              quasar
                              stellarLibrary
                            }
                          }
                        }
                      }
                    }
                  }
                  posAngleConstraint {
                    mode
                    angle {
                      degrees
                    }
                  }
                  scienceBand
                  observationDuration {
                    seconds
                    minutes
                    hours
                    iso
                  }
                  observerNotes
                  scienceRequirements {
                    mode
                    spectroscopy {
                      wavelength {
                        nanometers
                      }
                    }
                    exposureTimeMode {
                      signalToNoise {
                        value
                        at {
                          nanometers
                        }
                      }
                      timeAndCount {
                        time {
                          seconds
                        }
                        count
                        at {
                          nanometers
                        }
                      }
                    }
                  }
                  observingMode {
                    instrument
                    mode
                    gmosNorthLongSlit {
                      grating
                      filter
                      fpu
                      centralWavelength {
                        nanometers
                      }
                      wavelengthDithers {
                        nanometers
                      }
                      xBin
                      yBin
                      ampReadMode
                      roi
                      exposureTimeMode {
                        signalToNoise {
                          value
                          at {
                            nanometers
                          }
                        }
                        timeAndCount {
                          time {
                            seconds
                          }
                          count
                          at {
                            nanometers
                          }
                        }
                      }
                      offsets {
                        arcseconds
                      }
                    }
                    gmosSouthLongSlit {
                      grating
                      filter
                      fpu
                      centralWavelength {
                        nanometers
                      }
                      wavelengthDithers {
                        nanometers
                      }
                      xBin
                      yBin
                      ampReadMode
                      roi
                      exposureTimeMode {
                        signalToNoise {
                          value
                          at {
                            nanometers
                          }
                        }
                        timeAndCount {
                          time {
                            seconds
                          }
                          count
                          at {
                            nanometers
                          }
                        }
                      }
                      offsets {
                        arcseconds
                      }
                    }
                  }
                  program {
                    allocations {
                      scienceBand
                      duration {
                        hours
                      }
                    }
                    timeCharge {
                      band
                      time {
                        program {
                          hours
                        }
                      }
                    }
                  }
                }
                hasMore
              }
            }
            """)
        variables: dict[str, object] = {"programId": program_id}
        response = await self.execute(
            query=query,
            operation_name="GetGOATSObservations",
            variables=variables,
            **kwargs,
        )
        data = self.get_data(response)
        return GetGOATSObservations.model_validate(data)

    async def create_observation(
        self, input: CreateObservationInput, **kwargs: Any
    ) -> CreateObservation:
        query = gql("""
            mutation createObservation($input: CreateObservationInput!) {
              createObservation(input: $input) {
                observation {
                  ...ObservationDetails
                }
              }
            }

            fragment ConstraintSetDetails on ConstraintSet {
              imageQuality
              cloudExtinction
              skyBackground
              waterVapor
              elevationRange {
                airMass {
                  min
                  max
                }
                hourAngle {
                  minHours
                  maxHours
                }
              }
            }

            fragment ExposureTimeModeDetails on ExposureTimeMode {
              signalToNoise {
                value
                at {
                  nanometers
                }
              }
              timeAndCount {
                time {
                  seconds
                }
                count
                at {
                  nanometers
                }
              }
            }

            fragment Flamingos2LongSlitDetails on Flamingos2LongSlit {
              decker
              defaultDecker
              defaultOffsets {
                q {
                  arcseconds
                }
                p {
                  arcseconds
                }
              }
              disperser
              filter
              fpu
              telluricType {
                tag
                starTypes
              }
              exposureTimeMode {
                ...ExposureTimeModeDetails
              }
              explicitReadMode
              explicitReads
              explicitDecker
              readoutMode
              defaultReadoutMode
              offsets {
                q {
                  arcseconds
                }
                p {
                  arcseconds
                }
              }
              acquisition {
                exposureTimeMode {
                  ...ExposureTimeModeDetails
                }
              }
              initialDisperser
              initialFilter
              initialFpu
            }

            fragment GmosNorthImagingDetails on GmosNorthImaging {
              filters {
                filter
              }
              bin
            }

            fragment GmosNorthLongSlitDetails on GmosNorthLongSlit {
              grating
              filter
              fpu
              centralWavelength {
                nanometers
              }
              offsets {
                arcseconds
              }
              xBin
              yBin
            }

            fragment GmosSouthImagingDetails on GmosSouthImaging {
              filters {
                filter
              }
              bin
            }

            fragment GmosSouthLongSlitDetails on GmosSouthLongSlit {
              grating
              filter
              fpu
              centralWavelength {
                nanometers
              }
              offsets {
                arcseconds
              }
              xBin
              yBin
            }

            fragment NonsiderealTargetDetails on Nonsidereal {
              des
              keyType
              key
            }

            fragment ObservationCore on Observation {
              id
              existence
              reference {
                label
              }
              title
              instrument
              calibrationRole
            }

            fragment ObservationDetails on Observation {
              ...ObservationCore
              observerNotes
              subtitle
              program {
                ...ProgramCore
              }
              scienceRequirements {
                ...ScienceRequirementsDetails
              }
              scienceBand
              workflow {
                ...WorkflowDetails
              }
              observingMode {
                ...ObservingModeDetails
              }
              constraintSet {
                ...ConstraintSetDetails
              }
              timingWindows {
                ...TimingWindowDetails
              }
              targetEnvironment {
                ...TargetEnvironmentDetails
              }
            }

            fragment ObservingModeDetails on ObservingMode {
              instrument
              mode
              gmosNorthLongSlit {
                ...GmosNorthLongSlitDetails
              }
              gmosSouthLongSlit {
                ...GmosSouthLongSlitDetails
              }
              gmosNorthImaging {
                ...GmosNorthImagingDetails
              }
              gmosSouthImaging {
                ...GmosSouthImagingDetails
              }
              flamingos2LongSlit {
                ...Flamingos2LongSlitDetails
              }
            }

            fragment ProgramCore on Program {
              id
              name
              existence
              description
            }

            fragment ScienceRequirementsDetails on ScienceRequirements {
              mode
            }

            fragment SiderealTargetDetails on Sidereal {
              ra {
                hours
                hms
                degrees
              }
              dec {
                degrees
                dms
              }
              epoch
            }

            fragment TargetEnvironmentDetails on TargetEnvironment {
              asterism {
                name
                sidereal {
                  ...SiderealTargetDetails
                }
                nonsidereal {
                  ...NonsiderealTargetDetails
                }
              }
              explicitBase {
                ra {
                  hms
                }
                dec {
                  dms
                }
              }
            }

            fragment TimingWindowDetails on TimingWindow {
              inclusion
              startUtc
              end {
                __typename
                ... on TimingWindowEndAt {
                  atUtc
                }
                ... on TimingWindowEndAfter {
                  after {
                    seconds
                  }
                  repeat {
                    period {
                      seconds
                    }
                    times
                  }
                }
              }
            }

            fragment WorkflowCore on CalculatedObservationWorkflow {
              state
            }

            fragment WorkflowDetails on CalculatedObservationWorkflow {
              ...WorkflowCore
              value {
                state
                validTransitions
                validationErrors {
                  code
                  messages
                }
              }
            }
            """)
        variables: dict[str, object] = {"input": input}
        response = await self.execute(
            query=query,
            operation_name="createObservation",
            variables=variables,
            **kwargs,
        )
        data = self.get_data(response)
        return CreateObservation.model_validate(data)

    async def clone_observation(
        self, input: CloneObservationInput, **kwargs: Any
    ) -> CloneObservation:
        query = gql("""
            mutation cloneObservation($input: CloneObservationInput!) {
              cloneObservation(input: $input) {
                newObservation {
                  ...ObservationDetails
                }
              }
            }

            fragment ConstraintSetDetails on ConstraintSet {
              imageQuality
              cloudExtinction
              skyBackground
              waterVapor
              elevationRange {
                airMass {
                  min
                  max
                }
                hourAngle {
                  minHours
                  maxHours
                }
              }
            }

            fragment ExposureTimeModeDetails on ExposureTimeMode {
              signalToNoise {
                value
                at {
                  nanometers
                }
              }
              timeAndCount {
                time {
                  seconds
                }
                count
                at {
                  nanometers
                }
              }
            }

            fragment Flamingos2LongSlitDetails on Flamingos2LongSlit {
              decker
              defaultDecker
              defaultOffsets {
                q {
                  arcseconds
                }
                p {
                  arcseconds
                }
              }
              disperser
              filter
              fpu
              telluricType {
                tag
                starTypes
              }
              exposureTimeMode {
                ...ExposureTimeModeDetails
              }
              explicitReadMode
              explicitReads
              explicitDecker
              readoutMode
              defaultReadoutMode
              offsets {
                q {
                  arcseconds
                }
                p {
                  arcseconds
                }
              }
              acquisition {
                exposureTimeMode {
                  ...ExposureTimeModeDetails
                }
              }
              initialDisperser
              initialFilter
              initialFpu
            }

            fragment GmosNorthImagingDetails on GmosNorthImaging {
              filters {
                filter
              }
              bin
            }

            fragment GmosNorthLongSlitDetails on GmosNorthLongSlit {
              grating
              filter
              fpu
              centralWavelength {
                nanometers
              }
              offsets {
                arcseconds
              }
              xBin
              yBin
            }

            fragment GmosSouthImagingDetails on GmosSouthImaging {
              filters {
                filter
              }
              bin
            }

            fragment GmosSouthLongSlitDetails on GmosSouthLongSlit {
              grating
              filter
              fpu
              centralWavelength {
                nanometers
              }
              offsets {
                arcseconds
              }
              xBin
              yBin
            }

            fragment NonsiderealTargetDetails on Nonsidereal {
              des
              keyType
              key
            }

            fragment ObservationCore on Observation {
              id
              existence
              reference {
                label
              }
              title
              instrument
              calibrationRole
            }

            fragment ObservationDetails on Observation {
              ...ObservationCore
              observerNotes
              subtitle
              program {
                ...ProgramCore
              }
              scienceRequirements {
                ...ScienceRequirementsDetails
              }
              scienceBand
              workflow {
                ...WorkflowDetails
              }
              observingMode {
                ...ObservingModeDetails
              }
              constraintSet {
                ...ConstraintSetDetails
              }
              timingWindows {
                ...TimingWindowDetails
              }
              targetEnvironment {
                ...TargetEnvironmentDetails
              }
            }

            fragment ObservingModeDetails on ObservingMode {
              instrument
              mode
              gmosNorthLongSlit {
                ...GmosNorthLongSlitDetails
              }
              gmosSouthLongSlit {
                ...GmosSouthLongSlitDetails
              }
              gmosNorthImaging {
                ...GmosNorthImagingDetails
              }
              gmosSouthImaging {
                ...GmosSouthImagingDetails
              }
              flamingos2LongSlit {
                ...Flamingos2LongSlitDetails
              }
            }

            fragment ProgramCore on Program {
              id
              name
              existence
              description
            }

            fragment ScienceRequirementsDetails on ScienceRequirements {
              mode
            }

            fragment SiderealTargetDetails on Sidereal {
              ra {
                hours
                hms
                degrees
              }
              dec {
                degrees
                dms
              }
              epoch
            }

            fragment TargetEnvironmentDetails on TargetEnvironment {
              asterism {
                name
                sidereal {
                  ...SiderealTargetDetails
                }
                nonsidereal {
                  ...NonsiderealTargetDetails
                }
              }
              explicitBase {
                ra {
                  hms
                }
                dec {
                  dms
                }
              }
            }

            fragment TimingWindowDetails on TimingWindow {
              inclusion
              startUtc
              end {
                __typename
                ... on TimingWindowEndAt {
                  atUtc
                }
                ... on TimingWindowEndAfter {
                  after {
                    seconds
                  }
                  repeat {
                    period {
                      seconds
                    }
                    times
                  }
                }
              }
            }

            fragment WorkflowCore on CalculatedObservationWorkflow {
              state
            }

            fragment WorkflowDetails on CalculatedObservationWorkflow {
              ...WorkflowCore
              value {
                state
                validTransitions
                validationErrors {
                  code
                  messages
                }
              }
            }
            """)
        variables: dict[str, object] = {"input": input}
        response = await self.execute(
            query=query,
            operation_name="cloneObservation",
            variables=variables,
            **kwargs,
        )
        data = self.get_data(response)
        return CloneObservation.model_validate(data)

    async def update_observations(
        self, input: UpdateObservationsInput, **kwargs: Any
    ) -> UpdateObservations:
        query = gql("""
            mutation updateObservations($input: UpdateObservationsInput!) {
              updateObservations(input: $input) {
                hasMore
                observations {
                  ...ObservationDetails
                }
              }
            }

            fragment ConstraintSetDetails on ConstraintSet {
              imageQuality
              cloudExtinction
              skyBackground
              waterVapor
              elevationRange {
                airMass {
                  min
                  max
                }
                hourAngle {
                  minHours
                  maxHours
                }
              }
            }

            fragment ExposureTimeModeDetails on ExposureTimeMode {
              signalToNoise {
                value
                at {
                  nanometers
                }
              }
              timeAndCount {
                time {
                  seconds
                }
                count
                at {
                  nanometers
                }
              }
            }

            fragment Flamingos2LongSlitDetails on Flamingos2LongSlit {
              decker
              defaultDecker
              defaultOffsets {
                q {
                  arcseconds
                }
                p {
                  arcseconds
                }
              }
              disperser
              filter
              fpu
              telluricType {
                tag
                starTypes
              }
              exposureTimeMode {
                ...ExposureTimeModeDetails
              }
              explicitReadMode
              explicitReads
              explicitDecker
              readoutMode
              defaultReadoutMode
              offsets {
                q {
                  arcseconds
                }
                p {
                  arcseconds
                }
              }
              acquisition {
                exposureTimeMode {
                  ...ExposureTimeModeDetails
                }
              }
              initialDisperser
              initialFilter
              initialFpu
            }

            fragment GmosNorthImagingDetails on GmosNorthImaging {
              filters {
                filter
              }
              bin
            }

            fragment GmosNorthLongSlitDetails on GmosNorthLongSlit {
              grating
              filter
              fpu
              centralWavelength {
                nanometers
              }
              offsets {
                arcseconds
              }
              xBin
              yBin
            }

            fragment GmosSouthImagingDetails on GmosSouthImaging {
              filters {
                filter
              }
              bin
            }

            fragment GmosSouthLongSlitDetails on GmosSouthLongSlit {
              grating
              filter
              fpu
              centralWavelength {
                nanometers
              }
              offsets {
                arcseconds
              }
              xBin
              yBin
            }

            fragment NonsiderealTargetDetails on Nonsidereal {
              des
              keyType
              key
            }

            fragment ObservationCore on Observation {
              id
              existence
              reference {
                label
              }
              title
              instrument
              calibrationRole
            }

            fragment ObservationDetails on Observation {
              ...ObservationCore
              observerNotes
              subtitle
              program {
                ...ProgramCore
              }
              scienceRequirements {
                ...ScienceRequirementsDetails
              }
              scienceBand
              workflow {
                ...WorkflowDetails
              }
              observingMode {
                ...ObservingModeDetails
              }
              constraintSet {
                ...ConstraintSetDetails
              }
              timingWindows {
                ...TimingWindowDetails
              }
              targetEnvironment {
                ...TargetEnvironmentDetails
              }
            }

            fragment ObservingModeDetails on ObservingMode {
              instrument
              mode
              gmosNorthLongSlit {
                ...GmosNorthLongSlitDetails
              }
              gmosSouthLongSlit {
                ...GmosSouthLongSlitDetails
              }
              gmosNorthImaging {
                ...GmosNorthImagingDetails
              }
              gmosSouthImaging {
                ...GmosSouthImagingDetails
              }
              flamingos2LongSlit {
                ...Flamingos2LongSlitDetails
              }
            }

            fragment ProgramCore on Program {
              id
              name
              existence
              description
            }

            fragment ScienceRequirementsDetails on ScienceRequirements {
              mode
            }

            fragment SiderealTargetDetails on Sidereal {
              ra {
                hours
                hms
                degrees
              }
              dec {
                degrees
                dms
              }
              epoch
            }

            fragment TargetEnvironmentDetails on TargetEnvironment {
              asterism {
                name
                sidereal {
                  ...SiderealTargetDetails
                }
                nonsidereal {
                  ...NonsiderealTargetDetails
                }
              }
              explicitBase {
                ra {
                  hms
                }
                dec {
                  dms
                }
              }
            }

            fragment TimingWindowDetails on TimingWindow {
              inclusion
              startUtc
              end {
                __typename
                ... on TimingWindowEndAt {
                  atUtc
                }
                ... on TimingWindowEndAfter {
                  after {
                    seconds
                  }
                  repeat {
                    period {
                      seconds
                    }
                    times
                  }
                }
              }
            }

            fragment WorkflowCore on CalculatedObservationWorkflow {
              state
            }

            fragment WorkflowDetails on CalculatedObservationWorkflow {
              ...WorkflowCore
              value {
                state
                validTransitions
                validationErrors {
                  code
                  messages
                }
              }
            }
            """)
        variables: dict[str, object] = {"input": input}
        response = await self.execute(
            query=query,
            operation_name="updateObservations",
            variables=variables,
            **kwargs,
        )
        data = self.get_data(response)
        return UpdateObservations.model_validate(data)

    async def update_observation_by_id(
        self, observation_id: Any, set_: ObservationPropertiesInput, **kwargs: Any
    ) -> UpdateObservationById:
        query = gql("""
            mutation updateObservationById($observationId: ObservationId!, $SET: ObservationPropertiesInput!) {
              updateObservations(
                input: {SET: $SET, WHERE: {id: {EQ: $observationId}}, LIMIT: 1}
              ) {
                hasMore
                observations {
                  ...ObservationDetails
                }
              }
            }

            fragment ConstraintSetDetails on ConstraintSet {
              imageQuality
              cloudExtinction
              skyBackground
              waterVapor
              elevationRange {
                airMass {
                  min
                  max
                }
                hourAngle {
                  minHours
                  maxHours
                }
              }
            }

            fragment ExposureTimeModeDetails on ExposureTimeMode {
              signalToNoise {
                value
                at {
                  nanometers
                }
              }
              timeAndCount {
                time {
                  seconds
                }
                count
                at {
                  nanometers
                }
              }
            }

            fragment Flamingos2LongSlitDetails on Flamingos2LongSlit {
              decker
              defaultDecker
              defaultOffsets {
                q {
                  arcseconds
                }
                p {
                  arcseconds
                }
              }
              disperser
              filter
              fpu
              telluricType {
                tag
                starTypes
              }
              exposureTimeMode {
                ...ExposureTimeModeDetails
              }
              explicitReadMode
              explicitReads
              explicitDecker
              readoutMode
              defaultReadoutMode
              offsets {
                q {
                  arcseconds
                }
                p {
                  arcseconds
                }
              }
              acquisition {
                exposureTimeMode {
                  ...ExposureTimeModeDetails
                }
              }
              initialDisperser
              initialFilter
              initialFpu
            }

            fragment GmosNorthImagingDetails on GmosNorthImaging {
              filters {
                filter
              }
              bin
            }

            fragment GmosNorthLongSlitDetails on GmosNorthLongSlit {
              grating
              filter
              fpu
              centralWavelength {
                nanometers
              }
              offsets {
                arcseconds
              }
              xBin
              yBin
            }

            fragment GmosSouthImagingDetails on GmosSouthImaging {
              filters {
                filter
              }
              bin
            }

            fragment GmosSouthLongSlitDetails on GmosSouthLongSlit {
              grating
              filter
              fpu
              centralWavelength {
                nanometers
              }
              offsets {
                arcseconds
              }
              xBin
              yBin
            }

            fragment NonsiderealTargetDetails on Nonsidereal {
              des
              keyType
              key
            }

            fragment ObservationCore on Observation {
              id
              existence
              reference {
                label
              }
              title
              instrument
              calibrationRole
            }

            fragment ObservationDetails on Observation {
              ...ObservationCore
              observerNotes
              subtitle
              program {
                ...ProgramCore
              }
              scienceRequirements {
                ...ScienceRequirementsDetails
              }
              scienceBand
              workflow {
                ...WorkflowDetails
              }
              observingMode {
                ...ObservingModeDetails
              }
              constraintSet {
                ...ConstraintSetDetails
              }
              timingWindows {
                ...TimingWindowDetails
              }
              targetEnvironment {
                ...TargetEnvironmentDetails
              }
            }

            fragment ObservingModeDetails on ObservingMode {
              instrument
              mode
              gmosNorthLongSlit {
                ...GmosNorthLongSlitDetails
              }
              gmosSouthLongSlit {
                ...GmosSouthLongSlitDetails
              }
              gmosNorthImaging {
                ...GmosNorthImagingDetails
              }
              gmosSouthImaging {
                ...GmosSouthImagingDetails
              }
              flamingos2LongSlit {
                ...Flamingos2LongSlitDetails
              }
            }

            fragment ProgramCore on Program {
              id
              name
              existence
              description
            }

            fragment ScienceRequirementsDetails on ScienceRequirements {
              mode
            }

            fragment SiderealTargetDetails on Sidereal {
              ra {
                hours
                hms
                degrees
              }
              dec {
                degrees
                dms
              }
              epoch
            }

            fragment TargetEnvironmentDetails on TargetEnvironment {
              asterism {
                name
                sidereal {
                  ...SiderealTargetDetails
                }
                nonsidereal {
                  ...NonsiderealTargetDetails
                }
              }
              explicitBase {
                ra {
                  hms
                }
                dec {
                  dms
                }
              }
            }

            fragment TimingWindowDetails on TimingWindow {
              inclusion
              startUtc
              end {
                __typename
                ... on TimingWindowEndAt {
                  atUtc
                }
                ... on TimingWindowEndAfter {
                  after {
                    seconds
                  }
                  repeat {
                    period {
                      seconds
                    }
                    times
                  }
                }
              }
            }

            fragment WorkflowCore on CalculatedObservationWorkflow {
              state
            }

            fragment WorkflowDetails on CalculatedObservationWorkflow {
              ...WorkflowCore
              value {
                state
                validTransitions
                validationErrors {
                  code
                  messages
                }
              }
            }
            """)
        variables: dict[str, object] = {"observationId": observation_id, "SET": set_}
        response = await self.execute(
            query=query,
            operation_name="updateObservationById",
            variables=variables,
            **kwargs,
        )
        data = self.get_data(response)
        return UpdateObservationById.model_validate(data)

    async def update_observation_by_reference(
        self,
        observation_reference: Any,
        set_: ObservationPropertiesInput,
        **kwargs: Any,
    ) -> UpdateObservationByReference:
        query = gql("""
            mutation updateObservationByReference($observationReference: NonEmptyString!, $SET: ObservationPropertiesInput!) {
              updateObservations(
                input: {SET: $SET, WHERE: {reference: {label: {EQ: $observationReference}}}, LIMIT: 1}
              ) {
                hasMore
                observations {
                  ...ObservationDetails
                }
              }
            }

            fragment ConstraintSetDetails on ConstraintSet {
              imageQuality
              cloudExtinction
              skyBackground
              waterVapor
              elevationRange {
                airMass {
                  min
                  max
                }
                hourAngle {
                  minHours
                  maxHours
                }
              }
            }

            fragment ExposureTimeModeDetails on ExposureTimeMode {
              signalToNoise {
                value
                at {
                  nanometers
                }
              }
              timeAndCount {
                time {
                  seconds
                }
                count
                at {
                  nanometers
                }
              }
            }

            fragment Flamingos2LongSlitDetails on Flamingos2LongSlit {
              decker
              defaultDecker
              defaultOffsets {
                q {
                  arcseconds
                }
                p {
                  arcseconds
                }
              }
              disperser
              filter
              fpu
              telluricType {
                tag
                starTypes
              }
              exposureTimeMode {
                ...ExposureTimeModeDetails
              }
              explicitReadMode
              explicitReads
              explicitDecker
              readoutMode
              defaultReadoutMode
              offsets {
                q {
                  arcseconds
                }
                p {
                  arcseconds
                }
              }
              acquisition {
                exposureTimeMode {
                  ...ExposureTimeModeDetails
                }
              }
              initialDisperser
              initialFilter
              initialFpu
            }

            fragment GmosNorthImagingDetails on GmosNorthImaging {
              filters {
                filter
              }
              bin
            }

            fragment GmosNorthLongSlitDetails on GmosNorthLongSlit {
              grating
              filter
              fpu
              centralWavelength {
                nanometers
              }
              offsets {
                arcseconds
              }
              xBin
              yBin
            }

            fragment GmosSouthImagingDetails on GmosSouthImaging {
              filters {
                filter
              }
              bin
            }

            fragment GmosSouthLongSlitDetails on GmosSouthLongSlit {
              grating
              filter
              fpu
              centralWavelength {
                nanometers
              }
              offsets {
                arcseconds
              }
              xBin
              yBin
            }

            fragment NonsiderealTargetDetails on Nonsidereal {
              des
              keyType
              key
            }

            fragment ObservationCore on Observation {
              id
              existence
              reference {
                label
              }
              title
              instrument
              calibrationRole
            }

            fragment ObservationDetails on Observation {
              ...ObservationCore
              observerNotes
              subtitle
              program {
                ...ProgramCore
              }
              scienceRequirements {
                ...ScienceRequirementsDetails
              }
              scienceBand
              workflow {
                ...WorkflowDetails
              }
              observingMode {
                ...ObservingModeDetails
              }
              constraintSet {
                ...ConstraintSetDetails
              }
              timingWindows {
                ...TimingWindowDetails
              }
              targetEnvironment {
                ...TargetEnvironmentDetails
              }
            }

            fragment ObservingModeDetails on ObservingMode {
              instrument
              mode
              gmosNorthLongSlit {
                ...GmosNorthLongSlitDetails
              }
              gmosSouthLongSlit {
                ...GmosSouthLongSlitDetails
              }
              gmosNorthImaging {
                ...GmosNorthImagingDetails
              }
              gmosSouthImaging {
                ...GmosSouthImagingDetails
              }
              flamingos2LongSlit {
                ...Flamingos2LongSlitDetails
              }
            }

            fragment ProgramCore on Program {
              id
              name
              existence
              description
            }

            fragment ScienceRequirementsDetails on ScienceRequirements {
              mode
            }

            fragment SiderealTargetDetails on Sidereal {
              ra {
                hours
                hms
                degrees
              }
              dec {
                degrees
                dms
              }
              epoch
            }

            fragment TargetEnvironmentDetails on TargetEnvironment {
              asterism {
                name
                sidereal {
                  ...SiderealTargetDetails
                }
                nonsidereal {
                  ...NonsiderealTargetDetails
                }
              }
              explicitBase {
                ra {
                  hms
                }
                dec {
                  dms
                }
              }
            }

            fragment TimingWindowDetails on TimingWindow {
              inclusion
              startUtc
              end {
                __typename
                ... on TimingWindowEndAt {
                  atUtc
                }
                ... on TimingWindowEndAfter {
                  after {
                    seconds
                  }
                  repeat {
                    period {
                      seconds
                    }
                    times
                  }
                }
              }
            }

            fragment WorkflowCore on CalculatedObservationWorkflow {
              state
            }

            fragment WorkflowDetails on CalculatedObservationWorkflow {
              ...WorkflowCore
              value {
                state
                validTransitions
                validationErrors {
                  code
                  messages
                }
              }
            }
            """)
        variables: dict[str, object] = {
            "observationReference": observation_reference,
            "SET": set_,
        }
        response = await self.execute(
            query=query,
            operation_name="updateObservationByReference",
            variables=variables,
            **kwargs,
        )
        data = self.get_data(response)
        return UpdateObservationByReference.model_validate(data)

    async def restore_observation_by_id(
        self, observation_id: Any, **kwargs: Any
    ) -> RestoreObservationById:
        query = gql("""
            mutation restoreObservationById($observationId: ObservationId!) {
              updateObservations(
                input: {SET: {existence: PRESENT}, WHERE: {id: {EQ: $observationId}}, LIMIT: 1, includeDeleted: true}
              ) {
                hasMore
                observations {
                  ...ObservationDetails
                }
              }
            }

            fragment ConstraintSetDetails on ConstraintSet {
              imageQuality
              cloudExtinction
              skyBackground
              waterVapor
              elevationRange {
                airMass {
                  min
                  max
                }
                hourAngle {
                  minHours
                  maxHours
                }
              }
            }

            fragment ExposureTimeModeDetails on ExposureTimeMode {
              signalToNoise {
                value
                at {
                  nanometers
                }
              }
              timeAndCount {
                time {
                  seconds
                }
                count
                at {
                  nanometers
                }
              }
            }

            fragment Flamingos2LongSlitDetails on Flamingos2LongSlit {
              decker
              defaultDecker
              defaultOffsets {
                q {
                  arcseconds
                }
                p {
                  arcseconds
                }
              }
              disperser
              filter
              fpu
              telluricType {
                tag
                starTypes
              }
              exposureTimeMode {
                ...ExposureTimeModeDetails
              }
              explicitReadMode
              explicitReads
              explicitDecker
              readoutMode
              defaultReadoutMode
              offsets {
                q {
                  arcseconds
                }
                p {
                  arcseconds
                }
              }
              acquisition {
                exposureTimeMode {
                  ...ExposureTimeModeDetails
                }
              }
              initialDisperser
              initialFilter
              initialFpu
            }

            fragment GmosNorthImagingDetails on GmosNorthImaging {
              filters {
                filter
              }
              bin
            }

            fragment GmosNorthLongSlitDetails on GmosNorthLongSlit {
              grating
              filter
              fpu
              centralWavelength {
                nanometers
              }
              offsets {
                arcseconds
              }
              xBin
              yBin
            }

            fragment GmosSouthImagingDetails on GmosSouthImaging {
              filters {
                filter
              }
              bin
            }

            fragment GmosSouthLongSlitDetails on GmosSouthLongSlit {
              grating
              filter
              fpu
              centralWavelength {
                nanometers
              }
              offsets {
                arcseconds
              }
              xBin
              yBin
            }

            fragment NonsiderealTargetDetails on Nonsidereal {
              des
              keyType
              key
            }

            fragment ObservationCore on Observation {
              id
              existence
              reference {
                label
              }
              title
              instrument
              calibrationRole
            }

            fragment ObservationDetails on Observation {
              ...ObservationCore
              observerNotes
              subtitle
              program {
                ...ProgramCore
              }
              scienceRequirements {
                ...ScienceRequirementsDetails
              }
              scienceBand
              workflow {
                ...WorkflowDetails
              }
              observingMode {
                ...ObservingModeDetails
              }
              constraintSet {
                ...ConstraintSetDetails
              }
              timingWindows {
                ...TimingWindowDetails
              }
              targetEnvironment {
                ...TargetEnvironmentDetails
              }
            }

            fragment ObservingModeDetails on ObservingMode {
              instrument
              mode
              gmosNorthLongSlit {
                ...GmosNorthLongSlitDetails
              }
              gmosSouthLongSlit {
                ...GmosSouthLongSlitDetails
              }
              gmosNorthImaging {
                ...GmosNorthImagingDetails
              }
              gmosSouthImaging {
                ...GmosSouthImagingDetails
              }
              flamingos2LongSlit {
                ...Flamingos2LongSlitDetails
              }
            }

            fragment ProgramCore on Program {
              id
              name
              existence
              description
            }

            fragment ScienceRequirementsDetails on ScienceRequirements {
              mode
            }

            fragment SiderealTargetDetails on Sidereal {
              ra {
                hours
                hms
                degrees
              }
              dec {
                degrees
                dms
              }
              epoch
            }

            fragment TargetEnvironmentDetails on TargetEnvironment {
              asterism {
                name
                sidereal {
                  ...SiderealTargetDetails
                }
                nonsidereal {
                  ...NonsiderealTargetDetails
                }
              }
              explicitBase {
                ra {
                  hms
                }
                dec {
                  dms
                }
              }
            }

            fragment TimingWindowDetails on TimingWindow {
              inclusion
              startUtc
              end {
                __typename
                ... on TimingWindowEndAt {
                  atUtc
                }
                ... on TimingWindowEndAfter {
                  after {
                    seconds
                  }
                  repeat {
                    period {
                      seconds
                    }
                    times
                  }
                }
              }
            }

            fragment WorkflowCore on CalculatedObservationWorkflow {
              state
            }

            fragment WorkflowDetails on CalculatedObservationWorkflow {
              ...WorkflowCore
              value {
                state
                validTransitions
                validationErrors {
                  code
                  messages
                }
              }
            }
            """)
        variables: dict[str, object] = {"observationId": observation_id}
        response = await self.execute(
            query=query,
            operation_name="restoreObservationById",
            variables=variables,
            **kwargs,
        )
        data = self.get_data(response)
        return RestoreObservationById.model_validate(data)

    async def restore_observation_by_reference(
        self, observation_reference: Any, **kwargs: Any
    ) -> RestoreObservationByReference:
        query = gql("""
            mutation restoreObservationByReference($observationReference: NonEmptyString!) {
              updateObservations(
                input: {SET: {existence: PRESENT}, WHERE: {reference: {label: {EQ: $observationReference}}}, LIMIT: 1, includeDeleted: true}
              ) {
                hasMore
                observations {
                  ...ObservationDetails
                }
              }
            }

            fragment ConstraintSetDetails on ConstraintSet {
              imageQuality
              cloudExtinction
              skyBackground
              waterVapor
              elevationRange {
                airMass {
                  min
                  max
                }
                hourAngle {
                  minHours
                  maxHours
                }
              }
            }

            fragment ExposureTimeModeDetails on ExposureTimeMode {
              signalToNoise {
                value
                at {
                  nanometers
                }
              }
              timeAndCount {
                time {
                  seconds
                }
                count
                at {
                  nanometers
                }
              }
            }

            fragment Flamingos2LongSlitDetails on Flamingos2LongSlit {
              decker
              defaultDecker
              defaultOffsets {
                q {
                  arcseconds
                }
                p {
                  arcseconds
                }
              }
              disperser
              filter
              fpu
              telluricType {
                tag
                starTypes
              }
              exposureTimeMode {
                ...ExposureTimeModeDetails
              }
              explicitReadMode
              explicitReads
              explicitDecker
              readoutMode
              defaultReadoutMode
              offsets {
                q {
                  arcseconds
                }
                p {
                  arcseconds
                }
              }
              acquisition {
                exposureTimeMode {
                  ...ExposureTimeModeDetails
                }
              }
              initialDisperser
              initialFilter
              initialFpu
            }

            fragment GmosNorthImagingDetails on GmosNorthImaging {
              filters {
                filter
              }
              bin
            }

            fragment GmosNorthLongSlitDetails on GmosNorthLongSlit {
              grating
              filter
              fpu
              centralWavelength {
                nanometers
              }
              offsets {
                arcseconds
              }
              xBin
              yBin
            }

            fragment GmosSouthImagingDetails on GmosSouthImaging {
              filters {
                filter
              }
              bin
            }

            fragment GmosSouthLongSlitDetails on GmosSouthLongSlit {
              grating
              filter
              fpu
              centralWavelength {
                nanometers
              }
              offsets {
                arcseconds
              }
              xBin
              yBin
            }

            fragment NonsiderealTargetDetails on Nonsidereal {
              des
              keyType
              key
            }

            fragment ObservationCore on Observation {
              id
              existence
              reference {
                label
              }
              title
              instrument
              calibrationRole
            }

            fragment ObservationDetails on Observation {
              ...ObservationCore
              observerNotes
              subtitle
              program {
                ...ProgramCore
              }
              scienceRequirements {
                ...ScienceRequirementsDetails
              }
              scienceBand
              workflow {
                ...WorkflowDetails
              }
              observingMode {
                ...ObservingModeDetails
              }
              constraintSet {
                ...ConstraintSetDetails
              }
              timingWindows {
                ...TimingWindowDetails
              }
              targetEnvironment {
                ...TargetEnvironmentDetails
              }
            }

            fragment ObservingModeDetails on ObservingMode {
              instrument
              mode
              gmosNorthLongSlit {
                ...GmosNorthLongSlitDetails
              }
              gmosSouthLongSlit {
                ...GmosSouthLongSlitDetails
              }
              gmosNorthImaging {
                ...GmosNorthImagingDetails
              }
              gmosSouthImaging {
                ...GmosSouthImagingDetails
              }
              flamingos2LongSlit {
                ...Flamingos2LongSlitDetails
              }
            }

            fragment ProgramCore on Program {
              id
              name
              existence
              description
            }

            fragment ScienceRequirementsDetails on ScienceRequirements {
              mode
            }

            fragment SiderealTargetDetails on Sidereal {
              ra {
                hours
                hms
                degrees
              }
              dec {
                degrees
                dms
              }
              epoch
            }

            fragment TargetEnvironmentDetails on TargetEnvironment {
              asterism {
                name
                sidereal {
                  ...SiderealTargetDetails
                }
                nonsidereal {
                  ...NonsiderealTargetDetails
                }
              }
              explicitBase {
                ra {
                  hms
                }
                dec {
                  dms
                }
              }
            }

            fragment TimingWindowDetails on TimingWindow {
              inclusion
              startUtc
              end {
                __typename
                ... on TimingWindowEndAt {
                  atUtc
                }
                ... on TimingWindowEndAfter {
                  after {
                    seconds
                  }
                  repeat {
                    period {
                      seconds
                    }
                    times
                  }
                }
              }
            }

            fragment WorkflowCore on CalculatedObservationWorkflow {
              state
            }

            fragment WorkflowDetails on CalculatedObservationWorkflow {
              ...WorkflowCore
              value {
                state
                validTransitions
                validationErrors {
                  code
                  messages
                }
              }
            }
            """)
        variables: dict[str, object] = {"observationReference": observation_reference}
        response = await self.execute(
            query=query,
            operation_name="restoreObservationByReference",
            variables=variables,
            **kwargs,
        )
        data = self.get_data(response)
        return RestoreObservationByReference.model_validate(data)

    async def delete_observation_by_id(
        self, observation_id: Any, **kwargs: Any
    ) -> DeleteObservationById:
        query = gql("""
            mutation deleteObservationById($observationId: ObservationId!) {
              updateObservations(
                input: {SET: {existence: DELETED}, WHERE: {id: {EQ: $observationId}}, LIMIT: 1}
              ) {
                hasMore
                observations {
                  ...ObservationDetails
                }
              }
            }

            fragment ConstraintSetDetails on ConstraintSet {
              imageQuality
              cloudExtinction
              skyBackground
              waterVapor
              elevationRange {
                airMass {
                  min
                  max
                }
                hourAngle {
                  minHours
                  maxHours
                }
              }
            }

            fragment ExposureTimeModeDetails on ExposureTimeMode {
              signalToNoise {
                value
                at {
                  nanometers
                }
              }
              timeAndCount {
                time {
                  seconds
                }
                count
                at {
                  nanometers
                }
              }
            }

            fragment Flamingos2LongSlitDetails on Flamingos2LongSlit {
              decker
              defaultDecker
              defaultOffsets {
                q {
                  arcseconds
                }
                p {
                  arcseconds
                }
              }
              disperser
              filter
              fpu
              telluricType {
                tag
                starTypes
              }
              exposureTimeMode {
                ...ExposureTimeModeDetails
              }
              explicitReadMode
              explicitReads
              explicitDecker
              readoutMode
              defaultReadoutMode
              offsets {
                q {
                  arcseconds
                }
                p {
                  arcseconds
                }
              }
              acquisition {
                exposureTimeMode {
                  ...ExposureTimeModeDetails
                }
              }
              initialDisperser
              initialFilter
              initialFpu
            }

            fragment GmosNorthImagingDetails on GmosNorthImaging {
              filters {
                filter
              }
              bin
            }

            fragment GmosNorthLongSlitDetails on GmosNorthLongSlit {
              grating
              filter
              fpu
              centralWavelength {
                nanometers
              }
              offsets {
                arcseconds
              }
              xBin
              yBin
            }

            fragment GmosSouthImagingDetails on GmosSouthImaging {
              filters {
                filter
              }
              bin
            }

            fragment GmosSouthLongSlitDetails on GmosSouthLongSlit {
              grating
              filter
              fpu
              centralWavelength {
                nanometers
              }
              offsets {
                arcseconds
              }
              xBin
              yBin
            }

            fragment NonsiderealTargetDetails on Nonsidereal {
              des
              keyType
              key
            }

            fragment ObservationCore on Observation {
              id
              existence
              reference {
                label
              }
              title
              instrument
              calibrationRole
            }

            fragment ObservationDetails on Observation {
              ...ObservationCore
              observerNotes
              subtitle
              program {
                ...ProgramCore
              }
              scienceRequirements {
                ...ScienceRequirementsDetails
              }
              scienceBand
              workflow {
                ...WorkflowDetails
              }
              observingMode {
                ...ObservingModeDetails
              }
              constraintSet {
                ...ConstraintSetDetails
              }
              timingWindows {
                ...TimingWindowDetails
              }
              targetEnvironment {
                ...TargetEnvironmentDetails
              }
            }

            fragment ObservingModeDetails on ObservingMode {
              instrument
              mode
              gmosNorthLongSlit {
                ...GmosNorthLongSlitDetails
              }
              gmosSouthLongSlit {
                ...GmosSouthLongSlitDetails
              }
              gmosNorthImaging {
                ...GmosNorthImagingDetails
              }
              gmosSouthImaging {
                ...GmosSouthImagingDetails
              }
              flamingos2LongSlit {
                ...Flamingos2LongSlitDetails
              }
            }

            fragment ProgramCore on Program {
              id
              name
              existence
              description
            }

            fragment ScienceRequirementsDetails on ScienceRequirements {
              mode
            }

            fragment SiderealTargetDetails on Sidereal {
              ra {
                hours
                hms
                degrees
              }
              dec {
                degrees
                dms
              }
              epoch
            }

            fragment TargetEnvironmentDetails on TargetEnvironment {
              asterism {
                name
                sidereal {
                  ...SiderealTargetDetails
                }
                nonsidereal {
                  ...NonsiderealTargetDetails
                }
              }
              explicitBase {
                ra {
                  hms
                }
                dec {
                  dms
                }
              }
            }

            fragment TimingWindowDetails on TimingWindow {
              inclusion
              startUtc
              end {
                __typename
                ... on TimingWindowEndAt {
                  atUtc
                }
                ... on TimingWindowEndAfter {
                  after {
                    seconds
                  }
                  repeat {
                    period {
                      seconds
                    }
                    times
                  }
                }
              }
            }

            fragment WorkflowCore on CalculatedObservationWorkflow {
              state
            }

            fragment WorkflowDetails on CalculatedObservationWorkflow {
              ...WorkflowCore
              value {
                state
                validTransitions
                validationErrors {
                  code
                  messages
                }
              }
            }
            """)
        variables: dict[str, object] = {"observationId": observation_id}
        response = await self.execute(
            query=query,
            operation_name="deleteObservationById",
            variables=variables,
            **kwargs,
        )
        data = self.get_data(response)
        return DeleteObservationById.model_validate(data)

    async def delete_observation_by_reference(
        self, observation_reference: Any, **kwargs: Any
    ) -> DeleteObservationByReference:
        query = gql("""
            mutation deleteObservationByReference($observationReference: NonEmptyString!) {
              updateObservations(
                input: {SET: {existence: DELETED}, WHERE: {reference: {label: {EQ: $observationReference}}}, LIMIT: 1}
              ) {
                hasMore
                observations {
                  ...ObservationDetails
                }
              }
            }

            fragment ConstraintSetDetails on ConstraintSet {
              imageQuality
              cloudExtinction
              skyBackground
              waterVapor
              elevationRange {
                airMass {
                  min
                  max
                }
                hourAngle {
                  minHours
                  maxHours
                }
              }
            }

            fragment ExposureTimeModeDetails on ExposureTimeMode {
              signalToNoise {
                value
                at {
                  nanometers
                }
              }
              timeAndCount {
                time {
                  seconds
                }
                count
                at {
                  nanometers
                }
              }
            }

            fragment Flamingos2LongSlitDetails on Flamingos2LongSlit {
              decker
              defaultDecker
              defaultOffsets {
                q {
                  arcseconds
                }
                p {
                  arcseconds
                }
              }
              disperser
              filter
              fpu
              telluricType {
                tag
                starTypes
              }
              exposureTimeMode {
                ...ExposureTimeModeDetails
              }
              explicitReadMode
              explicitReads
              explicitDecker
              readoutMode
              defaultReadoutMode
              offsets {
                q {
                  arcseconds
                }
                p {
                  arcseconds
                }
              }
              acquisition {
                exposureTimeMode {
                  ...ExposureTimeModeDetails
                }
              }
              initialDisperser
              initialFilter
              initialFpu
            }

            fragment GmosNorthImagingDetails on GmosNorthImaging {
              filters {
                filter
              }
              bin
            }

            fragment GmosNorthLongSlitDetails on GmosNorthLongSlit {
              grating
              filter
              fpu
              centralWavelength {
                nanometers
              }
              offsets {
                arcseconds
              }
              xBin
              yBin
            }

            fragment GmosSouthImagingDetails on GmosSouthImaging {
              filters {
                filter
              }
              bin
            }

            fragment GmosSouthLongSlitDetails on GmosSouthLongSlit {
              grating
              filter
              fpu
              centralWavelength {
                nanometers
              }
              offsets {
                arcseconds
              }
              xBin
              yBin
            }

            fragment NonsiderealTargetDetails on Nonsidereal {
              des
              keyType
              key
            }

            fragment ObservationCore on Observation {
              id
              existence
              reference {
                label
              }
              title
              instrument
              calibrationRole
            }

            fragment ObservationDetails on Observation {
              ...ObservationCore
              observerNotes
              subtitle
              program {
                ...ProgramCore
              }
              scienceRequirements {
                ...ScienceRequirementsDetails
              }
              scienceBand
              workflow {
                ...WorkflowDetails
              }
              observingMode {
                ...ObservingModeDetails
              }
              constraintSet {
                ...ConstraintSetDetails
              }
              timingWindows {
                ...TimingWindowDetails
              }
              targetEnvironment {
                ...TargetEnvironmentDetails
              }
            }

            fragment ObservingModeDetails on ObservingMode {
              instrument
              mode
              gmosNorthLongSlit {
                ...GmosNorthLongSlitDetails
              }
              gmosSouthLongSlit {
                ...GmosSouthLongSlitDetails
              }
              gmosNorthImaging {
                ...GmosNorthImagingDetails
              }
              gmosSouthImaging {
                ...GmosSouthImagingDetails
              }
              flamingos2LongSlit {
                ...Flamingos2LongSlitDetails
              }
            }

            fragment ProgramCore on Program {
              id
              name
              existence
              description
            }

            fragment ScienceRequirementsDetails on ScienceRequirements {
              mode
            }

            fragment SiderealTargetDetails on Sidereal {
              ra {
                hours
                hms
                degrees
              }
              dec {
                degrees
                dms
              }
              epoch
            }

            fragment TargetEnvironmentDetails on TargetEnvironment {
              asterism {
                name
                sidereal {
                  ...SiderealTargetDetails
                }
                nonsidereal {
                  ...NonsiderealTargetDetails
                }
              }
              explicitBase {
                ra {
                  hms
                }
                dec {
                  dms
                }
              }
            }

            fragment TimingWindowDetails on TimingWindow {
              inclusion
              startUtc
              end {
                __typename
                ... on TimingWindowEndAt {
                  atUtc
                }
                ... on TimingWindowEndAfter {
                  after {
                    seconds
                  }
                  repeat {
                    period {
                      seconds
                    }
                    times
                  }
                }
              }
            }

            fragment WorkflowCore on CalculatedObservationWorkflow {
              state
            }

            fragment WorkflowDetails on CalculatedObservationWorkflow {
              ...WorkflowCore
              value {
                state
                validTransitions
                validationErrors {
                  code
                  messages
                }
              }
            }
            """)
        variables: dict[str, object] = {"observationReference": observation_reference}
        response = await self.execute(
            query=query,
            operation_name="deleteObservationByReference",
            variables=variables,
            **kwargs,
        )
        data = self.get_data(response)
        return DeleteObservationByReference.model_validate(data)

    async def get_observation(
        self,
        observation_id: Union[Optional[Any], UnsetType] = UNSET,
        observation_reference: Union[Optional[Any], UnsetType] = UNSET,
        **kwargs: Any,
    ) -> GetObservation:
        query = gql("""
            query getObservation($observationId: ObservationId, $observationReference: ObservationReferenceLabel) {
              observation(
                observationId: $observationId
                observationReference: $observationReference
              ) {
                ...ObservationDetails
              }
            }

            fragment ConstraintSetDetails on ConstraintSet {
              imageQuality
              cloudExtinction
              skyBackground
              waterVapor
              elevationRange {
                airMass {
                  min
                  max
                }
                hourAngle {
                  minHours
                  maxHours
                }
              }
            }

            fragment ExposureTimeModeDetails on ExposureTimeMode {
              signalToNoise {
                value
                at {
                  nanometers
                }
              }
              timeAndCount {
                time {
                  seconds
                }
                count
                at {
                  nanometers
                }
              }
            }

            fragment Flamingos2LongSlitDetails on Flamingos2LongSlit {
              decker
              defaultDecker
              defaultOffsets {
                q {
                  arcseconds
                }
                p {
                  arcseconds
                }
              }
              disperser
              filter
              fpu
              telluricType {
                tag
                starTypes
              }
              exposureTimeMode {
                ...ExposureTimeModeDetails
              }
              explicitReadMode
              explicitReads
              explicitDecker
              readoutMode
              defaultReadoutMode
              offsets {
                q {
                  arcseconds
                }
                p {
                  arcseconds
                }
              }
              acquisition {
                exposureTimeMode {
                  ...ExposureTimeModeDetails
                }
              }
              initialDisperser
              initialFilter
              initialFpu
            }

            fragment GmosNorthImagingDetails on GmosNorthImaging {
              filters {
                filter
              }
              bin
            }

            fragment GmosNorthLongSlitDetails on GmosNorthLongSlit {
              grating
              filter
              fpu
              centralWavelength {
                nanometers
              }
              offsets {
                arcseconds
              }
              xBin
              yBin
            }

            fragment GmosSouthImagingDetails on GmosSouthImaging {
              filters {
                filter
              }
              bin
            }

            fragment GmosSouthLongSlitDetails on GmosSouthLongSlit {
              grating
              filter
              fpu
              centralWavelength {
                nanometers
              }
              offsets {
                arcseconds
              }
              xBin
              yBin
            }

            fragment NonsiderealTargetDetails on Nonsidereal {
              des
              keyType
              key
            }

            fragment ObservationCore on Observation {
              id
              existence
              reference {
                label
              }
              title
              instrument
              calibrationRole
            }

            fragment ObservationDetails on Observation {
              ...ObservationCore
              observerNotes
              subtitle
              program {
                ...ProgramCore
              }
              scienceRequirements {
                ...ScienceRequirementsDetails
              }
              scienceBand
              workflow {
                ...WorkflowDetails
              }
              observingMode {
                ...ObservingModeDetails
              }
              constraintSet {
                ...ConstraintSetDetails
              }
              timingWindows {
                ...TimingWindowDetails
              }
              targetEnvironment {
                ...TargetEnvironmentDetails
              }
            }

            fragment ObservingModeDetails on ObservingMode {
              instrument
              mode
              gmosNorthLongSlit {
                ...GmosNorthLongSlitDetails
              }
              gmosSouthLongSlit {
                ...GmosSouthLongSlitDetails
              }
              gmosNorthImaging {
                ...GmosNorthImagingDetails
              }
              gmosSouthImaging {
                ...GmosSouthImagingDetails
              }
              flamingos2LongSlit {
                ...Flamingos2LongSlitDetails
              }
            }

            fragment ProgramCore on Program {
              id
              name
              existence
              description
            }

            fragment ScienceRequirementsDetails on ScienceRequirements {
              mode
            }

            fragment SiderealTargetDetails on Sidereal {
              ra {
                hours
                hms
                degrees
              }
              dec {
                degrees
                dms
              }
              epoch
            }

            fragment TargetEnvironmentDetails on TargetEnvironment {
              asterism {
                name
                sidereal {
                  ...SiderealTargetDetails
                }
                nonsidereal {
                  ...NonsiderealTargetDetails
                }
              }
              explicitBase {
                ra {
                  hms
                }
                dec {
                  dms
                }
              }
            }

            fragment TimingWindowDetails on TimingWindow {
              inclusion
              startUtc
              end {
                __typename
                ... on TimingWindowEndAt {
                  atUtc
                }
                ... on TimingWindowEndAfter {
                  after {
                    seconds
                  }
                  repeat {
                    period {
                      seconds
                    }
                    times
                  }
                }
              }
            }

            fragment WorkflowCore on CalculatedObservationWorkflow {
              state
            }

            fragment WorkflowDetails on CalculatedObservationWorkflow {
              ...WorkflowCore
              value {
                state
                validTransitions
                validationErrors {
                  code
                  messages
                }
              }
            }
            """)
        variables: dict[str, object] = {
            "observationId": observation_id,
            "observationReference": observation_reference,
        }
        response = await self.execute(
            query=query, operation_name="getObservation", variables=variables, **kwargs
        )
        data = self.get_data(response)
        return GetObservation.model_validate(data)

    async def get_observations(
        self,
        include_deleted: bool,
        where: Union[Optional[WhereObservation], UnsetType] = UNSET,
        offset: Union[Optional[Any], UnsetType] = UNSET,
        limit: Union[Optional[Any], UnsetType] = UNSET,
        **kwargs: Any,
    ) -> GetObservations:
        query = gql("""
            query getObservations($WHERE: WhereObservation, $OFFSET: ObservationId, $LIMIT: NonNegInt, $includeDeleted: Boolean! = false) {
              observations(
                WHERE: $WHERE
                OFFSET: $OFFSET
                LIMIT: $LIMIT
                includeDeleted: $includeDeleted
              ) {
                hasMore
                matches {
                  ...ObservationDetails
                }
              }
            }

            fragment ConstraintSetDetails on ConstraintSet {
              imageQuality
              cloudExtinction
              skyBackground
              waterVapor
              elevationRange {
                airMass {
                  min
                  max
                }
                hourAngle {
                  minHours
                  maxHours
                }
              }
            }

            fragment ExposureTimeModeDetails on ExposureTimeMode {
              signalToNoise {
                value
                at {
                  nanometers
                }
              }
              timeAndCount {
                time {
                  seconds
                }
                count
                at {
                  nanometers
                }
              }
            }

            fragment Flamingos2LongSlitDetails on Flamingos2LongSlit {
              decker
              defaultDecker
              defaultOffsets {
                q {
                  arcseconds
                }
                p {
                  arcseconds
                }
              }
              disperser
              filter
              fpu
              telluricType {
                tag
                starTypes
              }
              exposureTimeMode {
                ...ExposureTimeModeDetails
              }
              explicitReadMode
              explicitReads
              explicitDecker
              readoutMode
              defaultReadoutMode
              offsets {
                q {
                  arcseconds
                }
                p {
                  arcseconds
                }
              }
              acquisition {
                exposureTimeMode {
                  ...ExposureTimeModeDetails
                }
              }
              initialDisperser
              initialFilter
              initialFpu
            }

            fragment GmosNorthImagingDetails on GmosNorthImaging {
              filters {
                filter
              }
              bin
            }

            fragment GmosNorthLongSlitDetails on GmosNorthLongSlit {
              grating
              filter
              fpu
              centralWavelength {
                nanometers
              }
              offsets {
                arcseconds
              }
              xBin
              yBin
            }

            fragment GmosSouthImagingDetails on GmosSouthImaging {
              filters {
                filter
              }
              bin
            }

            fragment GmosSouthLongSlitDetails on GmosSouthLongSlit {
              grating
              filter
              fpu
              centralWavelength {
                nanometers
              }
              offsets {
                arcseconds
              }
              xBin
              yBin
            }

            fragment NonsiderealTargetDetails on Nonsidereal {
              des
              keyType
              key
            }

            fragment ObservationCore on Observation {
              id
              existence
              reference {
                label
              }
              title
              instrument
              calibrationRole
            }

            fragment ObservationDetails on Observation {
              ...ObservationCore
              observerNotes
              subtitle
              program {
                ...ProgramCore
              }
              scienceRequirements {
                ...ScienceRequirementsDetails
              }
              scienceBand
              workflow {
                ...WorkflowDetails
              }
              observingMode {
                ...ObservingModeDetails
              }
              constraintSet {
                ...ConstraintSetDetails
              }
              timingWindows {
                ...TimingWindowDetails
              }
              targetEnvironment {
                ...TargetEnvironmentDetails
              }
            }

            fragment ObservingModeDetails on ObservingMode {
              instrument
              mode
              gmosNorthLongSlit {
                ...GmosNorthLongSlitDetails
              }
              gmosSouthLongSlit {
                ...GmosSouthLongSlitDetails
              }
              gmosNorthImaging {
                ...GmosNorthImagingDetails
              }
              gmosSouthImaging {
                ...GmosSouthImagingDetails
              }
              flamingos2LongSlit {
                ...Flamingos2LongSlitDetails
              }
            }

            fragment ProgramCore on Program {
              id
              name
              existence
              description
            }

            fragment ScienceRequirementsDetails on ScienceRequirements {
              mode
            }

            fragment SiderealTargetDetails on Sidereal {
              ra {
                hours
                hms
                degrees
              }
              dec {
                degrees
                dms
              }
              epoch
            }

            fragment TargetEnvironmentDetails on TargetEnvironment {
              asterism {
                name
                sidereal {
                  ...SiderealTargetDetails
                }
                nonsidereal {
                  ...NonsiderealTargetDetails
                }
              }
              explicitBase {
                ra {
                  hms
                }
                dec {
                  dms
                }
              }
            }

            fragment TimingWindowDetails on TimingWindow {
              inclusion
              startUtc
              end {
                __typename
                ... on TimingWindowEndAt {
                  atUtc
                }
                ... on TimingWindowEndAfter {
                  after {
                    seconds
                  }
                  repeat {
                    period {
                      seconds
                    }
                    times
                  }
                }
              }
            }

            fragment WorkflowCore on CalculatedObservationWorkflow {
              state
            }

            fragment WorkflowDetails on CalculatedObservationWorkflow {
              ...WorkflowCore
              value {
                state
                validTransitions
                validationErrors {
                  code
                  messages
                }
              }
            }
            """)
        variables: dict[str, object] = {
            "WHERE": where,
            "OFFSET": offset,
            "LIMIT": limit,
            "includeDeleted": include_deleted,
        }
        response = await self.execute(
            query=query, operation_name="getObservations", variables=variables, **kwargs
        )
        data = self.get_data(response)
        return GetObservations.model_validate(data)

    async def observation_edit(
        self, program_id: Union[Optional[Any], UnsetType] = UNSET, **kwargs: Any
    ) -> AsyncIterator[ObservationEdit]:
        query = gql("""
            subscription ObservationEdit($programId: ProgramId) {
              observationEdit(input: {programId: $programId}) {
                editType
                observationId
                value {
                  id
                  existence
                  reference {
                    label
                  }
                  calibrationRole
                  instrument
                  index
                  title
                  subtitle
                  scienceRequirements {
                    mode
                  }
                  scienceBand
                  observingMode {
                    instrument
                    mode
                    gmosNorthLongSlit {
                      grating
                      filter
                      fpu
                      centralWavelength {
                        nanometers
                      }
                    }
                    gmosSouthLongSlit {
                      grating
                      filter
                      fpu
                      centralWavelength {
                        nanometers
                      }
                    }
                  }
                  constraintSet {
                    imageQuality
                    cloudExtinction
                    skyBackground
                    waterVapor
                    elevationRange {
                      airMass {
                        min
                        max
                      }
                      hourAngle {
                        minHours
                        maxHours
                      }
                    }
                  }
                  timingWindows {
                    inclusion
                    startUtc
                    end {
                      __typename
                      ... on TimingWindowEndAt {
                        atUtc
                      }
                      ... on TimingWindowEndAfter {
                        after {
                          seconds
                        }
                        repeat {
                          period {
                            seconds
                          }
                          times
                        }
                      }
                    }
                  }
                  targetEnvironment {
                    asterism {
                      sidereal {
                        ra {
                          hms
                        }
                        dec {
                          dms
                        }
                        epoch
                      }
                      nonsidereal {
                        des
                      }
                      name
                    }
                    explicitBase {
                      ra {
                        hms
                      }
                      dec {
                        dms
                      }
                    }
                  }
                }
              }
            }
            """)
        variables: dict[str, object] = {"programId": program_id}
        async for data in self.execute_ws(
            query=query, operation_name="ObservationEdit", variables=variables, **kwargs
        ):
            yield ObservationEdit.model_validate(data)

    async def obs_calculation_update(
        self, program_id: Union[Optional[Any], UnsetType] = UNSET, **kwargs: Any
    ) -> AsyncIterator[ObsCalculationUpdate]:
        query = gql("""
            subscription ObsCalculationUpdate($programId: ProgramId) {
              obscalcUpdate(input: {programId: $programId}) {
                editType
                newCalculationState
                observationId
                oldCalculationState
                value {
                  id
                  observationTime
                  execution {
                    visits {
                      matches {
                        observation {
                          id
                        }
                        atomRecords {
                          matches {
                            executionState
                            id
                          }
                        }
                      }
                    }
                  }
                }
              }
            }
            """)
        variables: dict[str, object] = {"programId": program_id}
        async for data in self.execute_ws(
            query=query,
            operation_name="ObsCalculationUpdate",
            variables=variables,
            **kwargs,
        ):
            yield ObsCalculationUpdate.model_validate(data)

    async def create_program(
        self,
        include_deleted: bool,
        properties: Union[Optional[ProgramPropertiesInput], UnsetType] = UNSET,
        **kwargs: Any,
    ) -> CreateProgram:
        query = gql("""
            mutation createProgram($properties: ProgramPropertiesInput, $includeDeleted: Boolean! = false) {
              createProgram(input: {SET: $properties}) {
                program {
                  ...ProgramDetail
                  ...ProgramGroupElements
                }
              }
            }

            fragment ProgramCore on Program {
              id
              name
              existence
              description
            }

            fragment ProgramDetail on Program {
              ...ProgramCore
              type
              active {
                start
                end
              }
              proposalStatus
              proposal {
                call {
                  semester
                  active {
                    start
                    end
                  }
                }
              }
              pi {
                id
              }
            }

            fragment ProgramGroupElements on Program {
              allGroupElements(includeDeleted: $includeDeleted) {
                parentGroupId
                observation {
                  id
                  groupId
                }
                group {
                  id
                  name
                  minimumRequired
                  ordered
                  parentId
                  parentIndex
                  minimumInterval {
                    seconds
                  }
                  maximumInterval {
                    seconds
                  }
                  system
                }
              }
            }
            """)
        variables: dict[str, object] = {
            "properties": properties,
            "includeDeleted": include_deleted,
        }
        response = await self.execute(
            query=query, operation_name="createProgram", variables=variables, **kwargs
        )
        data = self.get_data(response)
        return CreateProgram.model_validate(data)

    async def update_programs(
        self,
        properties: ProgramPropertiesInput,
        include_deleted: bool,
        where: Union[Optional[WhereProgram], UnsetType] = UNSET,
        limit: Union[Optional[Any], UnsetType] = UNSET,
        **kwargs: Any,
    ) -> UpdatePrograms:
        query = gql("""
            mutation updatePrograms($properties: ProgramPropertiesInput!, $where: WhereProgram, $limit: NonNegInt, $includeDeleted: Boolean! = false) {
              updatePrograms(
                input: {SET: $properties, WHERE: $where, LIMIT: $limit, includeDeleted: $includeDeleted}
              ) {
                hasMore
                programs {
                  ...ProgramDetail
                  ...ProgramGroupElements
                }
              }
            }

            fragment ProgramCore on Program {
              id
              name
              existence
              description
            }

            fragment ProgramDetail on Program {
              ...ProgramCore
              type
              active {
                start
                end
              }
              proposalStatus
              proposal {
                call {
                  semester
                  active {
                    start
                    end
                  }
                }
              }
              pi {
                id
              }
            }

            fragment ProgramGroupElements on Program {
              allGroupElements(includeDeleted: $includeDeleted) {
                parentGroupId
                observation {
                  id
                  groupId
                }
                group {
                  id
                  name
                  minimumRequired
                  ordered
                  parentId
                  parentIndex
                  minimumInterval {
                    seconds
                  }
                  maximumInterval {
                    seconds
                  }
                  system
                }
              }
            }
            """)
        variables: dict[str, object] = {
            "properties": properties,
            "where": where,
            "limit": limit,
            "includeDeleted": include_deleted,
        }
        response = await self.execute(
            query=query, operation_name="updatePrograms", variables=variables, **kwargs
        )
        data = self.get_data(response)
        return UpdatePrograms.model_validate(data)

    async def update_program_by_id(
        self,
        program_id: Any,
        properties: ProgramPropertiesInput,
        include_deleted: bool,
        **kwargs: Any,
    ) -> UpdateProgramById:
        query = gql("""
            mutation updateProgramById($programId: ProgramId!, $properties: ProgramPropertiesInput!, $includeDeleted: Boolean! = false) {
              updatePrograms(
                input: {SET: $properties, WHERE: {id: {EQ: $programId}}, LIMIT: 1, includeDeleted: $includeDeleted}
              ) {
                hasMore
                programs {
                  ...ProgramDetail
                  ...ProgramGroupElements
                }
              }
            }

            fragment ProgramCore on Program {
              id
              name
              existence
              description
            }

            fragment ProgramDetail on Program {
              ...ProgramCore
              type
              active {
                start
                end
              }
              proposalStatus
              proposal {
                call {
                  semester
                  active {
                    start
                    end
                  }
                }
              }
              pi {
                id
              }
            }

            fragment ProgramGroupElements on Program {
              allGroupElements(includeDeleted: $includeDeleted) {
                parentGroupId
                observation {
                  id
                  groupId
                }
                group {
                  id
                  name
                  minimumRequired
                  ordered
                  parentId
                  parentIndex
                  minimumInterval {
                    seconds
                  }
                  maximumInterval {
                    seconds
                  }
                  system
                }
              }
            }
            """)
        variables: dict[str, object] = {
            "programId": program_id,
            "properties": properties,
            "includeDeleted": include_deleted,
        }
        response = await self.execute(
            query=query,
            operation_name="updateProgramById",
            variables=variables,
            **kwargs,
        )
        data = self.get_data(response)
        return UpdateProgramById.model_validate(data)

    async def restore_program_by_id(
        self, program_id: Any, **kwargs: Any
    ) -> RestoreProgramById:
        query = gql("""
            mutation restoreProgramById($programId: ProgramId!) {
              updatePrograms(
                input: {SET: {existence: PRESENT}, WHERE: {id: {EQ: $programId}}, LIMIT: 1, includeDeleted: true}
              ) {
                hasMore
                programs {
                  ...ProgramDetail
                  allGroupElements(includeDeleted: true) {
                    parentGroupId
                    observation {
                      id
                      groupId
                    }
                    group {
                      id
                      name
                      minimumRequired
                      ordered
                      parentId
                      parentIndex
                      minimumInterval {
                        seconds
                      }
                      maximumInterval {
                        seconds
                      }
                      system
                    }
                  }
                }
              }
            }

            fragment ProgramCore on Program {
              id
              name
              existence
              description
            }

            fragment ProgramDetail on Program {
              ...ProgramCore
              type
              active {
                start
                end
              }
              proposalStatus
              proposal {
                call {
                  semester
                  active {
                    start
                    end
                  }
                }
              }
              pi {
                id
              }
            }
            """)
        variables: dict[str, object] = {"programId": program_id}
        response = await self.execute(
            query=query,
            operation_name="restoreProgramById",
            variables=variables,
            **kwargs,
        )
        data = self.get_data(response)
        return RestoreProgramById.model_validate(data)

    async def delete_program_by_id(
        self, program_id: Any, **kwargs: Any
    ) -> DeleteProgramById:
        query = gql("""
            mutation deleteProgramById($programId: ProgramId!) {
              updatePrograms(
                input: {SET: {existence: DELETED}, WHERE: {id: {EQ: $programId}}, LIMIT: 1, includeDeleted: false}
              ) {
                hasMore
                programs {
                  ...ProgramDetail
                  allGroupElements(includeDeleted: false) {
                    parentGroupId
                    observation {
                      id
                      groupId
                    }
                    group {
                      id
                      name
                      minimumRequired
                      ordered
                      parentId
                      parentIndex
                      minimumInterval {
                        seconds
                      }
                      maximumInterval {
                        seconds
                      }
                      system
                    }
                  }
                }
              }
            }

            fragment ProgramCore on Program {
              id
              name
              existence
              description
            }

            fragment ProgramDetail on Program {
              ...ProgramCore
              type
              active {
                start
                end
              }
              proposalStatus
              proposal {
                call {
                  semester
                  active {
                    start
                    end
                  }
                }
              }
              pi {
                id
              }
            }
            """)
        variables: dict[str, object] = {"programId": program_id}
        response = await self.execute(
            query=query,
            operation_name="deleteProgramById",
            variables=variables,
            **kwargs,
        )
        data = self.get_data(response)
        return DeleteProgramById.model_validate(data)

    async def get_program_by_id(
        self, program_id: Any, include_deleted: bool, **kwargs: Any
    ) -> GetProgramById:
        query = gql("""
            query getProgramById($programId: ProgramId!, $includeDeleted: Boolean! = false) {
              program(programId: $programId) {
                ...ProgramDetail
                ...ProgramGroupElements
              }
            }

            fragment ProgramCore on Program {
              id
              name
              existence
              description
            }

            fragment ProgramDetail on Program {
              ...ProgramCore
              type
              active {
                start
                end
              }
              proposalStatus
              proposal {
                call {
                  semester
                  active {
                    start
                    end
                  }
                }
              }
              pi {
                id
              }
            }

            fragment ProgramGroupElements on Program {
              allGroupElements(includeDeleted: $includeDeleted) {
                parentGroupId
                observation {
                  id
                  groupId
                }
                group {
                  id
                  name
                  minimumRequired
                  ordered
                  parentId
                  parentIndex
                  minimumInterval {
                    seconds
                  }
                  maximumInterval {
                    seconds
                  }
                  system
                }
              }
            }
            """)
        variables: dict[str, object] = {
            "programId": program_id,
            "includeDeleted": include_deleted,
        }
        response = await self.execute(
            query=query, operation_name="getProgramById", variables=variables, **kwargs
        )
        data = self.get_data(response)
        return GetProgramById.model_validate(data)

    async def get_program_by_reference(
        self, program_reference: Any, include_deleted: bool, **kwargs: Any
    ) -> GetProgramByReference:
        query = gql("""
            query getProgramByReference($programReference: ProgramReferenceLabel!, $includeDeleted: Boolean! = false) {
              program(programReference: $programReference) {
                ...ProgramDetail
                ...ProgramGroupElements
              }
            }

            fragment ProgramCore on Program {
              id
              name
              existence
              description
            }

            fragment ProgramDetail on Program {
              ...ProgramCore
              type
              active {
                start
                end
              }
              proposalStatus
              proposal {
                call {
                  semester
                  active {
                    start
                    end
                  }
                }
              }
              pi {
                id
              }
            }

            fragment ProgramGroupElements on Program {
              allGroupElements(includeDeleted: $includeDeleted) {
                parentGroupId
                observation {
                  id
                  groupId
                }
                group {
                  id
                  name
                  minimumRequired
                  ordered
                  parentId
                  parentIndex
                  minimumInterval {
                    seconds
                  }
                  maximumInterval {
                    seconds
                  }
                  system
                }
              }
            }
            """)
        variables: dict[str, object] = {
            "programReference": program_reference,
            "includeDeleted": include_deleted,
        }
        response = await self.execute(
            query=query,
            operation_name="getProgramByReference",
            variables=variables,
            **kwargs,
        )
        data = self.get_data(response)
        return GetProgramByReference.model_validate(data)

    async def get_program_by_proposal_reference(
        self, proposal_reference: Any, include_deleted: bool, **kwargs: Any
    ) -> GetProgramByProposalReference:
        query = gql("""
            query getProgramByProposalReference($proposalReference: ProposalReferenceLabel!, $includeDeleted: Boolean! = false) {
              program(proposalReference: $proposalReference) {
                ...ProgramDetail
                ...ProgramGroupElements
              }
            }

            fragment ProgramCore on Program {
              id
              name
              existence
              description
            }

            fragment ProgramDetail on Program {
              ...ProgramCore
              type
              active {
                start
                end
              }
              proposalStatus
              proposal {
                call {
                  semester
                  active {
                    start
                    end
                  }
                }
              }
              pi {
                id
              }
            }

            fragment ProgramGroupElements on Program {
              allGroupElements(includeDeleted: $includeDeleted) {
                parentGroupId
                observation {
                  id
                  groupId
                }
                group {
                  id
                  name
                  minimumRequired
                  ordered
                  parentId
                  parentIndex
                  minimumInterval {
                    seconds
                  }
                  maximumInterval {
                    seconds
                  }
                  system
                }
              }
            }
            """)
        variables: dict[str, object] = {
            "proposalReference": proposal_reference,
            "includeDeleted": include_deleted,
        }
        response = await self.execute(
            query=query,
            operation_name="getProgramByProposalReference",
            variables=variables,
            **kwargs,
        )
        data = self.get_data(response)
        return GetProgramByProposalReference.model_validate(data)

    async def get_programs(
        self,
        include_deleted: bool,
        where: Union[Optional[WhereProgram], UnsetType] = UNSET,
        offset: Union[Optional[Any], UnsetType] = UNSET,
        limit: Union[Optional[Any], UnsetType] = UNSET,
        **kwargs: Any,
    ) -> GetPrograms:
        query = gql("""
            query getPrograms($where: WhereProgram, $offset: ProgramId, $limit: NonNegInt, $includeDeleted: Boolean! = false) {
              programs(
                WHERE: $where
                OFFSET: $offset
                LIMIT: $limit
                includeDeleted: $includeDeleted
              ) {
                hasMore
                matches {
                  ...ProgramDetail
                  ...ProgramGroupElements
                }
              }
            }

            fragment ProgramCore on Program {
              id
              name
              existence
              description
            }

            fragment ProgramDetail on Program {
              ...ProgramCore
              type
              active {
                start
                end
              }
              proposalStatus
              proposal {
                call {
                  semester
                  active {
                    start
                    end
                  }
                }
              }
              pi {
                id
              }
            }

            fragment ProgramGroupElements on Program {
              allGroupElements(includeDeleted: $includeDeleted) {
                parentGroupId
                observation {
                  id
                  groupId
                }
                group {
                  id
                  name
                  minimumRequired
                  ordered
                  parentId
                  parentIndex
                  minimumInterval {
                    seconds
                  }
                  maximumInterval {
                    seconds
                  }
                  system
                }
              }
            }
            """)
        variables: dict[str, object] = {
            "where": where,
            "offset": offset,
            "limit": limit,
            "includeDeleted": include_deleted,
        }
        response = await self.execute(
            query=query, operation_name="getPrograms", variables=variables, **kwargs
        )
        data = self.get_data(response)
        return GetPrograms.model_validate(data)

    async def program_edit(
        self, program_id: Union[Optional[Any], UnsetType] = UNSET, **kwargs: Any
    ) -> AsyncIterator[ProgramEdit]:
        query = gql("""
            subscription ProgramEdit($programId: ProgramId) {
              programEdit(input: {programId: $programId}) {
                editType
                value {
                  description
                  existence
                  name
                  id
                  allGroupElements {
                    observation {
                      id
                    }
                    group {
                      id
                    }
                  }
                }
              }
            }
            """)
        variables: dict[str, object] = {"programId": program_id}
        async for data in self.execute_ws(
            query=query, operation_name="ProgramEdit", variables=variables, **kwargs
        ):
            yield ProgramEdit.model_validate(data)

    async def get_scheduler_programs(
        self,
        programs_list: Union[Optional[list[Any]], UnsetType] = UNSET,
        **kwargs: Any,
    ) -> GetSchedulerPrograms:
        query = gql("""
            query GetSchedulerPrograms($programsList: [ProgramId!]) {
              programs(WHERE: {id: {IN: $programsList}}) {
                matches {
                  id
                  name
                  description
                  existence
                  type
                  reference {
                    __typename
                    label
                    type
                  }
                  active {
                    start
                    end
                  }
                  proposalStatus
                  proposal {
                    type {
                      __typename
                      scienceSubtype
                    }
                    call {
                      active {
                        start
                        end
                      }
                      semester
                    }
                  }
                  allocations {
                    category
                    duration {
                      hours
                    }
                    scienceBand
                  }
                  timeCharge {
                    band
                    time {
                      program {
                        hours
                      }
                      total {
                        hours
                      }
                      nonCharged {
                        hours
                      }
                    }
                  }
                  allGroupElements {
                    parentGroupId
                    group {
                      id
                      name
                      minimumRequired
                      ordered
                      parentId
                      parentIndex
                      minimumInterval {
                        seconds
                      }
                      maximumInterval {
                        seconds
                      }
                      system
                    }
                    observation {
                      id
                      groupId
                    }
                  }
                }
              }
            }
            """)
        variables: dict[str, object] = {"programsList": programs_list}
        response = await self.execute(
            query=query,
            operation_name="GetSchedulerPrograms",
            variables=variables,
            **kwargs,
        )
        data = self.get_data(response)
        return GetSchedulerPrograms.model_validate(data)

    async def get_scheduler_all_programs_id(
        self, today: Union[Optional[Any], UnsetType] = UNSET, **kwargs: Any
    ) -> GetSchedulerAllProgramsId:
        query = gql("""
            query GetSchedulerAllProgramsId($today: Date) {
              programs(
                WHERE: {activeEnd: {GTE: $today}, activeStart: {LT: $today}, OR: [{proposalStatus: {EQ: ACCEPTED}}, {type: {IN: [CALIBRATION, ENGINEERING]}}]}
              ) {
                matches {
                  reference {
                    __typename
                    label
                  }
                  id
                }
              }
            }
            """)
        variables: dict[str, object] = {"today": today}
        response = await self.execute(
            query=query,
            operation_name="GetSchedulerAllProgramsId",
            variables=variables,
            **kwargs,
        )
        data = self.get_data(response)
        return GetSchedulerAllProgramsId.model_validate(data)

    async def clone_target(
        self,
        target_id: Any,
        include_deleted: bool,
        properties: Union[Optional[TargetPropertiesInput], UnsetType] = UNSET,
        replace_in: Union[Optional[list[Any]], UnsetType] = UNSET,
        **kwargs: Any,
    ) -> CloneTarget:
        query = gql("""
            mutation cloneTarget($targetId: TargetId!, $properties: TargetPropertiesInput, $replaceIn: [ObservationId!], $includeDeleted: Boolean! = false) {
              cloneTarget(
                input: {targetId: $targetId, SET: $properties, REPLACE_IN: $replaceIn}
              ) {
                newTarget {
                  ...TargetDetails
                  ...TargetProgramSummary
                }
              }
            }

            fragment NonsiderealTargetDetails on Nonsidereal {
              des
              keyType
              key
            }

            fragment OpportunityTargetDetails on Opportunity {
              region {
                rightAscensionArc {
                  start {
                    degrees
                  }
                  end {
                    degrees
                  }
                }
                declinationArc {
                  start {
                    degrees
                  }
                  end {
                    degrees
                  }
                }
              }
            }

            fragment ProgramCore on Program {
              id
              name
              existence
              description
            }

            fragment SiderealTargetDetails on Sidereal {
              ra {
                hours
                hms
                degrees
              }
              dec {
                degrees
                dms
              }
              epoch
            }

            fragment TargetCore on Target {
              id
              existence
              name
              calibrationRole
            }

            fragment TargetDetails on Target {
              ...TargetCore
              opportunity {
                ...OpportunityTargetDetails
              }
              sidereal {
                ...SiderealTargetDetails
              }
              nonsidereal {
                ...NonsiderealTargetDetails
              }
            }

            fragment TargetProgramSummary on Target {
              program(includeDeleted: $includeDeleted) {
                ...ProgramCore
              }
            }
            """)
        variables: dict[str, object] = {
            "targetId": target_id,
            "properties": properties,
            "replaceIn": replace_in,
            "includeDeleted": include_deleted,
        }
        response = await self.execute(
            query=query, operation_name="cloneTarget", variables=variables, **kwargs
        )
        data = self.get_data(response)
        return CloneTarget.model_validate(data)

    async def create_target_by_program_id(
        self,
        program_id: Any,
        properties: TargetPropertiesInput,
        include_deleted: bool,
        **kwargs: Any,
    ) -> CreateTargetByProgramId:
        query = gql("""
            mutation createTargetByProgramId($programId: ProgramId!, $properties: TargetPropertiesInput!, $includeDeleted: Boolean! = false) {
              createTarget(input: {programId: $programId, SET: $properties}) {
                target {
                  ...TargetDetails
                  ...TargetProgramSummary
                }
              }
            }

            fragment NonsiderealTargetDetails on Nonsidereal {
              des
              keyType
              key
            }

            fragment OpportunityTargetDetails on Opportunity {
              region {
                rightAscensionArc {
                  start {
                    degrees
                  }
                  end {
                    degrees
                  }
                }
                declinationArc {
                  start {
                    degrees
                  }
                  end {
                    degrees
                  }
                }
              }
            }

            fragment ProgramCore on Program {
              id
              name
              existence
              description
            }

            fragment SiderealTargetDetails on Sidereal {
              ra {
                hours
                hms
                degrees
              }
              dec {
                degrees
                dms
              }
              epoch
            }

            fragment TargetCore on Target {
              id
              existence
              name
              calibrationRole
            }

            fragment TargetDetails on Target {
              ...TargetCore
              opportunity {
                ...OpportunityTargetDetails
              }
              sidereal {
                ...SiderealTargetDetails
              }
              nonsidereal {
                ...NonsiderealTargetDetails
              }
            }

            fragment TargetProgramSummary on Target {
              program(includeDeleted: $includeDeleted) {
                ...ProgramCore
              }
            }
            """)
        variables: dict[str, object] = {
            "programId": program_id,
            "properties": properties,
            "includeDeleted": include_deleted,
        }
        response = await self.execute(
            query=query,
            operation_name="createTargetByProgramId",
            variables=variables,
            **kwargs,
        )
        data = self.get_data(response)
        return CreateTargetByProgramId.model_validate(data)

    async def create_target_by_proposal_reference(
        self,
        proposal_reference: Any,
        properties: TargetPropertiesInput,
        include_deleted: bool,
        **kwargs: Any,
    ) -> CreateTargetByProposalReference:
        query = gql("""
            mutation createTargetByProposalReference($proposalReference: ProposalReferenceLabel!, $properties: TargetPropertiesInput!, $includeDeleted: Boolean! = false) {
              createTarget(input: {proposalReference: $proposalReference, SET: $properties}) {
                target {
                  ...TargetDetails
                  ...TargetProgramSummary
                }
              }
            }

            fragment NonsiderealTargetDetails on Nonsidereal {
              des
              keyType
              key
            }

            fragment OpportunityTargetDetails on Opportunity {
              region {
                rightAscensionArc {
                  start {
                    degrees
                  }
                  end {
                    degrees
                  }
                }
                declinationArc {
                  start {
                    degrees
                  }
                  end {
                    degrees
                  }
                }
              }
            }

            fragment ProgramCore on Program {
              id
              name
              existence
              description
            }

            fragment SiderealTargetDetails on Sidereal {
              ra {
                hours
                hms
                degrees
              }
              dec {
                degrees
                dms
              }
              epoch
            }

            fragment TargetCore on Target {
              id
              existence
              name
              calibrationRole
            }

            fragment TargetDetails on Target {
              ...TargetCore
              opportunity {
                ...OpportunityTargetDetails
              }
              sidereal {
                ...SiderealTargetDetails
              }
              nonsidereal {
                ...NonsiderealTargetDetails
              }
            }

            fragment TargetProgramSummary on Target {
              program(includeDeleted: $includeDeleted) {
                ...ProgramCore
              }
            }
            """)
        variables: dict[str, object] = {
            "proposalReference": proposal_reference,
            "properties": properties,
            "includeDeleted": include_deleted,
        }
        response = await self.execute(
            query=query,
            operation_name="createTargetByProposalReference",
            variables=variables,
            **kwargs,
        )
        data = self.get_data(response)
        return CreateTargetByProposalReference.model_validate(data)

    async def create_target_by_program_reference(
        self,
        program_reference: Any,
        properties: TargetPropertiesInput,
        include_deleted: bool,
        **kwargs: Any,
    ) -> CreateTargetByProgramReference:
        query = gql("""
            mutation createTargetByProgramReference($programReference: ProgramReferenceLabel!, $properties: TargetPropertiesInput!, $includeDeleted: Boolean! = false) {
              createTarget(input: {programReference: $programReference, SET: $properties}) {
                target {
                  ...TargetDetails
                  ...TargetProgramSummary
                }
              }
            }

            fragment NonsiderealTargetDetails on Nonsidereal {
              des
              keyType
              key
            }

            fragment OpportunityTargetDetails on Opportunity {
              region {
                rightAscensionArc {
                  start {
                    degrees
                  }
                  end {
                    degrees
                  }
                }
                declinationArc {
                  start {
                    degrees
                  }
                  end {
                    degrees
                  }
                }
              }
            }

            fragment ProgramCore on Program {
              id
              name
              existence
              description
            }

            fragment SiderealTargetDetails on Sidereal {
              ra {
                hours
                hms
                degrees
              }
              dec {
                degrees
                dms
              }
              epoch
            }

            fragment TargetCore on Target {
              id
              existence
              name
              calibrationRole
            }

            fragment TargetDetails on Target {
              ...TargetCore
              opportunity {
                ...OpportunityTargetDetails
              }
              sidereal {
                ...SiderealTargetDetails
              }
              nonsidereal {
                ...NonsiderealTargetDetails
              }
            }

            fragment TargetProgramSummary on Target {
              program(includeDeleted: $includeDeleted) {
                ...ProgramCore
              }
            }
            """)
        variables: dict[str, object] = {
            "programReference": program_reference,
            "properties": properties,
            "includeDeleted": include_deleted,
        }
        response = await self.execute(
            query=query,
            operation_name="createTargetByProgramReference",
            variables=variables,
            **kwargs,
        )
        data = self.get_data(response)
        return CreateTargetByProgramReference.model_validate(data)

    async def update_targets(
        self,
        properties: TargetPropertiesInput,
        include_deleted: bool,
        where: Union[Optional[WhereTarget], UnsetType] = UNSET,
        limit: Union[Optional[Any], UnsetType] = UNSET,
        **kwargs: Any,
    ) -> UpdateTargets:
        query = gql("""
            mutation updateTargets($properties: TargetPropertiesInput!, $where: WhereTarget, $limit: NonNegInt, $includeDeleted: Boolean! = false) {
              updateTargets(
                input: {SET: $properties, WHERE: $where, LIMIT: $limit, includeDeleted: $includeDeleted}
              ) {
                hasMore
                targets {
                  ...TargetDetails
                  ...TargetProgramSummary
                }
              }
            }

            fragment NonsiderealTargetDetails on Nonsidereal {
              des
              keyType
              key
            }

            fragment OpportunityTargetDetails on Opportunity {
              region {
                rightAscensionArc {
                  start {
                    degrees
                  }
                  end {
                    degrees
                  }
                }
                declinationArc {
                  start {
                    degrees
                  }
                  end {
                    degrees
                  }
                }
              }
            }

            fragment ProgramCore on Program {
              id
              name
              existence
              description
            }

            fragment SiderealTargetDetails on Sidereal {
              ra {
                hours
                hms
                degrees
              }
              dec {
                degrees
                dms
              }
              epoch
            }

            fragment TargetCore on Target {
              id
              existence
              name
              calibrationRole
            }

            fragment TargetDetails on Target {
              ...TargetCore
              opportunity {
                ...OpportunityTargetDetails
              }
              sidereal {
                ...SiderealTargetDetails
              }
              nonsidereal {
                ...NonsiderealTargetDetails
              }
            }

            fragment TargetProgramSummary on Target {
              program(includeDeleted: $includeDeleted) {
                ...ProgramCore
              }
            }
            """)
        variables: dict[str, object] = {
            "properties": properties,
            "where": where,
            "limit": limit,
            "includeDeleted": include_deleted,
        }
        response = await self.execute(
            query=query, operation_name="updateTargets", variables=variables, **kwargs
        )
        data = self.get_data(response)
        return UpdateTargets.model_validate(data)

    async def update_target_by_id(
        self,
        target_id: Any,
        properties: TargetPropertiesInput,
        include_deleted: bool,
        **kwargs: Any,
    ) -> UpdateTargetById:
        query = gql("""
            mutation updateTargetById($targetId: TargetId!, $properties: TargetPropertiesInput!, $includeDeleted: Boolean! = false) {
              updateTargets(
                input: {SET: $properties, WHERE: {id: {EQ: $targetId}}, LIMIT: 1, includeDeleted: $includeDeleted}
              ) {
                hasMore
                targets {
                  ...TargetDetails
                  ...TargetProgramSummary
                }
              }
            }

            fragment NonsiderealTargetDetails on Nonsidereal {
              des
              keyType
              key
            }

            fragment OpportunityTargetDetails on Opportunity {
              region {
                rightAscensionArc {
                  start {
                    degrees
                  }
                  end {
                    degrees
                  }
                }
                declinationArc {
                  start {
                    degrees
                  }
                  end {
                    degrees
                  }
                }
              }
            }

            fragment ProgramCore on Program {
              id
              name
              existence
              description
            }

            fragment SiderealTargetDetails on Sidereal {
              ra {
                hours
                hms
                degrees
              }
              dec {
                degrees
                dms
              }
              epoch
            }

            fragment TargetCore on Target {
              id
              existence
              name
              calibrationRole
            }

            fragment TargetDetails on Target {
              ...TargetCore
              opportunity {
                ...OpportunityTargetDetails
              }
              sidereal {
                ...SiderealTargetDetails
              }
              nonsidereal {
                ...NonsiderealTargetDetails
              }
            }

            fragment TargetProgramSummary on Target {
              program(includeDeleted: $includeDeleted) {
                ...ProgramCore
              }
            }
            """)
        variables: dict[str, object] = {
            "targetId": target_id,
            "properties": properties,
            "includeDeleted": include_deleted,
        }
        response = await self.execute(
            query=query,
            operation_name="updateTargetById",
            variables=variables,
            **kwargs,
        )
        data = self.get_data(response)
        return UpdateTargetById.model_validate(data)

    async def restore_target_by_id(
        self, target_id: Any, **kwargs: Any
    ) -> RestoreTargetById:
        query = gql("""
            mutation restoreTargetById($targetId: TargetId!) {
              updateTargets(
                input: {SET: {existence: PRESENT}, WHERE: {id: {EQ: $targetId}}, LIMIT: 1, includeDeleted: true}
              ) {
                hasMore
                targets {
                  ...TargetDetails
                  program(includeDeleted: true) {
                    id
                    name
                    description
                    existence
                  }
                }
              }
            }

            fragment NonsiderealTargetDetails on Nonsidereal {
              des
              keyType
              key
            }

            fragment OpportunityTargetDetails on Opportunity {
              region {
                rightAscensionArc {
                  start {
                    degrees
                  }
                  end {
                    degrees
                  }
                }
                declinationArc {
                  start {
                    degrees
                  }
                  end {
                    degrees
                  }
                }
              }
            }

            fragment SiderealTargetDetails on Sidereal {
              ra {
                hours
                hms
                degrees
              }
              dec {
                degrees
                dms
              }
              epoch
            }

            fragment TargetCore on Target {
              id
              existence
              name
              calibrationRole
            }

            fragment TargetDetails on Target {
              ...TargetCore
              opportunity {
                ...OpportunityTargetDetails
              }
              sidereal {
                ...SiderealTargetDetails
              }
              nonsidereal {
                ...NonsiderealTargetDetails
              }
            }
            """)
        variables: dict[str, object] = {"targetId": target_id}
        response = await self.execute(
            query=query,
            operation_name="restoreTargetById",
            variables=variables,
            **kwargs,
        )
        data = self.get_data(response)
        return RestoreTargetById.model_validate(data)

    async def delete_target_by_id(
        self, target_id: Any, **kwargs: Any
    ) -> DeleteTargetById:
        query = gql("""
            mutation deleteTargetById($targetId: TargetId!) {
              updateTargets(
                input: {SET: {existence: DELETED}, WHERE: {id: {EQ: $targetId}}, LIMIT: 1, includeDeleted: false}
              ) {
                hasMore
                targets {
                  ...TargetDetails
                  program(includeDeleted: false) {
                    id
                    name
                    description
                    existence
                  }
                }
              }
            }

            fragment NonsiderealTargetDetails on Nonsidereal {
              des
              keyType
              key
            }

            fragment OpportunityTargetDetails on Opportunity {
              region {
                rightAscensionArc {
                  start {
                    degrees
                  }
                  end {
                    degrees
                  }
                }
                declinationArc {
                  start {
                    degrees
                  }
                  end {
                    degrees
                  }
                }
              }
            }

            fragment SiderealTargetDetails on Sidereal {
              ra {
                hours
                hms
                degrees
              }
              dec {
                degrees
                dms
              }
              epoch
            }

            fragment TargetCore on Target {
              id
              existence
              name
              calibrationRole
            }

            fragment TargetDetails on Target {
              ...TargetCore
              opportunity {
                ...OpportunityTargetDetails
              }
              sidereal {
                ...SiderealTargetDetails
              }
              nonsidereal {
                ...NonsiderealTargetDetails
              }
            }
            """)
        variables: dict[str, object] = {"targetId": target_id}
        response = await self.execute(
            query=query,
            operation_name="deleteTargetById",
            variables=variables,
            **kwargs,
        )
        data = self.get_data(response)
        return DeleteTargetById.model_validate(data)

    async def get_target_by_id(
        self, target_id: Any, include_deleted: bool, **kwargs: Any
    ) -> GetTargetById:
        query = gql("""
            query getTargetById($targetId: TargetId!, $includeDeleted: Boolean! = false) {
              target(targetId: $targetId) {
                ...TargetDetails
                ...TargetProgramSummary
              }
            }

            fragment NonsiderealTargetDetails on Nonsidereal {
              des
              keyType
              key
            }

            fragment OpportunityTargetDetails on Opportunity {
              region {
                rightAscensionArc {
                  start {
                    degrees
                  }
                  end {
                    degrees
                  }
                }
                declinationArc {
                  start {
                    degrees
                  }
                  end {
                    degrees
                  }
                }
              }
            }

            fragment ProgramCore on Program {
              id
              name
              existence
              description
            }

            fragment SiderealTargetDetails on Sidereal {
              ra {
                hours
                hms
                degrees
              }
              dec {
                degrees
                dms
              }
              epoch
            }

            fragment TargetCore on Target {
              id
              existence
              name
              calibrationRole
            }

            fragment TargetDetails on Target {
              ...TargetCore
              opportunity {
                ...OpportunityTargetDetails
              }
              sidereal {
                ...SiderealTargetDetails
              }
              nonsidereal {
                ...NonsiderealTargetDetails
              }
            }

            fragment TargetProgramSummary on Target {
              program(includeDeleted: $includeDeleted) {
                ...ProgramCore
              }
            }
            """)
        variables: dict[str, object] = {
            "targetId": target_id,
            "includeDeleted": include_deleted,
        }
        response = await self.execute(
            query=query, operation_name="getTargetById", variables=variables, **kwargs
        )
        data = self.get_data(response)
        return GetTargetById.model_validate(data)

    async def get_targets(
        self,
        include_deleted: bool,
        where: Union[Optional[WhereTarget], UnsetType] = UNSET,
        offset: Union[Optional[Any], UnsetType] = UNSET,
        limit: Union[Optional[Any], UnsetType] = UNSET,
        **kwargs: Any,
    ) -> GetTargets:
        query = gql("""
            query getTargets($where: WhereTarget, $offset: TargetId, $limit: NonNegInt, $includeDeleted: Boolean! = false) {
              targets(
                WHERE: $where
                OFFSET: $offset
                LIMIT: $limit
                includeDeleted: $includeDeleted
              ) {
                hasMore
                matches {
                  ...TargetDetails
                  ...TargetProgramSummary
                }
              }
            }

            fragment NonsiderealTargetDetails on Nonsidereal {
              des
              keyType
              key
            }

            fragment OpportunityTargetDetails on Opportunity {
              region {
                rightAscensionArc {
                  start {
                    degrees
                  }
                  end {
                    degrees
                  }
                }
                declinationArc {
                  start {
                    degrees
                  }
                  end {
                    degrees
                  }
                }
              }
            }

            fragment ProgramCore on Program {
              id
              name
              existence
              description
            }

            fragment SiderealTargetDetails on Sidereal {
              ra {
                hours
                hms
                degrees
              }
              dec {
                degrees
                dms
              }
              epoch
            }

            fragment TargetCore on Target {
              id
              existence
              name
              calibrationRole
            }

            fragment TargetDetails on Target {
              ...TargetCore
              opportunity {
                ...OpportunityTargetDetails
              }
              sidereal {
                ...SiderealTargetDetails
              }
              nonsidereal {
                ...NonsiderealTargetDetails
              }
            }

            fragment TargetProgramSummary on Target {
              program(includeDeleted: $includeDeleted) {
                ...ProgramCore
              }
            }
            """)
        variables: dict[str, object] = {
            "where": where,
            "offset": offset,
            "limit": limit,
            "includeDeleted": include_deleted,
        }
        response = await self.execute(
            query=query, operation_name="getTargets", variables=variables, **kwargs
        )
        data = self.get_data(response)
        return GetTargets.model_validate(data)

    async def target_edit(
        self, target_edit: Union[Optional[Any], UnsetType] = UNSET, **kwargs: Any
    ) -> AsyncIterator[TargetEdit]:
        query = gql("""
            subscription TargetEdit($targetEdit: TargetId) {
              targetEdit(input: {targetId: $targetEdit}) {
                editType
                targetId
                value {
                  id
                  name
                  nonsidereal {
                    des
                    key
                  }
                  sidereal {
                    ra {
                      degrees
                    }
                    dec {
                      degrees
                    }
                  }
                }
              }
            }
            """)
        variables: dict[str, object] = {"targetEdit": target_edit}
        async for data in self.execute_ws(
            query=query, operation_name="TargetEdit", variables=variables, **kwargs
        ):
            yield TargetEdit.model_validate(data)

    async def ping(self, **kwargs: Any) -> Ping:
        query = gql("""
            query ping {
              programs(LIMIT: 1) {
                matches {
                  id
                }
              }
            }
            """)
        variables: dict[str, object] = {}
        response = await self.execute(
            query=query, operation_name="ping", variables=variables, **kwargs
        )
        data = self.get_data(response)
        return Ping.model_validate(data)

    async def set_observation_workflow_state(
        self, observation_id: Any, state: ObservationWorkflowState, **kwargs: Any
    ) -> SetObservationWorkflowState:
        query = gql("""
            mutation setObservationWorkflowState($observationId: ObservationId!, $state: ObservationWorkflowState!) {
              setObservationWorkflowState(
                input: {observationId: $observationId, state: $state}
              ) {
                ...ObservationWorkflowDetails
              }
            }

            fragment ObservationWorkflowCore on ObservationWorkflow {
              state
            }

            fragment ObservationWorkflowDetails on ObservationWorkflow {
              ...ObservationWorkflowCore
              validTransitions
              validationErrors {
                code
                messages
              }
            }
            """)
        variables: dict[str, object] = {"observationId": observation_id, "state": state}
        response = await self.execute(
            query=query,
            operation_name="setObservationWorkflowState",
            variables=variables,
            **kwargs,
        )
        data = self.get_data(response)
        return SetObservationWorkflowState.model_validate(data)

    async def get_observation_workflow_state_by_id(
        self, observation_id: Any, **kwargs: Any
    ) -> GetObservationWorkflowStateById:
        query = gql("""
            query getObservationWorkflowStateById($observationId: ObservationId!) {
              observation(observationId: $observationId) {
                ...ObservationCore
                program {
                  ...ProgramCore
                }
                workflow {
                  ...WorkflowDetails
                }
              }
            }

            fragment ObservationCore on Observation {
              id
              existence
              reference {
                label
              }
              title
              instrument
              calibrationRole
            }

            fragment ProgramCore on Program {
              id
              name
              existence
              description
            }

            fragment WorkflowCore on CalculatedObservationWorkflow {
              state
            }

            fragment WorkflowDetails on CalculatedObservationWorkflow {
              ...WorkflowCore
              value {
                state
                validTransitions
                validationErrors {
                  code
                  messages
                }
              }
            }
            """)
        variables: dict[str, object] = {"observationId": observation_id}
        response = await self.execute(
            query=query,
            operation_name="getObservationWorkflowStateById",
            variables=variables,
            **kwargs,
        )
        data = self.get_data(response)
        return GetObservationWorkflowStateById.model_validate(data)

    async def get_observation_workflow_state_by_reference(
        self, observation_reference: Any, **kwargs: Any
    ) -> GetObservationWorkflowStateByReference:
        query = gql("""
            query getObservationWorkflowStateByReference($observationReference: ObservationReferenceLabel!) {
              observation(observationReference: $observationReference) {
                ...ObservationCore
                program {
                  ...ProgramCore
                }
                workflow {
                  ...WorkflowDetails
                }
              }
            }

            fragment ObservationCore on Observation {
              id
              existence
              reference {
                label
              }
              title
              instrument
              calibrationRole
            }

            fragment ProgramCore on Program {
              id
              name
              existence
              description
            }

            fragment WorkflowCore on CalculatedObservationWorkflow {
              state
            }

            fragment WorkflowDetails on CalculatedObservationWorkflow {
              ...WorkflowCore
              value {
                state
                validTransitions
                validationErrors {
                  code
                  messages
                }
              }
            }
            """)
        variables: dict[str, object] = {"observationReference": observation_reference}
        response = await self.execute(
            query=query,
            operation_name="getObservationWorkflowStateByReference",
            variables=variables,
            **kwargs,
        )
        data = self.get_data(response)
        return GetObservationWorkflowStateByReference.model_validate(data)

    async def execute_custom_operation(
        self, *fields: GraphQLField, operation_type: OperationType, operation_name: str
    ) -> dict[str, Any]:
        selections = self._build_selection_set(fields)
        combined_variables = self._combine_variables(fields)
        variable_definitions = self._build_variable_definitions(
            combined_variables["types"]
        )
        operation_ast = self._build_operation_ast(
            selections, operation_type, operation_name, variable_definitions
        )
        response = await self.execute(
            print_ast(operation_ast),
            variables=combined_variables["values"],
            operation_name=operation_name,
        )
        return self.get_data(response)

    def _combine_variables(
        self, fields: tuple[GraphQLField, ...]
    ) -> dict[str, dict[str, Any]]:
        variables_types_combined = {}
        processed_variables_combined = {}
        for field in fields:
            formatted_variables = field.get_formatted_variables()
            variables_types_combined.update(
                {k: v["type"] for k, v in formatted_variables.items()}
            )
            processed_variables_combined.update(
                {k: v["value"] for k, v in formatted_variables.items()}
            )
        return {
            "types": variables_types_combined,
            "values": processed_variables_combined,
        }

    def _build_variable_definitions(
        self, variables_types_combined: dict[str, str]
    ) -> list[VariableDefinitionNode]:
        return [
            VariableDefinitionNode(
                variable=VariableNode(name=NameNode(value=var_name)),
                type=NamedTypeNode(name=NameNode(value=var_value)),
            )
            for var_name, var_value in variables_types_combined.items()
        ]

    def _build_operation_ast(
        self,
        selections: list[SelectionNode],
        operation_type: OperationType,
        operation_name: str,
        variable_definitions: list[VariableDefinitionNode],
    ) -> DocumentNode:
        return DocumentNode(
            definitions=[
                OperationDefinitionNode(
                    operation=operation_type,
                    name=NameNode(value=operation_name),
                    variable_definitions=variable_definitions,
                    selection_set=SelectionSetNode(selections=selections),
                )
            ]
        )

    def _build_selection_set(
        self, fields: tuple[GraphQLField, ...]
    ) -> list[SelectionNode]:
        return [field.to_ast(idx) for idx, field in enumerate(fields)]

    async def query(self, *fields: GraphQLField, operation_name: str) -> dict[str, Any]:
        return await self.execute_custom_operation(
            *fields, operation_type=OperationType.QUERY, operation_name=operation_name
        )

    async def mutation(
        self, *fields: GraphQLField, operation_name: str
    ) -> dict[str, Any]:
        return await self.execute_custom_operation(
            *fields,
            operation_type=OperationType.MUTATION,
            operation_name=operation_name,
        )
