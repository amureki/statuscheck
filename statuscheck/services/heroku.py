from typing import NamedTuple

import requests

from statuscheck.services._base import BaseServiceAPI
from statuscheck.status_types import TYPE_INCIDENT, TYPE_OUTAGE, TYPE_GOOD

STATUS_TYPE_MAPPING = {
    'green': TYPE_GOOD,
    'yellow': TYPE_INCIDENT,
    'red': TYPE_OUTAGE,
}


class ServiceSummary(NamedTuple):
    status: str
    status_development: str
    status_production: str
    incidents: list

    @classmethod
    def _get_incidents(cls, summary):
        incidents = summary['issues']
        filtered_data = []
        important_keys = ('title', 'status_dev', 'status_prod', 'full_url')
        for component in incidents:
            filtered_data.append(
                {k: component.get(k, None) for k in important_keys}
            )
        return filtered_data

    @classmethod
    def from_summary(cls, summary):
        status_data = summary['status']
        status_production = STATUS_TYPE_MAPPING[status_data['Production']]
        status_development = STATUS_TYPE_MAPPING[status_data['Development']]
        status = status_production

        if status_development != TYPE_GOOD:
            status = status_development
        if status_production != TYPE_GOOD:
            status = status_production

        return cls(
            status=status,
            status_production=status_production,
            status_development=status_development,
            incidents=cls._get_incidents(summary),
        )


class ServiceAPI(BaseServiceAPI):
    name = 'Heroku'
    base_url = 'https://status.heroku.com/api/v3/'
    status_url = 'https://status.heroku.com'

    def get_summary(self):
        url = self.base_url + 'current-status'
        response = requests.get(url)
        response.raise_for_status()
        return ServiceSummary.from_summary(summary=response.json())
