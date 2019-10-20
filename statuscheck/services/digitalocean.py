from statuscheck.services._statuspage import BaseStatusPageAPI


class ServiceAPI(BaseStatusPageAPI):
    name = "DigitalOcean"
    domain_id = "s2k7tnzlhrpw"
    status_url = "https://status.digitalocean.com/"
