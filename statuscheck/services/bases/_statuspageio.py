import httpx

from statuscheck.services.bases._base import BaseServiceAPI
from statuscheck.services.models.generic import (
    COMPONENT_TYPE_DEGRADED,
    COMPONENT_TYPE_GOOD,
    COMPONENT_TYPE_MAINTENANCE,
    COMPONENT_TYPE_MAJOR_OUTAGE,
    COMPONENT_TYPE_PARTIAL_OUTAGE,
    COMPONENT_TYPE_UNKNOWN,
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

COMPONENT_STATUS_GOOD = "operational"
COMPONENT_STATUS_MAINTENANCE = "under_maintenance"
COMPONENT_STATUS_DEGRADED = "degraded_performance"
COMPONENT_STATUS_PARTIAL_OUTAGE = "partial_outage"
COMPONENT_STATUS_MAJOR_OUTAGE = "major_outage"
COMPONENT_STATUS_UNKNOWN = ""

COMPONENT_STATUS_MAPPING = {
    COMPONENT_STATUS_GOOD: COMPONENT_TYPE_GOOD,
    COMPONENT_STATUS_MAINTENANCE: COMPONENT_TYPE_MAINTENANCE,
    COMPONENT_STATUS_DEGRADED: COMPONENT_TYPE_DEGRADED,
    COMPONENT_STATUS_PARTIAL_OUTAGE: COMPONENT_TYPE_PARTIAL_OUTAGE,
    COMPONENT_STATUS_MAJOR_OUTAGE: COMPONENT_TYPE_MAJOR_OUTAGE,
    COMPONENT_STATUS_UNKNOWN: COMPONENT_TYPE_UNKNOWN,
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
                        status=COMPONENT_STATUS_MAPPING[component["status"]],
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
                status=COMPONENT_STATUS_MAPPING[component["status"]],
                extra_data=component,
            )
            for component in response_json["components"]
        ]

        return Summary(status, components, incidents)
