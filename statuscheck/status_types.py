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
    'maintenance': TYPE_MAINTENANCE,
}

SPIO_COMPONENT_OPERATIONAL = 'operational'
SPIO_COMPONENT_DEGRADED = 'degraded_performance'
SPIO_COMPONENT_PARTIAL_OUTAGE = 'partial_outage'
SPIO_COMPONENT_MAJOR_OUTAGE = 'major_outage'
SPIO_COMPONENT_MAINTENANCE = 'under_maintenance'

SPIO_COMPONENTS_STATUSES = {
    SPIO_COMPONENT_OPERATIONAL: 'Operational',
    SPIO_COMPONENT_DEGRADED: 'Degraded performance',
    SPIO_COMPONENT_PARTIAL_OUTAGE: 'Partial outage',
    SPIO_COMPONENT_MAJOR_OUTAGE: 'Major outage',
    SPIO_COMPONENT_MAINTENANCE: 'Under Maintenance',
}

SPIO_INCIDENT_INVESTIGATING = 'Investigating'
SPIO_INCIDENT_IDENTIFIED = 'Identified'
SPIO_INCIDENT_MONITORING = 'Monitoring'
SPIO_INCIDENT_RESOLVED = 'Resolved'
SPIO_INCIDENT_POSTMORTEM = 'Postmortem'

SPIO_INCIDENTS_STATUSES = {
    SPIO_INCIDENT_INVESTIGATING: 'Investigating',
    SPIO_INCIDENT_IDENTIFIED: 'Identified',
    SPIO_INCIDENT_MONITORING: 'Monitoring',
    SPIO_INCIDENT_RESOLVED: 'Resolved',
    SPIO_INCIDENT_POSTMORTEM: 'Postmortem',
}
