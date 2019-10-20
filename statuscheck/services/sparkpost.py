from statuscheck.services._statuspage import BaseStatusPageAPI


class ServiceAPI(BaseStatusPageAPI):
    name = "SparkPost"
    domain_id = "7ky1q6zd3fyp"
    status_url = "https://status.sparkpost.com/"
