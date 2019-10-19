from typing import NamedTuple

import requests

from statuscheck.services._base import BaseServiceAPI
from statuscheck.status_types import SPIO_INDICATORS, SPIO_COMPONENT_OPERATIONAL, \
    SPIO_COMPONENTS_STATUSES, SPIO_INCIDENTS_STATUSES


class StatusPageIOSummary(NamedTuple):
    status: str
    incidents: list
    components: list

    @classmethod
    def _get_components(cls, summary):
        all_components = summary['components']
        damaged_components = [c for c in all_components
                              if c['status'] != SPIO_COMPONENT_OPERATIONAL]
        filtered_data = []
        important_keys = ('name', 'status', 'description')
        for component in damaged_components:
            data = {k: component.get(k, None) for k in important_keys}
            data['status'] = SPIO_COMPONENTS_STATUSES[data['status']]
            filtered_data.append(data)
        return filtered_data

    @classmethod
    def _get_incidents(cls, summary):
        incidents = summary['incidents']
        filtered_data = []
        important_keys = ('name', 'status', 'impact')
        for component in incidents:
            data = {k: component.get(k, None) for k in important_keys}
            data['status'] = SPIO_INCIDENTS_STATUSES[data['status']]
            filtered_data.append(data)
        return filtered_data

    @classmethod
    def from_summary(cls, summary):
        status = summary['status']
        status_type = SPIO_INDICATORS[status['indicator']]
        return cls(
            status=status_type,
            incidents=cls._get_incidents(summary),
            components=cls._get_components(summary)
        )


class BaseStatusPageAPI(BaseServiceAPI):
    domain_id: str = None
    summary = None

    def __init__(self):
        self.summary = self.get_summary()

    def _get_base_url(self):
        """Statuspage.io API URL for given service."""
        if not self.domain_id:
            raise NotImplementedError('Please, add domain id')
        return f'https://{self.domain_id}.statuspage.io/api/v2/'

    def get_summary(self):
        url = self._get_base_url() + 'summary.json'
        response = requests.get(url)
        response.raise_for_status()
        self.summary = StatusPageIOSummary.from_summary(summary=response.json())
        return self.summary
