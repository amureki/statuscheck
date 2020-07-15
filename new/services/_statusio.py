from new.services._base import BaseServiceAPI
from new.statusio.models import Component, Incident, Status, Summary

import httpx


class BaseStatusIOAPI(BaseServiceAPI):
    """
    Status.io pages API handler.

    API v2: https://statusio.docs.apiary.io
    Public status API: https://kb.status.io/developers/public-status-api/
    """

    domain_id: str = None

    def _get_base_url(self) -> str:
        if not self.domain_id:
            raise NotImplementedError("Please, add domain id")
        return f"https://api.status.io/1.0/status/{self.domain_id}"

    def get_simple_status(self):
        url = self._get_base_url()
        response_json = httpx.get(url).json()
        status_dict = response_json["result"]["status_overall"]
        status = Status(**status_dict)
        return status

    def get_summary(self):
        url = self._get_base_url()
        response_json = httpx.get(url).json()

        status_dict = response_json["result"]["status_overall"]
        status = Status(
            description=status_dict["status"],
            status_code=status_dict["status_code"],
            updated=status_dict["updated"],
        )

        components = [
            Component(
                component["id"],
                component["name"],
                component["updated"],
                component["status"],
                component["status_code"],
            )
            for component in response_json["result"]["status"]
        ]
        # incident payload contains trimmed component data, so we need to enrich it
        components_dict = {component.id: component for component in components}
        incidents = [
            Incident(
                incident["_id"],
                incident["name"],
                incident["datetime_open"],
                [
                    Component(
                        component["_id"],
                        component["name"],
                        components_dict[component["_id"]].updated,
                        components_dict[component["_id"]].status,
                        components_dict[component["_id"]].status_code,
                    )
                    for component in incident.get("components_affected", [])
                ],
            )
            for incident in response_json["result"]["incidents"]
        ]

        return Summary(status, components, incidents)
