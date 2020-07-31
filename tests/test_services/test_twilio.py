import respx

from statuscheck.services.models.statuspageio import STATUS_MINOR
from statuscheck.utils import get_statuscheck_api


class TestTwilio:
    @respx.mock
    def test_ok(self):
        with open("tests/test_services/test_data/twilio_incident.json", "rb") as f:
            mock_response_body = f.read()
        respx.get(
            "https://gpkpyklzq55q.statuspage.io/api/v2/summary.json",
            status_code=200,
            content=mock_response_body,
        )

        service_name = "twilio"
        service_api = get_statuscheck_api(service_name)

        assert service_api._module_name == service_name
        assert service_api.status_url
        assert service_api.service_url
        assert service_api.summary

        assert service_api.summary.status
        assert service_api.summary.incidents
        assert service_api.summary.components

        assert service_api.summary.status.code == STATUS_MINOR
        assert len(service_api.summary.incidents) == 11
        assert len(service_api.summary.components) == 73
