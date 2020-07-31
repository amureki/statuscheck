from statuscheck.services.bases._statuspageio import BaseStatusPageAPI


class ServiceAPI(BaseStatusPageAPI):
    name = "Bitbucket"
    domain_id = "bqlf8qjztdtr"
    status_url = "https://status.bitbucket.org/"
    service_url = "https://bitbucket.org/"
