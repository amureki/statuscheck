from statuscheck.services.bases._statuspageio import BaseStatusPageAPI


class ServiceAPI(BaseStatusPageAPI):
    name = "GitHub"
    domain_id = "kctbh9vrtdwd"
    status_url = "https://www.githubstatus.com/"
    service_url = "https://www.github.com/"
