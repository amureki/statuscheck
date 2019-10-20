from statuscheck.services._statuspage import BaseStatusPageAPI


class ServiceAPI(BaseStatusPageAPI):
    name = "Personio"
    domain_id = "68kf6yfjnk2d"
    status_url = "https://status.personio.de/"
