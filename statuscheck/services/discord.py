from statuscheck.services._statuspage import BaseStatusPageAPI


class ServiceAPI(BaseStatusPageAPI):
    name = "Discord"
    domain_id = "srhpyqt94yxb"
    status_url = "https://status.discord.com/"
    service_url = "https://discord.com"
