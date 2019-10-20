from statuscheck.services._statuspage import BaseStatusPageAPI


class ServiceAPI(BaseStatusPageAPI):
    name = "CircleCI"
    domain_id = "6w4r0ttlx5ft"
    status_url = "https://circleci.statuspage.io/"
