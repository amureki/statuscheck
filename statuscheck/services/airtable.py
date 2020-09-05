from statuscheck.services.bases._statuspageio import BaseStatusPageAPI


class ServiceAPI(BaseStatusPageAPI):
    name = "Airtable"
    domain_id = "5vv477bkm0kl"
    service_url = "https://airtable.com/"
    status_url = "https://status.airtable.com/"
