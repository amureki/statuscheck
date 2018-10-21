from statuscheck.check import get_statuscheck_api


def test_get_statuscheck_api():
    service = 'github'
    api = get_statuscheck_api(service)
    assert api.api_name == service
