from statuscheck.services.bases._statusio import BaseStatusIOAPI


class ServiceAPI(BaseStatusIOAPI):
    name = "GitLab"
    domain_id = "5b36dc6502d06804c08349f7"
    status_url = "https://status.gitlab.com/"
    service_url = "https://gitlab.com/"
