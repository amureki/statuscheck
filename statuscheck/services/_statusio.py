from typing import NamedTuple

import requests

from statuscheck.services._base import BaseServiceAPI
from statuscheck.status_types import TYPE_GOOD


class StatusIOSummary(NamedTuple):
    status: str
    incidents: list
    components: list

    @classmethod
    def _get_components(cls, summary):
        all_components = summary['status']
        damaged_components = [c for c in all_components
                              if c['status'] != 'Operational']
        filtered_data = []
        important_keys = ('name', 'status')
        for component in damaged_components:
            filtered_data.append(
                {k: component.get(k, None) for k in important_keys}
            )
        return filtered_data

    @classmethod
    def _get_incidents(cls, summary):
        incidents = summary['incidents']
        return incidents

    @classmethod
    def from_summary(cls, summary):
        status = summary['status_overall']['status']
        return cls(
            status=status,
            incidents=cls._get_incidents(summary),
            components=cls._get_components(summary)
        )


class BaseStatusioAPI(BaseServiceAPI):
    """
    Status.io pages API handler.

    API v2: https://statusio.docs.apiary.io
    Public status API: https://kb.status.io/developers/public-status-api/
    """
    STATUS_TYPE_MAPPING = {
        'Operational': TYPE_GOOD,
    }

    domain_id: str = None

    def _get_base_url(self):
        if not self.domain_id:
            raise NotImplementedError('Please, add domain key')
        return f'https://api.status.io/1.0/status/{self.domain_id}'

    def get_summary(self):
        response = requests.get(self._get_base_url())
        response.raise_for_status()
        return StatusIOSummary.from_summary(
            summary=response.json()['result']
        )
