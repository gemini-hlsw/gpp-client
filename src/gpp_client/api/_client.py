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
from .get_goats_observations import GetGOATSObservations
from .get_goats_programs import GetGOATSPrograms
from .get_scheduler_all_programs_id import GetSchedulerAllProgramsId
from .get_scheduler_programs import GetSchedulerPrograms
from .obs_calculation_update import ObsCalculationUpdate
from .observation_edit import ObservationEdit
from .program_edit import ProgramEdit
from .target_edit import TargetEdit


def gql(q: str) -> str:
    return q


class _GPPClient(AsyncBaseClient):
    async def get_goats_programs(self, **kwargs: Any) -> GetGOATSPrograms:
        query = gql(
            """
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
            """
        )
        variables: dict[str, object] = {}
        response = await self.execute(
            query=query,
            operation_name="GetGOATSPrograms",
            variables=variables,
            **kwargs
        )
        data = self.get_data(response)
        return GetGOATSPrograms.model_validate(data)

    async def get_goats_observations(
        self, program_id: Any, **kwargs: Any
    ) -> GetGOATSObservations:
        query = gql(
            """
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
            """
        )
        variables: dict[str, object] = {"programId": program_id}
        response = await self.execute(
            query=query,
            operation_name="GetGOATSObservations",
            variables=variables,
            **kwargs
        )
        data = self.get_data(response)
        return GetGOATSObservations.model_validate(data)

    async def get_scheduler_programs(
        self,
        programs_list: Union[Optional[list[Any]], UnsetType] = UNSET,
        **kwargs: Any
    ) -> GetSchedulerPrograms:
        query = gql(
            """
            query GetSchedulerPrograms($programsList: [ProgramId!]) {
              programs(WHERE: {id: {IN: $programsList}, proposalStatus: {EQ: ACCEPTED}}) {
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
            """
        )
        variables: dict[str, object] = {"programsList": programs_list}
        response = await self.execute(
            query=query,
            operation_name="GetSchedulerPrograms",
            variables=variables,
            **kwargs
        )
        data = self.get_data(response)
        return GetSchedulerPrograms.model_validate(data)

    async def get_scheduler_all_programs_id(
        self, **kwargs: Any
    ) -> GetSchedulerAllProgramsId:
        query = gql(
            """
            query GetSchedulerAllProgramsId {
              programs(WHERE: {proposalStatus: {EQ: ACCEPTED}}) {
                matches {
                  id
                }
              }
            }
            """
        )
        variables: dict[str, object] = {}
        response = await self.execute(
            query=query,
            operation_name="GetSchedulerAllProgramsId",
            variables=variables,
            **kwargs
        )
        data = self.get_data(response)
        return GetSchedulerAllProgramsId.model_validate(data)

    async def observation_edit(
        self, program_id: Union[Optional[Any], UnsetType] = UNSET, **kwargs: Any
    ) -> AsyncIterator[ObservationEdit]:
        query = gql(
            """
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
            """
        )
        variables: dict[str, object] = {"programId": program_id}
        async for data in self.execute_ws(
            query=query, operation_name="ObservationEdit", variables=variables, **kwargs
        ):
            yield ObservationEdit.model_validate(data)

    async def program_edit(
        self, program_id: Union[Optional[Any], UnsetType] = UNSET, **kwargs: Any
    ) -> AsyncIterator[ProgramEdit]:
        query = gql(
            """
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
            """
        )
        variables: dict[str, object] = {"programId": program_id}
        async for data in self.execute_ws(
            query=query, operation_name="ProgramEdit", variables=variables, **kwargs
        ):
            yield ProgramEdit.model_validate(data)

    async def target_edit(
        self, target_edit: Union[Optional[Any], UnsetType] = UNSET, **kwargs: Any
    ) -> AsyncIterator[TargetEdit]:
        query = gql(
            """
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
            """
        )
        variables: dict[str, object] = {"targetEdit": target_edit}
        async for data in self.execute_ws(
            query=query, operation_name="TargetEdit", variables=variables, **kwargs
        ):
            yield TargetEdit.model_validate(data)

    async def obs_calculation_update(
        self, program_id: Union[Optional[Any], UnsetType] = UNSET, **kwargs: Any
    ) -> AsyncIterator[ObsCalculationUpdate]:
        query = gql(
            """
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
            """
        )
        variables: dict[str, object] = {"programId": program_id}
        async for data in self.execute_ws(
            query=query,
            operation_name="ObsCalculationUpdate",
            variables=variables,
            **kwargs
        ):
            yield ObsCalculationUpdate.model_validate(data)

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
            operation_name=operation_name
        )
