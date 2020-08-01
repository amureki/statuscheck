import httpx

from statuscheck.services.bases._base import BaseServiceAPI
from statuscheck.services.models.generic import Status, Summary


class ServiceAPI(BaseServiceAPI):
    """Signal status page API handler."""

    STATUS_OK = "Signal is up and running."
    STATUS_TYPE_MAPPING = {STATUS_OK: "No issues"}

    name = "Signal"
    base_url = "https://status.signal.org/"
    status_url = base_url
    service_url = "https://signal.org/"

    def get_summary(self) -> Summary:
        response = httpx.get(self.base_url)
        response.raise_for_status()
        text = response.text
        if self.STATUS_OK in text:
            status = Status(
                code=self.STATUS_OK,
                description=self.STATUS_TYPE_MAPPING[self.STATUS_OK],
                is_ok=True,
            )
            return Summary(status=status, components=[], incidents=[])
        else:
            raise NotImplementedError("Signal status not implemented: %s", text)
