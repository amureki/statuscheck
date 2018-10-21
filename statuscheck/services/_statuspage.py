import requests

from statuscheck.services._base import BaseServiceAPI


class BaseStatusPageAPI(BaseServiceAPI):
    domain_key = None

    STATUSES = {
        'All Systems Operational': 'good',
        'Partially Degraded Service': 'minor',
        'Minor Service Outage': 'minor',
        'Major Service Outage': 'major',
        'Service Under Maintenance': 'maintenance',
    }

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

    def get_status_type(self):
        status = self.get_status()
        status_type = self.STATUSES.get(status, '')
        if not status_type:
            self.capture_log(status)
        return status_type
