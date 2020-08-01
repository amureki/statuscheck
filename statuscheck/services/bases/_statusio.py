import httpx

from statuscheck.services.bases._base import BaseServiceAPI
from statuscheck.services.models.generic import Component, Incident, Status, Summary
from statuscheck.services.models.statusio import (
    STATUS_TYPE_MAPPING,
    Component as _Component,
    Incident as _Incident,
    Status as _Status,
    Summary as _Summary,
)


class BaseStatusIOAPI(BaseServiceAPI):
    """
    Status.io pages API handler.

    Documentation: https://statusio.docs.apiary.io
    Public status API: https://kb.status.io/developers/public-status-api/
    """

    domain_id: str = None

    def _get_base_url(self) -> str:
        if not self.domain_id:
            raise NotImplementedError("Please, add domain id")
        return f"https://api.status.io/1.0/status/{self.domain_id}"

    def get_summary(self) -> Summary:
        summary = self._get_summary()
        incidents = [
            Incident(
                id=incident._id,
                name=incident.name,
                status="",
                components=[
                    Component(
                        id=component.id, name=component.name, status=component.status,
                    )
                    for component in incident.components
                ],
            )
            for incident in summary.incidents
        ]
        components = [
            Component(id=component.id, name=component.name, status=component.status,)
            for component in summary.components
        ]
        status = Status(
            code=summary.status.status_code,
            name=STATUS_TYPE_MAPPING[summary.status.status_code],
            description=summary.status.description,
            is_ok=summary.status.is_ok,
        )
        return Summary(status=status, components=components, incidents=incidents,)

    def _get_summary(self) -> _Summary:
        url = self._get_base_url()
        response_json = httpx.get(url).json()
        status_dict = response_json["result"]["status_overall"]
        status = _Status(
            description=status_dict["status"],
            status_code=status_dict["status_code"],
            updated=status_dict["updated"],
        )

        components = [
            _Component(
                component["id"],
                component["name"],
                component["updated"],
                component["status"],
                component["status_code"],
            )
            for component in response_json["result"]["status"]
        ]
        # incident payload contains trimmed component data, so we need to enrich it
        components_dict = {component.id: component for component in components}
        incidents = [
            _Incident(
                incident["_id"],
                incident["name"],
                incident["datetime_open"],
                [
                    _Component(
                        component["_id"],
                        component["name"],
                        components_dict[component["_id"]].updated,
                        components_dict[component["_id"]].status,
                        components_dict[component["_id"]].status_code,
                    )
                    for component in incident.get("components_affected", [])
                ],
            )
            for incident in response_json["result"]["incidents"]
        ]

        return _Summary(status, components, incidents)
