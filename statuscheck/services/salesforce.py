import requests

from statuscheck.services._base import BaseServiceAPI
from statuscheck.status_types import TYPE_GOOD, TYPE_INCIDENT, TYPE_OUTAGE


class ServiceAPI(BaseServiceAPI):
    STATUS_TYPE_MAPPING = {
        'All servers operational': TYPE_GOOD,
        'Minor incident': TYPE_INCIDENT,
        'Major incident': TYPE_OUTAGE,
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
        affected_servers = self._get_affected_servers()
        if not affected_servers:
            return 'All servers operational'
        issues = set([s.get('status').upper() for s in affected_servers])
        if 'MINOR_INCIDENT_CORE' in issues:
            return 'Minor incident'
        if 'MAJOR_INCIDENT_CORE' in issues:
            return 'Major incident'
        return ''

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
