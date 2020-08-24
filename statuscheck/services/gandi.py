from statuscheck.services.bases._statuspageio import BaseStatusPageAPI


class ServiceAPI(BaseStatusPageAPI):
    name = "Gandi"
    domain_id = "14qjgk812kgk"
    status_url = "https://status.gandi.net/"
    service_url = "https://gandi.net/"
