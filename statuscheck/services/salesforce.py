from typing import NamedTuple

import requests

from statuscheck.services._base import BaseServiceAPI
from statuscheck.status_types import TYPE_GOOD, TYPE_INCIDENT, TYPE_OUTAGE, TYPE_MAINTENANCE, \
    TYPE_UNKNOWN


class SalesforceSummary(NamedTuple):
    status: str
    incidents: list
    components: list

    @classmethod
    def _get_incidents(cls, summary):
        pass

    @classmethod
    def from_summary(cls, summary):
        return cls(
            status=summary['status'],
            incidents=summary['incidents'],
            components=summary['components'],
        )


class ServiceAPI(BaseServiceAPI):
    STATUS_OK = 'OK'
    STATUS_UNKNOWN = 'UNKNOWN'
    STATUS_CORE_OUTAGE = 'MAJOR_INCIDENT_CORE'
    STATUS_NONCORE_OUTAGE = 'MAJOR_INCIDENT_NONCORE'
    STATUS_CORE_INCIDENT = 'MINOR_INCIDENT_CORE'
    STATUS_NONCORE_INCIDENT = 'MINOR_INCIDENT_NONCORE'
    STATUS_CORE_MAINTENANCE = 'MAINTENANCE_CORE'
    STATUS_NONCORE_MAINTENANCE = 'MAINTENANCE_NONCORE'

    # sorted by severity
    NOT_GOOD_STATUSES = [
        STATUS_CORE_OUTAGE,
        STATUS_NONCORE_OUTAGE,
        STATUS_CORE_INCIDENT,
        STATUS_NONCORE_INCIDENT,
        STATUS_CORE_MAINTENANCE,
        STATUS_NONCORE_MAINTENANCE
    ]

    STATUS_TYPE_MAPPING = {
        STATUS_OK: TYPE_GOOD,
        STATUS_CORE_INCIDENT: TYPE_INCIDENT,
        STATUS_NONCORE_INCIDENT: TYPE_INCIDENT,
        STATUS_CORE_OUTAGE: TYPE_OUTAGE,
        STATUS_NONCORE_OUTAGE: TYPE_OUTAGE,
        STATUS_CORE_MAINTENANCE: TYPE_MAINTENANCE,
        STATUS_NONCORE_MAINTENANCE: TYPE_MAINTENANCE,
        STATUS_UNKNOWN: TYPE_UNKNOWN
    }

    name = 'Salesforce'
    base_url = 'https://api.status.salesforce.com/v1/'
    status_url = 'https://status.salesforce.com'

    def get_summary(self):
        self.data = self._get_status_data()
        self.summary = SalesforceSummary.from_summary(
            summary={
                'status': self.get_general_status(),
                'incidents': self._get_incidents(),
                'components': self._get_affected_servers()
            }
        )
        return self.summary

    def _get_status_data(self):
        url = self.base_url + 'instances/status/preview'
        response = requests.get(url)
        response.raise_for_status()
        return response.json()

    def _get_affected_servers(self) -> list:
        servers = []
        for server in self.data:
            if server.get('status') != self.STATUS_OK:
                servers.append(server)
        return servers

    def _get_incidents(self):
        incidents = []
        affected_servers = self._get_affected_servers()
        if not affected_servers:
            return incidents
        for server in affected_servers:
            data = server['Incidents']
            data['key'] = server['key']
            data['status'] = server['status']
            incidents.append(data)
        return incidents

    def get_general_status(self):
        incidents = self._get_incidents()
        if not incidents:
            return self.STATUS_TYPE_MAPPING[self.STATUS_OK]
        for incident in incidents:
            if incident['affectsAll']:
                return self.STATUS_TYPE_MAPPING[incident['status']]
