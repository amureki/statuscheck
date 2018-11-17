import importlib

from statuscheck.services import SERVICES


def _import_module(service):
    return importlib.import_module(f'statuscheck.services.{service}')


def get_statuscheck_api(service, extra_args=None):
    module = _import_module(service)
    return module.ServiceAPI(extra_args)


def get_available_services():
    return SERVICES
