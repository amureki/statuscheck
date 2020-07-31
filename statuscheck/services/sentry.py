from statuscheck.services.bases._statuspageio import BaseStatusPageAPI


class ServiceAPI(BaseStatusPageAPI):
    name = "Sentry"
    domain_id = "t687h3m0nh65"
    status_url = "https://status.sentry.io"
    service_url = "https://sentry.io/"
