from statuscheck.services.bases._statuspageio import BaseStatusPageAPI


class ServiceAPI(BaseStatusPageAPI):
    name = "New Relic"
    domain_id = "nwg5xmnm9d17"
    status_url = "https://status.newrelic.com/"
    service_url = "https://newrelic.com/"
