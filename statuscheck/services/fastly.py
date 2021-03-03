from statuscheck.services.bases._statuspageio import BaseStatusPageAPI


class ServiceAPI(BaseStatusPageAPI):
    name = "Fastly"
    domain_id = "889dh1w1xtt0"
    status_url = "https://status.fastly.com/"
    service_url = "https://fastly.com/"
