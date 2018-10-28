import requests

from statuscheck.services._base import BaseServiceAPI
from statuscheck.status_types import TYPE_GOOD, TYPE_INCIDENT, TYPE_OUTAGE, TYPE_MAINTENANCE, \
    TYPE_UNKNOWN


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

    base_url = 'https://api.status.salesforce.com/v1/'
    status_url = 'https://status.salesforce.com'

    def _get_status_data(self):
        url = self.base_url + 'instances/status'
        response = requests.get(url)
        response.raise_for_status()
        return response.json()

    def _get_affected_servers(self) -> list:
        servers = []
        for server in self.data:
            if server.get('status') != 'OK':
                servers.append(server)
        return servers

    def _get_main_status_message(self):
        if not self.data:
            self.data = self._get_status_data()
        affected_servers = self._get_affected_servers()
        if not affected_servers:
            return self.STATUS_OK
        issues = set([s.get('status').upper() for s in affected_servers])

        # return the most severe status
        for status in self.NOT_GOOD_STATUSES:
            if status in issues:
                return status

    def get_status(self):
        if not self.data:
            self.data = self._get_status_data()
        affected_servers = self._get_affected_servers()
        status = self._get_main_status_message()
        if not affected_servers:
            return status

        affected_servers_str = ", ".join([s.get('key') for s in affected_servers])
        status = f'{status}. Affected servers: {affected_servers_str}'
        return status

    def get_type(self):
        status = self._get_main_status_message()
        status_type = self.STATUS_TYPE_MAPPING.get(status, '')
        if not status_type:
            self.capture_log(status, extra=self._get_affected_servers())
        return status_type

    def get_active_incident(self):
        status_type = self.get_type()
        if status_type == TYPE_GOOD:
            return ''
        return self.get_status()
