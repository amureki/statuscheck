import httpx

from statuscheck.services.bases._base import BaseServiceAPI
from statuscheck.services.models.generic import (
    TYPE_CRITICAL,
    TYPE_GOOD,
    TYPE_INCIDENT,
    TYPE_MAINTENANCE,
    TYPE_OUTAGE,
    Component,
    Incident,
    Status,
    Summary,
)

STATUS_NONE = "none"
STATUS_MINOR = "minor"
STATUS_MAJOR = "major"
STATUS_CRITICAL = "critical"
STATUS_MAINTENANCE = "maintenance"

STATUS_TYPE_MAPPING = {
    STATUS_NONE: TYPE_GOOD,
    STATUS_MINOR: TYPE_INCIDENT,
    STATUS_MAJOR: TYPE_OUTAGE,
    STATUS_CRITICAL: TYPE_CRITICAL,
    STATUS_MAINTENANCE: TYPE_MAINTENANCE,
}


class BaseStatusPageAPI(BaseServiceAPI):
    """
    Statuspage.io pages API handler.

    Documentation: https://developer.statuspage.io/
    """

    domain_id: str = ""

    def _get_base_url(self) -> str:
        """Statuspage.io API URL for given service."""
        if not self.domain_id:
            raise NotImplementedError("Please, add domain id")
        return f"https://{self.domain_id}.statuspage.io/api/v2/"

    def get_summary(self) -> Summary:
        url = self._get_base_url() + "summary.json"
        response_json = httpx.get(url).json()
        status_dict = response_json["status"]
        status = Status(
            code=status_dict["indicator"],
            name=STATUS_TYPE_MAPPING[status_dict["indicator"]],
            description=status_dict["description"],
            is_ok=status_dict["indicator"] == STATUS_NONE,
        )

        incidents = [
            Incident(
                id=incident["id"],
                name=incident["name"],
                status=incident["status"],
                components=[
                    Component(
                        id=component["id"],
                        name=component["name"],
                        status=component["status"],
                    )
                    for component in incident.get("components", [])
                ],
                extra_data=incident,
            )
            for incident in response_json["incidents"]
            + response_json["scheduled_maintenances"]
        ]

        components = [
            Component(
                id=component["id"],
                name=component["name"],
                status=component["status"],
                extra_data=component,
            )
            for component in response_json["components"]
        ]

        return Summary(status, components, incidents)
