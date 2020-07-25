from statuscheck.services.bases._statuspageio import BaseStatusPageAPI


class ServiceAPI(BaseStatusPageAPI):
    name = "Redis Labs"
    domain_id = "j6ydyp75k0zx"
    status_url = "https://status.redislabs.com/"
    service_url = "https://redislabs.com/"
