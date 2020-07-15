from new.services._statuspage import BaseStatusPageAPI


class ServiceAPI(BaseStatusPageAPI):
    name = "GitHub"
    domain_id = "kctbh9vrtdwd"
    status_url = "https://www.githubstatus.com/"
    service_url = "https://www.github.com/"
