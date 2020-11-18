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

STATUS_OK = "OK"
STATUS_CORE_OUTAGE = "MAJOR_INCIDENT_CORE"
STATUS_NONCORE_OUTAGE = "MAJOR_INCIDENT_NONCORE"
STATUS_CORE_INCIDENT = "MINOR_INCIDENT_CORE"
STATUS_NONCORE_INCIDENT = "MINOR_INCIDENT_NONCORE"
STATUS_CORE_MAINTENANCE = "MAINTENANCE_CORE"
STATUS_NONCORE_MAINTENANCE = "MAINTENANCE_NONCORE"

# sorted by severity
NOT_GOOD_STATUSES = [
    STATUS_CORE_OUTAGE,
    STATUS_NONCORE_OUTAGE,
    STATUS_CORE_INCIDENT,
    STATUS_NONCORE_INCIDENT,
    STATUS_CORE_MAINTENANCE,
    STATUS_NONCORE_MAINTENANCE,
]

STATUS_TYPE_MAPPING = {
    STATUS_OK: TYPE_GOOD,
    STATUS_CORE_INCIDENT: TYPE_INCIDENT,
    STATUS_NONCORE_INCIDENT: TYPE_INCIDENT,
    STATUS_CORE_OUTAGE: TYPE_OUTAGE,
    STATUS_NONCORE_OUTAGE: TYPE_OUTAGE,
    STATUS_CORE_MAINTENANCE: TYPE_MAINTENANCE,
    STATUS_NONCORE_MAINTENANCE: TYPE_MAINTENANCE,
}


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
            Component(
                name=component["key"],
                status=component["status"],
                extra_data=component,
            )
            for component in components_raw
        ]

        incidents = [
            Incident(
                id=str(incident["id"]),
                name=localizations[incident["type"]],
                status=incident["status"],
                components=[
                    component
                    for component in components
                    if component.name in incident["instanceKeys"]
                ],
                extra_data=incident,
            )
            for incident in incidents_raw
        ]

        status = Status(
            code=STATUS_OK,
            name=STATUS_TYPE_MAPPING[STATUS_OK],
            description=STATUS_TYPE_MAPPING[STATUS_OK],
            is_ok=True,
        )

        for incident in incidents:
            if incident.extra_data["affectsAll"]:
                status.code = incident.status
                status.description = STATUS_TYPE_MAPPING[incident.status]
                break

        return Summary(status, components, incidents)
