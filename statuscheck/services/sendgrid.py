from statuscheck.services.bases._statuspageio import BaseStatusPageAPI


class ServiceAPI(BaseStatusPageAPI):
    name = "SendGrid"
    domain_id = "3tgl2vf85cht"
    status_url = "https://status.sendgrid.com/"
    service_url = "https://sendgrid.com/"
