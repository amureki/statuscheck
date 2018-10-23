from requests_html import HTMLSession

from statuscheck.services._base import BaseServiceAPI


class ServiceAPI(BaseServiceAPI):
    api_name = 'slack'
    base_url = 'https://status.slack.com/'

    def _get_status_data(self):
        url = self.base_url
        session = HTMLSession()
        response = session.get(url)
        response.raise_for_status()
        status = response.html.find('.container', first=True).find('h1', first=True).text
        status_icon = response.html.find('.container', first=True).find('img', first=True).attrs.get('src')
        status_type = status_icon.rsplit('.')[0].split('/')[-1]
        return {'status': status, 'status_type': status_type}

    def get_status(self):
        if not self.data:
            self.data = self._get_status_data()
        return self.data.get('status')

    def get_status_type(self):
        if not self.data:
            self.data = self._get_status_data()

        status_type = self.data.get('status_type')
        return status_type
