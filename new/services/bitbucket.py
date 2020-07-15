from new.services._statuspage import BaseStatusPageAPI


class ServiceAPI(BaseStatusPageAPI):
    name = "Bitbucket"
    domain_id = "bqlf8qjztdtr"
    status_url = "https://status.bitbucket.org/"
    service_url = "https://bitbucket.org/"
