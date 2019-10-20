from statuscheck.services._statuspage import BaseStatusPageAPI


class ServiceAPI(BaseStatusPageAPI):
    name = "Twilio"
    domain_id = "gpkpyklzq55q"
    status_url = "https://status.twilio.com"
