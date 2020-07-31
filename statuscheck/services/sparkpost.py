from statuscheck.services.bases._statuspageio import BaseStatusPageAPI


class ServiceAPI(BaseStatusPageAPI):
    name = "SparkPost"
    domain_id = "7ky1q6zd3fyp"
    status_url = "https://status.sparkpost.com/"
    service_url = "https://sparkpost.com/"
