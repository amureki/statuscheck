from statuscheck.services._statuspage import BaseStatusPageAPI


class ServiceAPI(BaseStatusPageAPI):
    name = "Atlassian"
    domain_id = "x67gp49yvrzv"
    status_url = "https://status.atlassian.com/"
