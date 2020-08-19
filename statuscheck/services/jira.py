from statuscheck.services.bases._statuspageio import BaseStatusPageAPI


class ServiceAPI(BaseStatusPageAPI):
    name = "Jira"
    domain_id = "7yh3h3y0c0x1"
    status_url = "https://jira-software.status.atlassian.com/"
    service_url = "https://www.atlassian.com/software/jira"
