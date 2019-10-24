from typing import NamedTuple

import requests

from statuscheck.services._base import BaseServiceAPI
from statuscheck.status_types import TYPE_GOOD

STATUS_TYPE_MAPPING = {"Operational": TYPE_GOOD}


class StatusIOSummary(NamedTuple):
    name: str
    status: str
    incidents: list
    components: list

    @classmethod
    def _get_components(cls, data):
        all_components = data["status"]
        damaged_components = [c for c in all_components if c["status"] != "Operational"]
        filtered_data = []
        important_keys = ("name", "status")
        for component in damaged_components:
            filtered_data.append({k: component.get(k, None) for k in important_keys})
        return filtered_data

    @classmethod
    def _get_incidents(cls, data):
        return data["incidents"]

    @classmethod
    def from_data(cls, name, data):
        status_raw = data["status_overall"]["status"]
        status = STATUS_TYPE_MAPPING.get(status_raw, "")
        return cls(
            name=name,
            status=status,
            incidents=cls._get_incidents(data),
            components=cls._get_components(data),
        )


class BaseStatusIOAPI(BaseServiceAPI):
    """
    Status.io pages API handler.

    API v2: https://statusio.docs.apiary.io
    Public status API: https://kb.status.io/developers/public-status-api/
    """

    domain_id: str = None

    def _get_base_url(self):
        if not self.domain_id:
            raise NotImplementedError("Please, add domain key")
        return f"https://api.status.io/1.0/status/{self.domain_id}"

    def get_summary(self):
        response = requests.get(self._get_base_url())
        response.raise_for_status()
        return StatusIOSummary.from_data(name=self.name, data=response.json()["result"])
