import requests

from statuscheck.services._base import BaseServiceAPI
from statuscheck.status_types import TYPE_GOOD


class BaseStatusioAPI(BaseServiceAPI):
    """
    Status.io pages API handler.

    API v2: https://statusio.docs.apiary.io
    Public status API: https://kb.status.io/developers/public-status-api/
    """
    STATUS_TYPE_MAPPING = {
        'Operational': TYPE_GOOD,
    }

    domain_key = None

    def _get_base_url(self):
        if not self.domain_key:
            raise NotImplementedError('Please, add domain key')
        return f'https://api.status.io/1.0/status/{self.domain_key}'

    def _get_status_data(self):
        response = requests.get(self._get_base_url())
        response.raise_for_status()
        return response.json()['result']

    def get_status(self):
        if not self.data:
            self.data = self._get_status_data()
        return self.data['status_overall']['status']

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
        if incidents:
            self.capture_log('NOT_OK', extra=self.data)
            # TODO: clarify data format
            return str(incidents[0])
        return self.get_status()
