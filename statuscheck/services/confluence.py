from statuscheck.services.bases._statuspageio import BaseStatusPageAPI


class ServiceAPI(BaseStatusPageAPI):
    name = "Confluence"
    domain_id = "4g2my7tbhjsq"
    status_url = "https://confluence.status.atlassian.com/"
    service_url = "https://www.atlassian.com/software/confluence"
