import httpx

from statuscheck.services.bases._base import BaseServiceAPI
from statuscheck.services.models.generic import (
    COMPONENT_TYPE_GOOD,
    COMPONENT_TYPE_MAINTENANCE,
    COMPONENT_TYPE_MAJOR_OUTAGE,
    COMPONENT_TYPE_PARTIAL_OUTAGE,
    TYPE_GOOD,
    TYPE_INCIDENT,
    TYPE_MAINTENANCE,
    TYPE_OUTAGE,
    Component,
    Incident,
    Status,
    Summary,
)

STATUS_GREEN = "green"
STATUS_YELLOW = "yellow"
STATUS_RED = "red"
STATUS_BLUE = "blue"

STATUS_TYPE_MAPPING = {
    STATUS_GREEN: TYPE_GOOD,
    STATUS_YELLOW: TYPE_INCIDENT,
    STATUS_RED: TYPE_OUTAGE,
    STATUS_BLUE: TYPE_MAINTENANCE,
}

COMPONENT_STATUS_GOOD = "green"
COMPONENT_STATUS_MAINTENANCE = "blue"
COMPONENT_STATUS_PARTIAL_OUTAGE = "yellow"
COMPONENT_STATUS_MAJOR_OUTAGE = "red"

COMPONENT_STATUS_MAPPING = {
    COMPONENT_STATUS_GOOD: COMPONENT_TYPE_GOOD,
    COMPONENT_STATUS_MAINTENANCE: COMPONENT_TYPE_MAINTENANCE,
    COMPONENT_STATUS_PARTIAL_OUTAGE: COMPONENT_TYPE_PARTIAL_OUTAGE,
    COMPONENT_STATUS_MAJOR_OUTAGE: COMPONENT_TYPE_MAJOR_OUTAGE,
}


class ServiceAPI(BaseServiceAPI):
    """
    Heroku status page API handler.

    Documentation: https://devcenter.heroku.com/articles/heroku-status

    """

    name = "Heroku"
    base_url = "https://status.heroku.com/api/v4/"
    status_url = "https://status.heroku.com"
    service_url = "https://heroku.com"

    def get_summary(self) -> Summary:
        url = self.base_url + "current-status"
        response_json = httpx.get(url).json()
        status_list = response_json["status"]
        incidents_list = response_json["incidents"]
        # scheduled_list = response_json["scheduled"]

        incidents = [
            Incident(
                id=incident["id"],
                name=incident["title"],
                status=incident["state"],
                components=[
                    Component(
                        name=component["system"],
                        status=COMPONENT_STATUS_MAPPING[component["status"]],
                    )
                    for component in status_list
                ],
                extra_data=incident,
            )
            for incident in incidents_list
        ]
        components = [
            Component(
                name=component["system"],
                status=COMPONENT_STATUS_MAPPING[component["status"]],
                extra_data=component,
            )
            for component in status_list
        ]

        worst_status = STATUS_GREEN

        for component in components:
            if component.status == COMPONENT_TYPE_MAJOR_OUTAGE:
                worst_status = STATUS_RED
            if (
                component.status == COMPONENT_TYPE_PARTIAL_OUTAGE
                and worst_status != COMPONENT_TYPE_MAJOR_OUTAGE
            ):
                worst_status = STATUS_YELLOW
            if (
                component.status == COMPONENT_TYPE_MAINTENANCE
                and worst_status == STATUS_GREEN
            ):
                worst_status = STATUS_BLUE

        status = Status(
            code=worst_status,
            name=STATUS_TYPE_MAPPING[worst_status],
            description=STATUS_TYPE_MAPPING[worst_status],
            is_ok=worst_status in (STATUS_GREEN, STATUS_BLUE),
        )

        return Summary(status, components, incidents)
