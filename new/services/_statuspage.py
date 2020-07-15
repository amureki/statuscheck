from new.services._base import BaseServiceAPI
from new.statuspage.models import Component, Incident, Status, Summary

import httpx


class BaseStatusPageAPI(BaseServiceAPI):
    """
    Statuspage.io pages API handler.

    API: https://developer.statuspage.io/
    """

    domain_id: str = None

    def _get_base_url(self) -> str:
        """Statuspage.io API URL for given service."""
        if not self.domain_id:
            raise NotImplementedError("Please, add domain id")
        return f"https://{self.domain_id}.statuspage.io/api/v2/"

    def get_simple_status(self) -> Status:
        url = self._get_base_url() + "status.json"
        response_json = httpx.get(url).json()
        status_dict = response_json["status"]
        status = Status(**status_dict)
        return status

    def get_summary(self) -> Summary:
        url = self._get_base_url() + "summary.json"
        # with open("tests/test_services/test_data/github_summary.json", "rb") as f:
        #     import json
        #     data = json.load(f)
        # response_json = data
        response_json = httpx.get(url).json()
        status_dict = response_json["status"]
        status = Status(**status_dict)
        incidents = [
            Incident(
                incident["id"],
                incident["name"],
                incident["status"],
                incident["impact"],
                incident.get("scheduled_for"),
                incident.get("scheduled_until"),
                [
                    Component(
                        component["id"],
                        component["description"],
                        component["status"],
                        component["name"],
                        component.get("only_show_if_degraded"),
                    )
                    for component in incident.get("components", [])
                ],
            )
            for incident in response_json["incidents"]
            + response_json["scheduled_maintenances"]
        ]
        components = [
            Component(
                component["id"],
                component["description"],
                component["status"],
                component["name"],
                component.get("only_show_if_degraded"),
            )
            for component in response_json["components"]
        ]

        return Summary(status, components, incidents)
