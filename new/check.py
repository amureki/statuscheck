import importlib
from new.services import SERVICES


def _import_module(service):
    return importlib.import_module(f"new.services.{service}")


def get_statuscheck_api(service):
    module = _import_module(service)
    return module.ServiceAPI()


def get_available_services():
    return SERVICES
