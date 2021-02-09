from statuscheck.services.bases._statuspageio import BaseStatusPageAPI


class ServiceAPI(BaseStatusPageAPI):
    name = "Clubhouse"
    domain_id = "27fcn0qntr9w"
    status_url = "https://status.clubhouse.io/"
    service_url = "https://clubhouse.io/"
