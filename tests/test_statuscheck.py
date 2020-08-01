import os

import pytest

from statuscheck.services import SERVICES
from statuscheck.utils import get_available_services, get_statuscheck_api

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


def test_get_available_services():
    services = get_available_services()
    assert services

    services_dir = os.path.join(BASE_DIR, "statuscheck", "services")
    service_files = os.listdir(services_dir)
    excluded_files = (
        "__pycache__",
        "__init__.py",
        "_base.py",
        "_custompage.py",
        "_statuspage.py",
        "_statusio.py",
    )
    service_files = [
        f[:-3]
        for f in service_files
        if f not in excluded_files and os.path.isfile(os.path.join(services_dir, f))
    ]
    assert set(services) == set(service_files)


@pytest.mark.parametrize("service", SERVICES)
def test_get_statuscheck_api(service):
    api = get_statuscheck_api(service)
    assert api._module_name == service
    assert api.status_url
    assert api.service_url
    assert api.summary
    assert api.summary.as_dict()
