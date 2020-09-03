from statuscheck.services.bases._statuspageio import BaseStatusPageAPI


class ServiceAPI(BaseStatusPageAPI):
    name = "Vercel"
    domain_id = "lvglq8h0mdyh"
    status_url = "https://www.vercel-status.com/"
    service_url = "https://vercel.com/"
