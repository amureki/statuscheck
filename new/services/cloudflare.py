from new.services._statuspage import BaseStatusPageAPI


class ServiceAPI(BaseStatusPageAPI):
    name = "Cloudflare"
    domain_id = "yh6f0r4529hb"
    status_url = "https://www.cloudflarestatus.com/"
    service_url = "https://www.cloudflare.com/"
