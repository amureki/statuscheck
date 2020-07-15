from new.services._statuspage import BaseStatusPageAPI


class ServiceAPI(BaseStatusPageAPI):
    name = "npm"
    domain_id = "wyvgptkd90hm"
    status_url = "https://status.npmjs.org/"
    service_url = "https://npmjs.org/"
