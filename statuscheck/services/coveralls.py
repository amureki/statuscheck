from statuscheck.services.bases._statuspageio import BaseStatusPageAPI


class ServiceAPI(BaseStatusPageAPI):
    name = "Coveralls"
    domain_id = "3h72wtpg5fqs"
    status_url = "https://status.coveralls.io/"
    service_url = "https://coveralls.io/"
