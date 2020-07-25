from statuscheck.services.bases._statuspageio import BaseStatusPageAPI


class ServiceAPI(BaseStatusPageAPI):
    name = "CloudAMQP"
    domain_id = "2126xm8ctzlk"
    status_url = "https://status.cloudamqp.com/"
    service_url = "https://cloudamqp.com/"
