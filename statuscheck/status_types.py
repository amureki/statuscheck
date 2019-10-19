TYPE_GOOD = 'No issues'
TYPE_MAINTENANCE = 'Maintenance'
TYPE_INCIDENT = 'Minor incident'
TYPE_OUTAGE = 'Major outage'
TYPE_UNKNOWN = ''

STATUS_TYPES = (
    TYPE_GOOD,
    TYPE_MAINTENANCE,
    TYPE_INCIDENT,
    TYPE_OUTAGE,
    TYPE_UNKNOWN
)

# Statuspage.io constants
SPIO_INDICATORS = {
    'none': TYPE_GOOD,
    'minor': TYPE_INCIDENT,
    'major': TYPE_OUTAGE,
    'critical': TYPE_OUTAGE,
}

SPIO_COMPONENT_OPERATIONAL = 'operational'
SPIO_COMPONENT_DEGRADED = 'degraded_performance'
SPIO_COMPONENT_PARTIAL_OUTAGE = 'partial_outage'
SPIO_COMPONENT_MAJOR_OUTAGE = 'major_outage'

SPIO_COMPONENTS_STATUSES = {
    SPIO_COMPONENT_OPERATIONAL: 'Operational',
    SPIO_COMPONENT_DEGRADED: 'Degraded performance',
    SPIO_COMPONENT_PARTIAL_OUTAGE: 'Partial outage',
    SPIO_COMPONENT_MAJOR_OUTAGE: 'Major outage',
}
