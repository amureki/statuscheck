import respx
from httpx import Response

from statuscheck.services.heroku import STATUS_BLUE, STATUS_YELLOW
from statuscheck.services.models.generic import (
    COMPONENT_TYPE_MAINTENANCE,
    COMPONENT_TYPE_PARTIAL_OUTAGE,
)
from statuscheck.utils import get_statuscheck_api


class TestSlack:
    @respx.mock
    def test_incident(self):
        with open("tests/test_services/test_data/heroku_incident.json", "rb") as f:
            mock_response_body = f.read()
        respx.get(
            "https://status.heroku.com/api/v4/current-status",
        ).mock(return_value=Response(200, content=mock_response_body))

        service_name = "heroku"
        service_api = get_statuscheck_api(service_name)

        assert service_api._module_name == service_name
        assert service_api.status_url
        assert service_api.service_url
        assert service_api.summary

        assert service_api.summary.status
        assert service_api.summary.incidents
        assert service_api.summary.components

        assert service_api.summary.status.code == STATUS_YELLOW
        assert len(service_api.summary.incidents) == 1
        assert len(service_api.summary.components) == 3

        component = service_api.summary.components[0]
        assert component.status == COMPONENT_TYPE_PARTIAL_OUTAGE

    @respx.mock
    def test_maintenance(self):
        with open("tests/test_services/test_data/heroku_maintenance.json", "rb") as f:
            mock_response_body = f.read()
        respx.get(
            "https://status.heroku.com/api/v4/current-status",
        ).mock(return_value=Response(200, content=mock_response_body))

        service_name = "heroku"
        service_api = get_statuscheck_api(service_name)

        assert service_api._module_name == service_name
        assert service_api.status_url
        assert service_api.service_url
        assert service_api.summary

        assert service_api.summary.status
        assert not service_api.summary.incidents
        assert service_api.summary.components

        assert service_api.summary.status.code == STATUS_BLUE
        assert len(service_api.summary.incidents) == 0
        assert len(service_api.summary.components) == 3

        component = service_api.summary.components[1]
        assert component.status == COMPONENT_TYPE_MAINTENANCE
