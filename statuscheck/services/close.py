from statuscheck.services.bases._statuspageio import BaseStatusPageAPI


class ServiceAPI(BaseStatusPageAPI):
    name = "Close"
    domain_id = "8vgwlwbg3zbc"
    status_url = "https://status.close.com/"
    service_url = "http://close.com/"
