from statuscheck.services.bases._statuspageio import BaseStatusPageAPI


class ServiceAPI(BaseStatusPageAPI):
    name = "Nylas"
    domain_id = "ltnt5xstwgqp"
    status_url = "https://status.nylas.com/"
    service_url = "https://nylas.com/"
