from new.services._statuspage import BaseStatusPageAPI


class ServiceAPI(BaseStatusPageAPI):
    name = "Redis Labs"
    domain_id = "j6ydyp75k0zx"
    status_url = "https://status.redislabs.com/"
    service_url = "https://redislabs.com/"
