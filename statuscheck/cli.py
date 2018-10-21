import sys
import click

from statuscheck.check import get_statuscheck_api

COLOR_GREEN = '\033[92m'
COLOR_YELLOW = '\033[93m'
COLOR_RED = '\033[91m'
COLOR_DEFAULT = '\033[99m'

STATUSES_COLORS_MAPPING = {
    '': COLOR_DEFAULT,
    'good': COLOR_GREEN,
    'minor': COLOR_YELLOW,
    'major': COLOR_RED,
    'maintenance': COLOR_DEFAULT,
}


@click.command()
@click.argument('service')
def main(service):
    """Console script for statuscheck."""
    service_api = get_statuscheck_api(service)
    status = service_api.get_status()
    status_type = service_api.get_status_type()
    status_color = STATUSES_COLORS_MAPPING.get(status_type, '')
    click.echo(f'{status_color}{status}')
    return 0


if __name__ == "__main__":
    sys.exit(main())  # pragma: no cover
