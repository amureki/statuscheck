from statuscheck.services._statuspage import BaseStatusPageAPI


class ServiceAPI(BaseStatusPageAPI):
    name = "Codecov"
    domain_id = "wdzsn5dlywj9"
    status_url = "https://status.codecov.io/"
