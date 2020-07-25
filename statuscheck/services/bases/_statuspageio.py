import httpx

from statuscheck.services.bases._base import BaseServiceAPI
from statuscheck.services.models.generic import Component, Incident, Status, Summary
from statuscheck.services.models.statuspageio import (
    Component as _Component,
    Incident as _Incident,
    Status as _Status,
    Summary as _Summary,
)


class BaseStatusPageAPI(BaseServiceAPI):
    """
    Statuspage.io pages API handler.

    Documentation: https://developer.statuspage.io/
    """

    domain_id: str = None

    def _get_base_url(self) -> str:
        """Statuspage.io API URL for given service."""
        if not self.domain_id:
            raise NotImplementedError("Please, add domain id")
        return f"https://{self.domain_id}.statuspage.io/api/v2/"

    def get_status(self) -> Status:
        statuspageio_status = self._get_status()
        return Status(
            code=statuspageio_status.indicator,
            description=statuspageio_status.description,
        )

    def get_summary(self) -> Summary:
        statuspageio_summary = self._get_summary()
        incidents = [
            Incident(
                id=incident.id,
                name=incident.name,
                status=incident.status,
                components=[
                    Component(
                        id=component.id, name=component.name, status=component.status,
                    )
                    for component in incident.components
                ],
            )
            for incident in statuspageio_summary.incidents
        ]
        components = [
            Component(id=component.id, name=component.name, status=component.status,)
            for component in statuspageio_summary.components
        ]
        summary = Summary(
            status=statuspageio_summary.status,
            components=components,
            incidents=incidents,
        )
        return summary

    def _get_status(self) -> _Status:
        url = self._get_base_url() + "status.json"
        response_json = httpx.get(url).json()
        status_dict = response_json["status"]
        return Status(**status_dict)

    def _get_summary(self) -> _Summary:
        url = self._get_base_url() + "summary.json"
        # with open("tests/test_services/test_data/github_summary.json", "rb") as f:
        #     import json
        #     data = json.load(f)
        # response_json = data
        response_json = httpx.get(url).json()
        status_dict = response_json["status"]
        status = _Status(**status_dict)
        incidents = [
            _Incident(
                incident["id"],
                incident["name"],
                incident["status"],
                incident["impact"],
                incident.get("scheduled_for"),
                incident.get("scheduled_until"),
                [
                    _Component(
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
            _Component(
                component["id"],
                component["description"],
                component["status"],
                component["name"],
                component.get("only_show_if_degraded"),
            )
            for component in response_json["components"]
        ]
        return _Summary(status, components, incidents)
