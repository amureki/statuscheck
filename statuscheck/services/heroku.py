import httpx

from statuscheck.services.bases._base import BaseServiceAPI
from statuscheck.services.models.generic import Component, Incident, Status, Summary
from statuscheck.services.models.heroku import (
    STATUS_GREEN,
    STATUS_RED,
    STATUS_TYPE_MAPPING,
    STATUS_YELLOW,
    Component as _Component,
    Incident as _Incident,
    Status as _Status,
    Summary as _Summary,
)


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
        summary = self._get_summary()
        components = [
            Component(name=component.name, status=component.status,)
            for component in summary.components
        ]
        incidents = [
            Incident(
                id=incident.id,
                name=incident.title,
                status=incident.state,
                components=[
                    Component(name=component.name, status=component.status,)
                    for component in incident.components
                ],
            )
            for incident in summary.incidents
        ]
        status = Status(
            code=summary.status.code,
            name=summary.status.description,
            description=summary.status.description,
            is_ok=summary.status.is_ok,
        )
        return Summary(status=status, components=components, incidents=incidents,)

    def _get_summary(self) -> _Summary:
        url = self.base_url + "current-status"
        response_json = httpx.get(url).json()
        status_list = response_json["status"]
        incidents_list = response_json["incidents"]
        # scheduled_list = response_json["scheduled"]

        incidents = [
            _Incident(
                id=incident["id"],
                title=incident["title"],
                state=incident["state"],
                components=[
                    _Component(name=component["system"], status=component["status"],)
                    for component in status_list
                ],
            )
            for incident in incidents_list
        ]
        components = [
            _Component(name=component["system"], status=component["status"],)
            for component in status_list
        ]

        worst_status = STATUS_GREEN

        for component in components:
            if component.status == STATUS_RED:
                worst_status = component.status
            if component.status == STATUS_YELLOW and worst_status != STATUS_RED:
                worst_status = component.status

        status = _Status(
            code=worst_status, description=STATUS_TYPE_MAPPING[worst_status],
        )

        return _Summary(status, components, incidents)
