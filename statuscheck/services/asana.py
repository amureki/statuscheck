from statuscheck.services.bases._statuspageio import BaseStatusPageAPI


class ServiceAPI(BaseStatusPageAPI):
    name = "Asana"
    domain_id = "w58858w0sjxx"
    service_url = "https://asana.com/"
    status_url = "https://trust.asana.com/"
