from statuscheck.services._custompage import BaseCustomStatusPageAPI
from statuscheck.status_types import TYPE_INCIDENT, TYPE_GOOD, TYPE_MAINTENANCE, TYPE_OUTAGE


class ServiceAPI(BaseCustomStatusPageAPI):
    STATUS_TYPE_MAPPING = {
        'Ok': TYPE_GOOD,
        'Incident': TYPE_INCIDENT,
        'Outage': TYPE_OUTAGE,
        'Maintenance': TYPE_MAINTENANCE,
    }

    base_url = 'https://status.slack.com/'
    status_url = base_url

    def _get_status_data(self):
        html = self._get_html_response()
        html_container = html.find('.container', first=True)
        status = html_container.find('h1', first=True).text
        status_icon = html_container.find('img', first=True).attrs.get('src')
        status_icon_type = status_icon.rsplit('.')[0].split('/')[-1]
        return {'status': status, 'status_icon_type': status_icon_type}

    def get_status(self):
        if not self.data:
            self.data = self._get_status_data()
        return self.data.get('status')

    def get_type(self):
        if not self.data:
            self.data = self._get_status_data()

        status_type = self.STATUS_TYPE_MAPPING.get(self.data.get('status_icon_type'), '')
        return status_type

    def get_active_incident(self):
        status_type = self.get_type()
        if status_type == TYPE_GOOD:
            return ''
        return self.data.get('status')
