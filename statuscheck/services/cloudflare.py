from statuscheck.services.bases._statuspageio import BaseStatusPageAPI


class ServiceAPI(BaseStatusPageAPI):
    name = "Cloudflare"
    domain_id = "yh6f0r4529hb"
    status_url = "https://www.cloudflarestatus.com/"
    service_url = "https://www.cloudflare.com/"
