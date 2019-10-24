from typing import NamedTuple

import requests

import statuscheck.status_types
from statuscheck.services._base import BaseServiceAPI

STATUS_TYPE_MAPPING = {
    "green": statuscheck.status_types.TYPE_GOOD,
    "yellow": statuscheck.status_types.TYPE_INCIDENT,
    "red": statuscheck.status_types.TYPE_OUTAGE,
}


class ServiceSummary(NamedTuple):
    name: str
    status: str
    status_development: str
    status_production: str
    incidents: list

    @classmethod
    def _get_incidents(cls, summary):
        incidents = summary["issues"]
        filtered_data = []
        important_keys = ("title", "status_dev", "status_prod", "full_url")
        for component in incidents:
            component_data = {k: component.get(k, None) for k in important_keys}
            component_data["name"] = component_data.pop("title")
            filtered_data.append(component_data)
        return filtered_data

    @classmethod
    def from_data(cls, name, data):
        status_data = data["status"]
        status_production = STATUS_TYPE_MAPPING[status_data["Production"]]
        status_development = STATUS_TYPE_MAPPING[status_data["Development"]]
        status = status_production

        if status_development != statuscheck.status_types.TYPE_GOOD:
            status = status_development
        if status_production != statuscheck.status_types.TYPE_GOOD:
            status = status_production

        return cls(
            name=name,
            status=status,
            status_production=status_production,
            status_development=status_development,
            incidents=cls._get_incidents(data),
        )


class ServiceAPI(BaseServiceAPI):
    name = "Heroku"
    base_url = "https://status.heroku.com/api/v3/"
    status_url = "https://status.heroku.com"

    def get_summary(self):
        url = self.base_url + "current-status"
        response = requests.get(url)
        response.raise_for_status()
        return ServiceSummary.from_data(name=self.name, data=response.json())
