import httpx

from statuscheck.services.bases._base import BaseServiceAPI
from statuscheck.services.models.generic import (
    COMPONENT_TYPE_DEGRADED,
    COMPONENT_TYPE_GOOD,
    COMPONENT_TYPE_MAINTENANCE,
    COMPONENT_TYPE_MAJOR_OUTAGE,
    COMPONENT_TYPE_PARTIAL_OUTAGE,
    COMPONENT_TYPE_SECURITY,
    COMPONENT_TYPE_UNKNOWN,
    TYPE_GOOD,
    TYPE_INCIDENT,
    TYPE_MAINTENANCE,
    TYPE_OUTAGE,
    TYPE_SECURITY,
    Component,
    Incident,
    Status,
    Summary,
)

STATUS_OK = 100
STATUS_PLANNED_MAINTENANCE = 200
STATUS_DEGRADED_PERFORMANCE = 300
STATUS_PARTIAL_SERVICE_DISRUPTION = 400
STATUS_MAJOR = 500
STATUS_SECURITY = 600

STATUS_TYPE_MAPPING = {
    STATUS_OK: TYPE_GOOD,
    STATUS_PLANNED_MAINTENANCE: TYPE_MAINTENANCE,
    STATUS_DEGRADED_PERFORMANCE: TYPE_INCIDENT,
    STATUS_PARTIAL_SERVICE_DISRUPTION: TYPE_INCIDENT,
    STATUS_MAJOR: TYPE_OUTAGE,
    STATUS_SECURITY: TYPE_SECURITY,
}

COMPONENT_STATUS_GOOD = 100
COMPONENT_STATUS_MAINTENANCE = 200
COMPONENT_STATUS_DEGRADED = 300
COMPONENT_STATUS_PARTIAL_OUTAGE = 400
COMPONENT_STATUS_MAJOR_OUTAGE = 500
COMPONENT_STATUS_SECURITY = 600
COMPONENT_STATUS_UNKNOWN = ""

COMPONENT_STATUS_MAPPING = {
    COMPONENT_STATUS_GOOD: COMPONENT_TYPE_GOOD,
    COMPONENT_STATUS_MAINTENANCE: COMPONENT_TYPE_MAINTENANCE,
    COMPONENT_STATUS_DEGRADED: COMPONENT_TYPE_DEGRADED,
    COMPONENT_STATUS_PARTIAL_OUTAGE: COMPONENT_TYPE_PARTIAL_OUTAGE,
    COMPONENT_STATUS_MAJOR_OUTAGE: COMPONENT_TYPE_MAJOR_OUTAGE,
    COMPONENT_STATUS_SECURITY: COMPONENT_TYPE_SECURITY,
    COMPONENT_STATUS_UNKNOWN: COMPONENT_TYPE_UNKNOWN,
}


class BaseStatusIOAPI(BaseServiceAPI):
    """
    Status.io pages API handler.

    Documentation: https://statusio.docs.apiary.io
    Public status API: https://kb.status.io/developers/public-status-api/
    """

    domain_id: str = ""

    def _get_base_url(self) -> str:
        if not self.domain_id:
            raise NotImplementedError("Please, add domain id")
        return f"https://api.status.io/1.0/status/{self.domain_id}"

    def get_summary(self) -> Summary:
        url = self._get_base_url()
        response_json = httpx.get(url).json()
        status_dict = response_json["result"]["status_overall"]
        status = Status(
            code=str(status_dict["status_code"]),
            name=STATUS_TYPE_MAPPING[status_dict["status_code"]],
            description=status_dict["status"],
            is_ok=status_dict["status_code"] == 100,
        )

        components = [
            Component(
                id=component["id"],
                name=component["name"],
                status=COMPONENT_STATUS_MAPPING[component["status_code"]],
                extra_data=component,
            )
            for component in response_json["result"]["status"]
        ]

        # incident payload contains trimmed component data, so we need to enrich it
        components_dict = {component.id: component for component in components}
        incidents = [
            Incident(
                id=incident["_id"],
                name=incident["name"],
                components=[
                    Component(
                        id=component["_id"],
                        name=component["name"],
                        status=components_dict[component["_id"]].status,
                    )
                    for component in incident.get("components_affected", [])
                ],
                extra_data=incident,
            )
            for incident in response_json["result"]["incidents"]
        ]

        self.summary = Summary(status, components, incidents)
        return self.summary
