from typing import NamedTuple

from statuscheck.services._custompage import BaseCustomStatusPageAPI
from statuscheck.status_types import TYPE_GOOD


class SignalSummary(NamedTuple):
    name: str
    status: str
    incidents: list

    @classmethod
    def from_data(cls, name, data):
        return cls(name=name, status=data["status"], incidents=data["incidents"])


class ServiceAPI(BaseCustomStatusPageAPI):
    STATUS_TYPE_MAPPING = {"Signal is up and running.": TYPE_GOOD}

    name = "Signal"
    base_url = "https://status.signal.org/"
    status_url = base_url

    def get_summary(self):
        html = self._get_html_response()
        status_raw = html.find("div", first=True).text
        status_text = status_raw.split("\n", 1)[1]
        # TODO: parse incidents
        status_type = self.STATUS_TYPE_MAPPING.get(status_text, "")
        incidents = []
        if status_type != TYPE_GOOD:
            incidents.append({"name": status_text, "status": status_type})
        return SignalSummary.from_data(
            name=self.name, data={"status": status_type, "incidents": incidents}
        )
