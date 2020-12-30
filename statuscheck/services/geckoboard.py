from statuscheck.services.bases._statuspageio import BaseStatusPageAPI


class ServiceAPI(BaseStatusPageAPI):
    name = "Geckoboard"
    domain_id = "pbh1zz50vzz3"
    status_url = "https://geckoboard.statuspage.io/"
    service_url = "https://www.geckoboard.com/"
