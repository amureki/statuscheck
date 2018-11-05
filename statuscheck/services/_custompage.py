from requests_html import HTMLSession

from statuscheck.services._base import BaseServiceAPI


class BaseCustomStatusPageAPI(BaseServiceAPI):
    def _get_html_response(self):
        session = HTMLSession()
        response = session.get(self.base_url)
        response.raise_for_status()
        return response.html
