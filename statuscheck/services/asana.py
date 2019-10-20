from statuscheck.services._statuspage import BaseStatusPageAPI


class ServiceAPI(BaseStatusPageAPI):
    name = "Asana"
    domain_id = "w58858w0sjxx"
    status_url = "https://trust.asana.com/"
