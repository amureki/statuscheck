import respx
from httpx import Response

from statuscheck.services.models.generic import (
    COMPONENT_TYPE_MAINTENANCE,
    COMPONENT_TYPE_SECURITY,
)
from statuscheck.utils import get_statuscheck_api


class TestGitlab:
    @respx.mock
    def test_security(self):
        with open("tests/test_services/test_data/gitlab_security.json", "rb") as f:
            mock_response_body = f.read()
        respx.get(
            "https://api.status.io/1.0/status/5b36dc6502d06804c08349f7",
        ).mock(return_value=Response(200, content=mock_response_body))

        service_name = "gitlab"
        service_api = get_statuscheck_api(service_name)

        assert service_api._module_name == service_name
        assert service_api.status_url
        assert service_api.service_url
        assert service_api.summary

        assert service_api.summary.status
        assert service_api.summary.incidents
        assert service_api.summary.components

        assert service_api.summary.status.code == "600"
        assert len(service_api.summary.incidents) == 1
        assert len(service_api.summary.components) == 13

        component = service_api.summary.components[0]
        assert component.status == COMPONENT_TYPE_SECURITY

    @respx.mock
    def test_maintenance(self):
        with open("tests/test_services/test_data/gitlab_maintenance.json", "rb") as f:
            mock_response_body = f.read()
        respx.get(
            "https://api.status.io/1.0/status/5b36dc6502d06804c08349f7",
        ).mock(return_value=Response(200, content=mock_response_body))

        service_name = "gitlab"
        service_api = get_statuscheck_api(service_name)

        assert service_api._module_name == service_name
        assert service_api.status_url
        assert service_api.service_url
        assert service_api.summary

        assert service_api.summary.status
        assert service_api.summary.incidents
        assert service_api.summary.components

        assert service_api.summary.status.code == "200"
        assert len(service_api.summary.incidents) == 1
        assert len(service_api.summary.components) == 15

        component = service_api.summary.components[14]
        assert component.status == COMPONENT_TYPE_MAINTENANCE
