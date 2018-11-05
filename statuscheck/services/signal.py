from statuscheck.services._custompage import BaseCustomStatusPageAPI
from statuscheck.status_types import TYPE_GOOD


class ServiceAPI(BaseCustomStatusPageAPI):
    # TODO: add incidents and outage mapping:
    STATUS_TYPE_MAPPING = {
        'Signal is up and running.': TYPE_GOOD,
    }

    base_url = 'https://status.signal.org/'
    status_url = base_url

    def _get_status_data(self):
        html = self._get_html_response()
        status_raw = html.find('div', first=True).text
        status_text = status_raw.split('\n', 1)[1]
        return {'status': status_text}

    def get_status(self):
        if not self.data:
            self.data = self._get_status_data()
        return self.data.get('status')

    def get_type(self):
        if not self.data:
            self.data = self._get_status_data()
        status = self.get_status()
        status_type = self.STATUS_TYPE_MAPPING.get(status, '')
        return status_type

    def get_active_incident(self):
        status_type = self.get_type()
        if status_type == TYPE_GOOD:
            return ''
        return self.data.get('status')
