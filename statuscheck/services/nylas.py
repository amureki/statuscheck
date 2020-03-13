from statuscheck.services._statuspage import BaseStatusPageAPI


class ServiceAPI(BaseStatusPageAPI):
    name = "Nylas"
    domain_id = "ltnt5xstwgqp"
    status_url = "https://status.nylas.com/"
