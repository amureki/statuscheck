import os

import pytest

from statuscheck.check import get_available_services, get_statuscheck_api
from statuscheck.services import SERVICES

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


def test_get_available_services():
    services = get_available_services()
    assert services

    service_files = os.listdir(os.path.join(BASE_DIR, "statuscheck", "services"))
    excluded_files = (
        "__pycache__",
        "__init__.py",
        "_base.py",
        "_custompage.py",
        "_statuspage.py",
        "_statusio.py",
    )
    service_files = [f[:-3] for f in service_files if f not in excluded_files]
    assert set(services) == set(service_files)


@pytest.mark.parametrize("service", SERVICES)
def test_get_statuscheck_api(service):
    api = get_statuscheck_api(service)
    assert api._module_name == service
    assert api.status_url
    assert api.summary
    print(api.summary)
