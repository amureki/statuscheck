from statuscheck.services._statusio import BaseStatusioAPI


class ServiceAPI(BaseStatusioAPI):
    name = 'Docker'
    domain_id = '533c6539221ae15e3f000031'
    status_url = 'https://status.docker.com/'
