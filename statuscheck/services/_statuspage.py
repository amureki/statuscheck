import requests

from statuscheck.services._base import BaseServiceAPI
from statuscheck.status_types import TYPE_GOOD, TYPE_MAINTENANCE, TYPE_INCIDENT, TYPE_OUTAGE


class BaseStatusPageAPI(BaseServiceAPI):
    STATUS_TYPE_MAPPING = {
        'All Systems Operational': TYPE_GOOD,
        'Partially Degraded Service': TYPE_INCIDENT,
        'Minor Service Outage': TYPE_INCIDENT,
        'Major Service Outage': TYPE_OUTAGE,
        'Service Under Maintenance': TYPE_MAINTENANCE,
    }

    domain_key = None

    def _get_status_data(self):
        url = self._get_base_url() + 'summary.json'
        response = requests.get(url)
        response.raise_for_status()
        return response.json()

    def _get_base_url(self):
        if not self.domain_key:
            raise NotImplementedError('Please, add domain key')
        return 'https://{}.statuspage.io/api/v2/'.format(self.domain_key)

    def get_status(self):
        if not self.data:
            self.data = self._get_status_data()
        return self.data['status']['description']

    def get_type(self):
        status = self.get_status()
        status_type = self.STATUS_TYPE_MAPPING.get(status, '')
        if not status_type:
            self.capture_log(status)
        return status_type

    def get_active_incident(self):
        status_type = self.get_type()
        if status_type == TYPE_GOOD:
            return ''
        incidents = self.data['incidents']
        return incidents[0]['name']
