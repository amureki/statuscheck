from statuscheck.services.bases._statuspageio import BaseStatusPageAPI


class ServiceAPI(BaseStatusPageAPI):
    name = "OwnBackup"
    domain_id = "99zkjtqfrc1m"
    status_url = "https://status.ownbackup.com/"
    service_url = "https://www.ownbackup.com/"
