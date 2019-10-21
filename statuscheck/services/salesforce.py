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
                "incidents": self._get_incidents(),
                "components": self._get_affected_servers(),
            },
        )

    def _get_status_data(self):
        url = self.base_url + "instances/status/preview"
        response = requests.get(url)
        response.raise_for_status()
        return response.json()

    def _get_affected_servers(self) -> list:
        servers = []
        for server in self.data:
            if server.get("status") != self.STATUS_OK:
                servers.append(server)
        return servers

    def _get_incidents(self):
        incidents = []
        affected_servers = self._get_affected_servers()
        if not affected_servers:
            return incidents
        for server in affected_servers:
            data = server["Incidents"]
            data["key"] = server["key"]
            data["status"] = server["status"]
            incidents.append(data)
        return incidents

    def get_general_status(self):
        incidents = self._get_incidents()
        if not incidents:
            return self.STATUS_TYPE_MAPPING[self.STATUS_OK]
        for incident in incidents:
            if incident["affectsAll"]:
                return self.STATUS_TYPE_MAPPING[incident["status"]]
