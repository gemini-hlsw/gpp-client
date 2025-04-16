__all__ = [
    "GET_OBSERVATION"
]


GET_OBSERVATION = """
query getObservation(
    $observationId: ObservationId,
    $observationReference: ObservationReferenceLabel
) {
    observation(
        observationId: $observationId,
        observationReference: $observationReference,
    ){
        {fields}
    }
}
"""
# 1. This would add pagination every single time we do the query.
# Adding a non paginated query should be by modifying this one or adding
# a variant in the Mixin?
# 2. I can break this query asking for to many fields. Should we have some
# rail guards about those cases?
# 3. Should whereObservation have a submanager?
GET_OBSERVATIONS = """
query getObservation(
    $where: WhereObservation,
    $offset: ObservationId,
    $limit: NonNegInt,
    $includeDeleted: Boolean = false
) {
    observations(
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

DEFAULT_FIELDS = """
    id
    title
    subtitle
    scienceBand
    observationTime
"""