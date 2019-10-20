from statuscheck.services._statuspage import BaseStatusPageAPI


class ServiceAPI(BaseStatusPageAPI):
    name = "PagerDuty"
    domain_id = "33yy6hwxnwr3"
    status_url = "https://status.pagerduty.com/"
