from typing import NamedTuple

import requests

import statuscheck.status_types
from statuscheck.services._base import BaseServiceAPI


class SalesforceSummary(NamedTuple):
    name: str
    status: str
    incidents: list
    components: list

    @classmethod
    def _get_incidents(cls, summary):
        pass

    @classmethod
    def from_data(cls, name, data):
        return cls(
            name=name,
            status=data["status"],
            incidents=data["incidents"],
            components=data["components"],
        )


class ServiceAPI(BaseServiceAPI):
    STATUS_OK = "OK"
    STATUS_UNKNOWN = "UNKNOWN"
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
        STATUS_OK: statuscheck.status_types.TYPE_GOOD,
        STATUS_CORE_INCIDENT: statuscheck.status_types.TYPE_INCIDENT,
        STATUS_NONCORE_INCIDENT: statuscheck.status_types.TYPE_INCIDENT,
        STATUS_CORE_OUTAGE: statuscheck.status_types.TYPE_OUTAGE,
        STATUS_NONCORE_OUTAGE: statuscheck.status_types.TYPE_OUTAGE,
        STATUS_CORE_MAINTENANCE: statuscheck.status_types.TYPE_MAINTENANCE,
        STATUS_NONCORE_MAINTENANCE: statuscheck.status_types.TYPE_MAINTENANCE,
        STATUS_UNKNOWN: statuscheck.status_types.TYPE_UNKNOWN,
    }

    name = "Salesforce"
    base_url = "https://api.status.salesforce.com/v1/"
    status_url = "https://status.salesforce.com"

    def get_summary(self):
        self.data = self._get_status_data()
        return SalesforceSummary.from_data(
            name=self.name,
            data={
                "status": self.get_general_status(),
                "incidents": self.get_incidents(),
                "components": self.get_components(),
            },
        )

    def _get_status_data(self):
        url = self.base_url + "instances/status/preview"
        response = requests.get(url)
        response.raise_for_status()
        return response.json()

    def get_components(self):
        servers = self._get_affected_servers()
        for server in servers:
            server["status"] = self.STATUS_TYPE_MAPPING[server["status"]]
        return servers

    def _get_affected_servers(self) -> list:
        servers = []
        for server in self.data:
            if server.get("status") != self.STATUS_OK:
                server["name"] = server["key"]
                servers.append(server)
        return servers

    def _get_general_incidents(self):
        incidents = self.get_incidents()
        general_incidents = []
        for incident in incidents:
            if incident["affectsAll"]:
                general_incidents.append(incident)
        return general_incidents

    def get_incidents(self):
        incident_keys = []
        incidents = []
        affected_servers = self._get_affected_servers()
        affected_server_keys = [s["key"] for s in affected_servers]
        if not affected_servers:
            return []

        for server in affected_servers:
            if server["key"] not in affected_server_keys:
                continue

            server_incidents = server["Incidents"]
            for incident in server_incidents:
                if incident["id"] in incident_keys:
                    continue

                incident["name"] = incident["IncidentImpacts"][0]["type"]
                incident["server_status"] = self.STATUS_TYPE_MAPPING[server["status"]]
                incidents.append(incident)
                incident_keys.append(incident["id"])

        return incidents

    def get_general_status(self):
        incidents = self._get_general_incidents()
        if not incidents:
            return self.STATUS_TYPE_MAPPING[self.STATUS_OK]

        return incidents[0]["server_status"]
