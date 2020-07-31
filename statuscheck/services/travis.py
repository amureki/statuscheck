from statuscheck.services.bases._statuspageio import BaseStatusPageAPI


class ServiceAPI(BaseStatusPageAPI):
    name = "Travis CI"
    domain_id = "pnpcptp8xh9k"
    status_url = "https://www.traviscistatus.com/"
    service_url = "https://travis-ci.com/"
