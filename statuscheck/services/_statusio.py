from typing import NamedTuple

import requests

from statuscheck.services._base import BaseServiceAPI
from statuscheck.status_types import TYPE_GOOD


class StatusioSummary(NamedTuple):
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

    summary = None

    def _get_base_url(self):
        if not self.domain_id:
            raise NotImplementedError('Please, add domain key')
        return f'https://api.status.io/1.0/status/{self.domain_id}'

    def get_summary(self):
        response = requests.get(self._get_base_url())
        response.raise_for_status()
        # return response.json()['result']
        self.summary = StatusioSummary.from_summary(
            summary=response.json()['result']
        )
        return self.summary

    # def _get_status_data(self):
    #     response = requests.get(self._get_base_url())
    #     response.raise_for_status()
    #     return response.json()['result']
    #
    # def get_status(self):
    #     if not self.data:
    #         self.data = self._get_status_data()
    #     return self.data['status_overall']['status']
    #
    # def get_type(self):
    #     status = self.get_status()
    #     status_type = self.STATUS_TYPE_MAPPING.get(status, '')
    #     if not status_type:
    #         self.capture_log(status)
    #     return status_type
    #
    # def get_active_incident(self):
    #     status_type = self.get_type()
    #     if status_type == TYPE_GOOD:
    #         return ''
    #     incidents = self.data['incidents']
    #     if incidents:
    #         self.capture_log('NOT_OK', extra=self.data)
    #         # TODO: clarify data format
    #         return str(incidents[0])
    #     return self.get_status()
