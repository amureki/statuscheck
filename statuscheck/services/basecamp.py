from statuscheck.services.bases._statuspageio import BaseStatusPageAPI


class ServiceAPI(BaseStatusPageAPI):
    name = "Basecamp"
    domain_id = "thc30769z1m9"
    status_url = "https://www.basecampstatus.com/"
    service_url = "http://basecamp.com/"
