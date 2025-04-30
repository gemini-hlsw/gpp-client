__all__ = ["GET_BATCH", "DEFAULT_FIELDS", "GET_BY_ID", "UPDATE_BATCH"]

GET_BY_ID = """
query GetCallForProposals($callForProposalsId: CallForProposalsId!) {
    callForProposals(callForProposalsId: $callForProposalsId) {
        {fields}
    }
}
"""

GET_BATCH = """
query GetCallsForProposals(
    $where: WhereCallForProposals,
    $offset: CallForProposalsId,
    $limit: NonNegInt,
    $includeDeleted: Boolean = false
) {
    callsForProposals(
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

UPDATE_BATCH = """
mutation UpdateCallsForProposals(
    $input: UpdateCallsForProposalsInput!
) {
    updateCallsForProposals(input: $input) {
        callsForProposals {
            {fields}
        }
        hasMore
    }
}
"""

DEFAULT_FIELDS = """
id
title
type
semester
coordinateLimits {
    north {
        raStart {
            hms
            hours
            degrees
            microarcseconds
            microseconds
        }
        raEnd {
            hms
            hours
            degrees
            microarcseconds
            microseconds
        }
        decStart {
            dms
            degrees
            microarcseconds
        }
        decEnd {
            dms
            degrees
            microarcseconds
        }
    }
    south {
        raStart {
            hms
            hours
            degrees
            microarcseconds
            microseconds
        }
        raEnd {
            hms
            hours
            degrees
            microarcseconds
            microseconds
        }
        decStart {
            dms
            degrees
            microarcseconds
        }
        decEnd {
            dms
            degrees
            microarcseconds
        }
    }
}
active {
    start
    end
}
submissionDeadlineDefault
partners {
    partner
    submissionDeadlineOverride
    submissionDeadline
}
allowsNonPartnerPi
nonPartnerDeadline
instruments
proprietaryMonths
existence
"""