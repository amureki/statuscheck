from statuscheck.services._statuspage import BaseStatusPageAPI


class ServiceAPI(BaseStatusPageAPI):
    name = "InVision"
    domain_id = "tv3rvsrmny3p"
    status_url = "https://status.invisionapp.com/"
