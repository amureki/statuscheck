from statuscheck.services.bases._statuspageio import BaseStatusPageAPI


class ServiceAPI(BaseStatusPageAPI):
    name = "DNSimple"
    domain_id = "tjym90yyv2zt"
    status_url = "https://dnsimple.statuspage.io/"
    service_url = "https://dnsimple.com/"
