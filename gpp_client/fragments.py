
RIGHT_ASCENSION_FIELDS = """
fragment RightAscensionFields on RightAscension {
  hms
  hours
  degrees
  microarcseconds
  microseconds
}
"""

DECLINATION_FIELDS = """
fragment DeclinationFields on Declination {
  dms
  degrees
  microarcseconds
}
"""

COORDINATE_LIMITS_FIELDS = f"""
{RIGHT_ASCENSION_FIELDS}
{DECLINATION_FIELDS}

fragment CoordinateLimitsFields on CoordinateLimits {
    raStart {
        ...RightAscensionFields
    }
    raEnd {
        ...RightAscensionFields
     }
    decStart {
        ...DeclinationFields
    }
    decEnd {
        ...DeclinationFields
    }
}
"""

SITE_COORDINATE_LIMITS_FIELDS = f"""
{COORDINATE_LIMITS_FIELDS}

fragment SiteCoordinateLimitsFields on SiteCoordinateLimits {
  north {
    ...CoordinateLimitsFields
  }
  south {
    ...CoordinateLimitsFields
  }
}
"""