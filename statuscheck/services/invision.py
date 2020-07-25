from statuscheck.services.bases._statuspageio import BaseStatusPageAPI


class ServiceAPI(BaseStatusPageAPI):
    name = "InVision"
    domain_id = "tv3rvsrmny3p"
    status_url = "https://status.invisionapp.com/"
    service_url = "https://invisionapp.com/"
