from statuscheck.services.bases._statuspageio import BaseStatusPageAPI


class ServiceAPI(BaseStatusPageAPI):
    name = "Epic Games"
    domain_id = "ft308v428dv3"
    status_url = "https://status.epicgames.com/"
    service_url = "http://epicgames.com/"
