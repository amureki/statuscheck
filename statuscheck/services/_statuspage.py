from typing import NamedTuple

import requests

from statuscheck.services._base import BaseServiceAPI
from statuscheck.status_types import (
    SPIO_COMPONENT_OPERATIONAL,
    SPIO_COMPONENTS_STATUSES,
    SPIO_INCIDENTS_STATUSES,
    SPIO_INDICATORS,
)


class StatusPageIOSummary(NamedTuple):
    name: str
    status: str
    incidents: list
    components: list

    @classmethod
    def _get_components(cls, data):
        all_components = data["components"]
        damaged_components = [
            c for c in all_components if c["status"] != SPIO_COMPONENT_OPERATIONAL
        ]
        filtered_data = []
        important_keys = ("name", "status", "description")
        for component in damaged_components:
            component_data = {k: component.get(k, None) for k in important_keys}
            component_data["status"] = SPIO_COMPONENTS_STATUSES[
                component_data["status"]
            ]
            filtered_data.append(component_data)
        return filtered_data

    @classmethod
    def _get_incidents(cls, data):
        incidents = data["incidents"]
        filtered_data = []
        important_keys = ("name", "status", "impact")
        for component in incidents:
            component_data = {k: component.get(k, None) for k in important_keys}
            component_data["status"] = SPIO_INCIDENTS_STATUSES[component_data["status"]]
            filtered_data.append(component_data)
        return filtered_data

    @classmethod
    def from_data(cls, name, data):
        status = data["status"]
        status_type = SPIO_INDICATORS[status["indicator"]]
        return cls(
            name=name,
            status=status_type,
            incidents=cls._get_incidents(data),
            components=cls._get_components(data),
        )


class BaseStatusPageAPI(BaseServiceAPI):
    domain_id: str = None

    def _get_base_url(self):
        """Statuspage.io API URL for given service."""
        if not self.domain_id:
            raise NotImplementedError("Please, add domain id")
        return f"https://{self.domain_id}.statuspage.io/api/v2/"

    def get_summary(self):
        url = self._get_base_url() + "summary.json"
        response = requests.get(url)
        response.raise_for_status()
        return StatusPageIOSummary.from_data(name=self.name, data=response.json())
