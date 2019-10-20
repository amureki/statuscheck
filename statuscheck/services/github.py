from statuscheck.services._statuspage import BaseStatusPageAPI


class ServiceAPI(BaseStatusPageAPI):
    name = "GitHub"
    domain_id = "kctbh9vrtdwd"
    status_url = "https://www.githubstatus.com/"
