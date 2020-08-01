import httpx

from statuscheck.services.bases._base import BaseServiceAPI
from statuscheck.services.models.generic import Component, Incident, Status, Summary
from statuscheck.services.models.slack import (
    STATUS_TYPE_MAPPING,
    Component as _Component,
    Incident as _Incident,
    Status as _Status,
    Summary as _Summary,
)


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
        summary = self._get_summary()
        status = Status(
            code=summary.status.code,
            name=summary.status.description,
            description=summary.status.description,
            is_ok=summary.status.is_ok,
        )
        components = [
            Component(name=component.name) for component in summary.components
        ]
        incidents = [
            Incident(
                id=incident.id,
                name=incident.title,
                status=incident.status,
                components=[
                    Component(name=component.name) for component in incident.components
                ],
            )
            for incident in summary.incidents
        ]
        return Summary(status=status, components=components, incidents=incidents,)

    def _get_summary(self) -> _Summary:
        url = self.base_url + "current"
        response_json = httpx.get(url).json()
        incidents_list = response_json["active_incidents"]
        status = _Status(
            code=response_json["status"],
            description=STATUS_TYPE_MAPPING[response_json["status"]],
        )

        incidents = [
            _Incident(
                id=incident["id"],
                title=incident["title"],
                status=incident["status"],
                type=incident["type"],
                components=[
                    _Component(name=component) for component in incident["services"]
                ],
            )
            for incident in incidents_list
        ]

        components = []
        for incident in incidents:
            components.extend(incident.components)

        return _Summary(status, components, incidents)
