import respx

from statuscheck.utils import get_statuscheck_api


class TestGithub:
    @respx.mock
    def test_ok(self):
        with open("tests/test_services/test_data/docker_partial.json", "rb") as f:
            mock_response_body = f.read()
        respx.get(
            "https://api.status.io/1.0/status/533c6539221ae15e3f000031",
            status_code=200,
            content=mock_response_body,
        )

        service_name = "docker"
        service_api = get_statuscheck_api(service_name)

        assert service_api._module_name == service_name
        assert service_api.status_url
        assert service_api.service_url
        assert service_api.summary

        assert service_api.summary.status
        assert service_api.summary.incidents
        assert service_api.summary.components

        assert service_api.summary.status.code == 400
        assert len(service_api.summary.incidents) == 1
        assert len(service_api.summary.components) == 8
