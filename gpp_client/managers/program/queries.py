__all__ = [
    "GET_PROGRAM",
    "GET_PROGRAMS",
    "CREATE_PROGRAM",
    "UPDATE_PROGRAMS",
    "DEFAULT_FIELDS",
]

GET_PROGRAM = """
query getProgram(
    $programId: ProgramId,
    $programReference: ProgramReferenceLabel,
    $proposalReference: ProposalReferenceLabel
) {
    program(
        programId: $programId,
        programReference: $programReference,
        proposalReference: $proposalReference
    ) {
        {fields}
    }
}
"""

GET_PROGRAMS = """
query getPrograms(
    $where: WhereProgram,
    $offset: ProgramId,
    $limit: NonNegInt,
    $includeDeleted: Boolean = false
) {
    programs(
        WHERE: $where,
        OFFSET: $offset,
        LIMIT: $limit,
        includeDeleted: $includeDeleted
    ) {
        matches {
            {fields}
        }
        hasMore
    }
}
"""

CREATE_PROGRAM = """
mutation createProgram($input: CreateProgramInput!) {
    createProgram(input: $input) {
        program {
            {fields}
        }
    }
}
"""

UPDATE_PROGRAMS = """
mutation updatePrograms($input: UpdateProgramsInput!) {
    updatePrograms(input: $input) {
        programs {
            {fields}
        }
        hasMore
    }
}
"""

DEFAULT_FIELDS = """
    id
    name
    description
    existence
    type
    reference {
        label
        type
    }
    proposal {
        reference {
            label
            semester
            semesterIndex
        }
        category
        type {
            scienceSubtype
        }
    }
    active {
        start
        end
    }
    goa {
        proprietaryMonths
        shouldNotify
        privateHeader
    }
"""
