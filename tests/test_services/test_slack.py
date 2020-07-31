import respx

from statuscheck.services.models.slack import STATUS_ACTIVE
from statuscheck.utils import get_statuscheck_api


class TestGithub:
    @respx.mock
    def test_ok(self):
        with open("tests/test_services/test_data/slack_incident.json", "rb") as f:
            mock_response_body = f.read()
        respx.get(
            "https://status.slack.com/api/v2.0.0/current",
            status_code=200,
            content=mock_response_body,
        )

        service_name = "slack"
        service_api = get_statuscheck_api(service_name)

        assert service_api._module_name == service_name
        assert service_api.status_url
        assert service_api.service_url
        assert service_api.summary

        assert service_api.summary.status
        assert service_api.summary.incidents
        assert service_api.summary.components

        assert service_api.summary.status.code == STATUS_ACTIVE
        assert len(service_api.summary.incidents) == 2
        assert len(service_api.summary.components) == 2
