import respx

from statuscheck.services.models.statuspageio import STATUS_MAINTENANCE
from statuscheck.utils import get_statuscheck_api


class TestCloudAMQP:
    @respx.mock
    def test_ok(self):
        with open(
            "tests/test_services/test_data/cloudamqp_maintenance.json", "rb"
        ) as f:
            mock_response_body = f.read()
        respx.get(
            "https://2126xm8ctzlk.statuspage.io/api/v2/summary.json",
            status_code=200,
            content=mock_response_body,
        )

        service_name = "cloudamqp"
        service_api = get_statuscheck_api(service_name)

        assert service_api._module_name == service_name
        assert service_api.status_url
        assert service_api.service_url
        assert service_api.summary

        assert service_api.summary.status
        assert service_api.summary.incidents
        assert service_api.summary.components

        assert service_api.summary.status.code == STATUS_MAINTENANCE
        assert len(service_api.summary.incidents) == 1
        assert len(service_api.summary.components) == 23
