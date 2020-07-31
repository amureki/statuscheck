from statuscheck.services.bases._statuspageio import BaseStatusPageAPI


class ServiceAPI(BaseStatusPageAPI):
    name = "Mailgun"
    domain_id = "6jp439mdyy0k"
    status_url = "https://status.mailgun.com/"
    service_url = "https://mailgun.com/"
