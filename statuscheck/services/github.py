import requests

from statuscheck.services._base import BaseServiceAPI


class ServiceAPI(BaseServiceAPI):
    api_name = 'github'
    base_url = 'https://status.github.com/api/'

    def _get_status_data(self):
        url = self.base_url + 'status.json'
        response = requests.get(url)
        response.raise_for_status()
        return response.json()

    def get_status(self):
        if not self.data:
            self.data = self._get_status_data()
        url = self.base_url + 'status.json'
        response = requests.get(url)
        response.raise_for_status()
        data = response.json()
        status = data['status']
        return status

    def get_status_type(self):
        return self.get_status()
