import requests

from statuscheck.services._base import BaseServiceAPI
from statuscheck.status_types import TYPE_INCIDENT, TYPE_OUTAGE, TYPE_GOOD


class ServiceAPI(BaseServiceAPI):
    STATUS_TYPE_MAPPING = {
        'green': TYPE_GOOD,
        'yellow': TYPE_INCIDENT,
        'red': TYPE_OUTAGE,
    }

    base_url = 'https://status.heroku.com/api/v3/'
    status_url = 'https://status.heroku.com'

    def _get_status_data(self):
        url = self.base_url + 'current-status'
        response = requests.get(url)
        response.raise_for_status()
        return response.json()

    def _is_status_good(self, status):
        return self.STATUS_TYPE_MAPPING.get(status, '') == TYPE_GOOD

    def get_status(self):
        if not self.data:
            self.data = self._get_status_data()
        status = status_prod = self.data['status']['Production']
        status_dev = self.data['status']['Development']
        if not self._is_status_good(status_dev):
            status = status_dev
        if not self._is_status_good(status_prod):
            status = status_prod
        return status

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
        incidents = self.data['issues']
        if incidents:
            return incidents[0]['title']
        return self.get_status()
