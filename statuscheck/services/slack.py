from typing import NamedTuple

import statuscheck.status_types
from statuscheck.services._custompage import BaseCustomStatusPageAPI


class SlackSummary(NamedTuple):
    name: str
    status: str
    incidents: list

    @classmethod
    def from_data(cls, name, data):
        return cls(name=name, status=data["status"], incidents=data["incidents"])


class ServiceAPI(BaseCustomStatusPageAPI):
    STATUS_TYPE_MAPPING = {
        "Ok": statuscheck.status_types.TYPE_GOOD,
        "Incident": statuscheck.status_types.TYPE_INCIDENT,
        "Outage": statuscheck.status_types.TYPE_OUTAGE,
        "Maintenance": statuscheck.status_types.TYPE_MAINTENANCE,
    }

    name = "Slack"
    base_url = "https://status.slack.com/"
    status_url = base_url

    def get_summary(self):
        html = self._get_html_response()
        html_container = html.find(".container", first=True)

        status_icon = html_container.find("img", first=True).attrs.get("src")
        status_icon_type = status_icon.rsplit(".")[0].split("/")[-1]
        status = self.STATUS_TYPE_MAPPING.get(status_icon_type, "")
        description = html_container.find("h1", first=True).text

        # TODO: parse Slack components and their statuses
        incidents = []
        if status != statuscheck.status_types.TYPE_GOOD:
            incidents.append({"name": description, "status": status})
        return SlackSummary.from_data(
            name=self.name, data={"status": status, "incidents": incidents}
        )
