import respx
from httpx import Response

from statuscheck.services.bases._statuspageio import STATUS_MAJOR
from statuscheck.services.models.generic import COMPONENT_TYPE_PARTIAL_OUTAGE
from statuscheck.utils import get_statuscheck_api


class TestGithub:
    @respx.mock
    def test_incident(self):
        with open("tests/test_services/test_data/github_incident.json", "rb") as f:
            mock_response_body = f.read()
        respx.get(
            "https://kctbh9vrtdwd.statuspage.io/api/v2/summary.json",
        ).mock(return_value=Response(200, content=mock_response_body))

        service_name = "github"
        service_api = get_statuscheck_api(service_name)

        assert service_api._module_name == service_name
        assert service_api.status_url
        assert service_api.service_url
        assert service_api.summary

        assert service_api.summary.status
        assert service_api.summary.incidents
        assert service_api.summary.components

        assert service_api.summary.status.code == STATUS_MAJOR
        assert len(service_api.summary.incidents) == 3
        assert len(service_api.summary.components) == 2

        component = service_api.summary.components[0]
        assert component.status == COMPONENT_TYPE_PARTIAL_OUTAGE
