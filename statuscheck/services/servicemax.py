from statuscheck.services.bases._statuspageio import BaseStatusPageAPI


class ServiceAPI(BaseStatusPageAPI):
    name = "ServiceMax"
    domain_id = "jtvt0b51c5wy"
    status_url = "https://servicemax.statuspage.io/"
    service_url = "https://www.servicemax.com/"
