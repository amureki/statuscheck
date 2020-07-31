import respx

from statuscheck.services.models.salesforce import STATUS_CORE_INCIDENT
from statuscheck.utils import get_statuscheck_api


class TestGithub:
    @respx.mock
    def test_ok(self):
        with open("tests/test_services/test_data/salesforce_incident.json", "rb") as f:
            mock_response_body = f.read()
        respx.get(
            "https://api.status.salesforce.com/v1/instances/status/preview",
            status_code=200,
            content=mock_response_body,
        )

        with open(
            "tests/test_services/test_data/salesforce_localizations.json", "rb"
        ) as f:
            mock_response_body = f.read()
        respx.get(
            "https://api.status.salesforce.com/v1/localizations",
            status_code=200,
            content=mock_response_body,
        )

        service_name = "salesforce"
        service_api = get_statuscheck_api(service_name)

        assert service_api._module_name == service_name
        assert service_api.status_url
        assert service_api.service_url
        assert service_api.summary

        assert service_api.summary.status
        assert service_api.summary.incidents
        assert service_api.summary.components

        assert service_api.summary.status.code == STATUS_CORE_INCIDENT
        assert len(service_api.summary.incidents) == 1
        assert len(service_api.summary.components) == 1
