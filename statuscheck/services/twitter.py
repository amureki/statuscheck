from statuscheck.services.bases._statuspageio import BaseStatusPageAPI


class ServiceAPI(BaseStatusPageAPI):
    name = "Twitter API"
    domain_id = "zjttvm6ql9lp"
    status_url = "https://api.twitterstat.us/"
    service_url = "https://twitter.com/"
