from statuscheck.services._statuspage import BaseStatusPageAPI


class ServiceAPI(BaseStatusPageAPI):
    name = "Sentry"
    domain_id = "t687h3m0nh65"
    status_url = "https://status.sentry.io"
