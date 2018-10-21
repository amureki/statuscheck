import importlib


def _import_module(service):
    return importlib.import_module(f'statuscheck.services.{service}')


def get_statuscheck_api(service):
    module = _import_module(service)
    return module.ServiceAPI()
