import httpx

from statuscheck.services.bases._base import BaseServiceAPI
from statuscheck.services.models.generic import (
    TYPE_GOOD,
    TYPE_INCIDENT,
    TYPE_MAINTENANCE,
    Component,
    Incident,
    Status,
    Summary,
)

STATUS_OK = "ok"
STATUS_ACTIVE = "active"
STATUS_RESOLVED = "resolved"
STATUS_SCHEDULED = "scheduled"
STATUS_COMPLETED = "completed"
STATUS_CANCELED = "canceled"

STATUS_TYPE_MAPPING = {
    STATUS_OK: TYPE_GOOD,
    STATUS_ACTIVE: TYPE_INCIDENT,
    STATUS_RESOLVED: TYPE_INCIDENT,
    STATUS_SCHEDULED: TYPE_MAINTENANCE,
    STATUS_COMPLETED: TYPE_MAINTENANCE,
    STATUS_CANCELED: TYPE_MAINTENANCE,
}


class ServiceAPI(BaseServiceAPI):
    """
    Slack status page API handler.

    Documentation: https://api.slack.com/docs/slack-status

    """

    name = "Slack"
    base_url = "https://status.slack.com/api/v2.0.0/"
    status_url = "https://status.slack.com/"
    service_url = "https://slack.com/"

    def get_summary(self) -> Summary:
        url = self.base_url + "current"
        response_json = httpx.get(url).json()
        incidents_list = response_json["active_incidents"]

        status_code = response_json["status"]

        status = Status(
            code=status_code,
            name=STATUS_TYPE_MAPPING[response_json["status"]],
            description=STATUS_TYPE_MAPPING[response_json["status"]],
            is_ok=status_code == STATUS_OK,
        )

        incidents = [
            Incident(
                id=incident["id"],
                name=incident["title"],
                status=incident["status"],
                components=[
                    Component(name=component) for component in incident["services"]
                ],
                extra_data=incident,
            )
            for incident in incidents_list
        ]

        components = []
        for incident in incidents:
            components.extend(incident.components)

        return Summary(status, components, incidents)
