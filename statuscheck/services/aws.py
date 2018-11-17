import feedparser

from statuscheck.exceptions import StatusCheckMissingArgumentsError, StatusCheckParsingError
from statuscheck.services._base import BaseServiceAPI
from statuscheck.status_types import TYPE_INCIDENT, TYPE_OUTAGE, TYPE_GOOD, TYPE_UNKNOWN


class ServiceAPI(BaseServiceAPI):
    base_url = 'https://status.aws.amazon.com/'
    status_url = base_url
    requires_extra_args = True

    def _raise_extra_args_error(self):
        raise StatusCheckMissingArgumentsError(
            f'{self._module_name} is missing service and region data to check.\n'
            f'Examples: \n'
            f'CLI: statuscheck aws -e s3 eu-west-1\n'
            f'API: get_statuscheck_api("aws", ("s3", "eu-west-1"))'
        )

    def _get_status_data(self):
        requested_feed = '-'.join(self.extra_args)
        parsed = feedparser.parse(self.base_url + 'rss/' + requested_feed + '.rss')
        if parsed.status != 200:
            raise StatusCheckParsingError(f'Could not parse status data for {self._module_name}')
        if parsed.entries:
            return parsed.entries[0]
        if parsed.get('feed', {}).get('title'):
            return {'title': 'Service is operating normally'}
        raise StatusCheckParsingError(f'Could not parse status data for {self._module_name}')

    def get_status(self):
        return self.get_type()

    def get_type(self):
        if not self.data:
            self.data = self._get_status_data()
        title = self.data['title']
        description = self.data.get('description', '')
        if any([
            title.startswith('Service is operating normally'),
            '[RESOLVED]' in title.upper(),
            'operating normally' in description,
        ]):
            return TYPE_GOOD

        if any([
            title.startswith('Informational message'),
            title.startswith('Performance issues')
        ]):
            return TYPE_INCIDENT

        if title.startswith('Service disruption'):
            return TYPE_OUTAGE

        return TYPE_UNKNOWN

    def get_active_incident(self):
        status_type = self.get_type()
        if status_type == TYPE_GOOD:
            return ''
        return self.data['title']
