from statuscheck.services.bases._statuspageio import BaseStatusPageAPI


class ServiceAPI(BaseStatusPageAPI):
    name = "PagerDuty"
    domain_id = "33yy6hwxnwr3"
    status_url = "https://status.pagerduty.com/"
    service_url = "https://pagerduty.com/"
