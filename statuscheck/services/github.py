import requests

from statuscheck.services._base import BaseServiceAPI
from statuscheck.status_types import TYPE_OUTAGE, TYPE_INCIDENT, TYPE_GOOD


class ServiceAPI(BaseServiceAPI):
    STATUS_TYPE_MAPPING = {
        'good': TYPE_GOOD,
        'minor': TYPE_INCIDENT,
        'major': TYPE_OUTAGE,
    }

    base_url = 'https://status.github.com/api/'
    status_url = 'https://status.github.com'

    def _get_status_data(self):
        url = self.base_url + 'last-message.json'
        response = requests.get(url)
        response.raise_for_status()
        return response.json()

    def get_status(self):
        if not self.data:
            self.data = self._get_status_data()
        return self.data['status']

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
        return self.data.get('body') or self.get_status()
