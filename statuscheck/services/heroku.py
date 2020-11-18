import httpx

from statuscheck.services.bases._base import BaseServiceAPI
from statuscheck.services.models.generic import (
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
                        status=component["status"],
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
                status=component["status"],
                extra_data=component,
            )
            for component in status_list
        ]

        worst_status = STATUS_GREEN

        for component in components:
            if component.status == STATUS_RED:
                worst_status = component.status
            if component.status == STATUS_YELLOW and worst_status != STATUS_RED:
                worst_status = component.status

        status = Status(
            code=worst_status,
            name=STATUS_TYPE_MAPPING[worst_status],
            description=STATUS_TYPE_MAPPING[worst_status],
            is_ok=worst_status == STATUS_GREEN,
        )

        return Summary(status, components, incidents)
