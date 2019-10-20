from statuscheck.services._statusio import BaseStatusIOAPI


class ServiceAPI(BaseStatusIOAPI):
    name = "Docker"
    domain_id = "533c6539221ae15e3f000031"
    status_url = "https://status.docker.com/"
