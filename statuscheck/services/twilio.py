from statuscheck.services.bases._statuspageio import BaseStatusPageAPI


class ServiceAPI(BaseStatusPageAPI):
    name = "Twilio"
    domain_id = "gpkpyklzq55q"
    status_url = "https://status.twilio.com"
    service_url = "https://twilio.com/"
