import os

import pytest

from statuscheck.check import get_available_services, get_statuscheck_api
from statuscheck.services import SERVICES

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


def test_get_available_services():
    services = get_available_services()
    assert services

    service_files = os.listdir(os.path.join(BASE_DIR, 'statuscheck', 'services'))
    service_files = [f[:-3] for f in service_files if
                     f not in ('__pycache__', '__init__.py', '_base.py', '_statuspage.py')]
    assert set(services) == set(service_files)


@pytest.mark.parametrize('service', SERVICES)
def test_get_statuscheck_api(service):
    api = get_statuscheck_api(service)
    assert api.data == {}
    assert api.status_url
