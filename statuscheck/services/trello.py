from statuscheck.services.bases._statuspageio import BaseStatusPageAPI


class ServiceAPI(BaseStatusPageAPI):
    name = "Trello"
    domain_id = "h5frqhb041yq"
    status_url = "https://trello.status.atlassian.com/"
    service_url = "https://www.atlassian.com/software/trello"
