from statuscheck.services.bases._statuspageio import BaseStatusPageAPI


class ServiceAPI(BaseStatusPageAPI):
    name = "Zoom"
    domain_id = "14qjgk812kgk"
    status_url = "https://status.zoom.us/"
    service_url = "https://zoom.us/"
