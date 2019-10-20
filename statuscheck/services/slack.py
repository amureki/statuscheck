from typing import NamedTuple

from statuscheck.services._custompage import BaseCustomStatusPageAPI
from statuscheck.status_types import TYPE_INCIDENT, TYPE_GOOD, TYPE_MAINTENANCE, TYPE_OUTAGE


class SlackSummary(NamedTuple):
    status: str
    incidents: list

    @classmethod
    def from_data(cls, data):
        return cls(
            status=data['status'],
            incidents=data['incidents'],
        )


class ServiceAPI(BaseCustomStatusPageAPI):
    STATUS_TYPE_MAPPING = {
        'Ok': TYPE_GOOD,
        'Incident': TYPE_INCIDENT,
        'Outage': TYPE_OUTAGE,
        'Maintenance': TYPE_MAINTENANCE,
    }

    name = 'Slack'
    base_url = 'https://status.slack.com/'
    status_url = base_url

    def get_summary(self):
        html = self._get_html_response()
        html_container = html.find('.container', first=True)

        status_icon = html_container.find('img', first=True).attrs.get('src')
        status_icon_type = status_icon.rsplit('.')[0].split('/')[-1]
        status = self.STATUS_TYPE_MAPPING.get(status_icon_type, '')
        description = html_container.find('h1', first=True).text

        # TODO: parse Slack components and their statuses
        incidents = []
        if status != TYPE_GOOD:
            incidents.append({'name': description, 'status': status})
        return SlackSummary.from_data(
            data={'status': status, 'incidents': incidents}
        )
