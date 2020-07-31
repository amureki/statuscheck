from statuscheck.services.bases._statuspageio import BaseStatusPageAPI


class ServiceAPI(BaseStatusPageAPI):
    name = "PyPI"
    domain_id = "2p66nmmycsj3"
    status_url = "https://status.python.org/"
    service_url = "https://pypi.org/"
