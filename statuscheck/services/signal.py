from html.parser import HTMLParser

import httpx

from statuscheck.services.bases._base import BaseServiceAPI
from statuscheck.services.models.generic import (
    TYPE_GOOD,
    TYPE_INCIDENT,
    Status,
    Summary,
)

STATUS_OK = "Signal is up and running."

STATUS_TYPE_MAPPING = {
    STATUS_OK: TYPE_GOOD,
}


class ParseSignalStatusPage(HTMLParser):
    is_relevant: bool = False
    data: list = []

    def handle_data(self, data):
        if self.is_relevant:
            self.data.append(data)

    def handle_starttag(self, tag, attrs):
        # Only parse the 'div' tag.
        if tag == "div":
            self.is_relevant = True

    def handle_endtag(self, tag):
        if tag == "div":
            self.is_relevant = False


class ServiceAPI(BaseServiceAPI):
    """Signal status page API handler."""

    name = "Signal"
    base_url = "https://status.signal.org/"
    status_url = base_url
    service_url = "https://signal.org/"

    def get_summary(self) -> Summary:
        response = httpx.get(self.base_url)
        response.raise_for_status()
        text = response.text
        if STATUS_OK in text:
            status = Status(
                code=STATUS_OK,
                name=STATUS_TYPE_MAPPING[STATUS_OK],
                description=STATUS_TYPE_MAPPING[STATUS_OK],
                is_ok=True,
            )
            return Summary(status=status, components=[], incidents=[])
        else:
            html_parser = ParseSignalStatusPage()
            html_parser.feed(response.text)
            parsed_data = html_parser.data
            # usual structure is:
            # div (0), then span (1), then text status (2)
            raw_status = parsed_data[2]
            status_text = raw_status.strip()
            status = Status(
                code=status_text,
                name=TYPE_INCIDENT,
                description=status_text,
                is_ok=False,
            )
            return Summary(status=status, components=[], incidents=[])
