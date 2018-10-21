import requests

from statuscheck.services._base import BaseServiceAPI


class ServiceAPI(BaseServiceAPI):
    api_name = 'heroku'
    base_url = 'https://status.heroku.com/api/v3/'

    STATUSES = {
        'green': 'good',
        'yellow': 'minor',
        'red': 'major',
    }

    def _get_status_data(self):
        url = self.base_url + 'current-status'
        response = requests.get(url)
        response.raise_for_status()
        return response.json()

    def get_status(self):
        if not self.data:
            self.data = self._get_status_data()
        return self.data['status']['Production']

    def get_status_type(self):
        status = self.get_status()
        status_type = self.STATUSES.get(status, '')
        if not status_type:
            self.capture_log(status)
        return status_type
