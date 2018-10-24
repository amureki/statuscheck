from requests_html import HTMLSession

from statuscheck.services._base import BaseServiceAPI
from statuscheck.status_types import TYPE_INCIDENT, TYPE_GOOD, TYPE_MAINTENANCE, TYPE_OUTAGE


class ServiceAPI(BaseServiceAPI):
    STATUS_TYPE_MAPPING = {
        'Ok': TYPE_GOOD,
        'Incident': TYPE_INCIDENT,
        'Outage': TYPE_OUTAGE,
        'Maintenance': TYPE_MAINTENANCE,
    }

    api_name = 'slack'
    base_url = 'https://status.slack.com/'

    def _get_status_data(self):
        url = self.base_url
        session = HTMLSession()
        response = session.get(url)
        response.raise_for_status()
        html_container = response.html.find('.container', first=True)
        status = html_container.find('h1', first=True).text
        status_icon = html_container.find('img', first=True).attrs.get('src')
        status_icon_type = status_icon.rsplit('.')[0].split('/')[-1]
        return {'status': status, 'status_icon_type': status_icon_type}

    def get_status(self):
        if not self.data:
            self.data = self._get_status_data()
        return self.data.get('status')

    def get_status_type(self):
        if not self.data:
            self.data = self._get_status_data()

        status_type = self.STATUS_TYPE_MAPPING.get(self.data.get('status_icon_type'), '')
        return status_type
