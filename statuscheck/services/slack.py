from requests_html import HTMLSession

from statuscheck.services._base import BaseServiceAPI


class ServiceAPI(BaseServiceAPI):
    api_name = 'slack'
    base_url = 'https://status.slack.com/'

    STATUSES = {
        'Smooth sailing!': 'good',
    }

    def _get_status_data(self):
        url = self.base_url
        session = HTMLSession()
        response = session.get(url)
        response.raise_for_status()
        status = response.html.find('.container', first=True).find('h1', first=True).text
        return status

    def get_status(self):
        if not self.data:
            self.data = self._get_status_data()
        return self.data

    def get_status_type(self):
        status = self.get_status()
        status_type = self.STATUSES.get(status, '')
        if not status_type:
            self.capture_log(status)
        return status_type
