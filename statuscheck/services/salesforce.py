import httpx

from statuscheck.services.bases._base import BaseServiceAPI
from statuscheck.services.models.generic import Component, Incident, Status, Summary
from statuscheck.services.models.salesforce import (
    STATUS_OK,
    STATUS_TYPE_MAPPING,
    Component as _Component,
    Incident as _Incident,
    Status as _Status,
    Summary as _Summary,
)


class ServiceAPI(BaseServiceAPI):
    """
    Salesforce status page API handler.

    Documentation: https://api.status.salesforce.com/v1/docs/
    """

    name = "Salesforce"
    base_url = "https://api.status.salesforce.com/v1/"
    status_url = "https://status.salesforce.com"
    service_url = "https://salesforce.com/"

    def get_summary(self) -> Summary:
        summary = self._get_summary()
        components = [
            Component(name=component.key, status=component.status,)
            for component in summary.components
        ]
        incidents = [
            Incident(
                id=str(incident.id),
                name=incident.text,
                status=incident.status,
                components=[
                    Component(
                        name=component.key,
                        # we put status in the incident, so we don't need it here
                        # status=component.status,
                    )
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
        url = self.base_url + "instances/status/preview"
        localizations_url = self.base_url + "localizations"
        response = httpx.get(url)
        response.raise_for_status()
        response_json = response.json()

        localizations_response = httpx.get(localizations_url)
        localizations_response.raise_for_status()
        localizations_response_json = localizations_response.json()
        localizations = {
            localization["modelKey"]: localization["text"]
            for localization in localizations_response_json
        }

        components_list = response_json
        incidents_raw = []
        incident_keys = []
        components_raw = []

        for component in components_list:
            if component["status"] != STATUS_OK:
                components_raw.append(component)
                component_incidents = component["Incidents"]
                for incident in component_incidents:
                    if incident["id"] in incident_keys:
                        continue
                    incident_keys.append(incident["id"])
                    incident["type"] = incident["IncidentImpacts"][0]["type"]
                    incident["status"] = component["status"]
                    incidents_raw.append(incident)

        components = [
            _Component(
                key=component["key"],
                location=component["location"],
                environment=component["environment"],
                status=component["status"],
                is_active=component["isActive"],
            )
            for component in components_raw
        ]

        incidents = [
            _Incident(
                id=incident["id"],
                type=incident["type"],
                text=localizations[incident["type"]],
                affects_all=incident["affectsAll"],
                is_core=incident["isCore"],
                status=incident["status"],
                instance_keys=incident["instanceKeys"],
                components=[
                    component
                    for component in components
                    if component.key in incident["instanceKeys"]
                ],
            )
            for incident in incidents_raw
        ]

        status = _Status(code=STATUS_OK, description=STATUS_TYPE_MAPPING[STATUS_OK])
        for incident in incidents:
            if incident.affects_all:
                status.code = incident.status
                status.description = STATUS_TYPE_MAPPING[incident.status]
                break

        return _Summary(status, components, incidents)
